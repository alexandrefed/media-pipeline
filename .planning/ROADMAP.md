# Roadmap: media-pipeline

## Overview

Wire existing extraction, processing, and storage components to a Telegram-first intake flow via OpenClaw, then layer on scheduled delivery, automated watching, operations hardening, and template extraction. This is primarily a brownfield wiring project -- most components exist and work. The work is configuration, routing, verification, and filling gaps (short-form mode, actionability tagging, spaced repetition, creator polling).

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [ ] **Phase 1: Telegram Intake & End-to-End Pipeline Wiring** - Wire Telegram to existing pipeline, add short-form mode + actionability tagging, verify all 5 storage targets
- [ ] **Phase 2: Scheduled Knowledge Delivery** - Daily spaced repetition reminders and weekly synthesis digest via OpenClaw crons
- [ ] **Phase 3: Automated Creator Watching** - Poll 15 creator accounts automatically, deduplicate, queue for processing
- [ ] **Phase 4: Operations & Monitoring** - Cookie health checks, observability logging, security whitelisting, CLI fallback verification
- [ ] **Phase 5: Reusable Workflow Template** - Externalize config, document Inputs-Pipe-Outputs pattern for future workflows

## Phase Details

### Phase 1: Telegram Intake & End-to-End Pipeline Wiring
**Goal**: User can forward any URL from phone to Telegram and receive processed knowledge back, with all 5 storage targets written
**Depends on**: Nothing (first phase)
**Requirements**: INTAKE-01, INTAKE-02, INTAKE-03, EXTRACT-01, EXTRACT-02, EXTRACT-03, EXTRACT-04, EXTRACT-05, PROC-01, PROC-02, PROC-03, PROC-04, PROC-05, PROC-06, PROC-07, STORE-01, STORE-02, STORE-03, STORE-04, STORE-05, STORE-06, DELIVER-01
**Success Criteria** (what must be TRUE):
  1. User sends a YouTube URL to Telegram bot and receives a processing confirmation with summary within 15 minutes, with memories in unified-memory, note in Notion, .md in Obsidian, entities in Neo4j, embeddings in pgvector
  2. User sends an Instagram Reel URL and receives a single concise note (short-form mode) with all 5 storage targets written
  3. Each takeaway in any processed content is classified as actionable/reference/awareness and actionable items are tagged with spaced-repetition metadata
  4. Non-URL messages to the bot are handled normally by OpenClaw (not routed to media agent)
  5. Processing failures produce a Telegram error message with suggested fix (e.g., "cookies expired")
**Plans**: 5 plans

Plans:
- [ ] 01-01-PLAN.md -- Update media agent: path fix, faster-whisper, short-form mode, Telegram confirmation
- [ ] 01-02-PLAN.md -- Actionability tagging in analyzers + standardized tags in store scripts
- [ ] 01-03-PLAN.md -- OpenClaw Telegram plugin config + orchestrator URL routing
- [ ] 01-04-PLAN.md -- Gaming-PC environment fix (yt-dlp, faster-whisper, .env, workspace)
- [ ] 01-05-PLAN.md -- End-to-end integration testing (YouTube + Instagram + negative tests)

### Phase 2: Scheduled Knowledge Delivery
**Goal**: User receives daily actionable reminders and weekly content digests via Telegram without lifting a finger
**Depends on**: Phase 1
**Requirements**: DELIVER-02, DELIVER-03, DELIVER-04
**Success Criteria** (what must be TRUE):
  1. User receives a Telegram message at 9 AM daily with up to 5 actionable items due for review, each with inline buttons (Done / Not Relevant / Remind Later)
  2. Tapping Done removes the item from the queue; tapping Not Relevant dismisses it; tapping Remind Later pushes it 3 days
  3. User receives a weekly synthesis digest Sunday 8 PM with total videos processed, top themes, and top actionable items
**Plans**: TBD

### Phase 3: Automated Creator Watching
**Goal**: New content from 15 watched accounts is discovered and processed automatically without user intervention
**Depends on**: Phase 1
**Requirements**: WATCH-01, WATCH-02, WATCH-03, WATCH-04, INTAKE-04
**Success Criteria** (what must be TRUE):
  1. New YouTube videos from 6 watched channels are detected within 4 hours of upload and auto-processed
  2. New Instagram posts from 9 watched accounts are detected within 6 hours and auto-processed
  3. Duplicate URLs are skipped (no re-processing of already-known content)
  4. User can add/remove watched accounts via Telegram commands (watch/unwatch/watchlist)
**Plans**: TBD

### Phase 4: Operations & Monitoring
**Goal**: Pipeline runs reliably with proactive alerts, observability, and security -- no silent failures
**Depends on**: Phase 1
**Requirements**: EXTRACT-06, INTAKE-05, OPS-01, OPS-02, OPS-03
**Success Criteria** (what must be TRUE):
  1. User receives a proactive Telegram alert when Instagram/Vimeo cookies are expiring (checked every 12h)
  2. Every processed URL is logged in unified-memory with status (success/failure/partial) and platform metadata
  3. Processing failures generate a Telegram notification with error context and suggested fix
  4. Messages from non-whitelisted Telegram users are silently dropped
  5. CLI intake via `uv run python main.py streamlined <URL>` works correctly at the updated project path
**Plans**: TBD

### Phase 5: Reusable Workflow Template
**Goal**: Adding a new content type or output target requires config changes only, and the pipeline pattern is documented for reuse
**Depends on**: Phase 4
**Requirements**: TMPL-01, TMPL-02, TMPL-03
**Success Criteria** (what must be TRUE):
  1. All pipeline settings (intake channels, processing agents, output targets, watchlist) are in pipeline-config.yaml -- no hardcoded values
  2. Each pipeline stage (intake, extraction, processing, storage, delivery) is independently replaceable without modifying other stages
  3. A developer reading the template documentation can create a minimal new workflow in under 1 day
**Plans**: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 4 -> 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Telegram Intake & Pipeline Wiring | 0/5 | Planned | - |
| 2. Scheduled Knowledge Delivery | 0/? | Not started | - |
| 3. Automated Creator Watching | 0/? | Not started | - |
| 4. Operations & Monitoring | 0/? | Not started | - |
| 5. Reusable Workflow Template | 0/? | Not started | - |
