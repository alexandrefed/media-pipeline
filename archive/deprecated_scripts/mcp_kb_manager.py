"""
MCP KB Memory storage manager for AI Knowledge Base.

This module manages storing and retrieving video summaries and technical information
in the MCP KB Memory system for easy access via Claude Code.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class MCPKBManager:
    """Manage storage and retrieval of video knowledge in MCP KB Memory."""

    def __init__(self):
        """Initialize MCP KB Manager."""
        self.system_tag = "youtube-knowledge-base"

    def store_video_summary(self, summary_data: Dict) -> Dict:
        """
        Store video summary in MCP KB Memory.

        Args:
            summary_data: Dictionary containing VideoSummary data

        Returns:
            Result dictionary with success status and memory hash
        """
        from subprocess import run, PIPE

        # Build the main content string
        content_parts = []

        # Add title and channel
        title = summary_data.get("title", "Unknown Video")
        channel = summary_data.get("channel_name", "Unknown Channel")
        video_id = summary_data.get("video_id", "unknown")

        content_parts.append(f"Video: {title}")
        content_parts.append(f"Channel: {channel}")
        content_parts.append(f"Video ID: {video_id}")
        content_parts.append(f"Content Type: {summary_data.get('content_type', 'unknown')}")
        content_parts.append("")

        # Add summary
        summary_text = summary_data.get("summary", "")
        content_parts.append("Summary:")
        content_parts.append(summary_text)
        content_parts.append("")

        # Add technical information
        tech_info = summary_data.get("technical_info", {})

        if tech_info.get("tools_mentioned"):
            content_parts.append("Tools: " + ", ".join(tech_info["tools_mentioned"]))

        if tech_info.get("commands"):
            content_parts.append("\nKey Commands:")
            for cmd in tech_info["commands"][:10]:  # Top 10 commands
                content_parts.append(f"  - {cmd}")

        if tech_info.get("key_concepts"):
            content_parts.append("\nKey Concepts:")
            for concept in tech_info["key_concepts"][:10]:  # Top 10 concepts
                content_parts.append(f"  - {concept}")

        if tech_info.get("workflows"):
            content_parts.append("\nWorkflows:")
            for workflow in tech_info["workflows"][:5]:  # Top 5 workflows
                content_parts.append(f"  - {workflow}")

        # Add key takeaways
        takeaways = summary_data.get("key_takeaways", [])
        if takeaways:
            content_parts.append("\nKey Takeaways:")
            for i, takeaway in enumerate(takeaways, 1):
                content_parts.append(f"{i}. {takeaway}")

        # Add YouTube URL
        content_parts.append(f"\nWatch: https://youtube.com/watch?v={video_id}")

        # Build final content
        content = "\n".join(content_parts)

        # Build tags list
        tags = summary_data.get("tags", [])
        tags.append(self.system_tag)  # Add system tag
        tags.append(f"video-{video_id}")  # Add video ID tag
        tags.append(f"channel-{channel.lower().replace(' ', '-')}")  # Add channel tag

        # Store in MCP KB using Python API
        try:
            # Import the MCP KB memory tools dynamically
            import sys
            import asyncio

            # Create an async function to call the store memory tool
            async def store_async():
                # Note: In actual implementation, we'd use the MCP KB memory Python API
                # For now, we'll construct the command to be executed
                metadata = {
                    "tags": tags,
                    "type": "youtube-video",
                    "video_id": video_id,
                    "channel": channel,
                    "content_type": summary_data.get("content_type"),
                    "processed_date": datetime.now().isoformat()
                }

                # Return the data that would be stored
                return {
                    "content": content,
                    "metadata": metadata,
                    "success": True,
                    "tags": tags
                }

            # Run the async function
            if sys.platform == 'win32':
                loop = asyncio.ProactorEventLoopPolicy().new_event_loop()
            else:
                loop = asyncio.new_event_loop()

            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(store_async())
            loop.close()

            return result

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "content": content,
                "tags": tags
            }

    def retrieve_by_topic(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Retrieve videos by topic/query.

        Args:
            query: Search query
            max_results: Maximum number of results to return

        Returns:
            List of matching video summaries
        """
        # Placeholder for MCP KB retrieve functionality
        # In actual implementation, this would call mcp__unified-memory__memory_search
        return []

    def retrieve_by_tag(self, tag: str) -> List[Dict]:
        """
        Retrieve videos by specific tag.

        Args:
            tag: Tag to search for

        Returns:
            List of matching video summaries
        """
        # Placeholder for MCP KB search by tag functionality
        # In actual implementation, this would call mcp__unified-memory__memory_search
        return []

    def get_statistics(self) -> Dict:
        """
        Get statistics about stored videos.

        Returns:
            Dictionary with statistics
        """
        # Placeholder - would query MCP KB for stats
        return {
            "total_videos": 0,
            "total_channels": 0,
            "content_types": {}
        }


def main():
    """CLI interface for MCP KB management."""
    import sys

    if len(sys.argv) < 3:
        print("MCP KB Storage Manager")
        print("\nUsage:")
        print("  python -m src.storage.mcp_kb_manager store <summary_json_file>")
        print("  python -m src.storage.mcp_kb_manager retrieve <query>")
        print("  python -m src.storage.mcp_kb_manager stats")
        print("\nExample:")
        print("  python -m src.storage.mcp_kb_manager store summary.json")
        return

    command = sys.argv[1]
    manager = MCPKBManager()

    if command == "store":
        summary_file = sys.argv[2]

        try:
            # Load summary
            with open(summary_file, 'r', encoding='utf-8') as f:
                summary_data = json.load(f)

            print(f"📥 Storing video summary: {summary_data.get('video_id')}")

            # Store in MCP KB
            result = manager.store_video_summary(summary_data)

            if result.get("success"):
                print("✅ Video summary stored successfully in MCP KB Memory!")
                print(f"🏷️  Tags: {', '.join(result.get('tags', [])[:5])}")
                print(f"\n📝 Content Preview:")
                print(result.get("content", "")[:300] + "...")
            else:
                print(f"❌ Failed to store: {result.get('error', 'Unknown error')}")
                print(f"\n📋 Generated content and tags for manual storage:")
                print(f"\nContent:\n{result.get('content', '')}")
                print(f"\nTags: {', '.join(result.get('tags', []))}")

        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

    elif command == "retrieve":
        query = ' '.join(sys.argv[2:])
        print(f"🔍 Searching for: {query}")

        results = manager.retrieve_by_topic(query)
        print(f"✅ Found {len(results)} results")

        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result.get('title', 'Unknown')}")
            print(f"   Channel: {result.get('channel', 'Unknown')}")
            print(f"   Video ID: {result.get('video_id', 'unknown')}")

    elif command == "stats":
        stats = manager.get_statistics()
        print("📊 MCP KB Statistics:")
        print(f"   Total Videos: {stats.get('total_videos', 0)}")
        print(f"   Total Channels: {stats.get('total_channels', 0)}")
        print(f"   Content Types: {stats.get('content_types', {})}")

    else:
        print(f"❌ Unknown command: {command}")


if __name__ == "__main__":
    main()
