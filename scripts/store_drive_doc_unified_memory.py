#!/usr/bin/env python3
"""Temporary helper to store a converted Google Drive document in unified-memory."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.storage.unified_memory_client import health_check, store_memory, store_note

folder = Path(sys.argv[1])
md_path = folder / "source.md"
analysis_path = folder / "analysis.json"
metadata_path = folder / "metadata.json"
md = md_path.read_text(encoding="utf-8")
analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

if not health_check():
    raise SystemExit("unified-memory health check failed")

tags = [
    "source:google-drive",
    "project:youtube-kb",
    "project:media-pipeline",
    "type:document-knowledge",
    "type:markdown-conversion",
    "area:vecia",
    "tool-claude-code",
    "tool-codex-cli",
    "tool-gemini-cli",
    "tool-pal-mcp-server",
    "feature-mcp",
    "feature-agents",
    f"document:{metadata['video_id']}",
]
base_meta = {
    "title": metadata["title"],
    "author": metadata["author"],
    "source_url": metadata["source_url"],
    "source_type": metadata["source_type"],
    "source_markdown": str(md_path),
    "folder": str(folder),
    "area": "vecia",
}

ids = []
note_content = analysis["summary"] + "\n\n## Key Takeaways\n" + "\n".join(
    f"- [{t['actionability']}] {t['takeaway']}" for t in analysis["key_takeaways"]
)
res = store_note(metadata["title"], note_content, note_type="document", metadata=base_meta)
ids.append({"kind": "note", "id": res.get("id") or res.get("uuid") or res.get("memory", {}).get("id"), "raw": res})

# Store overview/analysis memory
analysis_memory = "# " + metadata["title"] + "\n\n" + note_content + "\n\n## Commands\n" + "\n".join(
    f"- `{c['command']}` — {c['purpose']}" for c in analysis["commands"]
)
res = store_memory(analysis_memory, tags=tags + ["content-type:overview"], namespace="/alex/openclaw/documents/", metadata=base_meta | {"chunk": "overview"})
ids.append({"kind": "overview", "id": res.get("id") or res.get("uuid") or res.get("memory", {}).get("id"), "raw": res})

# Store full markdown in chunks within API content limit.
chunk_size = 4500
for i in range(0, len(md), chunk_size):
    chunk_no = i // chunk_size + 1
    chunk = md[i:i+chunk_size]
    content = f"# {metadata['title']} — Markdown chunk {chunk_no}\n\n{chunk}"
    res = store_memory(content, tags=tags + ["content-type:full-markdown", f"chunk:{chunk_no}"], namespace="/alex/openclaw/documents/", metadata=base_meta | {"chunk": chunk_no, "source_file": str(md_path)})
    ids.append({"kind": f"markdown-chunk-{chunk_no}", "id": res.get("id") or res.get("uuid") or res.get("memory", {}).get("id"), "raw": res})

(folder / "unified_memory_store_results.json").write_text(json.dumps(ids, indent=2), encoding="utf-8")
print(json.dumps({"stored": len(ids), "ids": [{"kind": x["kind"], "id": x["id"]} for x in ids]}, indent=2))
