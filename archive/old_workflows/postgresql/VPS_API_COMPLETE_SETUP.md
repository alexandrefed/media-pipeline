# VPS API Complete Setup Documentation

## Overview

The AI Knowledge Base API is deployed on VPS using Docker Compose, providing a REST API for querying the knowledge base with vector similarity search.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        VPS Server                             │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐        ┌─────────────────────────┐    │
│  │   PostgreSQL    │        │    FastAPI Server      │    │
│  │   + pgvector    │◄──────►│   (Docker Container)   │    │
│  │   Port: 5433    │        │     Port: 8001         │    │
│  └─────────────────┘        └─────────────────────────┘    │
│         ▲                              ▲                     │
│         │                              │                     │
│         └──────────────────────────────┘                     │
│              29 videos, 435 chunks                           │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Details

### Location
- **Main Directory**: `/root/vecia/services/ai-api/`
- **Database**: PostgreSQL 16 with pgvector extension
- **API Server**: FastAPI with Docker

### Directory Structure
```
/root/vecia/services/ai-api/
├── main.py                 # FastAPI application
├── Dockerfile             # Multi-stage build
├── requirements.txt       # Dependencies
├── docker-compose.yml     # Service orchestration
├── .env.docker           # Environment variables
├── auth/
│   └── security.py       # API key authentication
├── database/
│   ├── connection.py     # Asyncpg + pgvector
│   └── queries.py        # Vector search queries
├── models/
│   ├── requests.py       # Request models
│   └── responses.py      # Response models with Pydantic validators
├── utils/
│   ├── config.py         # Settings
│   └── embeddings.py     # Sentence-transformers
└── init-aidb/
    └── 01-init-schema.sql # Database schema
```

## Key Implementation Details

### 1. Pydantic Field Validators (2025 Approach)
The VPS implementation uses Pydantic field validators to handle PostgreSQL types:

```python
# models/responses.py
class ChunkResult(BaseModel):
    """Search result with JSONB handling"""
    processing_metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @field_validator('processing_metadata', mode='before')
    def parse_jsonb(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except:
                return {}
        return v or {}
```

### 2. Docker Compose Configuration
```yaml
services:
  vecia_aidb:
    image: pgvector/pgvector:pg16
    container_name: vecia_aidb
    ports:
      - "5433:5433"
    volumes:
      - ai_postgres_data:/var/lib/postgresql/data
    command: -p 5433
    
  vecia_ai_api:
    build: .
    container_name: vecia_ai_api
    ports:
      - "8001:8000"
    depends_on:
      vecia_aidb:
        condition: service_healthy
```

### 3. Environment Configuration
```env
# Database
DATABASE_URL=postgresql://ai_admin:${AIDB_ADMIN_PASSWORD}@vecia_aidb:5433/ai_knowledge_base
DATABASE_SCHEMA=ai_kb

# API
API_KEY=ai-knowledge-base-api-key-2025-secure-for-openai-custom-gpt
JWT_SECRET=your-secure-jwt-secret-key-2025

# Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIMENSION=384
```

## API Endpoints

### 1. Health Check
```bash
GET /health
```
No authentication required.

### 2. Query Endpoint (Main)
```bash
POST /api/v1/query
Headers: X-API-Key: <api-key>
Body: {
    "query": "string",
    "max_results": 10,
    "search_mode": "balanced"
}
```

### 3. Statistics
```bash
GET /api/v1/stats
Headers: X-API-Key: <api-key>
```

### 4. Token Exchange
```bash
POST /token
Headers: X-API-Key: <api-key>
```

## Current Status

- ✅ **Database**: 29 videos, 435 chunks
- ✅ **API**: Running on port 8001
- ✅ **Search**: ~1100ms average response time
- ✅ **Quality**: 0.9 average chunk quality
- ⏳ **SSL**: Pending api.vecia.fr setup

## Management Commands

### Check Status
```bash
cd /root/vecia/services/ai-api
docker compose ps
```

### View Logs
```bash
docker compose logs -f vecia_ai_api
```

### Restart API
```bash
docker compose restart vecia_ai_api
```

### Rebuild After Changes
```bash
docker compose build vecia_ai_api && docker compose up -d vecia_ai_api
```

### Test Query
```bash
curl -X POST http://localhost:8001/api/v1/query \
  -H "X-API-Key: ai-knowledge-base-api-key-2025-secure-for-openai-custom-gpt" \
  -H "Content-Type: application/json" \
  -d '{"query": "n8n automation", "max_results": 5}'
```

## Production Setup (Pending)

### 1. SSL Certificate
```bash
# Expand certificate for api.vecia.fr
certbot certonly --nginx --expand \
  -d vecia.fr \
  -d www.vecia.fr \
  -d api.vecia.fr
```

### 2. Nginx Configuration
Create `/etc/nginx/sites-available/api.vecia.fr`:
```nginx
server {
    listen 443 ssl http2;
    server_name api.vecia.fr;
    
    ssl_certificate /etc/letsencrypt/live/vecia.fr/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/vecia.fr/privkey.pem;
    
    location / {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. Enable Site
```bash
ln -s /etc/nginx/sites-available/api.vecia.fr /etc/nginx/sites-enabled/
nginx -t
systemctl reload nginx
```

## Performance Metrics

- **Search Time**: ~1100ms (including embedding generation)
- **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Vector Index**: pgvector with cosine similarity
- **Concurrent Requests**: Handled by uvicorn workers

## Security

- **API Key**: Required for all endpoints except /health
- **CORS**: Configured for OpenAI domains
- **Rate Limiting**: Via nginx (when configured)
- **Database**: Isolated in Docker network

## Troubleshooting

### API Not Responding
```bash
# Check container status
docker compose ps

# Check logs
docker compose logs vecia_ai_api --tail=50

# Restart if needed
docker compose restart vecia_ai_api
```

### Database Connection Issues
```bash
# Test database connection
docker compose exec vecia_aidb psql -U ai_admin -d ai_knowledge_base -c "SELECT 1"

# Check database logs
docker compose logs vecia_aidb --tail=50
```

### High Memory Usage
```bash
# Check resource usage
docker stats

# Restart services
docker compose restart
```

## Integration with Local Development

From your local machine, you can:
1. Process videos locally
2. Import chunks to VPS database (port 5433)
3. Query via API (port 8001)
4. Or query directly via `main.py query`

The system maintains consistency between local processing and VPS serving.