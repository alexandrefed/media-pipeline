# Stiles Dichter's "saved reels → AI setup" vs our media pipeline

Date: 2026-10-02 · Task: c58787e8 · Sources: three public guides by Stiles Dichter (@stilesai), saved word for word in `dev/platform/book-processing/processing/stiles-dichter-guides/` (`campaign.md`, `let-your-ai-doomscroll.md`, `test-new-models.md`).

## Bottom line

We are ahead on the front half: getting content in, transcribing it and keeping it searchable. He is ahead on the back half: his process **ends in skills that change how Claude works**, ours **ended in memories that sit there until someone searches**. We do have his merge step: the wiki (`~/Documents/WikiVault`) merges sources with line citations and a contradiction gate, but it covered only 42 of the 148 substantive processed videos, and Neo4j extraction is switched off, so nothing triaged the rest. *Correction 2026-10-04: the first version of this note said we had no cross-source merge; that was wrong, the wiki is it.* Follow-up done the same week: all 224 items triaged ([2026-10-video-triage.md](2026-10-video-triage.md)) and four skills built from the clearest clusters.

## His method in one paragraph

Sort Instagram saves into topic collections. Claude (desktop app + Claude in Chrome, logged into Instagram) opens each reel, reads the caption, transcribes the audio, looks at the frames, and writes up what it teaches as steps or rules with the link. It does the same for the guides that "comment this word" bots sent to his DMs. Everything for one topic goes into a Claude Project, where Claude groups it, keeps the most specific version of each idea, cites the source, drops the rest and flags contradictions: one playbook. The playbook becomes one skill per job plus one skill that runs them in order ("run a campaign for my new product"). A weekly scheduled task checks for new saves, updates the playbook and skills, and reports what changed. His own result: 7 reels became 3 skills that script, grade and edit his reels.

## Step by step

| His step | What our stack does today | Gap |
|---|---|---|
| 0. Sort saves into topic collections | Nothing. Intake is one link at a time, forwarded to the Telegram bot or run from the CLI (`CLAUDE.md`) | No grouping by topic at intake. Phase 3 of the roadmap (poll 15 creator accounts) is not started (`.planning/ROADMAP.md`) |
| 1a. Read each reel: caption, audio, frames | yt-dlp + faster-whisper on the gaming-PC GPU, with a browser fallback when Instagram blocks (`.claude/agents/references/instagram-browser-cdn-fallback.md`). Carousels are read slide by slide with vision (`references/instagram-image-carousel.md`, `scripts/ig_carousel_to_transcript.py`). Also YouTube, Vimeo, TikTok, X, Loom, Skool | **We do not look at reel frames.** On-screen text and visual demonstrations in reels are lost; only carousels get vision |
| 1b. Write up what each one teaches | An LLM summary and an analysis per item, takeaways tagged actionable / reference / awareness (`workspace/videos/<folder>/summary.md`, `analysis.json`) | Close. Ours is a summary; his is "steps or rules", which is closer to something a skill can use |
| 1c. DM "comment-a-keyword" freebies | Not handled | Small: forwarding the freebie link to the Telegram bot already works for any URL. We should not have an agent read Alexandre's DMs |
| 2. Merge by topic into one playbook | The wiki (`~/Documents/WikiVault`) merges sources into topic pages with line citations, and `bin/check-contradictions.py` gates contradictions at ingest. Per-video and per-caption dedup in the pipeline (`src/processing/caption_dedup.py`) | **Coverage:** the wiki holds 42 of 148 substantive videos (sports, career and content: none). Neo4j extraction is disabled (`.claude/agents/media-ingestion-agent.md` §4c), so nothing triaged the rest until 2026-10-04 |
| 3. Playbook → skills, plus one that runs them | Skills exist but are written by hand (`~/.claude/skills/content-engine`, `voice-dna`). Nothing turns ingested knowledge into a skill | **The main gap.** Ingested knowledge never changes how Claude behaves unless someone searches it |
| 4. Weekly check, update, report what changed | No scheduler in media-pipeline. A Sunday digest is planned (roadmap Phase 2, not started) | Partly planned, but planned as a digest to read, not an update to the skills |

## What we do that he does not

- **Intake from the phone without opening Claude:** forward a link to the bot, the gaming-PC does the rest.
- **No Claude usage for transcription:** he warns his method "uses a good amount of usage" because Claude drives the browser and transcribes every reel. Ours runs on local Whisper.
- **Durable search across everything:** pgvector memories, QMD full text, Notion, and the files themselves, reachable by any agent rather than locked in one Claude Project.
- **Sources beyond Instagram:** YouTube, Vimeo, TikTok, X, Loom, Skool courses, and Claude artifacts (the last two added 2026-09-30 and 2026-10-01).
- **Checks that the work really landed:** a completion stamp written last (`src/pipeline/completion.py`) and a ledger that verifies items are retrievable.

## Recommendation, and what happened

The first version recommended a by-hand trial on making reels. Alexandre corrected it on 2026-10-03: the trial is about skills **built from the videos the pipeline processed**, and reel-making belongs to the content lane (handed to `content-main`, task 3ceda4f4).

What was done instead (task 4f74d683):
1. All 224 processed items triaged: [2026-10-video-triage.md](2026-10-video-triage.md) + JSON.
2. Four skills built from the clearest clusters, each with a cited playbook, in `dev/platform/agentic-platform/skills/`: `endurance-strength-programming`, `agent-memory-design`, `job-search-tactics`, `skill-authoring`.
3. Follow-ups filed: the duplicate YouTube-stub bug, wiki ingest of the ~106 substantive items not yet in the wiki, a check-in on 2026-10-18.

The remaining gap from his method is step 4, a scheduled refresh that updates playbooks and skills as new videos arrive. Decide after the 2026-10-18 check-in.

The frame gap stands: we don't run vision on reel frames, only on carousels.

## His model-testing guide, beside our rules

His third guide tests every new model on three of your own tasks: does it sound like me, does it cut corners (passes by deleting something), does it finish a long job. Each task is run twice and graded against your best answer so far. Our model rules (global CLAUDE.md, 2026-09-01 bake-off) choose models by role and cost; his three tasks would make a cheap standing check to rerun when a model ships, with Alexandre's own writing as the voice task.
