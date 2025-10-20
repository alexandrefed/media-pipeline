"""Formatter for AI tools content"""

from typing import Dict, Any
from .base_formatter import BaseFormatter


class AIToolsFormatter(BaseFormatter):
    """Formats AI tools analysis into rich Telegram messages"""

    def format(self, analysis: Dict[str, Any]) -> str:
        """
        Format AI tools analysis into HTML message

        Args:
            analysis: Parsed analysis JSON data

        Returns:
            Formatted HTML message string
        """
        message = self._build_header("🎬", "NEW VIDEO PROCESSED", analysis)
        message += self._build_summary(analysis)
        message += self._build_takeaways(analysis)
        message += self._build_tools(analysis)
        message += self._build_concepts(analysis)
        message += self._build_key_insight(analysis)
        message += self._build_footer(analysis)

        return message

    def _build_takeaways(self, analysis: Dict[str, Any]) -> str:
        """Build key takeaways section"""
        takeaways = analysis.get('key_takeaways', [])

        if not takeaways:
            return ""

        # Truncate to max_takeaways
        takeaways = self._truncate_list(takeaways)

        section = "<b>🔑 Top Takeaways:</b>\n"

        for i, takeaway in enumerate(takeaways, 1):
            # Truncate individual takeaways if too long
            if len(takeaway) > 200:
                takeaway = takeaway[:197] + "..."

            section += f"{i}. {self._escape_html(takeaway)}\n"

        section += "\n"

        return section

    def _build_tools(self, analysis: Dict[str, Any]) -> str:
        """Build tools mentioned section"""
        tools = analysis.get('tools_mentioned', [])

        if not tools:
            return ""

        # Limit to 8 tools to keep message concise
        tools = self._truncate_list(tools, max_items=8)

        section = "<b>🛠️ Tools Mentioned:</b>\n"
        section += ", ".join(self._escape_html(tool) for tool in tools)
        section += "\n\n"

        return section

    def _build_concepts(self, analysis: Dict[str, Any]) -> str:
        """Build key concepts section"""
        concepts = analysis.get('key_concepts', [])

        if not concepts:
            return ""

        # Limit to 5 concepts
        concepts = self._truncate_list(concepts, max_items=5)

        section = "<b>💭 Key Concepts:</b>\n"
        section += ", ".join(self._escape_html(concept) for concept in concepts)
        section += "\n\n"

        return section

    def _build_key_insight(self, analysis: Dict[str, Any]) -> str:
        """Build key insight or notable quote"""
        # Try to get a notable quote from practical examples or actionable insights
        practical_examples = analysis.get('practical_examples', [])
        actionable_insights = analysis.get('actionable_insights', [])

        insight = None

        if practical_examples:
            insight = practical_examples[0]
        elif actionable_insights:
            insight = actionable_insights[0]

        if not insight:
            return ""

        # Truncate if too long
        if len(insight) > 250:
            insight = insight[:247] + "..."

        return f"<b>💡 Key Insight:</b>\n<i>{self._escape_html(insight)}</i>\n"
