"""
Unified Memory API client for storing video notes and memories.

Calls the unified-memory HTTP API directly instead of requiring MCP tool context.
See UNIFIED-MEMORY-INTEGRATION.md for API reference.
"""

import logging
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Config from environment, with token file fallback
# Default is gaming-PC over the tailnet — the host that actually serves this API.
# It was previously bluelion-vps (85.25.172.47:8085), which answers nothing; the
# storage step failed silently for every run that did not set MEMORY_BASE_URL.
API_BASE = os.environ.get("MEMORY_BASE_URL", "http://100.112.33.86:8085")

# Keychain item the Mac's MCP config uses. Its token belongs to claude-main, so a
# token read from it must be sent as claude-main: as openclaw-main it gets 403.
_KEYCHAIN_SERVICE = "mcp-api/gateway-token"
_KEYCHAIN_AGENT = "claude-main"


def _keychain_token() -> str:
    """The gateway token from the macOS keychain, or "" off a Mac / when absent.

    Read into memory only, never written to disk (2026-10-12, task 7dec0486: a
    Mac run had no token at all, sent "Bearer " and every write failed).
    """
    if sys.platform != "darwin":
        return ""
    try:
        out = subprocess.run(  # noqa: S603 — fixed argv, no shell
            [
                "/usr/bin/security",
                "find-generic-password",
                "-s",
                _KEYCHAIN_SERVICE,
                "-a",
                "default",
                "-w",
            ],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return out.stdout.strip() if out.returncode == 0 else ""


# Token: env var first, then ~/.config/unified-memory/token (the box), then the
# macOS keychain. The agent id follows the token's owner unless set explicitly.
API_TOKEN = os.environ.get("MEMORY_TOKEN", "")
_token_owner = "openclaw-main"
if not API_TOKEN:
    _token_path = Path.home() / ".config" / "unified-memory" / "token"
    if _token_path.exists():
        API_TOKEN = _token_path.read_text().strip()
if not API_TOKEN:
    API_TOKEN = _keychain_token()
    if API_TOKEN:
        _token_owner = _KEYCHAIN_AGENT
AGENT_ID = os.environ.get("MEMORY_AGENT_ID", _token_owner)

MAX_RETRIES = 3
RETRY_BACKOFF = 2  # seconds, doubles each attempt


def _headers() -> dict[str, str]:
    if not API_TOKEN:
        # Fail before the first write: an empty bearer makes every write 401 and
        # the run reports a partial store instead of saying why.
        raise RuntimeError(
            "No unified-memory token: set MEMORY_TOKEN, create ~/.config/unified-memory/token, "
            f"or (Mac) add the keychain item {_KEYCHAIN_SERVICE}."
        )
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
        "source:claude-main",
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


MEMORY_CHAR_LIMIT = 5000


def split_for_store(text: str, limit: int = MEMORY_CHAR_LIMIT) -> list[str]:
    """Split a section into parts that each fit one memory, at paragraph breaks.

    store_memory() keeps only the first 5,000 characters, so a longer section
    used to lose its tail in silence (2026-10-10: three of goldcast-6c25235e's
    sections ended mid-sentence). Parts after the first repeat the section's
    first line and say which part they are, so each still names its video.
    """
    if len(text) <= limit:
        return [text]
    head = text.split("\n", 1)[0][:200]
    budget = limit - len(head) - 40  # room for the "(part i of n)" header
    chunks: list[str] = []
    current = ""
    for block in text.split("\n\n"):
        while len(block) > budget:  # one paragraph longer than a whole part
            if current:
                chunks.append(current)
                current = ""
            chunks.append(block[:budget])
            block = block[budget:]
        candidate = f"{current}\n\n{block}" if current else block
        if len(candidate) > budget:
            chunks.append(current)
            current = block
        else:
            current = candidate
    if current:
        chunks.append(current)
    n = len(chunks)
    return [chunks[0]] + [
        f"{head} (part {i} of {n})\n\n{c}" for i, c in enumerate(chunks[1:], start=2)
    ]


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
