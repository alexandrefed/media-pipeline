#!/usr/bin/env python3
"""
Streamlined YouTube video processing workflow using agent-based analysis.

This script combines:
1. Auto-enhancement (174+ corrections)
2. Agent-based intelligent analysis
3. MCP KB Memory preparation

Usage:
    uv run python scripts/streamlined_process.py <youtube_url>
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, description: str) -> tuple[bool, str]:
    """Run a shell command and return success status and output."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} complete")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False, e.stderr


def main():
    if len(sys.argv) < 2:
        print("Streamlined YouTube Video Processing")
        print("\nUsage:")
        print("  uv run python scripts/streamlined_process.py <youtube_url>")
        print("\nExample:")
        print("  uv run python scripts/streamlined_process.py https://youtube.com/watch?v=VIDEO_ID")
        print("\nWorkflow:")
        print("  1. Extract transcript")
        print("  2. Auto-enhance (apply 174+ corrections)")
        print("  3. Intelligent analysis with specialized agent")
        print("  4. Prepare for MCP KB Memory storage")
        return

    youtube_url = sys.argv[1]

    print("\n" + "=" * 80)
    print("STREAMLINED YOUTUBE VIDEO PROCESSING")
    print("=" * 80)
    print(f"\nVideo URL: {youtube_url}")
    print("\nThis workflow will:")
    print("  ✓ Create video folder with metadata")
    print("  ✓ Extract raw transcript")
    print("  ✓ Auto-enhance with 174+ mapped corrections")
    print("  ✓ Analyze using specialized @youtube-transcript-analyzer agent")
    print("  ✓ Generate MCP KB Memory-ready content")
    print("\n" + "=" * 80)

    video_id = youtube_url.split("v=")[-1].split("&")[0]

    # Step 1: Extract transcript
    success, output = run_command(
        f'uv run python main.py extract "{youtube_url}"', "Step 1/4: Extracting raw transcript"
    )

    # Find the video folder (may have been created by extractor)
    video_dirs = list(Path("workspace/videos").glob(f"*--{video_id}--*"))

    if not video_dirs or not success:
        # Fallback: create folder manually and extract via yt-dlp captions
        print("   Trying fallback: direct yt-dlp caption extraction...")
        import re

        Path("workspace/videos").mkdir(parents=True, exist_ok=True)

        # Get metadata via yt-dlp
        meta_cmd = f'yt-dlp --skip-download --print "%(upload_date)s|||%(channel)s|||%(title)s" "{youtube_url}"'
        meta_ok, meta_out = run_command(meta_cmd, "Fetching video metadata")
        if not meta_ok:
            print(f"❌ Cannot fetch metadata for {youtube_url}")
            return

        parts = meta_out.strip().split("|||")
        upload_date = parts[0] if len(parts) > 0 else "00000000"
        channel = parts[1] if len(parts) > 1 else "unknown"
        title = parts[2] if len(parts) > 2 else "unknown"

        channel_slug = re.sub(r"[^a-z0-9-]", "-", channel.lower())[:25]
        title_slug = re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")
        title_slug = "-".join(re.sub(r"-+", "-", title_slug).strip("-").split("-")[:8])

        folder_name = f"{upload_date}--{video_id}--yt--{channel_slug}--{title_slug}"
        video_dir = Path("workspace/videos") / folder_name
        video_dir.mkdir(parents=True, exist_ok=True)

        # Write metadata.json
        import json
        from datetime import datetime, timezone
        metadata = {
            "video_id": video_id, "title": title, "channel": channel,
            "platform": "yt", "upload_date": upload_date, "url": youtube_url,
            "processed_at": datetime.now(timezone.utc).isoformat(),
        }
        (video_dir / "metadata.json").write_text(json.dumps(metadata, indent=2))

        # Download captions via yt-dlp
        vtt_file = video_dir / "subs.en.vtt"
        cap_ok, _ = run_command(
            f'yt-dlp --write-auto-sub --sub-lang en --skip-download --sub-format vtt -o "{video_dir}/subs" "{youtube_url}"',
            "Downloading captions",
        )
        if not cap_ok or not vtt_file.exists():
            print(f"❌ No captions available for {youtube_url}")
            return

        # Convert VTT to text
        vtt_ok, _ = run_command(
            f'uv run python scripts/vtt_to_text.py "{vtt_file}" -o "{video_dir}/transcript_raw.txt"',
            "Converting VTT to text",
        )
        if not vtt_ok:
            print(f"❌ VTT conversion failed")
            return
    else:
        video_dir = video_dirs[0]

    raw_file = video_dir / "transcript_raw.txt"
    if not raw_file.exists():
        print(f"❌ transcript_raw.txt not found in {video_dir}")
        return

    print(f"   📁 Video folder: {video_dir}")
    print(f"   📄 Raw transcript: {raw_file}")

    # Step 2: Auto-enhance
    success, output = run_command(
        f'uv run python -m src.processing.auto_enhancer "{raw_file}"',
        "Step 2/4: Auto-enhancing transcript (174+ corrections)",
    )
    if not success:
        return

    # auto_enhancer writes transcript_raw_auto_enhanced.txt next to input — rename it
    enhanced_legacy = video_dir / "transcript_raw_auto_enhanced.txt"
    enhanced_file = video_dir / "transcript_enhanced.txt"
    if enhanced_legacy.exists():
        enhanced_legacy.rename(enhanced_file)
    print(f"   📄 Enhanced transcript: {enhanced_file}")

    # Step 3: Intelligent analysis with agent
    print("\n🔄 Step 3/4: Analyzing with @youtube-transcript-analyzer agent...")
    print("   (Using specialized agent for high-quality extraction)")

    analysis_file = video_dir / "analysis.json"

    # Use Claude Code to invoke the specialized agent
    agent_cmd = f'claude "Use @youtube-transcript-analyzer to analyze {enhanced_file} and save the JSON output to {analysis_file}"'

    print("\n   💡 Run this command to use the specialized agent:")
    print(f"   {agent_cmd}")
    print("\n   Or manually invoke the agent in Claude Code")

    # Check if analysis exists (user may have run it)
    if analysis_file.exists():
        print("✅ Step 3/4: Analysis complete")
        print(f"   📄 Analysis JSON: {analysis_file}")

        # Step 4: Prepare for MCP KB
        success, output = run_command(
            f'uv run python scripts/store_in_mcp_kb.py "{analysis_file}"',
            "Step 4/4: Preparing for MCP KB Memory",
        )

        if success:
            print("\n" + "=" * 80)
            print("✅ WORKFLOW COMPLETE!")
            print("=" * 80)
            print(f"\n📁 Video folder: {video_dir}")
            print("\n📋 Generated Files:")
            print(f"   1. Raw: {raw_file}")
            print(f"   2. Enhanced: {enhanced_file}")
            print(f"   3. Analysis: {analysis_file}")
            print("\n💡 Next Step:")
            print("   Store in MCP KB Memory using: mcp__unified-memory__memory_store")
            print("=" * 80 + "\n")
    else:
        print("\n⏸️  Workflow paused at Step 3")
        print("   Run the command above to continue with agent analysis")


if __name__ == "__main__":
    main()
