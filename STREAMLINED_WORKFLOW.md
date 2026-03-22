# Streamlined YouTube Video Processing Workflow

## Overview

The streamlined workflow uses an intelligent agent-based system to process YouTube videos into high-quality knowledge base entries with **10x faster processing** and **zero manual work**.

**NEW**: The system now supports **dual-pipeline processing** optimized for different content types:
- **AI Tools Pipeline**: Technical tutorials, coding workflows, tool demonstrations
- **Sports Pipeline**: Training protocols, exercise science, biomechanical analysis

See `DUAL_PIPELINE_GUIDE.md` for complete dual-pipeline documentation.

## Workflow Comparison

### Old Manual Workflow (25 minutes per video)
```
1. Extract transcript                    → 30 seconds
2. Manual enhancement in Claude Code     → 15 minutes
3. Manual chunking                       → 10 minutes
4. Import to PostgreSQL VPS              → 2 minutes
5. Query via API                         → instant
```

### New Streamlined Workflow (2 minutes per video)

**AI Tools Pipeline**:
```
1. Extract transcript                            → 30 seconds
2. Auto-enhancement (174+ corrections)           → 5 seconds
3. Agent analysis (@youtube-transcript-analyzer) → 30 seconds
4. Generate detailed summary                     → 10 seconds
5. Store in unified-memory                        → instant
6. /compact (clean context)                      → instant
```

**Sports Pipeline**:
```
1. Extract transcript                              → 30 seconds
2. Auto-enhancement (174+ corrections)             → 5 seconds
3. Agent analysis (@sports-transcript-analyzer)    → 30 seconds
4. Generate sports summary                         → 10 seconds
5. Store in unified-memory (sport-specific tags)    → instant
6. /compact (clean context)                        → instant
```

## Quick Start

**AI Tools Videos** (Claude Code, development tools, programming):
```bash
# Use slash command
/process-youtube

# Or manual streamlined command
uv run python main.py streamlined "https://youtube.com/watch?v=VIDEO_ID"
```

**Sports Training Videos** (exercise protocols, scientific research):
```bash
# Use slash command
/process-sports-video

# This command handles sport-specific extraction, evidence tiers, and biomechanics
```

**How to Choose**:
- **Code/tools/workflows** → AI Tools Pipeline (`/process-youtube`)
- **Exercise/training/physiology** → Sports Pipeline (`/process-sports-video`)

See `DUAL_PIPELINE_GUIDE.md` for detailed decision criteria.

## Step-by-Step Guide

### 1. Extract & Auto-Enhance

```bash
# The streamlined command automatically:
# - Extracts raw transcript
# - Applies 174+ mapped corrections
uv run python main.py streamlined "https://youtube.com/watch?v=nGhsgdQplHw"
```

**Output**:
- `raw_text_for_enhancement_nGhsgdQplHw.txt` (raw)
- `raw_text_for_enhancement_nGhsgdQplHw_auto_enhanced.txt` (cleaned)

### 2. Intelligent Analysis with Specialized Agent

The workflow will prompt you to run:

```bash
claude "Use @youtube-transcript-analyzer to analyze raw_text_for_enhancement_nGhsgdQplHw_auto_enhanced.txt and save the JSON output to raw_text_for_enhancement_nGhsgdQplHw_auto_enhanced_analysis.json"
```

**What the Agent Does**:
- ✅ Comprehends the entire video content
- ✅ Extracts real tools (not fragments like "the new", "for automation")
- ✅ Identifies executable commands (`/scout`, `git push`, etc.)
- ✅ Captures meaningful concepts (Scout-Plan-Build, R&D Framework)
- ✅ Describes complete workflows with context
- ✅ Synthesizes actionable takeaways with WHY they matter

**Output**: High-quality JSON with structured knowledge

### 3. Generate Detailed Human-Readable Summary

After analysis, generate a comprehensive markdown summary:

```bash
uv run python scripts/generate_detailed_summary.py VIDEO_ID
```

**What Gets Generated**:
- 📄 Detailed markdown summary with 20+ sections
- 🔧 Technical implementation details (code snippets, configurations)
- 📝 Step-by-step setup guides
- 💡 Real-world examples and use cases
- ✅ Action items and checklists

**Output**: `workspace/summaries/VIDEO_ID_detailed_summary.md`

**Template**: Based on `src/templates/detailed_summary_template.md`

**Quality Standards**:
- ✅ Full code blocks with inline comments
- ✅ Actual configuration files (not descriptions)
- ✅ Complete command sequences with all flags
- ✅ File paths and directory structures
- ✅ Before/after examples for comparisons

### 4. Store in unified-memory

```bash
# Prepare content for MCP KB
uv run python scripts/store_in_mcp_kb.py raw_text_for_enhancement_nGhsgdQplHw_auto_enhanced_analysis.json
```

**Output**:
- `raw_text_for_enhancement_nGhsgdQplHw_auto_enhanced_mcp_kb_ready.txt`

Then store in unified-memory:

```
Use mcp__unified-memory__memory_store with the content from the _mcp_kb_ready.txt file
```

### 5. Clean Up Context (Recommended)

After successfully storing the video knowledge, clean up your conversation context:

```
/compact
```

**Why this matters**:
- Frees up 5-10% of context window for next video
- Removes processing noise from conversation history
- Maintains clean context between videos
- Follows best practices from AI Jason's context optimization video

**When to skip**: If you need to reference the current conversation for documentation or troubleshooting.

### 6. Query Anytime

```
Use mcp__unified-memory__memory_search with query: "Claude Code context window management"
```

## The Specialized Agents

The system uses domain-specific agents optimized for different content types:

### AI Tools Agent (@youtube-transcript-analyzer)

**Location**: `.claude/agents/youtube-transcript-analyzer.md`

**Optimized For**: Technical tutorials, coding workflows, tool demonstrations

**Capabilities**:
1. **Content Comprehension**: Understands technical tutorials, demos, workflows
2. **Tool Identification**: Filters real tools from conversational noise
3. **Command Extraction**: Finds actual executable commands
4. **Concept Recognition**: Identifies frameworks, patterns, methodologies
5. **Workflow Analysis**: Captures multi-step processes with full context
6. **Takeaway Synthesis**: Distills actionable insights with metrics
7. **Implementation Details**: Extracts exact setup steps, configuration values, code snippets, and troubleshooting guides

### Sports Agent (@sports-transcript-analyzer)

**Location**: `.claude/agents/sports-transcript-analyzer.md`

**Optimized For**: Training protocols, exercise science, biomechanical analysis

**Capabilities**:
1. **Protocol Extraction**: Volume, frequency, intensity, tempo, progression
2. **Evidence Classification**: Scientific citations with 4-tier evidence system
3. **Biomechanics Quantification**: Joint angles, muscle activation, force vectors
4. **WHY Reasoning**: Biomechanical, physiological, and tactical rationale
5. **Injury Considerations**: Contraindications, modifications, safety
6. **Equipment Analysis**: Specifications, alternatives, substitution quality
7. **Neo4j Integration**: Direct mapping to knowledge graph schema

See `DUAL_PIPELINE_GUIDE.md` for agent comparison and selection criteria.

### Quality Standards

**✅ GOOD** (What the agent extracts):
- Real tools: "Claude Code 2.0", "UV package manager", "GitHub"
- Executable commands: `/scout-plan-build`, `git push`, `uv run script.py`
- Complete concepts: "R&D Framework (Reduce and Delegate)"
- Detailed workflows: "Scout phase runs 4 parallel sub-agents..."
- Actionable takeaways: "Disable autocompact to save 22% context window"
- Implementation details: "Navigate to chrome.google.com/webstore, search 'Claude for Chrome', click Add to Chrome"

**❌ BAD** (What the agent filters out):
- Fragments: "the new", "for agentic", "more compute"
- Incomplete phrases: "from that", "really good"
- Vague concepts: "powerful tool", "nice feature"
- Generic instructions: "Install the extension and configure it"

## Example: IndyDevDan Video Analysis

**Video**: Claude Code 2.0 Agentic Coding
**ID**: nGhsgdQplHw

### Agent Output Quality

```json
{
  "tools_mentioned": [
    "Claude Code 2.0",
    "Claude 4.5 Sonnet",
    "OpenAI Agent SDK",
    "UV (package manager)",
    "Gemini Light",
    "Codex"
  ],
  "commands": [
    "/scout-plan-build",
    "/context",
    "/config autocompact false",
    "uv run",
    "git push"
  ],
  "key_concepts": [
    "Scout-Plan-Build Workflow",
    "R&D Framework (Reduce and Delegate)",
    "Autocompact Buffer",
    "Out-of-Loop Agentic Systems"
  ],
  "implementation_details": {
    "setup_steps": [
      "Create .claude/commands/scout-plan-build.md file",
      "Add frontmatter with name and variables",
      "Define command sequence: /scout, /plan, /build"
    ],
    "configuration": {
      "autocompact_disable": "/config autocompact false",
      "file_location": ".claude/commands/",
      "command_format": "markdown with YAML frontmatter"
    },
    "code_snippets": [
      {
        "language": "bash",
        "purpose": "Disable autocompact buffer to save context",
        "code": "/config autocompact false"
      }
    ]
  }
}
```

**Zero fragments, 100% actionable knowledge with implementation details.**

## Benefits

### Speed
- **Old**: 25 minutes manual work per video
- **New**: 2 minutes automated process
- **Improvement**: 12.5x faster

### Quality
- **Old**: Manual chunking, subjective quality
- **New**: Agent-based analysis, consistent quality
- **Improvement**: Repeatable, verifiable

### Scalability
- **Old**: PostgreSQL VPS, API complexity
- **New**: Local unified-memory, instant queries
- **Improvement**: Simpler infrastructure

### Accessibility
- **Old**: Query via API or VPS connection
- **New**: Direct Claude Code MCP KB integration
- **Improvement**: Native Claude Code experience

## Architecture

```
YouTube URL
    ↓
[Extract] → raw_text_for_enhancement_VIDEO_ID.txt
    ↓
[Auto-Enhance] → _auto_enhanced.txt (174+ corrections applied)
    ↓
[@youtube-transcript-analyzer] → _analysis.json (intelligent extraction)
    ↓
[Generate Detailed Summary] → workspace/summaries/VIDEO_ID_detailed_summary.md
    ↓
[MCP KB Storage] → _mcp_kb_ready.txt
    ↓
[mcp__unified-memory__memory_store] → Stored in KB
    ↓
[/compact] → Clean context for next video
    ↓
[Query Anytime] via mcp__unified-memory__memory_search
```

## Learning System Integration

The workflow maintains the existing learning system:

- `learning/processing_knowledge_base.json` (174+ corrections)
- `learning/processing_history.md` (video processing logs)

New corrections discovered during enhancement are still tracked and can be added to the knowledge base for future improvements.

## Migration from Old System

### If You Have Existing Videos

**Option 1**: Re-process with new workflow
```bash
# Extract and enhance
uv run python main.py extract "YOUTUBE_URL"
uv run python -m src.processing.auto_enhancer raw_text_*.txt

# Use agent for analysis
claude "Use @youtube-transcript-analyzer to analyze..."
```

**Option 2**: Keep existing PostgreSQL data
- VPS database still functional
- Can query via API as before
- New videos use unified-memory

### Recommended Approach
Use the streamlined workflow for all new videos. The unified-memory provides better integration with Claude Code and faster development cycles.

## Troubleshooting

### Agent Not Found
```bash
# Verify agent file exists
ls -la .claude/agents/youtube-transcript-analyzer.md

# Check Claude Code can see it
claude "list agents"
```

### Poor Quality Output
- Ensure transcript is auto-enhanced first
- Check that the enhanced file has corrections applied
- Review the agent's quality standards section

### unified-memory Issues
```bash
# Check MCP KB stats
mcp__unified-memory__sync_status

# Verify storage worked
mcp__unified-memory__memory_search with tag "youtube-knowledge-base"
```

## Future Enhancements

Potential improvements:
1. Fully automated pipeline (no manual Claude invocation)
2. Batch processing multiple videos
3. Channel-specific agent variants
4. Auto-tagging based on content analysis
5. Duplicate detection before storage

## Support

For issues or questions:
1. Check `.claude/agents/youtube-transcript-analyzer.md` for agent details
2. Review `learning/processing_knowledge_base.json` for correction patterns
3. Test with `scripts/streamlined_process.py` individually

---

**Last Updated**: January 2025
**Version**: 1.0 (Agent-based workflow)
