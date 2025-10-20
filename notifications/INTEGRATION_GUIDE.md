# Integration Guide - Adding Notifications to Your Workflow

This guide shows how to integrate the notification system into your existing video processing workflow.

## Overview

The notification system can be integrated at three levels:

1. **Manual**: Call the script after processing each video
2. **Semi-Automated**: Add to slash commands
3. **Fully Automated**: Use n8n to trigger automatically

## Option 1: Manual Integration (Start Here)

After processing a video, manually send the notification:

```bash
# 1. Process video
/process-youtube
# ... or ...
/process-sports-video

# 2. Send notification
uv run python notifications/scripts/send_notification.py workspace/analysis/VIDEO_ID_analysis.json
```

**Pros**: Simple, explicit control
**Cons**: Easy to forget

## Option 2: Integrate into Slash Commands

### Modify `/process-youtube` Command

Edit `.claude/commands/process-youtube.md`:

```markdown
---
name: process-youtube
description: Process YouTube video through streamlined pipeline with notification
---

Process a YouTube video through the complete AI tools pipeline:

1. Extract & auto-enhance transcript
2. Analyze with @youtube-transcript-analyzer
3. Generate detailed summary
4. Store in MCP KB Memory
5. **Send Telegram notification**
6. Clean context with /compact

After each step completes successfully, provide clear instructions for the next step.

**Important**: Always wait for user confirmation before proceeding to next step.

## Step 5: Send Notification

After successfully storing in MCP KB, send notification:

```bash
uv run python notifications/scripts/send_notification.py workspace/analysis/{VIDEO_ID}_analysis.json
```

This sends a rich formatted message to your Telegram with:
- Video title, channel, duration
- Executive summary
- Top 5 key takeaways
- Tools mentioned and key concepts
- Link to full analysis

**Check your Telegram** to see the notification!
```

### Modify `/process-sports-video` Command

Similar changes to `.claude/commands/process-sports-video.md`:

```markdown
## Step 5: Send Notification

After successfully storing in MCP KB, send notification:

```bash
uv run python notifications/scripts/send_notification.py workspace/analysis/{VIDEO_ID}_sports_analysis.json
```

This sends a rich formatted message with:
- Video title, channel, duration
- Executive summary
- Evidence tier (1-4)
- Top 5 key findings
- Protocol details (volume, frequency, intensity)
- WHY reasoning (biomechanical/physiological)
- Link to full analysis

**Check your Telegram** to see the sports science notification!
```

**Pros**: Integrated into workflow, hard to miss
**Cons**: Still requires manual execution

## Option 3: Automated with Python Script

Create a wrapper script that does everything:

`scripts/process_and_notify.py`:

```python
#!/usr/bin/env python3
"""
Process video and automatically send notification

Usage:
    python scripts/process_and_notify.py <youtube_url>
"""

import sys
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/process_and_notify.py <youtube_url>")
        sys.exit(1)

    youtube_url = sys.argv[1]

    # Extract video ID
    if 'v=' in youtube_url:
        video_id = youtube_url.split('v=')[1].split('&')[0]
    else:
        video_id = youtube_url.split('/')[-1]

    print(f"Processing video: {video_id}")

    # 1. Extract and enhance
    result = subprocess.run([
        'uv', 'run', 'python', 'main.py', 'streamlined', youtube_url
    ])

    if result.returncode != 0:
        print("Failed to extract/enhance transcript")
        sys.exit(1)

    # 2. Prompt for manual analysis
    print("\n" + "="*50)
    print("Next: Run the analyzer agent")
    print("="*50)
    print(f"claude \"Use @youtube-transcript-analyzer to analyze workspace/transcripts/enhanced/raw_text_for_enhancement_{video_id}_auto_enhanced.txt and save to workspace/analysis/{video_id}_analysis.json\"")
    print("\nPress Enter after analysis is complete...")
    input()

    # 3. Check if analysis exists
    analysis_path = Path(f"workspace/analysis/{video_id}_analysis.json")
    if not analysis_path.exists():
        print(f"Analysis file not found: {analysis_path}")
        sys.exit(1)

    # 4. Send notification
    print("\nSending notification...")
    result = subprocess.run([
        'uv', 'run', 'python',
        'notifications/scripts/send_notification.py',
        str(analysis_path)
    ])

    if result.returncode == 0:
        print("\n✓ Video processed and notification sent!")
    else:
        print("\n✗ Notification failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

**Usage**:
```bash
chmod +x scripts/process_and_notify.py
uv run python scripts/process_and_notify.py "https://youtube.com/watch?v=VIDEO_ID"
```

**Pros**: One command for everything
**Cons**: Still requires manual analyzer step

## Option 4: Fully Automated with n8n (Recommended for Scale)

See `n8n/README.md` for complete n8n integration.

**Basic Workflow**:

1. **File Watcher**: n8n watches `workspace/analysis/` for new JSON files
2. **Auto-Trigger**: When new file appears, n8n automatically calls notification script
3. **Result**: Notification sent within seconds of processing

**Setup**:

```json
{
  "nodes": [
    {
      "name": "Watch Analysis Folder",
      "type": "n8n-nodes-base.fileSystemTrigger",
      "parameters": {
        "path": "workspace/analysis",
        "event": "create",
        "include": "**/*_analysis.json"
      }
    },
    {
      "name": "Send Notification",
      "type": "n8n-nodes-base.executeCommand",
      "parameters": {
        "command": "uv run python notifications/scripts/send_notification.py {{ $json.path }}"
      }
    }
  ]
}
```

**Pros**: Completely automated, never forget
**Cons**: Requires n8n setup

## Workflow Comparison

| Method | Effort | Automation | Best For |
|--------|--------|------------|----------|
| Manual | Low setup, manual execution | None | Testing, occasional use |
| Slash Commands | Medium setup, manual execution | Partial | Regular use, learning |
| Python Wrapper | Medium setup, semi-auto | Medium | Batch processing |
| n8n Workflows | High setup, fully auto | Full | Production, scale |

## Recommended Path

1. **Week 1**: Start with manual integration
   - Process 2-3 videos manually
   - Get comfortable with the notification format
   - Adjust `max_takeaways` in config if needed

2. **Week 2**: Integrate into slash commands
   - Update `/process-youtube` and `/process-sports-video`
   - Make notifications part of your normal workflow
   - Build the habit

3. **Week 3**: Add n8n automation
   - Install n8n MCP
   - Set up file watcher workflow
   - Let automation handle notifications

4. **Week 4**: Enable advanced features
   - Weekly digest on Sundays
   - Spaced repetition for retention
   - Google Sheets tracking

## Testing the Integration

Before going live, test with existing analysis files:

```bash
# Test with AI tools content
uv run python notifications/scripts/send_notification.py \
    workspace/analysis/VZkm1jSs8Lg_analysis.json

# Test with Sports content
uv run python notifications/scripts/send_notification.py \
    workspace/analysis/lIojfAWU9FA_sports_analysis.json

# Verify formatting looks good in Telegram
# Adjust max_takeaways in config.yaml if needed
```

## Customization Options

### Change Notification Verbosity

Edit `config.yaml`:

```yaml
notifications:
  immediate:
    max_takeaways: 3  # Show fewer takeaways (default: 5)
```

### Filter by Content Type

Only send notifications for specific content types:

```python
# Modify scripts/send_notification.py

content_type = detect_content_type(analysis)

# Only send for AI tools
if content_type != 'ai_tools':
    print("Skipping notification for non-AI-tools content")
    sys.exit(0)
```

### Send to Multiple Channels

Create different configs for different topics:

```bash
# config_ai_tools.yaml - AI tools channel
# config_sports.yaml - Sports science channel

# Send to appropriate channel
if content_type == 'sports':
    config = ConfigManager('notifications/config/config_sports.yaml')
else:
    config = ConfigManager('notifications/config/config_ai_tools.yaml')
```

## Monitoring and Analytics

Track notifications in Google Sheets:

| Timestamp | Video ID | Title | Channel | Type | Sent | Read |
|-----------|----------|-------|---------|------|------|------|
| 2025-01-15 10:30 | VZkm1jSs8Lg | Master Vibe Coding | Sean Kochel | ai_tools | ✓ | ✓ |

Add to n8n workflow:

```json
{
  "name": "Log to Sheets",
  "type": "n8n-nodes-base.googleSheets",
  "parameters": {
    "operation": "append",
    "range": "Notifications!A:G",
    "values": "={{ $json }}"
  }
}
```

## Troubleshooting Integration

### Notification Not Sent

**Check**:
1. Is `immediate.enabled: true` in config.yaml?
2. Did the analysis file get created?
3. Does the file path match exactly?
4. Run test_notification.py to verify bot works

### Wrong Formatter Used

**Check**:
- Analysis JSON has correct fields for detection
- For sports: Must have `sport_discipline`, `biomechanical_principles`, etc.
- For AI tools: Must have `tools_mentioned`, `commands`, etc.

### Rate Limiting

If processing many videos:
- Telegram allows ~30 messages/second
- Add delays between notifications
- Use weekly digest instead

## Next Steps

1. Choose your integration method
2. Test with existing videos
3. Process new videos with notifications enabled
4. Review notification quality
5. Adjust config as needed
6. Scale up with n8n if needed

---

**Remember**: The goal is to make you actually **consume** the knowledge you're building, not just archive it. The notifications should be valuable enough to read without watching the video!
