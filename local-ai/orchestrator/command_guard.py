"""Authorization policy for parser-derived local validation commands."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable

from .models import DeclaredCommand


@dataclass(frozen=True)
class CommandAuthorizationError(ValueError):
    """Raised when a command is unsafe or absent from the active declaration."""

    message: str
    category: str

    def __str__(self) -> str:
        return self.message


class CommandGuard:
    """Allow only exactly declared commands after safe whitespace normalization.

    ``denylist=False`` skips the git, network, and package-manager checks. The command must still equal a
    command declared in the goal file, so the executor model can never choose what runs.
    """

    def __init__(self, *, denylist: bool = True) -> None:
        self.denylist = denylist

    _DENYLIST: tuple[tuple[str, str], ...] = (
        ("git", r"(?:^|[\s;&|])git(?:\s|$)"),
        (
            "network",
            r"(?:^|[\s;&|])(?:curl|wget|invoke-webrequest|invoke-restmethod|iwr|irm|ssh|scp)(?:\s|$)",
        ),
        (
            "package",
            r"(?:^|[\s;&|])(?:pip|pip3|npx|yarn|pnpm|winget|choco)(?:\s|$)|"
            r"(?:^|[\s;&|])python(?:\.exe)?\s+-m\s+pip(?:\s|$)",
        ),
    )

    # npm is allowed only for version checks, ``npm test``, and ``npm run <script>``. Every other subcommand
    # (install, ci, add, update, exec, publish, ...) is denied, and so is a bare ``npm``.
    _NPM_INVOCATION = re.compile(r"(?:^|[\s;&|(`$])npm(?:\.cmd)?(?=\s|$)(?P<rest>[^\n;&|)]*)", re.IGNORECASE)
    _NPM_SCRIPT_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9:_.-]*")

    @classmethod
    def _npm_forms_allowed(cls, command: str) -> bool:
        for match in cls._NPM_INVOCATION.finditer(command):
            tokens = match.group("rest").split()
            if not tokens:
                return False
            first = tokens[0].lower()
            if first in {"-v", "--version", "test"}:
                continue
            if first in {"run", "run-script"} and len(tokens) > 1 and cls._NPM_SCRIPT_NAME.fullmatch(tokens[1]):
                continue
            return False
        return True

    @staticmethod
    def normalize(command: str) -> str:
        """Collapse whitespace outside quoted literals without changing their contents."""
        pieces: list[str] = []
        whitespace = False
        quote: str | None = None
        escaped = False
        for character in command.strip():
            if quote is not None:
                pieces.append(character)
                if escaped:
                    escaped = False
                elif character == "`":
                    escaped = True
                elif character == quote:
                    quote = None
                continue
            if character in {"'", '"'}:
                if whitespace and pieces:
                    pieces.append(" ")
                whitespace = False
                quote = character
                pieces.append(character)
            elif character.isspace():
                whitespace = True
            else:
                if whitespace and pieces:
                    pieces.append(" ")
                whitespace = False
                pieces.append(character)
        return "".join(pieces)

    def authorize(
        self, *, candidate: str, declared_commands: Iterable[DeclaredCommand]
    ) -> str:
        """Return the matching canonical command or raise before process invocation."""
        normalized_candidate = self.normalize(candidate)
        self._reject_denied(candidate)
        for command in declared_commands:
            canonical = self.normalize(command.canonical_text)
            self._reject_denied(command.canonical_text)
            if normalized_candidate == canonical:
                return command.canonical_text
        raise CommandAuthorizationError(
            "command is not an exactly declared canonical command", "declared"
        )

    @staticmethod
    def _executable_text(raw: str) -> str:
        """Drop full-line PowerShell comments. They never run, so their words must not trigger a denial.

        Exact matching still compares the full text, comments included.
        """
        kept = [line for line in raw.replace("\r\n", "\n").split("\n") if not line.lstrip().startswith("#")]
        return "\n".join(kept)

    def _reject_denied(self, raw: str) -> None:
        if not self.denylist:
            return
        command = self.normalize(self._executable_text(raw))
        for category, pattern in self._DENYLIST:
            if re.search(pattern, command, flags=re.IGNORECASE):
                raise CommandAuthorizationError(
                    f"{category} command activity is denied", category
                )
        if not self._npm_forms_allowed(command):
            raise CommandAuthorizationError("package command activity is denied", "package")
