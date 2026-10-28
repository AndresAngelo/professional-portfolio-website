"""Constrained adapter for running an already-authorized PowerShell command."""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True)
class CommandResult:
    """Captured, non-interactive command outcome."""

    stdout: str
    stderr: str
    exit_code: int


class ProcessRunner(Protocol):
    """Minimal subprocess seam used to keep validation tests process-free."""

    def run(
        self, *, argv: list[str], cwd: Path, environment: dict[str, str]
    ) -> CommandResult: ...


class SubprocessRunner:
    """Production implementation of the constrained subprocess seam."""

    def run(
        self, *, argv: list[str], cwd: Path, environment: dict[str, str]
    ) -> CommandResult:
        completed = subprocess.run(
            argv,
            cwd=cwd,
            env=environment,
            capture_output=True,
            check=False,
            text=True,
        )
        return CommandResult(
            stdout=completed.stdout, stderr=completed.stderr, exit_code=completed.returncode
        )


class PowerShellRunner:
    """Run commands with no profile and a minimal inherited environment."""

    def __init__(self, *, process_runner: ProcessRunner, workspace: Path) -> None:
        self._process_runner = process_runner
        self._workspace = workspace.resolve()

    def run(self, command: str) -> CommandResult:
        """Run a pre-authorized command at the canonical workspace root."""
        environment = {"PATH": os.environ.get("PATH", "")}
        return self._process_runner.run(
            argv=["powershell", "-NoProfile", "-NonInteractive", "-Command", command],
            cwd=self._workspace,
            environment=environment,
        )
