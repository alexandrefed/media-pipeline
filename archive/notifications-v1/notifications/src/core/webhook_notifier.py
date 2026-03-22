#!/usr/bin/env python3
"""
Webhook notifier for auto-syncing MCP KB Memory storage to n8n workflows.

This module automatically calls the n8n webhook after storing videos in MCP KB Memory,
enabling immediate notifications, spaced repetition, and weekly digest features.
"""

import json
import os
import time
from typing import Dict, List, Optional
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import requests
except ImportError:
    print("⚠️  Warning: 'requests' library not installed. Webhook notifications disabled.")
    print("   Install with: uv add requests")
    requests = None


class WebhookNotifier:
    """Handles automatic webhook calls to n8n for notification workflows."""

    def __init__(self, webhook_url: str = None):
        self.webhook_url = webhook_url or os.getenv(
            "N8N_WEBHOOK_URL",
            "https://n8n.vecia.fr/webhook/ai-kb-video-insights"
        )
        self.max_retries = 3
        self.retry_delay = 2  # seconds

    def extract_insights_from_ai_tools(self, analysis: Dict) -> List[Dict]:
        """
        Extract insights from AI tools analysis JSON.

        Looks for insights in various locations:
        - analysis['insights'] (array)
        - analysis['key_takeaways'] (array)
        - analysis['actionable_insights'] (array)
        """
        insights = []

        # Try different insight locations
        insight_sources = [
            analysis.get('insights', []),
            analysis.get('actionable_insights', []),
            analysis.get('key_takeaways', [])
        ]

        for source in insight_sources:
            if not source:
                continue

            for item in source:
                if isinstance(item, dict):
                    insight = {
                        'text': item.get('text', item.get('insight', item.get('takeaway', ''))),
                        'type': item.get('type', 'concept'),
                        'context': item.get('context', item.get('description', '')),
                        'category': item.get('category', ''),
                        'tags': item.get('tags', []),
                        'timestamp_start': item.get('timestamp_start'),
                        'timestamp_end': item.get('timestamp_end'),
                        'quality_score': item.get('quality_score', item.get('quality', 0.7)),
                        'priority': item.get('priority', item.get('priority_level', 'medium')),
                        'actionable': item.get('actionable', True)
                    }
                elif isinstance(item, str):
                    insight = {
                        'text': item,
                        'type': 'concept',
                        'context': '',
                        'category': '',
                        'tags': [],
                        'timestamp_start': None,
                        'timestamp_end': None,
                        'quality_score': 0.7,
                        'priority': 'medium',
                        'actionable': True
                    }

                # Only add if we have actual text
                if insight.get('text'):
                    insights.append(insight)

        return insights

    def extract_insights_from_sports(self, analysis: Dict) -> List[Dict]:
        """
        Extract insights from sports analysis JSON.

        Converts protocols, techniques, and evidence into insights format.
        """
        insights = []

        # Extract from exercise protocols
        protocols = analysis.get('exercise_protocols', analysis.get('protocols', []))
        for protocol in protocols:
            if isinstance(protocol, dict):
                # Create insight from protocol
                text = protocol.get('exercise', protocol.get('name', ''))
                if protocol.get('volume') or protocol.get('frequency'):
                    text += f" - {protocol.get('volume', '')} at {protocol.get('frequency', '')}"

                insights.append({
                    'text': text,
                    'type': 'protocol',
                    'context': protocol.get('notes', protocol.get('rationale', '')),
                    'category': analysis.get('sport_discipline', 'training'),
                    'tags': ['protocol', 'exercise'],
                    'timestamp_start': protocol.get('timestamp_start'),
                    'timestamp_end': protocol.get('timestamp_end'),
                    'quality_score': protocol.get('quality_score', 0.8),
                    'priority': 'high',
                    'actionable': True
                })

        # Extract from key findings
        key_findings = analysis.get('key_findings', [])
        for finding in key_findings:
            if isinstance(finding, dict):
                insights.append({
                    'text': finding.get('text', finding.get('finding', '')),
                    'type': 'technique',
                    'context': finding.get('evidence', finding.get('context', '')),
                    'category': analysis.get('sport_discipline', 'training'),
                    'tags': ['finding', 'evidence'],
                    'timestamp_start': finding.get('timestamp_start'),
                    'timestamp_end': finding.get('timestamp_end'),
                    'quality_score': finding.get('quality_score', 0.75),
                    'priority': finding.get('priority', 'medium'),
                    'actionable': finding.get('actionable', True)
                })
            elif isinstance(finding, str):
                insights.append({
                    'text': finding,
                    'type': 'technique',
                    'context': '',
                    'category': analysis.get('sport_discipline', 'training'),
                    'tags': ['finding'],
                    'timestamp_start': None,
                    'timestamp_end': None,
                    'quality_score': 0.75,
                    'priority': 'medium',
                    'actionable': True
                })

        return insights

    def build_webhook_payload(self, analysis_file: Path) -> Optional[Dict]:
        """
        Build webhook payload from analysis JSON file.

        Returns payload dict or None if file not found/invalid.
        """
        if not analysis_file.exists():
            print(f"❌ Analysis file not found: {analysis_file}")
            return None

        try:
            with open(analysis_file, 'r', encoding='utf-8') as f:
                analysis = json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in analysis file: {e}")
            return None

        # Extract metadata
        metadata = analysis.get('video_metadata', analysis.get('metadata', {}))

        # Determine pipeline type
        is_sports = (
            'sport_discipline' in analysis or
            'exercise_protocols' in analysis or
            '_sports_analysis' in str(analysis_file)
        )
        pipeline_type = 'sports' if is_sports else 'ai_tools'

        # Extract video ID
        video_id = metadata.get('video_id', '')
        if not video_id:
            # Try to extract from filename
            filename = analysis_file.stem
            if '_analysis' in filename:
                video_id = filename.replace('_analysis', '').replace('_sports', '')

        # Extract insights based on type
        if is_sports:
            insights = self.extract_insights_from_sports(analysis)
        else:
            insights = self.extract_insights_from_ai_tools(analysis)

        # Build payload
        payload = {
            'video_id': video_id,
            'title': metadata.get('video_title', metadata.get('title', f'Video {video_id}')),
            'channel_name': metadata.get('channel', metadata.get('channel_name', 'Unknown Channel')),
            'channel_id': metadata.get('channel_id', ''),
            'url': metadata.get('video_url', metadata.get('url', f'https://youtube.com/watch?v={video_id}')),
            'duration_seconds': metadata.get('duration_seconds', metadata.get('duration', 0)),
            'pipeline_type': pipeline_type,
            'tags': analysis.get('tags', analysis.get('content_tags', [])),
            'total_chunks': analysis.get('total_chunks', len(insights)),
            'insights': insights
        }

        return payload

    def send_to_webhook(self, payload: Dict) -> bool:
        """
        Send payload to n8n webhook with retries.

        Returns True if successful, False otherwise.
        """
        if not requests:
            print("⚠️  Skipping webhook (requests library not available)")
            return False

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.post(
                    self.webhook_url,
                    json=payload,  # Direct payload - n8n webhook puts this in $json.body
                    headers={'Content-Type': 'application/json'},
                    timeout=10
                )

                if response.status_code == 200:
                    # Try to parse JSON response, handle empty responses
                    try:
                        result = response.json() if response.text else {}
                    except ValueError:
                        result = {}

                    print(f"✅ Webhook sent successfully!")
                    print(f"   Video ID: {payload['video_id']}")
                    print(f"   Insights: {len(payload['insights'])}")
                    print(f"   Pipeline: {payload['pipeline_type']}")
                    if result.get('notification_sent'):
                        print(f"   📱 Telegram notification sent")
                    return True
                else:
                    print(f"⚠️  Webhook attempt {attempt}/{self.max_retries} failed: HTTP {response.status_code}")
                    if attempt < self.max_retries:
                        time.sleep(self.retry_delay)

            except requests.exceptions.Timeout:
                print(f"⚠️  Webhook attempt {attempt}/{self.max_retries} timed out")
                if attempt < self.max_retries:
                    time.sleep(self.retry_delay)
            except requests.exceptions.RequestException as e:
                print(f"❌ Webhook error: {e}")
                return False

        print(f"❌ Webhook failed after {self.max_retries} attempts")
        return False

    def notify_from_analysis_file(self, analysis_file: str) -> bool:
        """
        Main entry point: Build payload from analysis file and send to webhook.

        Returns True if successful, False otherwise.
        """
        analysis_path = Path(analysis_file)

        print(f"\n🔔 Sending webhook notification...")
        print(f"   Analysis: {analysis_path.name}")

        # Build payload
        payload = self.build_webhook_payload(analysis_path)
        if not payload:
            return False

        # Send to webhook
        return self.send_to_webhook(payload)


def notify_video_processed(analysis_file: str) -> bool:
    """
    Convenience function for scripts to call.

    Usage:
        from notifications.src.core.webhook_notifier import notify_video_processed
        notify_video_processed('workspace/analysis/VIDEO_ID_analysis.json')
    """
    notifier = WebhookNotifier()
    return notifier.notify_from_analysis_file(analysis_file)


if __name__ == '__main__':
    # CLI usage
    if len(sys.argv) < 2:
        print("Usage: python webhook_notifier.py <analysis_file.json>")
        sys.exit(1)

    analysis_file = sys.argv[1]
    success = notify_video_processed(analysis_file)
    sys.exit(0 if success else 1)
