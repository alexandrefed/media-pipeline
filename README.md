# AI Knowledge Base 🧠

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/badge/package%20manager-uv-orange)](https://github.com/astral-sh/uv)
[![Claude Code Ready](https://img.shields.io/badge/Claude%20Code-Ready-purple)](https://claude.ai/code)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Transform YouTube videos into a searchable AI knowledge base using **dual-pipeline processing** with intelligent specialized agents and unified-memory integration.

## ✨ Dual-Pipeline Processing System

The system now supports **two specialized pipelines** optimized for different content types:

### 🔧 AI Tools Pipeline
- 🤖 **Channel-Specific Agents** - IndyDevDan, Sean Kochel analyzers
- 💻 **Code & Tools Focus** - Commands, workflows, implementation details
- ⚡ **Auto-Enhancement** - 174+ transcription corrections
- 🎯 **Intelligent Orchestration** - R&D Framework (Reduce and Delegate)

### 🏃 Sports Pipeline
- 🎯 **Protocol Extraction** - Volume, frequency, intensity, tempo
- 📚 **Evidence Classification** - 4-tier scientific evidence system
- 🧬 **Biomechanics Analysis** - Joint angles, muscle activation, force vectors
- 🧠 **WHY Reasoning** - Biomechanical, physiological, tactical rationale
- 🔗 **Neo4j Integration** - Direct knowledge graph mapping

**Shared Benefits**:
- 💾 **unified-memory** - Native Claude Code integration
- 🚀 **12.5x Faster** - 2 minutes vs 25 minutes per video
- 📊 **10-100x Better Quality** - Domain-specific extraction vs generic

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- uv package manager
- Claude Code with unified-memory

### Installation

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone and setup**:
   ```bash
   git clone https://github.com/yourusername/ai-knowledge-base.git
   cd ai-knowledge-base

   # Install all dependencies (auto-creates .venv)
   uv sync
   ```

## ⚙️ Configuration

### Initial Setup

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Configure your environment** (edit `.env`):
   ```bash
   # Required for database features:
   DATABASE_URL=postgresql://user:password@host:port/database
   DB_SCHEMA=ai_kb

   # Optional for API server:
   API_SERVER_URL=http://your-server:8085
   API_KEY=your-secure-api-key
   ```

3. **Install dependencies**:
   ```bash
   uv sync
   ```

**⚠️ Important**: Never commit your `.env` file! It contains sensitive credentials and is automatically ignored by git.

## 📖 Usage

### Complete Workflow (One Command)

**AI Tools Videos** (Claude Code, development tools, programming):
```bash
# Process AI tool tutorial
/process-youtube
```

**Sports Training Videos** (exercise protocols, scientific research):
```bash
# Process sports training video
/process-sports-video
```

**How to Choose**:
- **Code/tools/workflows** → `/process-youtube` (AI Tools Pipeline)
- **Exercise/training/physiology** → `/process-sports-video` (Sports Pipeline)

Both commands execute the Scout-Plan-Summarize-Build pattern:
1. **Scout**: Extract → Auto-enhance (174+ corrections)
2. **Plan**: Analyze with domain-specific agent
3. **Summarize**: Generate detailed markdown summary
4. **Build**: Store in unified-memory → Instant queries

See `DUAL_PIPELINE_GUIDE.md` for detailed pipeline comparison.

### Step-by-Step Workflow

#### 1. Extract & Auto-Enhance
```bash
uv run python main.py extract "https://youtube.com/watch?v=VIDEO_ID"
uv run python -m src.processing.auto_enhancer raw_text_*.txt
```

#### 2. Intelligent Analysis with Orchestrator
```
Use @youtube-processing-orchestrator to analyze the enhanced transcript
```

The orchestrator will:
- Detect channel (IndyDevDan, Sean Kochel, or generic)
- Delegate to specialized analyst
- Generate high-quality structured JSON

#### 3. Store in unified-memory
```bash
uv run python scripts/store_in_mcp_kb.py [analysis_file].json
```

Then store using Claude Code:
```
Use mcp__unified-memory__memory_store with the prepared content
```

#### 4. Query Anytime
```
Use mcp__unified-memory__memory_search with query: "Claude Code sub-agents"
```

## 🏗️ Project Structure

```
ai-knowledge-base/
├── src/                          # Core application code
│   ├── pipeline/                 # YouTube processing
│   ├── processing/               # Auto-enhancement & entity correction
│   ├── database/                 # Database operations (legacy)
│   └── search/                   # Query system (legacy)
├── workspace/                    # Active work area (NEW in Phase 1)
│   ├── transcripts/
│   │   ├── raw/                 # Raw extracted transcripts
│   │   └── enhanced/            # Auto-enhanced transcripts
│   ├── analysis/                # Agent analysis JSON files
│   └── mcp_ready/               # Prepared MCP KB content
├── .claude/                      # Claude Code configuration (NEW)
│   ├── agents/                  # Specialized agents
│   │   ├── youtube-transcript-analyzer.md      # AI tools agent
│   │   ├── sports-transcript-analyzer.md       # Sports agent
│   │   ├── youtube-processing-orchestrator.md
│   │   ├── indydevdan-analyzer.md
│   │   └── seankochel-analyzer.md
│   └── commands/                # Custom slash commands
│       ├── process-youtube.md          # AI tools pipeline
│       └── process-sports-video.md     # Sports pipeline
├── archive/                      # Historical files (NEW)
│   ├── old_workflows/           # PostgreSQL VPS phase
│   └── unused/                  # Explored but not adopted
├── learning/                     # AI learning system
│   ├── processing_knowledge_base.json  # 174+ corrections
│   └── processing_history.md           # Processing logs
├── scripts/                      # Utility scripts
├── docs/                         # Documentation
├── main.py                       # CLI entry point
└── pyproject.toml               # uv configuration
```

## 🔄 How It Works

### Agentic Workflow (Phase 1)

```
YouTube URL
    ↓
[Extract] → raw_text_for_enhancement_VIDEO_ID.txt
    ↓
[Auto-Enhance] → _auto_enhanced.txt (174+ corrections)
    ↓
[@youtube-processing-orchestrator]
    ↓
[Detects Channel] → IndyDevDan / Sean Kochel / Generic
    ↓
[Delegates to Specialist] → @indydevdan-analyzer / @seankochel-analyzer
    ↓
[Analysis] → _analysis.json (structured knowledge)
    ↓
[MCP KB Storage] → Stored in Claude Code memory
    ↓
[Query] → Instant retrieval via MCP
```

### Why Agentic Approach?

**Traditional** (What we had):
```
User → Single Agent → Regex Extraction → Poor Quality
```

**Agentic** (What we built):
```
User → Orchestrator → Detects Channel → Specialist → High Quality
       (R&D Framework)  (Smart Routing)  (Domain Expertise)
```

## ✨ Specialized Agents

### AI Tools Pipeline Agents

**1. YouTube Transcript Analyzer (General-Purpose AI Tools)**
- Filters fragments, extracts real tools
- Identifies executable commands
- Captures complete workflows
- Synthesizes actionable takeaways
- Extracts implementation details (setup, configuration, troubleshooting)

**2. IndyDevDan Analyzer (Advanced Claude Code)**
- Extracts agentic coding patterns
- Captures philosophical frameworks
- Identifies prompt engineering techniques
- Recognizes context management strategies
- Documents exact commands, file paths, and performance metrics

**3. Sean Kochel Analyzer (Productivity)**
- Extracts step-by-step methodologies
- Captures time-saving metrics
- Identifies professional workflow principles
- Recognizes tool integration patterns
- Documents procedures with exact configuration values

**4. YouTube Processing Orchestrator**
- Implements R&D Framework
- Detects channel automatically
- Routes to appropriate specialist
- Coordinates workflow execution

### Sports Pipeline Agent

**5. Sports Transcript Analyzer**
- Extracts exercise protocols (volume, frequency, intensity, tempo)
- Classifies scientific evidence (4-tier system)
- Quantifies biomechanics (joint angles, muscle activation, force vectors)
- Identifies WHY reasoning (biomechanical, physiological, tactical)
- Documents injury considerations and modifications
- Maps to Neo4j knowledge graph schema

See `DUAL_PIPELINE_GUIDE.md` for complete agent comparison.

## 🛠️ Tech Stack

- **Language**: Python 3.11+
- **Package Manager**: uv (10-100x faster than pip)
- **Core Libraries**: yt-dlp, rapidfuzz, pydantic
- **Embedding Model**: nomic-embed-text (768-dim, via Ollama)
- **Storage**: unified-memory (Claude Code integration)
- **Enhancement**: Auto-enhancer with 174+ corrections

## 📊 Quality Comparison

### Before (General Agent + Regex)
- Tools: "for agentic", "the new" (fragments)
- Commands: "more compute" (not executable)
- Analysis: Generic, surface-level

### After (Orchestrator + Specialists)
- Tools: "Claude Code 2.0", "UV package manager" (real tools)
- Commands: "/scout-plan-build", "uv run" (executable)
- Analysis: Deep, context-aware, domain-optimized

**Improvement**: **10-100x better quality** depending on content type

## 🧪 Development

### Adding Dependencies
```bash
uv add requests              # Runtime dependency
uv add pytest --dev          # Development dependency
uv sync                      # Sync all dependencies
```

### Code Quality
```bash
uv run black src/            # Format code
uv run ruff check src/       # Lint code
uv run mypy src/             # Type checking
uv run pytest tests/         # Run tests
```

## 📚 Documentation

**Current Workflow:**
- [DUAL_PIPELINE_GUIDE.md](DUAL_PIPELINE_GUIDE.md) - **NEW** - Complete dual-pipeline architecture
- [STREAMLINED_WORKFLOW.md](STREAMLINED_WORKFLOW.md) - Updated for dual pipelines
- [CLAUDE.md](CLAUDE.md) - Project overview and instructions
- [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) - Complete docs map

**Agent Documentation:**
- `.claude/agents/youtube-transcript-analyzer.md` - AI tools agent
- `.claude/agents/sports-transcript-analyzer.md` - Sports agent
- `.claude/agents/youtube-processing-orchestrator.md` - Orchestrator
- `.claude/agents/indydevdan-analyzer.md` - IndyDevDan specialist
- `.claude/agents/seankochel-analyzer.md` - Sean Kochel specialist

**Historical Reference:**
- [archive/README.md](archive/README.md) - Archived workflows and docs
- PostgreSQL VPS phase (July 2025) - 29 videos, 435 chunks
- Manual chunking workflow documentation

## 🎯 Benefits

### 1. Intelligence
- Automatic channel detection
- Specialized domain analysis
- Context-aware extraction

### 2. Quality
- Channel-specific terminology
- Deeper concept extraction
- Better context preservation

### 3. Speed
- **Old**: 25 minutes manual per video
- **New**: 2 minutes automated per video
- **Phase 2**: Batch overnight (0 active time)

### 4. Scalability
- Easy to add new specialists
- Each agent is independent
- Learning system improves all agents

## 🔄 Migration from PostgreSQL Phase

If you have existing videos in the old PostgreSQL VPS system:

**Option 1**: Re-process with new workflow
```bash
uv run python main.py extract "YOUTUBE_URL"
/process-youtube https://youtube.com/watch?v=VIDEO_ID
```

**Option 2**: Keep existing PostgreSQL data
- VPS database still functional (29 videos, 435 chunks)
- Can query via API as before
- New videos use unified-memory

See `archive/old_workflows/postgresql/` for complete VPS documentation.

## 📋 Roadmap

### Phase 1: Agentic Processing ✅
- Custom slash commands
- Orchestrator agent
- Specialized channel analysts
- unified-memory integration

### Phase 2: Batch & Parallel (Future)
- Monitor folder for new videos
- Auto-process overnight
- Parallel processing (10 videos simultaneously)
- Self-improving system

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes
6. Push and open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for [Claude Code](https://claude.ai/code)
- Uses [uv](https://github.com/astral-sh/uv) for fast package management
- Inspired by IndyDevDan's agentic coding patterns
- Designed for AI automation tool knowledge extraction

---

**Last Updated**: January 2025 (Phase 1: Agentic Workflow)
