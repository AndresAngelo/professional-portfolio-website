"""Startup verification that binds each model role to one loaded LM Studio model.

LM Studio's OpenAI-compatible ``GET /v1/models`` lists models that exist. The native
``GET /api/v0/models`` reports whether each model is loaded and at what context length.
Requests need the exact identifier, and the prompt budgets assume the loaded context, so
both endpoints are read. Any ambiguity or mismatch is reported as a problem.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

from .config import MODEL_ROLE_NAMES, LmStudioConfig, ModelRole, ModelRoleName, ModelRoles, derive_artifact_path

# UI labels such as "1b-" (size) and "embed-" (type) are not part of LM Studio identifiers.
_LABEL_PREFIX = re.compile(r"^(?:\d+b|embed|llm)-")


class CatalogTransport(Protocol):
    def request(self, *, method: str, url: str, payload: dict[str, Any] | None, timeout: int) -> dict[str, Any]: ...


class ModelVerificationError(RuntimeError):
    """Startup verification could not complete, so no model role may be used."""


@dataclass(frozen=True)
class CatalogEntry:
    model_id: str
    state: str
    loaded_context_length: int | None
    max_context_length: int | None


@dataclass(frozen=True)
class RoleBinding:
    role: ModelRoleName
    label: str
    model_id: str | None
    state: str | None
    configured_context_length: int
    loaded_context_length: int | None
    problems: tuple[str, ...]
    warnings: tuple[str, ...]

    @property
    def verified(self) -> bool:
        return self.model_id is not None and not self.problems


@dataclass(frozen=True)
class Verification:
    bindings: tuple[RoleBinding, ...]
    catalog: tuple[CatalogEntry, ...]

    @property
    def ok(self) -> bool:
        return all(binding.verified for binding in self.bindings)

    def problems(self) -> list[str]:
        return [f"{binding.role}: {problem}" for binding in self.bindings for problem in binding.problems]

    def routable_roles(self, configured: ModelRoles) -> ModelRoles:
        """Return the roles with exact identifiers; a role that did not verify keeps its label.

        Only verified roles may receive requests. The caller is responsible for checking
        ``RoleBinding.verified`` before routing to a role.
        """
        replacements: dict[str, ModelRole] = {}
        for binding in self.bindings:
            if binding.model_id is not None:
                replacements[binding.role] = replace(
                    configured.for_role(binding.role), model_id=binding.model_id
                )
        return ModelRoles(
            embedding=replacements.get("embedding", configured.embedding),
            router=replacements.get("router", configured.router),
            executor=replacements.get("executor", configured.executor),
        )


def base_key(identifier: str) -> str:
    """Strip the publisher prefix and quantization suffix: ``google/x@q4`` becomes ``x``."""
    return identifier.rsplit("/", 1)[-1].split("@", 1)[0].lower()


def label_key(label: str) -> str:
    """Strip the UI display prefix from a configured label, keeping the model's own name."""
    return _LABEL_PREFIX.sub("", label.lower(), count=1)


def fetch_catalog(transport: CatalogTransport, base_url: str, *, timeout: int = 20) -> tuple[CatalogEntry, ...]:
    """Read the listed identifiers and their load state; fail closed if either read fails."""
    v1 = base_url.rstrip("/")
    root = v1.removesuffix("/v1")
    try:
        listed = transport.request(method="GET", url=f"{v1}/models", payload=None, timeout=timeout)
        native = transport.request(method="GET", url=f"{root}/api/v0/models", payload=None, timeout=timeout)
    except (RuntimeError, OSError) as error:
        raise ModelVerificationError(f"could not read the LM Studio catalog: {error}") from error

    listed_ids = {
        item["id"] for item in listed.get("data", []) if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    entries: list[CatalogEntry] = []
    for item in native.get("data", []):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or item["id"] not in listed_ids:
            continue
        loaded = item.get("loaded_context_length")
        maximum = item.get("max_context_length")
        entries.append(
            CatalogEntry(
                model_id=item["id"],
                state=str(item.get("state", "not-reported")),
                loaded_context_length=loaded if isinstance(loaded, int) else None,
                max_context_length=maximum if isinstance(maximum, int) else None,
            )
        )
    return tuple(entries)


def _bind(role: ModelRoleName, configured: ModelRole, catalog: tuple[CatalogEntry, ...], enforce_context: bool) -> RoleBinding:
    label = configured.model_id
    exact = [entry for entry in catalog if entry.model_id == label]
    matches = exact or [entry for entry in catalog if base_key(entry.model_id) == label_key(label)]
    if not matches:
        return RoleBinding(
            role, label, None, None, configured.context_length, None,
            (f"no model in GET /v1/models matches '{label}'",), (),
        )
    loaded = [entry for entry in matches if entry.state == "loaded"]
    if len(loaded) != 1:
        names = ", ".join(f"{entry.model_id} ({entry.state})" for entry in matches)
        return RoleBinding(
            role, label, None, None, configured.context_length, None,
            (f"expected exactly one loaded match for '{label}', found {len(loaded)} among: {names}",), (),
        )
    chosen = loaded[0]
    problems: list[str] = []
    warnings: list[str] = []
    context_note = ""
    if chosen.loaded_context_length is None:
        context_note = f"{chosen.model_id} reports no loaded_context_length, so its context cap cannot be verified"
    elif chosen.loaded_context_length != configured.context_length:
        context_note = (
            f"{chosen.model_id} is loaded at context {chosen.loaded_context_length}, but the configured cap is "
            f"{configured.context_length}; reload it in LM Studio with context length {configured.context_length}"
        )
    if context_note:
        (problems if enforce_context else warnings).append(context_note)
    return RoleBinding(
        role, label, chosen.model_id, chosen.state, configured.context_length,
        chosen.loaded_context_length, tuple(problems), tuple(warnings),
    )


def verify_models(
    config: LmStudioConfig,
    transport: CatalogTransport,
    *,
    roles: tuple[ModelRoleName, ...] = MODEL_ROLE_NAMES,
    enforce_context: bool = True,
) -> Verification:
    """Bind the requested roles to loaded models. ``enforce_context=False`` is for diagnostics only."""
    catalog = fetch_catalog(transport, config.base_url)
    bindings = tuple(_bind(role, config.models.for_role(role), catalog, enforce_context) for role in roles)
    return Verification(bindings=bindings, catalog=catalog)


def write_snapshot(workspace_root: Path, verification: Verification) -> Path:
    """Persist the verification evidence under workspace-local telemetry, pass or fail."""
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    target = derive_artifact_path(
        workspace=workspace_root,
        artifact_kind="telemetry",
        task_id="runtime",
        relative_name=f"startup-models-{timestamp}.json",
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    document = {
        "recorded_at": datetime.now(UTC).isoformat(),
        "ok": verification.ok,
        "bindings": [asdict(binding) for binding in verification.bindings],
        "catalog": [asdict(entry) for entry in verification.catalog],
    }
    target.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target
