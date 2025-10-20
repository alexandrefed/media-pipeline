# Quick Reference - Notification System

## Common Commands

### Setup
```bash
# Install dependencies
uv sync

# Create config from template
cp notifications/config/config.example.yaml notifications/config/config.yaml

# Test the system
uv run python notifications/scripts/test_notification.py
```

### Send Notifications
```bash
# Send notification for a video
uv run python notifications/scripts/send_notification.py workspace/analysis/VIDEO_ID_analysis.json

# Examples
uv run python notifications/scripts/send_notification.py workspace/analysis/VZkm1jSs8Lg_analysis.json
uv run python notifications/scripts/send_notification.py workspace/analysis/lIojfAWU9FA_sports_analysis.json
```

### Telegram Bot Commands

| Task | Command |
|------|---------|
| Create bot | Message `@BotFather` → `/newbot` |
| Get your chat ID | Message `@userinfobot` |
| Set bot description | `/setdescription` to @BotFather |
| Revoke token (if leaked) | `/token` → select bot → `/revoke` |

## Message Format Examples

### AI Tools Notification
```
🎬 NEW VIDEO PROCESSED

Master Vibe Coding: The 5-Step Product Manager Framework
📺 Sean Kochel | ⏱️ 30 minutes

Executive Summary:
The core problem isn't bad prompts - it's lack of systematic planning...

🔑 Top Takeaways:
1. Create North Star document as decision lens
2. Write detailed user stories BEFORE building
3. Use 'anti-yes-man' prompting to surface unknowns
4. Specificity principle: Build for everyone = build for no one
5. Plan functional AND non-functional requirements explicitly

🛠️ Tools Mentioned:
Claude Code, Cursor, Windsurf, Gemini CLI, Linear

💭 Key Concepts:
5-Step Product Manager Framework, Vibe Coding Planning Process, ...

💡 Key Insight:
Problems emerge when you're 75% done building - systematic planning prevents costly rework

Tags: vibe-coding, product-management, ai-tools
Watch Video
```

### Sports Science Notification
```
🏋️ NEW SPORTS SCIENCE PROCESSED

What Weighted Vests do to your Body: New Evidence!
📺 Physionic | ⏱️ 8 minutes

Executive Summary:
Pilot study shows weighted vests preserve metabolism during weight loss...

🔬 Evidence Quality: Tier 2 (RCT)

🔑 Key Findings:
1. Preserved RMR while controls lost >200 cal/day
2. Benefits persist 18 months after stopping use
3. Gravistat hypothesis: bone cells sense loading, regulate metabolism
4. Feasible even for osteoarthritis patients
5. Passive intervention - wear during daily activities

📊 Protocol:
• Volume: Six-month active intervention wearing weighted vest...
• Frequency: Regular wearing pattern needed for consistent...
• Intensity: Load should be sufficient for osteocyte mechanical sensing...

🎯 WHY It Works:
When body mass decreases, reduced gravitational load on skeleton triggers bone-mediated hunger/metabolism signaling. Weighted vests maintain this load signal...

Tags: weight-loss, metabolism, exercise-physiology
Watch Video
```

## Configuration Reference

### config.yaml Structure
```yaml
telegram:
  bot_token: "YOUR_BOT_TOKEN"  # From @BotFather
  chat_id: "YOUR_CHAT_ID"      # From @userinfobot

notifications:
  immediate:
    enabled: true               # Send after each video
    max_takeaways: 5           # Number of key points

  weekly_digest:
    enabled: false             # Weekly summary
    day: "sunday"
    time: "19:00"

  spaced_repetition:
    enabled: false             # Daily reminders
    daily_time: "09:00"
```

## File Structure
```
notifications/
├── README.md                   # Main documentation
├── SETUP.md                    # Setup guide
├── QUICK_REFERENCE.md         # This file
├── config/
│   ├── config.example.yaml    # Template
│   └── config.yaml            # Your config (not in git)
├── src/
│   ├── core/
│   │   ├── telegram_client.py # Telegram API wrapper
│   │   └── config_manager.py  # Config handling
│   ├── formatters/
│   │   ├── ai_tools_formatter.py
│   │   └── sports_formatter.py
│   └── utils/
│       └── json_parser.py
├── scripts/
│   ├── send_notification.py   # Main CLI tool
│   └── test_notification.py   # Test script
└── n8n/
    └── README.md              # n8n integration
```

## Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| Config not found | `cp notifications/config/config.example.yaml notifications/config/config.yaml` |
| Unauthorized error | Check bot token in config.yaml |
| Chat not found | Use @userinfobot to get correct chat ID |
| Bot blocked | Unblock bot in Telegram |
| Module not found | `uv sync` or `uv add requests pyyaml` |
| Formatting broken | Check analysis JSON structure |

## Python API Usage

```python
from notifications.src.core.telegram_client import TelegramNotifier
from notifications.src.formatters.ai_tools_formatter import AIToolsFormatter
from notifications.src.utils.json_parser import load_analysis_json

# Load analysis
analysis = load_analysis_json('path/to/analysis.json')

# Format message
formatter = AIToolsFormatter(max_takeaways=5)
message = formatter.format(analysis)

# Send notification
notifier = TelegramNotifier()
result = notifier.send(message)
```

## HTML Formatting Reference

The system uses HTML formatting for reliability:

```html
<b>Bold text</b>
<i>Italic text</i>
<u>Underline</u>
<s>Strikethrough</s>
<a href="url">Link</a>
<code>Monospace</code>
<pre>Preformatted block</pre>
```

**Important**: Special characters (`<`, `>`, `&`) are automatically escaped.

## Next Steps After Setup

1. **Process a video**: Use `/process-youtube` or `/process-sports-video`
2. **Send notification**: `uv run python notifications/scripts/send_notification.py path/to/analysis.json`
3. **Check Telegram**: You should receive a rich notification
4. **Set up n8n**: See `n8n/README.md` for automated workflows
5. **Enable weekly digest**: Edit `config.yaml` when ready
6. **Add spaced repetition**: Edit `config.yaml` for long-term retention

## Tips

- **Test first**: Always run `test_notification.py` after config changes
- **Check JSON**: Ensure analysis files are valid before sending
- **Rate limits**: Telegram allows ~30 messages/second
- **Long messages**: Automatically split if > 4096 characters
- **Security**: Never commit `config.yaml` to git
- **Multiple channels**: Use different configs for different topics

## Getting Help

- **Setup issues**: See [SETUP.md](SETUP.md)
- **n8n integration**: See [n8n/README.md](n8n/README.md)
- **Telegram API**: https://core.telegram.org/bots/api
- **Test with examples**: Use existing analysis JSONs in `workspace/analysis/`
