"""
YouTube Transcript Processor
Main processor that orchestrates the entire transcript processing pipeline
"""

import json
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import parse_qs, urlparse

from .raw_transcript_extractor import RawTranscriptExtractor
from .text_reconstructor import TextReconstructor
from .chapter_extractor import ChapterExtractor
from .hierarchical_chunker import HierarchicalChunker, KnowledgeChunk


class YouTubeProcessor:
    """Main processor for YouTube transcript processing."""
    
    def __init__(self, max_tokens: int = 800, min_tokens: int = 200):
        """Initialize the YouTube processor."""
        self.max_tokens = max_tokens
        self.min_tokens = min_tokens
        
        # Initialize components
        self.raw_extractor = RawTranscriptExtractor()
        self.text_reconstructor = TextReconstructor()
        self.chapter_extractor = ChapterExtractor()
        self.hierarchical_chunker = HierarchicalChunker(max_tokens, min_tokens)
        
        print(f"✅ YouTube processor initialized (max: {max_tokens}, min: {min_tokens} tokens)")
    
    def process_video(self, url: str, save_intermediates: bool = True) -> Dict:
        """Process a YouTube video through the complete pipeline."""
        print(f"\n🎬 Processing video: {url}")
        print("=" * 60)
        
        # Step 1: Extract raw transcript
        print("\n📥 Step 1: Extracting raw transcript...")
        raw_data = self._extract_raw_transcript(url)
        
        if save_intermediates:
            self._save_json(raw_data, f"raw_segments_{raw_data['metadata']['id']}.json")
        
        # Step 2: Reconstruct clean text
        print("\n📝 Step 2: Reconstructing clean text...")
        text_data = self._reconstruct_text(raw_data)
        
        if save_intermediates:
            self._save_json(text_data, f"reconstructed_text_{raw_data['metadata']['id']}.json")
        
        # Step 3: Extract chapters
        print("\n📚 Step 3: Extracting chapters...")
        chapter_data = self._extract_chapters(raw_data, text_data)
        
        if save_intermediates:
            self._save_json(chapter_data, f"extracted_chapters_{raw_data['metadata']['id']}.json")
        
        # Step 4: Apply hierarchical chunking
        print("\n🔄 Step 4: Applying hierarchical chunking...")
        chunk_data = self._apply_chunking(chapter_data)
        
        if save_intermediates:
            self._save_json(chunk_data, f"hierarchical_chunks_{raw_data['metadata']['id']}.json")
        
        # Step 5: Create final output
        print("\n📊 Step 5: Creating final output...")
        final_data = self._create_final_output(raw_data, text_data, chapter_data, chunk_data)
        
        print(f"\n✅ Processing complete! Generated {len(final_data['chunks'])} chunks")
        return final_data
    
    def _extract_raw_transcript(self, url: str) -> Dict:
        """Extract raw transcript segments."""
        # Extract metadata
        metadata = self.raw_extractor.extract_video_metadata(url)
        
        # Extract raw segments
        raw_segments = self.raw_extractor.extract_raw_segments(url)
        
        return {
            'extraction_timestamp': datetime.now().isoformat(),
            'metadata': metadata,
            'raw_segments': raw_segments,
            'total_segments': len(raw_segments)
        }
    
    def _reconstruct_text(self, raw_data: Dict) -> Dict:
        """Reconstruct clean text from raw segments."""
        raw_segments = raw_data['raw_segments']
        
        # Extract clean segments
        clean_segments = self.text_reconstructor.extract_clean_segments(raw_segments)
        
        # Reconstruct full text and sentences
        full_text, sentences = self.text_reconstructor.reconstruct_with_sentence_boundaries(clean_segments)
        
        # Create timestamped segments
        timestamped_segments = self.text_reconstructor.create_timestamped_segments(clean_segments)
        
        # Get reconstruction stats
        stats = self.text_reconstructor.get_reconstruction_stats(
            raw_segments, clean_segments, full_text, sentences
        )
        
        return {
            'metadata': raw_data['metadata'],
            'reconstruction_stats': stats,
            'full_text': full_text,
            'sentences': sentences,
            'clean_segments': clean_segments,
            'timestamped_segments': timestamped_segments
        }
    
    def _extract_chapters(self, raw_data: Dict, text_data: Dict) -> Dict:
        """Extract chapters from video."""
        metadata = raw_data['metadata']
        clean_segments = text_data['clean_segments']
        
        # Try to extract chapters from description
        chapters = self.chapter_extractor.extract_chapters_from_description(metadata['description'])
        
        # If no chapters found, generate from segments
        if not chapters:
            chapters = self.chapter_extractor.extract_chapters_from_segments(
                clean_segments, metadata['duration_seconds']
            )
        
        # Split segments by chapters
        chapter_segments = self.chapter_extractor.split_segments_by_chapters(clean_segments, chapters)
        
        # Get chapter stats
        stats = self.chapter_extractor.get_chapter_stats(chapters, chapter_segments)
        
        return {
            'metadata': metadata,
            'chapters': [
                {
                    'index': ch.index,
                    'start_time': ch.start_time,
                    'end_time': ch.end_time,
                    'title': ch.title,
                    'timestamp_text': ch.timestamp_text
                }
                for ch in chapters
            ],
            'chapter_segments': chapter_segments,
            'stats': stats
        }
    
    def _apply_chunking(self, chapter_data: Dict) -> Dict:
        """Apply hierarchical chunking."""
        chapters = chapter_data['chapters']
        chapter_segments = chapter_data['chapter_segments']
        
        # Level 1: Chunk by chapters
        chapter_chunks = self.hierarchical_chunker.chunk_by_chapters(chapters, chapter_segments)
        
        # Apply hierarchical chunking
        final_chunks = self.hierarchical_chunker.apply_hierarchical_chunking(chapter_chunks)
        
        # Get statistics and validation
        stats = self.hierarchical_chunker.get_chunking_stats(final_chunks)
        validation = self.hierarchical_chunker.validate_chunks(final_chunks)
        
        return {
            'metadata': chapter_data['metadata'],
            'chunks': final_chunks,
            'stats': stats,
            'validation': validation
        }
    
    def _create_final_output(self, raw_data: Dict, text_data: Dict, 
                           chapter_data: Dict, chunk_data: Dict) -> Dict:
        """Create final output with all processing results."""
        chunks = chunk_data['chunks']
        
        # Convert chunks to serializable format
        serializable_chunks = []
        for chunk in chunks:
            serializable_chunks.append({
                'id': chunk.id,
                'chapter_index': chunk.chapter_index,
                'chapter_title': chunk.chapter_title,
                'chunk_index': chunk.chunk_index,
                'start_time': chunk.start_time,
                'end_time': chunk.end_time,
                'text': chunk.text,
                'token_count': chunk.token_count,
                'sentences': chunk.sentences,
                'level': chunk.level,
                'overlap_with_previous': chunk.overlap_with_previous
            })
        
        return {
            'processing_timestamp': datetime.now().isoformat(),
            'video_metadata': raw_data['metadata'],
            'processing_stats': {
                'raw_segments': raw_data['total_segments'],
                'clean_segments': text_data['reconstruction_stats']['clean_segments_count'],
                'chapters': len(chapter_data['chapters']),
                'final_chunks': len(chunks),
                'reconstruction_stats': text_data['reconstruction_stats'],
                'chunking_stats': chunk_data['stats'],
                'validation': chunk_data['validation']
            },
            'chapters': chapter_data['chapters'],
            'full_text': text_data['full_text'],
            'chunks': serializable_chunks
        }
    
    def _save_json(self, data: Dict, filename: str):
        """Save data to JSON file."""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"💾 Saved intermediate result: {filename}")
    
    def extract_video_id(self, url: str) -> str:
        """Extract video ID from YouTube URL."""
        return self.raw_extractor.extract_video_id(url)
    
    def process_for_manual_enhancement(self, url: str) -> str:
        """Process video and return clean text for manual Claude Code enhancement."""
        print(f"\n📝 Extracting clean text for manual enhancement...")
        
        # Extract and reconstruct text
        raw_data = self._extract_raw_transcript(url)
        text_data = self._reconstruct_text(raw_data)
        
        # Save full text for manual processing
        video_id = raw_data['metadata']['id']
        text_filename = f"raw_text_for_enhancement_{video_id}.txt"
        
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write(f"Video: {raw_data['metadata']['title']}\n")
            f.write(f"Channel: {raw_data['metadata']['channel_name']}\n")
            f.write(f"Duration: {raw_data['metadata']['duration_seconds']} seconds\n")
            f.write(f"Description: {raw_data['metadata']['description'][:200]}...\n")
            f.write("=" * 80 + "\n\n")
            f.write(text_data['full_text'])
        
        print(f"✅ Raw text saved to: {text_filename}")
        print(f"📄 Text length: {len(text_data['full_text'])} characters")
        print(f"📝 Sentences: {len(text_data['sentences'])}")
        
        return text_filename
    
    def process_enhanced_text(self, enhanced_text: str, original_url: str) -> Dict:
        """Process enhanced text through chunking pipeline."""
        print(f"\n🔄 Processing enhanced text through chunking pipeline...")
        
        # Get original metadata
        video_id = self.extract_video_id(original_url)
        metadata = self.raw_extractor.extract_video_metadata(original_url)
        
        # Create mock text data
        from .text_reconstructor import TextReconstructor
        reconstructor = TextReconstructor()
        sentences = reconstructor.segment_into_sentences(enhanced_text)
        
        text_data = {
            'metadata': metadata,
            'full_text': enhanced_text,
            'sentences': sentences,
            'clean_segments': [],  # Not needed for enhanced text
            'reconstruction_stats': {
                'clean_segments_count': 0,
                'sentences_count': len(sentences),
                'total_characters': len(enhanced_text)
            }
        }
        
        # Extract chapters from enhanced text structure
        extracted_chapters = self.chapter_extractor.extract_chapters_from_description(metadata['description'])
        if not extracted_chapters:
            # Create simple chapters based on text length
            from .chapter_extractor import VideoChapter
            extracted_chapters = [VideoChapter(
                index=0,
                start_time=0,
                end_time=metadata['duration_seconds'],
                title='Full Video',
                timestamp_text='00:00 Full Video'
            )]
        
        # Convert to dict format for chunking
        chapters = [
            {
                'index': ch.index,
                'start_time': ch.start_time,
                'end_time': ch.end_time,
                'title': ch.title,
                'timestamp_text': ch.timestamp_text
            }
            for ch in extracted_chapters
        ]
        
        # Create mock chapter segments
        chapter_segments = {0: [{'text': enhanced_text, 'start_time': 0, 'end_time': metadata['duration_seconds']}]}
        
        chapter_data = {
            'metadata': metadata,
            'chapters': chapters,
            'chapter_segments': chapter_segments,
            'stats': {}
        }
        
        # Apply chunking
        chunk_data = self._apply_chunking(chapter_data)
        
        # Create final output
        final_data = self._create_final_output(
            {'metadata': metadata, 'total_segments': 0},
            text_data,
            chapter_data,
            chunk_data
        )
        
        return final_data


def main():
    """Main processing function."""
    processor = YouTubeProcessor(max_tokens=800, min_tokens=200)
    
    # Get URL from user
    url = input("Enter YouTube video URL: ").strip()
    if not url:
        print("No URL provided, exiting.")
        return
    
    try:
        # Process video
        result = processor.process_video(url, save_intermediates=True)
        
        # Save final result
        video_id = processor.extract_video_id(url)
        final_filename = f"final_processed_{video_id}.json"
        
        with open(final_filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"\n🎉 Final result saved to: {final_filename}")
        
        # Show summary
        print(f"\n📊 Processing Summary:")
        print(f"  Video: {result['video_metadata']['title']}")
        print(f"  Chapters: {result['processing_stats']['chapters']}")
        print(f"  Final chunks: {result['processing_stats']['final_chunks']}")
        print(f"  Validation: {result['processing_stats']['validation']['valid_chunks']} valid chunks")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()