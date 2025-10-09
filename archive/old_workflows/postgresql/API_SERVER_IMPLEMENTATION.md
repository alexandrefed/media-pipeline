# AI Knowledge Base API Server Implementation Guide

This guide provides complete instructions for deploying a FastAPI server that exposes the AI Knowledge Base query system as a REST API compatible with OpenAI Custom GPT Actions.

## Overview

The API server provides:
- REST endpoint for natural language queries
- Complete metadata in responses (date, link, timestamp)
- OAuth2 and API key authentication options
- OpenAPI 3.1.0 specification for Custom GPT Actions
- CORS support for web access
- Rate limiting and monitoring

## Server Requirements

### System Dependencies
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip nginx certbot python3-certbot-nginx

# Install uv for package management
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Project Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-knowledge-base.git
cd ai-knowledge-base

# Install dependencies with uv
uv sync
uv add fastapi uvicorn python-jose python-multipart httpx
```

## FastAPI Server Implementation

### 1. Create `src/api/server.py`

```python
"""
FastAPI server for AI Knowledge Base Query API.
Provides Custom GPT Actions compatible endpoints.
"""

import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Security, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
from jose import JWTError, jwt

from src.search.query_system import AIKnowledgeQuery, QueryConfig, SearchMode
from src.database.connection import init_database, close_database

# Configuration
API_KEY = os.getenv("AI_KB_API_KEY", "your-secure-api-key-here")
SECRET_KEY = os.getenv("AI_KB_SECRET_KEY", "your-jwt-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Global query system instance
query_system = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    global query_system
    
    # Initialize database and query system
    await init_database()
    query_system = AIKnowledgeQuery()
    print("✅ AI Knowledge Base API initialized")
    
    yield
    
    # Cleanup
    await close_database()
    print("👋 AI Knowledge Base API shutting down")


# FastAPI app
app = FastAPI(
    title="AI Knowledge Base Query API",
    description="Natural language search API for AI tool knowledge base",
    version="1.0.0",
    servers=[
        {
            "url": "https://api.yourdomain.com",
            "description": "Production server"
        }
    ],
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chat.openai.com"],  # For Custom GPT Actions
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# Request/Response models
class QueryRequest(BaseModel):
    """Query request model."""
    query: str = Field(..., description="Natural language search query", min_length=3, max_length=500)
    max_results: Optional[int] = Field(10, description="Maximum results to return", ge=1, le=50)
    search_mode: Optional[SearchMode] = Field(SearchMode.BALANCED, description="Search precision mode")
    include_context: Optional[bool] = Field(True, description="Include surrounding context")
    quality_threshold: Optional[float] = Field(0.2, description="Minimum quality score", ge=0, le=1)


class ChunkResult(BaseModel):
    """Single search result with metadata."""
    chunk_id: int
    content: str
    similarity_score: float
    source_title: str
    source_url: str
    channel_name: str
    start_time: float
    end_time: float
    mentioned_tools: List[str]
    quality_score: float
    published_date: str = Field(..., description="ISO format date when video was published")
    source_id: int = Field(..., description="Source video ID for full metadata")
    timestamp_url: str = Field(..., description="Direct YouTube link with timestamp")
    context_before: Optional[str] = ""
    context_after: Optional[str] = ""


class QueryResponse(BaseModel):
    """Complete query response."""
    query: str
    results: List[ChunkResult]
    total_found: int
    search_time_ms: float
    detected_entities: List[str]
    search_strategy: str
    suggestions: List[str]
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "How to use n8n with databases",
                "total_found": 3,
                "search_time_ms": 245.3,
                "detected_entities": ["n8n"],
                "search_strategy": "entity_focused_hybrid",
                "suggestions": ["n8n database integration", "n8n MySQL setup"],
                "results": [
                    {
                        "chunk_id": 123,
                        "content": "n8n provides native database nodes for MySQL, PostgreSQL...",
                        "similarity_score": 0.89,
                        "source_title": "Complete n8n Database Integration Guide",
                        "source_url": "https://youtube.com/watch?v=abc123",
                        "channel_name": "AI Automation Channel",
                        "start_time": 120.5,
                        "end_time": 185.3,
                        "mentioned_tools": ["n8n", "MySQL", "PostgreSQL"],
                        "quality_score": 0.85,
                        "published_date": "2025-01-15T10:30:00Z",
                        "source_id": 42,
                        "timestamp_url": "https://youtube.com/watch?v=abc123&t=120s"
                    }
                ]
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


# Authentication functions
async def verify_api_key(api_key: str = Depends(api_key_header)) -> bool:
    """Verify API key authentication."""
    if api_key and api_key == API_KEY:
        return True
    return False


async def verify_token(token: str = Depends(oauth2_scheme)) -> Optional[Dict]:
    """Verify JWT token."""
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_auth(
    api_key_valid: bool = Depends(verify_api_key),
    token_data: Optional[Dict] = Depends(verify_token)
) -> bool:
    """Check if request is authenticated via API key or OAuth2."""
    if api_key_valid or token_data:
        return True
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


# API Endpoints
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": "AI Knowledge Base Query API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "query": "/api/v1/query",
            "health": "/health",
            "openapi": "/openapi.json"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": "connected" if query_system else "disconnected"
    }


@app.post(
    "/api/v1/query",
    response_model=QueryResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Authentication failed"},
        422: {"model": ErrorResponse, "description": "Validation error"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    tags=["Query"],
    summary="Search the AI Knowledge Base",
    description="Perform natural language search across AI tool video transcripts with complete metadata"
)
async def query_knowledge_base(
    request: QueryRequest,
    authenticated: bool = Depends(get_current_auth)
) -> QueryResponse:
    """
    Query the AI knowledge base with natural language.
    
    Returns search results with complete metadata including:
    - Video title and channel
    - Published date
    - Direct timestamp URLs for each result
    - Tools mentioned in the content
    - Quality scores
    
    Authentication required via API key or OAuth2 token.
    """
    try:
        # Execute search
        response = await query_system.search(
            query=request.query,
            max_results=request.max_results,
            search_mode=request.search_mode,
            include_context=request.include_context,
            quality_threshold=request.quality_threshold
        )
        
        # Convert to API response format
        results = []
        for result in response.results:
            results.append(ChunkResult(
                chunk_id=result.chunk_id,
                content=result.content,
                similarity_score=result.similarity_score,
                source_title=result.source_title,
                source_url=result.source_url,
                channel_name=result.channel_name,
                start_time=result.start_time,
                end_time=result.end_time,
                mentioned_tools=result.mentioned_tools,
                quality_score=result.quality_score,
                published_date=result.published_date,
                source_id=result.source_id,
                timestamp_url=result.timestamp_url,
                context_before=result.context_before,
                context_after=result.context_after
            ))
        
        return QueryResponse(
            query=response.query,
            results=results,
            total_found=response.total_found,
            search_time_ms=response.search_time_ms,
            detected_entities=response.detected_entities,
            search_strategy=response.search_strategy,
            suggestions=response.suggestions
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Query processing failed: {str(e)}"
        )


@app.post("/token", tags=["Authentication"])
async def create_access_token(api_key: str = Depends(api_key_header)):
    """Create JWT access token from API key."""
    if not api_key or api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": "api_user", "exp": expire}
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if os.getenv("DEBUG") else None,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "src.api.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True if os.getenv("DEBUG") else False
    )
```

### 2. Create `src/api/__init__.py`

```python
"""AI Knowledge Base API module."""
```

### 3. Create Systemd Service File

Save as `/etc/systemd/system/ai-kb-api.service`:

```ini
[Unit]
Description=AI Knowledge Base Query API
After=network.target

[Service]
Type=exec
User=ai_kb_user
Group=ai_kb_user
WorkingDirectory=/home/ai_kb_user/ai-knowledge-base
Environment="PATH=/home/ai_kb_user/.local/bin:/usr/local/bin:/usr/bin:/bin"
Environment="AI_KB_API_KEY=your-secure-api-key-here"
Environment="AI_KB_SECRET_KEY=your-jwt-secret-key-here"
ExecStart=/home/ai_kb_user/.local/bin/uv run uvicorn src.api.server:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 4. Nginx Configuration

Save as `/etc/nginx/sites-available/ai-kb-api`:

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;
    
    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com;
    
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    # CORS headers for Custom GPT
    add_header Access-Control-Allow-Origin "https://chat.openai.com" always;
    add_header Access-Control-Allow-Methods "GET, POST, OPTIONS" always;
    add_header Access-Control-Allow-Headers "Authorization, X-API-Key, Content-Type" always;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    limit_req zone=api burst=20 nodelay;
}
```

## Deployment Steps

### 1. Server Setup

```bash
# Create user
sudo useradd -m -s /bin/bash ai_kb_user
sudo usermod -aG sudo ai_kb_user

# Switch to user
sudo su - ai_kb_user

# Clone repository
git clone https://github.com/yourusername/ai-knowledge-base.git
cd ai-knowledge-base

# Install uv and dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
uv sync
uv add fastapi uvicorn python-jose python-multipart httpx
```

### 2. Environment Configuration

Create `.env` file:

```bash
# API Configuration
AI_KB_API_KEY=your-secure-api-key-here
AI_KB_SECRET_KEY=your-jwt-secret-key-here

# Database Configuration (from AI_KNOWLEDGE_BASE_GUIDE.md)
DB_HOST=85.25.172.47
DB_PORT=5433
DB_NAME=aidb
DB_USER=ai_admin
DB_PASSWORD=AIKnowledgeBase2025SecurePassword
DB_SCHEMA=ai_kb
```

### 3. SSL Certificate Setup

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d api.yourdomain.com
```

### 4. Start Services

```bash
# Enable and start the service
sudo systemctl enable ai-kb-api.service
sudo systemctl start ai-kb-api.service

# Enable nginx site
sudo ln -s /etc/nginx/sites-available/ai-kb-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Check status
sudo systemctl status ai-kb-api
sudo journalctl -u ai-kb-api -f
```

## API Testing

### Test with cURL

```bash
# Health check
curl https://api.yourdomain.com/health

# Query with API key
curl -X POST https://api.yourdomain.com/api/v1/query \
  -H "X-API-Key: your-secure-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How to use n8n with databases",
    "max_results": 5
  }'

# Get JWT token
curl -X POST https://api.yourdomain.com/token \
  -H "X-API-Key: your-secure-api-key-here"

# Query with JWT token
curl -X POST https://api.yourdomain.com/api/v1/query \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "n8n automation workflows",
    "max_results": 3,
    "search_mode": "precise"
  }'
```

### Test with Python

```python
import httpx
import asyncio

async def test_api():
    async with httpx.AsyncClient() as client:
        # Test query
        response = await client.post(
            "https://api.yourdomain.com/api/v1/query",
            headers={"X-API-Key": "your-secure-api-key-here"},
            json={
                "query": "How to integrate Claude with n8n",
                "max_results": 3
            }
        )
        
        data = response.json()
        print(f"Found {data['total_found']} results")
        
        for result in data['results']:
            print(f"\n📄 {result['source_title']}")
            print(f"🔗 {result['timestamp_url']}")
            print(f"📅 {result['published_date']}")
            print(f"📝 {result['content'][:100]}...")

asyncio.run(test_api())
```

## Monitoring and Maintenance

### 1. Log Monitoring

```bash
# API logs
sudo journalctl -u ai-kb-api -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### 2. Performance Monitoring

Create `monitor_api.py`:

```python
#!/usr/bin/env python3
import httpx
import asyncio
import time
from statistics import mean, median

async def monitor_performance():
    """Monitor API response times."""
    async with httpx.AsyncClient() as client:
        response_times = []
        
        for i in range(10):
            start = time.time()
            
            response = await client.post(
                "https://api.yourdomain.com/api/v1/query",
                headers={"X-API-Key": "your-secure-api-key-here"},
                json={"query": "test query", "max_results": 5}
            )
            
            elapsed = (time.time() - start) * 1000
            response_times.append(elapsed)
            
            print(f"Request {i+1}: {elapsed:.1f}ms - Status: {response.status_code}")
            await asyncio.sleep(1)
        
        print(f"\nAverage: {mean(response_times):.1f}ms")
        print(f"Median: {median(response_times):.1f}ms")
        print(f"Min: {min(response_times):.1f}ms")
        print(f"Max: {max(response_times):.1f}ms")

asyncio.run(monitor_performance())
```

### 3. Database Maintenance

```bash
# Connect to database
PGPASSWORD='AIKnowledgeBase2025SecurePassword' psql -h 85.25.172.47 -p 5433 -U ai_admin -d aidb

-- Check query performance
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements 
WHERE query LIKE '%chunks%'
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Vacuum and analyze
VACUUM ANALYZE ai_kb.chunks;
VACUUM ANALYZE ai_kb.sources;
```

## Security Best Practices

1. **API Keys**: Generate strong API keys using:
   ```python
   import secrets
   print(secrets.token_urlsafe(32))
   ```

2. **Rate Limiting**: Adjust nginx rate limits based on usage:
   ```nginx
   limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
   ```

3. **CORS**: Only allow OpenAI's domain:
   ```python
   allow_origins=["https://chat.openai.com"]
   ```

4. **Database Security**: Use read-only database user if possible:
   ```sql
   CREATE USER ai_api_user WITH PASSWORD 'secure_password';
   GRANT CONNECT ON DATABASE aidb TO ai_api_user;
   GRANT USAGE ON SCHEMA ai_kb TO ai_api_user;
   GRANT SELECT ON ALL TABLES IN SCHEMA ai_kb TO ai_api_user;
   ```

5. **Environment Variables**: Never commit secrets:
   ```bash
   # Use .env file (add to .gitignore)
   echo ".env" >> .gitignore
   ```

## Troubleshooting

### Common Issues

1. **Connection Refused**
   ```bash
   # Check if service is running
   sudo systemctl status ai-kb-api
   
   # Check if port is listening
   sudo netstat -tlnp | grep 8000
   ```

2. **Database Connection Error**
   ```bash
   # Test database connection
   PGPASSWORD='AIKnowledgeBase2025SecurePassword' psql -h 85.25.172.47 -p 5433 -U ai_admin -d aidb -c "SELECT 1"
   ```

3. **SSL Certificate Issues**
   ```bash
   # Renew certificate
   sudo certbot renew
   ```

4. **High Memory Usage**
   ```bash
   # Check memory usage
   sudo systemctl status ai-kb-api
   
   # Restart service
   sudo systemctl restart ai-kb-api
   ```

## Production Deployment Experience

The API has been successfully deployed to production with the following achievements:

### Current Status
- ✅ **API Fully Operational**: https://api.vecia.fr
- ✅ **SSL/HTTPS Configured**: Valid Let's Encrypt certificate
- ✅ **Database Connected**: 29 videos, 435 chunks with real embeddings
- ✅ **Performance**: ~1100ms average response time

### Key Technical Details
- **Deployment**: Docker Compose with multi-stage builds
- **Database**: PostgreSQL 16 with pgvector extension
- **Embeddings**: 384-dimensional vectors using sentence-transformers
- **Authentication**: API key-based for OpenAI Custom GPT

### Important Implementation Notes
During production deployment, we encountered and solved several challenges. For detailed lessons learned, including:
- PostgreSQL type handling with AsyncPG and Pydantic
- SSL certificate configuration for api.vecia.fr
- Docker optimization for ML dependencies
- Pragmatic approaches to complex type conversions

See: **[IMPLEMENTATION_LESSONS_LEARNED.md](./IMPLEMENTATION_LESSONS_LEARNED.md)**

## Future Enhancement Ideas (Optional)

1. **Monitoring**: Implement Prometheus/Grafana for metrics
2. **Caching**: Add Redis for frequently accessed queries
3. **Webhooks**: Real-time updates when new content is added
4. **Rate Limiting**: Fine-tune based on actual usage patterns
5. **Additional Endpoints**: Video listing, chunk details

This completes the server implementation. The API is now ready for OpenAI Custom GPT integration.