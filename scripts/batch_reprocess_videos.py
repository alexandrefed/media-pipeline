#!/usr/bin/env python3
"""
Batch re-process all existing videos with enhanced v2 storage.

This script:
1. Finds all analysis JSON files
2. Generates multi-memory storage for each
3. Outputs a JSON file for Claude Code to store via MCP KB API
"""

import json
from pathlib import Path

from store_in_mcp_kb import EnhancedKBStorage


def find_analysis_files(analysis_dir: Path) -> list[Path]:
    """Find all analysis JSON files."""
    # Find files matching the pattern raw_text_for_enhancement_*_auto_enhanced_analysis.json
    # These are the original JSON files before store_in_mcp_kb.py overwrote some
    enhanced_files = list(
        analysis_dir.glob("raw_text_for_enhancement_*_auto_enhanced_analysis.json")
    )

    # Also find clean pattern files (VIDEO_ID_analysis.json) that still have valid JSON
    clean_pattern = list(analysis_dir.glob("*_analysis.json"))
    clean_files = [f for f in clean_pattern if not f.name.startswith("raw_text_for_enhancement")]

    # Combine and deduplicate by video ID
    all_files = enhanced_files + clean_files

    # Deduplicate - prefer enhanced files over clean files
    seen_ids = set()
    unique_files = []
    for f in all_files:
        # Check if file is valid JSON
        try:
            with open(f) as test_file:
                json.load(test_file)
            # Extract video ID
            name = f.stem
            if "_analysis" in name:
                vid_id = (
                    name.replace("_analysis", "")
                    .replace("raw_text_for_enhancement_", "")
                    .replace("_auto_enhanced", "")
                )
            else:
                vid_id = name
            if vid_id not in seen_ids:
                seen_ids.add(vid_id)
                unique_files.append(f)
        except (json.JSONDecodeError, Exception):
            # Skip invalid JSON files
            continue

    return sorted(unique_files)


def process_all_videos(analysis_dir: Path, output_dir: Path) -> dict:
    """Process all videos and generate memories."""
    analysis_files = find_analysis_files(analysis_dir)

    print(f"🎬 Found {len(analysis_files)} videos to process")
    print("=" * 80)

    results = {"total_videos": len(analysis_files), "total_memories": 0, "videos": []}

    for i, analysis_file in enumerate(analysis_files, 1):
        print(f"\n[{i}/{len(analysis_files)}] Processing: {analysis_file.name}")

        try:
            # Create storage handler
            storage = EnhancedKBStorage(str(analysis_file))

            # Generate memories
            memories = storage.generate_all_memories()

            print(f"   ✅ Generated {len(memories)} memories for {storage.video_id}")

            # Save to output directory
            output_file = output_dir / f"{storage.video_id}_memories.json"
            video_data = {
                "video_id": storage.video_id,
                "total_memories": len(memories),
                "memories": memories,
            }

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(video_data, f, indent=2)

            results["total_memories"] += len(memories)
            results["videos"].append(
                {
                    "video_id": storage.video_id,
                    "memories_count": len(memories),
                    "output_file": str(output_file),
                }
            )

        except Exception as e:
            print(f"   ❌ Error processing {analysis_file.name}: {e}")
            continue

    return results


def main():
    """CLI entry point."""
    print("=" * 80)
    print("BATCH VIDEO REPROCESSING - Enhanced MCP KB Storage")
    print("=" * 80)

    # Setup paths
    project_root = Path(__file__).parent.parent
    analysis_dir = project_root / "workspace" / "analysis"
    output_dir = project_root / "workspace" / "mcp_ready"
    output_dir.mkdir(exist_ok=True)

    # Process all videos
    results = process_all_videos(analysis_dir, output_dir)

    # Save summary
    summary_file = output_dir / "_batch_processing_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print("\n" + "=" * 80)
    print("📊 BATCH PROCESSING SUMMARY")
    print("=" * 80)
    print(f"Total videos processed: {results['total_videos']}")
    print(f"Total memories generated: {results['total_memories']}")
    print(f"Average memories per video: {results['total_memories'] / results['total_videos']:.1f}")
    print(f"\n✅ All memories saved to: {output_dir}")
    print(f"📄 Summary saved to: {summary_file}")
    print("\n💡 Next step: Use Claude Code to store all memories via MCP KB API")
    print("=" * 80)


if __name__ == "__main__":
    main()
