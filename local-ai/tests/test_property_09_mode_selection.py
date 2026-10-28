"""Property coverage for observable execution-mode selection."""

from __future__ import annotations

from hypothesis import given, settings, strategies as st

from orchestrator.mode_selector import ModeSelector, PreflightEvidence, ValidationFailure
from orchestrator.models import ExecutionMode


# Feature: stateless-turn-python-orchestrator-pipeline, Property 9: Observable preflight and validation evidence determines mode
# Validates: Requirements 7.1, 7.2, 7.3, 7.4
_NONZERO_EXIT_CODES = st.integers(min_value=-255, max_value=255).filter(bool)
_STDERR = st.text(max_size=256)


def _expected_preflight_mode(
    *, target_exists: bool, missing_import: bool, unresolved_dependency: bool, signature_mismatch: bool
) -> ExecutionMode:
    """Express the required precedence for independently observed preflight facts."""
    if not target_exists:
        return ExecutionMode.SCAFFOLD
    if missing_import or unresolved_dependency or signature_mismatch:
        return ExecutionMode.ALIGNER
    return ExecutionMode.COT_TASK


@settings(max_examples=100, deadline=None)
@given(
    target_exists=st.booleans(),
    missing_import=st.booleans(),
    unresolved_dependency=st.booleans(),
    signature_mismatch=st.booleans(),
)
def test_preflight_observations_select_one_deterministic_mode(
    target_exists: bool,
    missing_import: bool,
    unresolved_dependency: bool,
    signature_mismatch: bool,
) -> None:
    """Absent targets take precedence; otherwise observed mismatches select Aligner."""
    evidence = PreflightEvidence(
        target_exists=target_exists,
        missing_import=missing_import,
        unresolved_dependency=unresolved_dependency,
        signature_mismatch=signature_mismatch,
    )
    selector = ModeSelector()

    first = selector.select_preflight(evidence)
    second = selector.select_preflight(evidence)

    assert first == second
    assert first.mode is _expected_preflight_mode(
        target_exists=target_exists,
        missing_import=missing_import,
        unresolved_dependency=unresolved_dependency,
        signature_mismatch=signature_mismatch,
    )
    assert first.evidence == evidence


@settings(max_examples=100, deadline=None)
@given(exit_code=_NONZERO_EXIT_CODES, stderr=_STDERR)
def test_nonzero_validation_evidence_selects_error_with_next_request_details(
    exit_code: int, stderr: str
) -> None:
    """Every nonzero validation result becomes Error-mode context without alteration."""
    failure = ValidationFailure(exit_code=exit_code, stderr=stderr)

    decision = ModeSelector().select_after_validation(failure)

    assert decision.mode is ExecutionMode.ERROR
    assert decision.evidence == failure
    assert decision.evidence.exit_code == exit_code
    assert decision.evidence.stderr == stderr
