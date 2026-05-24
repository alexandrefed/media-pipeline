# SOP: YouTube Video Processing

## Purpose
Standard operating procedure for processing YouTube videos from extraction through unified-memory storage.

## When to Use
- Processing a new YouTube video into the knowledge base
- Re-processing a video with improved methods
- Batch processing multiple videos

## Prerequisites
- YouTube URL
- Internet connection
- uv environment set up
- unified-memory server running

## Procedure

### 1. Extract and Auto-Enhance (30 seconds)
```bash
uv run python main.py streamlined "https://youtube.com/watch?v=VIDEO_ID"
```

**What this does:**
- Extracts raw transcript from YouTube
- Applies 174+ mapped corrections automatically
- Creates two files:
  - `raw_text_for_enhancement_VIDEO_ID.txt` (raw)
  - `raw_text_for_enhancement_VIDEO_ID_auto_enhanced.txt` (cleaned)

**Quality Check:**
- ✅ Both files created in workspace
- ✅ Enhanced file has corrections applied
- ✅ No extraction errors in console

### 2. Agent Analysis (30 seconds)

Use the specialized agent to analyze:
```
Use @youtube-transcript-analyzer to analyze raw_text_for_enhancement_VIDEO_ID_auto_enhanced.txt and save JSON output to workspace/analysis/VIDEO_ID_analysis.json
```

**Agent Selection Logic:**
- **IndyDevDan videos** → @indydevdan-analyzer
- **Sean Kochel videos** → @seankochel-analyzer
- **Other AI/automation videos** → @youtube-transcript-analyzer
- **Uncertain** → @youtube-processing-orchestrator (auto-delegates)

**Quality Check:**
- ✅ JSON file created in workspace/analysis/
- ✅ Contains tools, commands, concepts, workflows, takeaways
- ✅ No fragments or incomplete data
- ✅ Implementation details included

### 3. Generate Summary (LLM-written)

The agent reads `analysis.json` and writes `summary.md` directly — no Python script.

**What it produces:**
- Executive Summary (rewritten from analysis, 2-3 paragraphs)
- Key Takeaways with actionability tags (actionable/reference/awareness)
- Tools & Technologies with context
- Implementation Details (setup steps, config, code snippets)
- Workflows & Patterns
- Commands Reference with syntax blocks
- Only sections with actual content are included

**Output:** `workspace/videos/{folder}/summary.md`

**Quality Standards:**

**MUST INCLUDE:**
- Data sourced from analysis.json fields, not regex extraction from transcript
- Actionability classification on every takeaway
- Complete code snippets with language tags
- Specific setup steps, config values, and file paths from implementation_details

**MUST AVOID:**
- Unfilled placeholder text (e.g., "*[Extract architectural patterns]*")
- Regex-extracted "tools" that are actually common English words
- Empty sections — omit them entirely if no content exists

**Quality Check:**
- Summary file created in workspace/videos/{folder}/
- All included sections have real content (no placeholders)
- Tools listed match analysis.json.tools_mentioned exactly
- Takeaways have actionability tags

### 4. Store in unified-memory (instant)

Prepare content:
```bash
uv run python scripts/store_in_mcp_kb.py workspace/analysis/VIDEO_ID_analysis.json
```

Then store:
```
Use mcp__unified-memory__memory_store with content from output and appropriate tags
```

**Tags to include:**
- `youtube-knowledge-base` (always)
- `video-VIDEO_ID` (for reference)
- `channel-CHANNEL_NAME` (lowercase, hyphens)
- Content-specific tags (e.g., `claude-code`, `n8n`, `automation`)

**Quality Check:**
- ✅ Memory stored successfully
- ✅ Can query and retrieve the content
- ✅ Tags are correct and searchable

### 5. Clean Up Context (recommended)

After completing the video:
```
/compact
```

**Why:**
- Frees up context window for next video
- Removes processing noise
- Maintains clean conversation history

## Common Issues

### Issue: Extraction fails
**Solution:** Check YouTube URL is valid and video has captions enabled

### Issue: Auto-enhancement missed corrections
**Solution:** Add new corrections to `learning/processing_knowledge_base.json`

### Issue: Agent extracts fragments
**Solution:** Ensure enhanced file was used (not raw), review agent quality standards

### Issue: Summary lacks technical details
**Solution:**
- Verify enhanced transcript has good quality content
- Check that analysis JSON has implementation_details section
- Manually enhance summary using template at `src/templates/detailed_summary_template.md`
- Reference the enhanced transcript for missing technical content

### Issue: Summary generation script fails
**Solution:**
- Verify analysis file exists in workspace/analysis/
- Check enhanced transcript is available
- Ensure workspace/summaries/ directory exists
- Review script output for specific errors

### Issue: MCP KB storage fails
**Solution:** Check MCP server is running with `mcp__unified-memory__sync_status`

## Success Metrics

**Per video:**
- Processing time: ~2 minutes
- Tools extracted: 5-15 (varies by content)
- Commands extracted: 3-10 (if tutorial)
- Concepts extracted: 8-20
- Implementation details: Present for tutorial content
- Takeaways: 5-7 actionable insights
- Detailed summary: 20+ sections with technical implementation details
- Summary quality: Code snippets, configurations, step-by-step guides present

## Related Documents

- [Learning System Updates SOP](./learning-system-updates.md)
- [unified-memory Management SOP](./mcp-kb-memory-management.md)
- [STREAMLINED_WORKFLOW.md](../../STREAMLINED_WORKFLOW.md)

## Version History

- v1.1 (Jan 2025): Added detailed summary generation as standard deliverable
- v1.0 (Jan 2025): Initial SOP based on streamlined workflow
