"""
Auto-enhancement system for YouTube transcripts.

This module automatically applies corrections from the processing_knowledge_base.json,
which contains 174+ mapped transcription errors and channel-specific patterns.
"""

import json
import re
from pathlib import Path

from pydantic import BaseModel


class EnhancementResult(BaseModel):
    """Result of automatic enhancement."""

    original_text: str
    enhanced_text: str
    corrections_applied: int
    corrections_list: list[dict]  # Changed from Dict[str, str] to allow mixed types
    channel_name: str | None = None
    video_id: str | None = None

    class Config:
        arbitrary_types_allowed = True


class AutoEnhancer:
    """Automatically enhance transcripts using the knowledge base."""

    def __init__(self, knowledge_base_path: str = "learning/processing_knowledge_base.json"):
        """Initialize the auto enhancer with knowledge base."""
        self.kb_path = Path(knowledge_base_path)
        self.knowledge_base = self._load_knowledge_base()
        self.corrections = self.knowledge_base.get("transcription_corrections", {})
        self.common_errors = self.corrections.get("common_errors", {})
        self.contextual_corrections = self.corrections.get("contextual_corrections", {})

    def _load_knowledge_base(self) -> dict:
        """Load the processing knowledge base."""
        if not self.kb_path.exists():
            raise FileNotFoundError(f"Knowledge base not found at {self.kb_path}")

        with open(self.kb_path, encoding="utf-8") as f:
            return json.load(f)

    def enhance_transcript(
        self, text: str, channel_name: str | None = None, video_id: str | None = None
    ) -> EnhancementResult:
        """
        Automatically enhance transcript with all corrections.

        Args:
            text: Raw transcript text
            channel_name: Optional channel name for channel-specific patterns
            video_id: Optional video ID for tracking

        Returns:
            EnhancementResult with corrections applied
        """
        original_text = text
        enhanced_text = text
        corrections_list = []

        # Apply common error corrections
        for error, correction in self.common_errors.items():
            if error in enhanced_text:
                # Count occurrences
                count = enhanced_text.count(error)
                enhanced_text = enhanced_text.replace(error, correction)
                corrections_list.append(
                    {
                        "original": error,
                        "corrected": correction,
                        "count": count,
                        "type": "common_error",
                    }
                )

        # Apply contextual corrections
        for context, context_corrections in self.contextual_corrections.items():
            for error, correction in context_corrections.items():
                # Build context-aware pattern
                if context == "followed_by_code":
                    pattern = rf"\b{re.escape(error)}\s+code\b"
                    enhanced_text = re.sub(
                        pattern, f"{correction} Code", enhanced_text, flags=re.IGNORECASE
                    )
                elif context == "followed_by_servers":
                    pattern = rf"\b{re.escape(error)}\s+servers\b"
                    enhanced_text = re.sub(
                        pattern, f"{correction} servers", enhanced_text, flags=re.IGNORECASE
                    )

        # Apply channel-specific patterns if provided
        if channel_name:
            enhanced_text = self._apply_channel_patterns(enhanced_text, channel_name)

        # Calculate corrections made
        corrections_applied = len(corrections_list)

        return EnhancementResult(
            original_text=original_text,
            enhanced_text=enhanced_text,
            corrections_applied=corrections_applied,
            corrections_list=corrections_list,
            channel_name=channel_name,
            video_id=video_id,
        )

    def _apply_channel_patterns(self, text: str, channel_name: str) -> str:
        """Apply channel-specific patterns and corrections."""
        # Normalize channel name for lookup
        channel_key = channel_name.lower().replace(" ", "").replace("-", "")

        # Check for channel patterns in video_patterns
        video_patterns = self.knowledge_base.get("video_patterns", {})

        if channel_key in video_patterns:
            video_patterns[channel_key]

            # Apply any channel-specific transcription patterns
            # (Currently channels don't have specific corrections, but structure is ready)
            pass

        return text

    def enhance_file(self, input_file: str, output_file: str | None = None) -> EnhancementResult:
        """
        Enhance a transcript file.

        Args:
            input_file: Path to raw transcript file
            output_file: Optional output path (defaults to input_file with _enhanced suffix)

        Returns:
            EnhancementResult with statistics
        """
        input_path = Path(input_file)

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        # Read input file
        with open(input_path, encoding="utf-8") as f:
            text = f.read()

        # Extract metadata from filename if possible
        video_id = None
        if "raw_text_for_enhancement_" in input_path.name:
            video_id = input_path.stem.replace("raw_text_for_enhancement_", "")

        # Enhance text
        result = self.enhance_transcript(text, video_id=video_id)

        # Determine output path
        if output_file is None:
            output_file = str(input_path).replace(".txt", "_auto_enhanced.txt")

        # Write enhanced text
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result.enhanced_text)
            f.write("\n\n")
            f.write("=" * 80)
            f.write("\nAUTO-ENHANCEMENT REPORT")
            f.write("\n" + "=" * 80)
            f.write(f"\nVideo ID: {result.video_id or 'Unknown'}")
            f.write(f"\nCorrections Applied: {result.corrections_applied}")
            f.write(f"\nQuality Score: {self._calculate_quality_score(result):.2f}")
            f.write("\n\nTop Corrections:")
            for i, correction in enumerate(result.corrections_list[:10], 1):
                f.write(
                    f"\n{i}. \"{correction['original']}\" → \"{correction['corrected']}\" ({correction['count']} occurrences)"
                )
            f.write("\n" + "=" * 80 + "\n")

        print(f"✅ Enhanced transcript saved to: {output_file}")
        print(f"📊 Corrections applied: {result.corrections_applied}")

        return result

    def _calculate_quality_score(self, result: EnhancementResult) -> float:
        """Calculate quality score based on corrections applied."""
        # Simple quality metric: more corrections = higher initial quality impact
        # Max score of 0.95 for fully corrected transcripts
        if result.corrections_applied == 0:
            return 0.85  # Base quality for clean transcripts
        elif result.corrections_applied < 10:
            return 0.90
        elif result.corrections_applied < 30:
            return 0.92
        else:
            return 0.95  # Extensive corrections suggest thorough processing

    def get_statistics(self) -> dict:
        """Get statistics about the knowledge base."""
        return {
            "total_common_errors": len(self.common_errors),
            "contextual_correction_types": len(self.contextual_corrections),
            "total_channels_tracked": len(self.knowledge_base.get("video_patterns", {})),
            "knowledge_base_version": self.knowledge_base.get("metadata", {}).get(
                "version", "unknown"
            ),
            "last_updated": self.knowledge_base.get("metadata", {}).get("last_updated", "unknown"),
            "total_videos_processed": self.knowledge_base.get("metadata", {}).get(
                "total_videos_processed", 0
            ),
        }


def main():
    """CLI interface for auto-enhancement."""
    import sys

    if len(sys.argv) < 2:
        print("Auto-Enhancement Tool")
        print("\nUsage:")
        print("  python -m src.processing.auto_enhancer <input_file> [output_file]")
        print("\nExample:")
        print("  python -m src.processing.auto_enhancer raw_text_for_enhancement_VIDEO_ID.txt")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        enhancer = AutoEnhancer()

        # Show statistics
        stats = enhancer.get_statistics()
        print("\n📚 Knowledge Base Statistics:")
        print(f"   Version: {stats['knowledge_base_version']}")
        print(f"   Last Updated: {stats['last_updated']}")
        print(f"   Common Errors Mapped: {stats['total_common_errors']}")
        print(f"   Channels Tracked: {stats['total_channels_tracked']}")
        print(f"   Videos Processed: {stats['total_videos_processed']}")
        print()

        # Enhance file
        print(f"🔧 Enhancing: {input_file}")
        result = enhancer.enhance_file(input_file, output_file)

        print("\n✅ Enhancement complete!")
        print(f"📈 Quality Score: {enhancer._calculate_quality_score(result):.2f}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
