#!/usr/bin/env python3
"""
Basic Usage Example for AI Knowledge Base

This script demonstrates how to use the YouTube processor to extract
and process video transcripts for knowledge base creation.
"""

import sys
import os

# Add src to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pipeline.youtube_processor import YouTubeProcessor


def main():
    """Basic usage example."""
    
    # Initialize the processor
    processor = YouTubeProcessor(max_tokens=800, min_tokens=200)
    
    # Example YouTube URL (replace with your video)
    video_url = "https://www.youtube.com/watch?v=mKEq_YaJjPI"
    
    print("🎬 AI Knowledge Base - Basic Usage Example")
    print("=" * 50)
    print(f"Processing video: {video_url}")
    print()
    
    try:
        # Method 1: Extract for manual enhancement
        print("📥 Method 1: Extract for manual enhancement")
        text_file = processor.process_for_manual_enhancement(video_url)
        print(f"✅ Raw text saved to: {text_file}")
        print("🔄 Next: Enhance this text manually in Claude Code")
        print()
        
        # Method 2: Process through complete pipeline
        print("📊 Method 2: Complete pipeline processing")
        result = processor.process_video(video_url, save_intermediates=True)
        
        print(f"✅ Processing complete!")
        print(f"📊 Generated {len(result['chunks'])} chunks")
        print(f"📚 Found {len(result['chapters'])} chapters")
        
        # Show sample chunks
        print("\n📝 Sample chunks:")
        for i, chunk in enumerate(result['chunks'][:3]):
            print(f"  {i+1}. {chunk['text'][:100]}...")
            print(f"     Tokens: {chunk['token_count']}")
            print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())