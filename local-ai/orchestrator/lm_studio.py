"""Loopback-only fresh-request adapter for the configured local model."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import urlparse
from uuid import uuid4

from .config import LmStudioConfig, LowVramConfig, derive_artifact_path
from .telemetry import LowVramApplication, LowVramCapabilityGate


MODEL_ID = "yuxinlu1/gemma-4-12B-agentic-fable5-composer2.5-v2-3.5x-tau2-GGUF"


class ModelRequestError(RuntimeError):
    """A local model transport failure, preserved as a local artifact."""


class LocalTransport(Protocol):
    def request(self, *, method: str, url: str, payload: dict[str, Any] | None, timeout: int) -> dict[str, Any]: ...


class ModelPort(Protocol):
    def request(self, *, payload: dict[str, Any]) -> Any: ...


class LmStudioAdapter:
    """Send each fresh mode/attempt request to one configured model."""

    def __init__(
        self,
        *,
        config: LmStudioConfig | None = None,
        storage: Path | None = None,
        transport: LocalTransport | None = None,
        model_port: ModelPort | None = None,
    ) -> None:
        if config is None:
            if model_port is None:
                raise ValueError("adapter needs LmStudioConfig or a test model port")
            self.base_url = ""
            self.timeout = 0
            self.loopback_only = True
            self.model_id = MODEL_ID
        else:
            self.base_url = config.base_url.rstrip("/")
            self.timeout = config.request_timeout_seconds
            self.loopback_only = config.allow_loopback_only
            self.model_id = config.model_id
            if self.model_id != MODEL_ID:
                raise ValueError("LM Studio model identifier is fixed")
            self._validate_loopback()
        if transport is not None and model_port is not None:
            raise ValueError("choose either HTTP transport or model port")
        if transport is None and model_port is None:
            raise ValueError("a local transport boundary is required")
        self.storage = storage.resolve() if storage is not None else None
        self.transport = transport
        self.model_port = model_port

    def request(self, payload: dict[str, Any], task_id: str | None = None) -> Any:
        return self._request(payload=payload, task_id=task_id)

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

    def _request(self, *, payload: dict[str, Any], task_id: str | None) -> Any:
        request_id = f"req_{uuid4().hex}"
        task = task_id or self._task_id(payload)
        request = dict(payload)
        request["model"] = self.model_id
        if self.model_port is not None:
            return self.model_port.request(payload=request)
        assert self.transport is not None
        try:
            self._write_artifact(
                task,
                f"{request_id}-request.json",
                {"request_id": request_id, "task_id": task, "model_id": self.model_id, "payload": request},
            )
            response = self.transport.request(
                method="POST", url=f"{self.base_url}/chat/completions", payload=request, timeout=self.timeout
            )
            if not isinstance(response, dict) or response.get("error"):
                raise RuntimeError(f"non-success local response: {response!r}")
            self._write_artifact(
                task,
                f"{request_id}-response.json",
                {"request_id": request_id, "task_id": task, "model_id": self.model_id, "response": response},
            )
            return response
        except (ConnectionError, TimeoutError, RuntimeError, OSError, ValueError) as error:
            self._write_error(task, request_id, error)
            raise ModelRequestError(f"local request for {self.model_id} failed: {error}") from error

    @staticmethod
    def _task_id(payload: dict[str, Any]) -> str:
        context = payload.get("context", {})
        scope = context.get("active_task_scope", {}) if isinstance(context, dict) else {}
        return str(scope.get("task_id", "unknown-task"))

    def _write_error(self, task_id: str, request_id: str, error: Exception) -> None:
        self._write_artifact(
            task_id,
            f"{request_id}-request-error.json",
            {
                "request_id": request_id,
                "task_id": task_id,
                "model_id": self.model_id,
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
        if self.loopback_only and parsed.hostname not in {"127.0.0.1", "localhost"}:
            raise ValueError("LM Studio endpoint must be loopback-only")

    @staticmethod
    def _capability_keys() -> tuple[str, ...]:
        return ("flash_attention", "gpu_offload", "unified_kv", "kv_cache_type", "kv_offload")

    @staticmethod
    def _capability_state(value: Any) -> str:
        return "supported" if value is True else "unsupported" if value is False else "not-reported"
