# System: API Architecture

## Overview

The AI Knowledge Base exposes a REST API for querying processed YouTube content with natural language. Designed for OpenAI Custom GPT Actions integration.

**API Base URL**: https://api.vecia.fr (production)
**Local Development**: http://localhost:8085

## Technology Stack

- **Framework**: FastAPI (async)
- **Server**: Uvicorn (ASGI)
- **Authentication**: API Key + OAuth2 JWT
- **Database**: PostgreSQL 16 with pgvector
- **Embedding Model**: nomic-embed-text (768-dim, via Ollama)
- **Deployment**: Docker Compose
- **Reverse Proxy**: Nginx with Let's Encrypt SSL

## Architecture Components

```
Client Request
    ↓
[Nginx] (SSL termination, rate limiting, CORS)
    ↓
[FastAPI Application] (authentication, routing)
    ↓
[Query System] (search logic, entity detection)
    ↓
[PostgreSQL + pgvector] (vector similarity search)
    ↓
[Response] (JSON with metadata and timestamps)
```

## API Endpoints

### 1. Health Check
```
GET /health
```

**Purpose**: Verify API server and database connectivity

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-01-09T10:30:00Z",
  "database": "connected"
}
```

**Use case**: Monitoring, uptime checks

### 2. Root Information
```
GET /
```

**Purpose**: API information and available endpoints

**Response**:
```json
{
  "name": "AI Knowledge Base Query API",
  "version": "1.0.0",
  "status": "operational",
  "endpoints": {
    "query": "/api/v1/query",
    "health": "/health",
    "openapi": "/openapi.json"
  }
}
```

### 3. Query Knowledge Base (Main Endpoint)
```
POST /api/v1/query
```

**Purpose**: Natural language search across YouTube video knowledge

**Authentication**: Required (API Key or JWT)

**Request Body**:
```json
{
  "query": "How to use Claude Code context window management",
  "max_results": 10,
  "search_mode": "balanced",
  "include_context": true,
  "quality_threshold": 0.2
}
```

**Parameters**:
- `query` (required): Natural language search query (3-500 chars)
- `max_results` (optional): Maximum results (1-50, default: 10)
- `search_mode` (optional): "precise" | "balanced" | "broad" (default: balanced)
- `include_context` (optional): Include surrounding context (default: true)
- `quality_threshold` (optional): Minimum quality score 0-1 (default: 0.2)

**Response**:
```json
{
  "query": "How to use Claude Code context window management",
  "total_found": 5,
  "search_time_ms": 245.3,
  "detected_entities": ["Claude Code"],
  "search_strategy": "entity_focused_hybrid",
  "suggestions": ["Claude Code context optimization", "autocompact buffer"],
  "results": [
    {
      "chunk_id": 123,
      "content": "To optimize Claude Code's context window...",
      "similarity_score": 0.89,
      "source_title": ".agent folder is making claude code 10x better",
      "source_url": "https://youtube.com/watch?v=MW3t6jP9AOs",
      "channel_name": "AI Jason",
      "start_time": 120.5,
      "end_time": 185.3,
      "mentioned_tools": ["Claude Code", "Codex"],
      "quality_score": 0.85,
      "published_date": "2025-01-09T10:30:00Z",
      "source_id": 42,
      "timestamp_url": "https://youtube.com/watch?v=MW3t6jP9AOs&t=120s",
      "context_before": "Previous context...",
      "context_after": "Following context..."
    }
  ]
}
```

**Result Fields**:
- `chunk_id`: Unique chunk identifier
- `content`: Cleaned, enhanced content text
- `similarity_score`: Relevance score (0-1)
- `source_title`: Video title
- `source_url`: YouTube video URL
- `channel_name`: Creator/channel name
- `start_time/end_time`: Timestamp in video (seconds)
- `mentioned_tools`: Tools referenced in content
- `quality_score`: Information density (0-1)
- `published_date`: ISO 8601 date
- `source_id`: Database source ID
- `timestamp_url`: Direct YouTube link with timestamp
- `context_before/after`: Surrounding context (if requested)

### 4. Generate Access Token
```
POST /token
```

**Purpose**: Exchange API key for JWT token

**Headers**:
```
X-API-Key: your-api-key-here
```

**Response**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

**Use case**: OAuth2 authentication for Custom GPT

## Authentication

### API Key (Recommended for Custom GPT)

**Header**:
```
X-API-Key: your-secure-api-key-here
```

**Usage**:
```bash
curl -X POST https://api.vecia.fr/api/v1/query \
  -H "X-API-Key: your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{"query": "search terms", "max_results": 5}'
```

### JWT Bearer Token

**Header**:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Usage**:
```bash
# Get token
TOKEN=$(curl -X POST https://api.vecia.fr/token \
  -H "X-API-Key: your-api-key-here" | jq -r '.access_token')

# Use token
curl -X POST https://api.vecia.fr/api/v1/query \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "search terms"}'
```

## Search Modes

### Precise
- Exact entity matching
- Higher similarity threshold (0.75+)
- Fewer but highly relevant results
- **Use case**: Finding specific tool documentation

### Balanced (Default)
- Hybrid search (entity + semantic)
- Moderate threshold (0.5+)
- Good mix of precision and recall
- **Use case**: General queries, exploration

### Broad
- Semantic similarity focus
- Lower threshold (0.3+)
- More results, wider context
- **Use case**: Discovering related content

## Query System Logic

### 1. Entity Detection
```python
# Detects known tools from query
"How to use n8n with Claude" → entities: ["n8n", "Claude"]
```

### 2. Search Strategy Selection
- **Entity-focused**: If known tools detected
- **Semantic**: If no specific entities
- **Hybrid**: Combination of both

### 3. Vector Similarity Search
- Generates query embedding (768-dim)
- Compares with stored chunk embeddings
- Uses cosine similarity via pgvector
- Filters by quality threshold

### 4. Post-Processing
- Ranks by similarity score
- Applies quality score weighting
- Generates timestamp URLs
- Adds context windows
- Suggests related queries

## Performance Characteristics

**Current Production Metrics:**
- Average response time: ~1100ms
- Database: 29 videos, 435 chunks
- Vector search: HNSW index for speed
- Quality filtering: Pre-filters before ranking

**Optimization Tips:**
- Use quality_threshold > 0.5 for faster queries
- Reduce max_results for quicker responses
- Set include_context: false if not needed
- Use precise mode for specific tool queries

## Security Features

### Rate Limiting
```nginx
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
limit_req zone=api burst=20 nodelay;
```

### CORS
- Restricted to: https://chat.openai.com
- Methods: GET, POST
- Headers: Authorization, X-API-Key, Content-Type

### SSL/TLS
- Let's Encrypt SSL certificate
- HSTS header enabled
- Forced HTTPS redirect

### API Key Security
- Environment variables (never committed)
- 32+ character random tokens
- Separate development/production keys

## Error Handling

### 401 Unauthorized
```json
{
  "error": "Invalid authentication credentials",
  "timestamp": "2025-01-09T10:30:00Z"
}
```

**Cause**: Missing or invalid API key/token

### 422 Validation Error
```json
{
  "error": "Validation failed",
  "detail": "query must be at least 3 characters",
  "timestamp": "2025-01-09T10:30:00Z"
}
```

**Cause**: Invalid request parameters

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "detail": "Query processing failed: connection timeout",
  "timestamp": "2025-01-09T10:30:00Z"
}
```

**Cause**: Database issues, processing errors

## Deployment Architecture

### Production (VPS)
```yaml
services:
  nginx:
    - SSL termination
    - Reverse proxy to FastAPI
    - Rate limiting
    - CORS headers

  api:
    - FastAPI application
    - Port 8085 (internal)
    - Environment variables from .env

  database:
    - PostgreSQL 16 + pgvector
    - Port 5433
    - ai_kb schema
```

### Environment Variables
```bash
# API Configuration
AI_KB_API_KEY=your-secure-api-key-here
AI_KB_SECRET_KEY=your-jwt-secret-key-here

# Database Configuration
DATABASE_URL=postgresql://user:pass@host:port/database
DB_SCHEMA=ai_kb
```

## Integration Examples

### OpenAI Custom GPT Actions

**Schema URL**: https://api.vecia.fr/openapi.json

**Authentication**:
- Type: API Key
- Header: X-API-Key
- Key: [your-api-key]

**Action Configuration**:
```yaml
servers:
  - url: https://api.vecia.fr

paths:
  /api/v1/query:
    post:
      summary: Search AI knowledge base
      operationId: queryKnowledgeBase
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                query:
                  type: string
                max_results:
                  type: integer
                  default: 5
```

### Python Client
```python
import httpx
import asyncio

async def query_knowledge_base(query: str, max_results: int = 10):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.vecia.fr/api/v1/query",
            headers={"X-API-Key": "your-api-key-here"},
            json={"query": query, "max_results": max_results}
        )
        return response.json()

# Usage
results = asyncio.run(query_knowledge_base("Claude Code workflows"))
for result in results['results']:
    print(f"{result['source_title']} - {result['timestamp_url']}")
```

### cURL
```bash
curl -X POST https://api.vecia.fr/api/v1/query \
  -H "X-API-Key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "n8n automation workflows",
    "max_results": 5,
    "search_mode": "balanced"
  }' | jq '.results[] | {title: .source_title, url: .timestamp_url}'
```

## Monitoring and Maintenance

### Health Checks
```bash
# Simple health check
curl https://api.vecia.fr/health

# Monitor response time
time curl https://api.vecia.fr/health
```

### Logs
```bash
# API server logs
sudo journalctl -u ai-kb-api -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log
```

### Performance Monitoring
```bash
# Database query performance
psql -h host -p port -U user -d aidb
SELECT query, mean_exec_time FROM pg_stat_statements
WHERE query LIKE '%chunks%' ORDER BY mean_exec_time DESC LIMIT 10;
```

## Common Issues and Solutions

### Slow Query Response
- **Check**: Vector index integrity
- **Fix**: REINDEX INDEX idx_chunks_embedding
- **Optimize**: Increase quality_threshold

### Connection Timeout
- **Check**: Database connectivity
- **Fix**: Restart PostgreSQL service
- **Monitor**: Connection pool settings

### High Memory Usage
- **Check**: Embedding model loaded multiple times
- **Fix**: Restart API service
- **Optimize**: Use lighter embedding model

## Future Enhancements

Potential improvements:
1. **Caching**: Redis for frequently queried content
2. **Webhooks**: Real-time notifications on new content
3. **Batch Queries**: Process multiple queries in parallel
4. **Advanced Filtering**: Filter by channel, date range, tools
5. **Analytics**: Track popular queries and response times

## Related Documents

- [Database Schema](./database-schema.md)
- [MCP KB Memory Management SOP](../SOPs/mcp-kb-memory-management.md)
- Implementation details: `archive/old_workflows/postgresql/API_SERVER_IMPLEMENTATION.md`

## Version History

- v1.0 (Jan 2025): Initial API architecture documentation
- Production deployment: api.vecia.fr operational since Dec 2024
