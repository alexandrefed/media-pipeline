# Triage of the 224 processed videos

Date: 2026-10-04 · Task: 4f74d683 · Data: [2026-10-video-triage.json](2026-10-video-triage.json), one row per item: domain, sub-topic, type, quality, the job it teaches, whether it is in the wiki, which wiki pages cite it, which skill it fed.

## Bottom line

The pipeline has processed 224 items, and **148 are substantive**: most are agent and Claude Code tutorials, plus a usable slice of training, business and job-search material. Nothing triaged them before today: the wiki holds only 42 of the 148, and the graph, although extraction into it has run since 2026-07-13, splits every entity per writing agent and duplicates it across types, so it cannot group videos by topic (fix: task 46b4c5d8). *(Corrected the same day: the first version said Neo4j extraction was switched off; the docs I relied on were stale.)* Four skills were built from the clearest clusters (see below). 48 items failed, and 40 of those come from one pipeline bug.

## How it was done

Two read-only passes on the gaming-PC (`/home/alexandre/projects/workflows/media-pipeline/workspace/videos/`) read each item's `summary.md`, `analysis.json`, or the start of the transcript when no summary exists. Each item got a domain, sub-topic, type, quality grade and "the job it would teach someone to do better". Wiki coverage is matched against `~/Documents/WikiVault/raw/videos/` and the citations inside `atlas/` pages. Items without a summary were judged from their transcript opening (16 items, listed in the JSON as substantive but less certain).

## Counts

| Domain | Items | Substantive | In the wiki |
|---|---|---|---|
| Agents, Claude Code, AI tooling, knowledge tools | 118 | 102 | 38 |
| Business: offers, ads, validation, operations | 25 | 16 | 6 |
| Sports and training | 13 | 12 | 0 |
| Content making | 6 | 6 | 0 |
| Career / job search | 4 | 4 | 0 |
| Soft skills | 4 | 2 | 2 |
| Other (dashboards, Postgres, generative art, EU politics) | 6 | 6 | 2 |
| Failed | 48 | 0 | 0 |
| **Total** | **224** | **148** | **48 files in the wiki's source folder, 42 of them substantive** |

Platforms: 126 YouTube, 88 Instagram, 5 local, 3 X, 1 Loom, 1 Drive.

## What failed, and why it matters

- **40 YouTube-labelled stubs** hold only `metadata.json`. Each one shares its shortcode with an Instagram item that processed correctly. The pipeline creates a second, empty "yt" folder for some Instagram reels. Cost: inflated counts, noise in every listing, and a risk that an agent reads the empty twin. Filed as a task.
- **1 empty folder** (`20260823--DcXaxzwFect--ig--agentic-james--…`).
- **7 metadata-only or duplicate items**: four local Alegria recordings and one Carl Vellotti masterclass that were never transcribed, plus three duplicates. The four Alegria talks are French event recordings that may be worth transcribing.

## Clusters and the skill each one fed

| Cluster | Items | Became |
|---|---|---|
| Training: aerobic base, Billat intervals, downhill, Soviet submax strength, contrast power, high-low split, mountain endurance, kettlebell, RDL, weighted vest | 12 | skill `endurance-strength-programming` |
| Agent memory and context: graphs, ontology, indexes, wiki as memory, lessons from traces, cleaning stale memory, progressive disclosure, cheap rerank | 16 | skill `agent-memory-design` |
| Job search: Reddit/X sourcing, ATS `site:` searches, outreach after applying, recruiter messages, proof-of-work portfolio | 6 | skill `job-search-tactics` |
| Writing skills: skill vs MCP vs sub-agent vs command, skill factories, improving a skill from transcripts | 7 | skill `skill-authoring` |
| Content making (growth plan, daily skill pipeline, capture-to-research, persona accounts, stage-gated animation) | 6 | handed to the content lane (task 3ceda4f4) |

The skills live in `dev/platform/agentic-platform/skills/<name>/`; each has a cited playbook in `references/playbook.md`.

## Candidate skills not built yet

Ranked by substantive items. Each would take the same path: extract cited rules, merge, write the skill.

1. **Plan, build and verify with coding agents** (~17): plan-first, verifier agents, end-to-end tests, loops with gates, task sizing by context budget, tracing. Much of this is already fleet policy in the global CLAUDE.md, so a skill would mostly add the verification recipes.
2. **Multi-agent setup and harness design** (~15): orchestrators, peer-to-peer messaging, PTY supervision, sandboxes, software factories, multi-model teams.
3. **Always-on personal agents** (6): OpenClaw / Hermes deployment, VPS hardening, cost routing.
4. **Offers and paid acquisition** (~10): Meta ads testing and mechanics, ad-as-content hooks, customer-language positioning, demand validation, advertorial landers. For Vecia.
5. **MCP and tool design** (4) and **cheap classifiers as a decision layer** (4).
6. **n8n with Claude Code** (5).
7. **Knowledge tools** (~7): Obsidian, Notion, NotebookLM setups.

## Follow-ups filed

- Fix the duplicate YouTube-stub bug and remove the 40 empty twins.
- Bring the ~106 substantive items that are not in the wiki into it, starting with the clusters above, so the wiki stays the merge layer.
- Check on 2026-10-18 whether agents load the four skills and whether they helped.
