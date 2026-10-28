"""Test-first examples for capability-gated low-VRAM telemetry.

Task 7.3 must implement these contracts with local runtime data only.  The
examples use no real model, PowerShell, or network connection.
"""

from __future__ import annotations

import json
from pathlib import Path

from orchestrator.config import LowVramConfig
from orchestrator.telemetry import (
    CapabilityState,
    LowVramCapabilityGate,
    TelemetryWriter,
)


def low_vram_config(**overrides: str | bool) -> LowVramConfig:
    """Create benchmark configuration with explicit setting requests."""
    values: dict[str, str | bool] = {
        "benchmark_enabled": True,
        "requested_flash_attention": "enabled",
        "requested_unified_kv": "auto",
        "requested_kv_cache_type": "Q4_0",
        "requested_kv_offload": "auto",
        "requested_gpu_offload_layers": "24",
    }
    values.update(overrides)
    return LowVramConfig(**values)  # type: ignore[arg-type]


def test_capability_gate_normalizes_runtime_support_states() -> None:
    """Only explicit booleans establish support; absent or unknown values stay unreported."""
    normalized = LowVramCapabilityGate.normalize_capabilities(
        {
            "flash_attention": True,
            "unified_kv": False,
            "kv_cache_type": "Q4_0",
            "gpu_offload_layers": None,
        }
    )

    assert normalized == {
        "flash_attention": CapabilityState.SUPPORTED,
        "unified_kv": CapabilityState.UNSUPPORTED,
        "kv_cache_type": CapabilityState.NOT_REPORTED,
        "kv_offload": CapabilityState.NOT_REPORTED,
        "gpu_offload_layers": CapabilityState.NOT_REPORTED,
    }


def test_unsupported_or_unreported_settings_retain_runtime_defaults() -> None:
    """A requested setting cannot override a runtime that did not confirm support."""
    result = LowVramCapabilityGate(low_vram_config()).apply(
        capabilities={
            "flash_attention": CapabilityState.UNSUPPORTED,
            "unified_kv": CapabilityState.NOT_REPORTED,
            "kv_cache_type": CapabilityState.SUPPORTED,
            "kv_offload": CapabilityState.UNSUPPORTED,
            "gpu_offload_layers": CapabilityState.NOT_REPORTED,
        },
        effective_values={"kv_cache_type": "Q4_0"},
    )

    assert result.configured_values == {"kv_cache_type": "Q4_0"}
    assert result.statuses == {
        "flash_attention": "unsupported",
        "unified_kv": "not-reported",
        "kv_cache_type": "applied",
        "kv_offload": "unsupported",
        "gpu_offload_layers": "not-reported",
    }


def test_effective_runtime_value_must_confirm_requested_supported_setting() -> None:
    """Support alone does not justify claiming a setting was applied."""
    result = LowVramCapabilityGate(low_vram_config()).apply(
        capabilities={name: CapabilityState.SUPPORTED for name in LowVramCapabilityGate.setting_names()},
        effective_values={"flash_attention": "disabled", "kv_cache_type": "Q8_0", "gpu_offload_layers": "24"},
    )

    assert result.statuses["flash_attention"] == "default"
    assert result.statuses["kv_cache_type"] == "default"
    assert result.statuses["gpu_offload_layers"] == "applied"
    assert "flash_attention" not in result.configured_values
    assert "kv_cache_type" not in result.configured_values


def test_benchmarked_requests_append_one_ndjson_record_and_preserve_absent_memory(workspace: Path) -> None:
    """Each benchmark event appends one record and never invents memory telemetry."""
    writer = TelemetryWriter(workspace=workspace)
    writer.append_benchmark_request(
        task_id="M5.G1.T1",
        request_id="req_first",
        model_id="yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF",
        execution_mode="CoT-Task",
        timestamp="2026-01-01T00:00:00Z",
        elapsed_ms=1250,
        low_vram={"flash_attention": "applied"},
        reported_memory=None,
    )
    writer.append_benchmark_request(
        task_id="M5.G1.T1",
        request_id="req_second",
        model_id="yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF",
        execution_mode="Error",
        timestamp="2026-01-01T00:00:01Z",
        elapsed_ms=900,
        low_vram={"flash_attention": "unsupported"},
        reported_memory={"vram_used_mb": 6200},
    )

    record_path = workspace / "local-ai" / "telemetry" / "benchmark.ndjson"
    lines = record_path.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    first, second = (json.loads(line) for line in lines)
    assert first["request_id"] == "req_first"
    assert "reported_memory" not in first
    assert second["request_id"] == "req_second"
    assert second["reported_memory"] == {"vram_used_mb": 6200}
