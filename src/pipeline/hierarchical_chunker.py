"""
Hierarchical Chunker for YouTube Transcripts
Implements 3-level chunking strategy: Chapters → Semantic → Sentence boundaries
"""

import os
from dataclasses import dataclass

import tiktoken


@dataclass
class KnowledgeChunk:
    """Represents a knowledge chunk for the database."""

    id: str
    chapter_index: int
    chapter_title: str
    chunk_index: int
    start_time: float
    end_time: float
    text: str
    token_count: int
    sentences: list[str]
    level: str  # 'chapter', 'semantic', or 'sentence'
    overlap_with_previous: bool = False


class HierarchicalChunker:
    """Implements hierarchical chunking strategy."""

    def __init__(
        self, max_tokens: int = 800, min_tokens: int = 200, overlap_percentage: float = 0.15
    ):
        """Initialize the hierarchical chunker."""
        self.max_tokens = max_tokens
        self.min_tokens = min_tokens
        self.overlap_percentage = overlap_percentage

        # Initialize tokenizer
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

        # Sentence model lazy-loaded on first use (optional dependency)
        self._sentence_model = None

        print(f"✅ Hierarchical chunker initialized (max: {max_tokens}, min: {min_tokens} tokens)")

    @property
    def sentence_model(self):
        """Lazy-load sentence transformer for semantic chunking. Returns None if unavailable."""
        if self._sentence_model is None:
            try:
                from sentence_transformers import SentenceTransformer

                model_name = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
                self._sentence_model = SentenceTransformer(model_name)
            except ImportError:
                pass
        return self._sentence_model

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.tokenizer.encode(text))

    def chunk_by_chapters(
        self, chapters: list[dict], chapter_segments: dict[int, list[dict]]
    ) -> list[KnowledgeChunk]:
        """Level 1: Chunk by chapters."""
        chunks = []

        for chapter in chapters:
            chapter_index = chapter["index"]
            segments = chapter_segments.get(chapter_index, [])

            if not segments:
                continue

            # Reconstruct chapter text
            chapter_text = " ".join(seg["text"] for seg in segments if seg["text"].strip())

            if not chapter_text.strip():
                continue

            # Calculate chapter timing
            start_time = min(seg["start_time"] for seg in segments)
            end_time = max(seg["end_time"] for seg in segments)

            # Count tokens
            token_count = self.count_tokens(chapter_text)

            # Create chunk ID
            chunk_id = f"chapter_{chapter_index}"

            # Extract sentences
            sentences = self._extract_sentences(chapter_text)

            chunk = KnowledgeChunk(
                id=chunk_id,
                chapter_index=chapter_index,
                chapter_title=chapter["title"],
                chunk_index=0,
                start_time=start_time,
                end_time=end_time,
                text=chapter_text,
                token_count=token_count,
                sentences=sentences,
                level="chapter",
            )

            chunks.append(chunk)

        print(f"✅ Level 1: Created {len(chunks)} chapter chunks")
        return chunks

    def apply_hierarchical_chunking(
        self, chapter_chunks: list[KnowledgeChunk]
    ) -> list[KnowledgeChunk]:
        """Apply hierarchical chunking to all chapters."""
        final_chunks = []

        for chapter_chunk in chapter_chunks:
            if chapter_chunk.token_count <= self.max_tokens:
                # Chapter fits in one chunk
                final_chunks.append(chapter_chunk)
            else:
                # Apply Level 2: Semantic chunking
                semantic_chunks = self._apply_semantic_chunking(chapter_chunk)

                # Apply Level 3: Sentence chunking to oversized semantic chunks
                for semantic_chunk in semantic_chunks:
                    if semantic_chunk.token_count <= self.max_tokens:
                        final_chunks.append(semantic_chunk)
                    else:
                        sentence_chunks = self._apply_sentence_chunking(semantic_chunk)
                        final_chunks.extend(sentence_chunks)

        print(f"✅ Hierarchical chunking complete: {len(final_chunks)} final chunks")
        return final_chunks

    def _apply_semantic_chunking(self, chapter_chunk: KnowledgeChunk) -> list[KnowledgeChunk]:
        """Level 2: Semantic chunking based on sentence similarity."""
        sentences = chapter_chunk.sentences

        if len(sentences) <= 1:
            return [chapter_chunk]

        if self.sentence_model is None:
            # No embedding model available — skip semantic chunking, fall through to Level 3
            return [chapter_chunk]

        # Get sentence embeddings
        embeddings = self.sentence_model.encode(sentences)

        # Find semantic boundaries using cosine similarity
        boundaries = self._find_semantic_boundaries(embeddings)

        # Create chunks from boundaries
        semantic_chunks = []
        start_idx = 0

        for i, boundary in enumerate(boundaries + [len(sentences)]):
            if boundary > start_idx:
                chunk_sentences = sentences[start_idx:boundary]
                chunk_text = " ".join(chunk_sentences)

                # Skip very small chunks
                if len(chunk_text.strip()) < 50:
                    continue

                token_count = self.count_tokens(chunk_text)

                chunk_id = f"chapter_{chapter_chunk.chapter_index}_semantic_{i}"

                semantic_chunk = KnowledgeChunk(
                    id=chunk_id,
                    chapter_index=chapter_chunk.chapter_index,
                    chapter_title=chapter_chunk.chapter_title,
                    chunk_index=i,
                    start_time=chapter_chunk.start_time,  # Approximate timing
                    end_time=chapter_chunk.end_time,
                    text=chunk_text,
                    token_count=token_count,
                    sentences=chunk_sentences,
                    level="semantic",
                )

                semantic_chunks.append(semantic_chunk)
                start_idx = boundary

        print(f"✅ Level 2: Split chapter into {len(semantic_chunks)} semantic chunks")
        return semantic_chunks

    def _find_semantic_boundaries(self, embeddings, threshold: float = 0.3) -> list[int]:
        """Find semantic boundaries using cosine similarity."""
        import numpy as np

        boundaries = []

        for i in range(1, len(embeddings)):
            # Calculate similarity with previous sentence
            similarity = np.dot(embeddings[i - 1], embeddings[i])

            # If similarity drops below threshold, it's a boundary
            if similarity < threshold:
                boundaries.append(i)

        return boundaries

    def _apply_sentence_chunking(self, semantic_chunk: KnowledgeChunk) -> list[KnowledgeChunk]:
        """Level 3: Sentence-based chunking with overlap."""
        sentences = semantic_chunk.sentences

        if len(sentences) <= 1:
            return [semantic_chunk]

        sentence_chunks = []
        current_sentences = []
        current_tokens = 0
        chunk_index = 0

        for _i, sentence in enumerate(sentences):
            sentence_tokens = self.count_tokens(sentence)

            # Check if adding this sentence would exceed max tokens
            if current_tokens + sentence_tokens > self.max_tokens and current_sentences:
                # Create chunk from current sentences
                chunk_text = " ".join(current_sentences)

                chunk_id = f"chapter_{semantic_chunk.chapter_index}_sentence_{chunk_index}"

                sentence_chunk = KnowledgeChunk(
                    id=chunk_id,
                    chapter_index=semantic_chunk.chapter_index,
                    chapter_title=semantic_chunk.chapter_title,
                    chunk_index=chunk_index,
                    start_time=semantic_chunk.start_time,
                    end_time=semantic_chunk.end_time,
                    text=chunk_text,
                    token_count=current_tokens,
                    sentences=current_sentences.copy(),
                    level="sentence",
                )

                sentence_chunks.append(sentence_chunk)
                chunk_index += 1

                # Start new chunk with overlap
                overlap_size = int(len(current_sentences) * self.overlap_percentage)
                if overlap_size > 0:
                    current_sentences = current_sentences[-overlap_size:]
                    current_tokens = sum(self.count_tokens(s) for s in current_sentences)
                    sentence_chunk.overlap_with_previous = True
                else:
                    current_sentences = []
                    current_tokens = 0

            current_sentences.append(sentence)
            current_tokens += sentence_tokens

        # Add remaining sentences as final chunk
        if current_sentences:
            chunk_text = " ".join(current_sentences)

            chunk_id = f"chapter_{semantic_chunk.chapter_index}_sentence_{chunk_index}"

            sentence_chunk = KnowledgeChunk(
                id=chunk_id,
                chapter_index=semantic_chunk.chapter_index,
                chapter_title=semantic_chunk.chapter_title,
                chunk_index=chunk_index,
                start_time=semantic_chunk.start_time,
                end_time=semantic_chunk.end_time,
                text=chunk_text,
                token_count=current_tokens,
                sentences=current_sentences,
                level="sentence",
            )

            sentence_chunks.append(sentence_chunk)

        print(f"✅ Level 3: Split semantic chunk into {len(sentence_chunks)} sentence chunks")
        return sentence_chunks

    def _extract_sentences(self, text: str) -> list[str]:
        """Extract sentences from text."""
        import pysbd

        segmenter = pysbd.Segmenter(language="en", clean=False)
        sentences = segmenter.segment(text)

        # Clean and filter sentences
        clean_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 5:
                clean_sentences.append(sentence)

        return clean_sentences

    def get_chunking_stats(self, chunks: list[KnowledgeChunk]) -> dict:
        """Get statistics about the chunking process."""
        stats = {
            "total_chunks": len(chunks),
            "levels": {
                "chapter": len([c for c in chunks if c.level == "chapter"]),
                "semantic": len([c for c in chunks if c.level == "semantic"]),
                "sentence": len([c for c in chunks if c.level == "sentence"]),
            },
            "token_stats": {
                "min_tokens": min(c.token_count for c in chunks) if chunks else 0,
                "max_tokens": max(c.token_count for c in chunks) if chunks else 0,
                "avg_tokens": sum(c.token_count for c in chunks) / len(chunks) if chunks else 0,
            },
            "chunks_by_chapter": {},
        }

        # Group by chapter
        for chunk in chunks:
            chapter_idx = chunk.chapter_index
            if chapter_idx not in stats["chunks_by_chapter"]:
                stats["chunks_by_chapter"][chapter_idx] = {
                    "title": chunk.chapter_title,
                    "count": 0,
                    "total_tokens": 0,
                }

            stats["chunks_by_chapter"][chapter_idx]["count"] += 1
            stats["chunks_by_chapter"][chapter_idx]["total_tokens"] += chunk.token_count

        return stats

    def validate_chunks(self, chunks: list[KnowledgeChunk]) -> dict:
        """Validate that chunks meet quality criteria."""
        validation = {
            "total_chunks": len(chunks),
            "valid_chunks": 0,
            "oversized_chunks": 0,
            "undersized_chunks": 0,
            "empty_chunks": 0,
            "issues": [],
        }

        for chunk in chunks:
            if not chunk.text.strip():
                validation["empty_chunks"] += 1
                validation["issues"].append(f"Empty chunk: {chunk.id}")
            elif chunk.token_count > self.max_tokens:
                validation["oversized_chunks"] += 1
                validation["issues"].append(
                    f"Oversized chunk: {chunk.id} ({chunk.token_count} tokens)"
                )
            elif chunk.token_count < self.min_tokens:
                validation["undersized_chunks"] += 1
                validation["issues"].append(
                    f"Undersized chunk: {chunk.id} ({chunk.token_count} tokens)"
                )
            else:
                validation["valid_chunks"] += 1

        return validation


def main():
    """Test the hierarchical chunker."""
    import json

    try:
        # Load extracted chapters
        with open("extracted_chapters.json") as f:
            chapter_data = json.load(f)

        chapters = chapter_data["chapters"]
        chapter_segments = chapter_data["chapter_segments"]

        print(f"Loaded {len(chapters)} chapters")

        # Initialize chunker
        chunker = HierarchicalChunker(max_tokens=800, min_tokens=200)

        # Level 1: Chunk by chapters
        chapter_chunks = chunker.chunk_by_chapters(chapters, chapter_segments)

        # Apply hierarchical chunking
        final_chunks = chunker.apply_hierarchical_chunking(chapter_chunks)

        # Get statistics
        stats = chunker.get_chunking_stats(final_chunks)
        validation = chunker.validate_chunks(final_chunks)

        print("\n=== Chunking Statistics ===")
        print(f"Total chunks: {stats['total_chunks']}")
        print(f"Levels: {stats['levels']}")
        print(f"Token stats: {stats['token_stats']}")

        print("\n=== Validation Results ===")
        print(f"Valid chunks: {validation['valid_chunks']}")
        print(f"Oversized chunks: {validation['oversized_chunks']}")
        print(f"Undersized chunks: {validation['undersized_chunks']}")
        print(f"Empty chunks: {validation['empty_chunks']}")

        # Show sample chunks
        print("\n=== Sample Chunks ===")
        for i, chunk in enumerate(final_chunks[:3]):
            print(f"{i+1}. {chunk.id} ({chunk.level})")
            print(f"   Chapter: {chunk.chapter_title}")
            print(f"   Tokens: {chunk.token_count}")
            print(f"   Text: {chunk.text[:100]}...")
            print()

        # Save results
        output_data = {
            "metadata": chapter_data["metadata"],
            "chunks": [
                {
                    "id": chunk.id,
                    "chapter_index": chunk.chapter_index,
                    "chapter_title": chunk.chapter_title,
                    "chunk_index": chunk.chunk_index,
                    "start_time": chunk.start_time,
                    "end_time": chunk.end_time,
                    "text": chunk.text,
                    "token_count": chunk.token_count,
                    "sentences": chunk.sentences,
                    "level": chunk.level,
                    "overlap_with_previous": chunk.overlap_with_previous,
                }
                for chunk in final_chunks
            ],
            "stats": stats,
            "validation": validation,
        }

        with open("hierarchical_chunks.json", "w") as f:
            json.dump(output_data, f, indent=2)

        print("✅ Results saved to hierarchical_chunks.json")

    except FileNotFoundError:
        print("❌ Chapter data not found. Run chapter_extractor.py first.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
