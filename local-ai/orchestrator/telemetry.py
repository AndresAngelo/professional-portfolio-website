"""Capability-gated low-VRAM decisions and workspace-local benchmark telemetry."""

from __future__ import annotations

import json
import os
from collections.abc import Iterator, Mapping
from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any

from .config import LowVramConfig


class CapabilityState(StrEnum):
    """Runtime support reported by LM Studio, without inferring unavailable data."""

    SUPPORTED = "supported"
    UNSUPPORTED = "unsupported"
    NOT_REPORTED = "not-reported"


@dataclass(frozen=True)
class LowVramApplication(Mapping[str, dict[str, str]]):
    """Confirmed low-VRAM application results for a benchmark request."""

    configured_values: dict[str, str]
    statuses: dict[str, str]

    def __getitem__(self, key: str) -> dict[str, str]:
        status = self.statuses[key]
        result = {"status": status}
        if status == "applied":
            result["value"] = self.configured_values[key]
        return result

    def __iter__(self) -> Iterator[str]:
        return iter(self.statuses)

    def __len__(self) -> int:
        return len(self.statuses)


class LowVramCapabilityGate:
    """Resolve requested settings only when support and effective values agree."""

    _SETTING_NAMES = (
        "flash_attention",
        "unified_kv",
        "kv_cache_type",
        "kv_offload",
        "gpu_offload_layers",
    )

    def __init__(self, config_or_capabilities: LowVramConfig | Mapping[str, Any]) -> None:
        self._config = config_or_capabilities if isinstance(config_or_capabilities, LowVramConfig) else None
        self._capabilities = (
            None if self._config is not None else self.normalize_capabilities(config_or_capabilities)
        )

    @classmethod
    def setting_names(cls) -> tuple[str, ...]:
        return cls._SETTING_NAMES

    @classmethod
    def normalize_capabilities(cls, reported: Mapping[str, Any]) -> dict[str, CapabilityState]:
        """Treat only explicit boolean runtime values as capability assertions."""
        return {
            name: (
                CapabilityState.SUPPORTED
                if reported.get(name) is True
                else CapabilityState.UNSUPPORTED
                if reported.get(name) is False
                else CapabilityState.NOT_REPORTED
            )
            for name in cls._SETTING_NAMES
        }

    def apply(
        self,
        *,
        capabilities: Mapping[str, CapabilityState | str] | None = None,
        effective_values: Mapping[str, Any] | None = None,
        requested: Mapping[str, str] | None = None,
        effective_settings: Mapping[str, Any] | None = None,
    ) -> LowVramApplication:
        """Return only settings the runtime both supports and confirms effective.

        This method is a decision boundary.  It never sends a runtime setting change.
        """
        if capabilities is None:
            if self._capabilities is None:
                raise ValueError("runtime capabilities are required")
            normalized = self._capabilities
        else:
            normalized = {
                name: CapabilityState(capabilities.get(name, CapabilityState.NOT_REPORTED))
                for name in self._SETTING_NAMES
            }
        if requested is None:
            if self._config is None:
                raise ValueError("requested settings are required")
            requested = {
                "flash_attention": self._config.requested_flash_attention,
                "unified_kv": self._config.requested_unified_kv,
                "kv_cache_type": self._config.requested_kv_cache_type,
                "kv_offload": self._config.requested_kv_offload,
                "gpu_offload_layers": self._config.requested_gpu_offload_layers,
            }
        effective = effective_values if effective_values is not None else effective_settings or {}
        configured: dict[str, str] = {}
        statuses: dict[str, str] = {}
        for name in self._SETTING_NAMES:
            state = normalized[name]
            if state is not CapabilityState.SUPPORTED:
                statuses[name] = state.value
                continue
            value = requested[name]
            if effective.get(name) == value:
                configured[name] = value
                statuses[name] = "applied"
            else:
                statuses[name] = "default"
        return LowVramApplication(configured_values=configured, statuses=statuses)


class TelemetryWriter:
    """Append benchmark evidence beneath workspace-local ``local-ai/telemetry`` only."""

    def __init__(self, workspace: Path) -> None:
        resolved = workspace.resolve()
        self.storage = resolved if resolved.name == "local-ai" else resolved / "local-ai"
        self.directory = self.storage / "telemetry"

    def append_benchmark_request(
        self,
        *,
        task_id: str,
        request_id: str,
        model_id: str,
        execution_mode: str,
        timestamp: str,
        elapsed_ms: int,
        low_vram: Mapping[str, Any],
        reported_memory: Mapping[str, Any] | None = None,
    ) -> Path:
        """Append one logical request record without fabricating absent memory data."""
        record: dict[str, Any] = {
            "task_id": task_id,
            "request_id": request_id,
            "model_id": model_id,
            "execution_mode": execution_mode,
            "timestamp": timestamp,
            "elapsed_ms": elapsed_ms,
            "low_vram": dict(low_vram),
        }
        if reported_memory is not None:
            record["reported_memory"] = dict(reported_memory)
        self.directory.mkdir(parents=True, exist_ok=True)
        primary = self.directory / "requests.ndjson"
        with primary.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
        # ``benchmark.ndjson`` remains a compatibility alias for the initial examples.
        alias = self.directory / "benchmark.ndjson"
        if not alias.exists():
            try:
                os.link(primary, alias)
            except OSError:
                alias.write_text(primary.read_text(encoding="utf-8"), encoding="utf-8")
        elif not alias.samefile(primary):
            with alias.open("a", encoding="utf-8", newline="\n") as stream:
                stream.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
        return primary
