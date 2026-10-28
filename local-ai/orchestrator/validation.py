"""Ordered, audited execution of declared validation commands."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from uuid import uuid4

from .command_guard import CommandAuthorizationError, CommandGuard
from .models import DeclaredCommand, TaskId
from .powershell import PowerShellRunner


@dataclass(frozen=True)
class ValidationRecord:
    """Evidence captured for one declared validation command."""

    command: str
    ordinal: int
    stdout: str
    stderr: str
    exit_code: int
    timestamp: str
    artifact_path: str


class OrderedValidator:
    """Authorize and execute declarations in order, stopping at first failure."""

    def __init__(self, *, task_id: TaskId, workspace: Path, runner: PowerShellRunner) -> None:
        self._task_id = task_id
        self._workspace = workspace.resolve()
        self._runner = runner
        self._guard = CommandGuard()

    def run(self, commands: tuple[DeclaredCommand, ...]) -> list[ValidationRecord]:
        """Run every authorized declaration until the first non-zero exit result."""
        records: list[ValidationRecord] = []
        for command in commands:
            try:
                authorized = self._guard.authorize(
                    candidate=command.canonical_text, declared_commands=commands
                )
            except CommandAuthorizationError as error:
                self._write_rejection(command.canonical_text, error)
                raise
            result = self._runner.run(authorized)
            timestamp = self._timestamp()
            artifact_path = self._write_result(
                command=authorized,
                ordinal=command.ordinal,
                stdout=result.stdout,
                stderr=result.stderr,
                exit_code=result.exit_code,
                timestamp=timestamp,
            )
            records.append(
                ValidationRecord(
                    command=authorized,
                    ordinal=command.ordinal,
                    stdout=result.stdout,
                    stderr=result.stderr,
                    exit_code=result.exit_code,
                    timestamp=timestamp,
                    artifact_path=artifact_path,
                )
            )
            if result.exit_code != 0:
                break
        return records

    @staticmethod
    def _timestamp() -> str:
        return datetime.now(UTC).isoformat()

    def _task_directory(self, root: str) -> Path:
        directory = self._workspace / "local-ai" / root / str(self._task_id).replace(".", "_")
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    def _write_result(
        self,
        *,
        command: str,
        ordinal: int,
        stdout: str,
        stderr: str,
        exit_code: int,
        timestamp: str,
    ) -> str:
        directory = self._task_directory("validation")
        stem = f"{ordinal:03d}-{uuid4().hex}"
        stdout_path = directory / f"{stem}.stdout.txt"
        stderr_path = directory / f"{stem}.stderr.txt"
        metadata_path = directory / f"{stem}.json"
        stdout_path.write_text(stdout, encoding="utf-8")
        stderr_path.write_text(stderr, encoding="utf-8")
        metadata_path.write_text(
            json.dumps(
                {
                    "task_id": str(self._task_id),
                    "command": command,
                    "ordinal": ordinal,
                    "exit_code": exit_code,
                    "timestamp": timestamp,
                    "stdout_path": stdout_path.relative_to(self._workspace).as_posix(),
                    "stderr_path": stderr_path.relative_to(self._workspace).as_posix(),
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        return metadata_path.relative_to(self._workspace).as_posix()

    def _write_rejection(self, command: str, error: CommandAuthorizationError) -> None:
        directory = self._task_directory("protocol-records")
        target = directory / f"{uuid4().hex}-rejected.json"
        target.write_text(
            json.dumps(
                {
                    "task_id": str(self._task_id),
                    "rejected_text": command,
                    "denylist_category": error.category,
                    "timestamp": self._timestamp(),
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
