#!/usr/bin/env python3
"""
Audio Transcription Script using AssemblyAI

Transcribes audio files (M4A, MP3, WAV, etc.) to text using AssemblyAI's API.
Supports large files (4+ hours, 100+ MB) with progress tracking.

Usage:
    uv run python scripts/transcribe_audio.py <audio_file.m4a>
    uv run python scripts/transcribe_audio.py <audio_file.m4a> --output transcript.txt

Features:
    - Supports M4A, MP3, WAV, FLAC, and other formats
    - Progress tracking during transcription
    - Speaker diarization (optional)
    - Automatic punctuation and formatting
    - Timestamps for each word/phrase
"""

import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import assemblyai as aai
except ImportError:
    print("❌ Error: assemblyai library not installed")
    print("   Install with: uv add assemblyai")
    sys.exit(1)

# Load API key from environment
from dotenv import load_dotenv

load_dotenv()

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")


class AudioTranscriber:
    """Handles audio transcription using AssemblyAI."""

    def __init__(self, api_key: str | None = None):
        """
        Initialize transcriber with API key.

        Args:
            api_key: AssemblyAI API key (if not provided, loads from env)
        """
        self.api_key = api_key or ASSEMBLYAI_API_KEY

        if not self.api_key:
            raise ValueError(
                "AssemblyAI API key not found!\n"
                "Please set ASSEMBLYAI_API_KEY in your .env file or pass it as argument.\n"
                "Sign up for free at: https://www.assemblyai.com/"
            )

        # Configure AssemblyAI
        aai.settings.api_key = self.api_key

    def transcribe_file(
        self,
        audio_file: str,
        output_file: str | None = None,
        speaker_labels: bool = False,
        auto_highlights: bool = True,
        language: str = "en",
    ) -> str:
        """
        Transcribe an audio file to text.

        Args:
            audio_file: Path to audio file (M4A, MP3, WAV, etc.)
            output_file: Optional output file path (default: audio_file + .txt)
            speaker_labels: Enable speaker diarization (who spoke when)
            auto_highlights: Automatically detect key phrases/topics
            language: Language code (en, fr, es, de, etc.)

        Returns:
            Path to the output transcript file
        """
        audio_path = Path(audio_file)

        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_file}")

        # Get file info
        file_size_mb = audio_path.stat().st_size / (1024 * 1024)
        print(f"\n{'=' * 80}")
        print("AUDIO TRANSCRIPTION - AssemblyAI")
        print(f"{'=' * 80}")
        print(f"\n📁 File: {audio_path.name}")
        print(f"📊 Size: {file_size_mb:.1f} MB")
        print(f"🔑 Using API key: {self.api_key[:8]}...{self.api_key[-4:]}")
        print()

        # Configure transcription settings
        config = aai.TranscriptionConfig(
            speaker_labels=speaker_labels, auto_highlights=auto_highlights, language_code=language
        )

        # Create transcriber
        transcriber = aai.Transcriber(config=config)

        # Upload and transcribe
        print("🔄 Step 1/3: Uploading audio file...")
        print("   (This may take a few minutes for large files)")

        transcript = transcriber.transcribe(str(audio_path))

        # Wait for transcription to complete
        print("\n🔄 Step 2/3: Transcribing audio...")
        print("   (Processing time: ~0.25x audio duration)")
        print("   For 4-hour audio: ~60 minutes expected\n")

        # Poll for status
        while transcript.status not in [aai.TranscriptStatus.completed, aai.TranscriptStatus.error]:
            print(f"   Status: {transcript.status.value}...", end="\r")
            transcript.get_transcript()

        print()  # New line after polling

        if transcript.status == aai.TranscriptStatus.error:
            raise Exception(f"Transcription failed: {transcript.error}")

        print("✅ Step 2/3: Transcription complete!")

        # Prepare output
        print("\n🔄 Step 3/3: Saving transcript...")

        if not output_file:
            output_file = audio_path.stem + "_transcript.txt"

        output_path = Path(output_file)

        # Build transcript content
        content = []
        content.append("# Audio Transcription")
        content.append(f"# File: {audio_path.name}")
        content.append(f"# Transcribed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        content.append(f"# Duration: {transcript.audio_duration / 60:.1f} minutes")
        content.append("# Service: AssemblyAI")
        content.append(f"\n{'=' * 80}\n")

        # Add main transcript
        content.append("## Full Transcript\n")
        content.append(transcript.text)
        content.append("\n")

        # Add speaker labels if enabled
        if speaker_labels and transcript.utterances:
            content.append(f"\n{'=' * 80}")
            content.append("\n## Transcript with Speaker Labels\n")
            for utterance in transcript.utterances:
                content.append(
                    f"\n**Speaker {utterance.speaker}** ({utterance.start / 1000:.1f}s - {utterance.end / 1000:.1f}s):"
                )
                content.append(f"{utterance.text}\n")

        # Add key highlights if available
        if auto_highlights and transcript.auto_highlights:
            content.append(f"\n{'=' * 80}")
            content.append("\n## Key Highlights & Topics\n")
            for highlight in transcript.auto_highlights.results:
                content.append(f"\n### {highlight.text}")
                content.append(f"Relevance: {highlight.rank * 100:.0f}%")
                content.append(
                    f"Timestamps: {', '.join([f'{ts / 1000:.1f}s' for ts in highlight.timestamps])}"
                )
                content.append("")

        # Write to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(content))

        print(f"✅ Step 3/3: Transcript saved to {output_path}")

        # Print stats
        print(f"\n{'=' * 80}")
        print("📊 TRANSCRIPTION STATISTICS")
        print(f"{'=' * 80}")
        print(f"   Audio Duration: {transcript.audio_duration / 60:.1f} minutes")
        print(f"   Words: {len(transcript.text.split())}")
        print(f"   Characters: {len(transcript.text)}")

        if speaker_labels and transcript.utterances:
            num_speakers = len({u.speaker for u in transcript.utterances})
            print(f"   Speakers Detected: {num_speakers}")

        if auto_highlights and transcript.auto_highlights:
            print(f"   Key Topics: {len(transcript.auto_highlights.results)}")

        print(f"\n✅ Transcription complete! Check {output_path}")
        print()

        return str(output_path)


def main():
    """Main entry point for CLI."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Transcribe audio files using AssemblyAI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Basic transcription
    uv run python scripts/transcribe_audio.py conference.m4a

    # Specify output file
    uv run python scripts/transcribe_audio.py conference.m4a --output transcript.txt

    # Enable speaker labels (who spoke when)
    uv run python scripts/transcribe_audio.py conference.m4a --speakers

    # Disable auto-highlights
    uv run python scripts/transcribe_audio.py conference.m4a --no-highlights

Get your free API key at: https://www.assemblyai.com/
(100 hours free transcription)
        """,
    )

    parser.add_argument("audio_file", help="Path to audio file (M4A, MP3, WAV, FLAC, etc.)")

    parser.add_argument(
        "--output",
        "-o",
        help="Output transcript file path (default: <input>_transcript.txt)",
        default=None,
    )

    parser.add_argument(
        "--speakers",
        "-s",
        action="store_true",
        help="Enable speaker diarization (detect who spoke when)",
    )

    parser.add_argument(
        "--no-highlights", action="store_true", help="Disable automatic key highlights detection"
    )

    parser.add_argument(
        "--api-key", help="AssemblyAI API key (or set ASSEMBLYAI_API_KEY in .env)", default=None
    )

    parser.add_argument(
        "--language",
        "-l",
        help="Language code (en, fr, es, de, it, pt, nl, hi, ja, zh, etc.)",
        default="en",
    )

    args = parser.parse_args()

    try:
        # Create transcriber
        transcriber = AudioTranscriber(api_key=args.api_key)

        # Transcribe
        output_file = transcriber.transcribe_file(
            audio_file=args.audio_file,
            output_file=args.output,
            speaker_labels=args.speakers,
            auto_highlights=not args.no_highlights,
            language=args.language,
        )

        print("💡 Next steps:")
        print(f"   1. Review the transcript: {output_file}")
        print("   2. Extract key sections for your startup strategy")
        print("   3. Use AI Knowledge Base tools to analyze insights")
        print()

    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
