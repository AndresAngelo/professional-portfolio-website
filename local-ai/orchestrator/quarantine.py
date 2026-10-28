"""Workspace-local quarantine reports for unsafe or malformed parsed sources."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from .config import OrchestratorConfig, derive_artifact_path


def write_parse_quarantine_report(
    config: OrchestratorConfig,
    *,
    source_path: Path,
    missing_element: str,
    raw_section: str,
    category: str = "parse-failure",
    detail: str | None = None,
) -> Path:
    """Write local evidence for an excluded source section and return its path."""
    relative_source = source_path.resolve().relative_to(config.workspace.root).as_posix()
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    report = derive_artifact_path(
        workspace=config.workspace.root,
        artifact_kind="quarantine",
        task_id="parse",
        relative_name=f"{timestamp}.md",
    )
    report.parent.mkdir(parents=True, exist_ok=True)
    extra = f"\n- **Detail:** {detail}" if detail else ""
    report.write_text(
        f"# Quarantine: parsed goal input\n\n"
        f"- **Category:** {category}\n"
        f"- **Source:** `{relative_source}`\n"
        f"- **Missing or invalid element:** {missing_element}\n"
        f"- **Parser timestamp:** {datetime.now(UTC).isoformat()}"
        f"{extra}\n\n## Raw Markdown section\n\n{raw_section}\n",
        encoding="utf-8",
    )
    return report


def write_state_quarantine_report(
    *,
    workspace: Path,
    category: str,
    detail: str,
    evidence: str | None = None,
) -> Path:
    """Persist workspace-local scheduler-state evidence without touching source files."""
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    report = (workspace.resolve() / "local-ai" / "quarantine" / f"{timestamp}-{category}.md").resolve()
    try:
        report.relative_to((workspace.resolve() / "local-ai").resolve())
    except ValueError as error:
        raise ValueError("state quarantine report must remain workspace-local") from error
    report.parent.mkdir(parents=True, exist_ok=True)
    evidence_section = f"\n## Evidence\n\n```text\n{evidence}\n```\n" if evidence else ""
    report.write_text(
        "# Quarantine: Run State\n\n"
        f"- **Category:** {category}\n"
        f"- **Recorded:** `{datetime.now(UTC).isoformat()}`\n"
        f"- **Detail:** {detail}\n"
        "- **Recovery:** task execution is refused until valid state is restored\n"
        f"{evidence_section}",
        encoding="utf-8",
    )
    return report


def write_validation_failure_quarantine_report(
    *,
    workspace: Path,
    task_id: object,
    mode_history: list[object],
    validation_artifact_paths: list[str],
    changed_workspace_paths: list[str],
    retry_count: int,
    validation_evidence: list[dict[str, object]] | None = None,
) -> Path:
    """Write terminal validation evidence without changing workspace source files."""
    root = workspace.resolve()
    timestamp = datetime.now(UTC)
    report = root / "local-ai" / "quarantine" / f"{timestamp.strftime('%Y%m%dT%H%M%S%fZ')}-validation-permanent-failure.md"
    report.parent.mkdir(parents=True, exist_ok=True)

    evidence_rows: list[str] = []
    for failure in validation_evidence or []:
        evidence_rows.extend(
            [
                f"### `{failure['artifact_path']}`",
                f"- **Command:** `{failure['command']}`",
                f"- **Exit code:** {failure['exit_code']}",
                "- **Standard output:**",
                "```text",
                str(failure['stdout']),
                "```",
                "- **Standard error:**",
                "```text",
                str(failure['stderr']),
                "```",
            ]
        )
    for artifact_path in validation_artifact_paths:
        artifact = (root / artifact_path).resolve()
        if not artifact.is_relative_to(root / "local-ai"):
            continue
        stdout = ""
        stderr = ""
        exit_code = "unknown"
        command = "unknown"
        try:
            import json

            data = json.loads(artifact.read_text(encoding="utf-8"))
            command = str(data.get("command", command))
            exit_code = str(data.get("exit_code", exit_code))
            stdout_path = root / str(data.get("stdout_path", ""))
            stderr_path = root / str(data.get("stderr_path", ""))
            if stdout_path.is_file():
                stdout = stdout_path.read_text(encoding="utf-8")
            if stderr_path.is_file():
                stderr = stderr_path.read_text(encoding="utf-8")
        except (OSError, ValueError):
            pass
        evidence_rows.extend(
            [
                f"### `{artifact_path}`",
                f"- **Command:** `{command}`",
                f"- **Exit code:** {exit_code}",
                "- **Standard output:**",
                "```text",
                stdout,
                "```",
                "- **Standard error:**",
                "```text",
                stderr,
                "```",
            ]
        )

    history = " → ".join(getattr(mode, "value", str(mode)) for mode in mode_history)
    changed = "\n".join(f"- `{path}`" for path in changed_workspace_paths) or "- None recorded"
    artifacts = "\n".join(f"- `{path}`" for path in validation_artifact_paths) or "- None recorded"
    validation_text = "\n".join(evidence_rows) if evidence_rows else "No readable validation artifacts were available."
    report.write_text(
        f"# Quarantine: {task_id}\n\n"
        "- **Category:** validation-permanent-failure\n"
        f"- **Recorded:** `{timestamp.isoformat()}`\n"
        "- **Recovery:** partial workspace changes preserved; task marked quarantined\n"
        f"- **Error-mode retry count:** {retry_count}\n\n"
        "## Mode history\n\n"
        f"{history}\n\n"
        "## Validation artifact links\n\n"
        f"{artifacts}\n\n"
        "## Validation evidence\n\n"
        f"{validation_text}\n\n"
        "## Changed workspace paths\n\n"
        f"{changed}\n",
        encoding="utf-8",
    )
    return report
