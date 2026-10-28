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
    """Allow only exactly declared commands after safe whitespace normalization."""

    _DENYLIST: tuple[tuple[str, str], ...] = (
        ("git", r"(?:^|[\s;&|])git(?:\s|$)"),
        (
            "network",
            r"(?:^|[\s;&|])(?:curl|wget|invoke-webrequest|invoke-restmethod|iwr|irm|ssh|scp)(?:\s|$)",
        ),
        (
            "package",
            r"(?:^|[\s;&|])(?:pip|pip3|npm|yarn|pnpm|winget|choco)(?:\s|$)|"
            r"(?:^|[\s;&|])python(?:\.exe)?\s+-m\s+pip(?:\s|$)",
        ),
    )

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
        self._reject_denied(normalized_candidate)
        for command in declared_commands:
            canonical = self.normalize(command.canonical_text)
            self._reject_denied(canonical)
            if normalized_candidate == canonical:
                return command.canonical_text
        raise CommandAuthorizationError(
            "command is not an exactly declared canonical command", "declared"
        )

    def _reject_denied(self, command: str) -> None:
        for category, pattern in self._DENYLIST:
            if re.search(pattern, command, flags=re.IGNORECASE):
                raise CommandAuthorizationError(
                    f"{category} command activity is denied", category
                )
