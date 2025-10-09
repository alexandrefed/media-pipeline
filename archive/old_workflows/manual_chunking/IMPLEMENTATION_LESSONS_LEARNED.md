# AI Knowledge Base Implementation Lessons Learned

## Overview

This document captures critical lessons learned during the production deployment of the AI Knowledge Base API on VPS. These insights are particularly valuable for future database projects involving PostgreSQL with custom types, Docker deployments, and API integrations.

## 1. PostgreSQL Type Handling Issues and Solutions

### Problem
AsyncPG was returning JSONB fields as strings (`'{}'`) instead of dictionaries, causing Pydantic validation errors. This is a common issue when working with PostgreSQL custom types and modern Python ORMs.

### Solution
Implemented Pydantic field validators with `mode='before'` to handle type conversion at the model level:

```python
# models/responses.py
from pydantic import BaseModel, Field, field_validator
from typing import Any, Dict
import json

class ChunkResult(BaseModel):
    """Search result with JSONB handling"""
    processing_metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @field_validator('processing_metadata', mode='before')
    @classmethod
    def parse_processing_metadata(cls, v: Any) -> dict:
        """Parse JSONB string to dict if needed - 2025 pragmatic approach."""
        if v is None:
            return {}
        if isinstance(v, dict):
            return v
        if isinstance(v, str):
            if not v.strip() or v.strip() == '{}':
                return {}
            try:
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return {}
        return {}
```

### Key Insight
**2025 Best Practice**: Use Pydantic field validators for type conversion instead of fighting database driver type codecs. This provides clean separation between database raw types and API response types.

## 2. Real Embeddings Generation

### Implementation Details
- Successfully integrated `sentence-transformers/all-MiniLM-L6-v2` model
- Generated 384-dimensional embeddings for all transcript chunks
- Optimized Docker build with multi-stage approach for ML dependencies

### Docker Optimization
```dockerfile
# Multi-stage build example
FROM python:3.11-slim as builder
# Install build dependencies
RUN apt-get update && apt-get install -y gcc g++ 

FROM python:3.11-slim
# Copy only necessary files from builder
# Keeps final image size manageable despite ML dependencies
```

## 3. SSL Certificate and DNS Configuration

### Process
1. **Nginx Reverse Proxy Setup**
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

2. **Let's Encrypt Certificate Expansion**
   ```bash
   certbot certonly --nginx --expand \
     -d vecia.fr \
     -d www.vecia.fr \
     -d api.vecia.fr
   ```

### Result
API now accessible at `https://api.vecia.fr` with proper HTTPS, eliminating the port specification issue for OpenAI Custom GPT integration.

## 4. Key Technical Achievements

### Database Status
- **Videos**: 29 YouTube videos indexed
- **Chunks**: 435 high-quality transcript segments
- **Tools Tracked**: 8 AI tools (n8n, Make.com, Claude, Cursor, etc.)
- **Embeddings**: 384-dimensional vectors using sentence-transformers
- **Quality Score**: 0.9 average (manually curated chunks)

### API Performance
- **Search Time**: ~1100ms average (including embedding generation)
- **Response Format**: Clean JSON with YouTube timestamps
- **Authentication**: API key-based for Custom GPT integration

## 5. Pragmatic Approaches That Worked

1. **Type Handling**: Don't fight the database driver - handle conversions in the application layer
2. **Docker Strategy**: Multi-stage builds are essential for ML dependencies
3. **API Design**: Simple, focused endpoints with clear authentication
4. **Documentation**: Create comprehensive guides during implementation, not after

## 6. Lessons for Future Projects

### Do's
- ✅ Use Pydantic field validators for type conversions
- ✅ Plan for SSL/DNS from the start (avoid port-based URLs)
- ✅ Test with actual client tools (e.g., OpenAI Custom GPT) early
- ✅ Document issues and solutions as you encounter them
- ✅ Use Docker multi-stage builds for complex dependencies

### Don'ts
- ❌ Don't try to modify database driver behavior for type handling
- ❌ Don't assume external services (like OpenAI) support all URL formats
- ❌ Don't skip the nginx reverse proxy step for production APIs
- ❌ Don't underestimate the value of manual content curation

## 7. Current Production Status

✅ **API Fully Operational**: https://api.vecia.fr
- Vector search working with real embeddings
- All 435 chunks searchable
- Returns YouTube timestamps for precise navigation

✅ **SSL/HTTPS Configured**: Valid Let's Encrypt certificate until 2025-10-25

✅ **Documentation Complete**: Ready for Custom GPT integration

✅ **Database Populated**: 29 videos, 435 chunks, real embeddings

## 8. Code Snippets for Future Reference

### AsyncPG Connection with pgvector
```python
import asyncpg
from pgvector.asyncpg import register_vector

async def get_connection():
    conn = await asyncpg.connect(DATABASE_URL)
    await register_vector(conn)
    return conn
```

### Vector Similarity Search Query
```sql
SELECT 
    chunk_id,
    content,
    1 - (embedding <=> $1::vector) as similarity_score
FROM chunks
WHERE 1 - (embedding <=> $1::vector) > $2
ORDER BY similarity_score DESC
LIMIT $3
```

### API Endpoint with Proper Error Handling
```python
@app.post("/api/v1/query")
async def query_knowledge(
    request: QueryRequest,
    api_key: str = Depends(verify_api_key)
):
    try:
        # Implementation
        return QueryResponse(...)
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
```

## Conclusion

The successful deployment of the AI Knowledge Base API demonstrates that pragmatic solutions often trump perfect implementations. By focusing on what works (Pydantic validators) rather than fighting the system (AsyncPG type codecs), we achieved a clean, maintainable solution that's now serving real queries through OpenAI Custom GPTs.

The combination of proper SSL configuration, thoughtful API design, and comprehensive documentation has resulted in a production-ready system that can serve as a template for future projects.

---

*Last Updated: 2025-01-27*
*API Version: 1.0.0*
*Database: 29 videos, 435 chunks, 8 AI tools tracked*