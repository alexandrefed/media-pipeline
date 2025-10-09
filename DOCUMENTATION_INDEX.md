# Documentation Index 📚

Complete guide to all documentation in the AI Knowledge Base project. Start here to find what you need.

## 🎯 Getting Started

### New to the Project?
1. **[README.md](README.md)** - Project overview and quick start
2. **[STREAMLINED_WORKFLOW.md](STREAMLINED_WORKFLOW.md)** - Complete Phase 1 workflow
3. **[CLAUDE.md](CLAUDE.md)** - Claude Code instructions

### Want to Process Videos?
1. **[STREAMLINED_WORKFLOW.md](STREAMLINED_WORKFLOW.md)** - Step-by-step guide
2. **[.claude/commands/process-youtube.md](.claude/commands/process-youtube.md)** - `/process-youtube` command
3. **[PHASE1_COMPLETE.md](PHASE1_COMPLETE.md)** - Agentic patterns explained

## 📁 Documentation by Category

### Core Documentation

#### Project Overview
- **[README.md](README.md)** - Main project README with Phase 1 features
- **[CLAUDE.md](CLAUDE.md)** - Complete project instructions for Claude Code
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines for developers
- **[LICENSE](LICENSE)** - MIT License

#### Workflow Guides
- **[STREAMLINED_WORKFLOW.md](STREAMLINED_WORKFLOW.md)** - Complete Phase 1 workflow (START HERE)
  - Extract → Auto-enhance → Orchestrate → Analyze → Store
  - 12.5x faster than old workflow
  - MCP KB Memory integration

### Specialized Agents

Located in `.claude/agents/` - these are the intelligent analysts that process videos:

#### Active Agents
- **[youtube-transcript-analyzer.md](.claude/agents/youtube-transcript-analyzer.md)** - General-purpose analyzer
  - Filters fragments, extracts real tools
  - Identifies executable commands
  - Captures workflows and concepts
  - Synthesizes actionable takeaways
  - Extracts technical implementation details (setup, config, code)

- **[youtube-processing-orchestrator.md](.claude/agents/youtube-processing-orchestrator.md)** - R&D Framework orchestrator
  - Detects channel automatically
  - Routes to appropriate specialist
  - Coordinates workflow execution
  - Implements Reduce and Delegate pattern

- **[indydevdan-analyzer.md](.claude/agents/indydevdan-analyzer.md)** - Advanced Claude Code specialist
  - Extracts agentic coding patterns
  - Captures philosophical frameworks
  - Identifies prompt engineering techniques
  - Recognizes context management strategies
  - Documents exact commands, file structures, performance metrics

- **[seankochel-analyzer.md](.claude/agents/seankochel-analyzer.md)** - Productivity specialist
  - Extracts step-by-step methodologies
  - Captures time-saving metrics
  - Identifies professional workflow principles
  - Recognizes tool integration patterns
  - Documents step-by-step procedures with exact settings

### Custom Commands

Located in `.claude/commands/` - slash commands for Claude Code:

- **[process-youtube.md](.claude/commands/process-youtube.md)** - Complete video processing
  - `/process-youtube <URL>` - One command for entire workflow
  - Implements Scout-Plan-Build pattern
  - Chains Extract → Enhance → Analyze → Store

### Learning System

Located in `learning/` - AI learning and improvement:

- **[processing_knowledge_base.json](learning/processing_knowledge_base.json)** - 174+ transcription corrections
  - AI tool names ("mate and" → "n8n")
  - Technical terms corrections
  - Channel-specific patterns
  - Content type guidelines

- **[processing_history.md](learning/processing_history.md)** - Processing logs
  - Video processing history
  - Learnings from each video
  - Quality metrics
  - Continuous improvement notes

### Active Scripts

Located in `scripts/` - only essential utilities for Phase 1 workflow:

- **[scripts/streamlined_process.py](scripts/streamlined_process.py)** - Automated video processing
  - Complete pipeline automation
  - Extract → Auto-enhance → Prepare for analysis

- **[scripts/store_in_mcp_kb.py](scripts/store_in_mcp_kb.py)** - MCP KB Memory preparation
  - Formats agent analysis for storage
  - Creates _mcp_kb_ready.txt files

- **[scripts/README.md](scripts/README.md)** - Scripts directory documentation
  - Usage examples for each script
  - Guidelines for adding new scripts

### Technical Reference

- **[ai_docs/tools/uv_package_manager.md](ai_docs/tools/uv_package_manager.md)** - uv usage guide
  - 10-100x faster than pip
  - Installation instructions
  - Common commands
  - Best practices

- **[docs/PIPELINE_ENHANCEMENT_SUMMARY.md](docs/PIPELINE_ENHANCEMENT_SUMMARY.md)** - Implementation details enhancement
  - New `implementation_details` field in analysis schema
  - Extraction guidelines for technical content
  - Validation checklist for agents
  - Before/after examples

- **[docs/IMPLEMENTATION_DETAILS_EXAMPLE.json](docs/IMPLEMENTATION_DETAILS_EXAMPLE.json)** - Complete example analysis
  - Shows full `implementation_details` structure
  - Setup steps, configuration, code snippets
  - Technical specifications and troubleshooting
  - Reference template for agents

- **[.env.example](.env.example)** - Environment configuration template
  - Database connection settings
  - API server configuration
  - Processing parameters

## 🗄️ Historical Documentation

### Archived Workflows

Located in `archive/` - preserved for reference but not current workflow:

#### PostgreSQL VPS Phase (July 2025)
**Location**: `archive/old_workflows/postgresql/`

- **AI_KNOWLEDGE_BASE_GUIDE.md** - Comprehensive VPS database setup
- **VPS_API_COMPLETE_SETUP.md** - API server deployment on VPS
- **API_SERVER_IMPLEMENTATION.md** - FastAPI implementation details
- **VPS_API_INTEGRATION_SUMMARY.md** - Architecture summary

**What it was**: 29 videos with 435 high-quality manual chunks stored in PostgreSQL with pgvector. REST API for querying. Time-intensive but high quality.

**Why archived**: Phase 1 agentic workflow is 12.5x faster with comparable quality using MCP KB Memory.

#### Manual Chunking Workflow (July 2025)
**Location**: `archive/old_workflows/manual_chunking/`

- **CLAUDE_CODE_WORKFLOW.md** - Manual enhancement and chunking process
- **IMPLEMENTATION_LESSONS_LEARNED.md** - Lessons from 29 videos
- **transcript-enhancer/** - Interactive enhancement agent

**What it was**: Extract → Manual enhance (15 min) → Manual chunk (10 min) → PostgreSQL

**Why archived**: Auto-enhancement (5 sec) + specialized agents (30 sec) is much faster.

#### Video Tracking (July 2025)
**Location**: `archive/old_workflows/video_tracking/`

- **list.md** - Historical video processing queue (29 videos ✅ DONE)

**Why archived**: Replaced by `workspace/` directory organization where files naturally progress from `raw/` → `enhanced/` → `analysis/` → `mcp_ready/`

### Deprecated Scripts (Phase 1 Cleanup - January 2025)

**Location**: `archive/deprecated_scripts/`

- **[archive/deprecated_scripts/README.md](archive/deprecated_scripts/README.md)** - Complete documentation of 47 deprecated scripts
  - chunkers/ - 18 video-specific manual chunking scripts
  - postgresql_imports/ - 21 PostgreSQL import scripts
  - experimental/ - 6 experimental and one-off scripts

**What was archived**: All scripts from PostgreSQL VPS phase and manual chunking workflow

**Why archived**: Phase 1 uses agent-based analysis with MCP KB Memory instead of manual chunking and PostgreSQL

**Scripts remaining**: 2 active scripts (streamlined_process.py, store_in_mcp_kb.py)

### Milestone Documentation

**Location**: `archive/milestones/`

- **PHASE1_COMPLETE.md** - Phase 1 agentic workflow completion summary
- **HOUSEKEEPING_COMPLETE.md** - Project organization and cleanup milestone

**Why archived**: Historical milestones preserved for reference but not needed for day-to-day work

### Unused Features

Located in `archive/unused/` - explored but not adopted:

#### Custom GPT Integration
**Location**: `archive/unused/custom_gpt/`

- **CUSTOM_GPT_SETUP.md** - OpenAI Custom GPT setup
- **CUSTOM_GPT_INSTRUCTIONS.md** - GPT configuration
- **CUSTOM_GPT_AUTH_TROUBLESHOOTING.md** - Authentication debugging

**Why not used**: Phase 1 agentic workflow with MCP KB Memory provides better Claude Code integration without external API configuration.

#### Obsolete Commands
**Location**: `archive/unused/commands/`

- **check-status.md** - Old status check (used `pending/` directory)
- **list-pending.md** - Old pending list (used `pending/` directory)
- **resume-video.md** - Old resume command (used `pending/` directory)
- **enhance-transcript.md** - Interactive enhancement (superseded by auto-enhancer)

**Why not used**: These referenced the old `pending/` and `processed/` directory structure from manual chunking workflow. Replaced by `workspace/` organization.

## 🎓 Learning Path

### For New Contributors

1. **Understand the System**
   - Read [README.md](README.md) for overview
   - Review [PHASE1_COMPLETE.md](PHASE1_COMPLETE.md) for agentic patterns
   - Study [CLAUDE.md](CLAUDE.md) for project structure

2. **Learn the Workflow**
   - Follow [STREAMLINED_WORKFLOW.md](STREAMLINED_WORKFLOW.md)
   - Try processing a video with `/process-youtube`
   - Review agent files in `.claude/agents/`

3. **Understand the Agents**
   - Read agent instructions to understand their expertise
   - See how orchestrator detects and delegates
   - Study channel-specific patterns

4. **Explore the Learning System**
   - Check `learning/processing_knowledge_base.json` for corrections
   - Review `learning/processing_history.md` for insights
   - Understand continuous improvement approach

### For Understanding History

1. **See What Was Built Before**
   - Read [archive/README.md](archive/README.md) for overview
   - Review PostgreSQL VPS documentation
   - Understand manual chunking workflow

2. **Learn Why Changes Were Made**
   - Compare [STREAMLINED_WORKFLOW.md](STREAMLINED_WORKFLOW.md) with archived manual workflow
   - See quality improvements (10-100x)
   - Understand speed improvements (12.5x)

## 🔍 Finding Documentation

### By Topic

**Video Processing**:
- [STREAMLINED_WORKFLOW.md](STREAMLINED_WORKFLOW.md)
- [.claude/commands/process-youtube.md](.claude/commands/process-youtube.md)

**Agentic Patterns**:
- [PHASE1_COMPLETE.md](PHASE1_COMPLETE.md)
- [.claude/agents/youtube-processing-orchestrator.md](.claude/agents/youtube-processing-orchestrator.md)

**Channel-Specific Analysis**:
- [.claude/agents/indydevdan-analyzer.md](.claude/agents/indydevdan-analyzer.md)
- [.claude/agents/seankochel-analyzer.md](.claude/agents/seankochel-analyzer.md)

**Project Setup**:
- [README.md](README.md)
- [CLAUDE.md](CLAUDE.md)

**Tool Usage**:
- [ai_docs/tools/uv_package_manager.md](ai_docs/tools/uv_package_manager.md)

**Historical Context**:
- [archive/README.md](archive/README.md)

### By File Location

**Root Directory** (5 files):
- README.md, CLAUDE.md, STREAMLINED_WORKFLOW.md, PHASE1_COMPLETE.md, HOUSEKEEPING_COMPLETE.md

**`.claude/` Directory**:
- `agents/` - 4 specialized analysts
- `commands/` - 1 custom command

**`learning/` Directory**:
- processing_knowledge_base.json, processing_history.md

**`ai_docs/` Directory**:
- `tools/uv_package_manager.md`

**`archive/` Directory**:
- `old_workflows/` - PostgreSQL VPS, manual chunking, video tracking
- `unused/` - Custom GPT, obsolete commands

## 📊 Documentation Statistics

**Total Files**: 16 active + 15 archived = 31 markdown files

**Current Workflow** (9 files):
- 5 core docs
- 4 agent files
- 1 command file

**Infrastructure** (3 files):
- 2 learning system files
- 1 technical reference

**Archived** (15 files):
- 6 PostgreSQL VPS docs
- 3 Custom GPT docs
- 5 obsolete commands/tracking
- 1 old enhancement agent

**Organization**:
- Root: 5 docs (clean, focused)
- .claude/: 5 files (4 agents + 1 command)
- learning/: 2 files
- ai_docs/: 1 file
- archive/: 15 files

## 🚀 Quick Reference

### Most Important Files

1. **[STREAMLINED_WORKFLOW.md](STREAMLINED_WORKFLOW.md)** - How to process videos
2. **[CLAUDE.md](CLAUDE.md)** - Complete project instructions
3. **[README.md](README.md)** - Project overview
4. **[PHASE1_COMPLETE.md](PHASE1_COMPLETE.md)** - System architecture

### Daily Use

- Process video: [.claude/commands/process-youtube.md](.claude/commands/process-youtube.md)
- Check agent behavior: [.claude/agents/](.claude/agents/)
- Review corrections: [learning/processing_knowledge_base.json](learning/processing_knowledge_base.json)

### Historical Reference

- PostgreSQL system: [archive/old_workflows/postgresql/](archive/old_workflows/postgresql/)
- Manual workflow: [archive/old_workflows/manual_chunking/](archive/old_workflows/manual_chunking/)
- All archived docs: [archive/README.md](archive/README.md)

---

**Last Updated**: January 2025 (Phase 1: Agentic Workflow)

**Note**: This index reflects the current Phase 1 agentic workflow. Historical documentation is preserved in `archive/` for reference.
