# SOP: Learning System Updates

## Purpose
Standard operating procedure for maintaining and updating the learning system that powers our auto-enhancement pipeline.

## When to Use
- Discovered new transcription errors during enhancement
- Found recurring patterns in specific channels
- Improved chunking strategies
- Updated quality standards
- New tool releases or name changes

## Learning System Components

### 1. `learning/processing_knowledge_base.json`
**Contains:**
- `entity_corrections`: 174+ mapped corrections (e.g., "mate and" → "n8n")
- `channel_patterns`: Channel-specific quirks and styles
- `content_type_guidelines`: Chunking strategies per content type
- `quality_metrics`: Standards for rating chunk quality

### 2. `learning/processing_history.md`
**Contains:**
- Processing logs for each video
- Issues encountered and solutions
- Performance metrics over time
- Lessons learned

## Procedure

### Adding New Entity Corrections

**1. Identify the Pattern**
- Watch for repeated transcription errors
- Note the incorrect → correct mapping
- Verify it's not a one-time error

**2. Update processing_knowledge_base.json**
```json
{
  "entity_corrections": {
    "incorrect phrase": "Correct Name",
    "another error": "Another Correction"
  }
}
```

**3. Test the Correction**
```bash
# Re-run auto-enhancer on a test transcript
uv run python -m src.processing.auto_enhancer raw_text_for_enhancement_TEST.txt
```

**Quality Check:**
- ✅ Correction applied correctly
- ✅ No false positives (changing wrong phrases)
- ✅ Case-sensitivity handled properly

### Adding Channel Patterns

**When a channel has consistent characteristics:**

```json
{
  "channel_patterns": {
    "IndyDevDan": {
      "style": "rapid-fire technical tutorials",
      "typical_errors": ["clawed code", "cursor AI"],
      "content_focus": ["Claude Code", "agentic coding", "workflow automation"],
      "avg_video_length": "15-20 minutes",
      "chunking_preference": "dense, action-oriented"
    }
  }
}
```

### Updating Content Type Guidelines

**When you discover better chunking strategies:**

```json
{
  "content_type_guidelines": {
    "technical_tutorial": {
      "target_chunk_size": "300-500 tokens",
      "priority": "preserve command sequences and implementation steps",
      "quality_threshold": 0.7
    }
  }
}
```

### Logging to Processing History

**After each video processed:**

```markdown
## Video: [Title] (VIDEO_ID)
**Channel**: Channel Name
**Processed**: 2025-01-09
**Duration**: 18:32

### Corrections Applied
- 23 instances of "mate and" → "n8n"
- 5 instances of "clawed code" → "Claude Code"

### Quality Metrics
- Tools extracted: 12
- Commands extracted: 8
- Concepts extracted: 15
- Average chunk quality: 0.82

### Issues Encountered
- None

### Lessons Learned
- This channel consistently uses "slash commands" pattern
- High-quality implementation details throughout

### New Corrections Added
- "zero dot dev" → "v0.dev"
```

## Validation Process

### Before Committing Changes

1. **Test with Sample Transcripts**
```bash
# Run auto-enhancer on 2-3 different videos
uv run python -m src.processing.auto_enhancer sample_transcript.txt
```

2. **Verify No Regressions**
- Check that old corrections still work
- Ensure no new false positives

3. **Document the Change**
- Update processing_history.md
- Note why the change was made
- Include test results

## Quality Standards

### Good Corrections ✅
- **Specific**: Maps exact phrases, not broad terms
- **Consistent**: Works across all content types
- **Verified**: Tested on multiple transcripts
- **Documented**: Reason for correction is clear

**Examples:**
- "mate and" → "n8n" (specific transcription error)
- "make dot com" → "Make.com" (proper capitalization)
- "cursor AI" → "Cursor" (tool name normalization)

### Poor Corrections ❌
- **Too broad**: Could apply to wrong contexts
- **Ambiguous**: Unclear when to apply
- **Untested**: No verification on multiple files
- **Undocumented**: No explanation

**Examples to avoid:**
- "the new" → "" (too vague, loses context)
- "AI" → "artificial intelligence" (changes meaning)
- "tool" → "Tool" (unnecessary capitalization)

## Continuous Improvement

### Monthly Review
- Analyze correction effectiveness
- Remove corrections that cause false positives
- Consolidate similar patterns
- Update documentation

### Performance Metrics to Track
- Number of corrections applied per video
- Time saved vs manual enhancement
- Accuracy rate (correct vs false positives)
- Coverage (% of errors caught automatically)

## Common Issues

### Issue: Correction not being applied
**Check:**
1. Exact phrase match in JSON (case-sensitive)
2. No typos in the mapping
3. Auto-enhancer script is using latest JSON

### Issue: False positives (wrong corrections)
**Solution:**
1. Make correction more specific
2. Add context requirements
3. Consider channel-specific overrides

### Issue: New tool not recognized
**Solution:**
1. Add to entity_corrections immediately
2. Test on existing transcripts
3. Update agent extraction guidelines

## Related Documents

- [YouTube Video Processing SOP](./youtube-video-processing.md)
- [STREAMLINED_WORKFLOW.md](../../STREAMLINED_WORKFLOW.md)
- `learning/processing_knowledge_base.json`
- `learning/processing_history.md`

## Version History

- v1.0 (Jan 2025): Initial SOP for learning system maintenance
