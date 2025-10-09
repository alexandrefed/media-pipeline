# Deprecated Scripts Archive

This directory contains scripts from previous project phases that are no longer part of the active workflow. They are preserved for historical reference and learning purposes.

## Directory Structure

```
deprecated_scripts/
├── chunkers/               # Video-specific manual chunking scripts (18 files)
├── postgresql_imports/     # PostgreSQL database import scripts (21 files)
├── experimental/           # Experimental and one-off scripts (6 files)
└── one_off/                # One-time video processing scripts (2 files)
```

---

## chunkers/ (18 files)

**Phase**: Manual Chunking Workflow (July 2025)

**Purpose**: Video-specific chunking scripts created for individual videos during the manual PostgreSQL import phase.

**Files**:
- `manual_chunker_3_folders.py`
- `manual_chunker_ai_labs_n8n_mcp.py`
- `manual_chunker_ai_labs_superClaude.py`
- `manual_chunker_claude_commands.py`
- `manual_chunker_claude_engineering_forever.py`
- `manual_chunker_claude_sub_agents.py`
- `manual_chunker_liam_ottley_9_ai_tools.py`
- `manual_chunker_liam_ottley_comprehensive.py`
- `manual_chunker_liam_ottley_entrepreneur.py`
- `manual_chunker_mcp.py`
- `manual_chunker_n8n_agents.py`
- `manual_chunker_n8n_agents_v2.py`
- `manual_chunker_n8n_automation_video.py`
- `manual_chunker_nick_saraev_comprehensive.py`
- `manual_chunker_openmemory.py`
- `manual_chunker_sean_kochel_claude_features.py`
- `manual_chunker_vibe_code.py`
- `manual_chunker_voice_claude.py`

**Why Deprecated**:
- Phase 1 uses agent-based analysis instead of manual chunking
- MCP KB Memory storage instead of PostgreSQL manual import
- These were video-specific, not reusable core functionality

**Historical Value**:
- Shows evolution of chunking strategies
- Contains video-specific insights that informed agent design
- Demonstrates manual quality standards that agents now automate

---

## postgresql_imports/ (21 files)

**Phase**: PostgreSQL VPS Deployment (July 2025)

**Purpose**: Import manually chunked videos into PostgreSQL database with pgvector embeddings.

**Files**:
- `import_manual_chunks.py` - Generic chunk importer
- `import_all_chunks.py` - Batch import all chunks
- `import_remaining_videos.py` - Import queue processor
- Plus 18 video-specific importers (import_*_chunks.py)

**Why Deprecated**:
- Phase 1 uses MCP KB Memory instead of PostgreSQL
- Agent analysis replaces manual chunking workflow
- Streamlined process eliminates need for separate import step

**Historical Value**:
- Documents PostgreSQL schema and import process
- Shows embedding generation workflow
- Contains 29 videos worth of processing insights

---

## experimental/ (6 files)

**Phase**: Various exploratory phases

**Purpose**: Experimental features and one-off analysis scripts.

**Files**:
- `adaptive_video_processor.py` - Experimental adaptive processing
- `analyze_first_video.py` - Initial proof of concept
- `enhance_with_learning.py` - Early auto-enhancement attempt
- `reprocess_video.py` - Video reprocessing utility
- `manual_chunker.py` - Original generic manual chunker
- Plus other experimental utilities

**Why Deprecated**:
- Features either incorporated into core system or abandoned
- Superseded by more robust implementations
- One-off scripts for specific analysis tasks

**Historical Value**:
- Shows feature exploration and iteration
- Documents dead ends and learning
- Contains ideas that might be revisited

---

## one_off/ (2 files)

**Phase**: Manual Chunking Workflow

**Purpose**: One-time scripts for specific video processing needs.

**Files**:
- `manual_chunk_autogen_video.py`
- `manual_chunk_programmable_video.py`

**Why Deprecated**:
- Video-specific, not generalizable
- Replaced by agent-based analysis

---

## Migration to Phase 1

**Old Workflow** (Deprecated Scripts):
```
Extract → Manual Enhance (15 min) → Manual Chunk (10 min)
→ Import to PostgreSQL → Query via API
```

**New Workflow** (Active Scripts):
```
Extract → Auto-Enhance (5 sec) → Agent Analysis (30 sec)
→ Store in MCP KB → Query Instantly
```

**Key Improvements**:
- 12.5x faster processing
- 10-100x better quality through specialized agents
- Native Claude Code integration
- No manual chunking required

---

## When to Reference These Scripts

**Good Reasons**:
- Understanding historical approach to chunking
- Learning about PostgreSQL + pgvector implementation
- Studying video-specific processing strategies
- Comparing manual vs automated quality

**Bad Reasons**:
- Using them in current workflow (use active scripts instead)
- Creating new video-specific chunkers (use agents instead)
- Importing to PostgreSQL (use MCP KB Memory instead)

---

## Further Reading

- `../../archive/old_workflows/manual_chunking/` - Detailed manual chunking documentation
- `../../archive/old_workflows/postgresql/` - PostgreSQL VPS setup and API documentation
- `../../STREAMLINED_WORKFLOW.md` - Current Phase 1 agentic workflow
- `../../docs/PIPELINE_ENHANCEMENT_SUMMARY.md` - Latest pipeline improvements

---

**Last Updated**: January 2025 (Phase 1 Cleanup)
**Total Deprecated Scripts**: 47 files
**Reason for Preservation**: Historical reference, learning resource, architectural evolution documentation
