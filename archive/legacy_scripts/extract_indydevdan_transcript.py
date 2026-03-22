#!/usr/bin/env python3
"""Extract transcript from IndyDevDan's MCP video."""

from src.youtube_extractor import YouTubeExtractor
import json

def main():
    extractor = YouTubeExtractor()
    
    # The video URL you provided
    video_url = "https://www.youtube.com/watch?v=mKEq_YaJjPI&t=565s"
    
    try:
        metadata, transcript = extractor.extract_video_data(video_url)
        
        print(f"\n📹 Video: {metadata.title}")
        print(f"📺 Channel: {metadata.channel_name}")
        print(f"📅 Published: {metadata.published_date}")
        print(f"⏱️  Duration: {metadata.duration_seconds} seconds")
        print(f"👀 Views: {metadata.view_count:,}")
        
        # Save full transcript to file
        output_data = {
            "metadata": metadata.dict(),
            "transcript": [segment.dict() for segment in transcript]
        }
        
        with open("indydevdan_mcp_transcript.json", "w") as f:
            json.dump(output_data, f, indent=2, default=str)
        
        print(f"\n✅ Saved full transcript to indydevdan_mcp_transcript.json")
        print(f"📝 Total segments: {len(transcript)}")
        
        # Show preview
        print(f"\n📝 Transcript Preview (first 10 segments):")
        for i, segment in enumerate(transcript[:10]):
            print(f"[{segment.start_time:.1f}s - {segment.end_time:.1f}s] {segment.text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()