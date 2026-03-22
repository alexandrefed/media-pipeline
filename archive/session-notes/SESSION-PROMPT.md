# Session Prompt — AI-Knowledge-Base-PRD Fix & Modernize

Read `~/.claude/conventions/claude-md.md` and `~/Desktop/ClaudeMCP/agentic-platform/CONTRIBUTING.md` first.

## What This Project Is

Media processing pipeline: YouTube/Instagram/Vimeo/TikTok → transcription → AI analysis → unified-memory storage. Used by OpenClaw's media agent on gaming-pc. Also has n8n notification system (Telegram + spaced repetition).

## Current State: BROKEN

### Critical Issues (fix in order)

**1. Embedding model mismatch**
- Mac .env: `sentence-transformers/all-MiniLM-L6-v2` (384-dim) — OLD
- Gaming-PC .env: `nomic-embed-text` (768-dim) — CORRECT
- Fix: Update Mac .env to match gaming-pc. Standardize on nomic-embed-text (768-dim, via Ollama on gaming-pc at `gaming-pc:11434`)

**2. Storage path confusion**
- Mac .env still has direct PostgreSQL connection (`DATABASE_URL=postgresql://...`)
- Gaming-PC .env has unified-memory API (`MEMORY_BASE_URL=http://85.25.172.47:8085`)
- The project has `src/storage/unified_memory_client.py` (new) AND `src/database/connection.py` (old, hardcoded creds)
- Fix: Unified-memory API is the primary store now. PostgreSQL (aidb on VPS port 5433) is legacy. Update main.py and pipeline to use unified_memory_client.py, not direct DB.

**3. Neo4j URI**
- Was: AuraDB (`neo4j+s://d308cefa.databases.neo4j.io`)
- Now: Local VPS (`bolt://vecia_neo4j:7687`) — accessible from gaming-pc via Tailscale
- Neo4j password in Mac keychain: `security find-generic-password -s "mcp-api/neo4j-password-vps" -w` → `OHAU2hbnk1OPr70lPE3i3OBpdaskx4ok`
- Fix: Update any Neo4j connection strings in code + .env

**4. yt-dlp outdated**
- Gaming-PC: v2024.04.09 (2 years old)
- Fix: `ssh gaming-pc "pip install -U yt-dlp"`
- Instagram/TikTok extractors break frequently with old versions

**5. No whisper on gaming-pc**
- openai-whisper is NOT installed
- Needed for Instagram/TikTok pipeline (yt-dlp downloads audio → whisper transcribes)
- Fix: Install whisper or use Ollama whisper model, or use AssemblyAI API

**6. n8n webhook broken**
- Workflow "Store Video Insights" has data path corruption (`propertyValues[itemName]` not iterable)
- Blocks Weekly Digest + Spaced Repetition downstream
- Webhook: `https://n8n.vecia.fr/webhook/video-processed`

### Non-Critical

- 96 untracked files in git (new agents, scripts, docs) — need selective `git add`
- 8 modified tracked files not committed
- CLAUDE.md references old architecture (manual chunking workflow, PostgreSQL as primary)
- UNIFIED-MEMORY-INTEGRATION.md describes migration as incomplete

## What to Do

### Phase 1: Fix Credentials & Config
1. Update Mac `.env` — switch to nomic-embed-text (768-dim), add MEMORY_BASE_URL
2. Verify gaming-pc `.env` has correct unified-memory token: `ssh gaming-pc "cat ~/.config/unified-memory/token"`
3. Update any hardcoded Neo4j URIs from AuraDB → `bolt://vecia_neo4j:7687`
4. Remove hardcoded PostgreSQL creds from `src/database/connection.py`

### Phase 2: Test Pipeline on Gaming-PC
1. `ssh gaming-pc "pip install -U yt-dlp"` — update yt-dlp
2. Test YouTube pipeline: `ssh gaming-pc "cd ~/projects/AI-Knowledge-Base-PRD && uv run python main.py streamlined 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'"` (use a short video)
3. Verify output lands in `workspace/transcripts/`
4. Verify unified-memory storage: check `curl http://85.25.172.47:8085/v1/memories/search -X POST -H 'Content-Type: application/json' -d '{"query":"test video"}'`

### Phase 3: Update Documentation
1. Rewrite CLAUDE.md following `~/.claude/conventions/claude-md.md` template
2. Add Area: vecia
3. Add Shared Library block
4. Update UNIFIED-MEMORY-INTEGRATION.md to reflect current state
5. Commit all changes

### Phase 4: Register in Monorepo
1. Update `~/Desktop/ClaudeMCP/agentic-platform/AGENTS.md` — AI-Knowledge-Base-PRD section with current components
2. Evaluate: is any part of this pipeline generic enough to promote to agentic-platform? (probably not — it's project-specific)

## SSH Access
- Gaming-PC: `ssh gaming-pc` (user: alexandre)
- VPS: `ssh vecia-vps` (root) or `ssh vecia` (alexandre)
- Neo4j password: `security find-generic-password -s "mcp-api/neo4j-password-vps" -w`

## Key Files
| File | Purpose |
|------|---------|
| `main.py` | CLI entry point (streamlined, extract, query) |
| `src/storage/unified_memory_client.py` | NEW: unified-memory HTTP client |
| `src/database/connection.py` | OLD: direct PostgreSQL (has hardcoded creds) |
| `src/pipeline/youtube_processor.py` | YouTube extraction |
| `src/processing/auto_enhancer.py` | 174+ transcription corrections |
| `.claude/agents/media-ingestion-agent.md` | OpenClaw media agent spec |
| `.claude/commands/process-youtube.md` | /process-youtube slash command |
| `.env.example` | Full config template |
| `DUAL_PIPELINE_GUIDE.md` | Two-pipeline architecture |
| `notifications/N8N_INTEGRATION_SUMMARY.md` | n8n status |
