# n8n Integration Guide

This guide shows you how to integrate the notification system with n8n for automated workflows.

## Overview

Once you have n8n MCP installed, you can create powerful automated workflows:

1. **Immediate Notifications**: Auto-send when new analysis files are created
2. **Weekly Digest**: Aggregate all videos from the week
3. **Spaced Repetition**: Resurface insights at optimal intervals

## Prerequisites

- n8n installed and running
- n8n MCP server configured in Claude Code
- Telegram bot set up (see ../SETUP.md)
- Knowledge of n8n basics

## Workflow Templates

### 1. Immediate Notification Workflow

**Trigger**: When a new analysis JSON is created in `workspace/analysis/`

**Steps**:
1. **File Created Trigger** - Watch for new JSON files
2. **Read File** - Get the analysis content
3. **Python Script** - Run send_notification.py
4. **Telegram Node** - Send formatted message

**Implementation**:

```json
{
  "name": "Immediate Video Notification",
  "nodes": [
    {
      "parameters": {
        "path": "workspace/analysis",
        "event": "create",
        "options": {
          "depth": 1
        }
      },
      "name": "Watch for New Analysis",
      "type": "n8n-nodes-base.fileSystemTrigger"
    },
    {
      "parameters": {
        "command": "uv run python notifications/scripts/send_notification.py {{ $json.path }}"
      },
      "name": "Send Notification",
      "type": "n8n-nodes-base.executeCommand"
    }
  ]
}
```

**Alternative**: Call the Python API directly from n8n

```json
{
  "parameters": {
    "language": "python3",
    "code": "import sys\nsys.path.insert(0, 'notifications/src')\n\nfrom core.telegram_client import TelegramNotifier\nfrom formatters.ai_tools_formatter import AIToolsFormatter\nimport json\n\n# Get analysis from n8n\nanalysis = json.loads($input.json.body)\n\n# Format and send\nformatter = AIToolsFormatter()\nmessage = formatter.format(analysis)\nnotifier = TelegramNotifier()\nnotifier.send(message)\n\nreturn {'sent': True}"
  },
  "name": "Send via Python API",
  "type": "n8n-nodes-base.python"
}
```

### 2. Weekly Digest Workflow

**Trigger**: Every Sunday at 7 PM

**Steps**:
1. **Schedule Trigger** - Weekly on Sunday
2. **List Files** - Get all analysis files from past week
3. **Aggregate Insights** - Collect key takeaways
4. **Format Digest** - Create summary message
5. **Send to Telegram** - Deliver digest

**Implementation**:

```python
# n8n Python node - Aggregate weekly insights

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, 'notifications/src')

# Get files from last 7 days
workspace = Path('workspace/analysis')
one_week_ago = datetime.now() - timedelta(days=7)

analyses = []
for file in workspace.glob('*_analysis.json'):
    if file.stat().st_mtime > one_week_ago.timestamp():
        with open(file) as f:
            analyses.append(json.load(f))

# Build digest
digest = f"📊 <b>WEEKLY KNOWLEDGE DIGEST</b>\n\n"
digest += f"<b>Videos Processed This Week:</b> {len(analyses)}\n\n"

for analysis in analyses:
    title = analysis.get('title', 'Unknown')
    channel = analysis.get('channel', 'Unknown')
    digest += f"• <b>{title}</b> ({channel})\n"

digest += "\n<b>🔥 Top Insights:</b>\n"

# Collect all takeaways
all_takeaways = []
for analysis in analyses:
    all_takeaways.extend(analysis.get('key_takeaways', [])[:2])

# Show top 10
for i, takeaway in enumerate(all_takeaways[:10], 1):
    if len(takeaway) > 150:
        takeaway = takeaway[:147] + "..."
    digest += f"{i}. {takeaway}\n"

return {'digest': digest}
```

### 3. Spaced Repetition Workflow

**Trigger**: Daily at 9 AM

**Steps**:
1. **Schedule Trigger** - Daily
2. **Query Database** - Get insights from 1 week, 1 month, 3 months ago
3. **Select Random Insights** - One from each time period
4. **Format Message** - Create reminder
5. **Send to Telegram** - Deliver reminder

**Implementation**:

```python
# n8n Python node - Spaced repetition

import sys
import json
import random
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, 'notifications/src')

# Time periods for spaced repetition
intervals = [
    (7, "1 week ago"),
    (30, "1 month ago"),
    (90, "3 months ago")
]

workspace = Path('workspace/analysis')
insights_by_period = {label: [] for _, label in intervals}

# Collect insights from each time period
for days, label in intervals:
    target_date = datetime.now() - timedelta(days=days)

    for file in workspace.glob('*_analysis.json'):
        file_date = datetime.fromtimestamp(file.stat().st_mtime)

        # Within 3 days of target
        if abs((file_date - target_date).days) <= 3:
            with open(file) as f:
                analysis = json.load(f)
                takeaways = analysis.get('key_takeaways', [])
                if takeaways:
                    insights_by_period[label].append({
                        'insight': random.choice(takeaways),
                        'title': analysis.get('title'),
                        'channel': analysis.get('channel')
                    })

# Build spaced repetition message
message = "🔄 <b>DAILY KNOWLEDGE REMINDER</b>\n\n"

for _, label in intervals:
    insights = insights_by_period[label]
    if insights:
        item = random.choice(insights)
        message += f"<b>From {label}:</b>\n"
        message += f"<i>{item['title']}</i> ({item['channel']})\n\n"
        message += f"{item['insight']}\n\n"

return {'message': message}
```

## Google Sheets Integration

Track all notifications and insights in Google Sheets for analytics.

**Workflow**: After sending notification, log to sheets

```json
{
  "parameters": {
    "operation": "append",
    "sheetId": "YOUR_SHEET_ID",
    "range": "Notifications!A:E",
    "values": {
      "timestamp": "={{ $now }}",
      "video_id": "={{ $json.video_id }}",
      "title": "={{ $json.title }}",
      "channel": "={{ $json.channel }}",
      "content_type": "={{ $json.content_type }}"
    }
  },
  "name": "Log to Google Sheets",
  "type": "n8n-nodes-base.googleSheets"
}
```

**Sheet Structure**:

| Timestamp | Video ID | Title | Channel | Content Type | Sent |
|-----------|----------|-------|---------|--------------|------|
| 2025-01-15 10:30 | VZkm1jSs8Lg | Master Vibe Coding | Sean Kochel | ai_tools | ✓ |

## Advanced: Smart Notification Routing

Send different content types to different channels:

```python
# n8n Python node - Smart routing

import sys
sys.path.insert(0, 'notifications/src')

from core.telegram_client import TelegramNotifier
from core.config_manager import ConfigManager
from utils.json_parser import detect_content_type

analysis = $input.json.body

content_type = detect_content_type(analysis)

# Route to different channels
config = ConfigManager()

if content_type == 'sports':
    config.config['telegram']['chat_id'] = 'SPORTS_CHANNEL_ID'
else:
    config.config['telegram']['chat_id'] = 'AI_TOOLS_CHANNEL_ID'

# Send to appropriate channel
notifier = TelegramNotifier(config)
# ... format and send
```

## Webhook Integration

Trigger workflows from external sources (e.g., when video is added to playlist):

```json
{
  "parameters": {
    "httpMethod": "POST",
    "path": "video-processed",
    "responseMode": "responseNode"
  },
  "name": "Webhook Trigger",
  "type": "n8n-nodes-base.webhook"
}
```

**Trigger from Python**:

```python
import requests

requests.post('http://localhost:5678/webhook/video-processed', json={
    'video_id': 'VZkm1jSs8Lg',
    'analysis_path': 'workspace/analysis/VZkm1jSs8Lg_analysis.json'
})
```

## Error Handling

Add error handlers to your workflows:

```json
{
  "parameters": {
    "rules": {
      "values": [
        {
          "conditions": {
            "string": [
              {
                "value1": "={{ $json.error }}",
                "operation": "isNotEmpty"
              }
            ]
          },
          "renameOutput": true,
          "outputKey": "hasError"
        }
      ]
    }
  },
  "name": "Check for Errors",
  "type": "n8n-nodes-base.switch"
}
```

## Testing Workflows

1. **Create test analysis file**:
   ```bash
   cp workspace/analysis/VZkm1jSs8Lg_analysis.json workspace/analysis/test_analysis.json
   ```

2. **Manually trigger workflow** in n8n

3. **Check Telegram** for notification

4. **Delete test file**:
   ```bash
   rm workspace/analysis/test_analysis.json
   ```

## Best Practices

1. **Use error notifications**: Send yourself a message if workflow fails
2. **Log all operations**: Track what was sent and when
3. **Rate limiting**: Don't send more than 30 messages/second to Telegram
4. **Idempotency**: Track sent notifications to avoid duplicates
5. **Graceful degradation**: If Telegram fails, log locally

## Troubleshooting

### Workflow doesn't trigger

- Check file watcher path is correct
- Ensure n8n has permission to read workspace directory
- Verify workflow is activated

### Python script fails in n8n

- Check Python path in n8n settings
- Ensure dependencies are installed in n8n's Python environment
- Check logs: n8n → Executions → View error

### Messages not formatted correctly

- Test formatter separately with `send_notification.py`
- Check JSON structure matches expected format
- Validate HTML escaping is working

## Next Steps

1. Install n8n MCP server
2. Import workflow templates
3. Configure triggers and schedules
4. Test with example data
5. Monitor and refine

---

**Want more examples?** Check the `workflows/` directory for complete workflow JSON files you can import directly into n8n.
