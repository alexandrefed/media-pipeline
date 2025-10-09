---
description: Resume processing a YouTube video from any stage with full context
allowed-tools: [Read, Bash, Grep]
---

# Resume Video Processing - Recovery Command

## Current Project State
!echo "Checking current video processing state..."
!ls -la pending/raw_transcripts/ | tail -5
!ls -la processed/manual_chunks/ | tail -5

## Load Context
@learning/processing_knowledge_base.json
@learning/processing_history.md
@CLAUDE.md
@CLAUDE_CODE_WORKFLOW.md

## Video to Resume: $ARGUMENTS

Based on the video ID/URL provided ($ARGUMENTS), here's what I'll do:

1. **Identify Current Stage**:
   - Check if raw transcript exists in `pending/raw_transcripts/`
   - Check if enhanced transcript exists in `pending/enhanced_no_chunks/`
   - Check if chunks exist in `processed/manual_chunks/`

2. **Load Learning System**:
   - Review processing_knowledge_base.json (v2.4) with 115+ transcription corrections
   - Check channel-specific patterns for optimal chunking
   - Apply learnings from 21 previously processed videos

3. **Continue From Last Step**:
   - If no raw transcript: Run `uv run python main.py extract "$ARGUMENTS"`
   - If raw exists but not enhanced: Enhance transcript with corrections
   - If enhanced but no chunks: Create custom manual_chunker script
   - If chunks exist: Update learning system and mark complete

4. **Key Workflow Reminders**:
   - Manual chunking creates 93% fewer but 13x larger chunks
   - Average tokens per chunk varies by content type:
     - Technical tutorials: 300-500 tokens
     - Productivity content: 100-150 tokens
     - Voice demonstrations: 185-345 tokens
   - Always update learning system after processing

Let me analyze the current state and continue processing...