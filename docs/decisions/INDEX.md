# Decisions Index

Architectural Decision Records for media-pipeline. One file per decision:
`docs/decisions/NNNN-slug.md`. Newest at top. Living history of *why* the pipeline
is shaped the way it is — the dated entries in `CONTEXT.md` are the source these
graduate from.

| # | Decision | Date | Status |
|---|----------|------|--------|
| — | Summary generation is LLM-written by the agent from `analysis.json`, not a Python/regex script | 2026-05-24 | Active |
| — | Auto-enhancer uses word-boundary regex matching (no substring corruption) | 2026-05-24 | Active |
| — | Video folders deduplicated by video ID before creation | 2026-05-24 | Active |
| — | OpenClaw → Hermes migration on gaming-PC (self-improving media agent) | 2026-05-16 | Active |
| — | unified-memory API runs on gaming-PC (tailnet `100.112.33.86:8085` / `127.0.0.1:8085`), NOT the VPS | 2026-05-25 | Active |
| — | Extraction commands must exit non-zero on empty output; browser/CDN fallbacks for IG/X/Loom | 2026-08-02 | Active |
| — | n8n removed — Hermes gateway handles Telegram intake | 2026-03-29 | Active |
| — | Neo4j graph extraction disabled per V2 vision | 2026-04-14 | Active |

## Known open items (not yet ADR'd)

- **unified-memory namespace**: store scripts write to `/alex/openclaw/videos/` (legacy name from the OpenClaw era). Kept as-is to avoid fragmenting the ~127 existing videos across namespaces; retrieval works fine. Revisit only if consolidating namespaces project-wide.

> To formalize any row above into a full ADR, run `/icm docs` — it migrates decisions
> into `NNNN-slug.md` files with frontmatter and pgvector indexing.
