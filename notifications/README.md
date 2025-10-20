# Knowledge Base Notification System

A professional notification system for consuming knowledge base content through rich Telegram messages, weekly digests, and spaced repetition.

## The Problem

You're building an amazing knowledge base by processing YouTube videos, but you're not actually consuming the content. This system solves that by delivering knowledge directly to you in digestible, valuable formats.

## Features

### 🔔 Immediate Rich Notifications
- **Triggered**: After each video is processed
- **Platform**: Telegram (HTML formatted)
- **Content**: Title, summary, top 5 takeaways, tools/protocols, key insights
- **Value**: Learn without watching the video - notifications are self-contained

### 📊 Weekly Synthesis Digest (Coming Soon)
- **Triggered**: Every Sunday evening
- **Platform**: Telegram or Email
- **Content**: Cross-cutting themes, patterns across multiple videos
- **Value**: Big-picture synthesis and connections

### 🔄 Spaced Repetition (Coming Soon)
- **Triggered**: Daily at your chosen time
- **Platform**: Telegram
- **Content**: Insights from 1 week, 1 month, and 3 months ago
- **Value**: Long-term retention through scientifically-proven spaced repetition

## Quick Start

```bash
# 1. Set up Telegram bot (see SETUP.md)

# 2. Configure your bot token
cp notifications/config/config.example.yaml notifications/config/config.yaml
# Edit config.yaml with your bot token and chat ID

# 3. Test the notification system
uv run python notifications/scripts/test_notification.py

# 4. Send notification for a processed video
uv run python notifications/scripts/send_notification.py workspace/analysis/VIDEO_ID_analysis.json
```

## Architecture

```
notifications/
├── src/
│   ├── core/              # Core notification engine
│   ├── formatters/        # Message formatters (AI tools, Sports)
│   └── utils/             # Helper utilities
├── scripts/               # CLI tools
├── n8n/                   # n8n workflow templates
├── config/                # Configuration files
└── examples/              # Example outputs
```

## Integration Points

### 1. Python CLI
```bash
# Send notification after processing
uv run python notifications/scripts/send_notification.py path/to/analysis.json
```

### 2. n8n Workflows
- Pre-built workflow templates in `n8n/workflows/`
- Automatic notifications on file creation
- Weekly digest aggregation
- Spaced repetition scheduler

### 3. Direct Integration
```python
from notifications.src.core.telegram_client import TelegramNotifier
from notifications.src.formatters.ai_tools_formatter import AIToolsFormatter

notifier = TelegramNotifier()
formatter = AIToolsFormatter()
message = formatter.format(analysis_data)
notifier.send(message)
```

## Configuration

All configuration is managed through `config/config.yaml`:

```yaml
telegram:
  bot_token: "YOUR_BOT_TOKEN"
  chat_id: "YOUR_CHAT_ID"

notifications:
  immediate:
    enabled: true
    max_takeaways: 5
  weekly_digest:
    enabled: false
    day: "sunday"
    time: "19:00"
  spaced_repetition:
    enabled: false
    daily_time: "09:00"
```

## Message Examples

### AI Tools Video
```
🎬 NEW VIDEO PROCESSED

Master Vibe Coding: The 5-Step Product Manager Framework
📺 Sean Kochel | ⏱️ 30 minutes

Executive Summary:
The core problem isn't bad prompts - it's lack of systematic planning...

🔑 Top 5 Takeaways:
1. Create North Star document as decision lens
2. Write detailed user stories BEFORE building
...
```

### Sports Video
```
🏋️ NEW SPORTS SCIENCE PROCESSED

What Weighted Vests do to your Body: New Evidence!
📺 Physionic | ⏱️ 8 minutes

Executive Summary:
Pilot study shows weighted vests preserve metabolism during weight loss...

🔬 Evidence Tier: 2 (Pilot RCT)
...
```

## Documentation

- **[SETUP.md](SETUP.md)** - Complete setup guide for Telegram bot and configuration
- **[n8n/README.md](n8n/README.md)** - n8n workflow integration guide
- **[examples/](examples/)** - Example analysis JSONs and output messages

## Requirements

```bash
# Install dependencies
uv add requests pyyaml

# Or using pip
pip install requests pyyaml
```

## Future Enhancements

- [ ] Email digest support
- [ ] Notion page creation integration
- [ ] Google Sheets tracking dashboard
- [ ] Slack integration
- [ ] Discord bot support
- [ ] Custom AI-generated summaries
- [ ] Voice message summaries (Telegram voice notes)

## Support

For issues or questions:
1. Check [SETUP.md](SETUP.md) for configuration help
2. Review [n8n/README.md](n8n/README.md) for workflow integration
3. Test with example files in `examples/`

---

**Version**: 1.0
**Last Updated**: January 2025
**Maintained by**: AI Knowledge Base Project
