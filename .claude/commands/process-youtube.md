---
description: Process a YouTube video from URL to MCP KB Memory storage
---

# Process YouTube Video - Complete End-to-End Workflow

**Purpose**: Process a YouTube video from URL to MCP KB Memory storage using the Scout-Plan-Summarize-Build pattern inspired by agentic coding best practices.

**Pattern**: This command implements prompt composition by chaining five distinct phases:
1. **Scout**: Extract and enhance transcript
2. **Plan**: Analyze with specialized agent
3. **Summarize**: Generate detailed human-readable summary
4. **Build**: Store in knowledge base + auto-notify via n8n webhook
5. **Graph**: Extract entities and relationships to Neo4j Knowledge Graph

## Usage

```
/process-youtube
```

## Your Task - START HERE

**🚨 IMPORTANT: Slash commands cannot accept arguments!**

**STEP 0: Always Ask for the URL First**

When this command is invoked, IMMEDIATELY ask the user:

> "Please provide the YouTube video URL you want to process."

Then WAIT for the user's response before proceeding with any steps below.

## Workflow

### Phase 1: Scout (Extract & Enhance)

Extract the raw transcript and automatically apply 174+ mapped corrections:

```bash
# Extract raw transcript using the URL provided by the user
uv run python main.py streamlined "[URL]"
```

**What this does**:
- Extracts raw transcript from YouTube
- Applies 174+ mapped corrections automatically
- Creates enhanced transcript ready for analysis

**Output**: Enhanced transcript ready for analysis

### Phase 2: Plan (Intelligent Analysis)

Use the orchestrator to select the appropriate specialized agent and analyze:

```bash
# Orchestrator detects video type and delegates to specialized agent
Use @youtube-processing-orchestrator to analyze the enhanced transcript
```

**Orchestrator will**:
- Detect channel (IndyDevDan, Sean Kochel, Liam Ottley, etc.)
- Select specialized analyzer if available
- Fall back to general @youtube-transcript-analyzer
- Generate structured JSON analysis

**Output**: High-quality JSON with tools, commands, concepts, workflows, takeaways

### Phase 3: Summarize (Generate Detailed Summary)

Generate a comprehensive human-readable markdown summary:

```bash
# Extract video ID from URL
# Example: 4nthc76rSl8 from https://youtube.com/watch?v=4nthc76rSl8
uv run python scripts/generate_detailed_summary.py [VIDEO_ID]
```

**Summary includes**:
- 📄 20+ detailed sections (Executive Summary, Technical Deep Dive, etc.)
- 🔧 Technical implementation details (code snippets, configurations)
- 📝 Step-by-step setup guides
- 💡 Real-world examples and use cases
- ✅ Action items and checklists

**Output**: `workspace/summaries/[VIDEO_ID]_detailed_summary.md`

**Review**: User can review the detailed summary for accuracy and completeness

### Phase 4: Build (Store Knowledge + Auto-Notify)

Generate multi-memory storage and automatically sync to n8n for notifications:

```bash
# Generate enhanced multi-memory storage (v2)
uv run python scripts/store_in_mcp_kb.py workspace/analysis/[VIDEO_ID]_analysis.json

# This creates 5-7 specialized memories:
# 1. Overview (summary + takeaways)
# 2. Tools (all tools with context)
# 3. Commands (all commands with syntax)
# 4. Workflows (step-by-step processes)
# 5. Code Examples (complete snippets)
# 6. Setup Guide (installation, configuration)
# 7. Troubleshooting (common issues, solutions)

# AUTOMATICALLY:
# - Stores memories in local MCP KB Memory (ChromaDB)
# - Calls n8n webhook with video data + insights
# - Syncs to VPS PostgreSQL for notifications
# - Sends immediate Telegram notification
# - Schedules spaced repetition reminders
# - Enables weekly digest tracking
```

**What's different**:
- Creates **5-7 specialized memories** instead of 1 generic memory
- Uses **entity-based tagging** (tool-X, feature-Y, content-type-Z)
- Preserves **complete code examples** and workflows
- Based on **2025 RAG best practices**
- **NEW**: Automatically calls n8n webhook for notifications

**Dual Storage Architecture**:
- **Local (MCP KB Memory)**: Primary knowledge storage for instant retrieval
- **VPS (PostgreSQL)**: Secondary storage for notifications & workflows

**Output**:
- Video knowledge stored as multiple searchable memories
- Immediate Telegram notification sent automatically
- Spaced repetition reminders scheduled (daily 9 AM)
- Weekly digest tracking enabled (Sunday 8 PM)

**Check Telegram**: You should receive the notification within seconds!

### Phase 5: Graph (Entity Extraction → Neo4j Knowledge Graph)

Extract key entities and relationships from the analysis for graph-based querying:

**Step 1**: Use Haiku agent to extract entities from the analysis JSON:

```
Task(
  description="Extract entities from video analysis",
  prompt="""Extract key entities and relationships from this video analysis.

VIDEO ANALYSIS:
{paste analysis JSON from Phase 2}

Return ONLY valid JSON with:
{
  "entities": [
    {
      "name": "Entity Name",
      "type": "person|technology|concept|organization|topic",
      "observations": ["Key fact 1", "Key fact 2", "Usage context"]
    }
  ],
  "relationships": [
    {
      "source": "Entity1",
      "target": "Entity2",
      "relationType": "USES|RELATES_TO|CREATED_BY|PART_OF|BUILDS_ON"
    }
  ]
}

Entity Types:
- person: Named individuals (speakers, researchers, developers)
- technology: Tools, frameworks, languages, libraries
- concept: Abstract ideas, methodologies, patterns
- organization: Companies, institutions, communities
- topic: Subject areas, domains

Relationship Types:
- USES: Technology dependency (Tool A USES Library B)
- RELATES_TO: General association
- CREATED_BY: Attribution (Tool CREATED_BY Person)
- PART_OF: Containment (Feature PART_OF System)
- BUILDS_ON: Conceptual foundation""",
  model="haiku",
  subagent_type="general-purpose"
)
```

**Step 2**: Store entities and relationships in Neo4j:

```
# Create entities
mcp__unified-memory__enrichment_create(entities=[...extracted entities...])

# Create relationships
mcp__unified-memory__enrichment_create(relations=[...extracted relationships...])

# Verify storage
mcp__unified-memory__memory_search(query="main topic from video")
```

**Why both unified-memory + Neo4j?**
- **unified-memory**: "Find content about X" (semantic similarity search)
- **Neo4j**: "What entities exist? How do they relate?" (structured graph queries)

**Output**: Entities and relationships stored in Neo4j Knowledge Graph

### Phase 6: Clean Up (Context Management)

After successful processing, clean up the conversation context:

```
/compact
```

**Why**: Frees 5-10% context window for next video, removes processing noise

## Example Flow

```
User: /process-youtube

Claude: Please provide the YouTube video URL you want to process.

User: https://youtube.com/watch?v=nGhsgdQplHw

Claude: I'll process this video using the Scout-Plan-Summarize-Build workflow:

**Phase 1: Scout** - Extracting and enhancing transcript...
✅ Enhanced transcript with 18 corrections applied

**Phase 2: Plan** - Using @youtube-transcript-analyzer...
✅ Analysis complete with 16 tools, 12 commands, 16 concepts extracted

**Phase 3: Summarize** - Generating detailed summary...
✅ Detailed summary created at workspace/summaries/nGhsgdQplHw_detailed_summary.md

**Phase 4: Build** - Storing in MCP KB Memory + auto-notify...
✅ Generated 7 specialized memories (Overview, Tools, Commands, Workflows, Code, Setup, Troubleshooting)
✅ All memories stored with entity-based tags for precise retrieval
✅ Automatically synced to n8n webhook
✅ Video metadata + insights stored in VPS PostgreSQL
✅ Immediate Telegram notification sent
✅ Spaced repetition reminders scheduled (daily 9 AM)
✅ Weekly digest tracking enabled (Sunday 8 PM)

**Phase 5: Graph** - Extracting entities to Neo4j...
✅ Extracted 8 entities (3 technologies, 2 people, 2 concepts, 1 organization)
✅ Created 12 relationships (USES, CREATED_BY, RELATES_TO)
✅ Verified in Neo4j Knowledge Graph

**Phase 6: Clean Up** - Running /compact...
✅ Context cleaned for next video

Video processed! Summary available for review, knowledge searchable in base, entities mapped in graph, notifications enabled!
```

## Alternative: Natural Language

You can also just say: "Process this YouTube video: [URL]" and Claude will follow the same workflow based on CLAUDE.md context.

## Benefits

- **Consistency**: Same high-quality process every time
- **Efficiency**: Automated 5-phase workflow
- **Intelligence**: Channel-specific specialized analysis
- **Documentation**: Detailed human-readable summaries for review
- **Reusability**: Works for any YouTube video
- **Composability**: Can be used in other workflows

## Related Commands

- `/extract-youtube` - Just extract and enhance (Scout only)
- `/analyze-video` - Just analyze (Plan only)

## Notes

- Uses prompt composition pattern from agentic coding best practices
- Implements R&D framework (Reduce and Delegate) through orchestrator
- Maintains learning system for continuous improvement
- All extracted knowledge stored in MCP KB Memory for instant retrieval
