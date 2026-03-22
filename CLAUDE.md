# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the AI Knowledge Base System - a YouTube-first knowledge management tool designed to process videos and create a searchable expertise database. The project now supports **dual-pipeline processing** optimized for different content types:

- **AI Tools Pipeline**: Technical tutorials, coding workflows, development tools
- **Sports Pipeline**: Training protocols, exercise science, biomechanical analysis

Both pipelines share the same infrastructure (extraction, auto-enhancement, MCP KB storage) but use domain-specific agents and templates for optimal extraction quality. See `DUAL_PIPELINE_GUIDE.md` for complete documentation.

## Project Status

**Phase: Production-Ready with API**
- Clean, professional project structure
- Database schema deployed on VPS (PostgreSQL 16 + pgvector)
- Complete YouTube processing pipeline with manual enhancement workflow
- **Unified Memory API running on VPS** at port 8085 (https://api.vecia.fr)
- 29 videos processed with 435 high-quality chunks
- Ready for OpenAI Custom GPT integration

## CRITICAL: Manual Chunking Workflow

**Key Insight**: Manual chunking with Claude Code creates much better results than algorithmic chunking:

1. **Extract**: `uv run python main.py extract <youtube_url>`
2. **Enhance**: Fix transcription errors manually in Claude Code
3. **Chunk**: `uv run python manual_chunker.py` for high-quality chunks
4. **Results**: 17 high-quality chunks (378 tokens avg) vs 222 tiny fragments (29 tokens avg)

See `CLAUDE_CODE_WORKFLOW.md` for detailed instructions.

## Key Technologies

- **Language**: Python 3.11+
- **Package Manager**: uv (see ai_docs/tools/uv_package_manager.md)
- **Database**: PostgreSQL 16 with pgvector (768-dim embeddings)
- **Core Libraries**: yt-dlp, rapidfuzz, psycopg2/asyncpg, pydantic
- **Embedding Model**: nomic-embed-text (768-dim, via Ollama)
- **Automation**: n8n for email workflows
- **Environment**: Virtual environment managed by uv

## Project Structure

The project uses a clean workspace/archive structure for active work and historical files.

```
ai-knowledge-base/
├── src/                          # Core application code
├── workspace/                    # Active work area
│   ├── transcripts/
│   │   ├── raw/                 # Raw extracted transcripts
│   │   └── enhanced/            # Auto-enhanced transcripts
│   ├── analysis/                # Agent analysis JSON files
│   └── mcp_ready/               # Prepared MCP KB content
├── archive/                      # Historical/deprecated files
│   ├── legacy_scripts/          # Old PostgreSQL import scripts
│   ├── old_workflows/           # Old pending/processed directories
│   └── test_files/              # Test and experimental files
├── learning/                     # AI learning system
│   ├── processing_knowledge_base.json
│   └── processing_history.md
├── .claude/                      # Claude Code configuration
│   ├── agents/                  # Specialized agents
│   │   ├── youtube-transcript-analyzer.md      # AI tools agent
│   │   ├── sports-transcript-analyzer.md       # Sports agent
│   │   ├── youtube-processing-orchestrator.md
│   │   ├── indydevdan-analyzer.md
│   │   └── seankochel-analyzer.md
│   └── commands/                # Custom slash commands
│       ├── process-youtube.md          # AI tools pipeline
│       └── process-sports-video.md     # Sports pipeline
├── scripts/                      # Utility scripts
├── docs/                         # Documentation
├── main.py                       # CLI entry point
└── pyproject.toml               # uv configuration
```

## Development Commands

### Initial Setup
```bash
# IMPORTANT: Use uv for all package management (10-100x faster than pip)
# See ai_docs/tools/uv_package_manager.md for detailed documentation

# Install all dependencies (auto-creates .venv)
uv sync

# Add new dependency
uv add psycopg2-binary

# Add development dependency
uv add pytest --dev

# Run scripts in project environment
uv run python main.py
```

### Main CLI Commands
```bash
# Extract transcript for manual enhancement
uv run python main.py extract <youtube_url>

# Create manual chunks (after enhancement)
uv run python manual_chunker.py

# Import chunks to database
uv run python scripts/import_manual_chunks.py

# Search the knowledge base (local)
uv run python main.py query "search terms"

# Search via API (from anywhere - requires configuration)
# See .env.example for API_SERVER_URL and API_KEY configuration
curl -X POST ${API_SERVER_URL}/api/v1/query \
  -H "X-API-Key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"query": "search terms", "max_results": 10}'

# Check system status
uv run python main.py status

# Test entity correction
uv run python main.py test-correction
```

### Database Connection
```bash
# Configuration via Environment Variables
# Copy .env.example to .env and fill in your values

# Database connection (from .env)
# DATABASE_URL=postgresql://user:password@host:port/database
# DB_SCHEMA=ai_kb

# API Server (from .env)
# API_SERVER_URL=http://your-server:port
# API_KEY=your-api-key

# For detailed setup instructions, see:
# - .env.example for configuration template
# - archive/old_workflows/postgresql/AI_KNOWLEDGE_BASE_GUIDE.md for database setup
# - archive/old_workflows/postgresql/VPS_API_COMPLETE_SETUP.md for API server setup
```

## Architecture Overview

The system follows a clean, modular architecture:

1. **Ingestion Layer**: src/pipeline/ - YouTube video processing with transcript extraction
2. **Processing Layer**: src/processing/ - Entity correction and text enhancement
3. **Storage Layer**: src/database/ - PostgreSQL with vector embeddings
4. **Query Layer**: src/search/ - Natural language interface
5. **CLI Layer**: main.py - Simple command-line interface

## Key Implementation Priorities

1. **Clean Architecture**: Modular design with clear separation of concerns
2. **Transcription Accuracy**: Fuzzy matching to fix tool name errors
3. **Context Preservation**: Chunks maintain semantic coherence
4. **Quality Scoring**: Prioritize actionable content over theory
5. **Source Attribution**: Always include timestamps and video references

## Complete Video Processing Workflow

The system now supports both local processing and API access:

1. **Process Videos Locally** → Extract, enhance, chunk
2. **Import to VPS Database** → Generate embeddings, store chunks
3. **Query via API or CLI** → Get results with timestamps and metadata

### Quick Start for New Video

**AI Tools Videos** (Claude Code, development tools, programming):
```bash
# Use slash command for automated pipeline
/process-youtube

# Or manual steps:
# 1. Extract & enhance: uv run python main.py streamlined "URL"
# 2. Analyze: Use @youtube-transcript-analyzer
# 3. Summary: uv run python scripts/generate_detailed_summary.py VIDEO_ID
# 4. Store: uv run python scripts/store_in_mcp_kb.py analysis.json
# 5. Clean: /compact
```

**Sports Training Videos** (exercise protocols, scientific research):
```bash
# Use slash command for automated pipeline
/process-sports-video

# This handles sport-specific extraction:
# - Protocols (volume, frequency, intensity, tempo)
# - Evidence tiers (1-4 classification)
# - Biomechanics (joint angles, muscle activation)
# - WHY reasoning (biomechanical, physiological, tactical)
# - Neo4j mapping for knowledge graph integration
```

**How to Choose Pipeline**:
- **Code/tools/workflows** → `/process-youtube` (AI Tools Pipeline)
- **Exercise/training/physiology** → `/process-sports-video` (Sports Pipeline)

See `DUAL_PIPELINE_GUIDE.md` for detailed decision criteria and architecture.

## Manual Enhancement Workflow with Learning System

### Learning System Files
The project includes an AI learning system that improves with each processed video:
- **`processing_knowledge_base.json`** - Contains transcription corrections, channel patterns, and chunking guidelines
- **`processing_history.md`** - Tracks processing history and learnings from each video

### Step 1: Extract Raw Transcript
```bash
uv run python main.py extract "https://youtube.com/watch?v=VIDEO_ID"
```
This creates a file like `raw_text_for_enhancement_VIDEO_ID.txt`

### Step 2: Manual Enhancement in Claude Code
1. **Review Learning System**: Check `processing_knowledge_base.json` for:
   - Channel-specific patterns
   - Common transcription errors (29+ mapped)
   - Content type guidelines

2. **Apply Corrections**:
   - "mate and" → "n8n"
   - "clawed code" → "Claude Code"  
   - "zero" → "v0"
   - See full list in knowledge base

3. **Save Enhanced Version**: Use `_manual.txt` suffix

### Step 3: Create Manual Chunks
```bash
uv run python manual_chunker.py
```
This creates high-quality chunks following content type guidelines:
- Technical tutorials: 300-500 tokens
- Productivity content: 100-150 tokens
- Command tutorials: ~145 tokens
- Code walkthroughs: 300-600 tokens

### Step 4: Update Learning System
After processing, update:
- New transcription errors discovered
- Channel patterns identified
- Successful chunking strategies
- Quality metrics

## Common Development Tasks

When implementing features, follow this pattern:

1. **For pipeline changes**: Work in `src/pipeline/`
2. **For database operations**: Use `src/database/`
3. **For search functionality**: Modify `src/search/`
4. **For new processing**: Add to `src/processing/`

## Testing Approach

Critical test cases:
- Tool name corrections (especially "mate and" → "n8n", "make" → "Make.com")
- Chunk boundary context preservation
- Query relevance for strategic questions
- Timestamp accuracy for source verification
- Quality score differentiation

## Development Tools

```bash
# Format code
uv run black src/

# Lint code
uv run ruff check src/

# Type checking
uv run mypy src/

# Run tests
uv run pytest tests/
```

## Domain-Specific Knowledge

The system uses dual pipelines to build expertise in multiple domains:

**AI Tools & Development** (AI Tools Pipeline):
- AI automation tools (n8n, Make.com, Zapier)
- AI development tools (Cursor, v0, Claude Code)
- Agency strategies and best practices
- Client implementation patterns
- Programming workflows and code patterns

**Sports & Training** (Sports Pipeline):
- Exercise protocols and programming
- Scientific research and evidence-based training
- Biomechanical analysis and movement patterns
- Training periodization and concurrent training
- Injury prevention and rehabilitation
- Sport-specific adaptations (ultra-running, Hyrox, strength training)

## GitHub Integration

This project is now GitHub-ready with:
- Professional project structure
- Comprehensive documentation
- GitHub Actions for CI/CD
- Issue templates and contribution guidelines
- Clean .gitignore for data files

## When to Check ai_docs

Always consult the `ai_docs/` folder when:
- Using external tools (especially uv for package management)
- Implementing new patterns or algorithms
- Integrating with external APIs
- Making architectural decisions
- Unsure about project-specific conventions

The documentation in `ai_docs/` takes precedence over general knowledge.

## Recovery After Context Loss

If Cursor crashes or you lose context, use these custom commands:

1. **Check Current Status**: `/check-status`
   - Shows completed vs pending videos
   - Displays last processed video
   - Lists any work in progress

2. **Resume Specific Video**: `/resume-video <video_id_or_url>`
   - Automatically detects processing stage
   - Loads all necessary context
   - Continues from last completed step

3. **List Pending Work**: `/list-pending`
   - Shows next videos in queue
   - Provides quick start commands

Example recovery workflow:
```bash
# After crash, check status
/check-status

# Resume the last video being processed
/resume-video LvkZuY7rJOM

# Or start the next pending video
/list-pending
# Then extract the next URL shown
```

## Important Instruction Reminders

Do what has been asked; nothing more, nothing less.
NEVER create files unless they're absolutely necessary for achieving your goal.
ALWAYS prefer editing an existing file to creating a new one.
NEVER proactively create documentation files (*.md) or README files. Only create documentation files if explicitly requested by the User.

This context may or may not be relevant to your tasks. You should not respond to this context or otherwise consider it in your response unless it is highly relevant to your task. Most of the time, it is not relevant.