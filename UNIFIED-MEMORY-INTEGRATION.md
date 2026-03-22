# AI Knowledge Base → Unified Memory Integration

> Created: 2026-03-21
> Purpose: Complete migration guide for integrating this pipeline with the unified-memory system.
> Read this FIRST, then execute phases in order.

---

## Current State (What's Broken)

1. **Storage scripts print to stdout** — `scripts/store_in_mcp_kb.py` and `scripts/store_sports_in_mcp_kb.py` create memory objects but never call the unified-memory API
2. **Hardcoded credentials** — `src/database/connection.py` has plaintext password and public IP (`85.25.172.47:5433`). The `.env` file has them too.
3. **Dead MCP references** — Agent docs reference `mcp__mcp-kb-memory__*` and `mcp__MCP_DOCKER__*` which no longer exist
4. **Neo4j** — Any references point to defunct AuraDB. Neo4j is now self-hosted on VPS at `bolt://vecia_neo4j:7687`
5. **No phone intake** — URLs are manually pasted into Claude Code sessions
6. **Gaming-PC** — has the extraction pipeline but no `.env` for unified-memory, yt-dlp is outdated
7. **CLAUDE.md** — references old architecture (custom API on port 8001, pgvector 384-dim, algorithmic chunking)

## Target State (What We're Building)

```
Phone → Notion "Video Inbox" → n8n webhook → PGMQ queue
                                                ↓
Gaming-PC polls queue → yt-dlp → Whisper → Haiku summary
                                                ↓
HTTP POST to unified-memory API → Note stored
                                                ↓
Automatic: Notion sync + Neo4j graph extraction
                                                ↓
Result: Searchable note + graph connections + Notion visibility
```

---

## Phase 1: Credentials & Environment

### 1.1 Fix `src/database/connection.py`

The direct PostgreSQL connection to `aidb` on the VPS is **no longer the storage path**. Storage goes through the unified-memory HTTP API. However, if you still need direct DB access for legacy queries:

Replace hardcoded values with env var reads:
```python
import os

class DatabaseConfig:
    host: str = os.environ.get("DB_HOST", "85.25.172.47")
    port: int = int(os.environ.get("DB_PORT", "5433"))
    database: str = os.environ.get("DB_NAME", "aidb")
    user: str = os.environ.get("DB_USER", "ai_admin")
    password: str = os.environ.get("DB_PASSWORD", "")  # NEVER hardcode
```

### 1.2 Update `.env`

Add unified-memory API credentials:
```env
# ── Unified Memory API (primary storage path) ──────────
MEMORY_BASE_URL=http://85.25.172.47:8085
MEMORY_TOKEN=aa541b80f9ec1b0979cc6bf1af2bd177cd71e68fe1b8e5ea6557b8f762685259
MEMORY_AGENT_ID=openclaw-main

# ── Legacy Database (direct access, read-only) ─────────
DB_HOST=85.25.172.47
DB_PORT=5433
DB_NAME=aidb
DB_USER=ai_admin
DB_PASSWORD=  # Get from: ssh vecia-vps 'pass show ai-knowledge-base/db-password'

# ── Neo4j (DO NOT connect directly — graph extraction is automatic) ──
# Neo4j is at bolt://vecia_neo4j:7687 on VPS internal network
# Scripts should NOT connect to Neo4j — unified-memory API handles graph extraction

# ── Processing ─────────────────────────────────────────
EMBEDDING_MODEL=nomic-embed-text
EMBEDDING_DIM=768
# Note: unified-memory uses nomic-embed-text (768-dim) via Ollama on gaming-pc
# The old sentence-transformers/all-MiniLM-L6-v2 (384-dim) is deprecated
```

### 1.3 Gaming-PC Environment

On gaming-pc, the token already exists at `~/.config/unified-memory/token`. Create a symlink or env file:
```bash
# On gaming-pc:
mkdir -p ~/.config/ai-knowledge-base
cat > ~/.config/ai-knowledge-base/.env << 'EOF'
MEMORY_BASE_URL=http://85.25.172.47:8085
MEMORY_TOKEN=$(cat ~/.config/unified-memory/token)
MEMORY_AGENT_ID=openclaw-main
EOF
```

### 1.4 Update yt-dlp

```bash
# On gaming-pc:
uv tool install yt-dlp
# Or: pip install --upgrade yt-dlp
```

---

## Phase 2: Fix Storage Scripts

### 2.1 The Key Change

**Store as NOTES, not memories.** Notes sync to Notion Notes DB and are visible in customer/project linked views. Memories are internal agent state.

### 2.2 Unified Memory API Reference

**CRITICAL: All POST endpoints need a trailing slash or they 301 redirect and lose the body.**

```
**IMPORTANT: There is NO /v1/notes/ endpoint.** Notes are stored as memories with a `type:note` tag.
The sync service detects `type:note` memories and pushes them to the Notion Notes DB automatically.

POST http://85.25.172.47:8085/v1/memories/
  Headers:
    Authorization: Bearer <MEMORY_TOKEN>
    X-Agent-ID: openclaw-main
    Content-Type: application/json

  **To create a Notion-synced note (video content):**
    {
      "content": "# Video: {video title}\n\n## Summary\n{summary}\n\n## Key Takeaways\n{takeaways}",
      "namespace": "/alex/openclaw/videos/",
      "tags": [
        "source:openclaw-main",
        "type:note",                   // THIS makes it sync to Notion Notes DB
        "area:vecia",                  // or "area:mutora" for sports content
        "project:ai-knowledge-base"
      ],
      "metadata": {
        "video_id": "PdPPR6co7nY",
        "source": "youtube",           // or "instagram"
        "url": "https://youtube.com/watch?v=...",
        "duration": "12:34",
        "channel": "Channel Name",
        "format": "long"               // or "short"
      }
    }

  **To store detailed extraction (for agent retrieval, not Notion-visible):**
    {
      "content": "{full detailed extraction with all entities, commands, tools}",
      "namespace": "/alex/openclaw/videos/",
      "tags": ["source:openclaw-main", "type:context", "area:vecia", "project:ai-knowledge-base"],
      "metadata": {"video_id": "...", "area": "vecia"}
    }

GET  http://85.25.172.47:8085/v1/health    ← health check (no auth needed)
```

### 2.3 Rewrite Storage Flow

In `scripts/store_in_mcp_kb.py`, replace the print-to-stdout approach with HTTP calls. The script currently creates 5-7 entity-based memories per video. The new approach:

1. **One NOTE** per video (the main structured content — title, summary, key takeaways, tools, commands). This syncs to Notion and is human-readable.
2. **One MEMORY** per video (the full detailed extraction — for agent retrieval). This is searchable via `memory_search`.

```python
import httpx
import os

API_BASE = os.environ.get("MEMORY_BASE_URL", "http://85.25.172.47:8085")
API_TOKEN = os.environ.get("MEMORY_TOKEN", "")
AGENT_ID = os.environ.get("MEMORY_AGENT_ID", "openclaw-main")

def store_video_note(title: str, content: str, metadata: dict, area: str = "vecia") -> dict:
    """Store video as a note in unified-memory (syncs to Notion Notes DB).

    Notes = memories with type:note tag. No separate /v1/notes/ endpoint exists.
    """
    resp = httpx.post(
        f"{API_BASE}/v1/memories/",
        headers={
            "Authorization": f"Bearer {API_TOKEN}",
            "X-Agent-ID": AGENT_ID,
            "Content-Type": "application/json",
        },
        json={
            "content": f"# Video: {title}\n\n{content[:2000]}",
            "namespace": "/alex/openclaw/videos/",
            "tags": [
                "source:openclaw-main",
                "type:note",
                f"area:{area}",
                "project:ai-knowledge-base",
            ],
            "metadata": metadata,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()

def store_video_memory(content: str, tags: list, metadata: dict) -> dict:
    """Store detailed video extraction as a memory (for agent retrieval)."""
    resp = httpx.post(
        f"{API_BASE}/v1/memories/",
        headers={
            "Authorization": f"Bearer {API_TOKEN}",
            "X-Agent-ID": AGENT_ID,
            "Content-Type": "application/json",
        },
        json={
            "content": content[:5000],
            "namespace": "/alex/openclaw/videos/",
            "tags": tags,
            "metadata": metadata,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()
```

### 2.4 Two Processing Paths

**Long videos (>3min — YouTube tutorials, interviews, deep dives):**
```
yt-dlp → audio extract → Whisper (small model, RTX 3070) → full transcript
→ Haiku summarize → structured note:
  ## Summary
  {2-3 sentences}
  ## Key Takeaways
  1. ...
  2. ...
  ## Tools & Technologies
  - Tool 1: context
  ## Key Points
  - Point 1
  - Point 2
  ## Full Transcript
  {truncated to 2000 chars for note, full in memory}
```

**Short videos (<3min — Instagram Reels, YouTube Shorts, TikTok):**
```
yt-dlp → audio extract → Whisper → short transcript (50-200 words)
→ No summarization needed — transcript IS the content
→ Store as note with format: "short"
→ The transcript is short enough to be the full note content
```

### 2.5 Area Classification

- **vecia**: AI tools, automation, MCP, Claude, development, business
- **mutora**: Sports science, training, biomechanics, nutrition, recovery, Hyrox, CrossFit

The area determines where the note shows up in Notion (Vecia or Mutora area) and how Neo4j entities are tagged. The `_RESERVED_LABELS` denylist in Neo4j prevents Mutora data from mixing with Vecia data in the graph.

---

## Phase 3: CLAUDE.md Rewrite

Replace the current CLAUDE.md with updated architecture. Key changes:

- **Storage**: unified-memory HTTP API (not direct PostgreSQL, not MCP tools)
- **Embeddings**: nomic-embed-text 768-dim via Ollama on gaming-pc (not sentence-transformers 384-dim)
- **Neo4j**: bolt://vecia_neo4j:7687 on VPS (not AuraDB). Scripts don't connect directly — graph extraction is automatic when you store via the API.
- **Agent ID**: `openclaw-main` (registered in unified-memory agent registry)
- **Notion sync**: Automatic via heartbeat every 30 minutes. Notes stored via API appear in Notion Notes DB.
- **Dual pipeline**: AI Tools (area=vecia) + Sports (area=mutora) — same storage, different tags

Include in the new CLAUDE.md:
- The API reference from Phase 2.2
- The processing flow diagram from the Target State section above
- How to test: `curl -sf http://85.25.172.47:8085/v1/health` to check API
- The gaming-pc setup (yt-dlp, Whisper via `uv run --with openai-whisper`, CLIProxy at localhost:8317)

## Phase 4: AGENTS.md Registration

Create `AGENTS.md` to register this pipeline in the unified-memory ecosystem:

```markdown
# Agents

## video-processor
- **Role**: Extract, transcribe, summarize video content from YouTube and Instagram
- **Agent ID**: openclaw-main (shared with OpenClaw — same machine, same token)
- **Runs on**: gaming-pc (100.112.33.86 via Tailscale)
- **Inputs**: Video URLs from Notion Video Inbox or direct CLI
- **Outputs**: Notes in unified-memory (auto-sync to Notion + Neo4j graph)
- **Processing**: yt-dlp → Whisper (local GPU) → Haiku (via CLIProxy) → unified-memory API
- **Pipelines**: AI Tools (area=vecia), Sports (area=mutora)
- **Storage**: HTTP POST to unified-memory API (not MCP tools, not direct DB)
```

## Phase 5: MCP Reference Cleanup

Search all files for these dead references and remove/replace:

| Dead Reference | Replace With |
|----------------|-------------|
| `mcp__mcp-kb-memory__*` | HTTP calls to `http://85.25.172.47:8085/v1/` |
| `mcp__MCP_DOCKER__*` | Remove entirely |
| `neo4j+s://` or AuraDB references | `bolt://vecia_neo4j:7687` (but scripts shouldn't connect directly) |
| `sentence-transformers/all-MiniLM-L6-v2` | `nomic-embed-text` (768-dim, via Ollama) |
| Port 8001 API references | Port 8085 (unified-memory API) |
| `mcp-api/neo4j-*-aura` keychain entries | No longer used |

Run: `grep -rn "mcp__mcp-kb-memory\|MCP_DOCKER\|aura\|8001\|all-MiniLM" --include="*.py" --include="*.md" .`

---

## Phase 6: Notion Video Inbox (Phone Intake)

### 6.1 Create the Database

Create a "Video Inbox" database in Notion under the Vecia area page. Properties:

| Property | Type | Options |
|----------|------|---------|
| Title | title | (the video title or just "New video") |
| URL | url | the video link |
| Status | select | inbox, processing, done, failed |
| Type | select | youtube-long, youtube-short, instagram-reel |
| Area | select | vecia, mutora |
| Tags | multi-select | (free-form tags for categorization) |
| Processed Note | relation | → Notes DB |
| Created time | created_time | (auto) |

### 6.2 Phone Workflow

From your iPhone:
1. Open YouTube/Instagram → Share → Notion → "Video Inbox" database
2. Or: open Notion app → Video Inbox → "+" → paste URL, select Area
3. Status defaults to "inbox"

### 6.3 n8n Automation

Create an n8n workflow on the VPS:
- **Trigger**: Notion database polling (every 5min) on Video Inbox, filter `Status = inbox`
- **Step 1**: Extract URL and metadata from the Notion page
- **Step 2**: POST to unified-memory PGMQ queue:
  ```
  POST http://localhost:8085/v1/pgmq/send/
  Body: {
    "queue_name": "video_processing",
    "payload": {
      "url": "...",
      "area": "vecia",
      "type": "youtube-long",
      "notion_page_id": "..."
    }
  }
  ```
  Note: if the PGMQ send endpoint doesn't exist, use a simpler approach — n8n directly SSHs to gaming-pc and runs the processing script, or posts to a webhook on gaming-pc.
- **Step 3**: Update Notion page Status to "processing"

### 6.4 Gaming-PC Processing

Create a polling script or systemd timer on gaming-pc that:
1. Checks the PGMQ queue (or receives webhook from n8n)
2. Detects video type from URL:
   - `youtube.com/shorts/` or `youtu.be/` with short duration → youtube-short
   - `instagram.com/reel/` → instagram-reel
   - Everything else → youtube-long
3. Runs the appropriate pipeline (long vs short processing)
4. Stores the result via unified-memory API
5. Updates the Notion Video Inbox entry: Status = done, links the processed note

### 6.5 Alternative: Simpler Intake (No n8n)

If n8n integration is complex, a simpler approach:
- Create an Apple Shortcut that POSTs the URL directly to the unified-memory API as a task:
  ```
  POST http://85.25.172.47:8085/v1/tasks/
  Body: {
    "title": "Process video: {url}",
    "metadata": {"area": "vecia", "url": "...", "type": "youtube-long"},
    "target_agent_id": "openclaw-main"
  }
  ```
- OpenClaw picks up the task via task_queue and processes it
- Less visual than Notion inbox, but works immediately

---

## Phase 7: Verification

### Test the full flow:

1. **Storage test**: Run one of the fixed storage scripts on an existing analysis JSON:
   ```bash
   MEMORY_BASE_URL=http://85.25.172.47:8085 \
   MEMORY_TOKEN=aa541b80f9ec1b0979cc6bf1af2bd177cd71e68fe1b8e5ea6557b8f762685259 \
   MEMORY_AGENT_ID=openclaw-main \
   uv run python scripts/store_in_mcp_kb.py workspace/analysis/<some-file>.json
   ```
   Check: note appears in Notion Notes DB

2. **Graph test**: After storing, wait 1 minute, then:
   ```bash
   curl -sf -X POST http://85.25.172.47:8085/v1/graph/search/facts \
     -H "Authorization: Bearer <token>" \
     -H "X-Agent-ID: openclaw-main" \
     -H "Content-Type: application/json" \
     -d '{"query": "<video topic>", "limit": 5}'
   ```
   Check: entities from the video appear in the graph

3. **End-to-end test** (once Notion inbox is set up):
   - Add a YouTube URL to Video Inbox
   - Wait for processing
   - Check: note in Notion, graph entities in Neo4j, searchable via context_recall

4. **Test with each format**:
   - One long YouTube video (>10min tutorial)
   - One YouTube Short (<60sec)
   - One Instagram Reel

---

## Architecture Reference

```
┌─ Phone ──────────────────────────────────────┐
│  Share video → Notion "Video Inbox"          │
│  OR: Apple Shortcut → unified-memory task    │
└──────────────────────────────────────────────┘
        ↓
┌─ VPS (85.25.172.47) ─────────────────────────┐
│  n8n watches Video Inbox → queues for gaming  │
│  unified-memory API (:8085)                   │
│  Neo4j (:7687) — graph store                  │
│  Supabase PostgreSQL — pgvector store         │
│  Notion sync (every 30min via heartbeat)      │
└──────────────────────────────────────────────┘
        ↓                        ↑
┌─ Gaming-PC (100.112.33.86) ──────────────────┐
│  yt-dlp → download audio                     │
│  Whisper (RTX 3070 GPU) → transcribe         │
│  CLIProxy (:8317) → Haiku summarize          │
│  HTTP POST → unified-memory API              │
│  Ollama → nomic-embed-text embeddings        │
└──────────────────────────────────────────────┘
        ↓
┌─ Automatic (no code needed) ─────────────────┐
│  Graph extraction → Neo4j entities/relations  │
│  Notion sync → Notes DB visible in views      │
│  Consolidation → dedup similar content        │
│  Enrichment → auto-categorize and link        │
└──────────────────────────────────────────────┘
```

## Neo4j Graph — Why It Matters for Videos

When videos are stored as notes, the enrichment pipeline automatically extracts entities (people, tools, techniques, concepts) and relationships. This means:

- A 5-second Instagram reel about "wall balls" connects to a 45-minute Hyrox training deep dive through shared "Hyrox" and "wall balls" entities
- A Claude API tutorial connects to an MCP server tutorial through shared "Claude" and "API" entities
- You can query: "Who talks about periodization?" → graph returns all videos mentioning it, with their channels and contexts

No custom Neo4j code needed. Just store via the API and the pipeline does the rest.
