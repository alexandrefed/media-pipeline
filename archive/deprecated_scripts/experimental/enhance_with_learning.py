"""
Enhanced Video Processing with Adaptive Learning
Combines transcript enhancement with knowledge base learning.
"""

import json
import sys
from pathlib import Path
from adaptive_video_processor import AdaptiveVideoProcessor
from datetime import datetime


def process_video_with_learning(raw_file_path: str):
    """Process a video transcript with adaptive learning."""
    
    # Initialize processor
    processor = AdaptiveVideoProcessor()
    
    # Read raw transcript
    with open(raw_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Extract metadata
    metadata = {}
    content_start = 0
    for i, line in enumerate(lines):
        if line.startswith('Video:'):
            metadata['title'] = line.replace('Video:', '').strip()
        elif line.startswith('Channel:'):
            metadata['channel'] = line.replace('Channel:', '').strip()
        elif line.startswith('Duration:'):
            metadata['duration'] = line.replace('Duration:', '').strip()
        elif line.startswith('====='):
            content_start = i + 2
            break
    
    # Get transcript text
    raw_text = ''.join(lines[content_start:])
    
    print(f"\n📚 Processing: {metadata.get('title', 'Unknown')}")
    print(f"📺 Channel: {metadata.get('channel', 'Unknown')}")
    print("="*70)
    
    # Apply learned corrections
    print("\n🔧 Applying learned corrections...")
    corrected_text, corrections_made = processor.apply_learned_corrections(raw_text)
    
    if corrections_made:
        print(f"✅ Applied {len(corrections_made)} automatic corrections:")
        for correction in corrections_made[:5]:  # Show first 5
            print(f"   - {correction}")
        if len(corrections_made) > 5:
            print(f"   ... and {len(corrections_made) - 5} more")
    else:
        print("ℹ️  No automatic corrections needed")
    
    # Analyze content
    print("\n🔍 Analyzing content...")
    analysis = processor.analyze_video_content(corrected_text, metadata)
    print(f"📊 Content type: {analysis['estimated_content_type']}")
    print(f"🏷️  Topics detected: {', '.join(analysis['detected_topics'])}")
    
    # Generate suggestions
    print("\n💡 Generating enhancement suggestions...")
    suggestions = processor.generate_enhancement_suggestions(corrected_text, corrections_made)
    
    # Show chunk boundary suggestions
    if suggestions['chunk_boundary_suggestions']:
        print(f"\n📍 Found {len(suggestions['chunk_boundary_suggestions'])} potential chunk boundaries:")
        for i, boundary in enumerate(suggestions['chunk_boundary_suggestions'][:10]):
            context = corrected_text[boundary['position']:boundary['position']+50]
            print(f"   {i+1}. [{boundary['type']}] '{boundary['phrase']}' at position {boundary['position']}")
            print(f"      Context: ...{context}...")
    
    # Show potential corrections needing review
    if suggestions['potential_corrections']:
        print(f"\n⚠️  {len(suggestions['potential_corrections'])} potential corrections need review:")
        for i, correction in enumerate(suggestions['potential_corrections'][:5]):
            print(f"   {i+1}. '{correction['text']}' - {correction['note']}")
            print(f"      Context: ...{correction['context']}...")
    
    # Save enhanced version
    video_id = Path(raw_file_path).stem.replace('raw_text_for_enhancement_', '')
    enhanced_file = f"enhanced_transcript_{video_id}_auto.txt"
    
    with open(enhanced_file, 'w', encoding='utf-8') as f:
        # Write metadata
        for line in lines[:content_start]:
            f.write(line)
        # Write corrected content
        f.write(corrected_text)
    
    print(f"\n💾 Saved auto-enhanced transcript to: {enhanced_file}")
    
    # Generate processing report
    report = processor.generate_processing_report(
        f"https://www.youtube.com/watch?v={video_id}",
        {
            'corrections_made': corrections_made,
            'content_type': analysis['estimated_content_type'],
            'topics': analysis['detected_topics'],
            'chunk_size': analysis.get('suggested_chunk_size', {}),
            'suggestions': [s['note'] for s in suggestions['potential_corrections'][:3]],
            'quality_notes': suggestions.get('quality_notes', [])
        }
    )
    
    # Append to processing history
    with open('processing_history.md', 'a') as f:
        f.write(f"\n\n---\n{report}")
    
    print("\n📝 Updated processing history")
    
    # Return results for further processing
    return {
        'video_id': video_id,
        'metadata': metadata,
        'corrected_text': corrected_text,
        'corrections_made': corrections_made,
        'analysis': analysis,
        'suggestions': suggestions
    }


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        raw_file = sys.argv[1]
    else:
        # Default to the latest extracted file
        raw_file = "raw_text_for_enhancement_arWg7gYVD_0.txt"
    
    if not Path(raw_file).exists():
        print(f"❌ File not found: {raw_file}")
        return
    
    results = process_video_with_learning(raw_file)
    
    print("\n" + "="*70)
    print("✅ Auto-enhancement complete!")
    print("\n🎯 Next steps:")
    print("1. Review the auto-enhanced transcript")
    print("2. Make any additional manual corrections")
    print("3. Create manual chunks using the boundary suggestions")
    print("4. Update knowledge base with new learnings")


if __name__ == "__main__":
    main()