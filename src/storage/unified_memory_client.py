"""
Unified Memory API client for storing video notes and memories.

Calls the unified-memory HTTP API directly instead of requiring MCP tool context.
See UNIFIED-MEMORY-INTEGRATION.md for API reference.
"""

import logging
import os
import time
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Config from environment, with token file fallback
API_BASE = os.environ.get("MEMORY_BASE_URL", "http://85.25.172.47:8085")
AGENT_ID = os.environ.get("MEMORY_AGENT_ID", "openclaw-main")

# Token: env var first, then ~/.config/unified-memory/token file
API_TOKEN = os.environ.get("MEMORY_TOKEN", "")
if not API_TOKEN:
    _token_path = Path.home() / ".config" / "unified-memory" / "token"
    if _token_path.exists():
        API_TOKEN = _token_path.read_text().strip()

MAX_RETRIES = 3
RETRY_BACKOFF = 2  # seconds, doubles each attempt


def _headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {API_TOKEN}",
        "X-Agent-ID": AGENT_ID,
        "Content-Type": "application/json",
    }


def _post_with_retry(url: str, payload: dict[str, Any], timeout: int = 30) -> dict[str, Any]:
    """POST with exponential backoff retry."""
    last_error = None
    for attempt in range(MAX_RETRIES):
        try:
            resp = httpx.post(url, headers=_headers(), json=payload, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except (httpx.HTTPStatusError, httpx.ConnectError, httpx.TimeoutException) as e:
            last_error = e
            if attempt < MAX_RETRIES - 1:
                wait = RETRY_BACKOFF * (2**attempt)
                logger.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                logger.error(f"All {MAX_RETRIES} attempts failed: {e}")
    raise last_error  # type: ignore[misc]


def health_check() -> bool:
    """Check if unified-memory API is reachable."""
    try:
        resp = httpx.get(f"{API_BASE}/v1/health", timeout=10)
        return resp.status_code == 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return False


def store_note(
    title: str,
    content: str,
    note_type: str = "video",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Store a video note as a memory with note-like metadata.

    The /v1/notes/ endpoint doesn't exist in the current API.
    Instead, store as a memory with type:note tag so the Notion sync
    pipeline picks it up. The MCP note_create tool can be used from
    agent context for proper Notion note creation.
    """
    note_metadata = metadata or {}
    note_metadata["note_type"] = note_type
    note_metadata["title"] = title

    tags = [
        "source:openclaw-main",
        "project:ai-knowledge-base",
        "type:note",
        f"area:{note_metadata.get('area', 'vecia')}",
        "youtube-knowledge-base",
    ]
    if note_metadata.get("video_id"):
        tags.append(f"video-{note_metadata['video_id']}")

    payload = {
        "content": f"# {title}\n\n{content[:4000]}",
        "namespace": "/alex/openclaw/videos/",
        "tags": tags,
        "metadata": note_metadata,
    }
    return _post_with_retry(f"{API_BASE}/v1/memories/", payload)


def store_memory(
    content: str,
    tags: list[str] | None = None,
    namespace: str = "/alex/openclaw/videos/",
    metadata: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Store a memory in unified-memory (for agent retrieval).

    CRITICAL: Trailing slash on endpoint — without it, 301 redirect loses the body.
    """
    payload = {
        "content": content[:5000],
        "namespace": namespace,
        "tags": tags or [],
        "metadata": metadata or {},
    }
    return _post_with_retry(f"{API_BASE}/v1/memories/", payload)
