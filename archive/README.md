# Archive Directory

This directory contains historical documentation and files from previous phases of the AI Knowledge Base project. All files are preserved for reference but are not part of the current workflow.

## 📁 Directory Structure

### `old_workflows/`
Documentation from previous project phases:

#### `postgresql/`
PostgreSQL + VPS API phase (July 2025):
- AI_KNOWLEDGE_BASE_GUIDE.md - Comprehensive VPS database setup
- VPS_API_COMPLETE_SETUP.md - API server deployment
- API_SERVER_IMPLEMENTATION.md - FastAPI implementation details
- VPS_API_INTEGRATION_SUMMARY.md - System architecture summary

#### `manual_chunking/`
Manual chunking workflow (July 2025):
- CLAUDE_CODE_WORKFLOW.md - Manual enhancement and chunking process
- IMPLEMENTATION_LESSONS_LEARNED.md - Lessons from 29 videos processed

#### `video_tracking/`
Old video processing queue:
- list.md - Historical video tracking list (29 videos ✅ DONE)

### `unused/`
Features that were explored but not adopted:

#### `custom_gpt/`
OpenAI Custom GPT integration (July 2025):
- CUSTOM_GPT_SETUP.md - Setup instructions
- CUSTOM_GPT_INSTRUCTIONS.md - GPT configuration
- CUSTOM_GPT_AUTH_TROUBLESHOOTING.md - Authentication debugging

#### `commands/`
Obsolete Claude Code commands:
- check-status.md - Used old pending/ directory structure
- list-pending.md - Used old pending/ directory structure
- resume-video.md - Used old pending/ directory structure

### `legacy_scripts/`
Old Python import scripts from PostgreSQL phase (14 files):
- add_*_source.py scripts for database imports

### `old_workflows/pending/` & `old_workflows/processed/` ⚠️ LOCAL ONLY
Original manual chunking workflow directories:
- **65 files preserved locally** - enhanced transcripts and manual chunks
- **NOT uploaded to VPS** - these files exist only in local repository
- **NOT in git** - excluded by .gitignore to keep repo size manageable
- **Important**: Do not delete these directories - they contain processed work not yet migrated

### `test_files/`
Test and experimental files:
- openapi_schema.json

## 🔄 Evolution of the Project

### Phase 1: PostgreSQL VPS + Manual Chunking (July 2025)
- **Workflow**: Extract → Manual enhance (15 min) → Manual chunk (10 min) → PostgreSQL → API
- **Result**: 29 videos, 435 chunks, high quality but time-intensive
- **Storage**: PostgreSQL 16 with pgvector on VPS
- **Access**: REST API at api.vecia.fr

### Phase 2: Agentic Workflow + MCP KB (October 2025) - **CURRENT**
- **Workflow**: Extract → Auto-enhance (5s) → Agent analyze (30s) → MCP KB Memory
- **Result**: 12.5x faster processing with consistent quality
- **Storage**: MCP KB Memory (local Claude Code integration)
- **Access**: Direct Claude Code queries via MCP

### Key Improvements in Phase 2:
1. **Auto-enhancement**: 174+ corrections applied automatically
2. **Specialized Agents**: Channel-specific analyzers (IndyDevDan, Sean Kochel)
3. **R&D Framework**: Intelligent orchestration and delegation
4. **Simplified Storage**: MCP KB Memory instead of VPS infrastructure
5. **Better Integration**: Native Claude Code experience

## 📖 Why Files Were Archived

### PostgreSQL Documentation
Still technically functional but no longer the primary workflow. The PostgreSQL VPS contains **29 videos with 435 chunks** that can still be queried via API if needed. However, **65+ additional processed files exist locally** in `archive/old_workflows/processed/` that were never uploaded to VPS. New videos use the MCP KB Memory approach for better Claude Code integration.

### Custom GPT Files
OpenAI Custom GPT integration was explored but not adopted. The agentic workflow with MCP KB Memory provides better integration with Claude Code without requiring external API configurations.

### Old Commands
Commands like `/check-status`, `/list-pending`, and `/resume-video` referenced the old `pending/` and `processed/` directory structure from the manual chunking workflow. These have been superseded by the `workspace/` organization and agentic processing pipeline.

### Video Tracking List
`list.md` tracked 29 videos through the manual processing queue. This has been replaced by the `workspace/` directory structure where files naturally progress from `raw/` → `enhanced/` → `analysis/` → `mcp_ready/`.

## 🎯 Current Documentation

For current workflow documentation, see:
- **STREAMLINED_WORKFLOW.md** - Complete Phase 2 workflow
- **CLAUDE.md** - Project overview and structure
- **PHASE1_COMPLETE.md** - Agentic patterns implementation
- **DOCUMENTATION_INDEX.md** - Complete documentation map

## 💡 Accessing Archived Systems

### PostgreSQL VPS (Still Operational)
If you need to access the 29 videos with 435 chunks in the old system:

```bash
# Database connection
Host: 85.25.172.47
Port: 5433
Database: aidb
Schema: ai_kb

# API query
curl -X POST http://85.25.172.47:8001/api/v1/query \
  -H "X-API-Key: ai-knowledge-base-api-key-2025-secure-for-openai-custom-gpt" \
  -H "Content-Type: application/json" \
  -d '{"query": "your search", "max_results": 10}'
```

See archived documentation in `old_workflows/postgresql/` for complete details.

---

**Nothing is deleted** - all historical work is preserved here for reference, learning, and potential future use.
