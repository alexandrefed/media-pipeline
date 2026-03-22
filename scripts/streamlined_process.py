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
    print("  ✓ Extract raw transcript")
    print("  ✓ Auto-enhance with 174+ mapped corrections")
    print("  ✓ Analyze using specialized @youtube-transcript-analyzer agent")
    print("  ✓ Generate MCP KB Memory-ready content")
    print("\n" + "=" * 80)

    # Step 1: Extract
    success, output = run_command(
        f'uv run python main.py extract "{youtube_url}"', "Step 1/4: Extracting raw transcript"
    )
    if not success:
        return

    # Find the generated raw transcript file
    # Pattern: raw_text_for_enhancement_VIDEO_ID.txt
    video_id = youtube_url.split("v=")[-1].split("&")[0]
    raw_file = f"raw_text_for_enhancement_{video_id}.txt"

    if not Path(raw_file).exists():
        print(f"❌ Could not find extracted file: {raw_file}")
        return

    print(f"   📄 Raw transcript: {raw_file}")

    # Step 2: Auto-enhance
    success, output = run_command(
        f'uv run python -m src.processing.auto_enhancer "{raw_file}"',
        "Step 2/4: Auto-enhancing transcript (174+ corrections)",
    )
    if not success:
        return

    enhanced_file = raw_file.replace(".txt", "_auto_enhanced.txt")
    print(f"   📄 Enhanced transcript: {enhanced_file}")

    # Step 3: Intelligent analysis with agent
    print("\n🔄 Step 3/4: Analyzing with @youtube-transcript-analyzer agent...")
    print("   (Using specialized agent for high-quality extraction)")

    # Use Claude Code to invoke the specialized agent
    agent_cmd = f'claude "Use @youtube-transcript-analyzer to analyze {enhanced_file} and save the JSON output to {enhanced_file.replace(".txt", "_analysis.json")}"'

    print("\n   💡 Run this command to use the specialized agent:")
    print(f"   {agent_cmd}")
    print("\n   Or manually invoke the agent in Claude Code")

    analysis_file = enhanced_file.replace(".txt", "_analysis.json")

    # Check if analysis exists (user may have run it)
    if Path(analysis_file).exists():
        print("✅ Step 3/4: Analysis complete")
        print(f"   📄 Analysis JSON: {analysis_file}")

        # Step 4: Prepare for MCP KB
        success, output = run_command(
            f'uv run python scripts/store_in_mcp_kb.py "{analysis_file}"',
            "Step 4/4: Preparing for MCP KB Memory",
        )

        if success:
            mcp_ready_file = analysis_file.replace("_analysis.json", "_mcp_kb_ready.txt")
            print(f"   📄 MCP KB ready: {mcp_ready_file}")

            print("\n" + "=" * 80)
            print("✅ WORKFLOW COMPLETE!")
            print("=" * 80)
            print("\n📋 Generated Files:")
            print(f"   1. Raw: {raw_file}")
            print(f"   2. Enhanced: {enhanced_file}")
            print(f"   3. Analysis: {analysis_file}")
            print(f"   4. MCP KB Ready: {mcp_ready_file}")
            print("\n💡 Next Step:")
            print(f"   Store in MCP KB Memory using the content in: {mcp_ready_file}")
            print("\n   Use: mcp__unified-memory__memory_store")
            print("=" * 80 + "\n")
    else:
        print("\n⏸️  Workflow paused at Step 3")
        print("   Run the command above to continue with agent analysis")


if __name__ == "__main__":
    main()
