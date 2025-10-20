"""Telegram client for sending notifications"""

import requests
from typing import Optional, Dict, Any
from .config_manager import ConfigManager


class TelegramNotifier:
    """Handles sending messages via Telegram Bot API"""

    def __init__(self, config: Optional[ConfigManager] = None):
        """
        Initialize Telegram notifier

        Args:
            config: ConfigManager instance. If None, creates a new one.
        """
        self.config = config or ConfigManager()
        self.bot_token = self.config.telegram_bot_token
        self.chat_id = self.config.telegram_chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send(self, message: str, parse_mode: str = "HTML", disable_preview: bool = False) -> Dict[str, Any]:
        """
        Send a message to Telegram

        Args:
            message: Message text (supports HTML formatting)
            parse_mode: Message parse mode ('HTML', 'Markdown', or None)
            disable_preview: Disable link previews

        Returns:
            Response from Telegram API

        Raises:
            requests.RequestException: If the request fails
            ValueError: If the response indicates an error
        """
        url = f"{self.base_url}/sendMessage"

        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_preview
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()

            data = response.json()

            if not data.get('ok'):
                error_description = data.get('description', 'Unknown error')
                raise ValueError(f"Telegram API error: {error_description}")

            return data

        except requests.RequestException as e:
            raise requests.RequestException(
                f"Failed to send Telegram message: {str(e)}\n"
                f"Please check your bot token and chat ID in the configuration."
            ) from e

    def send_long_message(self, message: str, parse_mode: str = "HTML") -> list[Dict[str, Any]]:
        """
        Send a long message, splitting it if necessary (Telegram has 4096 char limit)

        Args:
            message: Message text (supports HTML formatting)
            parse_mode: Message parse mode ('HTML', 'Markdown', or None)

        Returns:
            List of responses from Telegram API (one per message part)
        """
        MAX_LENGTH = 4096

        if len(message) <= MAX_LENGTH:
            return [self.send(message, parse_mode=parse_mode)]

        # Split message into chunks
        responses = []
        parts = self._split_message(message, MAX_LENGTH)

        for i, part in enumerate(parts):
            if i > 0:
                # Add continuation indicator
                part = f"<i>(continued...)</i>\n\n{part}"

            responses.append(self.send(part, parse_mode=parse_mode))

        return responses

    def _split_message(self, message: str, max_length: int) -> list[str]:
        """
        Split a message into chunks that respect HTML tags and max length

        Args:
            message: Message to split
            max_length: Maximum length per chunk

        Returns:
            List of message chunks
        """
        if len(message) <= max_length:
            return [message]

        # Simple split at newlines to avoid breaking HTML tags
        parts = []
        current_part = ""

        for line in message.split('\n'):
            if len(current_part) + len(line) + 1 <= max_length:
                current_part += line + '\n'
            else:
                if current_part:
                    parts.append(current_part.rstrip())
                current_part = line + '\n'

        if current_part:
            parts.append(current_part.rstrip())

        return parts

    def test_connection(self) -> bool:
        """
        Test the Telegram bot connection

        Returns:
            True if connection is successful, False otherwise
        """
        url = f"{self.base_url}/getMe"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('ok'):
                bot_info = data.get('result', {})
                print(f"✓ Connected to Telegram bot: @{bot_info.get('username')}")
                return True
            else:
                print(f"✗ Telegram API error: {data.get('description')}")
                return False

        except requests.RequestException as e:
            print(f"✗ Connection failed: {str(e)}")
            return False
