# VPS API Integration Summary

## Overview

The AI Knowledge Base system is now fully operational with:
- **Local**: Video processing pipeline and chunk management
- **VPS**: PostgreSQL database and REST API at `api.vecia.fr` (pending SSL)

## Current Architecture

```
┌─────────────────────┐     ┌──────────────────────────┐
│   Local Machine     │     │      VPS Server          │
├─────────────────────┤     ├──────────────────────────┤
│ • Video Processing  │     │ • PostgreSQL + pgvector  │
│ • Manual Enhancement│────▶│ • FastAPI (Docker)       │
│ • Chunk Creation    │     │ • Real-time Search API   │
│ • Import Scripts    │     │ • 29 videos, 435 chunks  │
└─────────────────────┘     └──────────────────────────┘
```

## Database Status

- **Videos Processed**: 29
- **Total Chunks**: 435
- **Average Quality**: 0.9 (high-quality manual chunks)
- **AI Tools Tracked**: 8 (n8n, Claude, Cursor, etc.)

## API Details

### Endpoints
- `POST /api/v1/query` - Natural language search
- `GET /api/v1/stats` - Database statistics
- `GET /health` - Health check

### Authentication
- Header: `X-API-Key`
- Key: `ai-knowledge-base-api-key-2025-secure-for-openai-custom-gpt`

### Example Query
```bash
curl -X POST http://localhost:8001/api/v1/query \
  -H "X-API-Key: ai-knowledge-base-api-key-2025-secure-for-openai-custom-gpt" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How to use Claude Code with n8n",
    "max_results": 5
  }'
```

## Local Workflow

### 1. Process New Video
```bash
# Extract transcript for enhancement
uv run python main.py extract "https://youtube.com/watch?v=VIDEO_ID"

# After manual enhancement in Claude Code
uv run python manual_chunker.py

# Import to database
uv run python scripts/import_manual_chunks.py
```

### 2. Query Database
```bash
# From local machine
uv run python main.py query "your search query"

# Via API
curl -X POST https://api.vecia.fr/api/v1/query ...
```

## Key Technical Decisions

1. **Pydantic Field Validators**: Clean type conversion for PostgreSQL types
2. **Docker Deployment**: Containerized API for easy management
3. **Manual Chunking**: Higher quality than algorithmic chunking
4. **Entity Correction**: Fixes common transcription errors

## Next Steps

1. **SSL Certificate**: Expand Let's Encrypt cert for api.vecia.fr
2. **Custom GPT Setup**: Configure OpenAI Custom GPT with API
3. **Monitoring**: Set up logging and performance tracking
4. **Backup Strategy**: Regular database backups

## Connection Details

- **Database Host**: 85.25.172.47
- **Database Port**: 5433
- **API URL**: http://localhost:8001 (will be https://api.vecia.fr)
- **Schema**: ai_kb

## Performance Metrics

- **Search Time**: ~1100ms average
- **Embedding Model**: sentence-transformers/all-MiniLM-L6-v2
- **Vector Dimensions**: 384
- **Quality Threshold**: 0.2 (configurable)