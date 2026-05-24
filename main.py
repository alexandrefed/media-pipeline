"""
AI Knowledge Base - Main Application Entry Point

This is the main entry point for the AI Knowledge Base system.
Provides CLI interface for video processing and knowledge querying.
"""

import sys

from src.pipeline.youtube_processor import YouTubeProcessor


def extract_video_for_enhancement(url: str) -> None:
    """Extract video transcript for manual Claude Code enhancement."""
    print(f"Extracting video for manual enhancement: {url}")

    processor = YouTubeProcessor()
    try:
        text_file = processor.process_for_manual_enhancement(url)
        print(f"Text extracted and saved to: {text_file}")
        print(f"Next step: Enhance this text manually in Claude Code")
    except Exception as e:
        print(f"Error extracting video: {e}")


def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print("AI Knowledge Base - Usage:")
        print()
        print("  python main.py streamlined <youtube_url>  - Complete workflow with agent analysis")
        print("  python main.py extract <youtube_url>      - Extract transcript only")
        return

    command = sys.argv[1]

    if command == "streamlined":
        if len(sys.argv) < 3:
            print("Error: Please provide a YouTube URL")
            return

        url = sys.argv[2]
        print("Running streamlined workflow...")
        print("   This uses the new agent-based analysis system")
        print()

        # Import and run streamlined process
        import subprocess
        subprocess.run([sys.executable, "scripts/streamlined_process.py", url])

    elif command == "extract":
        if len(sys.argv) < 3:
            print("Error: Please provide a YouTube URL")
            return

        url = sys.argv[2]
        extract_video_for_enhancement(url)

    else:
        print(f"Error: Unknown command: {command}")
        print("Run 'python main.py' with no arguments to see usage.")


if __name__ == "__main__":
    main()
