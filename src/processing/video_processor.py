"""
Video Processing Pipeline for AI Knowledge Base.

This module orchestrates the complete video processing pipeline:
1. Extract video metadata and transcript using yt-dlp
2. Apply entity correction to fix transcription errors
3. Perform intelligent chunking with context preservation
4. Generate embeddings and store in database
"""

import asyncio
import logging
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel

from ..database.connection import get_database, get_sources_table, get_chunks_table
from .entity_correction import EntityCorrector
from ..pipeline.youtube_extractor import YouTubeExtractor, VideoMetadata, TranscriptSegment
from .transcript_processor import TranscriptProcessor, ProcessedSegment, ProcessingAction

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProcessingConfig(BaseModel):
    """Configuration for video processing."""
    chunk_size: int = 150  # words per chunk
    chunk_overlap: int = 20  # word overlap between chunks
    min_chunk_words: int = 50  # minimum words for a valid chunk
    quality_threshold: float = 3.0  # minimum quality score
    context_window: int = 2  # sentences before/after for context


class ChunkData(BaseModel):
    """Data for a processed chunk."""
    source_id: int
    content: str
    cleaned_content: str
    start_time: float
    end_time: float
    chunk_index: int
    mentioned_tools: List[str]
    mentioned_prices: List[str]
    quality_score: float
    context_before: str
    context_after: str


class VideoProcessor:
    """Main video processing pipeline."""
    
    def __init__(self, config: Optional[ProcessingConfig] = None):
        """Initialize the video processor."""
        self.config = config or ProcessingConfig()
        self.extractor = YouTubeExtractor()
        self.corrector = EntityCorrector()
        self.transcript_processor = TranscriptProcessor()
        self.db = get_database()
        
    async def process_video(self, url: str) -> Dict[str, any]:
        """Process a complete video through the pipeline."""
        try:
            logger.info(f"🎬 Starting video processing: {url}")
            
            # Step 1: Extract video data
            metadata, transcript = self.extractor.extract_video_data(url)
            logger.info(f"📹 Extracted {len(transcript)} transcript segments")
            
            # Step 2: Check if video already exists and is completed
            sources_table = get_sources_table()
            existing_source = await sources_table.get_source_by_url(url)
            
            if existing_source and existing_source['processing_status'] == 'completed':
                logger.info(f"🔄 Video already exists and is completed: {existing_source['id']}")
                return {
                    'status': 'already_exists',
                    'source_id': existing_source['id'],
                    'metadata': metadata.dict()
                }
            elif existing_source:
                logger.info(f"🔄 Video exists but not completed, reprocessing: {existing_source['id']}")
                source_id = existing_source['id']
            else:
                # Step 3: Store video metadata
                source_data = self._prepare_source_data(metadata)
                source_id = await sources_table.insert_source(source_data)
                logger.info(f"💾 Stored video metadata with ID: {source_id}")
            
            # Step 3: Process transcript with Claude Code intelligence
            processed_segments = await self.transcript_processor.process_transcript(transcript)
            logger.info(f"🧠 Claude Code processed {len(processed_segments)} segments")
            logger.info(f"📊 Processing stats: {self.transcript_processor.get_processing_summary()}")
            
            # Step 4: Apply entity correction to processed segments
            corrected_segments = self._apply_entity_correction_to_processed(processed_segments)
            logger.info(f"✅ Applied entity correction to processed segments")
            
            # Step 5: Create intelligent chunks
            chunks = self._create_intelligent_chunks_from_processed(corrected_segments, source_id)
            logger.info(f"📄 Created {len(chunks)} chunks")
            
            # Step 6: Store chunks in database
            chunks_table = get_chunks_table()
            chunk_ids = []
            
            for chunk in chunks:
                chunk_id = await chunks_table.insert_chunk(chunk.dict())
                chunk_ids.append(chunk_id)
            
            logger.info(f"💾 Stored {len(chunk_ids)} chunks in database")
            
            # Step 7: Update processing status
            await self._update_processing_status(source_id, 'completed')
            
            return {
                'status': 'completed',
                'source_id': source_id,
                'chunks_created': len(chunk_ids),
                'metadata': metadata.dict(),
                'processing_stats': {
                    'total_segments': len(transcript),
                    'processed_segments': len(processed_segments),
                    'segments_removed': self.transcript_processor.processing_stats['segments_removed'],
                    'segments_summarized': self.transcript_processor.processing_stats['segments_summarized'],
                    'corrected_segments': len(corrected_segments),
                    'total_chunks': len(chunks),
                    'average_chunk_quality': sum(c.quality_score for c in chunks) / len(chunks) if chunks else 0
                }
            }
            
        except Exception as e:
            logger.error(f"❌ Error processing video {url}: {str(e)}")
            if 'source_id' in locals():
                await self._update_processing_status(source_id, 'failed')
            raise
    
    def _prepare_source_data(self, metadata: VideoMetadata) -> Dict[str, any]:
        """Prepare source data for database insertion."""
        return {
            'url': metadata.url,
            'title': metadata.title,
            'channel_name': metadata.channel_name,
            'channel_id': metadata.channel_id,
            'published_date': metadata.published_date,
            'duration_seconds': metadata.duration_seconds,
            'view_count': metadata.view_count,
            'like_count': metadata.like_count,
            'description': metadata.description,
            'thumbnail_url': metadata.thumbnail_url,
            'quality_score': self._calculate_video_quality(metadata),
            'technical_level': self._determine_technical_level(metadata),
            'content_type': self._determine_content_type(metadata),
            'transcript_available': True,
            'processing_status': 'processing'
        }
    
    def _calculate_video_quality(self, metadata: VideoMetadata) -> float:
        """Calculate video quality score based on metadata."""
        score = 5.0  # Base score
        
        # Adjust based on view count
        if metadata.view_count > 100000:
            score += 1.0
        elif metadata.view_count > 10000:
            score += 0.5
        
        # Adjust based on duration (prefer 5-30 minute videos)
        duration_minutes = metadata.duration_seconds / 60
        if 5 <= duration_minutes <= 30:
            score += 1.0
        elif duration_minutes < 5:
            score -= 1.0
        elif duration_minutes > 60:
            score -= 0.5
        
        # Adjust based on title indicators
        title_lower = metadata.title.lower()
        if any(word in title_lower for word in ['tutorial', 'guide', 'how to', 'demo']):
            score += 1.0
        if any(word in title_lower for word in ['automation', 'workflow', 'ai', 'tools']):
            score += 0.5
        
        # Normalize to 0-1 range as required by database constraint
        return max(0.1, min(1.0, score / 10.0))
    
    def _determine_technical_level(self, metadata: VideoMetadata) -> str:
        """Determine technical level from metadata."""
        title_desc = f"{metadata.title} {metadata.description}".lower()
        
        if any(word in title_desc for word in ['beginner', 'basic', 'intro', 'getting started']):
            return 'beginner'
        elif any(word in title_desc for word in ['advanced', 'expert', 'deep dive', 'complex']):
            return 'advanced'
        else:
            return 'intermediate'
    
    def _determine_content_type(self, metadata: VideoMetadata) -> str:
        """Determine content type from metadata."""
        title_desc = f"{metadata.title} {metadata.description}".lower()
        
        if any(word in title_desc for word in ['tutorial', 'how to', 'guide']):
            return 'tutorial'
        elif any(word in title_desc for word in ['demo', 'demonstration', 'walkthrough']):
            return 'demo'
        elif any(word in title_desc for word in ['review', 'comparison', 'vs']):
            return 'review'
        else:
            return 'tutorial'
    
    def _apply_entity_correction(self, segments: List[TranscriptSegment]) -> List[TranscriptSegment]:
        """Apply entity correction to transcript segments."""
        corrected_segments = []
        
        for segment in segments:
            # Apply entity correction
            correction_result = self.corrector.correct_text(segment.text)
            
            # Create corrected segment
            corrected_segment = TranscriptSegment(
                start_time=segment.start_time,
                end_time=segment.end_time,
                text=correction_result.corrected_text,
                segment_index=segment.segment_index
            )
            
            corrected_segments.append(corrected_segment)
        
        return corrected_segments
    
    def _apply_entity_correction_to_processed(self, processed_segments: List[ProcessedSegment]) -> List[ProcessedSegment]:
        """Apply entity correction to already processed segments."""
        corrected_segments = []
        
        for segment in processed_segments:
            # Apply entity correction to the processed text
            correction_result = self.corrector.correct_text(segment.processed_text)
            
            # Update the segment with corrected text
            segment.processed_text = correction_result.corrected_text
            
            # Update extracted tools with corrected entities
            corrected_tools = [e['corrected'] for e in correction_result.detected_entities 
                             if e['category'] in ['automation', 'development', 'ai_model']]
            segment.extracted_tools.extend(corrected_tools)
            segment.extracted_tools = list(set(segment.extracted_tools))
            
            corrected_segments.append(segment)
        
        return corrected_segments
    
    def _create_intelligent_chunks(self, segments: List[TranscriptSegment], source_id: int) -> List[ChunkData]:
        """Create intelligent chunks with context preservation."""
        chunks = []
        
        # Combine all segments into a single text with timing info
        full_text = ""
        segment_boundaries = []  # Track where each segment starts/ends in the full text
        
        for segment in segments:
            start_pos = len(full_text)
            segment_text = segment.text + " "
            full_text += segment_text
            end_pos = len(full_text)
            
            segment_boundaries.append({
                'start_pos': start_pos,
                'end_pos': end_pos,
                'start_time': segment.start_time,
                'end_time': segment.end_time,
                'segment_index': segment.segment_index
            })
        
        # Split into sentences for better chunk boundaries
        sentences = re.split(r'[.!?]+', full_text)
        sentence_positions = []
        
        current_pos = 0
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                start_pos = full_text.find(sentence, current_pos)
                if start_pos != -1:
                    end_pos = start_pos + len(sentence)
                    sentence_positions.append({
                        'text': sentence,
                        'start_pos': start_pos,
                        'end_pos': end_pos
                    })
                    current_pos = end_pos
        
        # Create chunks based on word count
        current_chunk_sentences = []
        current_word_count = 0
        chunk_index = 0
        
        for i, sentence_info in enumerate(sentence_positions):
            sentence = sentence_info['text']
            sentence_words = len(sentence.split())
            
            # Check if adding this sentence would exceed chunk size
            if current_word_count + sentence_words > self.config.chunk_size and current_chunk_sentences:
                # Create chunk from current sentences
                chunk_data = self._create_chunk_from_sentences(
                    current_chunk_sentences, 
                    source_id,
                    chunk_index,
                    segment_boundaries,
                    sentence_positions,
                    i
                )
                if chunk_data:
                    chunks.append(chunk_data)
                    chunk_index += 1
                
                # Start new chunk with overlap
                overlap_sentences = current_chunk_sentences[-self.config.chunk_overlap:]
                current_chunk_sentences = overlap_sentences + [sentence_info]
                current_word_count = sum(len(s['text'].split()) for s in current_chunk_sentences)
            else:
                current_chunk_sentences.append(sentence_info)
                current_word_count += sentence_words
        
        # Handle remaining sentences
        if current_chunk_sentences:
            chunk_data = self._create_chunk_from_sentences(
                current_chunk_sentences,
                source_id,
                chunk_index,
                segment_boundaries,
                sentence_positions,
                len(sentence_positions)
            )
            if chunk_data:
                chunks.append(chunk_data)
        
        return chunks
    
    def _create_intelligent_chunks_from_processed(self, processed_segments: List[ProcessedSegment], source_id: int) -> List[ChunkData]:
        """Create intelligent chunks from processed segments."""
        chunks = []
        current_chunk_segments = []
        current_word_count = 0
        chunk_index = 0
        
        for i, segment in enumerate(processed_segments):
            # Skip removed segments
            if segment.action == ProcessingAction.REMOVE:
                continue
            
            segment_words = len(segment.processed_text.split())
            
            # Check if adding this segment would exceed chunk size
            if current_word_count + segment_words > self.config.chunk_size and current_chunk_segments:
                # Create chunk from current segments
                chunk = self._create_chunk_from_processed_segments(
                    current_chunk_segments, 
                    chunk_index, 
                    source_id,
                    processed_segments,
                    i
                )
                chunks.append(chunk)
                
                # Start new chunk with overlap
                overlap_segments = self._get_overlap_segments(current_chunk_segments)
                current_chunk_segments = overlap_segments + [segment]
                current_word_count = sum(len(s.processed_text.split()) for s in current_chunk_segments)
                chunk_index += 1
            else:
                # Add to current chunk
                current_chunk_segments.append(segment)
                current_word_count += segment_words
        
        # Create final chunk if segments remain
        if current_chunk_segments:
            chunk = self._create_chunk_from_processed_segments(
                current_chunk_segments, 
                chunk_index, 
                source_id,
                processed_segments,
                len(processed_segments)
            )
            chunks.append(chunk)
        
        return chunks
    
    def _create_chunk_from_processed_segments(
        self, 
        segments: List[ProcessedSegment], 
        chunk_index: int, 
        source_id: int,
        all_segments: List[ProcessedSegment],
        current_position: int
    ) -> ChunkData:
        """Create a chunk from processed segments."""
        # Combine segment texts
        chunk_text = " ".join(s.processed_text for s in segments)
        
        # Get time boundaries
        start_time = segments[0].start_time
        end_time = segments[-1].end_time
        
        # Combine all tools and prices
        mentioned_tools = []
        mentioned_prices = []
        total_info_density = 0
        
        for segment in segments:
            mentioned_tools.extend(segment.extracted_tools)
            mentioned_prices.extend(segment.extracted_prices)
            total_info_density += segment.information_density
        
        mentioned_tools = list(set(mentioned_tools))
        mentioned_prices = list(set(mentioned_prices))
        
        # Calculate average information density as quality score
        quality_score = total_info_density / len(segments) if segments else 0.5
        
        # Get context
        context_before = self._get_processed_context_before(current_position - len(segments), all_segments)
        context_after = self._get_processed_context_after(current_position, all_segments)
        
        return ChunkData(
            source_id=source_id,
            content=chunk_text,
            cleaned_content=chunk_text,  # Already cleaned by processor
            start_time=start_time,
            end_time=end_time,
            chunk_index=chunk_index,
            mentioned_tools=mentioned_tools,
            mentioned_prices=mentioned_prices,
            quality_score=quality_score,
            context_before=context_before,
            context_after=context_after
        )
    
    def _get_overlap_segments(self, segments: List[ProcessedSegment]) -> List[ProcessedSegment]:
        """Get overlap segments for continuity."""
        if not segments:
            return []
        
        # Get last few segments for overlap
        overlap_word_count = 0
        overlap_segments = []
        
        for segment in reversed(segments):
            segment_words = len(segment.processed_text.split())
            if overlap_word_count + segment_words <= self.config.chunk_overlap:
                overlap_segments.insert(0, segment)
                overlap_word_count += segment_words
            else:
                break
        
        return overlap_segments
    
    def _get_processed_context_before(self, position: int, all_segments: List[ProcessedSegment]) -> str:
        """Get context before the current position from processed segments."""
        context_segments = []
        
        for i in range(max(0, position - self.config.context_window), max(0, position)):
            if i < len(all_segments):
                context_segments.append(all_segments[i].processed_text)
        
        return " ".join(context_segments)
    
    def _get_processed_context_after(self, position: int, all_segments: List[ProcessedSegment]) -> str:
        """Get context after the current position from processed segments."""
        context_segments = []
        
        for i in range(position, min(len(all_segments), position + self.config.context_window)):
            if i < len(all_segments):
                context_segments.append(all_segments[i].processed_text)
        
        return " ".join(context_segments)
    
    def _create_chunk_from_sentences(self, sentences: List[Dict], source_id: int, chunk_index: int, 
                                   segment_boundaries: List[Dict], all_sentences: List[Dict], 
                                   current_sentence_index: int) -> Optional[ChunkData]:
        """Create a chunk from a list of sentences."""
        if not sentences:
            return None
        
        # Combine sentences into chunk text
        chunk_text = " ".join(s['text'] for s in sentences).strip()
        
        # Skip if chunk is too short
        if len(chunk_text.split()) < self.config.min_chunk_words:
            return None
        
        # Find timing information
        start_pos = sentences[0]['start_pos']
        end_pos = sentences[-1]['end_pos']
        
        start_time = 0
        end_time = 0
        
        for boundary in segment_boundaries:
            if boundary['start_pos'] <= start_pos <= boundary['end_pos']:
                start_time = boundary['start_time']
            if boundary['start_pos'] <= end_pos <= boundary['end_pos']:
                end_time = boundary['end_time']
        
        # Apply entity correction to the chunk
        correction_result = self.corrector.correct_text(chunk_text)
        
        # Extract mentioned tools and prices
        mentioned_tools = [e['corrected'] for e in correction_result.detected_entities 
                          if e['category'] in ['automation', 'development', 'ai_model']]
        mentioned_prices = self._extract_prices(chunk_text)
        
        # Calculate quality score
        quality_score = self._calculate_chunk_quality(chunk_text, correction_result)
        
        # Get context
        context_before = self._get_context_before(current_sentence_index, all_sentences)
        context_after = self._get_context_after(current_sentence_index, all_sentences)
        
        return ChunkData(
            source_id=source_id,
            content=chunk_text,
            cleaned_content=correction_result.corrected_text,
            start_time=start_time,
            end_time=end_time,
            chunk_index=chunk_index,
            mentioned_tools=mentioned_tools,
            mentioned_prices=mentioned_prices,
            quality_score=quality_score,
            context_before=context_before,
            context_after=context_after
        )
    
    def _extract_prices(self, text: str) -> List[str]:
        """Extract price mentions from text."""
        price_patterns = [
            r'\$\d+(?:\.\d{2})?(?:/month|/mo|/year|/yr)?',
            r'\d+\s*(?:dollars?|bucks?|usd)\s*(?:per|/)\s*(?:month|year)',
            r'(?:free|paid|premium|pro)\s*(?:plan|tier|version)',
            r'\d+(?:\.\d{2})?\s*(?:per|/)\s*(?:user|seat|month|year)'
        ]
        
        prices = []
        for pattern in price_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            prices.extend(matches)
        
        return list(set(prices))
    
    def _calculate_chunk_quality(self, text: str, correction_result) -> float:
        """Calculate quality score for a chunk."""
        score = 5.0  # Base score
        
        # Adjust based on length
        word_count = len(text.split())
        if 100 <= word_count <= 200:
            score += 1.0
        elif word_count < 50:
            score -= 1.0
        
        # Adjust based on entity corrections
        if correction_result.corrections_made > 0:
            score += 0.5  # Good - we found and corrected entities
        
        # Adjust based on content indicators
        text_lower = text.lower()
        if any(word in text_lower for word in ['step', 'how to', 'tutorial', 'guide']):
            score += 1.0
        if any(word in text_lower for word in ['configure', 'setup', 'install', 'create']):
            score += 0.5
        
        # Penalize if too repetitive
        words = text_lower.split()
        unique_words = len(set(words))
        if unique_words / len(words) < 0.5:
            score -= 1.0
        
        # Normalize to 0-1 range as required by database constraint
        return max(0.1, min(1.0, score / 10.0))
    
    def _get_context_before(self, sentence_index: int, all_sentences: List[Dict]) -> str:
        """Get context sentences before the current chunk."""
        start_idx = max(0, sentence_index - self.config.context_window)
        context_sentences = all_sentences[start_idx:sentence_index]
        return " ".join(s['text'] for s in context_sentences[-self.config.context_window:])
    
    def _get_context_after(self, sentence_index: int, all_sentences: List[Dict]) -> str:
        """Get context sentences after the current chunk."""
        end_idx = min(len(all_sentences), sentence_index + self.config.context_window)
        context_sentences = all_sentences[sentence_index:end_idx]
        return " ".join(s['text'] for s in context_sentences[:self.config.context_window])
    
    async def _update_processing_status(self, source_id: int, status: str):
        """Update processing status in database."""
        async with self.db.get_connection() as conn:
            await conn.execute(
                "UPDATE sources SET processing_status = $1, processed_at = $2 WHERE id = $3",
                status, datetime.now(), source_id
            )


async def main():
    """Test the video processor with a sample video."""
    processor = VideoProcessor()
    
    # Test with a sample video URL (replace with actual AI tools video)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    try:
        print("🔧 Testing Video Processing Pipeline...")
        print(f"📹 Processing: {test_url}")
        
        result = await processor.process_video(test_url)
        
        print(f"✅ Processing completed!")
        print(f"📊 Status: {result['status']}")
        print(f"🆔 Source ID: {result['source_id']}")
        
        if result['status'] == 'completed':
            stats = result['processing_stats']
            print(f"📄 Chunks created: {result['chunks_created']}")
            print(f"📈 Processing stats:")
            print(f"   - Total segments: {stats['total_segments']}")
            print(f"   - Corrected segments: {stats['corrected_segments']}")
            print(f"   - Total chunks: {stats['total_chunks']}")
            print(f"   - Average chunk quality: {stats['average_chunk_quality']:.1f}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        await processor.db.close()


if __name__ == "__main__":
    asyncio.run(main())