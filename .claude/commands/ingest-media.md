---
description: Ingest any media URL (YouTube, Instagram, Vimeo, audio) into the AI Knowledge Base
---

# Ingest Media

**Purpose**: Process any media URL end-to-end — extract, analyze, and store across all targets (gaming-PC filesystem, unified-memory, Notion, Neo4j on VPS, VPS pgvector).

## Your Task — START HERE

**🚨 IMPORTANT: Slash commands cannot accept arguments!**

**STEP 0: Ask for the URL**

When this command is invoked, IMMEDIATELY ask the user:

> "Please provide the media URL to process (YouTube, Vimeo, Instagram, TikTok, or a local file path)."

Then WAIT for the user's response before proceeding.

**STEP 1: Delegate to @media-ingestion-agent**

Once you have the URL, hand off entirely to the agent:

```
Use @media-ingestion-agent to process this URL: {URL}
```

The agent handles everything:
- Link detection (YouTube / Instagram / Vimeo / audio)
- Sports vs AI Tools classification
- Pipeline execution on the gaming-PC filesystem
- Storage fan-out to all 5 targets
- Completion report

## Supported Sources

| Source | Authentication | Pipeline |
|--------|---------------|---------|
| YouTube | Public (yt-dlp) | AI Tools or Sports |
| Vimeo | Firefox cookies | Vimeo |
| Instagram Reels | Firefox cookies (yt-dlp) | Instagram/Whisper |
| TikTok | Firefox cookies (yt-dlp) | Instagram/Whisper |
| Local audio/video | None | Whisper direct |

## Output

After processing you will have:
- `workspace/analysis/{VIDEO_ID}_analysis.json` — structured extraction
- `workspace/summaries/{VIDEO_ID}_*summary.md` — human-readable summary
- 5-7 memories in unified-memory (searchable via `mcp__unified-memory__memory_search`)
- 1 note synced to Notion (Notes database)
- Entities in Neo4j on VPS (auto, via GraphExtractionPipeline)
- Embedded chunks in VPS pgvector (auto, via n8n webhook)

## Related Commands

- `/process-youtube` — YouTube-only with full phase-by-phase visibility
- `/process-sports-video` — Sports training videos with scientific evidence extraction
- `/compact` — Clean context after processing a batch of videos
