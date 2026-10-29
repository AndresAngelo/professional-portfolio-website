"""VRAM headroom gate: nvidia-smi readings fail closed, and the floor is applied exactly."""

from __future__ import annotations

from dataclasses import dataclass

import pytest
from hypothesis import given, settings, strategies as st

from orchestrator.vram import GpuMemory, GpuReadError, headroom_passes, parse_nvidia_smi, read_gpu_memory


def test_a_single_nvidia_row_is_parsed_into_mib() -> None:
    memory = parse_nvidia_smi("NVIDIA GeForce RTX 5070 Laptop GPU, 7300, 8188\n")

    assert memory == GpuMemory("NVIDIA GeForce RTX 5070 Laptop GPU", 7300, 8188)
    assert memory.free_mib == 888


def test_several_gpu_rows_fail_closed() -> None:
    with pytest.raises(GpuReadError, match="exactly one"):
        parse_nvidia_smi("GPU A, 1, 8\nGPU B, 2, 8\n")


@pytest.mark.parametrize("text", ["", "GPU, lots, 8", "GPU, 9, 8", "not a row"])
def test_malformed_output_fails_closed(text: str) -> None:
    with pytest.raises(GpuReadError):
        parse_nvidia_smi(text)


@dataclass
class _Completed:
    returncode: int
    stdout: str = ""
    stderr: str = ""


def test_a_failing_nvidia_smi_is_an_error_never_a_zero_reading() -> None:
    with pytest.raises(GpuReadError, match="exited with 9"):
        read_gpu_memory(lambda *args, **kwargs: _Completed(returncode=9, stderr="driver missing"))


def test_a_missing_nvidia_smi_is_an_error() -> None:
    def missing(*args: object, **kwargs: object) -> None:
        raise FileNotFoundError("nvidia-smi")

    with pytest.raises(GpuReadError, match="could not run"):
        read_gpu_memory(missing)


def test_the_floor_is_applied_exactly() -> None:
    memory = GpuMemory("gpu", used_mib=7500, total_mib=8188)

    assert headroom_passes(memory, 688) is True
    assert headroom_passes(memory, 689) is False


@settings(max_examples=100, deadline=None)
@given(total=st.integers(min_value=1, max_value=32768), data=st.data())
def test_the_gate_passes_exactly_when_free_memory_meets_the_floor(total: int, data: st.DataObject) -> None:
    used = data.draw(st.integers(min_value=0, max_value=total))
    floor = data.draw(st.integers(min_value=1, max_value=total + 1))

    assert headroom_passes(GpuMemory("gpu", used, total), floor) == (total - used >= floor)
