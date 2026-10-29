"""Ports and safe composition helpers for orchestrator commands.

The command surface depends on this module rather than constructing adapters at import
or argument-parsing time.  Tests can therefore supply explicit in-memory ports, and
real local adapters are created only after a user invokes a command.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import urlparse

from .config import LOOPBACK_HOST, ConfigurationError, OrchestratorConfig, load_configuration
from .discovery import discover_goal_files
from .models import RunState
from .state_store import AtomicStateStore, StateLoadError


class ModelClient(Protocol):
    def request(self, payload: dict[str, Any]) -> Any: ...
    def capabilities(self) -> Any: ...
    def runtime_capabilities(self) -> Any: ...


class StateStore(Protocol):
    def load(self) -> RunState: ...
    def commit(self, state: RunState) -> None: ...
    def write_json_artifact(self, relative_path: str, value: dict[str, Any]) -> str: ...


class CommandRunner(Protocol):
    def run_powershell(self, command: str, cwd: Path) -> Any: ...


class Clock(Protocol):
    def now(self) -> str: ...


@dataclass(frozen=True)
class SafetyChecks:
    """Preflight predicates kept separate from command implementation."""

    configuration_safe: Callable[[], bool]
    state_safe: Callable[[], bool]
    loopback_safe: Callable[[], bool]
    capabilities_safe: Callable[[], bool]


class LocalCommandService:
    """Compose config-backed, local-only command dependencies.

    This small service deliberately provides discovery only.  Executing a task needs
    configured model and process ports supplied by the application host; it never
    fabricates a network or PowerShell adapter on its own.
    """

    def __init__(self, config: OrchestratorConfig) -> None:
        self.config = config
        self.store = AtomicStateStore(
            workspace=config.workspace.root,
            workspace_id=str(config.workspace.root),
            schema_version=2,
        )
        self.pilot_procedure_path = config.workspace.local_storage / "context" / "pilot-procedure.md"

    def discover(self) -> int:
        return len(discover_goal_files(self.config))

    def run_once(self, *, resume: bool, task_limit: int) -> None:
        del resume, task_limit
        raise RuntimeError("task execution requires explicitly composed local model and process ports")

    def benchmark(self) -> None:
        raise RuntimeError("benchmark execution requires an explicitly composed local model adapter")

    def safety_checks(self) -> SafetyChecks:
        return SafetyChecks(
            configuration_safe=self._configuration_is_safe,
            state_safe=self._state_is_safe,
            loopback_safe=self._loopback_is_safe,
            capabilities_safe=lambda: True,
        )

    def _configuration_is_safe(self) -> bool:
        """Require the checked-in pilot procedure as part of CLI composition."""
        try:
            return self.pilot_procedure_path.is_file() and bool(
                self.pilot_procedure_path.read_text(encoding="utf-8").strip()
            )
        except OSError:
            return False

    def _state_is_safe(self) -> bool:
        # Missing state is safe for discovery but not for execution selection.
        if not self.store.state_path.exists():
            return False
        try:
            self.store.load()
        except StateLoadError:
            return False
        return True

    def _loopback_is_safe(self) -> bool:
        parsed = urlparse(self.config.lm_studio.base_url)
        return self.config.lm_studio.allow_loopback_only and parsed.hostname == LOOPBACK_HOST


def compose_local_command_service(config_path: Path) -> LocalCommandService:
    """Load validated configuration without contacting LM Studio or starting processes."""
    try:
        config = load_configuration(config_path)
    except ConfigurationError:
        raise
    return LocalCommandService(config)
