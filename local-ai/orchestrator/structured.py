"""Schema-constrained replies: validate with Pydantic and retry with fresh requests on schema failure.

One initial attempt plus two retries is the whole budget. Each retry is a new, history-free
request. Transport failures are not schema failures, so they propagate immediately.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol, TypeVar

from pydantic import BaseModel, ValidationError

from .config import ModelRoleName
from .lm_studio import reply_text

MAX_SCHEMA_ATTEMPTS = 3

ModelT = TypeVar("ModelT", bound=BaseModel)


class ChatAdapter(Protocol):
    def chat(
        self,
        role: ModelRoleName,
        messages: list[dict[str, str]],
        *,
        task_id: str | None = None,
        response_schema: dict[str, Any] | None = None,
        schema_name: str = "structured_reply",
    ) -> Any: ...


@dataclass(frozen=True)
class SchemaAttempt:
    attempt: int
    reply_excerpt: str
    error: str


class StructuredOutputError(RuntimeError):
    """Every schema attempt failed. The caller must quarantine the task rather than guess."""

    def __init__(self, role: ModelRoleName, model_name: str, attempts: tuple[SchemaAttempt, ...]) -> None:
        super().__init__(f"{role} reply failed {model_name} validation on all {len(attempts)} attempts")
        self.role = role
        self.model_name = model_name
        self.attempts = attempts


def structured_call(
    adapter: ChatAdapter,
    *,
    role: ModelRoleName,
    messages: list[dict[str, str]],
    model_cls: type[ModelT],
    task_id: str,
    schema_name: str,
    max_attempts: int = MAX_SCHEMA_ATTEMPTS,
) -> tuple[ModelT, tuple[SchemaAttempt, ...]]:
    """Return the first valid reply and the schema failures that preceded it.

    Raises :class:`StructuredOutputError` after ``max_attempts`` invalid replies.
    """
    if max_attempts < 1:
        raise ValueError("at least one attempt is required")
    schema = model_cls.model_json_schema()
    failures: list[SchemaAttempt] = []
    for attempt in range(1, max_attempts + 1):
        response = adapter.chat(role, messages, task_id=task_id, response_schema=schema, schema_name=schema_name)
        text = reply_text(response)
        try:
            parsed = model_cls.model_validate_json(text)
        except ValidationError as error:
            failures.append(SchemaAttempt(attempt=attempt, reply_excerpt=text[:500], error=str(error)[:1000]))
            continue
        return parsed, tuple(failures)
    raise StructuredOutputError(role, model_cls.__name__, tuple(failures))
