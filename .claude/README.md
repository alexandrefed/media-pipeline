# .claude Documentation Index

**Purpose**: Master index of all Claude Code configuration, agents, commands, SOPs, and system documentation.

**Last Updated**: January 2025 (v1.0)

## Quick Navigation

- [Agents](#agents) - Specialized AI agents for specific tasks
- [Commands](#commands) - Custom slash commands for workflows
- [SOPs](#standard-operating-procedures-sops) - Step-by-step procedures
- [System Docs](#system-documentation) - Architecture and technical details
- [Learning System](#learning-system) - Knowledge base and history

---

## Agents

Specialized agents for delegating specific tasks.

### 1. youtube-transcript-analyzer
**File**: `agents/youtube-transcript-analyzer.md`
**Purpose**: Analyze YouTube transcripts and extract structured knowledge
**Specialization**: General AI/automation content
**Output**: JSON with tools, commands, concepts, workflows, implementation details, takeaways

**When to use**:
- General AI tool videos
- Unknown content type
- First-time channel processing

### 2. indydevdan-analyzer
**File**: `agents/indydevdan-analyzer.md`
**Purpose**: Specialized analyzer for IndyDevDan videos
**Specialization**: Claude Code, agentic coding, rapid-fire technical tutorials
**Output**: High-density JSON optimized for IndyDevDan's style

**When to use**:
- IndyDevDan videos specifically
- Claude Code feature tutorials
- Agentic coding pattern videos

### 3. seankochel-analyzer
**File**: `agents/seankochel-analyzer.md`
**Purpose**: Specialized analyzer for Sean Kochel videos
**Specialization**: [Channel-specific patterns]
**Output**: JSON optimized for Sean's content style

**When to use**:
- Sean Kochel videos specifically
- [Specific content types]

### 4. youtube-processing-orchestrator
**File**: `agents/youtube-processing-orchestrator.md`
**Purpose**: Intelligent agent selector and workflow orchestrator
**Specialization**: Channel detection and agent delegation
**Output**: Delegates to specialized agents or handles directly

**When to use**:
- Uncertain which analyzer to use
- New channels without specialized agents
- Want automatic agent selection

---

## Commands

Custom slash commands for common workflows.

### 1. /process-youtube
**File**: `commands/process-youtube.md`
**Purpose**: Complete end-to-end YouTube video processing
**Pattern**: Scout-Plan-Build workflow

**Usage**: `/process-youtube` (you'll be prompted for the URL)

**Note**: Slash commands don't accept arguments - you'll be asked to provide the YouTube URL interactively

**Workflow**:
1. Scout: Extract & enhance transcript
2. Plan: Intelligent agent analysis
3. Build: Store in MCP KB Memory
4. Clean: /compact context

**Best for**:
- Processing new videos
- Consistent high-quality results
- Complete automation

### 2. /update-workflow
**File**: `commands/update-workflow.md`
**Purpose**: Update workflow documentation and learning system
**Inspired by**: AI Jason's /update-doc command

**Usage**: `/update-workflow` (you'll be prompted for type and details)

**Note**: Interactive command - you'll be asked what type of update to make

**Types**:
- `correction` - Add transcription correction
- `workflow` - Document improvement
- `sop` - Create/update SOP
- `learning` - Add insight
- `index` - Rebuild this README

**Best for**:
- Documenting improvements
- Adding new corrections
- Maintaining institutional knowledge
- Preventing repeated mistakes

---

## Standard Operating Procedures (SOPs)

Step-by-step procedures for common tasks.

### 1. YouTube Video Processing
**File**: `SOPs/youtube-video-processing.md`
**Purpose**: Standard procedure for processing YouTube videos

**Covers**:
- Extract and auto-enhance (30s)
- Agent analysis (30s)
- MCP KB Memory storage (instant)
- Quality checks and troubleshooting

**When to use**: Every video processing workflow

### 2. Learning System Updates
**File**: `SOPs/learning-system-updates.md`
**Purpose**: Maintain and update the learning system

**Covers**:
- Adding entity corrections
- Updating channel patterns
- Content type guidelines
- Validation process

**When to use**:
- Discovered new transcription errors
- Found channel patterns
- Updated quality standards

### 3. MCP KB Memory Management
**File**: `SOPs/mcp-kb-memory-management.md`
**Purpose**: Store, organize, and retrieve knowledge

**Covers**:
- Storage procedures
- Tagging conventions
- Query patterns
- Maintenance tasks

**When to use**:
- Storing processed videos
- Querying knowledge base
- Managing memories
- Health checks

---

## System Documentation

Architecture and technical details.

### 1. Database Schema
**File**: `system/database-schema.md`
**Purpose**: PostgreSQL database structure and usage

**Covers**:
- Tables: sources, chunks, processing_history
- Indexes and performance
- Common queries
- Maintenance procedures

**When to use**:
- Understanding data model
- Writing database queries
- Performance optimization
- Schema migrations

### 2. API Architecture
**File**: `system/api-architecture.md`
**Purpose**: REST API structure and integration

**Covers**:
- Endpoints and authentication
- Request/response formats
- Search modes and strategies
- Error handling

**When to use**:
- Integrating with API
- OpenAI Custom GPT setup
- Troubleshooting queries
- Performance tuning

### 3. MCP Optimization
**File**: `system/mcp-optimization.md`
**Purpose**: Optimize context window by managing MCP servers

**Covers**:
- Current MCP server audit
- Recommended disables (7-10 servers)
- Expected context gains (18-27%)
- Implementation steps

**When to use**:
- Context window running low
- Periodic optimization
- After installing new MCPs
- Following AI Jason's advice

---

## Learning System

Knowledge base and processing history.

### processing_knowledge_base.json
**Location**: `../learning/processing_knowledge_base.json`
**Purpose**: Central knowledge store for processing improvements

**Contains**:
- entity_corrections: 174+ mapped corrections
- channel_patterns: Channel-specific quirks
- content_type_guidelines: Chunking strategies
- quality_metrics: Standards for rating

**Update via**: `/update-workflow correction` or manual edit

### processing_history.md
**Location**: `../learning/processing_history.md`
**Purpose**: Historical log of all processed videos

**Contains**:
- Video processing logs
- Issues and solutions
- Performance metrics
- Lessons learned

**Update via**: `/update-workflow learning` or manual logging

---

## Context Optimization Tips

Based on AI Jason's video insights:

### 1. Remove Unused MCPs
**Recommended disables**: Google Slides, Notion, Puppeteer, Playwright, Strava, Neo4j, server-filesystem
**Expected gain**: 18-27% context window
**See**: `system/mcp-optimization.md`

### 2. Use Sub-Agents
**Pattern**: Delegate research to specialized agents
**Benefit**: Isolate token consumption
**Agents available**: 4 specialized analyzers

### 3. Proactive /compact
**When**: After each video processing
**Benefit**: Clean conversation history
**Saves**: 5-10% context per compact

### 4. Documentation System
**What**: This .claude folder structure
**Benefit**: Quick reference without deep codebase search
**Pattern**: Inspired by AI Jason's .agent folder system

---

## Quick Start Workflows

### Process a New Video
```
1. Type: /process-youtube
2. Paste YouTube URL when prompted
3. Wait ~2 minutes
4. Done! (context auto-cleaned with /compact)
```

**Or just say**: "Process this YouTube video: [URL]"

### Add New Correction
```
1. Type: /update-workflow
2. Select: correction
3. Provide: "error" → "fix"
4. Automatic testing and validation
```

**Or just say**: "Add this correction: 'error' should be 'fix'"

### Document Improvement
```
1. Type: /update-workflow
2. Select: workflow
3. Describe the improvement
4. Documentation automatically updated
```

**Or just say**: "Document this improvement: [description]"

### Check Context Usage
```
1. /context
2. Check MCP Tools token count
3. If > 25,000 → See system/mcp-optimization.md
4. If Messages > 150,000 → /compact
```

---

## File Structure

```
.claude/
├── README.md                          ← You are here
├── settings.local.json                ← Permissions config
├── agents/                            ← Specialized AI agents (4)
│   ├── youtube-transcript-analyzer.md
│   ├── indydevdan-analyzer.md
│   ├── seankochel-analyzer.md
│   └── youtube-processing-orchestrator.md
├── commands/                          ← Custom slash commands (2)
│   ├── process-youtube.md
│   └── update-workflow.md
├── SOPs/                              ← Standard Operating Procedures (3)
│   ├── youtube-video-processing.md
│   ├── learning-system-updates.md
│   └── mcp-kb-memory-management.md
└── system/                            ← Architecture docs (3)
    ├── database-schema.md
    ├── api-architecture.md
    └── mcp-optimization.md
```

---

## Statistics

**Total Documentation Files**: 12
- Agents: 4
- Commands: 2
- SOPs: 3
- System Docs: 3

**Learning System**:
- Transcription Corrections: 174+
- Videos Processed: 29
- Chunks Stored: 435
- Average Quality: 0.78

**Project Status**: Production-Ready
- Database: PostgreSQL 16 + pgvector on VPS
- API: https://api.vecia.fr (operational)
- MCP KB Memory: Active and queryable
- Streamlined Workflow: 2 minutes per video

---

## Recent Updates

**January 2025**:
- ✅ Created .claude folder documentation system
- ✅ Added 3 SOPs for standard procedures
- ✅ Created 3 system documentation files
- ✅ Implemented /update-workflow command
- ✅ Added MCP optimization recommendations
- ✅ Documented context window best practices

**Based on**:
- AI Jason: ".agent folder is making claude code 10x better"
- Video ID: MW3t6jP9AOs
- Key insights: Context engineering, documentation systems, /compact usage

---

## Maintenance

### Weekly
- [ ] Run `/context` to check token usage
- [ ] Review MCP tools consumption
- [ ] Check if any documentation needs updates

### Monthly
- [ ] Run `/update-workflow` → select `index` to rebuild this README
- [ ] Review SOPs for accuracy
- [ ] Check learning system for patterns
- [ ] Audit MCP server usage

### Quarterly
- [ ] Deep review of all documentation
- [ ] Update system diagrams
- [ ] Consolidate learnings
- [ ] Archive outdated docs

---

## Getting Help

**For**:
- **Video Processing Issues** → See `SOPs/youtube-video-processing.md`
- **Learning System** → See `SOPs/learning-system-updates.md`
- **MCP KB Memory** → See `SOPs/mcp-kb-memory-management.md`
- **Database Questions** → See `system/database-schema.md`
- **API Integration** → See `system/api-architecture.md`
- **Context Optimization** → See `system/mcp-optimization.md`

**Resources**:
- Main project guide: `CLAUDE.md` (project root)
- Streamlined workflow: `STREAMLINED_WORKFLOW.md`
- Learning system: `learning/` directory

---

## Version History

- **v1.0** (Jan 2025): Initial .claude documentation system
  - Created SOPs, system docs, README index
  - Implemented /update-workflow command
  - Added MCP optimization recommendations
  - Documented context window best practices

---

**This index is automatically updated by `/update-workflow index`**
