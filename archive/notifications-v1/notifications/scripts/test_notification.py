#!/usr/bin/env python3
"""
Test the Telegram notification system

This script tests:
1. Configuration loading
2. Telegram bot connection
3. Message formatting
4. Sending a test message

Usage:
    python test_notification.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.telegram_client import TelegramNotifier
from core.config_manager import ConfigManager


def main():
    print("=" * 50)
    print("Testing Telegram Notification System")
    print("=" * 50)
    print()

    # Test 1: Configuration loading
    print("1. Testing configuration...")
    try:
        config = ConfigManager()
        print("   ✓ Configuration loaded successfully")
        print(f"   - Bot token: {config.telegram_bot_token[:10]}...")
        print(f"   - Chat ID: {config.telegram_chat_id}")
        print(f"   - Immediate notifications: {'enabled' if config.immediate_notifications_enabled else 'disabled'}")
    except FileNotFoundError as e:
        print(f"   ❌ {e}")
        print()
        print("Please copy config.example.yaml to config.yaml and configure your settings:")
        print("  cp notifications/config/config.example.yaml notifications/config/config.yaml")
        sys.exit(1)
    except ValueError as e:
        print(f"   ❌ {e}")
        sys.exit(1)

    print()

    # Test 2: Telegram connection
    print("2. Testing Telegram bot connection...")
    try:
        notifier = TelegramNotifier(config)
        if notifier.test_connection():
            print("   ✓ Successfully connected to Telegram bot")
        else:
            print("   ❌ Failed to connect to Telegram bot")
            sys.exit(1)
    except Exception as e:
        print(f"   ❌ Connection error: {e}")
        sys.exit(1)

    print()

    # Test 3: Send test message
    print("3. Sending test message...")
    test_message = """<b>🧪 Test Message</b>

This is a test message from the Knowledge Base Notification System.

<b>Features:</b>
✓ HTML formatting support
✓ Bold and <i>italic</i> text
✓ Links: <a href="https://github.com">GitHub</a>

If you're seeing this message, the notification system is working correctly!

<i>Sent from notifications/scripts/test_notification.py</i>"""

    try:
        result = notifier.send(test_message)
        print("   ✓ Test message sent successfully")
        print(f"   - Message ID: {result.get('result', {}).get('message_id')}")
    except Exception as e:
        print(f"   ❌ Failed to send message: {e}")
        sys.exit(1)

    print()
    print("=" * 50)
    print("All tests passed! 🎉")
    print("=" * 50)
    print()
    print("Next steps:")
    print("1. Process a video using /process-youtube or /process-sports-video")
    print("2. Send notification:")
    print("   python notifications/scripts/send_notification.py path/to/analysis.json")
    print()


if __name__ == "__main__":
    main()
