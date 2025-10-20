#!/usr/bin/env python3
"""
Integration script to send processed videos to the Knowledge Base system
This bridges the local processing pipeline with n8n workflows
"""

import sys
import json
from pathlib import Path

# Add notifications module to path
sys.path.insert(0, str(Path(__file__).parent.parent / "notifications" / "src"))

from core.db_logger import (
    KnowledgeBaseLogger,
    VideoMetadata,
    VideoInsight,
    send_to_knowledge_base
)


def extract_video_id_from_url(url: str) -> str:
    """Extract YouTube video ID from URL"""
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    else:
        return url


def main():
    """
    Main integration script

    Usage:
        python integrate_with_knowledge_base.py workspace/analysis/ABC123_analysis.json
        python integrate_with_knowledge_base.py workspace/analysis/ABC123_analysis.json --dry-run
    """
    if len(sys.argv) < 2:
        print("Usage: python integrate_with_knowledge_base.py <analysis_file> [--dry-run]")
        sys.exit(1)

    analysis_file = Path(sys.argv[1])
    dry_run = "--dry-run" in sys.argv

    if not analysis_file.exists():
        print(f"Error: Analysis file not found: {analysis_file}")
        sys.exit(1)

    # Load analysis data to get video details
    with open(analysis_file, 'r') as f:
        data = json.load(f)

    # Extract video ID from filename or data
    video_id = data.get('video_id')
    if not video_id:
        # Try to extract from filename
        filename = analysis_file.stem
        video_id = filename.replace('_analysis', '')

    url = data.get('url') or f"https://youtube.com/watch?v={video_id}"

    print("=" * 60)
    print("AI Knowledge Base Integration")
    print("=" * 60)
    print(f"\nVideo ID: {video_id}")
    print(f"Analysis File: {analysis_file}")
    print(f"URL: {url}")

    if dry_run:
        print("\n⚠️  DRY RUN MODE - Will not send to server")

    print("\n" + "-" * 60)
    print("Sending to Knowledge Base...")
    print("-" * 60)

    # Send to knowledge base
    result = send_to_knowledge_base(
        video_id=video_id,
        analysis_file=analysis_file,
        url=url,
        dry_run=dry_run
    )

    # Print result
    print("\n" + "=" * 60)
    if dry_run:
        print("DRY RUN RESULT")
        print("=" * 60)
        print(json.dumps(result, indent=2))
    elif result.get('success'):
        print("✅ SUCCESS")
        print("=" * 60)
        print(f"Video ID: {result['video_id']}")
        print(f"Status Code: {result['status_code']}")
        if 'response' in result:
            print(f"\nResponse:")
            print(json.dumps(result['response'], indent=2))
    else:
        print("❌ ERROR")
        print("=" * 60)
        print(f"Video ID: {result.get('video_id', 'Unknown')}")
        print(f"Error: {result.get('error', 'Unknown error')}")
        sys.exit(1)


def example_programmatic_usage():
    """
    Example of programmatic usage in your processing scripts
    """
    # Create logger
    logger = KnowledgeBaseLogger()

    # Create insights manually
    insights = [
        VideoInsight(
            text="Use HTTP Request node to call external APIs in n8n workflows",
            type="tip",
            category="n8n",
            tags=["workflow", "http", "api"],
            timestamp_start=120,
            timestamp_end=240,
            quality_score=0.85,
            priority="high",
            actionable=True
        ),
        VideoInsight(
            text="Set credentials in n8n for secure API authentication",
            type="technique",
            category="n8n",
            tags=["security", "credentials"],
            timestamp_start=300,
            timestamp_end=420,
            quality_score=0.9,
            priority="high",
            actionable=True
        )
    ]

    # Create video metadata
    video = VideoMetadata(
        video_id="ABC123DEF456",
        title="Complete n8n Tutorial - Automating Workflows",
        channel_name="IndyDevDan",
        channel_id="UC123456789",
        url="https://youtube.com/watch?v=ABC123DEF456",
        duration_seconds=1800,
        pipeline_type="ai_tools",
        tags=["n8n", "automation", "workflow", "tutorial"],
        total_chunks=25,
        insights=insights
    )

    # Send to knowledge base
    result = logger.store_video_insights(video)

    if result['success']:
        print(f"✅ Successfully stored {len(insights)} insights for video {video.video_id}")
    else:
        print(f"❌ Error: {result['error']}")


if __name__ == "__main__":
    main()
