"""Immutable, workspace-contained runtime configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal
from urllib.parse import urlparse
import tomllib


class ConfigurationError(ValueError):
    """Raised when runtime configuration would violate a safety boundary."""


LOOPBACK_HOST = "127.0.0.1"
ModelRoleName = Literal["embedding", "router", "executor"]
MODEL_ROLE_NAMES: tuple[ModelRoleName, ...] = ("embedding", "router", "executor")
# The pinned single-model identifier is retired. It is rejected as a role binding and never routed.
RETIRED_MODEL_IDS: frozenset[str] = frozenset(
    {"yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF"}
)
# Planning estimate of UTF-8 prompt bytes per token. It is not a tokenizer measurement.
BYTES_PER_TOKEN = 4
_MODEL_ROLE_KEYS = frozenset({"model_id", "context_length", "output_reserve_tokens", "max_prompt_bytes"})
DEFAULT_MIN_HEADROOM_MB = 700


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
class ModelRole:
    """One LM Studio model binding with its context cap and prompt byte budget."""

    model_id: str
    context_length: int
    output_reserve_tokens: int
    max_prompt_bytes: int


@dataclass(frozen=True)
class ModelRoles:
    """The three LM Studio model bindings used by the mesh."""

    embedding: ModelRole
    router: ModelRole
    executor: ModelRole

    def for_role(self, role: ModelRoleName) -> ModelRole:
        bindings = {"embedding": self.embedding, "router": self.router, "executor": self.executor}
        return bindings[role]


@dataclass(frozen=True)
class LmStudioConfig:
    base_url: str
    request_timeout_seconds: int
    allow_loopback_only: bool
    models: ModelRoles


@dataclass(frozen=True)
class ContextConfig:
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
class VramConfig:
    """GPU memory that must stay free after the mesh is loaded, in MiB."""

    min_headroom_mb: int

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> VramConfig:
        section = raw.get("vram", {})
        if not isinstance(section, dict):
            raise ConfigurationError("[vram] must be a table")
        headroom = section.get("min_headroom_mb", DEFAULT_MIN_HEADROOM_MB)
        if not _is_positive_int(headroom):
            raise ConfigurationError("[vram] min_headroom_mb must be a positive integer")
        return cls(min_headroom_mb=headroom)


@dataclass(frozen=True)
class OrchestratorConfig:
    workspace: WorkspaceConfig
    discovery: DiscoveryConfig
    legacy_instruction_migration: LegacyInstructionMigrationConfig
    lm_studio: LmStudioConfig
    context: ContextConfig
    retry: RetryConfig
    low_vram: LowVramConfig
    vram: VramConfig


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
    if not loopback_only:
        raise ConfigurationError("LM Studio allow_loopback_only must be true; remote endpoints are not supported")
    if parsed.hostname != LOOPBACK_HOST:
        raise ConfigurationError(f"LM Studio base URL must use the loopback host {LOOPBACK_HOST}")


def _is_positive_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 1


def _is_non_negative_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _parse_model_role(role_name: str, raw: object) -> ModelRole:
    if not isinstance(raw, dict) or set(raw) != _MODEL_ROLE_KEYS:
        raise ConfigurationError(
            f"model role {role_name!r} must define exactly model_id, context_length, "
            "output_reserve_tokens, and max_prompt_bytes"
        )
    model_id = raw["model_id"]
    context_length = raw["context_length"]
    output_reserve = raw["output_reserve_tokens"]
    prompt_budget = raw["max_prompt_bytes"]
    if not isinstance(model_id, str) or not model_id or model_id != model_id.strip():
        raise ConfigurationError(f"model role {role_name!r} needs a non-empty model_id without surrounding spaces")
    if model_id in RETIRED_MODEL_IDS:
        raise ConfigurationError(f"model role {role_name!r} uses the retired pinned model identifier")
    if not _is_positive_int(context_length):
        raise ConfigurationError(f"model role {role_name!r} needs a positive integer context_length")
    if not _is_non_negative_int(output_reserve) or output_reserve >= context_length:
        raise ConfigurationError(
            f"model role {role_name!r} needs output_reserve_tokens from 0 up to, but not including, context_length"
        )
    capacity = (context_length - output_reserve) * BYTES_PER_TOKEN
    if not _is_positive_int(prompt_budget) or prompt_budget > capacity:
        raise ConfigurationError(
            f"model role {role_name!r} needs max_prompt_bytes from 1 to {capacity} "
            f"((context_length - output_reserve_tokens) x {BYTES_PER_TOKEN})"
        )
    return ModelRole(
        model_id=model_id,
        context_length=context_length,
        output_reserve_tokens=output_reserve,
        max_prompt_bytes=prompt_budget,
    )


def _parse_model_roles(lm_raw: dict[str, Any]) -> ModelRoles:
    if "model_id" in lm_raw:
        raise ConfigurationError(
            "single [lm_studio] model_id is retired; define [lm_studio.models.embedding], "
            "[lm_studio.models.router], and [lm_studio.models.executor] instead"
        )
    models_raw = lm_raw.get("models")
    if not isinstance(models_raw, dict) or set(models_raw) != set(MODEL_ROLE_NAMES):
        raise ConfigurationError("[lm_studio.models] must define exactly the roles embedding, router, and executor")
    roles = {name: _parse_model_role(name, models_raw[name]) for name in MODEL_ROLE_NAMES}
    identifiers = [role.model_id for role in roles.values()]
    if len(set(identifiers)) != len(identifiers):
        raise ConfigurationError("model roles must use three distinct model identifiers")
    return ModelRoles(embedding=roles["embedding"], router=roles["router"], executor=roles["executor"])


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
    model_roles = _parse_model_roles(lm_raw)
    timeout = int(lm_raw["request_timeout_seconds"])
    if "max_total_bytes" in context_raw:
        raise ConfigurationError("[context] max_total_bytes is retired; set max_prompt_bytes on each model role")
    per_file, active = int(context_raw["max_file_bytes"]), int(context_raw["max_active_files"])
    if min(timeout, per_file, active) < 1:
        raise ConfigurationError("timeout and context limits must be positive")
    retries = int(retry_raw["max_error_mode_requests"])
    if retries != 3:
        raise ConfigurationError("max error-mode requests must be exactly three")
    return OrchestratorConfig(
        workspace=WorkspaceConfig(root, spec_root, storage),
        discovery=DiscoveryConfig(enabled, future, str(discovery_raw["goal_glob"]), goals),
        legacy_instruction_migration=LegacyInstructionMigrationConfig(
            tuple(_resolve_under(root, str(alias), name="legacy root alias") for alias in legacy_raw["accepted_root_aliases"]),
            _resolve_under(root, str(legacy_raw["tracker_path"]), name="tracker path"), str(legacy_raw["tracker_mode"])),
        lm_studio=LmStudioConfig(
            base_url=base_url,
            request_timeout_seconds=timeout,
            allow_loopback_only=allow_loopback_only,
            models=model_roles,
        ),
        context=ContextConfig(per_file, active, _resolve_under(root, str(context_raw["rules_path"]), name="rules path"), _resolve_under(root, str(context_raw["architecture_path"]), name="architecture path")),
        retry=RetryConfig(retries),
        low_vram=LowVramConfig(**low_vram_raw),
        vram=VramConfig.from_raw(raw),
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
