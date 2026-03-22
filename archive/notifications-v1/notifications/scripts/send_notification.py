#!/usr/bin/env python3
"""
Send notification for a processed video

Usage:
    python send_notification.py <path_to_analysis_json>

Example:
    python send_notification.py workspace/analysis/VZkm1jSs8Lg_analysis.json
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.telegram_client import TelegramNotifier
from core.config_manager import ConfigManager
from formatters.ai_tools_formatter import AIToolsFormatter
from formatters.sports_formatter import SportsFormatter
from utils.json_parser import load_analysis_json, detect_content_type, validate_analysis_structure


def main():
    if len(sys.argv) < 2:
        print("Usage: python send_notification.py <path_to_analysis_json>")
        print("\nExample:")
        print("  python send_notification.py workspace/analysis/VZkm1jSs8Lg_analysis.json")
        sys.exit(1)

    analysis_path = sys.argv[1]

    try:
        # Load configuration
        print("Loading configuration...")
        config = ConfigManager()

        # Check if immediate notifications are enabled
        if not config.immediate_notifications_enabled:
            print("⚠️  Immediate notifications are disabled in config.yaml")
            print("Enable them by setting notifications.immediate.enabled to true")
            sys.exit(0)

        # Load and validate analysis JSON
        print(f"Loading analysis from: {analysis_path}")
        analysis = load_analysis_json(analysis_path)

        if not validate_analysis_structure(analysis):
            print("❌ Invalid analysis structure - missing required fields")
            print("Required fields: summary, video_id")
            sys.exit(1)

        # Detect content type
        content_type = detect_content_type(analysis)
        print(f"✓ Detected content type: {content_type}")

        # Select appropriate formatter
        max_takeaways = config.max_takeaways

        if content_type == 'sports':
            formatter = SportsFormatter(max_takeaways=max_takeaways)
        else:  # default to ai_tools
            formatter = AIToolsFormatter(max_takeaways=max_takeaways)

        # Format message
        print("Formatting message...")
        message = formatter.format(analysis)

        # Send notification
        print("Sending notification to Telegram...")
        notifier = TelegramNotifier(config)
        result = notifier.send_long_message(message)

        # Success
        print(f"✓ Notification sent successfully!")
        print(f"  - Message parts: {len(result)}")
        print(f"  - Content type: {content_type}")
        print(f"  - Video: {analysis.get('title', 'Unknown')}")

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
