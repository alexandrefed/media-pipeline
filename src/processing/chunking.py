"""
Intelligent text chunking module for AI Knowledge Base.

This module provides context-aware chunking strategies to preserve semantic
meaning while maintaining optimal chunk sizes for vector search.
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

from pydantic import BaseModel


class ChunkingStrategy(str, Enum):
    """Available chunking strategies."""
    SENTENCE_BOUNDARY = "sentence_boundary"
    PARAGRAPH_BOUNDARY = "paragraph_boundary"
    SEMANTIC_BOUNDARY = "semantic_boundary"
    FIXED_SIZE = "fixed_size"


@dataclass
class ChunkBoundary:
    """Information about a chunk boundary."""
    position: int
    score: float
    reason: str


class ChunkingConfig(BaseModel):
    """Configuration for text chunking."""
    strategy: ChunkingStrategy = ChunkingStrategy.SENTENCE_BOUNDARY
    target_size: int = 150  # Target words per chunk
    min_size: int = 50      # Minimum words per chunk
    max_size: int = 300     # Maximum words per chunk
    overlap: int = 20       # Word overlap between chunks
    preserve_sentences: bool = True
    context_window: int = 2  # Sentences for context


class TextChunk(BaseModel):
    """A single text chunk with metadata."""
    text: str
    start_position: int
    end_position: int
    word_count: int
    sentence_count: int
    chunk_index: int
    overlap_before: str
    overlap_after: str
    context_before: str
    context_after: str
    quality_score: float
    contains_entities: List[str]


class IntelligentChunker:
    """Intelligent text chunking with context preservation."""
    
    def __init__(self, config: Optional[ChunkingConfig] = None):
        """Initialize the chunker with configuration."""
        self.config = config or ChunkingConfig()
        
    def chunk_text(self, text: str) -> List[TextChunk]:
        """Chunk text using the configured strategy."""
        # Normalize text
        normalized_text = self._normalize_text(text)
        
        # Find sentence boundaries
        sentences = self._split_into_sentences(normalized_text)
        
        # Find optimal chunk boundaries
        boundaries = self._find_chunk_boundaries(sentences)
        
        # Create chunks
        chunks = self._create_chunks(sentences, boundaries)
        
        return chunks
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text for better chunking."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Fix common transcription issues
        text = re.sub(r'\s+([.!?])', r'\1', text)  # Fix spaced punctuation
        text = re.sub(r'([.!?])\s*([a-z])', r'\1 \2', text)  # Ensure space after punctuation
        
        return text.strip()
    
    def _split_into_sentences(self, text: str) -> List[Dict[str, any]]:
        """Split text into sentences with position information."""
        # Common sentence ending patterns
        sentence_endings = r'[.!?]+(?:\s+|$)'
        
        sentences = []
        current_pos = 0
        
        for match in re.finditer(sentence_endings, text):
            end_pos = match.end()
            sentence_text = text[current_pos:end_pos].strip()
            
            if sentence_text:
                sentences.append({
                    'text': sentence_text,
                    'start_pos': current_pos,
                    'end_pos': end_pos,
                    'word_count': len(sentence_text.split()),
                    'index': len(sentences)
                })
            
            current_pos = end_pos
        
        # Handle remaining text if no final punctuation
        if current_pos < len(text):
            remaining_text = text[current_pos:].strip()
            if remaining_text:
                sentences.append({
                    'text': remaining_text,
                    'start_pos': current_pos,
                    'end_pos': len(text),
                    'word_count': len(remaining_text.split()),
                    'index': len(sentences)
                })
        
        return sentences
    
    def _find_chunk_boundaries(self, sentences: List[Dict[str, any]]) -> List[int]:
        """Find optimal boundaries for chunking."""
        boundaries = [0]  # Always start with first sentence
        
        current_word_count = 0
        
        for i, sentence in enumerate(sentences):
            current_word_count += sentence['word_count']
            
            # Check if we should create a boundary
            if current_word_count >= self.config.target_size:
                # Look ahead to find the best boundary
                best_boundary = self._find_best_boundary(sentences, i)
                
                if best_boundary and best_boundary not in boundaries:
                    boundaries.append(best_boundary)
                    current_word_count = 0
                    
                    # Recalculate word count from the new boundary
                    for j in range(best_boundary, i + 1):
                        current_word_count += sentences[j]['word_count']
        
        return boundaries
    
    def _find_best_boundary(self, sentences: List[Dict[str, any]], current_index: int) -> Optional[int]:
        """Find the best boundary near the current position."""
        # Look for natural boundaries within a small window
        window_size = 3
        start_idx = max(0, current_index - window_size)
        end_idx = min(len(sentences), current_index + window_size)
        
        best_boundary = None
        best_score = 0
        
        for i in range(start_idx, end_idx):
            score = self._calculate_boundary_score(sentences, i)
            if score > best_score:
                best_score = score
                best_boundary = i
        
        return best_boundary if best_boundary is not None else current_index
    
    def _calculate_boundary_score(self, sentences: List[Dict[str, any]], index: int) -> float:
        """Calculate how good a boundary position is."""
        if index >= len(sentences):
            return 0
        
        sentence = sentences[index]
        score = 0
        
        # Prefer boundaries after certain sentence patterns
        text_lower = sentence['text'].lower()
        
        # Higher score for sentences that end topics
        if any(phrase in text_lower for phrase in [
            'now let\'s', 'next step', 'moving on', 'another way',
            'in summary', 'to conclude', 'finally'
        ]):
            score += 2.0
        
        # Medium score for sentences that start new topics
        if any(phrase in text_lower for phrase in [
            'first', 'second', 'then', 'after that', 'meanwhile'
        ]):
            score += 1.5
        
        # Lower score for sentences that seem to continue a thought
        if any(phrase in text_lower for phrase in [
            'also', 'additionally', 'furthermore', 'however', 'but'
        ]):
            score -= 1.0
        
        # Prefer longer sentences as boundaries
        if sentence['word_count'] > 15:
            score += 0.5
        
        return score
    
    def _create_chunks(self, sentences: List[Dict[str, any]], boundaries: List[int]) -> List[TextChunk]:
        """Create chunks from sentences and boundaries."""
        chunks = []
        
        for i in range(len(boundaries)):
            start_boundary = boundaries[i]
            end_boundary = boundaries[i + 1] if i + 1 < len(boundaries) else len(sentences)
            
            # Get sentences for this chunk
            chunk_sentences = sentences[start_boundary:end_boundary]
            
            if not chunk_sentences:
                continue
            
            # Create chunk
            chunk = self._create_single_chunk(chunk_sentences, sentences, i)
            if chunk:
                chunks.append(chunk)
        
        return chunks
    
    def _create_single_chunk(self, chunk_sentences: List[Dict[str, any]], 
                           all_sentences: List[Dict[str, any]], chunk_index: int) -> Optional[TextChunk]:
        """Create a single chunk from sentences."""
        if not chunk_sentences:
            return None
        
        # Combine sentences
        chunk_text = ' '.join(s['text'] for s in chunk_sentences)
        word_count = sum(s['word_count'] for s in chunk_sentences)
        
        # Skip if too small
        if word_count < self.config.min_size:
            return None
        
        # Get positions
        start_pos = chunk_sentences[0]['start_pos']
        end_pos = chunk_sentences[-1]['end_pos']
        
        # Get overlap and context
        overlap_before = self._get_overlap_before(chunk_sentences[0]['index'], all_sentences)
        overlap_after = self._get_overlap_after(chunk_sentences[-1]['index'], all_sentences)
        context_before = self._get_context_before(chunk_sentences[0]['index'], all_sentences)
        context_after = self._get_context_after(chunk_sentences[-1]['index'], all_sentences)
        
        # Calculate quality score
        quality_score = self._calculate_chunk_quality(chunk_text, chunk_sentences)
        
        return TextChunk(
            text=chunk_text,
            start_position=start_pos,
            end_position=end_pos,
            word_count=word_count,
            sentence_count=len(chunk_sentences),
            chunk_index=chunk_index,
            overlap_before=overlap_before,
            overlap_after=overlap_after,
            context_before=context_before,
            context_after=context_after,
            quality_score=quality_score,
            contains_entities=[]  # Will be populated by entity detection
        )
    
    def _get_overlap_before(self, sentence_index: int, all_sentences: List[Dict[str, any]]) -> str:
        """Get overlap text before the chunk."""
        start_idx = max(0, sentence_index - self.config.overlap)
        end_idx = sentence_index
        
        overlap_sentences = all_sentences[start_idx:end_idx]
        return ' '.join(s['text'] for s in overlap_sentences)
    
    def _get_overlap_after(self, sentence_index: int, all_sentences: List[Dict[str, any]]) -> str:
        """Get overlap text after the chunk."""
        start_idx = sentence_index + 1
        end_idx = min(len(all_sentences), sentence_index + 1 + self.config.overlap)
        
        overlap_sentences = all_sentences[start_idx:end_idx]
        return ' '.join(s['text'] for s in overlap_sentences)
    
    def _get_context_before(self, sentence_index: int, all_sentences: List[Dict[str, any]]) -> str:
        """Get context sentences before the chunk."""
        start_idx = max(0, sentence_index - self.config.context_window)
        end_idx = sentence_index
        
        context_sentences = all_sentences[start_idx:end_idx]
        return ' '.join(s['text'] for s in context_sentences)
    
    def _get_context_after(self, sentence_index: int, all_sentences: List[Dict[str, any]]) -> str:
        """Get context sentences after the chunk."""
        start_idx = sentence_index + 1
        end_idx = min(len(all_sentences), sentence_index + 1 + self.config.context_window)
        
        context_sentences = all_sentences[start_idx:end_idx]
        return ' '.join(s['text'] for s in context_sentences)
    
    def _calculate_chunk_quality(self, text: str, sentences: List[Dict[str, any]]) -> float:
        """Calculate quality score for a chunk."""
        score = 5.0  # Base score
        
        # Adjust based on length
        word_count = len(text.split())
        if self.config.target_size * 0.8 <= word_count <= self.config.target_size * 1.2:
            score += 2.0
        elif word_count < self.config.min_size:
            score -= 2.0
        elif word_count > self.config.max_size:
            score -= 1.0
        
        # Adjust based on sentence structure
        if len(sentences) > 1:
            score += 1.0  # Multi-sentence chunks are generally better
        
        # Adjust based on content indicators
        text_lower = text.lower()
        if any(word in text_lower for word in ['step', 'how to', 'configure', 'setup']):
            score += 1.0
        
        # Penalize if too repetitive
        words = text_lower.split()
        unique_words = len(set(words))
        if unique_words / len(words) < 0.5:
            score -= 1.0
        
        # Normalize to 0-1 range as required by database constraint
        return max(0.1, min(1.0, score / 10.0))


def main():
    """Test the chunking system."""
    chunker = IntelligentChunker()
    
    # Test text with AI tools content
    test_text = """
    So I'm using n8n for my automation workflow. First, you need to configure the API endpoints.
    Then you'll want to set up your database connections. Make sure to test each connection thoroughly.
    
    Next, let's move on to setting up the triggers. The webhook trigger is very powerful for real-time processing.
    You can also use the schedule trigger for batch operations. Both are essential for different use cases.
    
    Now let's talk about data transformation. n8n provides excellent tools for manipulating data between services.
    You can use the Code node for custom JavaScript logic. This is where the real power comes from.
    
    Finally, don't forget to set up error handling. Proper error handling is crucial for production workflows.
    Monitor your workflows regularly and set up alerts for failures.
    """
    
    print("🔧 Testing Intelligent Chunking System")
    print("=" * 50)
    
    chunks = chunker.chunk_text(test_text)
    
    print(f"📄 Created {len(chunks)} chunks:")
    
    for i, chunk in enumerate(chunks):
        print(f"\n{i+1}. Chunk {chunk.chunk_index}:")
        print(f"   Words: {chunk.word_count}")
        print(f"   Sentences: {chunk.sentence_count}")
        print(f"   Quality: {chunk.quality_score:.1f}")
        print(f"   Text: {chunk.text[:100]}...")
        
        if chunk.context_before:
            print(f"   Context before: {chunk.context_before[:50]}...")
        if chunk.context_after:
            print(f"   Context after: {chunk.context_after[:50]}...")
    
    print("\n" + "=" * 50)
    print("✅ Chunking system test completed")


if __name__ == "__main__":
    main()