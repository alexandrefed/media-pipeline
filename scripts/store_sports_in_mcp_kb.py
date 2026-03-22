#!/usr/bin/env python3
"""
Store Sports Training Video Content in MCP KB Memory

This script processes sports training video analysis JSON and prepares it for storage
in MCP KB Memory with sports-specific tags and metadata structure.

Usage:
    uv run python scripts/store_sports_in_mcp_kb.py <analysis_json_path>

Example:
    uv run python scripts/store_sports_in_mcp_kb.py workspace/analysis/abc123_sports_analysis.json
"""

import json
import sys
from pathlib import Path
from typing import Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import unified memory client for direct API storage
try:
    from src.storage.unified_memory_client import health_check, store_memory, store_note

    API_AVAILABLE = True
except ImportError:
    print("⚠️  Warning: Unified memory client not available. API storage disabled.")
    API_AVAILABLE = False

# Import webhook notifier for automatic n8n sync
try:
    from notifications.src.core.webhook_notifier import notify_video_processed

    WEBHOOK_AVAILABLE = True
except ImportError:
    print("⚠️  Warning: Webhook notifier not available. Notifications disabled.")
    WEBHOOK_AVAILABLE = False


def load_sports_analysis(json_path: str) -> dict[str, Any]:
    """Load sports analysis JSON file."""
    with open(json_path, encoding="utf-8") as f:
        return json.load(f)


def determine_sport_tags(analysis: dict[str, Any]) -> list[str]:
    """
    Determine sport-specific tags from analysis.

    Returns list of sport tags like:
    - sport-ultra-running
    - sport-hyrox
    - sport-strength-training
    - sport-crossfit
    """
    sport_discipline = analysis.get("sport_discipline", "").lower()

    # Map sport disciplines to tags
    sport_mapping = {
        "strength training": ["sport-strength-training"],
        "ultra running": ["sport-ultra-running", "sport-endurance"],
        "hyrox": ["sport-hyrox", "sport-hybrid-athlete"],
        "crossfit": ["sport-crossfit", "sport-functional-fitness"],
        "hybrid athlete": ["sport-hybrid-athlete", "sport-concurrent-training"],
        "powerlifting": ["sport-powerlifting", "sport-strength-training"],
        "olympic weightlifting": ["sport-olympic-lifting", "sport-strength-training"],
        "calisthenics": ["sport-calisthenics", "sport-bodyweight"],
        "running": ["sport-running", "sport-endurance"],
        "cycling": ["sport-cycling", "sport-endurance"],
        "triathlon": ["sport-triathlon", "sport-hybrid-athlete"],
    }

    tags = []
    for key, sport_tags in sport_mapping.items():
        if key in sport_discipline:
            tags.extend(sport_tags)

    # Fallback to generic if no match
    if not tags:
        tags.append("sport-general-fitness")

    return list(set(tags))  # Deduplicate


def determine_evidence_tier_tag(analysis: dict[str, Any]) -> str:
    """
    Determine highest evidence tier from citations.

    Returns tag like: evidence-tier-1, evidence-tier-2, etc.
    """
    citations = analysis.get("scientific_citations", [])

    if not citations:
        return "evidence-tier-4"  # No citations = lowest tier

    # Find highest evidence tier (1 is best)
    min_tier = min(citation.get("evidence_tier", 4) for citation in citations)

    return f"evidence-tier-{min_tier}"


def determine_content_tags(analysis: dict[str, Any]) -> list[str]:
    """
    Determine content-type tags based on what the video contains.

    Returns tags like:
    - content-exercise-technique
    - content-programming-protocol
    - content-injury-prevention
    - content-scientific-review
    """
    tags = []

    # Check for exercises
    if analysis.get("exercises_demonstrated"):
        tags.append("content-exercise-technique")

    # Check for protocols
    if analysis.get("exercises_demonstrated"):
        # If exercises have detailed protocols, tag as programming
        for exercise in analysis["exercises_demonstrated"]:
            if exercise.get("protocol"):
                tags.append("content-programming-protocol")
                break

    # Check for injury content
    if analysis.get("injury_considerations"):
        tags.append("content-injury-prevention")

    # Check for scientific evidence
    if analysis.get("scientific_citations"):
        tags.append("content-evidence-based")

        # If multiple high-tier citations, tag as review
        high_tier_citations = [
            c for c in analysis["scientific_citations"] if c.get("evidence_tier", 4) <= 2
        ]
        if len(high_tier_citations) >= 3:
            tags.append("content-scientific-review")

    # Check for biomechanics
    if analysis.get("biomechanical_principles"):
        tags.append("content-biomechanics")

    # Check for WHY reasoning
    if analysis.get("why_reasoning"):
        tags.append("content-why-reasoning")

    return tags


def format_exercise_for_kb(exercise: dict[str, Any]) -> str:
    """Format exercise details for KB storage."""
    name = exercise.get("name", "Unknown Exercise")
    category = exercise.get("category", "")
    protocol = exercise.get("protocol", {})

    sections = [f"**Exercise**: {name}"]

    if category:
        sections.append(f"**Category**: {category}")

    if protocol:
        sections.append("\n**Protocol**:")
        if protocol.get("volume"):
            sections.append(f"- Volume: {protocol['volume']}")
        if protocol.get("frequency"):
            sections.append(f"- Frequency: {protocol['frequency']}")
        if protocol.get("intensity"):
            sections.append(f"- Intensity: {protocol['intensity']}")
        if protocol.get("tempo"):
            sections.append(f"- Tempo: {protocol['tempo']}")
        if protocol.get("progression"):
            sections.append(f"- Progression: {protocol['progression']}")

    return "\n".join(sections)


def format_citation_for_kb(citation: dict[str, Any]) -> str:
    """Format scientific citation for KB storage."""
    cite = citation.get("citation", "Unknown")
    study_type = citation.get("study_type", "")
    finding = citation.get("finding", "")
    tier = citation.get("evidence_tier", 4)

    sections = [f"**{cite}** (Evidence Tier {tier})"]

    if study_type:
        sections.append(f"- Study Type: {study_type}")

    if finding:
        sections.append(f"- Finding: {finding}")

    return "\n".join(sections)


def create_mcp_kb_content(analysis: dict[str, Any], video_id: str, channel: str) -> str:
    """
    Create formatted content for MCP KB Memory storage.

    Structures content into searchable sections with clear hierarchy.
    """
    sections = []

    # Header
    sections.append(f"**Video**: {video_id}")
    sections.append(f"**Channel**: {channel}")
    sections.append(f"**Sport**: {analysis.get('sport_discipline', 'General Fitness')}")
    sections.append(f"**Target Audience**: {analysis.get('target_audience', 'All Levels')}")
    sections.append("")

    # Summary
    if analysis.get("summary"):
        sections.append("## Summary")
        sections.append(analysis["summary"])
        sections.append("")

    # Exercises
    if analysis.get("exercises_demonstrated"):
        sections.append("## Exercises Demonstrated")
        sections.append("")
        for i, exercise in enumerate(analysis["exercises_demonstrated"], 1):
            sections.append(f"### Exercise {i}")
            sections.append(format_exercise_for_kb(exercise))
            sections.append("")

    # Scientific Evidence
    if analysis.get("scientific_citations"):
        sections.append("## Scientific Evidence")
        sections.append("")
        for i, citation in enumerate(analysis["scientific_citations"], 1):
            sections.append(f"### Citation {i}")
            sections.append(format_citation_for_kb(citation))
            sections.append("")

    # Biomechanical Principles
    if analysis.get("biomechanical_principles"):
        sections.append("## Biomechanical Principles")
        sections.append("")
        for principle in analysis["biomechanical_principles"]:
            sections.append(f"- {principle}")
        sections.append("")

    # WHY Reasoning
    if analysis.get("why_reasoning"):
        sections.append("## WHY Reasoning")
        why = analysis["why_reasoning"]

        if why.get("biomechanical"):
            sections.append("### Biomechanical")
            sections.append(why["biomechanical"])
            sections.append("")

        if why.get("physiological"):
            sections.append("### Physiological")
            sections.append(why["physiological"])
            sections.append("")

        if why.get("tactical"):
            sections.append("### Tactical")
            sections.append(why["tactical"])
            sections.append("")

    # Implementation Details
    if analysis.get("implementation_details"):
        sections.append("## Implementation Details")
        impl = analysis["implementation_details"]

        if impl.get("setup"):
            sections.append("### Setup")
            for step in impl["setup"]:
                sections.append(f"- {step}")
            sections.append("")

        if impl.get("execution"):
            sections.append("### Execution")
            for step in impl["execution"]:
                sections.append(f"- {step}")
            sections.append("")

        if impl.get("common_errors"):
            sections.append("### Common Errors")
            for error in impl["common_errors"]:
                if isinstance(error, dict):
                    sections.append(f"- **Error**: {error.get('error', '')}")
                    sections.append(f"  **Fix**: {error.get('fix', '')}")
                else:
                    sections.append(f"- {error}")
            sections.append("")

    # Injury Considerations
    if analysis.get("injury_considerations"):
        sections.append("## Injury Considerations")
        inj = analysis["injury_considerations"]

        if inj.get("contraindications"):
            sections.append("### Contraindications")
            for contra in inj["contraindications"]:
                sections.append(f"- {contra}")
            sections.append("")

        if inj.get("modifications"):
            sections.append("### Modifications")
            for mod in inj["modifications"]:
                if isinstance(mod, dict):
                    sections.append(
                        f"- **{mod.get('condition', '')}**: {mod.get('modification', '')}"
                    )
                else:
                    sections.append(f"- {mod}")
            sections.append("")

    # Key Takeaways
    if analysis.get("key_takeaways"):
        sections.append("## Key Takeaways")
        sections.append("")
        for i, takeaway in enumerate(analysis["key_takeaways"], 1):
            sections.append(f"{i}. {takeaway}")
        sections.append("")

    # Watch link
    video_url = f"https://youtube.com/watch?v={video_id}"
    sections.append(f"**Watch**: {video_url}")

    return "\n".join(sections)


def generate_mcp_storage_instructions(
    content: str, video_id: str, channel: str, analysis: dict[str, Any]
) -> str:
    """
    Generate instructions for storing content in MCP KB Memory.

    Returns formatted text with tags and metadata structure.
    """
    # Determine all tags
    sport_tags = determine_sport_tags(analysis)
    evidence_tag = determine_evidence_tier_tag(analysis)
    content_tags = determine_content_tags(analysis)

    all_tags = (
        [
            "youtube-knowledge-base",
            f"video-{video_id}",
            f'channel-{channel.lower().replace(" ", "-")}',
            "content-type-sports",
            evidence_tag,
        ]
        + sport_tags
        + content_tags
    )

    # Remove duplicates
    all_tags = list(set(all_tags))

    # Format tags as comma-separated string
    ",".join(all_tags)

    instructions = []
    instructions.append("# MCP KB Memory Storage Instructions")
    instructions.append("")
    instructions.append("Use the following command to store this content in MCP KB Memory:")
    instructions.append("")
    instructions.append("```")
    instructions.append("Use mcp__unified-memory__memory_store with:")
    instructions.append("")
    instructions.append("content:")
    instructions.append('"""')
    instructions.append(content)
    instructions.append('"""')
    instructions.append("")
    instructions.append("tags: " + str(all_tags))
    instructions.append("namespace: 'youtube-knowledge-base'")
    instructions.append("metadata: {'type': 'sports-training'}")
    instructions.append("```")
    instructions.append("")
    instructions.append("## Tags Breakdown")
    instructions.append("")
    instructions.append("**Domain Tags**:")
    for tag in sport_tags:
        instructions.append(f"- {tag}")
    instructions.append("")
    instructions.append("**Evidence Quality**:")
    instructions.append(f"- {evidence_tag}")
    instructions.append("")
    instructions.append("**Content Type**:")
    for tag in content_tags:
        instructions.append(f"- {tag}")
    instructions.append("")
    instructions.append("**Metadata**:")
    instructions.append(f"- Video ID: {video_id}")
    instructions.append(f"- Channel: {channel}")
    instructions.append(f"- Sport: {analysis.get('sport_discipline', 'N/A')}")
    instructions.append(f"- Exercises: {len(analysis.get('exercises_demonstrated', []))}")
    instructions.append(f"- Citations: {len(analysis.get('scientific_citations', []))}")
    instructions.append("")

    return "\n".join(instructions)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(
            "Usage: uv run python scripts/store_sports_in_mcp_kb.py <analysis_json_path> [--dry-run]"
        )
        print("")
        print("Options:")
        print("  --dry-run    Save to file without storing via API (old behavior)")
        print("")
        print("Example:")
        print(
            "  uv run python scripts/store_sports_in_mcp_kb.py workspace/analysis/abc123_sports_analysis.json"
        )
        sys.exit(1)

    dry_run = "--dry-run" in sys.argv
    analysis_path = [a for a in sys.argv[1:] if not a.startswith("--")][0]

    # Validate file exists
    if not Path(analysis_path).exists():
        print(f"Error: File not found: {analysis_path}")
        sys.exit(1)

    # Load analysis
    print(f"Loading sports analysis from: {analysis_path}")
    analysis = load_sports_analysis(analysis_path)

    # Extract video metadata
    video_id = analysis.get("video_id")
    if not video_id:
        filename = Path(analysis_path).stem
        video_id = filename.replace("_sports_analysis", "").replace("_analysis", "")

    channel = analysis.get("channel", "Unknown Channel")

    print(f"Video ID: {video_id}")
    print(f"Channel: {channel}")
    print(f"Sport: {analysis.get('sport_discipline', 'N/A')}")
    print("")

    # Generate content
    print("Generating content...")
    content = create_mcp_kb_content(analysis, video_id, channel)

    # Determine tags
    sport_tags = determine_sport_tags(analysis)
    evidence_tag = determine_evidence_tier_tag(analysis)
    content_tags = determine_content_tags(analysis)

    all_tags = list(
        set(
            [
                "source:openclaw-main",
                "project:ai-knowledge-base",
                "type:context",
                "area:mutora",
                "youtube-knowledge-base",
                f"video-{video_id}",
                f"channel-{channel.lower().replace(' ', '-')}",
                "content-type-sports",
                evidence_tag,
            ]
            + sport_tags
            + content_tags
        )
    )

    if dry_run or not API_AVAILABLE:
        # Old behavior: save to file
        if not API_AVAILABLE and not dry_run:
            print("⚠️  API client unavailable, falling back to file output")

        instructions = generate_mcp_storage_instructions(content, video_id, channel, analysis)
        output_path = Path("workspace/mcp_ready") / f"{video_id}_sports_mcp_ready.txt"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(instructions)
        print(f"✅ MCP-ready content saved to: {output_path}")
    else:
        # NEW: Store via unified-memory API
        print("\n📡 Storing via unified-memory API...")

        if not health_check():
            print("❌ Unified-memory API unreachable. Use --dry-run to save to file instead.")
            sys.exit(1)

        video_url = f"https://youtube.com/watch?v={video_id}"

        # 1. Store NOTE (syncs to Notion)
        note_title = analysis.get("title", f"Sports: {video_id}")
        note_metadata = {
            "area": "mutora",
            "video_id": video_id,
            "source": "youtube",
            "url": video_url,
            "channel": channel,
            "format": "long",
            "sport": analysis.get("sport_discipline", ""),
        }
        # Build note: summary + key takeaways (truncated to ~2000 chars)
        note_parts = [f"# {note_title}", f"**Channel**: {channel}", ""]
        if analysis.get("summary"):
            note_parts.extend(["## Summary", analysis["summary"], ""])
        if analysis.get("key_takeaways"):
            note_parts.append("## Key Takeaways")
            for i, t in enumerate(analysis["key_takeaways"], 1):
                note_parts.append(f"{i}. {t}")
            note_parts.append("")
        note_parts.append(f"**Watch**: {video_url}")

        try:
            note_result = store_note(
                title=f"Video: {note_title}",
                content="\n".join(note_parts),
                note_type="video",
                metadata=note_metadata,
            )
            print(f"✅ Note stored (syncs to Notion): {note_result.get('id', 'ok')}")
        except Exception as e:
            print(f"⚠️  Note storage failed: {e}")

        # 2. Store MEMORY (full content for agent retrieval)
        try:
            mem_result = store_memory(
                content=content,
                tags=all_tags,
                namespace="/alex/openclaw/videos/",
                metadata={"video_id": video_id, "area": "mutora", "type": "video-knowledge"},
            )
            print(f"✅ Memory stored (agent retrieval): {mem_result.get('id', 'ok')}")
        except Exception as e:
            print(f"⚠️  Memory storage failed: {e}")

    print("\nQuick stats:")
    print(f"- Exercises extracted: {len(analysis.get('exercises_demonstrated', []))}")
    print(f"- Scientific citations: {len(analysis.get('scientific_citations', []))}")
    print(f"- Evidence tier: {evidence_tag}")
    print(f"- Sport tags: {', '.join(sport_tags)}")

    # Automatically sync to n8n webhook for notifications
    if WEBHOOK_AVAILABLE:
        print("\n🔔 Syncing to n8n for automated notifications...")
        try:
            webhook_success = notify_video_processed(analysis_path)
            if webhook_success:
                print("✅ Successfully synced to n8n - notifications enabled")
            else:
                print("⚠️  Webhook sync failed - see error messages above")
        except Exception as webhook_error:
            print(f"⚠️  Webhook sync error: {webhook_error}")


if __name__ == "__main__":
    main()
