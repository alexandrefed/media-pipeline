---
description: Show all pending videos with direct URLs
---

# Pending Videos for Processing

@list.md

## Next Videos to Process:
!grep -v "✅ DONE" list.md | grep -v "❌ NO SUBTITLES" | head -10

## Quick Start Commands:
The next video can be extracted with:
```bash
# Extract the next pending video
uv run python main.py extract "URL_FROM_ABOVE"
```

## Current Statistics:
- Videos completed: !grep -c "✅ DONE" list.md
- Videos pending: !grep -v "✅ DONE" list.md | grep -v "❌ NO SUBTITLES" | wc -l
- Success rate: High quality manual chunking achieving 13x larger chunks