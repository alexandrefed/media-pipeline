#!/usr/bin/env python3
"""
Enhanced MCP KB Memory storage with multi-memory entity-based approach.

Based on 2025 RAG best practices:
- Entity-based chunking for precise retrieval
- Multi-granularity storage (overview → implementation)
- Preserve complete logical units (code, workflows)
- Rich metadata with entity and content-type tags

This script creates 5-7 specialized memories per video instead of 1:
1. Overview (summary + takeaways)
2. Tools (all tools with context)
3. Commands (all commands with syntax)
4. Workflows (step-by-step processes)
5. Code Examples (complete snippets)
6. Setup Guide (installation, configuration)
7. Troubleshooting (common issues, solutions)
"""

import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import unified memory client for direct API storage
try:
    from src.storage.unified_memory_client import health_check, store_memory, store_note

    API_AVAILABLE = True
except ImportError:
    print("⚠️  Warning: Unified memory client not available. API storage disabled.")
    API_AVAILABLE = False



class EnhancedKBStorage:
    """Enhanced storage with entity-based multi-memory approach."""

    def __init__(self, analysis_file: str):
        self.analysis_file = Path(analysis_file)
        self.video_id = self._extract_video_id()
        self.analysis_data = self._load_analysis()
        self.memories_created = []

    def _extract_video_id(self) -> str:
        """Extract video ID from filename."""
        filename = self.analysis_file.stem
        # Handle various naming patterns
        if "_analysis" in filename:
            video_id = filename.replace("_analysis", "")
            # Remove common prefixes
            for prefix in ["raw_text_for_enhancement_", "video_", ""]:
                if video_id.startswith(prefix):
                    video_id = video_id[len(prefix) :]
            # Remove _auto_enhanced suffix if present
            if "_auto_enhanced" in video_id:
                video_id = video_id.replace("_auto_enhanced", "")
            return video_id
        return "unknown"

    def _load_analysis(self) -> dict:
        """Load and parse analysis JSON."""
        with open(self.analysis_file, encoding="utf-8") as f:
            return json.load(f)

    def _extract_metadata(self) -> dict:
        """Extract video metadata."""
        # Try new format first (video_metadata at root)
        metadata = self.analysis_data.get("video_metadata", {})

        # Fallback to old format (implementation_details.metadata)
        if not metadata:
            impl_details = self.analysis_data.get("implementation_details", {})
            metadata = impl_details.get("metadata", {})

        return {
            "video_title": metadata.get(
                "video_title", metadata.get("title", f"Video {self.video_id}")
            ),
            "channel": metadata.get("channel", "Unknown Channel"),
            "video_id": metadata.get("video_id", self.video_id),
            "content_type": metadata.get("content_type", "Technical Tutorial"),
            "video_url": metadata.get("video_url", f"https://youtube.com/watch?v={self.video_id}"),
        }

    def _extract_entity_tags(self) -> list[str]:
        """Extract entity tags from tools and concepts."""
        entity_tags = []

        # Extract tool entities
        tools = self.analysis_data.get("tools_mentioned", [])
        # Handle both list of strings and list of dicts
        for tool in tools:
            if isinstance(tool, dict):
                tool_name = tool.get("name", "")
            else:
                tool_name = str(tool)

            # Normalize tool names for tagging
            tool_tag = tool_name.lower().replace(" ", "-").replace(".", "")
            # Create entity tag
            if tool_tag:
                entity_tags.append(f"tool-{tool_tag}")

        # Extract feature entities from key concepts
        concepts = self.analysis_data.get("key_concepts", [])
        for concept in concepts:
            # Handle both string concepts and dict concepts
            if isinstance(concept, dict):
                concept_text = concept.get("concept", "")
            else:
                concept_text = str(concept)

            # Extract key features (e.g., "Callback System" → "feature-callbacks")
            concept_lower = concept_text.lower()
            if "agent" in concept_lower:
                entity_tags.append("feature-agents")
            if "mcp" in concept_lower or "model context protocol" in concept_lower:
                entity_tags.append("feature-mcp")
            if "callback" in concept_lower:
                entity_tags.append("feature-callbacks")
            if "filter" in concept_lower:
                entity_tags.append("feature-filtering")
            if "dashboard" in concept_lower:
                entity_tags.append("feature-dashboards")
            if "visualization" in concept_lower or "chart" in concept_lower:
                entity_tags.append("feature-visualization")
            if "planning" in concept_lower:
                entity_tags.append("feature-planning-mode")
            if "context engineering" in concept_lower:
                entity_tags.append("feature-context-engineering")
            if "command" in concept_lower and "slash" in concept_lower:
                entity_tags.append("feature-slash-commands")

        return list(set(entity_tags))  # Deduplicate

    def _create_base_tags(self, content_type: str) -> list[str]:
        """Create base tags for all memories."""
        metadata = self._extract_metadata()
        entity_tags = self._extract_entity_tags()

        # Safely format channel name
        channel = metadata.get("channel", "Unknown Channel")
        if isinstance(channel, str):
            channel_tag = channel.lower().replace(" ", "-")
        else:
            channel_tag = "unknown-channel"

        base_tags = [
            "source:claude-main",
            "project:youtube-kb",
            "type:video-knowledge",
            "area:vecia",
            f"video:{self.video_id}",
            f"channel:{channel_tag}",
            f"content-type:{content_type}",
        ]

        # Add entity tags
        base_tags.extend(entity_tags)

        return base_tags

    def create_overview_memory(self) -> dict:
        """Memory 1: Overview (summary + takeaways)."""
        metadata = self._extract_metadata()
        summary = self.analysis_data.get("summary", "")
        takeaways = self.analysis_data.get("key_takeaways", [])

        content_parts = [
            f"**Video**: {metadata['video_title']}",
            f"**Channel**: {metadata['channel']}",
            f"**Video ID**: {metadata['video_id']}",
            f"**Content Type**: {metadata['content_type']}",
            "",
            "## Summary",
            summary,
            "",
        ]

        if takeaways:
            content_parts.append("## Key Takeaways")
            for i, takeaway in enumerate(takeaways, 1):
                # Handle both string and dict format
                if isinstance(takeaway, dict):
                    takeaway_text = takeaway.get("takeaway", "")
                    actionability = takeaway.get("actionability", "")
                    if actionability:
                        takeaway_text += f" [{actionability}]"
                else:
                    takeaway_text = str(takeaway)
                content_parts.append(f"{i}. {takeaway_text}")
            content_parts.append("")

        content_parts.append(f"**Watch**: {metadata['video_url']}")

        # Build tags with actionability metadata
        tags = self._create_base_tags("overview")
        has_actionable = any(
            t.get("actionability") == "actionable" for t in takeaways if isinstance(t, dict)
        )
        if has_actionable:
            tags.append("has-actionable:true")

        return {
            "content": "\n".join(content_parts),
            "tags": tags,
            "type": "video-overview",
        }

    def create_tools_memory(self) -> dict | None:
        """Memory 2: Tools mentioned with context."""
        tools = self.analysis_data.get("tools_mentioned", self.analysis_data.get("tools", []))
        if not tools:
            return None

        metadata = self._extract_metadata()
        content_parts = [
            f"**Video**: {metadata['video_title']} - Tools & Technologies",
            f"**Video ID**: {metadata['video_id']}",
            "",
            "## Tools & Technologies Used",
            "",
        ]

        for tool in tools:
            # Handle both string and dict format
            if isinstance(tool, dict):
                tool_name = tool.get("name", "")
                tool_desc = tool.get("description", "")
                tool_category = tool.get("category", "")

                content_parts.append(f"### {tool_name}")
                if tool_category:
                    content_parts.append(f"**Category**: {tool_category}")
                if tool_desc:
                    content_parts.append(f"\n{tool_desc}\n")

                # Add use cases if present
                use_cases = tool.get("use_cases", [])
                if use_cases:
                    content_parts.append("**Use Cases:**")
                    for uc in use_cases:
                        content_parts.append(f"- {uc}")
                content_parts.append("")
            else:
                # String format - try to find context from summary
                content_parts.append(f"### {tool}")
                summary = self.analysis_data.get("summary", "").lower()
                tool_lower = str(tool).lower()
                if tool_lower in summary:
                    sentences = self.analysis_data.get("summary", "").split(". ")
                    for sent in sentences:
                        if tool_lower in sent.lower():
                            content_parts.append(f"{sent.strip()}.")
                            break
                content_parts.append("")

        content_parts.append(f"**Watch**: {metadata['video_url']}")

        return {
            "content": "\n".join(content_parts),
            "tags": self._create_base_tags("tools-reference"),
            "type": "technical-tools",
        }

    def create_commands_memory(self) -> dict | None:
        """Memory 3: Commands with syntax."""
        commands = self.analysis_data.get("commands", [])
        if not commands:
            return None

        metadata = self._extract_metadata()
        content_parts = [
            f"**Video**: {metadata['video_title']} - Commands Reference",
            f"**Video ID**: {metadata['video_id']}",
            "",
            "## Commands & Syntax",
            "",
        ]

        for cmd in commands:
            # Handle both string and dict format
            if isinstance(cmd, dict):
                cmd_name = cmd.get("command", "")
                cmd_desc = cmd.get("description", "")
                cmd_syntax = cmd.get("syntax", "")

                content_parts.append(f"### {cmd_name}")
                if cmd_desc:
                    content_parts.append(f"{cmd_desc}\n")
                if cmd_syntax:
                    content_parts.append("**Syntax**:")
                    content_parts.append("```")
                    content_parts.append(cmd_syntax)
                    content_parts.append("```")
                content_parts.append("")
            else:
                # String format
                content_parts.append("```")
                content_parts.append(str(cmd))
                content_parts.append("```")
                content_parts.append("")

        content_parts.append(f"**Watch**: {metadata['video_url']}")

        return {
            "content": "\n".join(content_parts),
            "tags": self._create_base_tags("command-reference"),
            "type": "technical-commands",
        }

    def create_workflows_memory(self) -> dict | None:
        """Memory 4: Workflows and step-by-step processes."""
        workflows = self.analysis_data.get("workflows", [])
        if not workflows:
            return None

        metadata = self._extract_metadata()
        content_parts = [
            f"**Video**: {metadata['video_title']} - Workflows & Processes",
            f"**Video ID**: {metadata['video_id']}",
            "",
            "## Workflows & Step-by-Step Guides",
            "",
        ]

        for i, workflow in enumerate(workflows, 1):
            # Handle both string and dict format
            if isinstance(workflow, dict):
                workflow_name = workflow.get("workflow_name", f"Workflow {i}")
                content_parts.append(f"### {workflow_name}")

                steps = workflow.get("steps", [])
                if steps:
                    for step in steps:
                        if isinstance(step, dict):
                            step_num = step.get("step", "")
                            action = step.get("action", "")
                            content_parts.append(f"{step_num}. {action}")
                        else:
                            content_parts.append(f"- {step}")
                content_parts.append("")
            else:
                # String format
                content_parts.append(f"### Workflow {i}")
                content_parts.append(str(workflow))
                content_parts.append("")

        content_parts.append(f"**Watch**: {metadata['video_url']}")

        return {
            "content": "\n".join(content_parts),
            "tags": self._create_base_tags("workflows"),
            "type": "workflows",
        }

    def create_code_memory(self) -> dict | None:
        """Memory 5: Code examples and snippets."""
        # Try root level first
        code_snippets = self.analysis_data.get("code_snippets", {})

        # Fallback to implementation_details
        if not code_snippets:
            impl_details = self.analysis_data.get("implementation_details", {})
            code_snippets = impl_details.get("code_snippets", [])

        # Handle dict with named snippets or list format
        if isinstance(code_snippets, dict):
            snippets_list = list(code_snippets.values())
        else:
            snippets_list = code_snippets

        if not snippets_list:
            return None

        metadata = self._extract_metadata()
        content_parts = [
            f"**Video**: {metadata['video_title']} - Code Examples",
            f"**Video ID**: {metadata['video_id']}",
            "",
            "## Code Examples & Snippets",
            "",
        ]

        for i, snippet_data in enumerate(snippets_list, 1):
            if isinstance(snippet_data, dict):
                purpose = snippet_data.get(
                    "purpose", snippet_data.get("description", f"Example {i}")
                )
                code = snippet_data.get("code", "")
                language = snippet_data.get("language", "python")

                content_parts.append(f"### {purpose}")
                content_parts.append(f"```{language}")
                content_parts.append(code)
                content_parts.append("```")
                content_parts.append("")
            else:
                # Plain string snippet
                content_parts.append(f"### Example {i}")
                content_parts.append("```")
                content_parts.append(str(snippet_data))
                content_parts.append("```")
                content_parts.append("")

        content_parts.append(f"**Watch**: {metadata['video_url']}")

        return {
            "content": "\n".join(content_parts),
            "tags": self._create_base_tags("code-examples"),
            "type": "code-examples",
        }

    def create_setup_memory(self) -> dict | None:
        """Memory 6: Setup and configuration guide."""
        # Try root level first
        setup_steps = self.analysis_data.get("setup_steps", [])

        # Fallback to implementation_details
        if not setup_steps:
            impl_details = self.analysis_data.get("implementation_details", {})
            setup_steps = impl_details.get("setup_steps", [])
            configuration = impl_details.get("configuration", {})
        else:
            configuration = {}

        if not setup_steps and not configuration:
            return None

        metadata = self._extract_metadata()
        content_parts = [
            f"**Video**: {metadata['video_title']} - Setup Guide",
            f"**Video ID**: {metadata['video_id']}",
            "",
            "## Setup & Configuration",
            "",
        ]

        if setup_steps:
            # Handle dict format (with categories like initial_installation, project_initialization)
            if isinstance(setup_steps, dict):
                for category, steps in setup_steps.items():
                    content_parts.append(f"### {category.replace('_', ' ').title()}")
                    if isinstance(steps, list):
                        for step in steps:
                            content_parts.append(f"- {step}")
                    content_parts.append("")
            else:
                # List format
                content_parts.append("### Setup Steps")
                for step in setup_steps:
                    content_parts.append(f"- {step}")
                content_parts.append("")

        if configuration:
            content_parts.append("### Configuration")
            content_parts.append("```json")
            content_parts.append(json.dumps(configuration, indent=2))
            content_parts.append("```")
            content_parts.append("")

        content_parts.append(f"**Watch**: {metadata['video_url']}")

        return {
            "content": "\n".join(content_parts),
            "tags": self._create_base_tags("setup-guide"),
            "type": "setup-guide",
        }

    def create_troubleshooting_memory(self) -> dict | None:
        """Memory 7: Troubleshooting and common issues."""
        # Try root level first
        troubleshooting = self.analysis_data.get("troubleshooting", {})

        # Fallback to implementation_details
        if not troubleshooting:
            impl_details = self.analysis_data.get("implementation_details", {})
            troubleshooting = impl_details.get("troubleshooting", [])

        if not troubleshooting:
            return None

        metadata = self._extract_metadata()
        content_parts = [
            f"**Video**: {metadata['video_title']} - Troubleshooting",
            f"**Video ID**: {metadata['video_id']}",
            "",
            "## Troubleshooting & Common Issues",
            "",
        ]

        # Handle dict format (with issue categories)
        if isinstance(troubleshooting, dict):
            for issue_name, issue_data in troubleshooting.items():
                if isinstance(issue_data, dict):
                    content_parts.append(f"### {issue_name.replace('_', ' ').title()}")
                    symptom = issue_data.get("symptom", "")
                    solutions = issue_data.get("solutions", [])
                    if symptom:
                        content_parts.append(f"**Symptom**: {symptom}")
                    if solutions:
                        content_parts.append("**Solutions**:")
                        for sol in solutions:
                            content_parts.append(f"- {sol}")
                    content_parts.append("")
        else:
            # List format
            for issue in troubleshooting:
                content_parts.append(f"- {issue}")

        content_parts.append("")
        content_parts.append(f"**Watch**: {metadata['video_url']}")

        return {
            "content": "\n".join(content_parts),
            "tags": self._create_base_tags("troubleshooting"),
            "type": "troubleshooting",
        }

    def create_takeaway_memories(self) -> list[dict]:
        """Create individual memories for actionable takeaways with spaced-repetition tags."""
        takeaways = self.analysis_data.get("key_takeaways", [])
        memories = []
        for takeaway in takeaways:
            if not isinstance(takeaway, dict):
                continue
            actionability = takeaway.get("actionability", "")
            if not actionability:
                continue
            takeaway_text = takeaway.get("takeaway", "")
            if not takeaway_text:
                continue

            tags = self._create_base_tags("takeaway")
            tags.append(f"takeaway-type:{actionability}")
            if actionability == "actionable":
                tags.append("spaced-repetition:pending")

            metadata = self._extract_metadata()
            content = (
                f"**Takeaway**: {takeaway_text}\n"
                f"**Type**: {actionability}\n"
                f"**Video**: {metadata['video_title']}\n"
                f"**Watch**: {metadata['video_url']}"
            )
            memories.append(
                {
                    "content": content,
                    "tags": tags,
                    "type": f"takeaway-{actionability}",
                }
            )
        return memories

    def generate_all_memories(self) -> list[dict]:
        """Generate all memory objects."""
        memories = []

        # Memory 1: Overview (always created)
        memories.append(self.create_overview_memory())

        # Memory 2: Tools (if available)
        tools_mem = self.create_tools_memory()
        if tools_mem:
            memories.append(tools_mem)

        # Memory 3: Commands (if available)
        commands_mem = self.create_commands_memory()
        if commands_mem:
            memories.append(commands_mem)

        # Memory 4: Workflows (if available)
        workflows_mem = self.create_workflows_memory()
        if workflows_mem:
            memories.append(workflows_mem)

        # Memory 5: Code (if available)
        code_mem = self.create_code_memory()
        if code_mem:
            memories.append(code_mem)

        # Memory 6: Setup (if available)
        setup_mem = self.create_setup_memory()
        if setup_mem:
            memories.append(setup_mem)

        # Memory 7: Troubleshooting (if available)
        troubleshooting_mem = self.create_troubleshooting_memory()
        if troubleshooting_mem:
            memories.append(troubleshooting_mem)

        # Memory 8+: Individual takeaway memories with actionability tags
        takeaway_mems = self.create_takeaway_memories()
        memories.extend(takeaway_mems)

        return memories

    def print_memories_for_manual_storage(self, memories: list[dict]) -> None:
        """Print memories in a format for manual MCP KB storage."""
        print("\n" + "=" * 80)
        print("ENHANCED UNIFIED MEMORY STORAGE - MULTI-MEMORY APPROACH")
        print("=" * 80)
        print(f"\nVideo ID: {self.video_id}")
        print(f"Total Memories: {len(memories)}")
        print("\n" + "=" * 80)

        for i, memory in enumerate(memories, 1):
            print(f"\n📦 MEMORY {i} - {memory['type'].upper()}")
            print("-" * 80)
            print("\n📋 Content:")
            print(
                memory["content"][:500] + "..."
                if len(memory["content"]) > 500
                else memory["content"]
            )
            print(
                f"\n🏷️  Tags: {', '.join(memory['tags'][:5])}{'...' if len(memory['tags']) > 5 else ''}"
            )
            print(f"📊 Type: {memory['type']}")
            print(f"📏 Size: {len(memory['content'])} characters")

        print("\n" + "=" * 80)
        print("\n💡 To store these memories, for each MEMORY above call:")
        print("   mcp__unified-memory__memory_store(")
        print("     content=<content above>,")
        print("     tags=<tags list above>,")
        print("     namespace='youtube-knowledge-base',")
        print("     metadata={'type': <type above>}")
        print("   )")
        print("\n" + "=" * 80)


def _build_note_content(storage: EnhancedKBStorage, memories: list) -> str:
    """Build a single note from overview + key sections (max ~2000 chars)."""
    metadata = storage._extract_metadata()
    parts = [
        f"# {metadata['video_title']}",
        f"**Channel**: {metadata['channel']}",
        f"**Video ID**: {metadata['video_id']}",
        "",
    ]

    # Add overview summary
    summary = storage.analysis_data.get("summary", "")
    if summary:
        parts.append("## Summary")
        parts.append(summary)
        parts.append("")

    # Add key takeaways
    takeaways = storage.analysis_data.get("key_takeaways", [])
    if takeaways:
        parts.append("## Key Takeaways")
        for i, t in enumerate(takeaways, 1):
            text = t.get("takeaway", str(t)) if isinstance(t, dict) else str(t)
            parts.append(f"{i}. {text}")
        parts.append("")

    # Add tools list (compact)
    tools = storage.analysis_data.get("tools_mentioned", [])
    if tools:
        parts.append("## Tools")
        for tool in tools[:10]:
            name = tool.get("name", str(tool)) if isinstance(tool, dict) else str(tool)
            parts.append(f"- {name}")
        parts.append("")

    parts.append(f"**Watch**: {metadata['video_url']}")
    return "\n".join(parts)


def _build_memory_content(memories: list) -> str:
    """Combine all memory sections into one detailed memory (max ~5000 chars)."""
    parts = []
    for mem in memories:
        parts.append(mem["content"])
        parts.append("")
    return "\n".join(parts)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Enhanced Unified Memory Storage Script (v2)")
        print("\nUsage:")
        print("  python scripts/store_in_mcp_kb.py <analysis_json_file> [--dry-run]")
        print("\nOptions:")
        print("  --dry-run    Print memories without storing (old behavior)")
        print("\nExample:")
        print("  python scripts/store_in_mcp_kb.py workspace/analysis/VIDEO_ID_analysis.json")
        return

    dry_run = "--dry-run" in sys.argv
    analysis_file = [a for a in sys.argv[1:] if not a.startswith("--")][0]

    if not Path(analysis_file).exists():
        print(f"❌ File not found: {analysis_file}")
        sys.exit(1)

    try:
        # Create storage handler
        storage = EnhancedKBStorage(analysis_file)

        # Generate all memories
        print(f"🎬 Processing video: {storage.video_id}")
        memories = storage.generate_all_memories()
        metadata = storage._extract_metadata()

        if dry_run or not API_AVAILABLE:
            # Old behavior: print for manual storage
            if not API_AVAILABLE and not dry_run:
                print("⚠️  API client unavailable, falling back to dry-run mode")
            storage.print_memories_for_manual_storage(memories)
        else:
            # NEW: Store via unified-memory API
            print("\n📡 Storing via unified-memory API...")

            if not health_check():
                print("❌ Unified-memory API unreachable. Use --dry-run to print instead.")
                sys.exit(1)

            # 1. Store one NOTE (syncs to Notion) — STORE-02
            note_content = _build_note_content(storage, memories)
            note_metadata = {
                "area": "vecia",
                "video_id": storage.video_id,
                "source": "youtube",
                "url": metadata["video_url"],
                "channel": metadata["channel"],
                "format": "long",
            }
            # Title format: {YEAR}-{MON}-Video-{SLUG} per CONTEXT.md
            from datetime import datetime

            now = datetime.now()
            slug = (
                metadata["video_title"]
                .lower()
                .replace(" ", "-")
                .replace(":", "")
                .replace("'", "")[:40]
            )
            note_title = f"{now.year}-{now.strftime('%b')}-Video-{slug}"
            try:
                note_result = store_note(
                    title=note_title,
                    content=note_content,
                    note_type="video",
                    metadata=note_metadata,
                )
                print(f"✅ Note stored (syncs to Notion): {note_result.get('id', 'ok')}")
            except Exception as e:
                print(f"⚠️  Note storage failed: {e}")

            # 2. Store one MEMORY (for agent retrieval)
            memory_content = _build_memory_content(memories)
            memory_tags = memories[0]["tags"] if memories else []
            memory_metadata = {
                "video_id": storage.video_id,
                "area": "vecia",
                "type": "video-knowledge",
            }
            try:
                mem_result = store_memory(
                    content=memory_content,
                    tags=memory_tags,
                    namespace="/alex/openclaw/videos/",
                    metadata=memory_metadata,
                )
                print(f"✅ Memory stored (agent retrieval): {mem_result.get('id', 'ok')}")
            except Exception as e:
                print(f"⚠️  Memory storage failed: {e}")

        print(f"\n✅ Generated {len(memories)} sections for video {storage.video_id}")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
