#!/usr/bin/env python3
"""
Direct MCP KB Memory integration script.

This script takes a video analysis JSON and stores it directly in MCP KB Memory
using comprehensive multi-chunk storage to prevent shallow memory issues.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def extract_summary_text(summary_data: Dict[str, Any]) -> str:
    """Extract summary text handling both dict and string formats."""
    summary = summary_data.get("summary", "")

    if isinstance(summary, dict):
        # New format: {"overview": "...", "key_points": [...]}
        overview = summary.get("overview", "")
        key_points = summary.get("key_points", [])

        parts = [overview]
        if key_points:
            parts.append("\n\n**Key Points:**")
            for point in key_points:
                parts.append(f"- {point}")

        return "\n".join(parts)
    else:
        # Old format: string
        return summary


def store_video_in_mcp_kb(analysis_file: str) -> None:
    """Store video analysis in MCP KB Memory with comprehensive multi-chunk approach."""

    # Load analysis
    with open(analysis_file, 'r', encoding='utf-8') as f:
        analysis_data = json.load(f)

    # Check if this is the new detailed analysis format
    video_metadata = analysis_data.get("video_metadata", {})

    if video_metadata:
        # New detailed analysis format
        store_comprehensive_analysis(analysis_data)
    else:
        # Old summary format
        store_legacy_summary(analysis_data)


def store_legacy_summary(summary_data: Dict[str, Any]) -> None:
    """Store old format summary (backward compatibility)."""

    # Extract key information
    title = summary_data.get("title", "Unknown Video")
    channel = summary_data.get("channel_name", "Unknown Channel")
    video_id = summary_data.get("video_id", "unknown")
    content_type = summary_data.get("content_type", "unknown")
    summary_text = extract_summary_text(summary_data)
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

    # Print for user to manually store
    print("\n" + "=" * 80)
    print("VIDEO SUMMARY FOR MCP KB MEMORY (Legacy Format)")
    print("=" * 80)
    print("\n📋 CONTENT:")
    print(content)
    print("\n🏷️  TAGS:")
    print(",".join(all_tags))
    print("\n" + "=" * 80)
    print("\n💡 To store in MCP KB Memory, use:")
    print(f'   mcp__unified-memory__memory_store with content above and tags: "{",".join(all_tags)}"')
    print("\n" + "=" * 80)


def store_comprehensive_analysis(analysis_data: Dict[str, Any]) -> None:
    """Store comprehensive analysis with multi-chunk approach to prevent shallow storage."""

    # Extract metadata
    metadata = analysis_data.get("video_metadata", {})
    video_id = metadata.get("video_id", "unknown")
    title = metadata.get("title", "Unknown Video")
    channel = metadata.get("channel_name", "Unknown Channel")

    # Extract all rich content
    summary = analysis_data.get("summary", {})
    tools = analysis_data.get("tools_and_technologies", [])
    concepts = analysis_data.get("concepts_and_workflows", [])
    detailed_takeaways = analysis_data.get("detailed_takeaways", [])
    workflows = analysis_data.get("workflows", [])
    timestamps = analysis_data.get("timestamps", [])
    commands = analysis_data.get("commands", [])

    print("\n" + "=" * 80)
    print(f"COMPREHENSIVE VIDEO ANALYSIS - {title} ({video_id})")
    print("=" * 80)
    print(f"\n📊 Analysis contains:")
    print(f"  - Summary with {len(summary.get('key_points', []))} key points")
    print(f"  - {len(tools)} tools and technologies")
    print(f"  - {len(concepts)} concepts and workflows")
    print(f"  - {len(detailed_takeaways)} detailed takeaways")
    print(f"  - {len(workflows)} workflows")
    print(f"  - {len(timestamps)} timestamped segments")
    print(f"  - {len(commands)} commands")
    print("\n" + "=" * 80)

    # Generate comprehensive chunks
    chunks = []

    # CHUNK 1: Overview & Tools
    chunk1_parts = [
        f"# {title} - Overview & Tools",
        f"\n**Channel**: {channel}",
        f"**Video ID**: {video_id}",
        f"\n## Overview",
        summary.get("overview", ""),
        "\n## Key Points",
    ]
    for point in summary.get("key_points", []):
        chunk1_parts.append(f"- {point}")

    if tools:
        chunk1_parts.append("\n## Tools & Technologies")
        for i, tool in enumerate(tools[:15], 1):  # Limit to 15 tools
            tool_name = tool.get("name", "Unknown")
            tool_desc = tool.get("description", "")
            if tool_desc and tool_desc != f"*[Details about {tool_name}]*":
                chunk1_parts.append(f"\n### {i}. {tool_name}")
                chunk1_parts.append(tool_desc)

    chunk1_parts.append(f"\n**Source**: https://youtube.com/watch?v={video_id}")
    chunks.append({
        "content": "\n".join(chunk1_parts),
        "tags": f"{channel.lower().replace(' ', '-')}, {video_id}, overview, tools, technologies",
        "type": "video-overview"
    })

    # CHUNK 2: Concepts & Workflows
    if concepts or workflows:
        chunk2_parts = [f"# {title} - Concepts & Workflows"]

        if concepts:
            chunk2_parts.append(f"\n## Core Concepts ({len(concepts)} total)")
            for i, concept in enumerate(concepts[:20], 1):  # Limit to 20 concepts
                concept_name = concept.get("concept", concept.get("name", "Unknown"))
                concept_desc = concept.get("description", concept.get("details", ""))
                if concept_desc:
                    chunk2_parts.append(f"\n### {i}. {concept_name}")
                    chunk2_parts.append(concept_desc)

        if workflows:
            chunk2_parts.append(f"\n## Workflows ({len(workflows)} total)")
            for i, workflow in enumerate(workflows, 1):
                workflow_name = workflow.get("workflow", workflow.get("name", f"Workflow {i}"))
                chunk2_parts.append(f"\n### Workflow {i}: {workflow_name}")

                # Handle different workflow structures
                if "phases" in workflow:
                    for phase in workflow.get("phases", []):
                        phase_name = phase.get("phase", phase.get("name", ""))
                        phase_steps = phase.get("steps", phase.get("actions", []))
                        chunk2_parts.append(f"\n**{phase_name}:**")
                        for step in phase_steps:
                            chunk2_parts.append(f"- {step}")
                elif "steps" in workflow:
                    for step in workflow.get("steps", []):
                        chunk2_parts.append(f"- {step}")

        chunk2_parts.append(f"\n**Source**: https://youtube.com/watch?v={video_id}")
        chunks.append({
            "content": "\n".join(chunk2_parts),
            "tags": f"{channel.lower().replace(' ', '-')}, {video_id}, concepts, workflows, methodologies",
            "type": "concepts-workflows"
        })

    # CHUNK 3: Detailed Takeaways
    if detailed_takeaways:
        chunk3_parts = [
            f"# {title} - Detailed Takeaways",
            f"\n{len(detailed_takeaways)} Comprehensive Insights:"
        ]

        for i, takeaway in enumerate(detailed_takeaways, 1):
            takeaway_title = takeaway.get("takeaway", f"Takeaway {i}")
            chunk3_parts.append(f"\n## {i}. {takeaway_title}")

            if "why_it_matters" in takeaway:
                chunk3_parts.append(f"\n**Why It Matters**: {takeaway['why_it_matters']}")

            if "implementation" in takeaway:
                chunk3_parts.append(f"\n**Implementation**: {takeaway['implementation']}")

            if "evidence" in takeaway:
                chunk3_parts.append(f"\n**Evidence**: {takeaway['evidence']}")

            if "example" in takeaway:
                chunk3_parts.append(f"\n**Example**: {takeaway['example']}")

        chunk3_parts.append(f"\n**Source**: https://youtube.com/watch?v={video_id}")
        chunks.append({
            "content": "\n".join(chunk3_parts),
            "tags": f"{channel.lower().replace(' ', '-')}, {video_id}, takeaways, insights, best-practices",
            "type": "detailed-takeaways"
        })

    # CHUNK 4: Timestamps & Commands
    if timestamps or commands:
        chunk4_parts = [f"# {title} - Reference Material"]

        if timestamps:
            chunk4_parts.append(f"\n## Video Timeline ({len(timestamps)} segments)")
            for ts in timestamps:
                time_range = ts.get("time_range", ts.get("timestamp", ""))
                description = ts.get("description", ts.get("content", ""))
                chunk4_parts.append(f"\n**{time_range}**: {description}")

        if commands:
            chunk4_parts.append(f"\n## Commands Reference ({len(commands)} commands)")
            for cmd in commands:
                cmd_name = cmd.get("command", cmd.get("name", ""))
                cmd_desc = cmd.get("description", cmd.get("usage", ""))
                chunk4_parts.append(f"\n### `{cmd_name}`")
                if cmd_desc:
                    chunk4_parts.append(cmd_desc)

        chunk4_parts.append(f"\n**Source**: https://youtube.com/watch?v={video_id}")
        chunks.append({
            "content": "\n".join(chunk4_parts),
            "tags": f"{channel.lower().replace(' ', '-')}, {video_id}, timestamps, commands, reference",
            "type": "reference-material"
        })

    # Print all chunks for manual storage
    for i, chunk in enumerate(chunks, 1):
        print(f"\n{'=' * 80}")
        print(f"CHUNK {i} of {len(chunks)} - {chunk['type']}")
        print("=" * 80)
        print(f"\n📋 CONTENT ({len(chunk['content'])} characters):")
        print(chunk['content'][:500] + "..." if len(chunk['content']) > 500 else chunk['content'])
        print(f"\n🏷️  TAGS:")
        print(chunk['tags'])
        print(f"\n💡 To store: mcp__unified-memory__memory_store")

    print("\n" + "=" * 80)
    print(f"✅ Generated {len(chunks)} comprehensive chunks (prevents shallow storage)")
    print("=" * 80)


def main():
    if len(sys.argv) < 2:
        print("=" * 80)
        print("MCP KB Comprehensive Storage Script")
        print("=" * 80)
        print("\nThis script prevents shallow storage by creating multi-chunk memories")
        print("from detailed video analysis files.")
        print("\nUsage:")
        print("  python scripts/store_in_mcp_kb.py <analysis_json_file>")
        print("\nExamples:")
        print("  # New format (comprehensive analysis):")
        print("  python scripts/store_in_mcp_kb.py workspace/analysis/VIDEO_ID_analysis.json")
        print("\n  # Old format (legacy summary):")
        print("  python scripts/store_in_mcp_kb.py workspace/summaries/VIDEO_ID_summary.json")
        print("\nOutput:")
        print("  - Detects format automatically")
        print("  - Generates 3-4 comprehensive chunks per video")
        print("  - Prevents shallow storage issue")
        print("  - Prints chunks for manual MCP KB Memory storage")
        print("=" * 80)
        return

    analysis_file = sys.argv[1]

    if not Path(analysis_file).exists():
        print(f"❌ File not found: {analysis_file}")
        sys.exit(1)

    try:
        store_video_in_mcp_kb(analysis_file)
    except Exception as e:
        print(f"\n❌ Error processing file: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
