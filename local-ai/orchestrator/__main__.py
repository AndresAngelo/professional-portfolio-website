"""Local-only command line surface for the stateless orchestrator.

No adapter is created at import time.  The injectable dependency record keeps tests
and operator preflight offline until a command deliberately delegates work.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import NoReturn

from .config import MODEL_ROLE_NAMES, ConfigurationError, load_configuration
from .live import run_build_index, run_init_state, run_measure, run_once_live, run_probe_router, run_query, run_verify_models
from .services import compose_local_command_service

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "orchestrator.toml"


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
    run_once = commands.add_parser("run-once")
    run_once.add_argument("--dry-run", action="store_true", help="run the gates and name the next task; call no model")
    run_once.add_argument("--start-at", help="start queue selection at a task ID such as M1.G1.T1")
    commands.add_parser("resume")
    init_state = commands.add_parser("init-state", help="create run-state.json from the enabled goal files")
    init_state.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    benchmark = commands.add_parser("benchmark")
    benchmark.add_argument("--enable-benchmark", action="store_true")
    pilot = commands.add_parser("pilot")
    pilot.add_argument("--enable-pilot", action="store_true")
    config_check = commands.add_parser("config-check", help="print the validated LM Studio model roles")
    config_check.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    verify = commands.add_parser("verify-models", help="bind model roles to loaded LM Studio models")
    verify.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    probe = commands.add_parser("probe-router", help="send one fixed task stub to the router and check its reply")
    probe.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    measure = commands.add_parser("measure", help="measure GPU headroom with the mesh loaded")
    measure.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    build = commands.add_parser("build-index", help="embed context and spec chunks into the local index")
    build.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    query = commands.add_parser("query", help="show the top chunks for a query")
    query.add_argument("text")
    query.add_argument("--top-k", type=int, default=5)
    query.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    return parser


def _default_dependencies() -> CliDependencies:
    service = compose_local_command_service(DEFAULT_CONFIG_PATH)
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


def _print_model_roles(config_path: Path) -> int:
    """Print validated role bindings without contacting LM Studio; fail closed on bad config."""
    try:
        config = load_configuration(config_path)
    except ConfigurationError as error:
        print(f"configuration rejected: {error}", file=sys.stderr)
        return 2
    print(f"base_url: {config.lm_studio.base_url}")
    for role_name in MODEL_ROLE_NAMES:
        role = config.lm_studio.models.for_role(role_name)
        print(
            f"{role_name}: model_id={role.model_id} context_length={role.context_length} "
            f"output_reserve_tokens={role.output_reserve_tokens} max_prompt_bytes={role.max_prompt_bytes}"
        )
    print("status: model IDs are unverified until verify-models checks GET /v1/models (Task 3)")
    return 0


def main(arguments: Sequence[str] | None = None, *, dependencies: CliDependencies | None = None) -> int:
    """Parse and delegate one local command, failing closed on unsafe preflight."""
    parsed = _parser().parse_args(arguments)
    if parsed.command == "config-check":
        return _print_model_roles(parsed.config)
    if parsed.command == "verify-models":
        return run_verify_models(parsed.config)
    if parsed.command == "probe-router":
        return run_probe_router(parsed.config)
    if parsed.command == "measure":
        return run_measure(parsed.config)
    if parsed.command == "init-state":
        return run_init_state(parsed.config)
    if parsed.command == "run-once" and dependencies is None:
        return run_once_live(parsed.config, dry_run=parsed.dry_run, start_at=parsed.start_at)
    if parsed.command == "build-index":
        return run_build_index(parsed.config)
    if parsed.command == "query":
        return run_query(parsed.config, parsed.text, parsed.top_k)
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
