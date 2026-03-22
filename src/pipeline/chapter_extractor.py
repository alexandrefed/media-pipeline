"""
Chapter Extractor for YouTube Videos
Extracts chapter information from video descriptions and timestamps
"""

import re
from dataclasses import dataclass


@dataclass
class VideoChapter:
    """Represents a video chapter with timing and title."""

    index: int
    start_time: float
    end_time: float | None
    title: str
    timestamp_text: str


class ChapterExtractor:
    """Extracts chapter information from video descriptions."""

    def __init__(self):
        """Initialize the chapter extractor."""
        # Common patterns for chapter timestamps
        self.timestamp_patterns = [
            r"(\d{1,2}):(\d{2})\s+(.+)",  # MM:SS Title
            r"(\d{1,2}):(\d{2}):(\d{2})\s+(.+)",  # HH:MM:SS Title
            r"(\d{1,2}):(\d{2})\s*-\s*(.+)",  # MM:SS - Title
            r"(\d{1,2}):(\d{2}):(\d{2})\s*-\s*(.+)",  # HH:MM:SS - Title
        ]

    def extract_chapters_from_description(self, description: str) -> list[VideoChapter]:
        """Extract chapters from video description."""
        chapters = []
        lines = description.split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Try each timestamp pattern
            for pattern in self.timestamp_patterns:
                match = re.match(pattern, line)
                if match:
                    chapter = self._create_chapter_from_match(match, line, len(chapters))
                    if chapter:
                        chapters.append(chapter)
                    break

        # Sort chapters by start time
        chapters.sort(key=lambda x: x.start_time)

        # Set end times for each chapter
        for i in range(len(chapters)):
            if i < len(chapters) - 1:
                chapters[i].end_time = chapters[i + 1].start_time
            else:
                chapters[i].end_time = None  # Last chapter goes to end of video

        print(f"✅ Extracted {len(chapters)} chapters from description")
        return chapters

    def _create_chapter_from_match(
        self, match: re.Match, line: str, index: int
    ) -> VideoChapter | None:
        """Create chapter from regex match."""
        groups = match.groups()

        try:
            if len(groups) == 3:  # MM:SS Title
                minutes, seconds, title = groups
                start_time = int(minutes) * 60 + int(seconds)
            elif len(groups) == 4:  # HH:MM:SS Title
                hours, minutes, seconds, title = groups
                start_time = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
            else:
                return None

            # Clean up title
            title = title.strip()
            title = re.sub(r"^-\s*", "", title)  # Remove leading dash
            title = re.sub(r"\s*-\s*$", "", title)  # Remove trailing dash

            return VideoChapter(
                index=index,
                start_time=start_time,
                end_time=None,  # Will be set later
                title=title,
                timestamp_text=line,
            )

        except (ValueError, IndexError):
            return None

    def extract_chapters_from_segments(
        self, segments: list[dict], video_duration: float
    ) -> list[VideoChapter]:
        """Extract chapters from segment analysis if description doesn't have them."""
        # This is a fallback method that creates chapters based on content analysis
        # For now, we'll create simple time-based chapters

        if not segments:
            return []

        chapter_duration = 300  # 5 minutes per chapter
        chapters = []

        current_time = 0
        chapter_index = 0

        while current_time < video_duration:
            end_time = min(current_time + chapter_duration, video_duration)

            # Find a meaningful title from segments in this time range
            title = self._find_chapter_title_from_segments(segments, current_time, end_time)

            chapter = VideoChapter(
                index=chapter_index,
                start_time=current_time,
                end_time=end_time if end_time < video_duration else None,
                title=title,
                timestamp_text=f"{self._format_timestamp(current_time)} {title}",
            )

            chapters.append(chapter)
            current_time = end_time
            chapter_index += 1

        print(f"✅ Generated {len(chapters)} chapters from segment analysis")
        return chapters

    def _find_chapter_title_from_segments(
        self, segments: list[dict], start_time: float, end_time: float
    ) -> str:
        """Find a meaningful title from segments in the time range."""
        relevant_segments = [seg for seg in segments if start_time <= seg["start_time"] <= end_time]

        if not relevant_segments:
            return f"Chapter {int(start_time // 60) + 1}"

        # Use the first segment's text as title (simplified approach)
        first_segment = relevant_segments[0]
        title = first_segment["text"][:50]  # First 50 characters

        # Clean up title
        title = title.strip()
        if title.endswith("."):
            title = title[:-1]

        return title if title else f"Chapter {int(start_time // 60) + 1}"

    def _format_timestamp(self, seconds: float) -> str:
        """Format timestamp in MM:SS format."""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def split_segments_by_chapters(
        self, segments: list[dict], chapters: list[VideoChapter]
    ) -> dict[int, list[dict]]:
        """Split segments into chapters."""
        chapter_segments = {}

        for chapter in chapters:
            chapter_segments[chapter.index] = []

        for segment in segments:
            segment_time = segment["start_time"]

            # Find which chapter this segment belongs to
            for chapter in chapters:
                if chapter.start_time <= segment_time:
                    if chapter.end_time is None or segment_time < chapter.end_time:
                        chapter_segments[chapter.index].append(segment)
                        break

        print(f"✅ Split {len(segments)} segments into {len(chapters)} chapters")
        return chapter_segments

    def get_chapter_stats(
        self, chapters: list[VideoChapter], chapter_segments: dict[int, list[dict]]
    ) -> dict:
        """Get statistics about chapters."""
        stats = {"total_chapters": len(chapters), "chapters": []}

        for chapter in chapters:
            segments = chapter_segments.get(chapter.index, [])

            chapter_stats = {
                "index": chapter.index,
                "title": chapter.title,
                "start_time": chapter.start_time,
                "end_time": chapter.end_time,
                "duration": (chapter.end_time - chapter.start_time) if chapter.end_time else None,
                "segments_count": len(segments),
                "total_text_length": sum(len(seg["text"]) for seg in segments),
            }

            stats["chapters"].append(chapter_stats)

        return stats


def main():
    """Test the chapter extractor with sample data."""
    import json

    try:
        # Load raw segments data
        with open("raw_segments_mKEq_YaJjPI.json") as f:
            data = json.load(f)

        metadata = data["metadata"]
        raw_segments = data["raw_segments"]

        print(f"Video: {metadata['title']}")
        print(f"Duration: {metadata['duration_seconds']} seconds")
        print(f"Description length: {len(metadata['description'])} characters")

        # Initialize extractor
        extractor = ChapterExtractor()

        # Extract chapters from description
        chapters = extractor.extract_chapters_from_description(metadata["description"])

        if not chapters:
            print("No chapters found in description, generating from segments...")
            # Load clean segments
            from .text_reconstructor import TextReconstructor

            reconstructor = TextReconstructor()
            clean_segments = reconstructor.extract_clean_segments(raw_segments)
            chapters = extractor.extract_chapters_from_segments(
                clean_segments, metadata["duration_seconds"]
            )

        # Show chapter information
        print("\n=== Extracted Chapters ===")
        for chapter in chapters:
            duration = (chapter.end_time - chapter.start_time) if chapter.end_time else "to end"
            print(
                f"{chapter.index + 1}. [{extractor._format_timestamp(chapter.start_time)}] {chapter.title}"
            )
            print(f"   Duration: {duration}")
            print(f"   Original: {chapter.timestamp_text}")
            print()

        # Split segments by chapters (using clean segments if available)
        try:
            from .text_reconstructor import TextReconstructor

            reconstructor = TextReconstructor()
            clean_segments = reconstructor.extract_clean_segments(raw_segments)
            chapter_segments = extractor.split_segments_by_chapters(clean_segments, chapters)
        except Exception:
            chapter_segments = extractor.split_segments_by_chapters(raw_segments, chapters)

        # Get chapter stats
        stats = extractor.get_chapter_stats(chapters, chapter_segments)

        print("=== Chapter Statistics ===")
        for chapter_stat in stats["chapters"]:
            print(f"Chapter {chapter_stat['index'] + 1}: {chapter_stat['title']}")
            print(f"  Segments: {chapter_stat['segments_count']}")
            print(f"  Text length: {chapter_stat['total_text_length']} characters")
            print()

        # Save results
        output_data = {
            "metadata": metadata,
            "chapters": [
                {
                    "index": ch.index,
                    "start_time": ch.start_time,
                    "end_time": ch.end_time,
                    "title": ch.title,
                    "timestamp_text": ch.timestamp_text,
                }
                for ch in chapters
            ],
            "chapter_segments": chapter_segments,
            "stats": stats,
        }

        with open("extracted_chapters.json", "w") as f:
            json.dump(output_data, f, indent=2)

        print("✅ Results saved to extracted_chapters.json")

    except FileNotFoundError:
        print("❌ Raw segments file not found. Run raw_transcript_extractor.py first.")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
