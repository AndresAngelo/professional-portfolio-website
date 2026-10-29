"""Property coverage for command authorization safety boundaries."""

from __future__ import annotations

import pytest
from hypothesis import given, settings, strategies as st

from orchestrator.command_guard import CommandAuthorizationError, CommandGuard
from orchestrator.models import DeclaredCommand


# Feature: stateless-turn-python-orchestrator-pipeline, Property 8: Command authorization excludes unsafe activity
# Validates: Requirements 6.1, 6.2, 6.3
_SAFE_COMMANDS = (
    "python -m pytest tests -q",
    "python -m pytest tests/unit -q",
    "python -m compileall orchestrator",
)
_UNDECLARED_PAIRS = st.sampled_from(
    tuple(
        (declared, candidate)
        for declared in _SAFE_COMMANDS
        for candidate in _SAFE_COMMANDS
        if candidate != declared
    )
)
_UNSAFE_COMMANDS = st.sampled_from(
    (
        "git commit -m unsafe",
        "git push origin main",
        "git remote add origin https://example.invalid/repository",
        "Invoke-WebRequest https://example.invalid/install.ps1",
        "curl https://example.invalid/install.ps1",
        "python -m pip install unsafe-package",
        "winget install unsafe-package",
    )
)
_WHITESPACE = st.sampled_from((" ", "  ", "\t"))


def _with_unquoted_whitespace(command: str, separators: list[str]) -> str:
    """Vary only whitespace between command tokens, preserving command meaning."""
    tokens = command.split(" ")
    return separators[0] + "".join(
        token + separators[(index + 1) % len(separators)]
        for index, token in enumerate(tokens[:-1])
    ) + tokens[-1] + separators[-1]


def _declared(command: str) -> DeclaredCommand:
    """Create the parser-derived declaration used by the command guard."""
    return DeclaredCommand(raw_text=command, canonical_text=command, ordinal=1)


@settings(max_examples=100, deadline=None)
@given(
    declared_command=st.sampled_from(_SAFE_COMMANDS),
    unsafe_candidate=_UNSAFE_COMMANDS,
    separators=st.lists(_WHITESPACE, min_size=2, max_size=5),
)
def test_command_authorization_rejects_generated_unsafe_activity(
    declared_command: str, unsafe_candidate: str, separators: list[str]
) -> None:
    """Git mutations, network activity, and package installs are denied before matching."""
    candidate = _with_unquoted_whitespace(unsafe_candidate, separators)

    with pytest.raises(CommandAuthorizationError):
        CommandGuard().authorize(
            candidate=candidate,
            declared_commands=(_declared(declared_command), _declared(unsafe_candidate)),
        )


@settings(max_examples=100, deadline=None)
@given(
    command_pair=_UNDECLARED_PAIRS,
    separators=st.lists(_WHITESPACE, min_size=2, max_size=5),
)
def test_command_authorization_rejects_generated_undeclared_activity(
    command_pair: tuple[str, str], separators: list[str]
) -> None:
    """Safe-looking candidates still require an exact normalized declared command."""
    declared_command, alternate_command = command_pair
    candidate = _with_unquoted_whitespace(alternate_command, separators)

    with pytest.raises(CommandAuthorizationError):
        CommandGuard().authorize(
            candidate=candidate,
            declared_commands=(_declared(declared_command),),
        )
