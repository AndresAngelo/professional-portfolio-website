"""Immutable, workspace-contained runtime configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
import tomllib


class ConfigurationError(ValueError):
    """Raised when runtime configuration would violate a safety boundary."""


@dataclass(frozen=True)
class WorkspaceConfig:
    root: Path
    spec_root: Path
    local_storage: Path


@dataclass(frozen=True)
class DiscoveryConfig:
    enabled_milestones: tuple[int, ...]
    future_milestones: tuple[int, ...]
    goal_glob: str
    required_goal_numbers: tuple[int, ...]


@dataclass(frozen=True)
class LegacyInstructionMigrationConfig:
    accepted_root_aliases: tuple[Path, ...]
    tracker_path: Path
    tracker_mode: str


@dataclass(frozen=True)
class LmStudioConfig:
    base_url: str
    model_id: str
    request_timeout_seconds: int
    allow_loopback_only: bool


@dataclass(frozen=True)
class ContextConfig:
    max_total_bytes: int
    max_file_bytes: int
    max_active_files: int
    rules_path: Path
    architecture_path: Path


@dataclass(frozen=True)
class RetryConfig:
    max_error_mode_requests: int


@dataclass(frozen=True)
class LowVramConfig:
    benchmark_enabled: bool
    requested_flash_attention: str
    requested_unified_kv: str
    requested_kv_cache_type: str
    requested_kv_offload: str
    requested_gpu_offload_layers: str


@dataclass(frozen=True)
class OrchestratorConfig:
    workspace: WorkspaceConfig
    discovery: DiscoveryConfig
    legacy_instruction_migration: LegacyInstructionMigrationConfig
    lm_studio: LmStudioConfig
    context: ContextConfig
    retry: RetryConfig
    low_vram: LowVramConfig


def _resolve_under(root: Path, raw_path: str, *, name: str) -> Path:
    candidate = Path(raw_path)
    resolved = candidate.resolve() if candidate.is_absolute() else (root / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as error:
        raise ConfigurationError(f"{name} must remain inside the workspace") from error
    return resolved


def _require_numbers(value: object, expected: tuple[int, ...], name: str) -> tuple[int, ...]:
    result = tuple(int(item) for item in value if isinstance(item, int)) if isinstance(value, list) else ()
    if result != expected:
        raise ConfigurationError(f"{name} must be {expected}")
    return result


def _validate_loopback(base_url: str, loopback_only: bool) -> None:
    parsed = urlparse(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ConfigurationError("LM Studio base URL must be a valid loopback URL")
    if loopback_only and parsed.hostname not in {"127.0.0.1", "localhost"}:
        raise ConfigurationError("LM Studio base URL must use an allowed loopback host")


def load_configuration(config_path: Path) -> OrchestratorConfig:
    """Load and validate the sole runtime authority without creating external paths."""
    try:
        raw = tomllib.loads(config_path.read_text(encoding="utf-8"))
        workspace_raw = raw["workspace"]
        discovery_raw = raw["discovery"]
        legacy_raw = raw["legacy_instruction_migration"]
        lm_raw = raw["lm_studio"]
        context_raw = raw["context"]
        retry_raw = raw["retry"]
        low_vram_raw = raw["low_vram"]
    except (OSError, KeyError, tomllib.TOMLDecodeError) as error:
        raise ConfigurationError(f"Unable to read configuration: {error}") from error

    root = Path(str(workspace_raw["root"])).resolve()
    if not root.is_dir():
        raise ConfigurationError("workspace root must be an existing directory")
    storage = _resolve_under(root, str(workspace_raw["local_storage"]), name="local storage")
    spec_root = _resolve_under(root, str(workspace_raw["spec_root"]), name="spec root")
    enabled = _require_numbers(discovery_raw["enabled_milestones"], (1, 2, 3, 4, 5), "enabled milestones")
    future = _require_numbers(discovery_raw["future_milestones"], (6, 7, 8, 9, 10), "future milestones")
    goals = _require_numbers(discovery_raw["required_goal_numbers"], tuple(range(1, 11)), "required goal numbers")
    if set(enabled) & set(future):
        raise ConfigurationError("enabled and future milestones must not overlap")
    allow_loopback_only = bool(lm_raw["allow_loopback_only"])
    base_url = str(lm_raw["base_url"])
    _validate_loopback(base_url, allow_loopback_only)
    model_id = str(lm_raw["model_id"])
    if model_id != "yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF":
        raise ConfigurationError("LM Studio model identifier is fixed")
    timeout = int(lm_raw["request_timeout_seconds"])
    total, per_file, active = int(context_raw["max_total_bytes"]), int(context_raw["max_file_bytes"]), int(context_raw["max_active_files"])
    if min(timeout, total, per_file, active) < 1 or per_file > total:
        raise ConfigurationError("timeout and context limits must be positive and coherent")
    retries = int(retry_raw["max_error_mode_requests"])
    if retries != 3:
        raise ConfigurationError("max error-mode requests must be exactly three")
    return OrchestratorConfig(
        workspace=WorkspaceConfig(root, spec_root, storage),
        discovery=DiscoveryConfig(enabled, future, str(discovery_raw["goal_glob"]), goals),
        legacy_instruction_migration=LegacyInstructionMigrationConfig(
            tuple(_resolve_under(root, str(alias), name="legacy root alias") for alias in legacy_raw["accepted_root_aliases"]),
            _resolve_under(root, str(legacy_raw["tracker_path"]), name="tracker path"), str(legacy_raw["tracker_mode"])),
        lm_studio=LmStudioConfig(base_url, model_id, timeout, allow_loopback_only),
        context=ContextConfig(total, per_file, active, _resolve_under(root, str(context_raw["rules_path"]), name="rules path"), _resolve_under(root, str(context_raw["architecture_path"]), name="architecture path")),
        retry=RetryConfig(retries),
        low_vram=LowVramConfig(**low_vram_raw),
    )


_ARTIFACT_DIRECTORIES = {"state": "program-states", "plan": "plans", "protocol": "protocol-records", "telemetry": "telemetry", "validation": "validation", "quarantine": "quarantine"}


def derive_artifact_path(*, workspace: Path, artifact_kind: str, task_id: str, relative_name: str) -> Path:
    """Derive a validated storage path; hostile components are rejected, never rewritten."""
    if artifact_kind not in _ARTIFACT_DIRECTORIES:
        raise ValueError(f"Unknown artifact kind: {artifact_kind}")
    root = workspace.resolve()
    storage = (root / "local-ai").resolve()
    name = Path(relative_name)
    if name.is_absolute() or ".." in name.parts or "\\" in relative_name:
        raise ValueError("Artifact name must be a safe relative POSIX path")
    safe_task_id = task_id.replace(".", "_")
    if not safe_task_id or any(character not in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-" for character in safe_task_id):
        raise ValueError("Invalid task identifier for artifact path")
    candidate = storage / _ARTIFACT_DIRECTORIES[artifact_kind] / safe_task_id / name
    resolved = candidate.resolve()
    try:
        resolved.relative_to(storage)
    except ValueError as error:
        raise ValueError("Artifact path escapes local storage") from error
    return resolved
