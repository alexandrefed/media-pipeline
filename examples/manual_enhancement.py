#!/usr/bin/env python3
"""
Manual Enhancement Workflow Example

This script demonstrates the recommended workflow for getting the best
results from the AI Knowledge Base system using Claude Code enhancement.
"""

import sys
import os

# Add src to path to import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pipeline.youtube_processor import YouTubeProcessor


def main():
    """Manual enhancement workflow example."""
    
    if len(sys.argv) < 2:
        print("Usage: python manual_enhancement.py <youtube_url>")
        print("Example: python manual_enhancement.py 'https://youtube.com/watch?v=VIDEO_ID'")
        return 1
    
    video_url = sys.argv[1]
    processor = YouTubeProcessor()
    
    print("🤖 AI Knowledge Base - Manual Enhancement Workflow")
    print("=" * 60)
    print(f"Video: {video_url}")
    print()
    
    try:
        # Step 1: Extract raw transcript
        print("📥 Step 1: Extracting raw transcript...")
        text_file = processor.process_for_manual_enhancement(video_url)
        print(f"✅ Raw text saved to: {text_file}")
        print()
        
        # Step 2: Instructions for manual enhancement
        print("🔄 Step 2: Manual Enhancement Instructions")
        print("=" * 40)
        print("1. Open the raw text file in Claude Code")
        print("2. Use Claude Code to enhance the transcript:")
        print("   - Fix transcription errors (e.g., 'mate and' → 'n8n')")
        print("   - Correct tool names (e.g., 'clawed code' → 'Claude Code')")
        print("   - Improve sentence flow and grammar")
        print("   - Fix fragmented punctuation")
        print("3. Save the enhanced version")
        print()
        
        # Step 3: Wait for user to complete enhancement
        input("Press Enter after you've enhanced the transcript...")
        
        # Step 4: Ask for enhanced file
        enhanced_file = input("Enter the path to your enhanced transcript file: ").strip()
        
        if not enhanced_file or not os.path.exists(enhanced_file):
            print("❌ Enhanced file not found. Please provide a valid file path.")
            return 1
        
        # Step 5: Process enhanced transcript
        print("\n📊 Step 3: Processing enhanced transcript...")
        
        with open(enhanced_file, 'r', encoding='utf-8') as f:
            enhanced_text = f.read()
        
        result = processor.process_enhanced_text(enhanced_text, video_url)
        
        # Step 6: Save results
        import json
        output_file = enhanced_file.replace('.txt', '_processed.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, default=str)
        
        print(f"✅ Enhanced transcript processed successfully!")
        print(f"📊 Generated {len(result['chunks'])} chunks")
        print(f"💾 Results saved to: {output_file}")
        
        # Show quality comparison
        chunks = result['chunks']
        token_counts = [chunk['token_count'] for chunk in chunks]
        print(f"\n📈 Quality Metrics:")
        print(f"  • Total chunks: {len(chunks)}")
        print(f"  • Token range: {min(token_counts)} - {max(token_counts)}")
        print(f"  • Average tokens: {sum(token_counts) / len(token_counts):.1f}")
        
        # Show sample enhanced chunks
        print(f"\n📝 Sample Enhanced Chunks:")
        for i, chunk in enumerate(chunks[:2]):
            print(f"  {i+1}. {chunk['text'][:150]}...")
            print(f"     Tokens: {chunk['token_count']}, Sentences: {len(chunk['sentences'])}")
            print()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())