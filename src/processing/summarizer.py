"""
Summarization and technical extraction for YouTube transcripts.

This module generates summaries and extracts technical information from enhanced transcripts
for storage in MCP KB Memory.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Set
from pydantic import BaseModel


class TechnicalInfo(BaseModel):
    """Extracted technical information."""
    tools_mentioned: List[str] = []
    commands: List[str] = []
    key_concepts: List[str] = []
    workflows: List[str] = []
    code_examples: List[str] = []
    timestamps: List[Dict[str, str]] = []  # {"time": "10:30", "topic": "..."}


class VideoSummary(BaseModel):
    """Complete video summary with technical details."""
    video_id: str
    channel_name: Optional[str] = None
    title: Optional[str] = None
    summary: str  # 200-300 word summary
    technical_info: TechnicalInfo
    content_type: str  # e.g., "technical_tutorial", "workflow_demo", etc.
    key_takeaways: List[str] = []
    tags: List[str] = []
    duration_seconds: Optional[int] = None


class TranscriptSummarizer:
    """Generate summaries and extract technical information."""

    def __init__(self, knowledge_base_path: str = "learning/processing_knowledge_base.json"):
        """Initialize summarizer with knowledge base."""
        self.kb_path = Path(knowledge_base_path)
        self.knowledge_base = self._load_knowledge_base()
        self.known_tools = self._extract_known_tools()
        self.video_patterns = self.knowledge_base.get("video_patterns", {})

    def _load_knowledge_base(self) -> Dict:
        """Load the processing knowledge base."""
        if self.kb_path.exists():
            with open(self.kb_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _extract_known_tools(self) -> Set[str]:
        """Extract all known tool names from knowledge base."""
        tools = set()

        # From technical terms
        tech_terms = self.knowledge_base.get("transcription_corrections", {}).get("technical_terms", {})
        if "AI_tools" in tech_terms:
            tools.update(tech_terms["AI_tools"])
        if "development_tools" in tech_terms:
            tools.update(tech_terms["development_tools"])

        # From common errors (the corrected values)
        common_errors = self.knowledge_base.get("transcription_corrections", {}).get("common_errors", {})
        tools.update(common_errors.values())

        return tools

    def summarize(self, text: str, video_id: str, channel_name: Optional[str] = None,
                 title: Optional[str] = None) -> VideoSummary:
        """
        Generate summary and extract technical information.

        Args:
            text: Enhanced transcript text
            video_id: YouTube video ID
            channel_name: Channel name
            title: Video title

        Returns:
            VideoSummary with all extracted information
        """
        # Extract technical information
        technical_info = self._extract_technical_info(text)

        # Detect content type
        content_type = self._detect_content_type(text, channel_name)

        # Generate summary
        summary = self._generate_summary(text, title, content_type)

        # Extract key takeaways
        key_takeaways = self._extract_key_takeaways(text, content_type)

        # Generate tags
        tags = self._generate_tags(channel_name, content_type, technical_info)

        return VideoSummary(
            video_id=video_id,
            channel_name=channel_name,
            title=title,
            summary=summary,
            technical_info=technical_info,
            content_type=content_type,
            key_takeaways=key_takeaways,
            tags=tags
        )

    def _extract_technical_info(self, text: str) -> TechnicalInfo:
        """Extract technical information from text."""
        # Extract tools mentioned
        tools_mentioned = []
        for tool in self.known_tools:
            if tool.lower() in text.lower():
                tools_mentioned.append(tool)

        # Extract commands (looking for command patterns)
        commands = []
        command_patterns = [
            r'`([^`]+)`',  # Inline code
            r'```([^```]+)```',  # Code blocks
            r'(?:run|execute|type|use)\s+([a-z]+\s+[a-z\-]+)',  # Command-like phrases
            r'(?:slash|/|command:)\s*([a-z\-]+)',  # Slash commands
            r'\$\s+([a-z][a-z\s\-\.]+)',  # Shell commands
        ]

        for pattern in command_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            commands.extend([m.strip() for m in matches if len(m.strip()) > 2])

        # Remove duplicates while preserving order
        commands = list(dict.fromkeys(commands))[:20]  # Limit to 20 commands

        # Extract key concepts (capitalized phrases, technical terms)
        key_concepts = []
        concept_patterns = [
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b',  # Title Case Phrases
            r'\b(AI|API|MCP|CLI|SDK|JSON|YAML|REST|GPT|LLM)\b',  # Common acronyms
            r'\b([a-z]+(?:-[a-z]+)+)\b',  # hyphenated-terms
        ]

        for pattern in concept_patterns:
            matches = re.findall(pattern, text)
            key_concepts.extend(matches)

        key_concepts = list(dict.fromkeys(key_concepts))[:30]  # Limit to 30 concepts

        # Extract workflows (step-based patterns)
        workflows = []
        workflow_patterns = [
            r'(?:Step\s+\d+|First|Second|Third|Finally)[:\s]+([^.]+)',
            r'(?:workflow|process|pipeline)[:\s]+([^.]+)',
        ]

        for pattern in workflow_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            workflows.extend([m.strip() for m in matches if len(m.strip()) > 10])

        workflows = list(dict.fromkeys(workflows))[:10]  # Limit to 10 workflows

        # Extract timestamps (if present)
        timestamps = []
        timestamp_pattern = r'\[?(\d{1,2}:\d{2}(?::\d{2})?)\]?\s*[:-]?\s*([^\n]+)'
        matches = re.findall(timestamp_pattern, text)
        for time, topic in matches[:15]:  # Limit to 15 timestamps
            timestamps.append({"time": time, "topic": topic.strip()[:100]})

        return TechnicalInfo(
            tools_mentioned=tools_mentioned[:15],  # Limit to 15 tools
            commands=commands,
            key_concepts=key_concepts,
            workflows=workflows,
            timestamps=timestamps
        )

    def _detect_content_type(self, text: str, channel_name: Optional[str]) -> str:
        """Detect content type from text and channel patterns."""
        if channel_name:
            # Normalize channel name
            channel_key = channel_name.lower().replace(" ", "").replace("-", "")

            # Check video patterns
            if channel_key in self.video_patterns:
                pattern_data = self.video_patterns[channel_key]
                if "content_style" in pattern_data:
                    return pattern_data["content_style"]

        # Fallback to text analysis
        text_lower = text.lower()

        if "step 1" in text_lower or "step 2" in text_lower:
            return "step_by_step_tutorial"
        elif "workflow" in text_lower or "automation" in text_lower:
            return "workflow_tutorial"
        elif "command" in text_lower and ("slash" in text_lower or "cli" in text_lower):
            return "command_tutorial"
        elif "architecture" in text_lower or "system design" in text_lower:
            return "technical_architecture"
        elif "business" in text_lower and "strategy" in text_lower:
            return "business_strategy"
        else:
            return "technical_tutorial"

    def _generate_summary(self, text: str, title: Optional[str], content_type: str) -> str:
        """Generate a 200-300 word summary."""
        # Extract first paragraph or first 500 characters as base
        lines = text.strip().split('\n')
        intro_lines = []

        for line in lines:
            if line.strip() and not line.startswith('='):
                intro_lines.append(line.strip())
                if len(' '.join(intro_lines)) > 300:
                    break

        summary_base = ' '.join(intro_lines[:10])  # First 10 lines max

        # Clean up summary
        summary = summary_base.replace('  ', ' ').strip()

        # Truncate to approximately 300 words
        words = summary.split()
        if len(words) > 300:
            summary = ' '.join(words[:300]) + "..."

        # Add title context if available
        if title and title not in summary[:100]:
            summary = f"{title}. {summary}"

        return summary

    def _extract_key_takeaways(self, text: str, content_type: str) -> List[str]:
        """Extract 3-5 key takeaways."""
        takeaways = []

        # Look for explicit takeaway sections
        takeaway_patterns = [
            r'(?:Key takeaway|Key learning|Important point|Remember)[:\s]+([^.]+\.)',
            r'(?:\d+\.|•|-)\s+([A-Z][^.]+\.)',  # Bullet points or numbered lists
        ]

        for pattern in takeaway_patterns:
            matches = re.findall(pattern, text)
            takeaways.extend([m.strip() for m in matches if len(m.strip()) > 20])

        # Remove duplicates
        takeaways = list(dict.fromkeys(takeaways))[:5]

        # If no takeaways found, extract from text structure
        if not takeaways:
            sentences = re.split(r'[.!?]+', text)
            for sentence in sentences:
                if any(word in sentence.lower() for word in ['should', 'must', 'important', 'key', 'essential', 'critical']):
                    if len(sentence.strip()) > 30:
                        takeaways.append(sentence.strip())
                        if len(takeaways) >= 5:
                            break

        return takeaways[:5]

    def _generate_tags(self, channel_name: Optional[str], content_type: str,
                      technical_info: TechnicalInfo) -> List[str]:
        """Generate relevant tags."""
        tags = []

        # Add channel as tag
        if channel_name:
            tags.append(channel_name.lower().replace(" ", "-"))

        # Add content type
        tags.append(content_type)

        # Add tool tags
        for tool in technical_info.tools_mentioned[:5]:  # Top 5 tools
            tags.append(tool.lower().replace(" ", "-").replace(".", ""))

        # Add concept tags
        for concept in technical_info.key_concepts[:3]:  # Top 3 concepts
            if len(concept) > 2:
                tags.append(concept.lower().replace(" ", "-"))

        return list(dict.fromkeys(tags))[:10]  # Limit to 10 unique tags

    def summarize_file(self, input_file: str, output_file: Optional[str] = None) -> VideoSummary:
        """
        Summarize a transcript file.

        Args:
            input_file: Path to enhanced transcript file
            output_file: Optional output path for JSON summary

        Returns:
            VideoSummary object
        """
        input_path = Path(input_file)

        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Extract metadata from filename
        video_id = "unknown"
        if "_enhancement_" in input_path.name:
            video_id = input_path.stem.split("_enhancement_")[1].split("_")[0]
        elif "nGhsgdQplHw" in input_path.name:
            video_id = "nGhsgdQplHw"

        # Extract title and channel from text if present
        title = None
        channel_name = None
        if text.startswith("Video:"):
            lines = text.split('\n')
            for line in lines[:5]:
                if line.startswith("Video:"):
                    title = line.replace("Video:", "").strip()
                elif line.startswith("Channel:"):
                    channel_name = line.replace("Channel:", "").strip()

        # Generate summary
        summary = self.summarize(text, video_id, channel_name, title)

        # Output to JSON if requested
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(summary.model_dump(), f, indent=2)
            print(f"✅ Summary saved to: {output_file}")

        return summary


def main():
    """CLI interface for summarization."""
    import sys

    if len(sys.argv) < 2:
        print("Transcript Summarization Tool")
        print("\nUsage:")
        print("  python -m src.processing.summarizer <input_file> [output_file]")
        print("\nExample:")
        print("  python -m src.processing.summarizer raw_text_for_enhancement_VIDEO_ID_auto_enhanced.txt summary.json")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.txt', '_summary.json')

    try:
        summarizer = TranscriptSummarizer()

        print(f"📊 Summarizing: {input_file}")
        summary = summarizer.summarize_file(input_file, output_file)

        print("\n✅ Summarization complete!")
        print(f"\n📹 Video: {summary.title or summary.video_id}")
        print(f"📺 Channel: {summary.channel_name or 'Unknown'}")
        print(f"📋 Content Type: {summary.content_type}")
        print(f"🔧 Tools Mentioned: {len(summary.technical_info.tools_mentioned)}")
        print(f"💻 Commands Extracted: {len(summary.technical_info.commands)}")
        print(f"🏷️  Tags: {', '.join(summary.tags[:5])}")
        print(f"\n📝 Summary Preview:")
        print(f"   {summary.summary[:200]}...")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
