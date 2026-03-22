"""JSON parsing utilities"""

import json
from pathlib import Path
from typing import Dict, Any


def load_analysis_json(file_path: str) -> Dict[str, Any]:
    """
    Load and parse an analysis JSON file

    Args:
        file_path: Path to JSON file

    Returns:
        Parsed JSON data as dictionary

    Raises:
        FileNotFoundError: If file doesn't exist
        json.JSONDecodeError: If file is not valid JSON
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Analysis file not found: {file_path}")

    with open(path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in {file_path}: {str(e)}",
                e.doc,
                e.pos
            ) from e

    return data


def detect_content_type(analysis: Dict[str, Any]) -> str:
    """
    Detect content type from analysis JSON

    Args:
        analysis: Parsed analysis data

    Returns:
        Content type: 'sports', 'ai_tools', or 'unknown'
    """
    # Check for sports-specific fields
    sports_indicators = [
        'sport_discipline',
        'exercises_demonstrated',
        'biomechanical_principles',
        'scientific_citations',
        'programming_logic'
    ]

    # Check for AI tools specific fields
    ai_tools_indicators = [
        'tools_mentioned',
        'commands',
        'workflows',
        'actionable_insights'
    ]

    sports_count = sum(1 for field in sports_indicators if field in analysis)
    ai_tools_count = sum(1 for field in ai_tools_indicators if field in analysis)

    if sports_count >= 3:
        return 'sports'
    elif ai_tools_count >= 2:
        return 'ai_tools'
    else:
        # Check metadata for hints
        metadata = analysis.get('metadata', {})
        analyzed_by = metadata.get('analyzed_by', '')

        if 'sports' in analyzed_by.lower():
            return 'sports'
        elif any(tool in analyzed_by.lower() for tool in ['youtube', 'seankochel', 'indydevdan']):
            return 'ai_tools'

        # Default to ai_tools if uncertain
        return 'ai_tools'


def validate_analysis_structure(analysis: Dict[str, Any]) -> bool:
    """
    Validate that analysis has minimum required structure

    Args:
        analysis: Parsed analysis data

    Returns:
        True if valid, False otherwise
    """
    # Required fields for any analysis
    required_fields = ['summary', 'video_id']

    for field in required_fields:
        if field not in analysis or not analysis[field]:
            return False

    return True
