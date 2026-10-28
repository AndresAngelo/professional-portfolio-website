"""Configured numeric discovery of populated goal Markdown files."""

from __future__ import annotations

from pathlib import Path

from .config import OrchestratorConfig


def discover_goal_files(config: OrchestratorConfig) -> list[Path]:
    """Return non-blank enabled goal files in numeric milestone/goal order.

    Discovery deliberately iterates the configured enabled coordinates rather than
    recursively scanning the specs tree, so disabled future milestones cannot enter
    the queue.
    """
    candidates: list[tuple[int, int, str, Path]] = []
    for milestone in config.discovery.enabled_milestones:
        for goal in config.discovery.required_goal_numbers:
            pattern = config.discovery.goal_glob.format(milestone=milestone, goal=goal)
            for path in config.workspace.spec_root.glob(pattern):
                if path.is_file() and path.read_text(encoding="utf-8").strip():
                    resolved = path.resolve()
                    candidates.append((milestone, goal, resolved.as_posix(), resolved))
    return [path for _, _, _, path in sorted(candidates)]
