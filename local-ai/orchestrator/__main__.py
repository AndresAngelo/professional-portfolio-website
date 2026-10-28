"""Local-only command line surface for the stateless orchestrator.

No adapter is created at import time.  The injectable dependency record keeps tests
and operator preflight offline until a command deliberately delegates work.
"""

from __future__ import annotations

import argparse
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn

from .services import compose_local_command_service


@dataclass(frozen=True)
class CliDependencies:
    """All command effects and safety checks required by :func:`main`."""

    discover: Callable[[], int]
    run_once: Callable[..., None]
    benchmark: Callable[[], None]
    configuration_safe: Callable[[], bool]
    state_safe: Callable[[], bool]
    loopback_safe: Callable[[], bool]
    capabilities_safe: Callable[[], bool]


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="python -m orchestrator")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("discover")
    commands.add_parser("run-once")
    commands.add_parser("resume")
    benchmark = commands.add_parser("benchmark")
    benchmark.add_argument("--enable-benchmark", action="store_true")
    pilot = commands.add_parser("pilot")
    pilot.add_argument("--enable-pilot", action="store_true")
    return parser


def _default_dependencies() -> CliDependencies:
    config_path = Path(__file__).resolve().parents[1] / "config" / "orchestrator.toml"
    service = compose_local_command_service(config_path)
    checks = service.safety_checks()
    return CliDependencies(
        discover=service.discover,
        run_once=service.run_once,
        benchmark=service.benchmark,
        configuration_safe=checks.configuration_safe,
        state_safe=checks.state_safe,
        loopback_safe=checks.loopback_safe,
        capabilities_safe=checks.capabilities_safe,
    )


def _safe_for_work(dependencies: CliDependencies) -> bool:
    return all(
        check()
        for check in (
            dependencies.configuration_safe,
            dependencies.state_safe,
            dependencies.loopback_safe,
            dependencies.capabilities_safe,
        )
    )


def main(arguments: Sequence[str] | None = None, *, dependencies: CliDependencies | None = None) -> int:
    """Parse and delegate one local command, failing closed on unsafe preflight."""
    parsed = _parser().parse_args(arguments)
    active_dependencies = dependencies if dependencies is not None else _default_dependencies()

    if parsed.command == "discover":
        active_dependencies.discover()
        return 0

    if parsed.command == "benchmark":
        if not parsed.enable_benchmark or not _safe_for_work(active_dependencies):
            return 2
        active_dependencies.benchmark()
        return 0

    if parsed.command == "pilot":
        if not parsed.enable_pilot or not _safe_for_work(active_dependencies):
            return 2
        active_dependencies.run_once(resume=False, task_limit=1)
        return 0

    if not _safe_for_work(active_dependencies):
        return 2
    active_dependencies.run_once(resume=parsed.command == "resume", task_limit=1)
    return 0


def _entrypoint() -> NoReturn:
    raise SystemExit(main())


if __name__ == "__main__":
    _entrypoint()
