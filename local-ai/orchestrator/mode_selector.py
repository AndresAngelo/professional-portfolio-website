"""Derive executor modes solely from observable preflight and validation evidence."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .models import ExecutionMode


@dataclass(frozen=True)
class PreflightEvidence:
    """Boolean observations gathered before an executor request."""

    target_exists: bool
    missing_import: bool = False
    unresolved_dependency: bool = False
    signature_mismatch: bool = False


@dataclass(frozen=True)
class ValidationFailure:
    """The exact nonzero validation details provided to an Error-mode request."""

    exit_code: int
    stderr: str

    def __post_init__(self) -> None:
        if self.exit_code == 0:
            raise ValueError("Error mode requires a nonzero validation exit code")


@dataclass(frozen=True)
class ModeDecision:
    """A mode and its unmodified evidence, ready for bounded request context."""

    mode: ExecutionMode
    evidence: object


@dataclass(frozen=True)
class ModeEvidence:
    """Filesystem and parsed mismatch observations for the convenience selector."""

    target_path: Path
    missing_imports: tuple[str, ...] = ()
    unresolved_dependencies: tuple[str, ...] = ()
    signature_mismatches: tuple[str, ...] = ()


class ModeSelector:
    """Apply the required deterministic precedence to observable evidence."""

    def select_preflight(self, evidence: PreflightEvidence) -> ModeDecision:
        """Prefer Scaffold for an absent target, then Aligner for a mismatch."""
        if not evidence.target_exists:
            return ModeDecision(ExecutionMode.SCAFFOLD, evidence)
        if evidence.missing_import or evidence.unresolved_dependency or evidence.signature_mismatch:
            return ModeDecision(ExecutionMode.ALIGNER, evidence)
        return ModeDecision(ExecutionMode.COT_TASK, evidence)

    def select_after_validation(self, failure: ValidationFailure) -> ModeDecision:
        """Turn only an observed nonzero validation result into Error mode."""
        return ModeDecision(ExecutionMode.ERROR, failure)


def _target_display_path(target: Path) -> str:
    """Render conventional source/test targets relative to their workspace segment."""
    if not target.is_absolute():
        return target.as_posix()
    for anchor in ("src", "tests", "local-ai", ".kiro"):
        if anchor in target.parts:
            return Path(*target.parts[target.parts.index(anchor) :]).as_posix()
    return target.name


def select_execution_mode(evidence: ModeEvidence) -> ModeDecision:
    """Classify a concrete target and return concise request-ready evidence text."""
    target = evidence.target_path
    if not target.exists():
        return ModeDecision(ExecutionMode.SCAFFOLD, f"target path is absent: {_target_display_path(target)}")

    mismatches = (
        *(f"missing import: {item}" for item in evidence.missing_imports),
        *(f"unresolved dependency: {item}" for item in evidence.unresolved_dependencies),
        *(f"signature mismatch: {item}" for item in evidence.signature_mismatches),
    )
    if mismatches:
        return ModeDecision(ExecutionMode.ALIGNER, "; ".join(mismatches))
    return ModeDecision(ExecutionMode.COT_TASK, "existing target has no observed alignment mismatch")
