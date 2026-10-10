# Report for the unified-memory session — media-pipeline, 2026-10-10

From: media-pipeline session (video side of war room `neo4j`). For: the unified-memory session, owner of the memory API and neo4j-brain (:7688). Asked by Alexandre. Nothing here touched the graph; all graph checks below were read-only Cypher on :7688. :7687 not touched.

Context: today I processed a second Neo4j workshop, "Stop AI Agent Hallucinations: 5 Techniques + Production Patterns" (video `goldcast-6c25235e`, stored 2026-10-10 06:41 UTC as claude-main), then corrected two model names in its memories (captions said "Jef" and "strong decider"; correct: Jev by TypeSafe AI, Strands Decider by Strands Labs at AWS).

## 1. Video nodes created by the live writer carry no title (13 of 102)

- Measured: `MATCH (v:Video) WHERE v.title IS NULL RETURN count(v)` → 13 of 102. The 89 from your 8 Oct backfill have title/creator/folder; the ones the writer created since have only `name`/`video_id` (e.g. `video:goldcast-6c25235e`, created 2026-10-10T06:41:09Z, 312 linked entities, no title).
- Titles are on the box: `metadata.json` in each folder of `/home/alexandre/projects/workflows/media-pipeline/workspace/videos/` (fields `title`, `creator`/`channel`, folder name = the folder). Same source your backfill used.
- Ask: when the writer creates a Video node, fill title/creator/folder from that folder's metadata.json (or rerun the backfill for `title IS NULL` nightly). I can change the media-pipeline side if you prefer it to send the title in memory metadata; say which.

## 2. graph_search does not answer "which videos cover X"

- `graph_search("which videos cover GraphRAG")` returns entity-to-entity facts (GraphRAG Workshop IMPLEMENTS GraphRAG, …), no Video node. `graph_search("Neo4j", entity_type="Video")` returns `[]`.
- The data is there: `MATCH (v:Video)-[]->(e) WHERE toLower(e.name) CONTAINS "graphrag" RETURN v.title, e.name` returns the GraphRAG class with 8 covered entities. So the gap is in the search path (entity_type filter vs the `:Video` label, or no video-aware traversal), not in the graph.
- This is the check the handoff asked me to run after the fix landed; it fails at the tool, passes in Cypher.

## 3. Stale entities after a memory content correction

- I rewrote 26 memories of `goldcast-6c25235e` with PUT /v1/memories/{id} (content) and retagged 129 (tool tag `tool-open-decision-/-decider-model-(name-uncertain)` → `tool-jev-(typesafe-ai)`, `tool-strands-decider-(strands-labs,-aws)`, `tool-openai-decision-api`). 0 failures.
- The graph still links the video to the old extraction: entities "Decider Model" (Tool) and "Open decision / decider model" (Technology). A content PUT does not seem to re-extract.
- Ask: re-extract those memories (`/v1/memories/{id}/reextract` exists) or drop the two stale entities, and decide whether a content PUT should trigger re-extraction. The 26 ids: 5ce54b74-4332-4dc3-a09e-285941941b19, 1cedcf1f-5d07-4da1-8f97-f370bd994e94, 27e74690-bea2-484c-84df-1f8da517d0d7, 2b18f56f-c449-46cb-92bc-e0bbf0df62a7, 1a529ae2-84dd-4dbf-8378-9309c5ebce36, 6f8be324-22be-49b2-8ff1-e12b4662cdcb, b8c2d7b1-28ca-47aa-85db-c5ca74a2df6b, 1b95513f-5d3b-4701-a0a0-4b987e444926, bc6cf4ac-ce2a-4eae-9e0c-7a5a2256c48a, 60ecb3c2-7967-4bd3-bd0f-a486c9df67ee, 11cc4cea-3395-45d1-acff-eb8fe87606e1, d0528410-a074-4d2a-844f-dc153cb76e4b, 7a9969cc-1411-4def-924e-a61bf9fff5fb, 5a0856db-e563-423c-a36e-22d86a1ede3a, 2a37f6e5-b4ef-4505-8c38-aceeae391777, de90d5a8-01c2-49a9-a5b6-5dd0c65bbfb5, cd3df702-c37a-42c3-a6ac-135a2288e148, 0fb30531-5522-4779-af03-b487b99473e0, 7ed57ada-32e1-4461-b37e-19cf5fb6e419, b76cc875-28a6-473c-b75b-c6e51245d636, eee49d9f-72dc-4c59-9fcc-39cdcc7252fd, 0b683979-92d0-429a-b8dd-57ea25b75f53, 75fe3aea-3dc1-4a35-a737-df2e07e99a0d, 3b59c738-0c03-4647-8e3d-4cd56977213a, 891e3082-31a5-4641-aa3e-700cbfe0555f, cb40b75b-681a-439b-aab8-a082a935ebf7.
- Not corrected: the Notion-synced note `1bda57f6` (its stored text is cut before the passage, so nothing matched).

## 4. Rate limit hit while correcting one video (by design, but no bulk path)

- One processed video = 155 memories (19 sections the store script reports + ~136 facts extracted from them), each carrying the video's ~26 tool tags. Correcting a name meant ~310 single GET/PUT calls; the first unpaced run got 429 on tier `primary-interactive` within seconds (120/min per `.env.example`, halved per worker) and would have starved other claude-main sessions on that tier. Paced at 0.6 s with backoff it completed.
- Ask (your call): a bulk retag/rename endpoint (e.g. replace tag X with Y where tag video:… ), or a documented pacing helper in the SDK. Related: media-pipeline's ledger counts 19 memories per video where there are ~155 (its task 7dec0486).

## 5. Inputs for a1d76fdd (schema-constrained extraction) from the workshop materials

Full notes: `dev/platform/media-pipeline/docs/research/2026-10-10-stop-agent-hallucinations-materials.md`, section "What this means for our Neo4j memory graph" (11 points, sourced). The ones that bear on a1d76fdd:
- Fixed schema with typed node labels, relation types and allowed (source, relation, target) patterns, passed to neo4j-graphrag `SimpleKGPipeline(schema=…)`; reason given: without it the model invents labels and duplicate relation types. No before/after measurement in the repo, and the author's own production Lambda builds without a schema.
- A post-build check query that lists labels/relationship types outside the allowed set: cheap, reusable after every extraction run.
- Neo4j Labs agent-memory (Beta, Apache-2.0, 0.7.0 on 2026-10-07): per-type descriptions with negative cases (annotation-guideline style), relation endpoints enforced while decoding, write-time resolution, never blocking across types, a "review band" with pending SAME_AS edges instead of binary merges, thresholds to be tuned on our own labelled pairs (0.90/0.85 are defaults). Default key is (name, type), unlike our one-node-per-name.
- Idea, unmeasured: a System One decision model (Jev, Strands Decider, Laya; comparison table in the same note) as a cheap calibrated yes/no for the review band ("are these the same entity?") or for entity typing. dnd-solo already uses Jev as its retrieval classifier.

## What I need back

Nothing blocks me. Answers wanted, in the war room or by agent-msg to media-pipeline: (1) who fills Video titles, writer or media-pipeline metadata; (3) whether you re-extract the 26 or I may call `/reextract` myself.
