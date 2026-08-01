# YouTube duplicate caption cleanup for analysis

> **Origin**: Crystallized by the Hermes self-improvement Curator (2026-07-06). Ported into the repo 2026-08-02.

## When this applies

Some YouTube caption extractions produce a `transcript_enhanced.txt` where short phrases are repeated 2-3 times in sequence. The enhanced transcript is still usable, but direct in-context analysis becomes noisy and may over-weight repeated statements.

Example symptom:

```text
Hey everyone, today. I'm going to share a. Hey everyone, today. I'm going to share a complete course...
```

## Recommended handling

1. Preserve the pipeline outputs as-is: `transcript_raw.txt`, `transcript_enhanced.txt`.
2. Create a helper file for analysis only, e.g. `transcript_cleaned_for_analysis.txt`.
3. Collapse repeated adjacent n-grams/phrases, but do not replace the canonical enhanced transcript unless the user explicitly asks.
4. Use the cleaned helper to extract tools, workflows, commands, takeaways, and implementation details.
5. Mention the helper file in the final report if it was created.

## Minimal cleanup script

Run from the media-pipeline repo with `VDIR` pointing at the video folder:

```bash
python3 - <<'PY'
from pathlib import Path
import re

vdir = Path("$VDIR")
p = vdir / "transcript_enhanced.txt"
t = p.read_text()

# Strip auto-enhancement report if present, while keeping transcript text.
body = t.split('=' * 80, 1)[1] if '=' * 80 in t else t
body = body.split('=' * 80 + '\nAUTO-ENHANCEMENT REPORT')[0]
body = re.sub(r'\s+', ' ', body).strip()

words = body.split()

def dedup_once(words):
    out = []
    i = 0
    while i < len(words):
        matched = False
        for n in range(15, 1, -1):
            if i + 2 * n <= len(words) and words[i:i+n] == words[i+n:i+2*n]:
                j = i + n
                while j + n <= len(words) and words[i:i+n] == words[j:j+n]:
                    j += n
                out.extend(words[i:i+n])
                i = j
                matched = True
                break
        if not matched:
            out.append(words[i])
            i += 1
    return out

for _ in range(3):
    new_words = dedup_once(words)
    if len(new_words) == len(words):
        break
    words = new_words

clean = ' '.join(words)
clean = re.sub(r'\s+([.,?!:;])', r'\1', clean)
(vdir / "transcript_cleaned_for_analysis.txt").write_text(clean)
print(f"wrote {vdir / 'transcript_cleaned_for_analysis.txt'} ({len(clean)} chars)")
PY
```

If using a literal heredoc, replace `Path("$VDIR")` with an explicit path or export/interpolate `VDIR` in the shell before running.
