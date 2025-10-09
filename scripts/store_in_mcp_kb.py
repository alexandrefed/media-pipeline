#!/usr/bin/env python3
"""
Direct MCP KB Memory integration script.

This script takes a video summary JSON and stores it directly in MCP KB Memory
using the Python interface.
"""

import json
import sys
from pathlib import Path


def store_video_in_mcp_kb(summary_file: str) -> None:
    """Store video summary in MCP KB Memory."""

    # Load summary
    with open(summary_file, 'r', encoding='utf-8') as f:
        summary_data = json.load(f)

    # Extract key information
    title = summary_data.get("title", "Unknown Video")
    channel = summary_data.get("channel_name", "Unknown Channel")
    video_id = summary_data.get("video_id", "unknown")
    content_type = summary_data.get("content_type", "unknown")
    summary_text = summary_data.get("summary", "")
    tech_info = summary_data.get("technical_info", {})
    takeaways = summary_data.get("key_takeaways", [])
    tags = summary_data.get("tags", [])

    # Build content string
    content_parts = []
    content_parts.append(f"**Video**: {title}")
    content_parts.append(f"**Channel**: {channel}")
    content_parts.append(f"**Video ID**: {video_id}")
    content_parts.append(f"**Content Type**: {content_type}")
    content_parts.append("")
    content_parts.append("## Summary")
    content_parts.append(summary_text)
    content_parts.append("")

    # Add technical information
    if tech_info.get("tools_mentioned"):
        content_parts.append("## Tools Mentioned")
        content_parts.append(", ".join(tech_info["tools_mentioned"]))
        content_parts.append("")

    if tech_info.get("commands"):
        content_parts.append("## Key Commands")
        for cmd in tech_info["commands"][:10]:
            content_parts.append(f"- `{cmd}`")
        content_parts.append("")

    if tech_info.get("key_concepts"):
        content_parts.append("## Key Concepts")
        for concept in tech_info["key_concepts"][:10]:
            content_parts.append(f"- {concept}")
        content_parts.append("")

    if tech_info.get("workflows"):
        content_parts.append("## Workflows")
        for workflow in tech_info["workflows"][:5]:
            content_parts.append(f"- {workflow}")
        content_parts.append("")

    # Add key takeaways
    if takeaways:
        content_parts.append("## Key Takeaways")
        for i, takeaway in enumerate(takeaways, 1):
            content_parts.append(f"{i}. {takeaway}")
        content_parts.append("")

    # Add YouTube link
    content_parts.append(f"**Watch**: https://youtube.com/watch?v={video_id}")

    content = "\n".join(content_parts)

    # Prepare tags
    all_tags = ["youtube-knowledge-base", f"video-{video_id}", f"channel-{channel.lower().replace(' ', '-')}"]
    all_tags.extend(tags)

    # Print for user to manually store (or we could use MCP KB API)
    print("\n" + "=" * 80)
    print("VIDEO SUMMARY FOR MCP KB MEMORY")
    print("=" * 80)
    print("\n📋 CONTENT:")
    print(content)
    print("\n🏷️  TAGS:")
    print(",".join(all_tags))
    print("\n" + "=" * 80)
    print("\n💡 To store in MCP KB Memory, use:")
    print(f'   mcp__mcp-kb-memory__store_memory with content above and tags: "{",".join(all_tags)}"')
    print("\n" + "=" * 80)

    # Also save to a file for easy reference
    output_file = summary_file.replace('_summary.json', '_mcp_kb_ready.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"CONTENT:\n{content}\n\nTAGS:\n{','.join(all_tags)}\n")

    print(f"\n✅ MCP KB ready content saved to: {output_file}")


def main():
    if len(sys.argv) < 2:
        print("MCP KB Storage Script")
        print("\nUsage:")
        print("  python scripts/store_in_mcp_kb.py <summary_json_file>")
        print("\nExample:")
        print("  python scripts/store_in_mcp_kb.py raw_text_for_enhancement_VIDEO_ID_auto_enhanced_summary.json")
        return

    summary_file = sys.argv[1]

    if not Path(summary_file).exists():
        print(f"❌ File not found: {summary_file}")
        sys.exit(1)

    try:
        store_video_in_mcp_kb(summary_file)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
