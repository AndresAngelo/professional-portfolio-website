"""Local retrieval index: heading-aware chunks, nomic embeddings, atomic JSON storage, cosine top-k."""

from __future__ import annotations

import json
import math
import os
import re
import tempfile
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
from typing import Protocol

from .config import OrchestratorConfig
from .discovery import discover_goal_files

CHUNK_CHARS = 1500
EMBED_BATCH = 16
DOCUMENT_PREFIX = "search_document: "
QUERY_PREFIX = "search_query: "
INDEX_RELATIVE = "local-ai/embeddings/index.json"
_HEADING = re.compile(r"^#{1,6}\s")


class Embedder(Protocol):
    def embed(self, texts: list[str], *, task_id: str | None = None) -> list[list[float]]: ...


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    source: str
    heading: str
    text: str

    @property
    def digest(self) -> str:
        return sha256(self.text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class IndexedChunk:
    chunk: Chunk
    digest: str
    vector: tuple[float, ...]


@dataclass(frozen=True)
class SearchHit:
    chunk: Chunk
    score: float


def _split_long(text: str, limit: int) -> list[str]:
    pieces: list[str] = []
    current = ""
    for paragraph in re.split(r"\n\s*\n", text):
        while len(paragraph) > limit:
            if current:
                pieces.append(current)
                current = ""
            pieces.append(paragraph[:limit])
            paragraph = paragraph[limit:]
        candidate = f"{current}\n\n{paragraph}" if current else paragraph
        if len(candidate) > limit and current:
            pieces.append(current)
            current = paragraph
        else:
            current = candidate
    if current.strip():
        pieces.append(current)
    return pieces


def chunk_markdown(text: str, source: str, max_chars: int = CHUNK_CHARS) -> list[Chunk]:
    """Split at headings, then at paragraph boundaries so no chunk exceeds ``max_chars``."""
    text = text.replace("\r\n", "\n")
    sections: list[tuple[str, list[str]]] = [("", [])]
    for line in text.split("\n"):
        if _HEADING.match(line):
            sections.append((line.lstrip("# ").strip(), [line]))
        else:
            sections[-1][1].append(line)
    chunks: list[Chunk] = []
    for heading, lines in sections:
        body = "\n".join(lines).strip()
        if not body:
            continue
        for piece in _split_long(body, max_chars):
            chunks.append(Chunk(f"{source}#{len(chunks) + 1}", source, heading, piece))
    return chunks


def collect_chunks(config: OrchestratorConfig) -> list[Chunk]:
    """Chunk the master files, the pipeline context files, and the enabled M1-M5 goal files."""
    root = config.workspace.root
    paths: list[Path] = sorted((root / "Artifacts" / "master-files").glob("*.md"))
    paths += sorted((root / "local-ai" / "context").glob("*.md"))
    paths += discover_goal_files(config)
    chunks: list[Chunk] = []
    for path in paths:
        relative = path.resolve().relative_to(root).as_posix()
        chunks += chunk_markdown(path.read_text(encoding="utf-8"), relative)
    return chunks


def cosine(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return dot / norm if norm else 0.0


class EmbeddingIndex:
    """Chunk vectors tied to the model that produced them."""

    def __init__(self, model_id: str, entries: list[IndexedChunk]) -> None:
        self.model_id = model_id
        self.entries = entries

    def to_dict(self) -> dict[str, object]:
        return {
            "model_id": self.model_id,
            "chunks": [
                {
                    "chunk_id": e.chunk.chunk_id, "source": e.chunk.source, "heading": e.chunk.heading,
                    "text": e.chunk.text, "sha256": e.digest, "vector": list(e.vector),
                }
                for e in self.entries
            ],
        }

    @classmethod
    def from_dict(cls, value: dict) -> EmbeddingIndex:
        entries = [
            IndexedChunk(
                Chunk(str(c["chunk_id"]), str(c["source"]), str(c["heading"]), str(c["text"])),
                str(c["sha256"]),
                tuple(float(x) for x in c["vector"]),
            )
            for c in value["chunks"]
        ]
        return cls(str(value["model_id"]), entries)

    def save(self, workspace: Path) -> Path:
        target = workspace / INDEX_RELATIVE
        target.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temp_name = tempfile.mkstemp(prefix=".index.", dir=target.parent)
        try:
            with os.fdopen(descriptor, "wb") as handle:
                handle.write(json.dumps(self.to_dict()).encode("utf-8"))
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_name, target)
        finally:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
        return target

    @classmethod
    def load(cls, workspace: Path) -> EmbeddingIndex | None:
        target = workspace / INDEX_RELATIVE
        if not target.is_file():
            return None
        try:
            return cls.from_dict(json.loads(target.read_text(encoding="utf-8")))
        except (OSError, ValueError, KeyError, TypeError):
            return None  # An unreadable index is rebuilt rather than trusted.

    def search(self, query_vector: list[float], k: int = 5) -> list[SearchHit]:
        query = tuple(query_vector)
        scored = [SearchHit(e.chunk, cosine(query, e.vector)) for e in self.entries]
        scored.sort(key=lambda hit: (-hit.score, hit.chunk.chunk_id))
        return scored[:k]


def build_index(
    chunks: list[Chunk], embedder: Embedder, model_id: str, existing: EmbeddingIndex | None
) -> tuple[EmbeddingIndex, int]:
    """Embed only chunks whose text hash is new or whose model changed. Returns (index, embedded_count)."""
    reusable: dict[tuple[str, str], tuple[float, ...]] = {}
    if existing is not None and existing.model_id == model_id:
        reusable = {(e.chunk.chunk_id, e.digest): e.vector for e in existing.entries}
    pending = [c for c in chunks if (c.chunk_id, c.digest) not in reusable]
    for start in range(0, len(pending), EMBED_BATCH):
        batch = pending[start : start + EMBED_BATCH]
        vectors = embedder.embed([DOCUMENT_PREFIX + c.text for c in batch])
        for chunk, vector in zip(batch, vectors):
            reusable[(chunk.chunk_id, chunk.digest)] = tuple(vector)
    entries = [IndexedChunk(c, c.digest, reusable[(c.chunk_id, c.digest)]) for c in chunks]
    return EmbeddingIndex(model_id, entries), len(pending)


def query_index(index: EmbeddingIndex, embedder: Embedder, text: str, k: int = 5) -> list[SearchHit]:
    vector = embedder.embed([QUERY_PREFIX + text])[0]
    return index.search(vector, k)
