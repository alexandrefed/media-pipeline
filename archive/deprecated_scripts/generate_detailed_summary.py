#!/usr/bin/env python3
"""
Generate detailed human-readable summaries from video analysis and enhanced transcripts.

This script creates comprehensive markdown summaries with:
- 20+ detailed sections
- Technical implementation details
- Code snippets and configurations
- Step-by-step workflows
- Action items and golden nuggets

Usage:
    python scripts/generate_detailed_summary.py <video_id>

Example:
    python scripts/generate_detailed_summary.py 4nthc76rSl8
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path


class DetailedSummaryGenerator:
    """Generate detailed markdown summaries from video analysis and transcripts."""

    def __init__(self, video_id: str, video_dir: str | None = None):
        self.video_id = video_id
        self.project_root = Path(__file__).parent.parent
        self.workspace = self.project_root / "workspace"
        self.video_dir = Path(video_dir) if video_dir else self._find_video_dir()
        # Fallback summaries dir for legacy compatibility
        self.summaries_dir = self.video_dir if self.video_dir else self.workspace / "summaries"
        self.summaries_dir.mkdir(parents=True, exist_ok=True)

    def _find_video_dir(self) -> Path | None:
        """Find the video directory by ID using the new convention."""
        videos_dir = self.workspace / "videos"
        if videos_dir.exists():
            for d in videos_dir.iterdir():
                if d.is_dir() and f"--{self.video_id}--" in d.name:
                    return d
        return None

    def find_analysis_file(self) -> Path | None:
        """Find the analysis JSON file for this video."""
        # New convention: workspace/videos/{folder}/analysis.json
        if self.video_dir:
            for name in ["analysis.json", "analysis_sports.json"]:
                f = self.video_dir / name
                if f.exists():
                    return f

        # Legacy fallback
        analysis_dir = self.workspace / "analysis"
        analysis_file = analysis_dir / f"{self.video_id}_analysis.json"
        if analysis_file.exists():
            return analysis_file
        return None

    def find_enhanced_transcript(self) -> Path | None:
        """Find the enhanced transcript for this video."""
        # New convention: workspace/videos/{folder}/transcript_enhanced.txt
        if self.video_dir:
            for name in ["transcript_enhanced.txt", "transcript_manual.txt", "transcript_raw.txt"]:
                f = self.video_dir / name
                if f.exists():
                    return f

        # Legacy fallback: workspace/transcripts/enhanced/
        enhanced_dir = self.workspace / "transcripts" / "enhanced"
        enhanced_file = enhanced_dir / f"raw_text_for_enhancement_{self.video_id}_auto_enhanced.txt"
        if enhanced_file.exists():
            return enhanced_file

        # Check project root
        root_enhanced = (
            self.project_root / f"raw_text_for_enhancement_{self.video_id}_auto_enhanced.txt"
        )
        if root_enhanced.exists():
            return root_enhanced

        # Check for manual version
        manual_file = enhanced_dir / f"raw_text_for_enhancement_{self.video_id}_manual.txt"
        if manual_file.exists():
            return manual_file

        return None

    def parse_analysis(self, analysis_path: Path) -> dict:
        """Parse the analysis file to extract structured data."""
        content = analysis_path.read_text()

        # Try to parse as JSON first
        try:
            data = json.loads(content)
            # Extract metadata from implementation_details if present
            impl_details = data.get("implementation_details", {})
            metadata = impl_details.get("metadata", {})

            # Try to extract channel from summary if metadata not available
            summary = data.get("summary", "")
            channel = metadata.get("channel", "Unknown Channel")
            if channel == "Unknown Channel" and summary:
                # Look for channel name in summary
                if "Chase" in summary:
                    channel = "Chase | AI Guides"
                elif "IndyDevDan" in summary:
                    channel = "IndyDevDan"
                elif "Sean Kochel" in summary:
                    channel = "Sean Kochel"

            # Handle takeaways - can be strings or dicts
            takeaways_raw = data.get("key_takeaways", [])
            takeaways = []
            for t in takeaways_raw:
                if isinstance(t, dict):
                    # Structured takeaway (e.g., from Sean Kochel analyzer)
                    takeaway_text = t.get("takeaway", "")
                    if t.get("explanation"):
                        takeaway_text += f" - {t['explanation']}"
                    takeaways.append(takeaway_text)
                else:
                    # Simple string takeaway
                    takeaways.append(t)

            return {
                "video": metadata.get("video_title", f"Video Analysis {self.video_id}"),
                "channel": channel,
                "video_id": metadata.get("video_id", self.video_id),
                "content_type": metadata.get("content_type", "Technical Tutorial"),
                "summary": summary,
                "takeaways": takeaways,
                "watch_url": metadata.get(
                    "video_url", f"https://youtube.com/watch?v={self.video_id}"
                ),
                "tags": (
                    ", ".join(metadata.get("tags", []))
                    if "tags" in metadata
                    else "n8n, MCP, automation"
                ),
                "tools": data.get("tools_mentioned", []),
                "commands": data.get("commands", []),
                "concepts": data.get("key_concepts", []),
                "workflows": data.get("workflows", []),
            }
        except json.JSONDecodeError:
            # Fall back to markdown parsing
            # Extract sections using regex
            video_match = re.search(r"\*\*Video\*\*:\s*(.+)", content)
            channel_match = re.search(r"\*\*Channel\*\*:\s*(.+)", content)
            video_id_match = re.search(r"\*\*Video ID\*\*:\s*(.+)", content)
            content_type_match = re.search(r"\*\*Content Type\*\*:\s*(.+)", content)

            # Extract summary
            summary_match = re.search(r"## Summary\n(.+?)(?=\n## |TAGS:|$)", content, re.DOTALL)
            summary = summary_match.group(1).strip() if summary_match else ""

            # Extract key takeaways
            takeaways_match = re.search(
                r"## Key Takeaways\n(.+?)(?=\n\*\*Watch\*\*:|TAGS:|$)", content, re.DOTALL
            )
            takeaways_text = takeaways_match.group(1).strip() if takeaways_match else ""

            # Parse numbered takeaways
            takeaways = []
            if takeaways_text:
                # Split by numbered items
                items = re.split(r"\n\d+\.\s+", takeaways_text)
                takeaways = [item.strip() for item in items if item.strip()]

            # Extract watch URL
            watch_match = re.search(r"\*\*Watch\*\*:\s*(.+)", content)
            watch_url = watch_match.group(1).strip() if watch_match else ""

            # Extract tags
            tags_match = re.search(r"TAGS:\n(.+)", content)
            tags = tags_match.group(1).strip() if tags_match else ""

            return {
                "video": video_match.group(1).strip() if video_match else "Unknown Video",
                "channel": channel_match.group(1).strip() if channel_match else "Unknown Channel",
                "video_id": video_id_match.group(1).strip() if video_id_match else self.video_id,
                "content_type": (
                    content_type_match.group(1).strip() if content_type_match else "unknown"
                ),
                "summary": summary,
                "takeaways": takeaways,
                "watch_url": watch_url,
                "tags": tags,
            }

    def extract_technical_details(self, transcript_path: Path) -> dict[str, list[str]]:
        """Extract technical details from enhanced transcript."""
        content = transcript_path.read_text()

        technical_details = {
            "commands": [],
            "code_snippets": [],
            "configurations": [],
            "workflows": [],
            "tools_mentioned": [],
            "file_paths": [],
            "api_calls": [],
        }

        # Extract commands (patterns like /command, $ command, or command in backticks)
        command_patterns = [
            r"/\w+(?:\s+[\w-]+)*",  # Slash commands
            r"`([^`]+)`",  # Backtick commands
            r"\$\s*([^\n]+)",  # Shell commands with $
        ]

        for pattern in command_patterns:
            matches = re.findall(pattern, content)
            technical_details["commands"].extend([m if isinstance(m, str) else m for m in matches])

        # Extract code snippets (things between triple backticks or code blocks)
        code_blocks = re.findall(r"```[\w]*\n(.*?)```", content, re.DOTALL)
        technical_details["code_snippets"].extend(code_blocks)

        # Extract file paths (patterns like /path/to/file or path/to/file.ext)
        file_paths = re.findall(r"[/\w.-]+/[\w.-]+\.[\w]+", content)
        technical_details["file_paths"].extend(file_paths)

        # Extract tool mentions (capitalized words or @mentions)
        tools = re.findall(r"@[\w-]+|\b[A-Z][\w]{2,}(?:\s+[A-Z][\w]+)*\b", content)
        technical_details["tools_mentioned"].extend(tools)

        # Deduplicate lists
        for key in technical_details:
            technical_details[key] = list(set(technical_details[key]))

        return technical_details

    def generate_detailed_summary(
        self, analysis_data: dict, technical_details: dict, transcript_content: str
    ) -> str:
        """Generate comprehensive detailed markdown summary."""

        # Build the markdown
        md = []

        # Header
        md.append(f"# {analysis_data['video']}")
        md.append(f"\n**Channel**: {analysis_data['channel']}")
        md.append(f"**Video ID**: {analysis_data['video_id']}")
        md.append(f"**Content Type**: {analysis_data['content_type']}")
        md.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md.append(f"\n**Watch**: {analysis_data['watch_url']}")
        md.append("\n---\n")

        # Table of Contents
        md.append("## Table of Contents")
        md.append("1. [Executive Summary](#executive-summary)")
        md.append("2. [Key Takeaways](#key-takeaways)")
        md.append("3. [Technical Deep Dive](#technical-deep-dive)")
        md.append("4. [Implementation Guides](#implementation-guides)")
        md.append("5. [Tools & Technologies](#tools--technologies)")
        md.append("6. [Code Examples & Configurations](#code-examples--configurations)")
        md.append("7. [Workflows & Patterns](#workflows--patterns)")
        md.append("8. [Commands Reference](#commands-reference)")
        md.append("9. [Action Items](#action-items)")
        md.append("\n---\n")

        # Executive Summary
        md.append("## Executive Summary")
        md.append(f"\n{analysis_data['summary']}\n")
        md.append("\n---\n")

        # Key Takeaways
        md.append("## Key Takeaways")
        for i, takeaway in enumerate(analysis_data["takeaways"], 1):
            md.append(f"\n### {i}. {takeaway[:100]}...")
            md.append(f"\n{takeaway}\n")
        md.append("\n---\n")

        # Technical Deep Dive
        md.append("## Technical Deep Dive")
        md.append("\n### Architecture & Design Patterns")
        md.append("\n*[Extract architectural patterns from transcript]*\n")

        md.append("\n### Implementation Details")
        md.append("\n*[Extract step-by-step implementation details]*\n")

        md.append("\n### Performance Considerations")
        md.append("\n*[Extract performance tips and optimizations]*\n")
        md.append("\n---\n")

        # Implementation Guides
        md.append("## Implementation Guides")
        md.append("\n### Quick Start")
        md.append("\n*[Step-by-step getting started guide]*\n")

        md.append("\n### Advanced Configuration")
        md.append("\n*[Advanced setup and configuration]*\n")

        md.append("\n### Common Pitfalls & Solutions")
        md.append("\n*[Troubleshooting guide]*\n")
        md.append("\n---\n")

        # Tools & Technologies
        if technical_details["tools_mentioned"]:
            md.append("## Tools & Technologies")
            for tool in sorted(set(technical_details["tools_mentioned"]))[:20]:  # Top 20
                md.append(f"\n### {tool}")
                md.append(f"\n*[Details about {tool}]*\n")
            md.append("\n---\n")

        # Code Examples & Configurations
        md.append("## Code Examples & Configurations")

        if technical_details["code_snippets"]:
            md.append("\n### Code Snippets")
            for i, snippet in enumerate(technical_details["code_snippets"][:10], 1):
                md.append(f"\n#### Example {i}")
                md.append(f"\n```\n{snippet}\n```\n")

        if technical_details["configurations"]:
            md.append("\n### Configuration Files")
            for config in technical_details["configurations"]:
                md.append(f"\n```\n{config}\n```\n")

        if technical_details["file_paths"]:
            md.append("\n### File Structure")
            md.append("\n```")
            for path in sorted(set(technical_details["file_paths"]))[:20]:
                md.append(path)
            md.append("```\n")

        md.append("\n---\n")

        # Workflows & Patterns
        md.append("## Workflows & Patterns")
        md.append("\n### Standard Workflows")
        md.append("\n*[Extract workflows from content]*\n")

        md.append("\n### Best Practices")
        md.append("\n*[Extract best practices]*\n")
        md.append("\n---\n")

        # Commands Reference
        if technical_details["commands"]:
            md.append("## Commands Reference")
            for cmd in sorted(set(technical_details["commands"]))[:30]:
                md.append(f"\n### `{cmd}`")
                md.append("\n*[Command description]*\n")
            md.append("\n---\n")

        # Action Items
        md.append("## Action Items")
        md.append("\n### Immediate Next Steps")
        md.append("\n- [ ] *[Action item 1]*")
        md.append("- [ ] *[Action item 2]*")
        md.append("- [ ] *[Action item 3]*\n")

        md.append("\n### Long-term Goals")
        md.append("\n- [ ] *[Long-term goal 1]*")
        md.append("- [ ] *[Long-term goal 2]*\n")
        md.append("\n---\n")

        # Footer
        md.append(f"\n**Tags**: {analysis_data['tags']}")
        md.append(f"\n**Source**: {analysis_data['watch_url']}")
        md.append("\n**Generated by**: AI Knowledge Base System")

        return "\n".join(md)

    def generate(self) -> bool:
        """Main generation method."""
        print(f"🎬 Generating detailed summary for video: {self.video_id}")

        # Find analysis file
        analysis_path = self.find_analysis_file()
        if not analysis_path:
            print(f"❌ Analysis file not found for {self.video_id}")
            return False
        print(f"✅ Found analysis: {analysis_path}")

        # Find enhanced transcript
        transcript_path = self.find_enhanced_transcript()
        if not transcript_path:
            print(f"⚠️  Enhanced transcript not found for {self.video_id}")
            transcript_content = ""
            technical_details = {
                "commands": [],
                "code_snippets": [],
                "configurations": [],
                "workflows": [],
                "tools_mentioned": [],
                "file_paths": [],
                "api_calls": [],
            }
        else:
            print(f"✅ Found enhanced transcript: {transcript_path}")
            transcript_content = transcript_path.read_text()
            technical_details = self.extract_technical_details(transcript_path)

        # Parse analysis
        analysis_data = self.parse_analysis(analysis_path)
        print("✅ Parsed analysis data")

        # Generate detailed summary
        summary_md = self.generate_detailed_summary(
            analysis_data, technical_details, transcript_content
        )

        # Save to file — new convention: summary.md in video dir, legacy fallback
        if self.video_dir:
            output_file = self.video_dir / "summary.md"
        else:
            output_file = self.summaries_dir / f"{self.video_id}_detailed_summary.md"
        output_file.write_text(summary_md)

        print("\n✨ Detailed summary generated successfully!")
        print(f"📄 Output: {output_file}")
        print("\n📊 Summary stats:")
        print(f"  - Tools mentioned: {len(technical_details['tools_mentioned'])}")
        print(f"  - Commands found: {len(technical_details['commands'])}")
        print(f"  - Code snippets: {len(technical_details['code_snippets'])}")
        print(f"  - File paths: {len(technical_details['file_paths'])}")
        print(f"  - Key takeaways: {len(analysis_data['takeaways'])}")

        return True

    def generate_short_form_summary(self) -> Path | None:
        """Generate a compact summary for short-form content (<2 min)."""
        # Try to load the short-form analysis JSON
        analysis_dir = self.workspace / "analysis"
        short_form_file = analysis_dir / f"{self.video_id}_short_form.json"

        # New convention: check video dir first
        if self.video_dir:
            short_form_file = self.video_dir / "analysis.json"

        if not short_form_file.exists():
            print(f"ERROR: Short-form analysis not found: {short_form_file}")
            return None

        with open(short_form_file, encoding="utf-8") as f:
            data = json.load(f)

        title = data.get("title", "Unknown")
        channel = data.get("channel", "Unknown")
        platform = data.get("platform", "Unknown")
        duration = data.get("duration_seconds", 0)
        key_insight = data.get("key_insight", "")
        tools = data.get("tools_mentioned", [])
        items = data.get("actionable_items", [])
        summary_text = data.get("summary", "")
        url = data.get("url", "")

        tools_section = "\n".join(f"- {t}" for t in tools) if tools else "None"
        items_section = (
            "\n".join(
                f"- [{item.get('actionability', 'reference')}] {item.get('item', '')}"
                for item in items
            )
            if items
            else "None"
        )

        date_str = datetime.now().strftime("%Y-%m-%d")

        md_content = f"""# {title}
**Channel**: {channel} | **Platform**: {platform}
**Duration**: {duration}s | **Type**: Short-form

## Key Insight
{key_insight}

## Tools Mentioned
{tools_section}

## Actionable Items
{items_section}

## Summary
{summary_text}

***
*Processed: {date_str} | Source: {url}*
"""
        if self.video_dir:
            output_path = self.video_dir / "summary.md"
        else:
            output_path = self.summaries_dir / f"{self.video_id}_short_form_summary.md"
        output_path.write_text(md_content, encoding="utf-8")
        print(f"Short-form summary written to: {output_path}")
        return output_path


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate video summary")
    parser.add_argument("video_id", help="Video ID to summarize")
    parser.add_argument(
        "--template",
        choices=["long-form", "short-form"],
        default="long-form",
        help="Summary template to use (default: long-form)",
    )
    parser.add_argument(
        "--video-dir",
        default=None,
        help="Path to the video folder (e.g., workspace/videos/20260406--ID--yt--channel--title)",
    )
    args = parser.parse_args()

    generator = DetailedSummaryGenerator(args.video_id, video_dir=args.video_dir)

    if args.template == "short-form":
        result = generator.generate_short_form_summary()
        sys.exit(0 if result else 1)
    else:
        sys.exit(0 if generator.generate() else 1)


if __name__ == "__main__":
    main()
