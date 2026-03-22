"""
AI Knowledge Base - Transcript Processor using Claude Code

This module provides Claude Code-powered transcript processing to:
- Remove filler words and unnecessary content
- Classify content types (tutorial, explanation, fluff)
- Summarize low-value segments while preserving technical content
- Extract key information and tools mentioned
"""

import asyncio
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any

from ..pipeline.youtube_extractor import TranscriptSegment

logger = logging.getLogger(__name__)


class SegmentType(str, Enum):
    """Types of content segments."""

    TECHNICAL_INSTRUCTION = "technical_instruction"
    CODE_EXAMPLE = "code_example"
    TOOL_DEMO = "tool_demo"
    EXPLANATION = "explanation"
    INTRODUCTION = "introduction"
    CONCLUSION = "conclusion"
    PROMOTION = "promotion"
    FLUFF = "fluff"
    TRANSITION = "transition"


class ProcessingAction(str, Enum):
    """Actions to take on segments."""

    PRESERVE = "preserve"
    SUMMARIZE = "summarize"
    REMOVE = "remove"
    CLEAN = "clean"


@dataclass
class ProcessedSegment:
    """A processed transcript segment."""

    original_text: str
    processed_text: str
    start_time: float
    end_time: float
    segment_type: SegmentType
    action: ProcessingAction
    confidence: float
    extracted_tools: list[str]
    extracted_prices: list[str]
    key_points: list[str]
    is_technical: bool
    information_density: float  # 0-1 score


class TranscriptProcessor:
    """Claude Code-powered transcript processor."""

    # Common filler words and phrases to remove
    FILLER_WORDS = {
        "um",
        "uh",
        "umm",
        "uhh",
        "ah",
        "er",
        "erm",
        "you know",
        "like like",
        "basically basically",
        "i mean i mean",
        "so so",
        "and and",
    }

    # YouTube-specific phrases to remove or summarize
    YOUTUBE_FLUFF = {
        "like and subscribe",
        "hit the bell",
        "leave a comment",
        "check the description",
        "links below",
        "sponsor message",
        "before we get started",
        "real quick before",
    }

    # Technical indicators
    TECHNICAL_INDICATORS = {
        "configure",
        "setup",
        "install",
        "api",
        "webhook",
        "endpoint",
        "function",
        "method",
        "class",
        "variable",
        "step 1",
        "step 2",
        "first",
        "then",
        "finally",
        "code",
        "script",
        "command",
        "terminal",
        "console",
    }

    def __init__(self):
        """Initialize the transcript processor."""
        self.processing_stats = {
            "segments_processed": 0,
            "segments_removed": 0,
            "segments_summarized": 0,
            "segments_preserved": 0,
            "total_reduction": 0,
        }

    async def process_transcript(
        self, segments: list[TranscriptSegment], batch_size: int = 10
    ) -> list[ProcessedSegment]:
        """
        Process transcript segments using Claude Code intelligence.

        This method will be called from Claude Code to analyze and process
        transcript segments intelligently.
        """
        processed_segments = []

        # Process in batches for efficiency
        for i in range(0, len(segments), batch_size):
            batch = segments[i : i + batch_size]

            # Claude Code will analyze this batch
            batch_results = await self._process_batch(batch)
            processed_segments.extend(batch_results)

            # Log progress
            logger.info(f"Processed {len(processed_segments)}/{len(segments)} segments")

        # Post-processing: merge related segments, ensure continuity
        processed_segments = self._post_process_segments(processed_segments)

        return processed_segments

    async def _process_batch(self, segments: list[TranscriptSegment]) -> list[ProcessedSegment]:
        """
        Process a batch of segments.

        Note: This uses rule-based processing. For better results,
        use Claude Code directly to analyze transcripts.
        """
        # Use the fallback method which has the original logic
        return await self._fallback_process_batch(segments)

    async def _fallback_process_batch(
        self, segments: list[TranscriptSegment]
    ) -> list[ProcessedSegment]:
        """
        Fallback rule-based processing if Claude Code analysis fails.
        This is the original implementation kept as backup.
        """
        results = []

        for segment in segments:
            # Clean basic filler words first
            cleaned_text = self._remove_filler_words(segment.text)

            # Analyze segment type and content
            segment_type = self._classify_segment(cleaned_text)
            action = self._determine_action(segment_type, cleaned_text)

            # Process based on action
            if action == ProcessingAction.REMOVE:
                self.processing_stats["segments_removed"] += 1
                continue  # Skip this segment entirely

            elif action == ProcessingAction.PRESERVE:
                processed_text = cleaned_text
                self.processing_stats["segments_preserved"] += 1

            elif action == ProcessingAction.SUMMARIZE:
                processed_text = self._summarize_segment(cleaned_text, segment_type)
                self.processing_stats["segments_summarized"] += 1

            else:  # CLEAN
                processed_text = cleaned_text

            # Extract additional information
            tools = self._extract_tools(cleaned_text)
            prices = self._extract_prices(cleaned_text)
            key_points = self._extract_key_points(cleaned_text, segment_type)

            # Calculate information density
            info_density = self._calculate_information_density(
                cleaned_text, segment_type, len(tools), len(key_points)
            )

            # Create processed segment
            processed_segment = ProcessedSegment(
                original_text=segment.text,
                processed_text=processed_text,
                start_time=segment.start_time,
                end_time=segment.end_time,
                segment_type=segment_type,
                action=action,
                confidence=0.7,  # Lower confidence for fallback
                extracted_tools=tools,
                extracted_prices=prices,
                key_points=key_points,
                is_technical=segment_type
                in [
                    SegmentType.TECHNICAL_INSTRUCTION,
                    SegmentType.CODE_EXAMPLE,
                    SegmentType.TOOL_DEMO,
                ],
                information_density=info_density,
            )

            results.append(processed_segment)
            self.processing_stats["segments_processed"] += 1

        return results

    def _remove_filler_words(self, text: str) -> str:
        """Remove common filler words and clean up text."""
        cleaned = text.lower()

        # Remove filler phrases
        for filler in self.FILLER_WORDS:
            cleaned = cleaned.replace(f" {filler} ", " ")
            cleaned = cleaned.replace(f"{filler} ", "")
            cleaned = cleaned.replace(f" {filler}", "")

        # Remove multiple spaces
        while "  " in cleaned:
            cleaned = cleaned.replace("  ", " ")

        # Restore original case for non-filler words
        words_lower = cleaned.split()
        words_original = text.split()

        result = []
        j = 0
        for _i, word in enumerate(words_original):
            if j < len(words_lower) and word.lower().strip(".,!?") == words_lower[j].strip(".,!?"):
                result.append(word)
                j += 1

        return " ".join(result).strip()

    def _classify_segment(self, text: str) -> SegmentType:
        """Classify the segment type based on content."""
        text_lower = text.lower()

        # Check for technical instructions
        technical_count = sum(
            1 for indicator in self.TECHNICAL_INDICATORS if indicator in text_lower
        )
        if technical_count >= 3:
            if any(word in text_lower for word in ["code", "function", "class", "variable"]):
                return SegmentType.CODE_EXAMPLE
            return SegmentType.TECHNICAL_INSTRUCTION

        # Check for tool demo
        if any(phrase in text_lower for phrase in ["let me show", "demonstration", "here's how"]):
            return SegmentType.TOOL_DEMO

        # Check for promotion/fluff
        if any(phrase in text_lower for phrase in self.YOUTUBE_FLUFF):
            return SegmentType.PROMOTION

        # Check for intro/conclusion
        if any(phrase in text_lower for phrase in ["welcome to", "in this video", "today we'll"]):
            return SegmentType.INTRODUCTION
        if any(
            phrase in text_lower for phrase in ["thanks for watching", "see you next", "that's all"]
        ):
            return SegmentType.CONCLUSION

        # Check for transitions
        if len(text.split()) < 10 and any(
            word in text_lower for word in ["now", "next", "so", "okay"]
        ):
            return SegmentType.TRANSITION

        # Default to explanation
        return SegmentType.EXPLANATION

    def _determine_action(self, segment_type: SegmentType, text: str) -> ProcessingAction:
        """Determine what action to take on a segment."""
        # Always preserve technical content
        if segment_type in [
            SegmentType.TECHNICAL_INSTRUCTION,
            SegmentType.CODE_EXAMPLE,
            SegmentType.TOOL_DEMO,
        ]:
            return ProcessingAction.PRESERVE

        # Remove pure fluff and most transitions
        if segment_type in [SegmentType.PROMOTION, SegmentType.FLUFF]:
            return ProcessingAction.REMOVE

        if segment_type == SegmentType.TRANSITION and len(text.split()) < 5:
            return ProcessingAction.REMOVE

        # Summarize introductions and conclusions
        if segment_type in [SegmentType.INTRODUCTION, SegmentType.CONCLUSION]:
            return ProcessingAction.SUMMARIZE

        # Clean explanations
        return ProcessingAction.CLEAN

    def _summarize_segment(self, text: str, segment_type: SegmentType) -> str:
        """
        Summarize a segment based on its type.

        Claude Code will provide intelligent summaries that preserve
        the essential information while removing fluff.
        """
        if segment_type == SegmentType.INTRODUCTION:
            # Extract the main topic
            if "video" in text.lower() and "about" in text.lower():
                return f"Introduction: {self._extract_main_topic(text)}"
            return "Introduction to the tutorial"

        elif segment_type == SegmentType.CONCLUSION:
            # Extract any important reminders or next steps
            if "next" in text.lower() or "follow" in text.lower():
                return f"Conclusion: {self._extract_next_steps(text)}"
            return "End of tutorial"

        elif segment_type == SegmentType.EXPLANATION:
            # Keep the core explanation, remove redundancy
            key_points = self._extract_key_points(text, segment_type)
            if key_points:
                return f"Explanation: {'; '.join(key_points[:2])}"
            return text[:100] + "..." if len(text) > 100 else text

        return text

    def _extract_tools(self, text: str) -> list[str]:
        """Extract mentioned tools from text."""
        tools = []

        # Common AI tools to look for
        tool_patterns = [
            "n8n",
            "make.com",
            "zapier",
            "cursor",
            "claude",
            "v0",
            "chatgpt",
            "github copilot",
            "webhook",
            "api",
            "automation",
        ]

        text_lower = text.lower()
        for tool in tool_patterns:
            if tool in text_lower:
                tools.append(tool)

        return list(set(tools))

    def _extract_prices(self, text: str) -> list[str]:
        """Extract pricing information from text."""
        prices = []

        # Look for price patterns
        import re

        # Dollar amounts
        dollar_pattern = r"\$\d+(?:\.\d{2})?(?:/(?:month|year|user))?"
        prices.extend(re.findall(dollar_pattern, text))

        # Free tier mentions
        if "free" in text.lower() and any(
            word in text.lower() for word in ["tier", "plan", "version"]
        ):
            prices.append("free tier")

        return prices

    def _extract_key_points(self, text: str, segment_type: SegmentType) -> list[str]:
        """Extract key points from a segment."""
        key_points = []

        # Split into sentences
        sentences = text.split(". ")

        for sentence in sentences:
            # Look for key indicators
            if any(
                indicator in sentence.lower()
                for indicator in [
                    "important",
                    "key",
                    "remember",
                    "note that",
                    "make sure",
                    "don't forget",
                    "tip:",
                    "pro tip",
                ]
            ):
                key_points.append(sentence.strip())

            # For technical segments, extract action items
            if segment_type == SegmentType.TECHNICAL_INSTRUCTION:
                if any(
                    action in sentence.lower()
                    for action in [
                        "click",
                        "select",
                        "enter",
                        "type",
                        "configure",
                        "set",
                        "enable",
                        "create",
                        "add",
                    ]
                ):
                    key_points.append(sentence.strip())

        return key_points[:3]  # Limit to top 3 points

    def _calculate_information_density(
        self, text: str, segment_type: SegmentType, tool_count: int, key_point_count: int
    ) -> float:
        """Calculate information density score (0-1)."""
        score = 0.5  # Base score

        # Adjust based on segment type
        type_scores = {
            SegmentType.TECHNICAL_INSTRUCTION: 0.9,
            SegmentType.CODE_EXAMPLE: 0.95,
            SegmentType.TOOL_DEMO: 0.85,
            SegmentType.EXPLANATION: 0.6,
            SegmentType.INTRODUCTION: 0.3,
            SegmentType.CONCLUSION: 0.3,
            SegmentType.PROMOTION: 0.1,
            SegmentType.FLUFF: 0.05,
            SegmentType.TRANSITION: 0.2,
        }

        score = type_scores.get(segment_type, 0.5)

        # Boost for tools and key points
        score += min(0.1 * tool_count, 0.2)
        score += min(0.05 * key_point_count, 0.15)

        # Penalize for low content
        word_count = len(text.split())
        if word_count < 10:
            score *= 0.5

        return min(1.0, max(0.0, score))

    def _extract_main_topic(self, text: str) -> str:
        """Extract the main topic from an introduction."""
        # Simple extraction - Claude Code would do this more intelligently
        if "about" in text.lower():
            parts = text.lower().split("about")
            if len(parts) > 1:
                topic = parts[1].split(".")[0].strip()
                return topic

        if "going to" in text.lower():
            parts = text.lower().split("going to")
            if len(parts) > 1:
                topic = parts[1].split(".")[0].strip()
                return topic

        return "the topic of this video"

    def _extract_next_steps(self, text: str) -> str:
        """Extract next steps from a conclusion."""
        if "next" in text.lower():
            parts = text.lower().split("next")
            if len(parts) > 1:
                return parts[1].split(".")[0].strip()

        return "check resources and practice"

    def _post_process_segments(self, segments: list[ProcessedSegment]) -> list[ProcessedSegment]:
        """Post-process segments to ensure continuity and merge related content."""
        if not segments:
            return segments

        # Merge consecutive segments of the same type with same action
        merged = []
        current = segments[0]

        for next_segment in segments[1:]:
            # Check if we should merge
            if (
                current.segment_type == next_segment.segment_type
                and current.action == next_segment.action
                and next_segment.start_time - current.end_time < 2.0
            ):  # Within 2 seconds

                # Merge segments
                current = ProcessedSegment(
                    original_text=current.original_text + " " + next_segment.original_text,
                    processed_text=current.processed_text + " " + next_segment.processed_text,
                    start_time=current.start_time,
                    end_time=next_segment.end_time,
                    segment_type=current.segment_type,
                    action=current.action,
                    confidence=min(current.confidence, next_segment.confidence),
                    extracted_tools=list(
                        set(current.extracted_tools + next_segment.extracted_tools)
                    ),
                    extracted_prices=list(
                        set(current.extracted_prices + next_segment.extracted_prices)
                    ),
                    key_points=current.key_points + next_segment.key_points,
                    is_technical=current.is_technical or next_segment.is_technical,
                    information_density=max(
                        current.information_density, next_segment.information_density
                    ),
                )
            else:
                merged.append(current)
                current = next_segment

        merged.append(current)

        return merged

    def get_processing_summary(self) -> dict[str, Any]:
        """Get a summary of processing statistics."""
        total = self.processing_stats["segments_processed"]
        if total == 0:
            return self.processing_stats

        return {
            **self.processing_stats,
            "removal_rate": self.processing_stats["segments_removed"] / total,
            "summarization_rate": self.processing_stats["segments_summarized"] / total,
            "preservation_rate": self.processing_stats["segments_preserved"] / total,
        }


# Example usage for Claude Code
async def main():
    """Example of how Claude Code would use this processor."""
    from src.youtube_extractor import YouTubeExtractor

    # Extract transcript
    extractor = YouTubeExtractor()
    metadata, transcript = extractor.extract_video_data("https://youtube.com/watch?v=example")

    # Process with Claude Code intelligence
    processor = TranscriptProcessor()
    processed_segments = await processor.process_transcript(transcript)

    # Show results
    print(f"Original segments: {len(transcript)}")
    print(f"Processed segments: {len(processed_segments)}")
    print(f"Processing summary: {processor.get_processing_summary()}")

    # Show some examples
    for segment in processed_segments[:5]:
        print(f"\nTime: {segment.start_time:.1f}s - {segment.end_time:.1f}s")
        print(f"Type: {segment.segment_type}, Action: {segment.action}")
        print(f"Original: {segment.original_text[:100]}...")
        print(f"Processed: {segment.processed_text[:100]}...")
        print(f"Info density: {segment.information_density:.2f}")


if __name__ == "__main__":
    asyncio.run(main())
