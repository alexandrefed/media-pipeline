"""Base formatter class for notification messages"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseFormatter(ABC):
    """Base class for message formatters"""

    def __init__(self, max_takeaways: int = 5):
        """
        Initialize formatter

        Args:
            max_takeaways: Maximum number of takeaways to include
        """
        self.max_takeaways = max_takeaways

    @abstractmethod
    def format(self, analysis: Dict[str, Any]) -> str:
        """
        Format analysis data into a rich HTML message

        Args:
            analysis: Parsed analysis JSON data

        Returns:
            Formatted HTML message string
        """
        pass

    def _escape_html(self, text: str) -> str:
        """
        Escape HTML special characters

        Args:
            text: Text to escape

        Returns:
            HTML-escaped text
        """
        if not text:
            return ""

        replacements = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
        }

        for char, escape in replacements.items():
            text = text.replace(char, escape)

        return text

    def _format_duration(self, seconds: int) -> str:
        """
        Format duration in seconds to human-readable format

        Args:
            seconds: Duration in seconds

        Returns:
            Formatted duration (e.g., "5:30" or "1:23:45")
        """
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"

    def _truncate_list(self, items: List[Any], max_items: int = None) -> List[Any]:
        """
        Truncate a list to maximum items

        Args:
            items: List to truncate
            max_items: Maximum number of items (uses self.max_takeaways if None)

        Returns:
            Truncated list
        """
        if max_items is None:
            max_items = self.max_takeaways

        return items[:max_items] if items else []

    def _build_header(self, emoji: str, title: str, analysis: Dict[str, Any]) -> str:
        """
        Build message header

        Args:
            emoji: Emoji for the header
            title: Title text
            analysis: Analysis data

        Returns:
            Formatted header HTML
        """
        channel = self._escape_html(analysis.get('channel', 'Unknown'))
        video_title = self._escape_html(analysis.get('title', 'Untitled'))
        duration = analysis.get('duration_seconds', 0)

        header = f"{emoji} <b>{title}</b>\n\n"
        header += f"<b>{video_title}</b>\n"
        header += f"📺 {channel}"

        if duration:
            header += f" | ⏱️ {self._format_duration(duration)}"

        header += "\n\n"

        return header

    def _build_summary(self, analysis: Dict[str, Any]) -> str:
        """
        Build summary section

        Args:
            analysis: Analysis data

        Returns:
            Formatted summary HTML
        """
        summary = analysis.get('summary', '')

        if not summary:
            return ""

        # Truncate if too long (keep first 500 chars)
        if len(summary) > 500:
            summary = summary[:497] + "..."

        return f"<b>Executive Summary:</b>\n{self._escape_html(summary)}\n\n"

    def _build_footer(self, analysis: Dict[str, Any]) -> str:
        """
        Build message footer

        Args:
            analysis: Analysis data

        Returns:
            Formatted footer HTML
        """
        video_id = analysis.get('video_id', '')
        metadata = analysis.get('metadata', {})

        footer = "\n"

        # Add tags if available
        if metadata.get('tags'):
            tags = metadata['tags']
            if isinstance(tags, list):
                tag_str = ', '.join(tags)
            else:
                tag_str = tags
            footer += f"<i>Tags: {self._escape_html(tag_str)}</i>\n"

        # Add video link
        if video_id:
            footer += f"\n<a href=\"https://youtube.com/watch?v={video_id}\">Watch Video</a>"

        return footer
