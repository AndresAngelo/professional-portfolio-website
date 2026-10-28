"""Property contract for capability-gated low-VRAM settings and telemetry."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from hypothesis import given, settings, strategies as st

from orchestrator.telemetry import LowVramCapabilityGate, TelemetryWriter


# Feature: stateless-turn-python-orchestrator-pipeline, Property 12: Capability-gated low-VRAM application and telemetry
# Validates: Requirements 9.3, 9.4, 9.5
_SETTING_NAMES = (
    "flash_attention",
    "unified_kv",
    "kv_cache_type",
    "kv_offload",
    "gpu_offload_layers",
)
_REQUESTED_VALUES = st.sampled_from(("auto", "enabled", "disabled", "Q4_0", "8"))
_TASK_IDS = st.from_regex(r"M[1-5]\.G(?:[1-9]|10)\.T(?:[1-9]|[1-9][0-9])", fullmatch=True)
_MODES = st.sampled_from(("Scaffold", "Aligner", "CoT-Task", "Error"))


@st.composite
def _support_matrices(draw: st.DrawFn) -> dict[str, Any]:
    """Generate reported, unsupported, and unreported runtime capabilities."""
    matrix: dict[str, Any] = {}
    for setting in _SETTING_NAMES:
        state = draw(st.sampled_from(("supported", "unsupported", "not-reported")))
        if state == "supported":
            matrix[setting] = True
        elif state == "unsupported":
            matrix[setting] = False
    return matrix


@st.composite
def _benchmark_requests(draw: st.DrawFn) -> list[dict[str, Any]]:
    """Create bounded request sequences with optional real memory telemetry."""
    requests: list[dict[str, Any]] = []
    for index in range(draw(st.integers(min_value=1, max_value=6))):
        request: dict[str, Any] = {
            "task_id": draw(_TASK_IDS),
            "request_id": f"req-{index}",
            "model_id": "yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF",
            "execution_mode": draw(_MODES),
            "timestamp": f"2026-01-01T00:00:{index:02d}Z",
            "elapsed_ms": draw(st.integers(min_value=0, max_value=120_000)),
        }
        if draw(st.booleans()):
            request["reported_memory"] = {"vram_used_mb": draw(st.integers(min_value=0, max_value=32_768))}
        requests.append(request)
    return requests


@settings(max_examples=100, deadline=None)
@given(
    support_matrix=_support_matrices(),
    requested=st.fixed_dictionaries({setting: _REQUESTED_VALUES for setting in _SETTING_NAMES}),
    benchmark_requests=_benchmark_requests(),
)
def test_low_vram_settings_are_capability_gated_and_benchmark_telemetry_is_append_only(
    tmp_path: Path,
    support_matrix: dict[str, Any],
    requested: dict[str, str],
    benchmark_requests: list[dict[str, Any]],
) -> None:
    """Only confirmed settings apply, and each benchmark request keeps honest local evidence."""
    gate = LowVramCapabilityGate(support_matrix)
    applied = gate.apply(requested=requested, effective_settings={key: requested[key] for key in support_matrix})

    for setting in _SETTING_NAMES:
        capability = support_matrix.get(setting)
        resolved = applied[setting]
        if capability is True:
            assert resolved["status"] == "applied"
            assert resolved["value"] == requested[setting]
        elif capability is False:
            assert resolved == {"status": "unsupported"}
        else:
            assert resolved == {"status": "not-reported"}

    writer = TelemetryWriter(tmp_path / "local-ai")
    for request in benchmark_requests:
        writer.append_benchmark_request(**request, low_vram=applied)

    telemetry_path = tmp_path / "local-ai" / "telemetry" / "requests.ndjson"
    records = [json.loads(line) for line in telemetry_path.read_text(encoding="utf-8").splitlines()]
    assert len(records) == len(benchmark_requests)

    for source, record in zip(benchmark_requests, records, strict=True):
        assert record["task_id"] == source["task_id"]
        assert record["request_id"] == source["request_id"]
        assert record["model_id"] == source["model_id"]
        assert record["execution_mode"] == source["execution_mode"]
        assert record["elapsed_ms"] == source["elapsed_ms"]
        assert record["low_vram"] == applied
        if "reported_memory" in source:
            assert record["reported_memory"] == source["reported_memory"]
        else:
            assert "reported_memory" not in record
