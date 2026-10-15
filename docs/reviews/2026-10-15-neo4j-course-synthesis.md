# Neo4j course synthesis: three Road to NODES 2026 workshops, joined

**Nothing needed from Alexandre.** 0 decisions, 5 things to know, 1 lesson; about 8 minutes. Written for the MUTORA-KG agent and for unified-memory's brain graph; Alexandre may skim the first topic.

| # | Tag | Topic |
|---|---|---|
| 1 | Know | The new course builds deterministic structure for an agent to navigate, which neither earlier workshop does |
| 2 | Know | The three workshops disagree mainly on when to extract entities |
| 3 | Know | For MUTORA-KG: a table-of-contents tree of each book would let seats navigate and cite sections |
| 4 | Know | For MUTORA-KG: gap queries, theme detection and current Cypher skills fit work already planned |
| 5 | Know | For the brain graph: a deterministic outline of videos and documents would answer "which videos cover X" |
| 6 | Learn | Decide the shape of context the agent needs before choosing the query tool |

<details><summary>The three videos (all Neo4j, all in unified-memory under project:youtube-kb)</summary>


- `goldcast-2191db0b`: "GenAI and Graph Foundations: Building GraphRAG with Neo4j", 2026-10-01, Martin O'Hanlon. LLM entity extraction with a schema (SimpleKGPipeline), vector, vector-Cypher and text-to-Cypher retrievers.
- `goldcast-6c25235e`: "Stop AI Agent Hallucinations: 5 Techniques + Production Patterns", 2026-10-08, Elizabeth Fuentes Leone (AWS). GraphRAG for exact counts, semantic tool selection, multi-agent validation, guardrail hooks, steering.
- `goldcast-6622e280` (new, processed today): "Build Your First Knowledge Layer", 2026-10-15, Zach Blumenfeld and Ryan Knight (Neo4j), 2 h 04 min. A knowledge layer for an agent over a warehouse plus a PDF library, built as three "shapes".

</details>

---

## 1. The new course builds deterministic structure for an agent to navigate, which neither earlier workshop does

**Ask:** nothing needed.

**What it is about.** The new course says retrieval is solved enough; the hard part is letting an agent combine and navigate documents and a warehouse. So it builds three deterministic views ("shapes") and has the agent walk them: a zero-copy map of the warehouse schema (Connections), a parsed tree of the document library with no LLM (Table of Contents), and document clusters found with Leiden (Themes). Around them: queries that prove what is missing, Claude Code writing each Cypher query from a spec with Neo4j's maintained skills, one agent skill tying the shapes together, and entity extraction deferred on purpose.

<details><summary>The eight additions in detail (timestamps in the new video)</summary>


- **Connections, a zero-copy semantic layer** (0:32:58 to 0:46:38). The Neo4j Labs project Neocarta reads a warehouse's schema (Databricks here; BigQuery and Postgres said to work) and writes database, schema, table, column, sample-value and join nodes into Neo4j. No rows are copied; the agent reads the map through an MCP server and writes better SQL. Joins can be inferred from keys, table comments or the query log (0:41:15).
- **Table of Contents, a document tree** (0:55:41 to 1:15:48). A plain parser, no LLM, loads library, folder, document and section nodes with containment, section order and cross-document links. Node ids are hierarchical URIs (library/folder/file#section). The load is idempotent. An outline script returns the whole tree, one depth, or one document with its links; a full-text search can be scoped to everything under a URI prefix. Vector search was skipped on purpose because embeddings from different providers are not compatible.
- **Themes, communities found from links** (1:23:07 to 1:35:55). Section links are rolled up to document-to-document links, projected undirected into Graph Data Science, clustered with Leiden, and the community id written back as a theme id. Conductance measures how cleanly each theme separates; gamma sets granularity (13 themes at the default, 14 at gamma 2). Themes are named from their most-linked documents, not by an LLM.
- **Proving a negative** (1:49:03 to 1:54:15). Comparing warehouse fault codes with document search found two high-volume codes with no documentation at all, which vector search cannot answer.
- **Neo4j CLI and skill bundles with spec-driven coding** (1:04:14 to 1:09:12, 1:42:02 to 1:45:14). Claude Code writes each Cypher query from a written output spec, using maintained Neo4j skills (Cypher, GDS, drivers, MCP) installed by the CLI, so it stops writing outdated Cypher. The CLI also runs Cypher with JSON output and dumps the schema.
- **A shapes-first agent skill** (1:45:14 to 1:56:00): the tools, example questions, an "answer with evidence" rule, and no raw CLI, because the agent sidesteps the procedures with it.
- **Extraction deferred, on purpose** (1:18:09 to 1:21:19, 1:51:56). The document graph and the warehouse graph stay unlinked and the agent infers the links. The speakers say to extract domain entities (parts, codes) once titles stop carrying them; the one weak answer in the demo was exactly that case.
- **Updates and versions** (1:58:50 to 2:00:06): reload a small corpus whole; for a large one reload part of the tree; model revisions as a revision id or a document-to-revision relationship with a "latest" flag.

</details>

**Rule to keep.** When an agent must answer across documents and tables, the cause of wrong answers is usually missing structure, not a weak model; give it an outline and a schema map to walk.

---

## 2. The three workshops disagree mainly on when to extract entities

**Ask:** nothing needed.

**What it is about.** The first workshop extracts entities with an LLM up front; the new one defers extraction. The other differences follow from that.

- All three agree vector search alone is not enough. The new course and `goldcast-6c25235e` give the same reasons: counts and "what is missing" questions.
- Entity extraction is the real disagreement. `goldcast-2191db0b` says extract with an LLM and a schema (unconstrained extraction gives a vague graph). The new course says navigate by structure first and extract only when needed. Neither calls the other wrong.
- Cypher at runtime or at build time. In the two earlier workshops an LLM writes Cypher while answering. In the new course Claude Code writes it once, at build time, behind fixed scripts, and the agent only calls those scripts.
- Only `goldcast-6c25235e` builds guardrails (hooks, steering) and any evaluation. The new course has no eval harness and says so (0:28:33).

**Rule to keep.** When a graph's entities are vague or duplicated, the cause is usually extraction before structure; build the deterministic skeleton first and extract against it.

<details><summary>Sources</summary>

- Transcripts: `workspace/videos/20261015--goldcast-6622e280--local--neo4j--build-your-first-knowledge-layer/transcript_readable.md` (every word checked against the caption track by script: 19,844 words identical) and the two earlier folders' `transcript_readable.md`, on the gaming-PC under `/home/alexandre/projects/workflows/media-pipeline/workspace/videos/`.
- Summaries: `summary.md` in each folder. Numbers such as "183 documents, 985 sections" come from garbled captions and are marked as likely in the new summary.
- Repo: no URL is spoken in the new course; it is a free GraphAcademy course that runs in GitHub Codespaces or locally.

</details>

---

## 3. For MUTORA-KG: a table-of-contents tree of each book would let seats navigate and cite sections

**Ask:** nothing needed from Alexandre; this is input for the MUTORA-KG agent to weigh.

**What it is about.** MUTORA-KG extracts training science from 66 licensed books into the private research graph (`neo4j-research`, box only) and promotes curated nodes to the app graph. Book seats find passages through qmd search today. The new course's Table of Contents shape is the missing middle layer: Book, Chapter and Section nodes loaded by a plain parser, ordered, with stable URIs.

**What it would give.**

- Seats could walk a book chapter by chapter ("outline, then depth, then one section") instead of searching, which is the course's progressive-disclosure pattern.
- Every curated Principle, Protocol or Exercise could cite a section URI (book/chapter#section) instead of free text, so provenance becomes a traversable edge. This fits the repo's "curated, cited nodes" rule and its per-book Licence nodes.
- The load is deterministic and idempotent, so it obeys MUTORA-KG's "additive MERGE only" rule and costs no LLM tokens.
- Full-text search scoped to one book's URI prefix keeps a seat inside the book it is extracting.

**Limits.** This belongs in `neo4j-research`, never directly in the app graph. The course deferred entity extraction; MUTORA-KG already extracts, so the tree would sit under the extracted nodes as their source, not replace them. Whether qmd's chunks map cleanly to sections has not been checked (inferred).

**Rule to keep.** When a curated node's citation is a free-text string, the cause is usually that the source has no structure in the graph; load the book's outline first and cite its section.

---

## 4. For MUTORA-KG: gap queries, theme detection and current Cypher skills fit work already planned

**Ask:** nothing needed.

**What it is about.** Three smaller patterns from the course map onto gaps MUTORA-KG's own CONTEXT.md already names.

- **Proving a negative.** The course compares two sources to find what is missing. MUTORA-KG's known gaps are of that kind: `evidence_level` on 10 of 122 Principles and Protocols, 0 Equipment-to-Exercise `REQUIRES` edges, Qualities with no grading TestStandard. A small set of saved "what is missing" queries would make those gaps a report rather than a note.
- **Themes with Leiden and conductance.** Running Leiden over Exercise-to-Quality `CAN_DEVELOP` edges (2,363) or over Principle co-citation could show clusters nobody named, and conductance says whether a temple's grouping is real or arbitrary (inferred; not tried). Naming clusters from their most-connected members avoids an LLM. Graph Data Science must be available on the instance; the course used a sandbox that includes it.
- **Neo4j CLI, skill bundles and spec-driven Cypher.** Seats that write Cypher could install the maintained Neo4j skills and work from an output spec, as the course does. The CLI's schema dump also gives a cheap check after each load: list any label or relationship type outside the allowed set.
- **A warehouse semantic layer.** The app's structured data lives in Supabase (Postgres). Neocarta is said to support Postgres, so the coach loop could get a zero-copy map of the Supabase schema beside the knowledge graph (inferred; Postgres support was stated with uncertainty at 0:34:15).

**Rule to keep.** When a gap is known but never shrinks, the cause is usually that nothing measures it; write the "what is missing" query and run it after every load.

---

## 5. For the brain graph: a deterministic outline of videos and documents would answer "which videos cover X"

**Ask:** nothing needed from Alexandre; input for unified-memory (the brain graph is written only by its API; nothing here wrote to any Neo4j).

**What it is about.** The brain graph (`neo4j-brain`, :7688) is built by LLM extraction from each stored memory. The 2026-10-10 report from this repo found that `graph_search` cannot answer "which videos cover GraphRAG" although the data is there, and that extraction leaves stale and duplicate entities. The new course argues for a deterministic skeleton first.

**What the course suggests.**

- **A tree for what is already structured.** Video, section of the video (overview, tools, workflows, takeaways) and the memories under it, loaded from metadata the pipeline already writes, no LLM. "Which videos cover X" becomes a walk from X up to Video, not a hope that extraction linked them. The same goes for `docs/` trees and the wiki, whose paths are already hierarchical URIs.
- **Scoped full-text search.** Memory namespaces are already hierarchical (`/alex/openclaw/videos/`), the same prefix-scoping the course uses for its library.
- **Themes over entity links.** Leiden with conductance over the brain graph's entity links could surface topics across memories that nobody named, and conductance would flag where clusters are noise (inferred).
- **Video titles.** The graph builder titles a Video node from `video_title`, `video_creator`, `video_platform` and `video_url` in memory metadata. The store script did not send them until today; it does now (topic footer). The earlier two Goldcast videos were stored without them and with `channel:unknown-channel`.

**Rule to keep.** When a graph cannot answer a question its data obviously supports, the cause is usually that the link was left to extraction; load the known structure deterministically and extract only what is truly unstructured.

---

## 6. Decide the shape of context the agent needs before choosing the query tool

**Ask:** nothing needed.

**What it is about.** The course's method in one line (0:31:00 to 0:32:58): do not start from "I need RAG, text-to-SQL or Cypher". Start from what the model should see (a table of contents, a set of themes, a map of connections), the way you would design a materialized view, then build it with whatever query fits.

**Rule to keep.** When an agent answers confidently but wrongly from good data, the cause is usually that it got a slice of the data rather than a view of it; design the view, then the tool.

---

<details><summary>Done and working (footer)</summary>

- New video processed end to end: folder `20261015--goldcast-6622e280--local--neo4j--build-your-first-knowledge-layer` (metadata, raw VTT, raw and enhanced transcript, word-checked readable transcript, analysis, summary), copied to the gaming-PC and reconciled into the ledger.
- Stored in unified-memory: 1 note and 30 sections as 36 memories, tagged like the other two (`source:claude-main`, `project:youtube-kb`, `type:video-knowledge`, `area:vecia`, `video:goldcast-6622e280`) plus `project:mutora-kg` and `series:road-to-nodes-2026`, with the four Video-title metadata keys.
- Store script fixed: falls back to the analysis's own title, channel and url and to the folder's `metadata.json`, sends the four Video-title keys, accepts `extra_tags`. VTT converter no longer leaks the `X-TIMESTAMP-MAP` header into transcripts (it had in both earlier Goldcast transcripts).
- Not done: the earlier two videos' memories were not re-stored or retagged; their titles and channel tag remain wrong in memory (their folders and summaries are correct).

</details>
