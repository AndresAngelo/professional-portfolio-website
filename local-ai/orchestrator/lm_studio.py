"""Loopback-only fresh-request adapter for the configured local model roles."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import urlparse
from uuid import uuid4

from .config import (
    LOOPBACK_HOST,
    LmStudioConfig,
    LowVramConfig,
    ModelRoleName,
    ModelRoles,
    derive_artifact_path,
)
from .telemetry import LowVramApplication, LowVramCapabilityGate


class ModelRequestError(RuntimeError):
    """A local model transport failure, preserved as a local artifact."""


class SpeculativeDecodingError(ModelRequestError):
    """A reply carried draft-model fields, so speculative decoding was active against the operator's setting."""


def draft_model_of(response: dict[str, Any]) -> str | None:
    """Return the draft model named in a chat reply, or None. LM Studio reports it at the top level and in stats."""
    stats = response.get("stats")
    candidate = response.get("draft_model") or (stats.get("draft_model") if isinstance(stats, dict) else None)
    return str(candidate) if candidate else None


class LocalTransport(Protocol):
    def request(self, *, method: str, url: str, payload: dict[str, Any] | None, timeout: int) -> dict[str, Any]: ...


class ModelPort(Protocol):
    def request(self, *, payload: dict[str, Any]) -> Any: ...


def build_messages(payload: dict[str, Any]) -> list[dict[str, str]]:
    """Turn one packed payload into chat messages.

    Static anchors become the system message. The active task scope becomes the user message
    as JSON. A payload without a ``context`` section is sent as one JSON user message.
    """
    context = payload.get("context")
    if not isinstance(context, dict):
        return [{"role": "user", "content": json.dumps(payload, sort_keys=True, ensure_ascii=False)}]
    anchors = [str(context[key]) for key in ("system_rules", "architecture_schema") if context.get(key)]
    scope = context.get("active_task_scope", {})
    return [
        {"role": "system", "content": "\n\n".join(anchors) or "You are a local coding orchestrator."},
        {"role": "user", "content": json.dumps(scope, sort_keys=True, ensure_ascii=False)},
    ]


def reply_text(response: dict[str, Any]) -> str:
    """Return the assistant text of a chat-completions reply, or fail with a local error."""
    try:
        content = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as error:
        raise ModelRequestError("local reply has no choices[0].message.content") from error
    if not isinstance(content, str):
        raise ModelRequestError("local reply content is not text")
    return content


class LmStudioAdapter:
    """Send each fresh request to the configured model bound to its role."""

    def __init__(
        self,
        *,
        config: LmStudioConfig | None = None,
        storage: Path | None = None,
        transport: LocalTransport | None = None,
        model_port: ModelPort | None = None,
    ) -> None:
        self.models: ModelRoles | None = None
        if config is None:
            if model_port is None:
                raise ValueError("adapter needs LmStudioConfig or a test model port")
            self.base_url = ""
            self.timeout = 0
            self.loopback_only = True
        else:
            self.base_url = config.base_url.rstrip("/")
            self.timeout = config.request_timeout_seconds
            self.loopback_only = config.allow_loopback_only
            self.models = config.models
            self._validate_loopback()
        if transport is not None and model_port is not None:
            raise ValueError("choose either HTTP transport or model port")
        if transport is None and model_port is None:
            raise ValueError("a local transport boundary is required")
        self.storage = storage.resolve() if storage is not None else None
        self.transport = transport
        self.model_port = model_port
        self.last_request_id: str | None = None
        self.last_model_id: str | None = None
        self.last_draft_model: str | None = None

    def request(self, payload: dict[str, Any], task_id: str | None = None) -> Any:
        """Executor shorthand: send a packed payload to the executor role's model.

        Routing and audit calls must use :meth:`chat` with an explicit role.
        """
        return self.chat("executor", build_messages(payload), task_id=task_id or self._task_id(payload))

    def chat(
        self,
        role: ModelRoleName,
        messages: list[dict[str, str]],
        *,
        task_id: str | None = None,
        response_schema: dict[str, Any] | None = None,
        schema_name: str = "structured_reply",
    ) -> Any:
        """Send one fresh chat request to ``role``'s model, optionally constrained to a JSON schema."""
        body: dict[str, Any] = {"messages": messages, "temperature": 0}
        if response_schema is not None:
            body["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": schema_name, "strict": True, "schema": response_schema},
            }
        return self._send(role=role, body=body, task=task_id or "unknown-task")

    def embed(self, texts: list[str], *, task_id: str | None = None) -> list[list[float]]:
        """Embed texts with the embedding role's model. Returns one vector per input, in order."""
        model_id = self.model_id_for("embedding")
        request_id = f"req_{uuid4().hex}"
        self.last_request_id = request_id
        self.last_model_id = model_id
        body = {"model": model_id, "input": texts}
        if self.model_port is not None:
            response = self.model_port.request(payload=body)
        else:
            assert self.transport is not None
            try:
                response = self.transport.request(
                    method="POST", url=f"{self.base_url}/embeddings", payload=body, timeout=self.timeout
                )
            except (ConnectionError, TimeoutError, RuntimeError, OSError, ValueError) as error:
                raise ModelRequestError(f"local embedding request for {model_id} failed: {error}") from error
        try:
            items = sorted(response["data"], key=lambda item: item["index"])
            vectors = [[float(x) for x in item["embedding"]] for item in items]
        except (KeyError, TypeError, ValueError) as error:
            raise ModelRequestError("local embedding reply has no usable data[*].embedding") from error
        if len(vectors) != len(texts):
            raise ModelRequestError(f"embedding reply has {len(vectors)} vectors for {len(texts)} inputs")
        return vectors

    def model_id_for(self, role: ModelRoleName) -> str:
        """Return the configured identifier for one role. Requests never fall back to a pinned model."""
        if self.models is None:
            raise ValueError("model roles require LmStudioConfig; a bare test port cannot route requests")
        return self.models.for_role(role).model_id

    def capabilities(self) -> dict[str, str]:
        """Return normalized runtime capability states for existing callers."""
        reported = self.runtime_capabilities()
        return {key: self._capability_state(reported.get(key)) for key in self._capability_keys()}

    def runtime_capabilities(self) -> dict[str, Any]:
        """Query local runtime capability data without changing any setting."""
        if self.transport is None:
            return {}
        response = self.transport.request(
            method="GET", url=f"{self.base_url}/capabilities", payload=None, timeout=self.timeout
        )
        if not isinstance(response, dict):
            raise ModelRequestError("local runtime returned invalid capability data")
        return response

    def prepare_benchmark_low_vram(
        self, *, config: LowVramConfig, effective_values: dict[str, Any]
    ) -> LowVramApplication:
        """Record a benchmark-only capability decision without applying runtime changes."""
        capabilities = LowVramCapabilityGate.normalize_capabilities(self.runtime_capabilities())
        application = LowVramCapabilityGate(config).apply(
            capabilities=capabilities, effective_values=effective_values
        )
        if self.storage is not None:
            workspace = self.storage.parent if self.storage.name == "local-ai" else self.storage
            target = derive_artifact_path(
                workspace=workspace,
                artifact_kind="telemetry",
                task_id="runtime",
                relative_name=f"capabilities-{uuid4().hex}.json",
            )
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(
                json.dumps(
                    {
                        "timestamp": datetime.now(UTC).isoformat(),
                        "capabilities": {name: state.value for name, state in capabilities.items()},
                        "benchmark_enabled": config.benchmark_enabled,
                        "low_vram": dict(application),
                    },
                    indent=2,
                    sort_keys=True,
                )
                + "\n",
                encoding="utf-8",
            )
        return application

    def _send(self, *, role: ModelRoleName, body: dict[str, Any], task: str) -> Any:
        request_id = f"req_{uuid4().hex}"
        model_id = self.model_id_for(role)
        request = {"model": model_id, **body}
        self.last_request_id = request_id
        self.last_model_id = model_id
        if self.model_port is not None:
            return self.model_port.request(payload=request)
        assert self.transport is not None
        try:
            self._write_artifact(
                task,
                f"{request_id}-request.json",
                {"request_id": request_id, "task_id": task, "role": role, "model_id": model_id, "payload": request},
            )
            response = self.transport.request(
                method="POST", url=f"{self.base_url}/chat/completions", payload=request, timeout=self.timeout
            )
            if not isinstance(response, dict) or response.get("error"):
                raise RuntimeError(f"non-success local response: {response!r}")
            self._write_artifact(
                task,
                f"{request_id}-response.json",
                {"request_id": request_id, "task_id": task, "role": role, "model_id": model_id, "response": response},
            )
            draft = draft_model_of(response)
            self.last_draft_model = draft
            if draft is not None:
                raise SpeculativeDecodingError(
                    f"{model_id} answered with draft model {draft}: speculative decoding is on. "
                    "Turn it off for this model in LM Studio and reload it."
                )
            return response
        except SpeculativeDecodingError:
            raise
        except (ConnectionError, TimeoutError, RuntimeError, OSError, ValueError) as error:
            self._write_error(task, request_id, error, role=role, model_id=model_id)
            raise ModelRequestError(f"local request for {model_id} failed: {error}") from error

    @staticmethod
    def _task_id(payload: dict[str, Any]) -> str:
        context = payload.get("context", {})
        scope = context.get("active_task_scope", {}) if isinstance(context, dict) else {}
        return str(scope.get("task_id", "unknown-task"))

    def _write_error(
        self, task_id: str, request_id: str, error: Exception, *, role: ModelRoleName, model_id: str
    ) -> None:
        self._write_artifact(
            task_id,
            f"{request_id}-request-error.json",
            {
                "request_id": request_id,
                "task_id": task_id,
                "role": role,
                "model_id": model_id,
                "endpoint_class": "loopback",
                "timestamp": datetime.now(UTC).isoformat(),
                "error": str(error),
            },
        )

    def _write_artifact(self, task_id: str, name: str, value: dict[str, Any]) -> None:
        if self.storage is None:
            return
        workspace = self.storage.parent if self.storage.name == "local-ai" else self.storage
        target = derive_artifact_path(workspace=workspace, artifact_kind="protocol", task_id=task_id, relative_name=name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def _validate_loopback(self) -> None:
        parsed = urlparse(self.base_url)
        if self.loopback_only and parsed.hostname != LOOPBACK_HOST:
            raise ValueError(f"LM Studio endpoint must be loopback-only at {LOOPBACK_HOST}")

    @staticmethod
    def _capability_keys() -> tuple[str, ...]:
        return ("flash_attention", "gpu_offload", "unified_kv", "kv_cache_type", "kv_offload")

    @staticmethod
    def _capability_state(value: Any) -> str:
        return "supported" if value is True else "unsupported" if value is False else "not-reported"
