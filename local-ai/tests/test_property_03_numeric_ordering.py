"""Property tests for numeric task-queue coordinate ordering."""

from __future__ import annotations

from hypothesis import given, settings, strategies as st

from orchestrator.models import TaskId


# Feature: stateless-turn-python-orchestrator-pipeline, Property 3: Numeric queue ordering is independent of digit width
# Validates: Requirements 2.1, 2.2, 2.3
_COORDINATES = st.tuples(
    st.integers(min_value=1, max_value=20),
    st.integers(min_value=1, max_value=20),
    st.integers(min_value=1, max_value=20),
)


@settings(max_examples=100)
@given(
    coordinates=st.lists(
        _COORDINATES,
        min_size=0,
        max_size=40,
        unique=True,
    ),
    permutation_seed=st.integers(),
)
def test_numeric_queue_ordering_is_independent_of_digit_width(
    coordinates: list[tuple[int, int, int]], permutation_seed: int
) -> None:
    """Queue coordinates sort numerically, including two-digit values."""
    task_ids = [TaskId(*coordinate) for coordinate in coordinates]
    task_ids.extend((TaskId(2, 10, 1), TaskId(2, 2, 1), TaskId(10, 1, 1)))

    offset = permutation_seed % len(task_ids)
    permuted = task_ids[offset:] + task_ids[:offset]
    if permutation_seed % 2:
        permuted.reverse()
    ordered = sorted(permuted)

    assert [task_id.to_dict() for task_id in ordered] == [
        task_id.to_dict() for task_id in sorted(
            task_ids,
            key=lambda task_id: (task_id.milestone, task_id.goal, task_id.task),
        )
    ]

    two_digit_goal = [task_id for task_id in ordered if task_id.milestone == 2]
    assert two_digit_goal.index(TaskId(2, 2, 1)) < two_digit_goal.index(TaskId(2, 10, 1))
