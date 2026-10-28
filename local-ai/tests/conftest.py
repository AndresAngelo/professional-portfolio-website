"""Deterministic test fixtures for the local-first orchestrator."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest


@dataclass
class FakeClock:
    """A manually advanced UTC clock for tests that need stable timestamps."""

    current: str = "2026-01-01T00:00:00Z"

    def now(self) -> str:
        return self.current

    def advance(self, timestamp: str) -> None:
        self.current = timestamp


@dataclass
class FakeModelPort:
    """Records local model-port calls without opening a network connection."""

    responses: list[Any] = field(default_factory=list)
    requests: list[dict[str, Any]] = field(default_factory=list)

    def request(self, *, payload: dict[str, Any]) -> Any:
        self.requests.append({"model": payload["model"], "payload": payload})
        if not self.responses:
            raise AssertionError("No fake model response was configured.")
        return self.responses.pop(0)


@dataclass
class FakeProcessPort:
    """Records process requests without starting a subprocess."""

    results: list[Any] = field(default_factory=list)
    calls: list[dict[str, Any]] = field(default_factory=list)

    def run(self, *, command: str, cwd: Path) -> Any:
        self.calls.append({"command": command, "cwd": cwd})
        if not self.results:
            raise AssertionError("No fake process result was configured.")
        return self.results.pop(0)


@pytest.fixture
def workspace(tmp_path: Path) -> Path:
    """Return a temporary workspace with storage rooted inside it."""
    (tmp_path / "local-ai").mkdir()
    return tmp_path


@pytest.fixture
def fake_clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def fake_model_port() -> FakeModelPort:
    return FakeModelPort()


@pytest.fixture
def fake_process_port() -> FakeProcessPort:
    return FakeProcessPort()


@pytest.fixture(autouse=True)
def no_network(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Fail fast if a test tries to create an outbound socket connection."""

    def deny_network(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("Network access is forbidden in orchestrator tests.")

    monkeypatch.setattr("socket.create_connection", deny_network)
    monkeypatch.setattr("socket.socket.connect", deny_network)
    yield
