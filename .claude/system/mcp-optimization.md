# System: MCP Server Optimization

## Overview

Based on insights from AI Jason's video on context window management, this document identifies opportunities to optimize our MCP server configuration for better context efficiency.

**Key Insight**: Removing unused MCP tools can reclaim 2-10% of the 200K token context window.

## Currently Active MCP Servers

### Essential (Keep Active)

#### 1. mcp-kb-memory
**Purpose**: Core knowledge base storage and retrieval
**Usage**: High - used for every video processing workflow
**Tools**: 25+ memory management tools
**Verdict**: ✅ **ESSENTIAL - Keep active**

**Justification**: This is our primary knowledge storage system. All processed videos are stored here and queried frequently.

#### 2. context7
**Purpose**: Fetch up-to-date library documentation
**Usage**: Medium - used when implementing features with external libraries
**Tools**: 2 (resolve-library-id, get-library-docs)
**Verdict**: ✅ **USEFUL - Keep active**

**Justification**: Lightweight (only 2 tools) and useful for getting current documentation during development.

#### 3. fetch
**Purpose**: Web content fetching
**Usage**: Medium - used for research and documentation lookup
**Tools**: 1 (fetch)
**Verdict**: ✅ **USEFUL - Keep active**

**Justification**: Single tool, minimal context overhead, useful for ad-hoc web fetching.

### Potentially Useful (Evaluate)

#### 4. brave-search / tavily-mcp
**Purpose**: Web search capabilities
**Usage**: Low - rarely used in current workflow
**Tools**: brave-search (2 tools), tavily (2 tools)
**Verdict**: ⚠️ **EVALUATE - Consider disabling one**

**Recommendation**: Keep tavily-mcp (more powerful), disable brave-search to reduce redundancy.

**Context Gain**: ~1-2%

#### 5. mcp-server-firecrawl
**Purpose**: Advanced web scraping
**Usage**: Low - could be useful for YouTube metadata
**Tools**: 8 (scrape, map, search, crawl, etc.)
**Verdict**: ⚠️ **EVALUATE - Monitor usage**

**Recommendation**: Keep for now, but monitor if actually used. Could be valuable for future YouTube processing enhancements.

#### 6. server-sequential-thinking
**Purpose**: Step-by-step reasoning tool
**Usage**: Unknown - not currently used in workflows
**Tools**: 1 (sequentialthinking)
**Verdict**: ⚠️ **EVALUATE - Disable if not used**

**Recommendation**: Disable unless specifically needed for complex problem-solving.

**Context Gain**: ~1%

### Not Needed (Disable)

#### 7. Google Slides MCP
**Purpose**: Create and manage Google Slides presentations
**Usage**: None - not relevant to YouTube processing workflow
**Tools**: 5 (create_presentation, get_presentation, batch_update, etc.)
**Verdict**: ❌ **DISABLE**

**Context Gain**: ~2-3%

#### 8. Notion API
**Purpose**: Notion workspace integration
**Usage**: None - we use MCP KB Memory instead
**Tools**: 15+ (pages, databases, blocks, comments)
**Verdict**: ❌ **DISABLE**

**Context Gain**: ~3-5%

#### 9. Puppeteer
**Purpose**: Browser automation
**Usage**: None - not needed for YouTube transcript processing
**Tools**: 7 (navigate, screenshot, click, fill, etc.)
**Verdict**: ❌ **DISABLE**

**Context Gain**: ~2%

#### 10. Playwright
**Purpose**: Advanced browser automation
**Usage**: None - overlaps with Puppeteer, both unnecessary
**Tools**: 15+ (navigate, click, evaluate, screenshot, etc.)
**Verdict**: ❌ **DISABLE**

**Context Gain**: ~3-4%

#### 11. Strava MCP
**Purpose**: Strava fitness data integration
**Usage**: None - completely unrelated to AI knowledge base
**Tools**: 20+ (athlete stats, activities, routes, segments)
**Verdict**: ❌ **DISABLE**

**Context Gain**: ~4-5%

#### 12. Neo4j (vecia-neo4j)
**Purpose**: Graph database integration
**Usage**: None - we use PostgreSQL
**Tools**: 3 (get_schema, read_cypher, write_cypher)
**Verdict**: ❌ **DISABLE**

**Context Gain**: ~1-2%

#### 13. server-filesystem
**Purpose**: File system operations
**Usage**: Redundant - Claude Code has built-in Read/Write/Edit tools
**Tools**: 15+ (read_file, write_file, list_directory, etc.)
**Verdict**: ❌ **DISABLE**

**Context Gain**: ~3-4%

#### 14. IDE Integration
**Purpose**: VS Code diagnostics and code execution
**Usage**: Low - might be useful but not actively used
**Tools**: 2 (getDiagnostics, executeCode)
**Verdict**: ⚠️ **EVALUATE - Disable if not debugging**

**Recommendation**: Disable unless actively debugging Python code issues.

**Context Gain**: ~1%

## Optimization Recommendations

### Immediate Disables (High Impact)

**Total Context Gain: ~18-27%**

1. ❌ Google Slides MCP
2. ❌ Notion API
3. ❌ Puppeteer
4. ❌ Playwright
5. ❌ Strava MCP
6. ❌ Neo4j
7. ❌ server-filesystem

### Optional Disables (Medium Impact)

**Additional Context Gain: ~3-4%**

8. ⚠️ brave-search (keep tavily instead)
9. ⚠️ server-sequential-thinking (if not used)
10. ⚠️ IDE integration (unless debugging)

### Keep Active

11. ✅ mcp-kb-memory (essential)
12. ✅ context7 (useful, lightweight)
13. ✅ fetch (useful, single tool)
14. ✅ tavily-mcp (web search, more powerful than brave)
15. ✅ mcp-server-firecrawl (potentially useful for YouTube)

## Implementation Steps

### 1. Review MCP Configuration

Check Claude Code settings:
```bash
# Location of MCP config (system-wide)
~/Library/Application Support/Claude/claude_desktop_config.json

# Project-specific permissions
.claude/settings.local.json
```

### 2. Disable Unused MCPs

Option A: Remove from claude_desktop_config.json
```json
{
  "mcpServers": {
    "mcp-kb-memory": { ... },
    "context7": { ... },
    "fetch": { ... },
    "tavily-mcp": { ... },
    "mcp-server-firecrawl": { ... }
    // Remove: google-slides, notion, puppeteer, playwright, strava, neo4j, filesystem
  }
}
```

Option B: Comment out in config (easier to re-enable)
```json
{
  "mcpServers": {
    // Disabled for context optimization - see .claude/system/mcp-optimization.md
    // "google-slides-mcp": { ... },
    // "notionApi": { ... },
    // etc.
  }
}
```

### 3. Restart Claude Code

Changes require full restart:
1. Quit Claude Code completely
2. Restart the application
3. Verify with `/context` command

### 4. Verify Context Savings

Before and after comparison:
```
Use /context command to check token consumption

Before:
System Prompts: 15,000 tokens
MCP Tools: 35,000 tokens  ← should decrease significantly
Messages: 50,000 tokens
Total: 100,000 / 200,000

After (expected):
System Prompts: 15,000 tokens
MCP Tools: 15,000 tokens  ← ~20,000 token savings
Messages: 50,000 tokens
Total: 80,000 / 200,000
```

## Context Window Best Practices

### From AI Jason Video

1. **Remove unused MCP tools** → 2-10% context gain
2. **Use sub-agents for research** → Isolate token consumption
3. **Proactive /compact usage** → Clean conversation history
4. **Maintain .agent folder documentation** → Reduce codebase searches

### Our Implementation

1. ✅ **Disable 7-10 unused MCPs** → ~20-30% context gain
2. ✅ **Use specialized agents** (@youtube-transcript-analyzer, etc.)
3. ⏸️ **Add /compact to workflow** → After each video processing
4. ✅ **Create .claude folder system** → SOPs, system docs, README

## Monitoring Context Usage

### Regular Checks

**Weekly**: Run `/context` command
- Monitor MCP tools token count
- Check if any new MCPs added
- Verify disabled MCPs stay disabled

**Monthly**: Review MCP usage
- Are disabled MCPs actually needed?
- Are active MCPs being used?
- Any new MCPs to evaluate?

### Expected Baselines (After Optimization)

```
Healthy Context Usage:
- System Prompts: ~15,000 tokens (can't reduce)
- MCP Tools: ~15,000 tokens (down from ~35,000)
- Messages: Variable (depends on conversation)
- Total Available: 200,000 tokens

Warning Signs:
- MCP Tools > 25,000 → Too many MCPs enabled
- Messages > 150,000 → Run /compact
- Total > 180,000 → Risk of context overflow
```

## Troubleshooting

### Issue: Needed functionality missing after disabling MCP

**Solution**: Re-enable that specific MCP
```json
// Add back to claude_desktop_config.json
{
  "mcpServers": {
    "needed-mcp": { ... }
  }
}
```

### Issue: Context usage not decreasing

**Check**:
1. Did you fully restart Claude Code?
2. Are MCPs actually removed from config?
3. Run `/context` to verify current state

### Issue: Don't know which MCPs are actually in use

**Solution**: Monitor for a week with all enabled, note which tools you use, then disable unused ones.

## Related Documents

- [AI Jason Video: .agent folder making claude code 10x better](mcp://retrieve-memory?query=agent-folder)
- [YouTube Video Processing SOP](../SOPs/youtube-video-processing.md)
- [STREAMLINED_WORKFLOW.md](../../STREAMLINED_WORKFLOW.md)

## Version History

- v1.0 (Jan 2025): Initial MCP optimization recommendations based on AI Jason video insights
