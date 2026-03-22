# SOP: MCP KB Memory Management

## Purpose
Standard operating procedure for storing, organizing, and retrieving knowledge from MCP KB Memory.

## When to Use
- Storing processed YouTube video analysis
- Organizing knowledge with tags
- Querying the knowledge base
- Maintaining and cleaning up memories
- Managing knowledge base health

## MCP KB Memory Tools

### Storage Tools
- `store_memory` - Store new knowledge with tags and metadata
- `update_memory_metadata` - Update tags without recreating memory

### Retrieval Tools
- `retrieve_memory` - Semantic search by content
- `recall_memory` - Natural language time-based queries
- `search_by_tag` - Find by specific tags
- `exact_match_retrieve` - Find exact content matches

### Management Tools
- `check_database_health` - System status and statistics
- `cleanup_duplicates` - Remove duplicate entries
- `delete_memory` - Remove specific memories by hash
- `delete_by_tag` - Bulk delete by tags

## Standard Procedures

### Storing YouTube Video Knowledge

**1. Prepare Content Structure**
```
**Video**: [Title]
**Channel**: [Channel Name]
**Video ID**: [VIDEO_ID]
**URL**: https://youtube.com/watch?v=[VIDEO_ID]

## Summary
[Comprehensive summary from agent analysis]

## Tools Mentioned
[Comma-separated list]

## Commands
[Bulleted list with descriptions]

## Key Concepts
[Comma-separated list]

## Key Takeaways
[Numbered list with actionable insights]
```

**2. Define Metadata and Tags**
```json
{
  "tags": "youtube-knowledge-base,video-VIDEO_ID,channel-CHANNEL_NAME,topic1,topic2",
  "type": "youtube-video",
  "video_id": "VIDEO_ID",
  "channel": "Channel Name",
  "topic": "Main Topic"
}
```

**3. Store with MCP Tool**
```
mcp__unified-memory__memory_store
- content: [structured content from step 1]
- metadata: [JSON from step 2]
```

### Tagging Conventions

**Required Tags (always include):**
- `youtube-knowledge-base` - Identifies all YouTube content
- `video-{VIDEO_ID}` - Unique video identifier
- `channel-{CHANNEL_NAME}` - Channel in lowercase with hyphens

**Topic Tags (choose relevant):**
- `claude-code` - Claude Code features and workflows
- `cursor` - Cursor AI features
- `n8n` - n8n automation
- `make` - Make.com automation
- `automation` - General automation content
- `ai-tools` - AI tool reviews/tutorials
- `agentic-coding` - Agentic coding patterns
- `context-engineering` - Context window optimization
- `agent-folder` - .agent folder documentation systems
- `workflow-optimization` - Process improvement

**Content Type Tags:**
- `tutorial` - Step-by-step instructional content
- `overview` - High-level tool overview
- `comparison` - Tool/approach comparisons
- `best-practices` - Recommended patterns and practices
- `case-study` - Real-world implementation examples

### Query Patterns

**1. Semantic Search (most common)**
```
mcp__unified-memory__memory_search
query: "Claude Code context window management techniques"
n_results: 10
```

**Use when:**
- Looking for conceptual knowledge
- Don't know exact phrasing
- Want related content

**2. Time-Based Recall**
```
mcp__unified-memory__context_recall
query: "videos about automation from last week"
n_results: 5
```

**Use when:**
- Recently processed content
- Time-specific queries
- "What did I learn yesterday?"

**3. Tag-Based Search**
```
mcp__unified-memory__memory_search
tags: ["claude-code", "agentic-coding"]
```

**Use when:**
- Filtering by specific topics
- Finding all content from a channel
- Category-based browsing

**4. Exact Match**
```
mcp__unified-memory__memory_search
content: "specific phrase or command"
```

**Use when:**
- Looking for exact command syntax
- Verifying specific quotes
- Debugging duplicate content

## Quality Standards

### Good Memory Content ✅

**Characteristics:**
- Complete and self-contained
- Structured with clear sections
- Includes source attribution (video URL, timestamp)
- Actionable takeaways with metrics
- Properly tagged with 5-8 relevant tags

**Example:**
```
**Video**: .agent folder is making claude code 10x better
**Channel**: AI Jason
**Video ID**: MW3t6jP9AOs
**URL**: https://youtube.com/watch?v=MW3t6jP9AOs

## Summary
This tutorial demonstrates advanced context engineering...

## Key Takeaways
1. Remove unused MCP tools to reclaim 2% of context window...
2. Use sub-agents to offload research tasks...

Tags: youtube-knowledge-base,ai-jason,claude-code,context-engineering,agent-folder
```

### Poor Memory Content ❌

**Avoid:**
- Fragmented or incomplete information
- No source attribution
- Vague takeaways without specifics
- Generic tags like "video" or "content"
- Duplicate information already stored

## Maintenance Tasks

### Weekly: Health Check
```bash
# Check database status
mcp__unified-memory__sync_status

# Get statistics
mcp__unified-memory__sync_status
```

**What to check:**
- Total memories stored
- Storage size
- Query performance
- No errors or corruption

### Monthly: Cleanup
```bash
# Find and remove duplicates
mcp__unified-memory__memory_delete

# Review old temporary tags
mcp__unified-memory__memory_search tags: ["temporary"]
# Delete if no longer needed
mcp__unified-memory__memory_delete tags: ["temporary"]
```

### Quarterly: Tag Audit
- Review tag usage patterns
- Consolidate similar tags
- Update tagging conventions
- Document new categories

## Common Issues

### Issue: Duplicate content stored
**Prevention:**
- Check if video ID already exists before storing
- Use exact_match_retrieve to verify

**Solution:**
```bash
mcp__unified-memory__memory_delete
```

### Issue: Can't find stored content
**Troubleshooting:**
1. Verify tags are correct
2. Try semantic search instead of exact match
3. Check if content was actually stored
4. Review query phrasing

### Issue: Too many results returned
**Solution:**
- Add more specific tags to filter
- Use tag-based search instead of semantic
- Reduce n_results parameter
- Refine query to be more specific

### Issue: Storage failing
**Check:**
1. MCP server is running
2. Database has sufficient space
3. Content format is valid
4. Metadata JSON is properly formatted

## Performance Optimization

### Query Speed
- Use tag-based search for large result sets
- Limit n_results to what you actually need (5-10 usually sufficient)
- Prefer specific queries over broad searches

### Storage Efficiency
- Avoid storing extremely long content (>10,000 chars)
- Use concise summaries for long videos
- Remove redundant information before storing
- Use metadata fields instead of embedding info in content

### Context Management
- Run `/compact` after batch storage operations
- Keep query results focused and relevant
- Don't retrieve more than needed for current task

## Success Metrics

**Storage Quality:**
- 95%+ content has all required tags
- Less than 5% duplicate content
- All memories have source attribution

**Retrieval Effectiveness:**
- Query finds relevant content in top 5 results
- Less than 10% "no results found"
- Tag coverage allows precise filtering

**System Health:**
- No database errors
- Query response time < 2 seconds
- Regular backups completed successfully

## Related Documents

- [YouTube Video Processing SOP](./youtube-video-processing.md)
- [Learning System Updates SOP](./learning-system-updates.md)
- [STREAMLINED_WORKFLOW.md](../../STREAMLINED_WORKFLOW.md)

## Version History

- v1.0 (Jan 2025): Initial SOP for MCP KB Memory management
