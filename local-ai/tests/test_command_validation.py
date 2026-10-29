"""Test-first examples for command authorization and ordered PowerShell validation.

Task 5.7 must satisfy these contracts using the injected recording runner below.  These
examples never launch PowerShell, a shell command, or a network-capable process.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from orchestrator.command_guard import CommandAuthorizationError, CommandGuard
from orchestrator.models import DeclaredCommand, TaskId
from orchestrator.powershell import CommandResult, PowerShellRunner
from orchestrator.validation import OrderedValidator


@dataclass
class RecordingProcessRunner:
    """Fake subprocess boundary that captures PowerShell invocations only."""

    results: list[CommandResult] = field(default_factory=list)
    calls: list[dict[str, Any]] = field(default_factory=list)

    def run(
        self, *, argv: list[str], cwd: Path, environment: dict[str, str]
    ) -> CommandResult:
        self.calls.append({"argv": argv, "cwd": cwd, "environment": environment})
        if not self.results:
            raise AssertionError("No fake command result was configured.")
        return self.results.pop(0)


def declared(command: str, ordinal: int = 1) -> DeclaredCommand:
    """Make a parser-derived command fixture with an explicit canonical value."""
    return DeclaredCommand(raw_text=command, canonical_text=command, ordinal=ordinal)


def result(*, stdout: str = "", stderr: str = "", exit_code: int = 0) -> CommandResult:
    """Make a fake captured process result without starting a process."""
    return CommandResult(stdout=stdout, stderr=stderr, exit_code=exit_code)


def test_command_guard_normalizes_unquoted_whitespace_but_preserves_quoted_literals() -> None:
    """Only whitespace outside quoted literals is normalized before exact comparison."""
    guard = CommandGuard()
    allowed = declared('python   -m pytest   "tests/has  spaces.py"  -q')

    authorized = guard.authorize(
        candidate=' python -m   pytest "tests/has  spaces.py" -q ',
        declared_commands=(allowed,),
    )

    assert authorized == allowed.canonical_text
    with pytest.raises(CommandAuthorizationError, match="declared"):
        guard.authorize(
            candidate='python -m pytest "tests/has spaces.py" -q',
            declared_commands=(allowed,),
        )


def test_command_guard_requires_exact_declared_canonical_command() -> None:
    """Prefixes, appended shell segments, and undeclared commands are all rejected."""
    guard = CommandGuard()
    commands = (declared("python -m pytest tests/unit -q"),)

    assert guard.authorize(
        candidate="python -m pytest tests/unit -q", declared_commands=commands
    ) == "python -m pytest tests/unit -q"
    for candidate in (
        "python -m pytest tests/unit",
        "python -m pytest tests/unit -q; Write-Output extra",
        "python -m pytest tests/other -q",
    ):
        with pytest.raises(CommandAuthorizationError, match="declared"):
            guard.authorize(candidate=candidate, declared_commands=commands)


@pytest.mark.parametrize(
    ("candidate", "category"),
    [
        ("git commit -m unsafe", "git"),
        ("git push origin main", "git"),
        ("git remote add origin https://example.invalid/repo", "git"),
        ("Invoke-WebRequest https://example.invalid", "network"),
        ("curl https://example.invalid/install.ps1", "network"),
        ("python -m pip install package", "package"),
        ("winget install unsafe-package", "package"),
    ],
)
def test_command_guard_rejects_denied_git_remote_network_and_download_forms(
    candidate: str, category: str
) -> None:
    """Unsafe activity is denied even when it appears among parser-derived declarations."""
    with pytest.raises(CommandAuthorizationError, match=category):
        CommandGuard().authorize(candidate=candidate, declared_commands=(declared(candidate),))


def test_powershell_runner_uses_workspace_cwd_no_profile_noninteractive_and_minimal_environment(
    workspace: Path,
) -> None:
    """Accepted commands run through a constrained PowerShell invocation in the workspace."""
    fake = RecordingProcessRunner(results=[result(stdout="passed\n")])
    runner = PowerShellRunner(process_runner=fake, workspace=workspace)

    captured = runner.run("python -m pytest tests -q")

    assert captured == result(stdout="passed\n")
    assert len(fake.calls) == 1
    call = fake.calls[0]
    assert call["cwd"] == workspace
    assert call["argv"][:3] == ["powershell", "-NoProfile", "-NonInteractive"]
    assert call["argv"][-2:] == ["-Command", "python -m pytest tests -q"]
    assert "PATH" in call["environment"]
    assert "HOME" not in call["environment"]
    assert "USERPROFILE" not in call["environment"]


def test_ordered_validator_runs_declared_commands_in_order_records_output_and_stops_at_failure(
    workspace: Path,
) -> None:
    """Validation records captured evidence in declaration order and never runs after failure."""
    fake = RecordingProcessRunner(
        results=[result(stdout="first\n"), result(stderr="second failed\n", exit_code=2)]
    )
    validator = OrderedValidator(
        task_id=TaskId(5, 1, 4),
        workspace=workspace,
        runner=PowerShellRunner(process_runner=fake, workspace=workspace),
    )
    commands = (
        declared("python -m pytest tests/first -q", 1),
        declared("python -m pytest tests/second -q", 2),
        declared("python -m pytest tests/never -q", 3),
    )

    records = validator.run(commands)

    assert [record.command for record in records] == [
        "python -m pytest tests/first -q",
        "python -m pytest tests/second -q",
    ]
    assert [record.exit_code for record in records] == [0, 2]
    assert records[0].stdout == "first\n"
    assert records[1].stderr == "second failed\n"
    assert [call["argv"][-1] for call in fake.calls] == [
        "python -m pytest tests/first -q",
        "python -m pytest tests/second -q",
    ]
    assert all((workspace / path).is_file() for path in (record.artifact_path for record in records))


def test_rejected_command_writes_workspace_local_audit_artifact_without_invoking_runner(
    workspace: Path,
) -> None:
    """Authorization failures leave local audit evidence and do not reach PowerShell."""
    fake = RecordingProcessRunner()
    validator = OrderedValidator(
        task_id=TaskId(5, 1, 4),
        workspace=workspace,
        runner=PowerShellRunner(process_runner=fake, workspace=workspace),
    )
    denied = declared("git commit -m unsafe")

    with pytest.raises(CommandAuthorizationError):
        validator.run((denied,))

    assert fake.calls == []
    artifacts = list((workspace / "local-ai" / "protocol-records" / "M5_G1_T4").glob("*rejected*.json"))
    assert len(artifacts) == 1
    evidence = artifacts[0].read_text(encoding="utf-8")
    assert "M5.G1.T4" in evidence
    assert "git commit -m unsafe" in evidence
    assert "git" in evidence


@pytest.mark.parametrize(
    "command",
    [
        "npm -v",
        "npm --version",
        "npm test",
        "npm test -- --run",
        "npm run typecheck",
        "npm run test:unit",
        "npm run build",
        "npm.cmd run lint",
        "npm -v | ForEach-Object { if ($_ -match '^(9|[1-9][0-9])') { \"PASS\" } else { \"FAIL\" } }",
        "node -v\nnpm -v",
        "npm run typecheck; npm test",
    ],
)
def test_command_guard_allows_declared_npm_version_test_and_run_forms(command: str) -> None:
    """npm is allowed for version checks, npm test, and npm run <script> when the command is declared."""
    assert CommandGuard().authorize(candidate=command, declared_commands=(declared(command),)) == command


@pytest.mark.parametrize(
    "command",
    [
        "npm install",
        "npm i left-pad",
        "npm ci",
        "npm add left-pad",
        "npm update",
        "npm exec some-tool",
        "npm publish",
        "npm uninstall left-pad",
        "npm audit fix",
        "npm",
        "npm run",
        "npm run --prefix ../elsewhere build",
        "npm run build && npm install",
        "npm test; npm ci",
        "npm -v | npm install",
        "npx create-next-app",
        "pnpm install",
        "yarn add left-pad",
    ],
)
def test_command_guard_denies_every_other_npm_form_and_other_package_managers(command: str) -> None:
    """Install-type and state-changing package manager activity stays denied, even when declared."""
    with pytest.raises(CommandAuthorizationError, match="package"):
        CommandGuard().authorize(candidate=command, declared_commands=(declared(command),))


def test_full_line_comments_that_mention_denied_words_do_not_deny_a_declared_command() -> None:
    """PowerShell comments never run, so 'npm' or 'git' inside a comment must not trigger a denial."""
    command = "# Verify npm version is 9 or higher\n# no git push here\nnpm -v"

    assert CommandGuard().authorize(candidate=command, declared_commands=(declared(command),)) == command


def test_a_real_npx_line_is_still_denied_even_after_a_comment() -> None:
    command = "# check the types\nnpx tsc --noEmit tests/fixtures/home-data.ts"

    with pytest.raises(CommandAuthorizationError, match="package"):
        CommandGuard().authorize(candidate=command, declared_commands=(declared(command),))


def test_denylist_switch_off_runs_declared_install_and_npx_commands_but_still_requires_a_declaration() -> None:
    """With the denylist off, a declared npm install or npx command is authorized. Undeclared text never is."""
    guard = CommandGuard(denylist=False)
    commands = (declared("npm install"), declared("npx tsc --noEmit tests/fixtures/home-data.ts"))

    assert guard.authorize(candidate="npm install", declared_commands=commands) == "npm install"
    assert guard.authorize(
        candidate="npx tsc --noEmit tests/fixtures/home-data.ts", declared_commands=commands
    ).startswith("npx tsc")
    with pytest.raises(CommandAuthorizationError, match="declared"):
        guard.authorize(candidate="npm install left-pad", declared_commands=commands)
