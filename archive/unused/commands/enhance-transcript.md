---
description: Enhance a YouTube transcript with transcription corrections and channel pattern recognition
allowed-tools: [Read, Edit, Grep]
subagent: transcript-enhancer
---

# Enhance YouTube Transcript

Enhance the transcript file with transcription corrections, channel pattern recognition, and quality validation.

## Usage

```
/enhance-transcript <filename>
```

**Example:**
```
/enhance-transcript raw_text_for_enhancement_nGhsgdQplHw.txt
```

## What This Command Does

This command invokes the **transcript-enhancer** agent to:

1. **Load Learning System**: Review 173+ transcription corrections from `processing_knowledge_base.json`
2. **Apply Corrections**: Fix all known transcription errors (AI tool names, technical terms, etc.)
3. **Recognize Patterns**: Apply channel-specific enhancements (IndyDevDan, Sean Kochel, etc.)
4. **Validate Quality**: Ensure proper capitalization, spacing, and technical accuracy
5. **Analyze Content**: Identify content type and suggest optimal chunking strategy
6. **Generate Report**: Provide enhancement summary with recommendations

## Expected Output

- Enhanced transcript saved as: `<original_filename>_manual.txt`
- Enhancement report included at end of file
- Ready for manual chunking with `manual_chunker.py`

## Context Files Required

The agent will automatically load:
- `@learning/processing_knowledge_base.json` - 173+ transcription corrections
- `@learning/processing_history.md` - Historical processing insights

## Workflow Integration

```bash
# 1. Extract transcript
uv run python main.py extract "https://youtube.com/watch?v=VIDEO_ID"

# 2. Enhance with agent (this command)
/enhance-transcript raw_text_for_enhancement_VIDEO_ID.txt

# 3. Create manual chunks
uv run python manual_chunker.py

# 4. Import to database
uv run python scripts/import_manual_chunks.py
```

## Target File

Transcript file to enhance: **$ARGUMENTS**

---

@learning/processing_knowledge_base.json
@learning/processing_history.md

Now enhancing transcript: $ARGUMENTS
