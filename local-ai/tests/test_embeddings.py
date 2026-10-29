"""Retrieval index contracts, using fake vectors only."""

from __future__ import annotations

from pathlib import Path

from orchestrator.embeddings import (
    DOCUMENT_PREFIX,
    QUERY_PREFIX,
    EmbeddingIndex,
    build_index,
    chunk_markdown,
    query_index,
)


class FakeEmbedder:
    """Maps text to a 2-D vector: 'alpha' texts point along x, everything else along y."""

    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def embed(self, texts, *, task_id=None):
        self.calls.append(list(texts))
        return [[1.0, 0.0] if "alpha" in t else [0.0, 1.0] for t in texts]


def test_chunks_split_at_headings_and_respect_the_size_limit() -> None:
    text = "intro\n\n# One\nalpha\n\n## Two\n" + ("word " * 100 + "\n\n") * 4
    chunks = chunk_markdown(text, "doc.md", max_chars=300)
    assert [c.heading for c in chunks][:2] == ["", "One"]
    assert all(len(c.text) <= 300 for c in chunks)
    assert len({c.chunk_id for c in chunks}) == len(chunks)


def test_only_new_or_changed_chunks_are_embedded_again() -> None:
    embedder = FakeEmbedder()
    first = chunk_markdown("# A\nalpha\n\n# B\nbeta", "d.md")
    index, embedded = build_index(first, embedder, "m1", None)
    assert embedded == 2

    changed = chunk_markdown("# A\nalpha\n\n# B\nbeta changed", "d.md")
    _, embedded_again = build_index(changed, embedder, "m1", index)
    assert embedded_again == 1
    assert embedder.calls[-1] == [DOCUMENT_PREFIX + "# B\nbeta changed"]


def test_a_different_model_rebuilds_every_vector() -> None:
    embedder = FakeEmbedder()
    chunks = chunk_markdown("# A\nalpha\n\n# B\nbeta", "d.md")
    index, _ = build_index(chunks, embedder, "m1", None)
    _, embedded = build_index(chunks, embedder, "m2", index)
    assert embedded == 2


def test_query_ranks_by_cosine_and_uses_the_query_prefix() -> None:
    embedder = FakeEmbedder()
    chunks = chunk_markdown("# A\nalpha\n\n# B\nbeta", "d.md")
    index, _ = build_index(chunks, embedder, "m1", None)
    hits = query_index(index, embedder, "alpha please", k=2)
    assert hits[0].chunk.heading == "A" and hits[0].score > hits[1].score
    assert embedder.calls[-1] == [QUERY_PREFIX + "alpha please"]


def test_index_round_trips_atomically_and_a_corrupt_file_is_ignored(workspace: Path) -> None:
    chunks = chunk_markdown("# A\nalpha", "d.md")
    index, _ = build_index(chunks, FakeEmbedder(), "m1", None)
    target = index.save(workspace)
    assert EmbeddingIndex.load(workspace).entries[0].vector == (1.0, 0.0)
    target.write_text("{not json", encoding="utf-8")
    assert EmbeddingIndex.load(workspace) is None
