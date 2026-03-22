# Dual-Pipeline YouTube Processing Guide

## Overview

This knowledge base system supports **two specialized processing pipelines** optimized for different content types:

1. **AI Tools Pipeline**: Technical tutorials, coding workflows, tool demonstrations
2. **Sports Pipeline**: Training protocols, exercise science, biomechanical analysis

Both pipelines share the same core infrastructure (extraction, auto-enhancement, MCP KB storage) but use domain-specific agents and templates for optimal extraction quality.

---

## When to Use Which Pipeline

### Use **AI Tools Pipeline** for:

- Claude Code tutorials and workflows
- Development tool demonstrations (Cursor, VS Code, n8n, etc.)
- Programming tutorials (Python, JavaScript, APIs, etc.)
- Technical setup guides and configurations
- Workflow automation content
- MCP server integrations
- AI agent development

**Key Indicators**:
- Video demonstrates code or commands
- Focus on tools, software, or technical workflows
- Contains slash commands, CLI operations, or code snippets
- Presenter shows screen with IDE or terminal

**Command**: `/process-youtube <youtube_url>`

---

### Use **Sports Pipeline** for:

- Exercise technique demonstrations
- Training program design and periodization
- Scientific reviews of training methods
- Biomechanical analysis of movements
- Injury prevention and rehabilitation
- Evidence-based coaching content
- Strength, endurance, or hybrid athlete training

**Key Indicators**:
- Video demonstrates physical exercises
- Focus on training protocols (sets/reps/frequency)
- Cites scientific research or studies
- Explains biomechanics or physiology
- Shows movement technique or form cues
- Discusses programming, periodization, or recovery

**Command**: `/process-sports-video <youtube_url>`

---

## Pipeline Comparison

| Feature | AI Tools Pipeline | Sports Pipeline |
|---------|------------------|-----------------|
| **Agent** | `@youtube-transcript-analyzer` | `@sports-transcript-analyzer` |
| **Template** | `detailed_summary_template.md` | `sports_summary_template.md` |
| **Storage Script** | `store_in_mcp_kb.py` | `store_sports_in_mcp_kb.py` |
| **Slash Command** | `/process-youtube` | `/process-sports-video` |
| **Key Extractions** | Commands, tools, workflows, code | Protocols, evidence, biomechanics, WHY |
| **Tags** | `tool-*`, `feature-*`, `content-type-*` | `sport-*`, `evidence-tier-*`, `content-*` |
| **Output Focus** | Actionable technical instructions | Evidence-backed training guidance |

---

## Shared Infrastructure

Both pipelines use the same core components:

### 1. **Extraction** (Identical)
```bash
uv run python main.py extract "https://youtube.com/watch?v=VIDEO_ID"
```
- Downloads transcript via yt-dlp
- Creates raw text file
- Works for all video types

### 2. **Auto-Enhancement** (Identical)
```bash
uv run python -m src.processing.auto_enhancer raw_text_*.txt
```
- Applies 174+ mapped corrections
- Fixes common transcription errors
- Domain-agnostic (works for both)

**Corrections include**:
- "mate and" → "n8n"
- "clawed code" → "Claude Code"
- "zero" → "v0"
- "hybrid athlete" transcription fixes
- Scientific terminology corrections

### 3. **unified-memory Storage** (Similar)
Both pipelines store in the same unified-memory instance, but with different tagging:

**AI Tools Tags**:
```
youtube-knowledge-base
video-{VIDEO_ID}
channel-{channel-name}
tool-{tool-name}
feature-{feature-name}
content-type-{type}
```

**Sports Tags**:
```
youtube-knowledge-base
video-{VIDEO_ID}
channel-{channel-name}
content-type-sports
sport-{discipline}
evidence-tier-{1-4}
content-{type}
```

### 4. **Querying** (Automatically Separated)

Semantic search naturally separates domains:

**AI Query**:
```
mcp__unified-memory__memory_search("Claude Code context window management")
```
→ Returns AI tool content only

**Sports Query**:
```
mcp__unified-memory__memory_search("Bulgarian split squat protocol")
```
→ Returns sports content only

**Tag-Based Filtering**:
```
# AI tools
mcp__unified-memory__memory_search(["tool-claude-code"])

# Sports
mcp__unified-memory__memory_search(["sport-ultra-running", "evidence-tier-1"])
```

---

## Detailed Pipeline Workflows

### AI Tools Pipeline Workflow

```mermaid
graph TD
    A[YouTube URL] --> B[Extract Transcript]
    B --> C[Auto-Enhance 174+ corrections]
    C --> D[@youtube-transcript-analyzer]
    D --> E[Analysis JSON]
    E --> F[Generate Detailed Summary]
    F --> G[Prepare MCP KB Ready]
    G --> H[Store in MCP KB]
    H --> I[Tag: tool-*, feature-*]
    I --> J[Query: AI Development]
```

**Command**: `/process-youtube "https://youtube.com/watch?v=VIDEO_ID"`

**Output Files**:
- `workspace/analysis/{VIDEO_ID}_analysis.json`
- `workspace/summaries/{VIDEO_ID}_detailed_summary.md`
- `workspace/mcp_ready/{VIDEO_ID}_mcp_ready.txt`

**Tags Applied**:
- `tool-claude-code`, `tool-cursor`, `tool-n8n`, etc.
- `feature-agents`, `feature-mcp`, `feature-context-window`, etc.
- `content-type-tutorial`, `content-type-command-reference`, etc.

**Key Extractions**:
- Tools and technologies used
- Executable commands (`/scout`, `git push`, `uv run`)
- Key concepts (Scout-Plan-Build, R&D Framework)
- Workflows and step-by-step guides
- Implementation details (setup, configuration, code)

---

### Sports Pipeline Workflow

```mermaid
graph TD
    A[YouTube URL] --> B[Extract Transcript]
    B --> C[Auto-Enhance 174+ corrections]
    C --> D[@sports-transcript-analyzer]
    D --> E[Sports Analysis JSON]
    E --> F[Generate Sports Summary]
    F --> G[Prepare Sports MCP KB Ready]
    G --> H[Store in MCP KB]
    H --> I[Tag: sport-*, evidence-tier-*]
    I --> J[Query: Training Protocols]
    J --> K[Optional: Neo4j Graph Integration]
```

**Command**: `/process-sports-video "https://youtube.com/watch?v=VIDEO_ID" sport="ultra-running"`

**Output Files**:
- `workspace/analysis/{VIDEO_ID}_sports_analysis.json`
- `workspace/summaries/{VIDEO_ID}_sports_summary.md`
- `workspace/mcp_ready/{VIDEO_ID}_sports_mcp_ready.txt`

**Tags Applied**:
- `sport-ultra-running`, `sport-hyrox`, `sport-strength-training`, etc.
- `evidence-tier-1` through `evidence-tier-4`
- `content-exercise-technique`, `content-programming-protocol`, etc.

**Key Extractions**:
- Exercise protocols (volume, frequency, intensity, tempo)
- Scientific citations (author, year, study type, evidence tier)
- Biomechanical principles (joint angles, muscle activation, force vectors)
- WHY reasoning (biomechanical, physiological, tactical)
- Implementation details (setup, execution, common errors)
- Equipment specifications and alternatives
- Progression criteria and injury modifications

---

## Agent Specialization

### @youtube-transcript-analyzer (AI Tools)

**Optimized For**:
- Tool identification (Claude Code 2.0, GitHub, UV)
- Command extraction (`/scout-plan-build`, `git commit`)
- Workflow analysis (multi-step processes)
- Code snippet extraction
- Configuration details

**Output Structure**:
```json
{
  "tools_mentioned": ["Claude Code 2.0", "UV", "GitHub"],
  "commands": ["/scout", "/context", "git push"],
  "key_concepts": ["Scout-Plan-Build", "R&D Framework"],
  "workflows": ["Complete workflow descriptions"],
  "implementation_details": {
    "setup_steps": [...],
    "code_snippets": [...]
  }
}
```

---

### @sports-transcript-analyzer (Sports)

**Optimized For**:
- Protocol extraction (3x6-8, 2x/week, 12-20kg)
- Evidence identification (McCurdy et al. 2010, Tier 2 RCT)
- Biomechanics quantification (25% quad activation increase)
- WHY reasoning (physiological mechanisms)
- Injury considerations and modifications

**Output Structure**:
```json
{
  "exercises_demonstrated": [{
    "name": "Bulgarian Split Squat",
    "protocol": {
      "volume": "3 sets x 6-8 reps per leg",
      "frequency": "2x per week",
      "intensity": "12-20kg dumbbells"
    }
  }],
  "scientific_citations": [{
    "citation": "McCurdy et al. 2010",
    "study_type": "RCT",
    "evidence_tier": 2,
    "finding": "25% higher quad activation"
  }],
  "biomechanical_principles": [...],
  "why_reasoning": {
    "biomechanical": "...",
    "physiological": "...",
    "tactical": "..."
  }
}
```

---

## Quality Separation Benefits

### 1. **Better Extraction Quality**

**AI Tools**:
- Commands extracted as executable syntax (not sports "sets/reps")
- Tool versions captured accurately
- Code snippets preserved with proper formatting

**Sports**:
- Protocols extracted systematically (volume/frequency/intensity)
- Evidence classified by tier (meta-analysis vs opinion)
- Biomechanics quantified (degrees, percentages, force)

### 2. **Cleaner Queries**

**Before (Single Pipeline)**:
```
Query: "Claude Code context management"
Returns: Mix of AI tools + sports content mentioning "context"
```

**After (Dual Pipeline)**:
```
Query: "Claude Code context management"
Returns: Only AI tool content (semantic + tag separation)
```

### 3. **Domain-Specific Templates**

**AI Tools Summary** includes:
- Tools & Technologies
- Commands & Syntax
- Workflows & Step-by-Step Guides
- Implementation Details (setup, code, config)

**Sports Summary** includes:
- Scientific Evidence & Research Citations
- Exercise Protocols
- Biomechanical Principles
- WHY Reasoning
- Injury Considerations
- Training Context & Integration

---

## Neo4j Integration (Sports Only)

The sports pipeline includes Neo4j mapping for knowledge graph integration:

```json
"neo4j_mapping": {
  "exercise_node_id": "ex_bulgarian_split_squat",
  "why_reasoning_tiers": {
    "foundation": "biomechanical + physiological (400-600 tokens)",
    "methodology": "programming_logic (250-350 tokens)",
    "implementation": "implementation_details (150-200 tokens)",
    "personalization": "injury_modifications (100-150 tokens)"
  },
  "scientific_paper_ids": ["paper_mccurdy_2010"],
  "equipment_ids": ["eq_kettlebell", "eq_dumbbell_pair"]
}
```

This enables direct import to the Neo4j knowledge graph (see `Sports/implementation_guides/02_knowledge_graph_expansion.md` for full schema).

---

## File Organization

```
.claude/
├── agents/
│   ├── youtube-transcript-analyzer.md    # AI tools agent
│   └── sports-transcript-analyzer.md     # Sports agent
├── commands/
│   ├── process-youtube.md                 # AI tools command
│   └── process-sports-video.md            # Sports command

src/
├── templates/
│   ├── detailed_summary_template.md       # AI tools template
│   └── sports_summary_template.md         # Sports template

scripts/
├── store_in_mcp_kb.py                     # AI tools storage
└── store_sports_in_mcp_kb.py              # Sports storage

workspace/
├── analysis/
│   ├── {VIDEO_ID}_analysis.json           # AI tools
│   └── {VIDEO_ID}_sports_analysis.json    # Sports
├── summaries/
│   ├── {VIDEO_ID}_detailed_summary.md     # AI tools
│   └── {VIDEO_ID}_sports_summary.md       # Sports
└── mcp_ready/
    ├── {VIDEO_ID}_mcp_ready.txt           # AI tools
    └── {VIDEO_ID}_sports_mcp_ready.txt    # Sports
```

---

## Quick Start Examples

### Example 1: Process IndyDevDan Claude Code Video

```bash
# AI Tools Pipeline (default)
/process-youtube "https://youtube.com/watch?v=nGhsgdQplHw"

# Extracts:
# - Tools: Claude Code 2.0, UV, Gemini, Codex
# - Commands: /scout, /plan, /build, /config autocompact false
# - Concepts: Scout-Plan-Build, R&D Framework
# - Workflows: Three-phase development pattern

# Tags: tool-claude-code, feature-agents, content-type-tutorial
```

### Example 2: Process Bulgarian Split Squat Training Video

```bash
# Sports Pipeline
/process-sports-video "https://youtube.com/watch?v=SPORTS_ID" sport="strength-training"

# Extracts:
# - Exercise: Bulgarian Split Squat
# - Protocol: 3x6-8, 2x/week, 12-20kg, 3-1-1 tempo
# - Evidence: McCurdy et al. 2010 (RCT, Tier 2)
# - Biomechanics: 25% quad activation increase, 15-20° ROM increase
# - WHY: Biomechanical/physiological/tactical reasoning

# Tags: sport-strength-training, evidence-tier-2, content-exercise-technique
```

### Example 3: Process Hybrid Athlete Training Video

```bash
# Sports Pipeline with hybrid athlete focus
/process-sports-video "https://youtube.com/watch?v=HYBRID_ID" sport="hybrid-athlete"

# Extracts:
# - Concurrent training principles
# - Interference mitigation strategies
# - Recovery protocols
# - Evidence on strength + endurance balance

# Tags: sport-hybrid-athlete, sport-concurrent-training, evidence-tier-*
```

---

## Migration Guide

### If You Have Existing Videos

**Option 1: Re-process with correct pipeline**
```bash
# Old video was AI tool content but processed generically
/process-youtube "OLD_VIDEO_URL"

# Old video was sports content but processed generically
/process-sports-video "OLD_VIDEO_URL" sport="ultra-running"
```

**Option 2: Keep existing data**
- Both pipelines query the same MCP KB
- Semantic search will naturally separate domains
- No migration required unless you want sports-specific structure

---

## Best Practices

### 1. **Choose the Right Pipeline**

Ask: "What is the primary content?"
- **Code, tools, workflows** → AI Tools Pipeline
- **Exercise, training, physiology** → Sports Pipeline

### 2. **Use Domain Tags for Precision**

**AI Tools**:
```
memory_search(["tool-claude-code", "feature-context-window"])
```

**Sports**:
```
memory_search(["sport-ultra-running", "evidence-tier-1"])
```

### 3. **Leverage Evidence Tiers**

For sports content, filter by evidence quality:
```
# Only meta-analyses and RCTs
memory_search(["evidence-tier-1"])
memory_search(["evidence-tier-2"])

# Exclude expert opinion
memory_search("training protocol") + exclude tier-4
```

### 4. **Combine Tags for Specific Queries**

```
# High-evidence hybrid athlete protocols
memory_search(["sport-hybrid-athlete", "evidence-tier-1", "content-programming-protocol"])

# Claude Code agent tutorials
memory_search(["tool-claude-code", "feature-agents", "content-type-tutorial"])
```

---

## Troubleshooting

### Wrong Pipeline Used

**Symptom**: AI video processed with sports pipeline (or vice versa)

**Solution**:
```bash
# Delete incorrect entry from MCP KB
mcp__unified-memory__memory_delete(content_hash="...")

# Re-process with correct pipeline
/process-youtube "VIDEO_URL"  # or /process-sports-video
```

### Mixed Content Video

**Symptom**: Video covers both AI tools AND training (e.g., "Using Claude Code to design workout programs")

**Solution**: Choose primary focus
- **Primary = AI tool usage** → AI Tools Pipeline
- **Primary = workout protocols** → Sports Pipeline
- Or process twice with different focus if both aspects are valuable

### Query Returns Wrong Domain

**Symptom**: Searching for "Claude context" returns sports content about "training context"

**Solution**: Use tag-based filtering
```
# Instead of:
memory_search("Claude context")  # Ambiguous

# Use:
memory_search(["tool-claude-code"]) + memory_search("context window")
```

---

## Performance Metrics

### Processing Time (per video)

Both pipelines: **~2 minutes** (10x faster than old manual workflow)

**Breakdown**:
- Extract: 30 seconds
- Auto-enhance: 5 seconds
- Agent analysis: 30-60 seconds
- Summary generation: 10 seconds
- Storage: instant

### Storage Efficiency

**AI Tools**: ~800-1200 tokens per video
**Sports**: ~1000-1500 tokens per video (more detailed protocols)

Both use unified-memory with efficient semantic search.

---

## Future Enhancements

### Planned Additions

1. **Auto-Detection**: Automatically choose pipeline based on video content
2. **Batch Processing**: Process multiple videos with correct pipeline
3. **Neo4j Integration**: Direct sports content → knowledge graph import
4. **Cross-Domain Links**: Connect AI tools used for sports app development

### Request Features

If you need additional pipelines (e.g., business/marketing, nutrition, etc.), the dual-pipeline architecture makes adding new domains straightforward:

1. Create new specialized agent (`.claude/agents/domain-analyzer.md`)
2. Create domain template (`src/templates/domain_template.md`)
3. Create storage script (`scripts/store_domain_in_mcp_kb.py`)
4. Create slash command (`.claude/commands/process-domain-video.md`)

---

## Summary

**Two Pipelines, One System**

✅ **AI Tools Pipeline**: Optimized for technical tutorials and coding workflows
✅ **Sports Pipeline**: Optimized for training protocols and exercise science
✅ **Shared Infrastructure**: Same extraction, enhancement, and storage
✅ **Automatic Separation**: Semantic search naturally separates domains
✅ **Tag-Based Precision**: Filter by domain, evidence tier, or content type

**When in doubt**: Use `/process-youtube` for AI tools, `/process-sports-video` for training content.

---

**Version**: 1.0
**Last Updated**: 2025-01-18
**Maintained By**: AI Knowledge Base System
