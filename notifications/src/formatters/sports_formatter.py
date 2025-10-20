"""Formatter for sports science content"""

from typing import Dict, Any
from .base_formatter import BaseFormatter


class SportsFormatter(BaseFormatter):
    """Formats sports science analysis into rich Telegram messages"""

    def format(self, analysis: Dict[str, Any]) -> str:
        """
        Format sports analysis into HTML message

        Args:
            analysis: Parsed analysis JSON data

        Returns:
            Formatted HTML message string
        """
        message = self._build_header("🏋️", "NEW SPORTS SCIENCE PROCESSED", analysis)
        message += self._build_summary(analysis)
        message += self._build_evidence_tier(analysis)
        message += self._build_takeaways(analysis)
        message += self._build_protocol(analysis)
        message += self._build_why_reasoning(analysis)
        message += self._build_footer(analysis)

        return message

    def _build_evidence_tier(self, analysis: Dict[str, Any]) -> str:
        """Build evidence tier section"""
        citations = analysis.get('scientific_citations', [])

        if not citations:
            return ""

        # Get highest quality citation (lowest tier number = highest quality)
        best_citation = min(citations, key=lambda x: x.get('evidence_tier', 4))
        tier = best_citation.get('evidence_tier', 0)

        tier_labels = {
            1: "Tier 1 (Meta-analysis/Systematic Review)",
            2: "Tier 2 (RCT)",
            3: "Tier 3 (Observational Study)",
            4: "Tier 4 (Expert Opinion/Theory)"
        }

        label = tier_labels.get(tier, "Not specified")

        section = f"<b>🔬 Evidence Quality:</b> {self._escape_html(label)}\n\n"

        return section

    def _build_takeaways(self, analysis: Dict[str, Any]) -> str:
        """Build key takeaways section"""
        takeaways = analysis.get('key_takeaways', [])

        if not takeaways:
            return ""

        # Truncate to max_takeaways
        takeaways = self._truncate_list(takeaways)

        section = "<b>🔑 Key Findings:</b>\n"

        for i, takeaway in enumerate(takeaways, 1):
            # Truncate individual takeaways if too long
            if len(takeaway) > 200:
                takeaway = takeaway[:197] + "..."

            section += f"{i}. {self._escape_html(takeaway)}\n"

        section += "\n"

        return section

    def _build_protocol(self, analysis: Dict[str, Any]) -> str:
        """Build protocol details section"""
        programming_logic = analysis.get('programming_logic', {})

        if not programming_logic:
            return ""

        volume = programming_logic.get('volume_rationale', '')
        frequency = programming_logic.get('frequency_rationale', '')
        intensity = programming_logic.get('intensity_rationale', '')

        if not any([volume, frequency, intensity]):
            return ""

        section = "<b>📊 Protocol:</b>\n"

        if volume:
            # Extract key info, truncate
            volume_short = volume.split('.')[0] if '.' in volume else volume
            if len(volume_short) > 100:
                volume_short = volume_short[:97] + "..."
            section += f"• <i>Volume:</i> {self._escape_html(volume_short)}\n"

        if frequency:
            frequency_short = frequency.split('.')[0] if '.' in frequency else frequency
            if len(frequency_short) > 100:
                frequency_short = frequency_short[:97] + "..."
            section += f"• <i>Frequency:</i> {self._escape_html(frequency_short)}\n"

        if intensity:
            intensity_short = intensity.split('.')[0] if '.' in intensity else intensity
            if len(intensity_short) > 100:
                intensity_short = intensity_short[:97] + "..."
            section += f"• <i>Intensity:</i> {self._escape_html(intensity_short)}\n"

        section += "\n"

        return section

    def _build_why_reasoning(self, analysis: Dict[str, Any]) -> str:
        """Build WHY reasoning section"""
        why_reasoning = analysis.get('why_reasoning', {})

        if not why_reasoning:
            return ""

        # Get biomechanical and physiological reasoning (most valuable)
        biomechanical = why_reasoning.get('biomechanical', '')
        physiological = why_reasoning.get('physiological', '')

        if not biomechanical and not physiological:
            return ""

        section = "<b>🎯 WHY It Works:</b>\n"

        # Prefer physiological, but use biomechanical if that's all we have
        reasoning = physiological if physiological else biomechanical

        # Truncate to 300 chars to keep message concise
        if len(reasoning) > 300:
            # Try to end at sentence boundary
            truncated = reasoning[:297]
            last_period = truncated.rfind('.')
            if last_period > 200:  # Only use sentence boundary if reasonable
                reasoning = reasoning[:last_period + 1]
            else:
                reasoning = truncated + "..."

        section += f"{self._escape_html(reasoning)}\n"

        return section
