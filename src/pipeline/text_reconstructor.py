"""
Text Reconstructor for YouTube Transcripts
Extracts clean, flowing text from raw VTT segments
"""

import re

import pysbd


class TextReconstructor:
    """Reconstructs clean text from raw VTT segments."""

    def __init__(self):
        """Initialize the text reconstructor."""
        self.segmenter = pysbd.Segmenter(language="en", clean=False)

    def extract_clean_segments(self, raw_segments: list[dict]) -> list[dict]:
        """Extract clean segments (short duration ones with clean text)."""
        clean_segments = []

        for segment in raw_segments:
            # Filter segments with very short duration (these contain clean text)
            if segment["duration"] < 0.1:  # Less than 0.1 seconds
                clean_segment = {
                    "segment_index": segment["segment_index"],
                    "start_time": segment["start_time"],
                    "end_time": segment["end_time"],
                    "text": self._clean_text(segment["raw_text"]),
                }
                clean_segments.append(clean_segment)

        print(
            f"✅ Extracted {len(clean_segments)} clean segments from {len(raw_segments)} raw segments"
        )
        return clean_segments

    def _clean_text(self, text: str) -> str:
        """Clean text by removing HTML tags and markup."""
        # Remove HTML-like tags: <00:00:00.480><c> you</c>
        text = re.sub(r"<[^>]+>", "", text)

        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def reconstruct_full_text(self, clean_segments: list[dict]) -> str:
        """Reconstruct full text from clean segments."""
        if not clean_segments:
            return ""

        # Sort segments by start time to ensure chronological order
        sorted_segments = sorted(clean_segments, key=lambda x: x["start_time"])

        # Join all text segments
        full_text = " ".join(
            segment["text"] for segment in sorted_segments if segment["text"].strip()
        )

        # Clean up spacing and punctuation
        full_text = self._fix_spacing_and_punctuation(full_text)

        print(f"✅ Reconstructed full text: {len(full_text)} characters")
        return full_text

    def _fix_spacing_and_punctuation(self, text: str) -> str:
        """Fix spacing and punctuation issues common in transcripts."""
        # Fix spacing around punctuation
        text = re.sub(r"\s+([.,!?;:])", r"\1", text)  # Remove space before punctuation
        text = re.sub(r"([.,!?;:])\s*", r"\1 ", text)  # Add space after punctuation

        # Fix multiple spaces
        text = re.sub(r"\s+", " ", text)

        # Fix common transcription issues
        text = re.sub(r"\s+\.", ".", text)  # Fix spaced periods
        text = re.sub(r"\s+,", ",", text)  # Fix spaced commas

        # Ensure proper sentence endings
        text = re.sub(r"([a-z])\s+([A-Z])", r"\1. \2", text)  # Add periods between sentences

        return text.strip()

    def create_timestamped_segments(self, clean_segments: list[dict]) -> list[dict]:
        """Create segments with text and timestamps for reference."""
        timestamped_segments = []

        for segment in clean_segments:
            if segment["text"].strip():
                timestamped_segments.append(
                    {
                        "start_time": segment["start_time"],
                        "end_time": segment["end_time"],
                        "text": segment["text"],
                        "timestamp_readable": self._format_timestamp(segment["start_time"]),
                    }
                )

        return timestamped_segments

    def _format_timestamp(self, seconds: float) -> str:
        """Format timestamp in MM:SS format."""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def segment_into_sentences(self, text: str) -> list[str]:
        """Segment text into sentences using pySBD."""
        if not text.strip():
            return []

        # Use pySBD for sentence boundary detection
        sentences = self.segmenter.segment(text)

        # Clean and filter sentences
        clean_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 5:  # Filter very short fragments
                clean_sentences.append(sentence)

        return clean_sentences

    def reconstruct_with_sentence_boundaries(
        self, clean_segments: list[dict]
    ) -> tuple[str, list[str]]:
        """Reconstruct text and return both full text and sentence list."""
        # Get full text
        full_text = self.reconstruct_full_text(clean_segments)

        # Segment into sentences
        sentences = self.segment_into_sentences(full_text)

        print(f"✅ Segmented into {len(sentences)} sentences")

        return full_text, sentences

    def get_reconstruction_stats(
        self,
        raw_segments: list[dict],
        clean_segments: list[dict],
        full_text: str,
        sentences: list[str],
    ) -> dict:
        """Get statistics about the reconstruction process."""
        return {
            "raw_segments_count": len(raw_segments),
            "clean_segments_count": len(clean_segments),
            "clean_segments_percentage": (len(clean_segments) / len(raw_segments)) * 100,
            "full_text_length": len(full_text),
            "sentences_count": len(sentences),
            "avg_sentence_length": len(full_text) / len(sentences) if sentences else 0,
        }


def main():
    """Test the text reconstructor with sample data."""
    import json

    # Load raw segments
    try:
        with open("raw_segments_mKEq_YaJjPI.json") as f:
            data = json.load(f)

        raw_segments = data["raw_segments"]
        print(f"Loaded {len(raw_segments)} raw segments")

        # Initialize reconstructor
        reconstructor = TextReconstructor()

        # Extract clean segments
        clean_segments = reconstructor.extract_clean_segments(raw_segments)

        # Reconstruct text with sentence boundaries
        full_text, sentences = reconstructor.reconstruct_with_sentence_boundaries(clean_segments)

        # Get stats
        stats = reconstructor.get_reconstruction_stats(
            raw_segments, clean_segments, full_text, sentences
        )

        print("\n=== Reconstruction Statistics ===")
        for key, value in stats.items():
            if isinstance(value, float):
                print(f"{key}: {value:.2f}")
            else:
                print(f"{key}: {value}")

        # Show sample sentences
        print("\n=== Sample Sentences ===")
        for i, sentence in enumerate(sentences[:5]):
            print(f"{i+1}. {sentence}")

        # Save results
        output_data = {
            "metadata": data["metadata"],
            "reconstruction_stats": stats,
            "full_text": full_text,
            "sentences": sentences,
            "clean_segments": clean_segments,
        }

        with open("reconstructed_text.json", "w") as f:
            json.dump(output_data, f, indent=2)

        print("\n✅ Results saved to reconstructed_text.json")

    except FileNotFoundError:
        print("❌ Raw segments file not found. Run raw_transcript_extractor.py first.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
