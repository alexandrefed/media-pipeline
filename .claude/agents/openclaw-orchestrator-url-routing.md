# OpenClaw Orchestrator URL Routing Reference

Reference document for configuring OpenClaw's Telegram intake and URL routing to the media-ingestion-agent. Apply these configurations on gaming-PC.

---

## Section 1: Telegram Plugin Configuration

Merge the following into `~/.openclaw/openclaw.json` on gaming-PC.

### Channels Configuration

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "8787779137:AAG30OrHeNtOhYapX0P6fDkO0yXwr7CfEus",
      "dmPolicy": "allowlist",
      "allowFrom": ["6616332223"],
      "capabilities": {
        "inlineButtons": "dm"
      }
    }
  }
}
```

### Plugins Configuration

Ensure `"telegram"` is in the `plugins.allow` array:

```json
{
  "plugins": {
    "allow": ["telegram"]
  }
}
```

### Configuration Notes

- **botToken**: From BotFather for @vecia_media_pipeline_bot
- **dmPolicy**: `"allowlist"` restricts the bot to only respond to approved user IDs
- **allowFrom**: Alexandre's Telegram user ID (`6616332223`). Add additional user IDs as strings to this array if needed.
- **inlineButtons**: `"dm"` enables inline keyboard buttons in direct messages (used for future spaced-repetition feedback buttons: Done/Not Relevant/Remind Later)

### Getting a Telegram User ID (if needed for new users)

1. Have the user send any message to the bot
2. Run `openclaw logs --follow` on gaming-PC
3. Look for the `from.id` field in the incoming message log entry
4. Add the numeric ID as a string to the `allowFrom` array

---

## Section 2: SOUL.md URL Detection and Routing Rules

Add the following section to the orchestrator's SOUL.md file on gaming-PC. This instructs the orchestrator to detect media URLs and dispatch them to the media-ingestion-agent via sessions_spawn.

### Text to Add to SOUL.md

```markdown
## URL Processing Rules

When a message contains a URL matching any of these supported platforms, follow the dispatch protocol below. Do NOT process the URL yourself.

### Supported Platform URL Patterns

| Platform   | URL Patterns                                                     |
|------------|------------------------------------------------------------------|
| YouTube    | `youtube.com/watch`, `youtu.be/`, `youtube.com/shorts/`         |
| Instagram  | `instagram.com/reel/`, `instagram.com/p/`                       |
| Facebook   | `fb.watch/`                                                      |
| Vimeo      | `vimeo.com/`                                                     |
| TikTok     | `tiktok.com/`                                                    |
| X (Twitter)| `x.com/` with `/status/` (video posts)                          |

### Dispatch Protocol

**Step 1 -- Acknowledge immediately:**
Reply to the user within 5 seconds:
> Processing: [URL] ([platform detected])

Example: "Processing: https://youtube.com/watch?v=abc123 (YouTube)"

**Step 2 -- Spawn media agent:**
Call sessions_spawn to delegate processing to the media-ingestion-agent:

sessions_spawn({
  task: "Process this [PLATFORM] URL: [URL]. Extract transcript, analyze content, store to all targets (unified-memory, Notion, Obsidian, Neo4j, pgvector), then announce completion summary back to the user.",
  agentId: "media",
  label: "media-[VIDEO_ID]",
  runTimeoutSeconds: 900
})

Replace [PLATFORM] with the detected platform name (YouTube, Instagram, TikTok, Vimeo, X).
Replace [URL] with the full URL from the message.
Replace [VIDEO_ID] with the video/post identifier extracted from the URL (e.g., the v= parameter for YouTube, the shortcode for Instagram).

**Step 3 -- Do NOT process the URL yourself.**
The media agent handles everything: extraction, enhancement, analysis, storage, and Telegram confirmation. Your only job is acknowledgement and dispatch.

### Platform Detection Rules

Apply these rules to determine the platform from the URL:

- Contains `youtube.com` or `youtu.be` --> **YouTube**
- Contains `instagram.com` --> **Instagram**
- Contains `fb.watch` --> **Facebook** (treat as Instagram pipeline)
- Contains `vimeo.com` --> **Vimeo**
- Contains `tiktok.com` --> **TikTok**
- Contains `x.com` AND contains `/status/` --> **X**

### Unsupported URLs

If the message contains a URL that does NOT match any supported platform above (e.g., reddit.com, medium.com, linkedin.com):

Reply: "Unsupported platform. Supported: YouTube, Instagram, TikTok, Vimeo, X"

Do NOT call sessions_spawn for unsupported URLs.

### Non-URL Messages

If the message does NOT contain any URL: handle it normally using your standard conversation behavior. Do NOT route non-URL messages to the media agent.

### Multiple URLs in One Message

If a message contains multiple URLs, process each one separately:
1. Acknowledge all URLs in a single reply: "Processing 3 URLs: [URL1] (YouTube), [URL2] (Instagram), [URL3] (TikTok)"
2. Call sessions_spawn once per URL with separate labels
```

---

## Section 3: Setup Steps (Gaming-PC)

Run these commands on gaming-PC via SSH.

### Step 1: Locate the orchestrator SOUL.md

```bash
find ~/.openclaw/agents/ -name "SOUL.md" -type f
```

Identify the orchestrator's SOUL.md (likely at `~/.openclaw/agents/<orchestrator-id>/SOUL.md` or similar).

### Step 2: Edit openclaw.json with Telegram config

```bash
# Open the OpenClaw config for editing
nano ~/.openclaw/openclaw.json
```

Merge the JSON from Section 1 into the existing config. If `channels` or `plugins` keys already exist, merge the sub-keys rather than replacing the entire object.

### Step 3: Add URL routing rules to SOUL.md

```bash
# Open the orchestrator SOUL.md
nano <path-from-step-1>
```

Append the entire content from Section 2 ("## URL Processing Rules" through the end of "### Multiple URLs in One Message") to the SOUL.md file.

### Step 4: Restart OpenClaw

```bash
openclaw restart
```

Wait for the restart to complete. Verify with:

```bash
openclaw status
```

### Step 5: Test with a YouTube URL

Send a YouTube URL to @vecia_media_pipeline_bot on Telegram:
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

**Expected:** Bot replies "Processing: https://www.youtube.com/watch?v=dQw4w9WgXcQ (YouTube)" within 5 seconds, then sessions_spawn dispatches to media agent.

### Step 6: Test with a non-URL message

Send a normal text message to the bot:
```
Hello, what can you do?
```

**Expected:** Bot responds conversationally (normal orchestrator behavior). Does NOT route to media agent.

### Step 7: Test with an unsupported URL

Send an unsupported platform URL:
```
https://www.reddit.com/r/programming/comments/abc123
```

**Expected:** Bot replies "Unsupported platform. Supported: YouTube, Instagram, TikTok, Vimeo, X"

### Step 8: Verify Telegram user ID in logs (if needed)

```bash
openclaw logs --follow
```

Send a message to the bot and look for the `from.id` field. Confirm it matches `6616332223`.

---

## Troubleshooting

### Bot not responding to messages
- Check `openclaw status` -- ensure gateway is running
- Verify `"telegram"` is in `plugins.allow`
- Verify bot token is correct in `channels.telegram.botToken`
- Check `openclaw logs --follow` for errors

### Bot responds but doesn't route URLs to media agent
- Verify the URL routing rules were added to the correct SOUL.md (the orchestrator's, not another agent's)
- Check that `agentId: "media"` matches the media agent's registered ID in OpenClaw
- Review `openclaw logs --follow` for sessions_spawn errors

### Media agent spawns but fails immediately
- Check that `~/projects/workflows/media-pipeline/` exists on gaming-PC
- Verify `.env` exists at that path with required variables (MEMORY_BASE_URL, MEMORY_TOKEN, MEMORY_AGENT_ID)
- Check yt-dlp version: `yt-dlp --version` (should be 2026.03.17+)

### "Unauthorized" or bot ignores messages from Alexandre
- Confirm `allowFrom` contains `"6616332223"` (as a string, not a number)
- Confirm `dmPolicy` is `"allowlist"` (not `"open"` or `"deny"`)
