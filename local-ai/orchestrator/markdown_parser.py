"""Faithful parsing and quarantine-aware queue construction for goal Markdown."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import hashlib
from pathlib import Path
import re

from .config import OrchestratorConfig
from .models import DeclaredCommand, GoalTask, TaskId, TaskQueueRecord
from .quarantine import write_parse_quarantine_report


_TASK_HEADING = re.compile(r"^(#{3,6})\s+(M\d+\.G\d+\.T\d+)\s*:\s*(.+?)\s*$", re.MULTILINE)
_FIELD = re.compile(
    r"^\*\*(Objective|Acceptance Criteria|Prerequisites|Implementation Details|Validation):\*\*\s*",
    re.MULTILINE,
)
_FENCE = re.compile(r"```powershell\s*\n(.*?)\n```", re.IGNORECASE | re.DOTALL)
_PATH_HINT = re.compile(r"`([^`\n]+(?:/|\\)[^`\n]+)`")


class MarkdownParseError(ValueError):
    """Raised when a goal file cannot produce a safe, complete task record."""

    def __init__(self, message: str, *, raw_section: str = "") -> None:
        super().__init__(message)
        self.raw_section = raw_section


@dataclass(frozen=True)
class ParseGoalFilesOutcome:
    """Queueable records plus paths to local evidence for excluded input."""

    queue: tuple[TaskQueueRecord, ...]
    quarantine_reports: tuple[Path, ...]


def _sections(source: str) -> list[tuple[re.Match[str], str]]:
    matches = list(_TASK_HEADING.finditer(source))
    return [(match, source[match.start() : matches[index + 1].start() if index + 1 < len(matches) else len(source)]) for index, match in enumerate(matches)]


def _field(section: str, name: str) -> str:
    matches = list(_FIELD.finditer(section))
    for index, match in enumerate(matches):
        if match.group(1) == name:
            end = matches[index + 1].start() if index + 1 < len(matches) else len(section)
            return section[match.end() : end].strip()
    return ""


def _bullets(value: str) -> tuple[str, ...]:
    return tuple(
        re.sub(r"^[-*]\s+(?:[✓✔]\s*)?", "", line).strip()
        for line in value.splitlines()
        if re.match(r"^[-*]\s+\S", line.strip())
    )


def _canonical_command(raw: str, config: OrchestratorConfig) -> str:
    normalized = raw.replace("\r\n", "\n").strip()
    lines = normalized.splitlines()
    if not lines:
        raise MarkdownParseError("validation command is empty")
    leading_cd = re.fullmatch(r'\s*cd\s+["\'](.+)["\']\s*', lines[0], re.IGNORECASE)
    if leading_cd:
        candidate = Path(leading_cd.group(1)).resolve()
        if candidate not in config.legacy_instruction_migration.accepted_root_aliases:
            raise MarkdownParseError("unrecognized legacy cd root")
        lines = lines[1:]
    elif re.match(r"\s*cd(?:\s|$)", lines[0], re.IGNORECASE):
        raise MarkdownParseError("unrecognized legacy cd root")
    canonical = "\n".join(lines).strip()
    if not canonical:
        raise MarkdownParseError("validation command is empty")
    return canonical


def _parse_section(
    section: str,
    match: re.Match[str],
    source_path: Path,
    source_hash: str,
    config: OrchestratorConfig,
) -> GoalTask:
    try:
        identifier = TaskId.from_string(match.group(2))
    except ValueError as error:
        raise MarkdownParseError("missing parseable task identifier", raw_section=section) from error
    heading = match.group(3).strip()
    objective = _field(section, "Objective")
    criteria = _bullets(_field(section, "Acceptance Criteria"))
    prerequisites = _bullets(_field(section, "Prerequisites"))
    implementation = _field(section, "Implementation Details")
    validation = _field(section, "Validation")
    if not heading or not objective:
        raise MarkdownParseError("missing coding objective", raw_section=section)
    if not criteria:
        raise MarkdownParseError("missing acceptance criteria", raw_section=section)
    blocks = _FENCE.findall(validation)
    if not blocks:
        raise MarkdownParseError("missing declared PowerShell validation block", raw_section=section)
    try:
        commands = tuple(
            DeclaredCommand(raw_text=block.replace("\r\n", "\n").strip(), canonical_text=_canonical_command(block, config), ordinal=index)
            for index, block in enumerate(blocks, start=1)
        )
    except MarkdownParseError as error:
        error.raw_section = section
        raise
    relative = source_path.resolve().relative_to(config.workspace.root).as_posix()
    hints = tuple(dict.fromkeys(_PATH_HINT.findall("\n".join((objective, implementation)))))
    return GoalTask(identifier, relative, source_hash, heading, objective, criteria, prerequisites, implementation, commands, hints)


def parse_goal_file(source_path: Path, config: OrchestratorConfig) -> list[GoalTask]:
    """Parse one file, raising if any task section is incomplete or unsafe."""
    raw_bytes = source_path.read_bytes()
    source = raw_bytes.decode("utf-8")
    source_hash = hashlib.sha256(raw_bytes).hexdigest()
    sections = _sections(source)
    if not sections:
        raise MarkdownParseError("missing parseable task identifier", raw_section=source)
    tasks = [_parse_section(section, match, source_path, source_hash, config) for match, section in sections]
    return sorted(tasks, key=lambda task: task.id.task)


def parse_goal_files(source_paths: tuple[Path, ...] | list[Path], config: OrchestratorConfig) -> ParseGoalFilesOutcome:
    """Parse independent files, quarantining malformed input and duplicate IDs."""
    accepted: list[GoalTask] = []
    reports: list[Path] = []
    for path in source_paths:
        try:
            accepted.extend(parse_goal_file(path, config))
        except MarkdownParseError as error:
            reports.append(write_parse_quarantine_report(config, source_path=path, missing_element=str(error), raw_section=error.raw_section or path.read_text(encoding="utf-8")))
    counts = Counter(str(task.id) for task in accepted)
    duplicates = {identifier for identifier, count in counts.items() if count > 1}
    queueable: list[GoalTask] = []
    for task in accepted:
        if str(task.id) in duplicates:
            reports.append(write_parse_quarantine_report(config, source_path=config.workspace.root / task.source_path, missing_element="duplicate task identifier", raw_section=_raw_task_section(config.workspace.root / task.source_path, str(task.id)), category="duplicate-task-identifier", detail=str(task.id)))
        else:
            queueable.append(task)
    ordered = sorted(queueable, key=lambda task: task.id)
    return ParseGoalFilesOutcome(tuple(TaskQueueRecord(task, ordinal) for ordinal, task in enumerate(ordered, start=1)), tuple(reports))


def _raw_task_section(path: Path, identifier: str) -> str:
    source = path.read_text(encoding="utf-8")
    for match, section in _sections(source):
        if match.group(2) == identifier:
            return section
    return source
