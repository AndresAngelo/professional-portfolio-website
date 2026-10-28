"""Offline CLI and controlled-pilot contracts.

Task 8.3 implements the small, injectable command surface specified here.  These
tests use only a recording fake service: they never open a model connection,
start a process, modify runtime model settings, or invoke Git.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import pytest

from orchestrator.__main__ import CliDependencies, main


@dataclass
class FakeCliService:
    """Records CLI delegation without performing external work."""

    discovered: int = 2
    configuration_safe: bool = True
    state_safe: bool = True
    loopback_safe: bool = True
    capabilities_safe: bool = True
    calls: list[tuple[str, dict[str, Any]]] = field(default_factory=list)

    def discover(self) -> int:
        self.calls.append(("discover", {}))
        return self.discovered

    def run_once(self, *, resume: bool, task_limit: int) -> None:
        self.calls.append(("run_once", {"resume": resume, "task_limit": task_limit}))

    def benchmark(self) -> None:
        self.calls.append(("benchmark", {}))


def dependencies(service: FakeCliService) -> CliDependencies:
    """Supply every command dependency explicitly, avoiding real adapters."""
    return CliDependencies(
        discover=service.discover,
        run_once=service.run_once,
        benchmark=service.benchmark,
        configuration_safe=lambda: service.configuration_safe,
        state_safe=lambda: service.state_safe,
        loopback_safe=lambda: service.loopback_safe,
        capabilities_safe=lambda: service.capabilities_safe,
    )


@pytest.mark.parametrize(
    ("arguments", "expected_call"),
    [
        (["discover"], ("discover", {})),
        (["run-once"], ("run_once", {"resume": False, "task_limit": 1})),
        (["resume"], ("run_once", {"resume": True, "task_limit": 1})),
    ],
)
def test_non_pilot_commands_are_parsed_and_limited_to_one_task(
    arguments: list[str], expected_call: tuple[str, dict[str, Any]]
) -> None:
    """Discover, normal execution, and resume use the injected local-only service."""
    service = FakeCliService()

    assert main(arguments, dependencies=dependencies(service)) == 0
    assert service.calls == [expected_call]


def test_benchmark_is_disabled_by_default_without_touching_runtime_settings() -> None:
    """Benchmark refuses unless explicitly enabled and does not call the benchmark adapter."""
    service = FakeCliService()

    assert main(["benchmark"], dependencies=dependencies(service)) == 2
    assert service.calls == []


def test_benchmark_requires_explicit_enablement_and_safe_loopback_capabilities() -> None:
    """An enabled benchmark is delegated only after local endpoint and capability preflight."""
    service = FakeCliService()

    assert main(["benchmark", "--enable-benchmark"], dependencies=dependencies(service)) == 0
    assert service.calls == [("benchmark", {})]


@pytest.mark.parametrize("unsafe_field", ["configuration_safe", "state_safe", "loopback_safe", "capabilities_safe"])
def test_unsafe_configuration_state_endpoint_or_capabilities_refuse_execution(
    unsafe_field: str,
) -> None:
    """Commands that could run work fail closed before service delegation."""
    service = FakeCliService()
    setattr(service, unsafe_field, False)

    assert main(["run-once"], dependencies=dependencies(service)) == 2
    assert service.calls == []


def test_pilot_requires_explicit_confirmation_before_any_task_is_selected() -> None:
    """A pilot command without opt-in is a no-op refusal."""
    service = FakeCliService()

    assert main(["pilot"], dependencies=dependencies(service)) == 2
    assert service.calls == []


def test_explicit_pilot_uses_safe_preflight_and_never_selects_more_than_one_task() -> None:
    """The controlled path invokes exactly one normal selection after every safety check."""
    service = FakeCliService()

    assert main(["pilot", "--enable-pilot"], dependencies=dependencies(service)) == 0
    assert service.calls == [("run_once", {"resume": False, "task_limit": 1})]


def test_pilot_rejects_an_unsafe_loopback_or_capability_preflight() -> None:
    """Pilot work cannot start when its local model endpoint or capability evidence is unsafe."""
    service = FakeCliService(loopback_safe=False)

    assert main(["pilot", "--enable-pilot"], dependencies=dependencies(service)) == 2
    assert service.calls == []
