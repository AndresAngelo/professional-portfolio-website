"""GPU memory readings from nvidia-smi and the headroom gate for the mesh's VRAM budget.

A reading must come from exactly one NVIDIA device and must be internally consistent. Anything
else fails closed, so an unreadable GPU can never look like free memory.
"""

from __future__ import annotations

import subprocess
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

NVIDIA_SMI_QUERY = ["nvidia-smi", "--query-gpu=name,memory.used,memory.total", "--format=csv,noheader,nounits"]


class GpuReadError(RuntimeError):
    """GPU memory could not be read as exactly one consistent NVIDIA device."""


@dataclass(frozen=True)
class GpuMemory:
    name: str
    used_mib: int
    total_mib: int

    @property
    def free_mib(self) -> int:
        return self.total_mib - self.used_mib


def parse_nvidia_smi(text: str) -> GpuMemory:
    """Parse one ``name, used, total`` row in MiB from ``nvidia-smi --format=csv,noheader,nounits``."""
    rows = [line.strip() for line in text.splitlines() if line.strip()]
    if len(rows) != 1:
        raise GpuReadError(f"expected exactly one NVIDIA GPU row, found {len(rows)}")
    fields = [field.strip() for field in rows[0].rsplit(",", 2)]
    if len(fields) != 3:
        raise GpuReadError("nvidia-smi row is not name, used, total")
    name, used, total = fields
    try:
        used_mib, total_mib = int(used), int(total)
    except ValueError as error:
        raise GpuReadError("nvidia-smi memory values are not integers") from error
    if total_mib <= 0 or not 0 <= used_mib <= total_mib:
        raise GpuReadError("nvidia-smi memory values are inconsistent")
    return GpuMemory(name=name, used_mib=used_mib, total_mib=total_mib)


def read_gpu_memory(runner: Callable[..., Any] = subprocess.run) -> GpuMemory:
    """Run the read-only nvidia-smi query. Any failure raises instead of returning a guess."""
    try:
        completed = runner(NVIDIA_SMI_QUERY, capture_output=True, text=True, timeout=20, check=False)
    except (OSError, subprocess.SubprocessError) as error:
        raise GpuReadError(f"nvidia-smi could not run: {error}") from error
    if completed.returncode != 0:
        raise GpuReadError(f"nvidia-smi exited with {completed.returncode}: {completed.stderr.strip()[:300]}")
    return parse_nvidia_smi(completed.stdout)


def headroom_passes(memory: GpuMemory, floor_mib: int) -> bool:
    """True only when the free memory is at or above the configured floor."""
    return memory.free_mib >= floor_mib
