from __future__ import annotations

import math
import re


class FixedSizeChunker:
    """
    Split text into fixed-size chunks with optional overlap.

    Rules:
        - Each chunk is at most chunk_size characters long.
        - Consecutive chunks share overlap characters.
        - The last chunk contains whatever remains.
        - If text is shorter than chunk_size, return [text].
    """

    def __init__(self, chunk_size: int = 500, overlap: int = 50) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        if len(text) <= self.chunk_size:
            return [text]

        step = self.chunk_size - self.overlap
        chunks: list[str] = []
        for start in range(0, len(text), step):
            chunk = text[start : start + self.chunk_size]
            chunks.append(chunk)
            if start + self.chunk_size >= len(text):
                break
        return chunks


class SentenceChunker:
    """
    Split text into chunks of at most max_sentences_per_chunk sentences.

    Sentence detection: split on ". ", "! ", "? " or ".\n".
    Strip extra whitespace from each chunk.
    """

    def __init__(self, max_sentences_per_chunk: int = 3) -> None:
        self.max_sentences_per_chunk = max(1, max_sentences_per_chunk)

    def chunk(self, text: str) -> list[str]:
        if not text or not text.strip():
            return []

        # Split on sentence boundaries while retaining sentence text
        # Lookbehind (?<=[.!?]) followed by whitespace or newline
        raw_sentences = re.split(r"(?<=[.!?])(?:\s+|\n+)", text.strip())
        sentences = [s.strip() for s in raw_sentences if s.strip()]

        if not sentences:
            return []

        chunks: list[str] = []
        for i in range(0, len(sentences), self.max_sentences_per_chunk):
            group = sentences[i : i + self.max_sentences_per_chunk]
            chunk_str = " ".join(group).strip()
            if chunk_str:
                chunks.append(chunk_str)

        return chunks


class RecursiveChunker:
    """
    Recursively split text using separators in priority order.

    Default separator priority:
        ["\n\n", "\n", ". ", " ", ""]
    """

    DEFAULT_SEPARATORS = ["\n\n", "\n", ". ", " ", ""]

    def __init__(self, separators: list[str] | None = None, chunk_size: int = 500) -> None:
        self.separators = self.DEFAULT_SEPARATORS if separators is None else list(separators)
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> list[str]:
        if not text:
            return []
        if len(text) <= self.chunk_size:
            return [text]
        return self._split(text, list(self.separators))

    def _split(self, current_text: str, remaining_separators: list[str]) -> list[str]:
        if not current_text:
            return []
        if len(current_text) <= self.chunk_size:
            return [current_text]

        # Base case: no remaining separators to split with
        if not remaining_separators:
            # Fall back to slicing by chunk_size
            return [
                current_text[i : i + self.chunk_size]
                for i in range(0, len(current_text), self.chunk_size)
            ]

        separator = remaining_separators[0]
        next_separators = remaining_separators[1:]

        # Split by the current separator
        if separator == "":
            splits = list(current_text)
        elif separator in current_text:
            splits = current_text.split(separator)
        else:
            # Separator not found in text, try next separator
            return self._split(current_text, next_separators)

        # Process each piece (if still too large, split recursively)
        pieces: list[str] = []
        for split_piece in splits:
            if not split_piece:
                continue
            if len(split_piece) > self.chunk_size:
                pieces.extend(self._split(split_piece, next_separators))
            else:
                pieces.append(split_piece)

        if not pieces:
            return []

        # Merge adjacent pieces up to chunk_size
        chunks: list[str] = []
        current_batch: list[str] = []
        current_len = 0

        for piece in pieces:
            piece_len = len(piece)
            sep_len = len(separator) if (current_batch and separator) else 0

            if current_batch and (current_len + sep_len + piece_len > self.chunk_size):
                merged = separator.join(current_batch).strip() if separator else "".join(current_batch)
                if merged:
                    chunks.append(merged)
                current_batch = [piece]
                current_len = piece_len
            else:
                current_batch.append(piece)
                current_len += sep_len + piece_len

        if current_batch:
            merged = separator.join(current_batch).strip() if separator else "".join(current_batch)
            if merged:
                chunks.append(merged)

        return chunks


def _dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def compute_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    """
    Compute cosine similarity between two vectors.

    cosine_similarity = dot(a, b) / (||a|| * ||b||)

    Returns 0.0 if either vector has zero magnitude.
    """
    if not vec_a or not vec_b or len(vec_a) != len(vec_b):
        return 0.0

    mag_a = math.sqrt(sum(x * x for x in vec_a))
    mag_b = math.sqrt(sum(y * y for y in vec_b))

    if mag_a == 0.0 or mag_b == 0.0:
        return 0.0

    dot_product = _dot(vec_a, vec_b)
    sim = dot_product / (mag_a * mag_b)
    # Clamp to [-1.0, 1.0] to handle slight floating-point inaccuracies
    return max(-1.0, min(1.0, sim))


class ChunkingStrategyComparator:
    """Run all built-in chunking strategies and compare their results."""

    def compare(self, text: str, chunk_size: int = 200) -> dict:
        if not text:
            empty_stat = {"count": 0, "avg_length": 0.0, "chunks": []}
            return {
                "fixed_size": dict(empty_stat),
                "by_sentences": dict(empty_stat),
                "recursive": dict(empty_stat),
            }

        fixed_chunker = FixedSizeChunker(chunk_size=chunk_size, overlap=max(0, chunk_size // 10))
        sentence_chunker = SentenceChunker(max_sentences_per_chunk=3)
        recursive_chunker = RecursiveChunker(chunk_size=chunk_size)

        strategies = {
            "fixed_size": fixed_chunker.chunk(text),
            "by_sentences": sentence_chunker.chunk(text),
            "recursive": recursive_chunker.chunk(text),
        }

        result = {}
        for name, chunks in strategies.items():
            count = len(chunks)
            avg_length = (sum(len(c) for c in chunks) / count) if count > 0 else 0.0
            result[name] = {
                "count": count,
                "avg_length": round(avg_length, 2),
                "chunks": chunks,
            }

        return result
