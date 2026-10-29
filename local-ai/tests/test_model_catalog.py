"""Startup model verification: exact identifiers, one loaded match per role, and the context cap.

The catalog shapes below mirror what LM Studio returned during the live check.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

from orchestrator.config import LmStudioConfig, ModelRole, ModelRoles
from orchestrator.model_catalog import (
    ModelVerificationError,
    base_key,
    label_key,
    verify_models,
    write_snapshot,
)
from orchestrator.transport import LoopbackHttpTransport, TransportError

V1 = "http://127.0.0.1:1234/v1"


def lm_config() -> LmStudioConfig:
    return LmStudioConfig(
        base_url=V1,
        request_timeout_seconds=12,
        allow_loopback_only=True,
        models=ModelRoles(
            embedding=ModelRole("embed-text-embedding-nomic-embed-text-v1.5", 2048, 0, 8192),
            router=ModelRole("1b-gemma-3-1b-it-qat", 2048, 512, 6144),
            executor=ModelRole("1b-gemma-4-e2b-it-qat", 4096, 1024, 12288),
        ),
    )


def native(model_id: str, state: str, loaded: int | None, maximum: int = 131072) -> dict[str, Any]:
    return {"id": model_id, "state": state, "loaded_context_length": loaded, "max_context_length": maximum}


def live_shaped_catalog(
    *,
    router_context: int = 2048,
    executor_context: int = 4096,
    executor_f16_loaded: bool = False,
    include_router: bool = True,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    natives = [
        native("text-embedding-nomic-embed-text-v1.5", "loaded", 2048, 2048),
        native("gemma-3-1b-it-qat", "loaded", router_context, 32768),
        native("gemma-4-e2b-it-qat@q4_k_xl", "loaded", executor_context),
        native("gemma-4-e2b-it-qat@f16", "loaded" if executor_f16_loaded else "not-loaded", None),
        native("google/gemma-4-e4b", "not-loaded", None),
    ]
    if not include_router:
        natives = [item for item in natives if item["id"] != "gemma-3-1b-it-qat"]
    listed = [{"id": item["id"], "object": "model"} for item in natives]
    return listed, natives


@dataclass
class FakeCatalog:
    listed: list[dict[str, Any]]
    native: list[dict[str, Any]] | Exception
    calls: list[str] = field(default_factory=list)

    def request(self, *, method: str, url: str, payload: dict[str, Any] | None, timeout: int) -> dict[str, Any]:
        self.calls.append(f"{method} {url}")
        if url.endswith("/v1/models"):
            return {"object": "list", "data": self.listed}
        if url.endswith("/api/v0/models"):
            if isinstance(self.native, Exception):
                raise self.native
            return {"object": "list", "data": self.native}
        raise AssertionError(f"unexpected request to {url}")


def test_labels_resolve_to_the_exact_loaded_identifiers_and_both_endpoints_are_read() -> None:
    """Each label binds to its one loaded identifier; the executor's unloaded F16 variant is ignored."""
    listed, natives = live_shaped_catalog()
    transport = FakeCatalog(listed, natives)

    verification = verify_models(lm_config(), transport)

    assert verification.ok
    resolved = {binding.role: binding.model_id for binding in verification.bindings}
    assert resolved == {
        "embedding": "text-embedding-nomic-embed-text-v1.5",
        "router": "gemma-3-1b-it-qat",
        "executor": "gemma-4-e2b-it-qat@q4_k_xl",
    }
    assert transport.calls == [
        "GET http://127.0.0.1:1234/v1/models",
        "GET http://127.0.0.1:1234/api/v0/models",
    ]
    routable = verification.routable_roles(lm_config().models)
    assert routable.executor.model_id == "gemma-4-e2b-it-qat@q4_k_xl"
    assert routable.executor.max_prompt_bytes == 12288


def test_context_mismatch_blocks_the_role_and_says_how_to_fix_it() -> None:
    """A router loaded above its cap is blocked, even though its identifier resolved."""
    listed, natives = live_shaped_catalog(router_context=16128)

    verification = verify_models(lm_config(), FakeCatalog(listed, natives))

    router = next(binding for binding in verification.bindings if binding.role == "router")
    assert not verification.ok
    assert not router.verified
    assert router.model_id == "gemma-3-1b-it-qat"
    assert any("reload it in LM Studio with context length 2048" in problem for problem in router.problems)


def test_diagnostic_mode_reports_the_context_mismatch_as_a_warning_only() -> None:
    """Diagnostics may route to a role, but the mismatch stays visible and is never silent."""
    listed, natives = live_shaped_catalog(router_context=16128)

    verification = verify_models(lm_config(), FakeCatalog(listed, natives), enforce_context=False)

    router = next(binding for binding in verification.bindings if binding.role == "router")
    assert verification.ok
    assert router.problems == ()
    assert any("16128" in warning for warning in router.warnings)


def test_two_loaded_variants_of_one_model_are_ambiguous() -> None:
    """Two loaded matches for one label cannot be bound safely."""
    listed, natives = live_shaped_catalog(executor_f16_loaded=True)

    verification = verify_models(lm_config(), FakeCatalog(listed, natives))

    executor = next(binding for binding in verification.bindings if binding.role == "executor")
    assert executor.model_id is None
    assert any("expected exactly one loaded match" in problem for problem in executor.problems)


def test_a_model_missing_from_the_listing_is_reported_by_role() -> None:
    """A configured label with no listed match blocks only its own role."""
    listed, natives = live_shaped_catalog(include_router=False)

    verification = verify_models(lm_config(), FakeCatalog(listed, natives))

    assert not verification.ok
    assert verification.problems() == ["router: no model in GET /v1/models matches '1b-gemma-3-1b-it-qat'"]


def test_an_unreadable_status_endpoint_fails_closed() -> None:
    """Without load state, no role may be bound, so verification raises instead of guessing."""
    listed, _ = live_shaped_catalog()
    transport = FakeCatalog(listed, RuntimeError("status endpoint unavailable"))

    with pytest.raises(ModelVerificationError, match="could not read the LM Studio catalog"):
        verify_models(lm_config(), transport)


def test_the_loopback_transport_refuses_other_hosts_before_connecting() -> None:
    """A remote host is refused locally, so no socket is ever opened for it."""
    with pytest.raises(TransportError, match="only http://127.0.0.1"):
        LoopbackHttpTransport().request(
            method="GET", url="http://192.168.1.10:1234/v1/models", payload=None, timeout=1
        )


def test_snapshot_records_pass_and_fail_evidence_under_local_telemetry(workspace: Path) -> None:
    """Every verification leaves a workspace-local snapshot with its bindings and catalog."""
    listed, natives = live_shaped_catalog(router_context=16128)
    verification = verify_models(lm_config(), FakeCatalog(listed, natives))

    snapshot = write_snapshot(workspace, verification)

    assert snapshot.parent == workspace / "local-ai" / "telemetry" / "runtime"
    text = snapshot.read_text(encoding="utf-8")
    assert '"ok": false' in text
    assert "gemma-4-e2b-it-qat@q4_k_xl" in text


def test_label_normalization_strips_display_prefixes_and_publisher_and_quantization() -> None:
    """Only UI display prefixes are removed; publisher and quantization suffixes are compared away."""
    assert label_key("1b-gemma-3-1b-it-qat") == "gemma-3-1b-it-qat"
    assert label_key("embed-text-embedding-nomic-embed-text-v1.5") == "text-embedding-nomic-embed-text-v1.5"
    assert base_key("gemma-4-e2b-it-qat@q4_k_xl") == "gemma-4-e2b-it-qat"
    assert base_key("google/gemma-4-e4b") == "gemma-4-e4b"
