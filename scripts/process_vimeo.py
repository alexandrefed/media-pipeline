#!/usr/bin/env python3
"""
Process Vimeo Video - Download Audio or Extract Transcript

This script handles Vimeo conference videos in two ways:
1. If subtitles exist: Extract them directly
2. If no subtitles: Download audio (MP3) for transcription

Usage:
    uv run python scripts/process_vimeo.py <vimeo_url> [--browser chrome|firefox|edge] [--audio-only]

Example:
    uv run python scripts/process_vimeo.py https://vimeo.com/1133050369
    uv run python scripts/process_vimeo.py https://vimeo.com/1133050369 --audio-only
    uv run python scripts/process_vimeo.py https://vimeo.com/1133050369 --browser firefox
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline.text_reconstructor import TextReconstructor
from src.pipeline.vimeo_extractor import VimeoTranscriptExtractor


def process_vimeo_video(url: str, browser: str = "chrome", audio_only: bool = False) -> None:
    """
    Extract and process a Vimeo video - audio or transcript.

    Steps:
        1. Try to extract subtitles if they exist
        2. If no subtitles (or audio_only=True), download audio as MP3

    Args:
        url: Vimeo video URL
        browser: Browser to use for authentication (chrome, firefox, edge, safari)
        audio_only: Skip subtitle extraction and download audio directly
    """
    print("=" * 80)
    print("VIMEO VIDEO PROCESSING")
    print("=" * 80)
    print(f"\n📹 Video URL: {url}")
    print(f"🔐 Authentication: {browser.title()} browser cookies")
    print()

    extractor = VimeoTranscriptExtractor(browser=browser)
    video_id = extractor.extract_video_id(url)

    # Try subtitle extraction first (unless audio_only is specified)
    if not audio_only:
        print("🔄 Step 1/2: Attempting to extract subtitles from Vimeo...")

        try:
            raw_segments_file = extractor.extract_and_save_raw(url)
            print(f"✅ Step 1/2: Subtitles found! Saved to {raw_segments_file}")

            # Step 2: Reconstruct readable text
            print("\n🔄 Step 2/2: Reconstructing readable text...")
            reconstructor = TextReconstructor()

            import json

            with open(raw_segments_file, encoding="utf-8") as f:
                data = json.load(f)

            raw_segments = data["raw_segments"]
            metadata = data["metadata"]

            # Reconstruct text
            reconstructed_text = reconstructor.reconstruct_from_segments(raw_segments)

            # Save to text file
            output_file = f"raw_text_for_enhancement_vimeo_{video_id}.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("# Vimeo Video Transcript\n")
                f.write(f"# Video ID: {video_id}\n")
                f.write(f"# Title: {metadata.get('title', 'Unknown')}\n")
                f.write(f"# URL: {url}\n")
                f.write(f"\n{'=' * 80}\n\n")
                f.write(reconstructed_text)

            print(f"✅ Step 2/2: Readable text saved to {output_file}")
            print("\n" + "=" * 80)
            print("✅ SUBTITLE EXTRACTION COMPLETE!")
            print("=" * 80)
            return

        except Exception as e:
            print(f"\n⚠️  No subtitles available: {e}")
            print("\n🎵 Falling back to audio download...")
    else:
        print("🎵 Audio-only mode: Skipping subtitle extraction")

    # Download audio
    print("\n🔄 Downloading audio from Vimeo video...")
    print("⏱️  This may take a few minutes for long videos...")
    print()

    try:
        mp3_file = extractor.download_audio(url, output_dir=".")
        print("\n✅ Audio downloaded successfully!")
        print(f"📁 File: {mp3_file}")

        # Get file size
        file_size_mb = Path(mp3_file).stat().st_size / (1024 * 1024)
        print(f"📊 Size: {file_size_mb:.1f} MB")

    except Exception as e:
        print(f"\n❌ Audio download failed: {e}")
        print("\n💡 Troubleshooting tips:")
        print(f"   1. Make sure you're logged into Vimeo in {browser.title()}")
        print(f"   2. Open the video in {browser.title()} and verify you can watch it")
        print("   3. Check if the video is private/restricted")
        print("   4. Try a different browser: --browser firefox or --browser edge")
        print("   5. Make sure ffmpeg is installed: brew install ffmpeg")
        sys.exit(1)

    print()
    print("=" * 80)
    print("✅ AUDIO DOWNLOAD COMPLETE!")
    print("=" * 80)
    print()
    print("📄 Next Steps - Transcription Options:")
    print()
    print("Option 1: Use OpenAI Whisper API (Recommended)")
    print("   - Most accurate for conference audio")
    print("   - Handles multiple speakers")
    print("   - Cost: ~$0.006/minute ($0.36 for 1 hour)")
    print("   - Setup: Add OPENAI_API_KEY to .env file")
    print()
    print("Option 2: Use Local Whisper (Free)")
    print("   - Install: pip install openai-whisper")
    print("   - Run: whisper " + mp3_file + " --model medium --language en")
    print("   - Slower but free")
    print()
    print("Option 3: Use Assembly AI (Alternative)")
    print("   - Good accuracy, fast processing")
    print("   - Cost: ~$0.015/minute")
    print()
    print("💡 For your use case:")
    print("   1. Transcribe the audio using one of the above options")
    print("   2. Review the transcript and identify key sections")
    print("   3. Extract strategic insights for your startup")
    print("   4. Add selected insights to your knowledge base")
    print()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    url = None
    browser = "chrome"
    audio_only = False

    # Parse arguments
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--browser" and i + 1 < len(args):
            browser = args[i + 1]
            i += 2
        elif args[i] == "--audio-only":
            audio_only = True
            i += 1
        elif args[i].startswith("--"):
            print(f"Unknown option: {args[i]}")
            print(__doc__)
            sys.exit(1)
        else:
            url = args[i]
            i += 1

    if not url:
        print("Error: No Vimeo URL provided")
        print(__doc__)
        sys.exit(1)

    # Validate browser choice
    valid_browsers = ["chrome", "firefox", "edge", "safari"]
    if browser not in valid_browsers:
        print(f"Error: Invalid browser '{browser}'. Choose from: {', '.join(valid_browsers)}")
        sys.exit(1)

    process_vimeo_video(url, browser, audio_only)


if __name__ == "__main__":
    main()
