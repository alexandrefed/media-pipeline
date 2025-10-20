"""Configuration management for notification system"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Manages configuration for the notification system"""

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager

        Args:
            config_path: Path to config file. If None, looks for config.yaml in notifications/config/
        """
        if config_path is None:
            # Default to notifications/config/config.yaml
            notifications_dir = Path(__file__).parent.parent.parent
            config_path = notifications_dir / "config" / "config.yaml"

        self.config_path = Path(config_path)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {self.config_path}\n"
                f"Please copy config.example.yaml to config.yaml and configure your settings."
            )

        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)

        # Validate required fields
        self._validate_config(config)

        return config

    def _validate_config(self, config: Dict[str, Any]) -> None:
        """Validate that required configuration fields are present"""
        required_fields = [
            ('telegram', 'bot_token'),
            ('telegram', 'chat_id')
        ]

        for *path, field in required_fields:
            current = config
            for key in path:
                if key not in current:
                    raise ValueError(f"Missing required config section: {key}")
                current = current[key]

            if field not in current or not current[field]:
                raise ValueError(
                    f"Missing required config field: {'.'.join([*path, field])}\n"
                    f"Please configure this in {self.config_path}"
                )

    @property
    def telegram_bot_token(self) -> str:
        """Get Telegram bot token"""
        return self.config['telegram']['bot_token']

    @property
    def telegram_chat_id(self) -> str:
        """Get Telegram chat ID"""
        return self.config['telegram']['chat_id']

    @property
    def immediate_notifications_enabled(self) -> bool:
        """Check if immediate notifications are enabled"""
        return self.config.get('notifications', {}).get('immediate', {}).get('enabled', True)

    @property
    def max_takeaways(self) -> int:
        """Get maximum number of takeaways to include"""
        return self.config.get('notifications', {}).get('immediate', {}).get('max_takeaways', 5)

    @property
    def weekly_digest_enabled(self) -> bool:
        """Check if weekly digest is enabled"""
        return self.config.get('notifications', {}).get('weekly_digest', {}).get('enabled', False)

    @property
    def spaced_repetition_enabled(self) -> bool:
        """Check if spaced repetition is enabled"""
        return self.config.get('notifications', {}).get('spaced_repetition', {}).get('enabled', False)

    def get(self, *path, default=None) -> Any:
        """
        Get configuration value by path

        Args:
            *path: Configuration path (e.g., 'telegram', 'bot_token')
            default: Default value if path doesn't exist

        Returns:
            Configuration value or default
        """
        current = self.config
        for key in path:
            if not isinstance(current, dict) or key not in current:
                return default
            current = current[key]
        return current
