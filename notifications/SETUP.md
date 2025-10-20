# Setup Guide - Knowledge Base Notification System

This guide walks you through setting up Telegram notifications for your knowledge base.

## Prerequisites

- Python 3.11+ with uv installed
- A Telegram account
- 5 minutes of your time

## Step 1: Create a Telegram Bot

1. **Open Telegram** and search for `@BotFather`

2. **Start a chat** with BotFather and send `/newbot`

3. **Follow the prompts**:
   - Choose a name for your bot (e.g., "My Knowledge Base Bot")
   - Choose a username (must end in 'bot', e.g., "my_kb_notifications_bot")

4. **Save your bot token**:
   ```
   Use this token to access the HTTP API:
   1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```
   **Keep this token secret!** Don't commit it to git.

5. **Optional: Set bot description**:
   ```
   /setdescription
   ```
   Then select your bot and enter:
   ```
   Sends rich notifications about processed videos in my knowledge base
   ```

## Step 2: Get Your Chat ID

You need to know where to send messages - either to yourself or a channel.

### Option A: Send to Yourself (Recommended for personal use)

1. **Search for `@userinfobot`** in Telegram

2. **Start a chat** and it will immediately send you your chat ID

3. **Save the number** (looks like: `123456789`)

### Option B: Send to a Channel

1. **Create a channel** in Telegram

2. **Add your bot as an administrator** to the channel:
   - Open channel settings
   - Click "Administrators"
   - Click "Add Administrator"
   - Search for your bot's username
   - Grant "Post Messages" permission

3. **Get the channel ID**:
   - Forward any message from the channel to `@userinfobot`
   - It will show you the channel ID (looks like: `-1001234567890`)
   - **Important**: Include the `-` sign!

## Step 3: Configure the Notification System

1. **Navigate to the notifications directory**:
   ```bash
   cd notifications/config
   ```

2. **Copy the example config**:
   ```bash
   cp config.example.yaml config.yaml
   ```

3. **Edit config.yaml**:
   ```bash
   # Open in your editor
   nano config.yaml
   # or
   code config.yaml
   ```

4. **Add your credentials**:
   ```yaml
   telegram:
     bot_token: "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"  # From Step 1
     chat_id: "123456789"  # From Step 2

   notifications:
     immediate:
       enabled: true  # Enable immediate notifications
       max_takeaways: 5
   ```

5. **Save and close** the file

## Step 4: Install Dependencies

```bash
# From the project root directory
uv add requests pyyaml

# Or if using pip
pip install requests pyyaml
```

## Step 5: Test the System

```bash
# Run the test script
uv run python notifications/scripts/test_notification.py
```

You should see:
```
==================================================
Testing Telegram Notification System
==================================================

1. Testing configuration...
   ✓ Configuration loaded successfully
   - Bot token: 1234567890...
   - Chat ID: 123456789
   - Immediate notifications: enabled

2. Testing Telegram bot connection...
   ✓ Connected to Telegram bot: @my_kb_notifications_bot
   ✓ Successfully connected to Telegram bot

3. Sending test message...
   ✓ Test message sent successfully
   - Message ID: 42

==================================================
All tests passed! 🎉
==================================================
```

**Check your Telegram** - you should receive a test message from your bot!

## Step 6: Send Your First Real Notification

```bash
# Send notification for an existing analysis
uv run python notifications/scripts/send_notification.py workspace/analysis/VZkm1jSs8Lg_analysis.json
```

You should see:
```
Loading configuration...
Loading analysis from: workspace/analysis/VZkm1jSs8Lg_analysis.json
✓ Detected content type: ai_tools
Formatting message...
Sending notification to Telegram...
✓ Notification sent successfully!
  - Message parts: 1
  - Content type: ai_tools
  - Video: Master Vibe Coding: The 5-Step Product Manager Framework
```

**Check Telegram** - you should see a rich, formatted notification!

## Step 7: Integrate into Workflow (Optional)

Add the notification step to your video processing workflows.

### For AI Tools Videos

Edit `.claude/commands/process-youtube.md` and add at the end:

```markdown
7. Send notification:
   uv run python notifications/scripts/send_notification.py workspace/analysis/{VIDEO_ID}_analysis.json
```

### For Sports Videos

Edit `.claude/commands/process-sports-video.md` and add at the end:

```markdown
7. Send notification:
   uv run python notifications/scripts/send_notification.py workspace/analysis/{VIDEO_ID}_sports_analysis.json
```

## Troubleshooting

### "Configuration file not found"

**Problem**: config.yaml doesn't exist

**Solution**:
```bash
cd notifications/config
cp config.example.yaml config.yaml
# Then edit config.yaml with your credentials
```

### "❌ Telegram API error: Unauthorized"

**Problem**: Invalid bot token

**Solutions**:
1. Check you copied the full token from BotFather
2. Make sure there are no extra spaces
3. The token should look like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### "❌ Telegram API error: Bad Request: chat not found"

**Problem**: Invalid chat ID

**Solutions**:
1. For personal messages: Use `@userinfobot` to get your correct chat ID
2. For channels: Make sure you added the bot as an administrator first
3. For channels: Include the `-` sign in the chat ID (e.g., `-1001234567890`)

### "❌ Telegram API error: Forbidden: bot was blocked by the user"

**Problem**: You blocked the bot

**Solution**: Go to Telegram, find the bot, and click "Start" or "Unblock"

### Bot sends message but formatting is broken

**Problem**: HTML parsing errors

**Solution**: Check your analysis JSON for special characters. The formatter should escape them automatically, but if issues persist, check `src/formatters/base_formatter.py`

### "ModuleNotFoundError: No module named 'yaml'"

**Problem**: Dependencies not installed

**Solution**:
```bash
uv add requests pyyaml
```

## Security Best Practices

1. **Never commit `config.yaml` to git**:
   ```bash
   # Add to .gitignore (already done)
   echo "notifications/config/config.yaml" >> .gitignore
   ```

2. **Use environment variables** for CI/CD:
   ```bash
   export TELEGRAM_BOT_TOKEN="your_token"
   export TELEGRAM_CHAT_ID="your_chat_id"
   ```

3. **Regenerate bot token** if accidentally exposed:
   - Message `@BotFather`
   - Send `/token`
   - Select your bot
   - Send `/revoke`

## Advanced Configuration

### Disable Immediate Notifications

Edit `config.yaml`:
```yaml
notifications:
  immediate:
    enabled: false  # Won't send after each video
```

### Change Number of Takeaways

Edit `config.yaml`:
```yaml
notifications:
  immediate:
    max_takeaways: 3  # Show only top 3 instead of 5
```

### Enable Weekly Digest (Coming Soon)

Edit `config.yaml`:
```yaml
notifications:
  weekly_digest:
    enabled: true
    day: "sunday"
    time: "19:00"
```

## Next Steps

1. **Process some videos** and watch the notifications arrive!

2. **Set up n8n workflows** for automated notifications (see `n8n/README.md`)

3. **Enable weekly digests** to get big-picture synthesis

4. **Set up spaced repetition** for long-term retention

## Getting Help

- **Configuration issues**: Review this guide, check `config.example.yaml`
- **Format issues**: Check `src/formatters/` code
- **Testing**: Run `test_notification.py` to isolate problems
- **Telegram API docs**: https://core.telegram.org/bots/api

---

**Pro tip**: After setup, you can test with different analysis files to see how AI tools vs Sports notifications look different!

```bash
# Test with AI tools content
uv run python notifications/scripts/send_notification.py workspace/analysis/VZkm1jSs8Lg_analysis.json

# Test with Sports content
uv run python notifications/scripts/send_notification.py workspace/analysis/lIojfAWU9FA_sports_analysis.json
```
