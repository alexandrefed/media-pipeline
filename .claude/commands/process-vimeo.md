# Process Vimeo Video - Extract Conference Transcript

**Purpose**: Extract transcript from a Vimeo conference video for manual review and selective knowledge base storage.

**Use Case**: For long conference videos (1-2 hours), extract the full transcript so you can review it, identify key sections, and manually select what insights to add to your knowledge base.

## Usage

```
/process-vimeo
```

## Your Task

When this command is invoked, IMMEDIATELY ask the user:

> "Please provide the Vimeo video URL you want to process."

Then WAIT for the user's response before proceeding.

## Workflow

### Step 1: Extract Transcript

Run the Vimeo extraction script:

```bash
uv run python scripts/process_vimeo.py "[URL]"
```

**What this does**:
- Uses yt-dlp with browser cookies to authenticate with Vimeo
- Extracts raw transcript segments
- Reconstructs into readable text
- Saves as `raw_text_for_enhancement_vimeo_[VIDEO_ID].txt`

**Browser Authentication**:
- Default: Chrome browser cookies
- If Chrome doesn't work, try: `--browser firefox` or `--browser edge`
- User must be logged into Vimeo in that browser

### Step 2: Review and Discuss

After extraction, guide the user:

1. **Review the transcript** - Open the generated text file
2. **Identify key sections** - What talks, demos, or insights are most relevant?
3. **Discuss strategy** - What specific information should go into the knowledge base?

### Step 3: Manual Selection (User-Driven)

**Important**: For long conference videos, DO NOT automatically process everything. Instead:

- Wait for user to identify specific sections
- Manually extract key insights and takeaways
- Create focused chunks for specific topics
- Store only what's relevant to their startup strategy

## Example Flow

```
User: /process-vimeo

Claude: Please provide the Vimeo video URL you want to process.

User: https://vimeo.com/1133050369

Claude: I'll extract the transcript from this Vimeo video.

[Runs extraction script]

✅ Transcript extracted successfully!
📄 File: raw_text_for_enhancement_vimeo_1133050369.txt

This appears to be a conference video. Let me open it so we can review the content together.

[Shows preview of transcript]

What sections of this conference are most relevant to your startup strategy?
We can focus on extracting specific insights from those parts.

User: I'm interested in the section about scaling AI systems around timestamp 45:30

Claude: Great! Let me help you extract and structure those insights...
```

## Key Differences from YouTube Pipeline

- **No automatic full processing** - Conference videos are too long
- **Manual review required** - User decides what's valuable
- **Selective extraction** - Only store relevant sections
- **Strategy-focused** - Prioritize insights that help the startup

## Troubleshooting

If extraction fails:
1. Verify user is logged into Vimeo in their browser
2. Check if video has captions enabled
3. Try different browser: `--browser firefox` or `--browser edge`
4. Confirm video is accessible (not private/restricted)

## Next Steps After Extraction

Once transcript is extracted and reviewed:
- Manually enhance key sections in Claude Code
- Create focused chunks for specific insights
- Store only relevant information in KB
- Keep original transcript file as reference

## Notes

- Vimeo requires authentication via browser cookies
- Works best with videos that have captions/subtitles
- Processing time depends on video length
- Full transcript saved for future reference
