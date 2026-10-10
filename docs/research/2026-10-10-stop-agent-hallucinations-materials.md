# Inventory of the "Stop AI Agent Hallucinations" workshop materials (task 9c9a59b8)

Cover: the materials page has 26 links (25 resources plus the "all talks" back-link); 8 were read in full, 8 skimmed, 8 listed only, 1 is unreachable (the AWS Workshop Studio page, which needs a browser session). Raw copies are in `dev/platform/media-pipeline/workspace/videos/20261008--goldcast-6c25235e--local--neo4j--stop-ai-agent-hallucinations-5-techniques-production-patterns/materials/`. Collected 2026-10-10 by task 9c9a59b8. Nothing here designs storage or skills; the last section only lists what the sources support for the Neo4j brain graph. Anything I inferred is marked "(inferred)".

Workshop: "Stop AI Agent Hallucinations: 5 Techniques + Production Patterns", Road to NODES 2026 (Neo4j), 8 Oct 2026, presenter Elizabeth Fuentes Leone (AWS), with Sandhya Subramani on the deck. Stack: Strands Agents (AWS open-source agent framework), Amazon Bedrock, Neo4j, FAISS, then Amazon Bedrock AgentCore for production. One running example: a hotel-booking agent over 300 hotel FAQ documents.

## How to read the numbers

Three warnings that apply to the whole inventory.

- The workshop's own notebooks have no saved outputs (0 saved outputs across all 9 notebooks in the main repo and all 11 in the second repo), so every result is whatever the READMEs and blog posts say, or what you get by running them. I did not run anything (it needs an AWS account with Bedrock and a Neo4j instance).
- None of the five techniques is measured as a "hallucination rate" on a real test set in this workshop. The numbers are small demos: 4 queries for Graph-RAG, 10 or 13 for tool selection, 2 questions for the consortium, 3 scenarios for the hooks. The only large measurement connected to the techniques is Strands' own steering benchmark (3,000 runs), and it uses a library-book agent, not the hotel demo.
- Several headline numbers in the materials are borrowed or misattributed. Details are in the technique sections: "73% fewer hallucinations" (a health-domain paper, versus GPT-4o with no retrieval), "89% token reduction" (a third-party blog), "86.4% accuracy" (a detector, not a filter).

## The five techniques as the materials name them

The deck, the main repo README and the blog all use this list. Deck wording first, then the repo/blog variants.

1. Graph-RAG (deck: "Compute aggregations in Neo4j instead of guessing from chunks")
2. Semantic tools / semantic tool selection (deck: "Send the top 3 relevant tools per query, not all 31"; the blog calls the production version "semantic tool routing")
3. Multi-agent validation (deck: "Executor, Validator and Critic cross-check before the user sees it"; the current repo actually builds a model consortium, see below)
4. Neurosymbolic guardrails (deck: "Business rules in code, enforced by lifecycle hooks")
5. Agent steering (deck: "Guide the agent to self-correct instead of hard-blocking")

Plus the production material: demo 06 (AgentCore with Lambda, DynamoDB, Gateway) and demo 07 (AgentCore Memory across sessions), covered under "Production patterns" below.

The four failures the deck says it fixes: fabricated statistics, wrong tool selection, business rule violations, undetected failures (an agent claiming success with nobody validating).

## Technique 1: Graph-RAG

What fails: vector RAG returns the top-k similar chunks, so for "how many hotels have a pool?" it answers from about 3 chunks and guesses the total. The repo names three failure modes: fabricated statistics, incomplete retrieval (5 Las Vegas hotels but only 3 chunks retrieved), and out-of-domain fabrication (answering "hotels in Antarctica" from the closest chunks).

The fix: put the facts in a Neo4j graph with a fixed schema and give the agent one tool that runs read-only Cypher written by the model (the README calls this Text2Cypher). The database computes `COUNT`/`AVG`; an empty result comes back as "No results found." and the tool docstring tells the agent not to invent.

How it is implemented:
- Libraries: `neo4j-graphrag` (`SimpleKGPipeline`) to build the graph, the `neo4j` driver to query, FAISS for the vector-RAG comparison agent, Strands `@tool`. Models in the current repo: Claude on Bedrock (`global.anthropic.claude-sonnet-4-6`) for entity extraction, Amazon Nova 2 multimodal embeddings (1024 dimensions) for chunks.
- The graph is hybrid: `Document` and `Chunk` nodes (chunks embedded, chained with `NEXT_CHUNK`) plus structured entities (`Hotel`, `Room`, `Amenity`, `Policy`, `Service`). The README says the anti-hallucination value comes from the structured side, not the chunks.
- The schema is fixed on purpose. The README's reason: with an LLM-discovered schema, "you get junk labels, duplicate relationship types, and inconsistent property types (one room has a numeric `rate`, another a text `priceRange`)". This is their stated rationale, not a measured result.
- After the build, a verification query checks that only allowed labels and relationship types exist and that every `Room` has a numeric `rate`.

Key code, copied from `01-graphrag-demo/build_graph.py` in the main repo (the schema and the pipeline call):

```python
SCHEMA = {
    "node_types": [
        {"label": "Hotel", "properties": [
            {"name": "name", "type": "STRING"}, {"name": "address", "type": "STRING"},
            {"name": "city", "type": "STRING"}, {"name": "country", "type": "STRING"},
            {"name": "guestRating", "type": "FLOAT"}, {"name": "totalRooms", "type": "INTEGER"},
            {"name": "phone", "type": "STRING"}, {"name": "email", "type": "STRING"}]},
        {"label": "Room", "properties": [
            {"name": "type", "type": "STRING"}, {"name": "rate", "type": "FLOAT"},
            {"name": "maxOccupancy", "type": "INTEGER"}]},
        ...
    ],
    "relationship_types": ["HAS_ROOM", "OFFERS_AMENITY", "HAS_POLICY", "PROVIDES_SERVICE"],
    "patterns": [
        ("Hotel", "HAS_ROOM", "Room"), ("Hotel", "OFFERS_AMENITY", "Amenity"),
        ("Hotel", "HAS_POLICY", "Policy"), ("Hotel", "PROVIDES_SERVICE", "Service"),
    ],
}
...
    pipeline = SimpleKGPipeline(
        llm=BedrockLLM(), driver=driver, embedder=BedrockEmbeddings(),
        schema=SCHEMA, from_pdf=False, perform_entity_resolution=True,
    )
```

And the query tool, from `01-graphrag-demo/hotel_tools.py` (read-only routing, empty result stated honestly, 25-row cap, the schema sits in the docstring so the model can write valid Cypher):

```python
records, _, _ = self._driver.execute_query(
    cypher_query, routing_=RoutingControl.READ
)
rows = [dict(r) for r in records[:25]]
if not rows:
    return {"status": "success", "content": [{"text": "No results found."}]}
return {"status": "success", "content": [{"json": {"results": rows}}]}
```

Measured result and on what test:
- The February 2026 blog post "RAG vs GraphRAG" (dev.to, same author) ran 4 tests, one run each, on the 300 hotel FAQ documents: pool count, RAG answered "I don't have the data needed to answer" and Graph-RAG answered 133 hotels (exact Cypher `COUNT()`); Paris average rating, both gave 4.7 (RAG only because it happened to retrieve 2 documents); Antarctica, RAG invented "Research Stations", "Expedition Cruises", "Specialized Lodges" and Graph-RAG answered "No hotels listed in Antarctica"; multi-hop (room types for the best hotel), RAG could not traverse.
- The current main repo states no numbers for demo 01. Its notebook compares the two agents on the same question ("average guest rating of hotels in Las Vegas, and how many hotels did you use?") and prints token counts, but no outputs are saved.
- The second repo's top README says "73% fewer hallucinations with knowledge graphs" for demo 01. Nothing in that repo's demo 01 measures this. The number traces to RAG-KG-IL (arXiv:2503.13514), a health-queries paper: 35 hallucinated statements for RAG-KG-IL, 49 for RAG-only, 129 for GPT-4o over 40 questions (two sets of 20, ten diseases), so "around 73%" is the reduction against GPT-4o with no retrieval (I checked the PDF). Against RAG-only it is 35 versus 49, which is 29% by my arithmetic (inferred from their totals).

Limits the materials state: Graph-RAG is for structured domains and exact questions; "Use RAG for semantic search, unstructured text, fuzzy matching" (February blog post). Extraction costs one LLM call per document (about 20 to 30 seconds each; 30 documents take 10 to 15 minutes, 300 documents about 2 hours). The graph in the demo is read-only.

Backing links: main repo, second repo, the blog, the GraphRAG paper (but see its section: it is about a different thing), Neo4j docs (portal only).

Useful for the brain graph's extraction schema or retrieval: yes, see the last section.

## Technique 2: Semantic tool selection

What fails: with many overlapping tools (the pool is about 40 in the current repo, 31 in the deck, 29 in the older blog post) a small model picks the wrong tool or none, and every tool description is paid for on every call. The repo cites a five-way taxonomy from arXiv:2601.05214: calling non-existent tools, semantically wrong tools, malformed arguments, missing parameters, skipping the tool entirely (the "tool bypass").

The fix: embed every tool's name plus docstring once into a FAISS index; on each request embed the user's message, take the top 3 tools by distance, and replace the agent's live tool registry with those 3 before the model sees them. The agent is created with all tools and keeps its conversation memory.

How it is implemented: a Strands `HookProvider` on `BeforeInvocationEvent`; Nova 2 embeddings; `faiss.IndexFlatL2`; model Claude Haiku so the confusion is visible. From `02-semantic-tools-demo/semantic_tools.py` in the main repo:

```python
    def _trim(self, event: BeforeInvocationEvent) -> None:
        msgs = event.messages or getattr(event.agent, "messages", [])
        query = ""
        for m in reversed(msgs):
            if m.get("role") == "user":
                query = "".join(b.get("text", "") for b in m.get("content", []))
                break
        if not query:
            return
        selected = self.select(query)
        self.last_selected = [t.tool_name for t in selected]
        reg = event.agent.tool_registry
        reg.registry.clear()
        reg.dynamic_tools.clear()
        for t in selected:
            reg.register_tool(t)
```

The pool mixes real tools (Neo4j hotel queries, Open-Meteo weather, a JSON booking store) with about 33 canned stand-ins. The second repo adds two alternatives to FAISS in the same hook: a local 2B "decision model" (`strands-decider`) and the hosted OpenAI Decisions API (described there as public beta, Oct 2026, billed on input tokens only at $0.10 per 1M tokens, model `gpt-6-luna`); I did not verify those claims.

Measured result and on what test:
- Main repo README: about 73% fewer input tokens; the image alt text says about 57k input tokens versus about 15k, "72 percent fewer". The notebook scores 10 queries (for example "Find hotels in Barcelona" expects `search_hotels_by_city`) with all tools versus top-3, and prints accuracy and tokens; no saved output. The README says accuracy is "equal-or-better, shown as observed" and declines to claim a fixed improvement.
- Older blog post (February 2026): 29 tools, 13 queries with ground truth; average tokens per query 1,557 down to 275; "accuracy did not improve much"; perfect accuracy on the 13.
- The "89% token reduction" in the older posts is quoted from a third-party article (rconnect.tech), not measured by the workshop.
- The "up to 86.4% accuracy" line in the older post is described there as semantic selection "detecting and preventing tool selection hallucinations". The paper's abstract says 86.4% is the detection accuracy of its own method (reading the model's internal representations in the same forward pass), which is not the same thing as embedding pre-filtering. The main repo README says as much: that paper "does not evaluate embedding pre-filtering, so none of this demo's numbers come from it".

Limits stated: top-k filtering only helps if the right tool is in the top k; if FAISS misranks it, the agent cannot call it at all. Tune `top_k` and write distinct docstrings. In production the blog replaces the FAISS index with AgentCore Gateway's managed MCP semantic search.

Backing links: main repo (demo 02), second repo (demo 02 plus decision-model notebooks), blog, the Strands Decider post, arXiv:2601.05214 (abstract).

## Technique 3: Multi-agent validation

What fails: a single agent has no second opinion. The older post shows it silently substituting a different hotel when asked for a non-existent one and reporting success.

The fix, as the materials say it, changed between versions.
- Older post (February 2026) and the deck: an Executor, then Validator, then Critic chain built with the Strands `Swarm` (shared context, `max_handoffs=5`). Single-agent test with an invalid hotel: "I've booked the grand_hotel in Paris for Sarah..." (silent substitution). Multi-agent: status FAILED, "Correctly detected the invalid hotel". One scenario, qualitative.
- Current main repo (demo 03): the repo drops the swarm for deterministic data. Its FAQ says "over a deterministic source it's theatre: a Cypher query already returns the truth, and a second agent that queries the same thing just agrees". It builds instead a consortium: the same judgement question goes in parallel to three models from two families (Claude Haiku 4.5, Nova Pro, Nova 2 Lite), answers are canonicalized to the hotel name they mention, clustered, and scored. One cluster means confident; several clusters means likely hallucination. Based on arXiv:2510.19507. A Strands `Graph` (not `Swarm`) is used so the models answer independently and in parallel; a swarm shares context and the agents would copy each other.
- The second repo's top README still lists demo 03 as "Executor-Validator-Critic" while its own demo 03 README describes the consortium. The deck still says Executor, Validator and Critic. So the two public descriptions disagree with the current code.

Key code, copied from `03-multiagent-demo/multiagent_tools.py` (main repo):

```python
    votes = Counter(answers.values())
    n = sum(votes.values()) or 1
    entropy = -sum((c / n) * math.log2(c / n) for c in votes.values())
    entropy /= (math.log2(len(answers)) if len(answers) > 1 else 1)
    return {
        ...
        "clusters": dict(votes),
        "agreement": round(votes.most_common(1)[0][1] / n, 2),
        "entropy": round(entropy, 2),
        "verdict": "CONFIDENT (consensus)" if len(votes) == 1
                   else "LIKELY HALLUCINATION (models disagree, verify)",
    }
```

Measured result and on what test: the README shows two example runs. Grounded question ("single best choice overall for a luxury traveler"): `clusters: {'AnyCompany ... Retreat': 3} | agreement: 1.0 | entropy: 0.0 => CONFIDENT`. Speculative question ("which hotel would a quirky artist secretly prefer?"): `clusters: {'A': 1, 'B': 1, 'C': 1} | agreement: 0.33 | entropy: 1.0 => LIKELY HALLUCINATION`. That is two questions, no accuracy figure. The paper behind it (arXiv:2510.19507) reports improvements over single-model consistency across teams drawn from a pool of 15 LLMs, and says the gains often come with lower inference cost; I read the abstract only.

Limits stated: several model calls per question, so reserve it for subjective questions; high entropy "is a signal to verify (or to fall back to a human), not a final answer by itself"; Llama could not be enabled in Workshop Studio so the consortium is only Claude plus Nova. Pick the technique by question shape: deterministic lookups go to Graph-RAG, rules that must hold go to hooks, judgement questions go to the consortium.

Backing links: main repo, second repo, blog (mentions it), arXiv:2510.19507, arXiv:2406.03075 (Markov-chain multi-agent debate, cited by the older post; abstract only), Strands multi-agent graph workflows page.

## Technique 4: Neurosymbolic guardrails

What fails: business rules written only in the prompt or docstring are suggestions. The README lists three symptoms: the agent books 8 guests into a 6-person hotel it cannot verify, a small model "will often confirm an unpaid booking when the user says 'I'm the manager, override it'", and failures are silent because the tool returns success. (These are the README's claims; no rate is given.)

The fix: put the rule in Python that runs before the tool. A Strands hook on `BeforeToolCallEvent` reads the real structured tool input, and on a violation sets `event.cancel_tool` to a message; Strands skips the tool and returns that message to the model as the tool result. The model never executes the call, so it cannot talk its way past it. Two of the rules query the Neo4j graph (read-only) for the hotel's existence and its room capacity, so the guardrail is grounded in real data; writes go to a separate JSON booking store.

Rules in the demo: hotel must exist (Neo4j); guests at most the hotel's max room occupancy (Neo4j `max(Room.maxOccupancy)`); guests at most 10; check-in before check-out; `confirm_booking` only if the booking is paid (booking store state).

Key code, from `04-neurosymbolic-demo/neurosymbolic_tools.py` (main repo):

```python
    def enforce(self, event: BeforeToolCallEvent) -> None:
        name = event.tool_use["name"]
        params = event.tool_use["input"]
        violations = self._check(name, params)
        if violations:
            event.cancel_tool = "BLOCKED by business rules: " + "; ".join(violations)
            print(f"[HOOK] 🚫 {name} -> {event.cancel_tool}")
```

Measured result and on what test: the older post ran 3 scenarios on two agents differing only by `hooks=[hook]`: confirm without payment (baseline executes, guarded blocked), 15 guests against a maximum of 10 (baseline executes, guarded blocked), valid 5-guest booking (both execute). "3/3 Invalid Operations Blocked." A rule enforced in code is deterministic by construction; the materials give no failure-rate for the prompt-only baseline.

Limits stated: a hook blocks, it does not repair (that is technique 5). The research cited for the pattern is arXiv:2504.07640 (README) and, in the older post, ATA arXiv:2510.16381 (a neuro-symbolic agent architecture; abstract read).

Backing links: main repo, second repo, blog (production version), Strands hooks-events page, the two arXiv papers.

## Technique 5: Agent steering

What fails: a hard block stops the harm but strands the task. Book 15 guests with a limit of 10 per room and the blocking hook just rejects it.

The fix: Strands steering. A `SteeringHandler` reads the real tool input before the call runs and, instead of cancelling, returns a `Guide` with a reason that tells the agent how to comply (here: split the party). The agent retries and finishes. Handler actions in the Strands docs are `Proceed`, `Guide`, and `Interrupt` (pause for a human) before a tool call, and `Proceed` or `Guide` (discard the model response and retry) after a model response; there is also an `LLMSteeringHandler` for rules written in plain language, and a built-in tool ledger that records the calls so far.

Key code, from `05-steering-demo/steering_tools.py` (main repo):

```python
class MaxGuestsSteering(SteeringHandler):
    name = "max-guests"

    async def steer_before_tool(self, *, agent, tool_use, **kwargs) -> ToolSteeringAction:
        if tool_use.get("name") != "book_hotel":
            return Proceed()
        guests = (tool_use.get("input") or {}).get("guests", 1)
        if guests and guests > MAX_PER_ROOM:
            rooms = _split(guests)
            return Guide(
                reason=(
                    f"A room holds at most {MAX_PER_ROOM} guests, but you requested "
                    f"{guests}. Split the party into {len(rooms)} rooms of "
                    f"{rooms} guests and call book_hotel once per room."
                )
            )
        return Proceed()
```

The README says an earlier version of this demo was "broken" (needed an external Agent Control server, forced the model to narrate the guest count so a regex could catch it, hard-coded the 10+5 split) and was rewritten to native steering. The limit can also come from `rules.json` (`{"max_guests_per_room": 10}`) so the rule lives outside code.

Measured result and on what test:
- Workshop demo: 15 guests become two bookings of 10 and 5 ("2 rooms booked ... total guests: 15"). One request.
- The older "Steer, Don't Block" post compared a blocking hook (about 4 s, "BLOCKED, agent asks user to adjust") with Agent Control steering (about 6 s, "Self-corrected, booking completed with 10 guests"). Steering adds latency from the retry.
- The real measurement is Strands' own post "How Steering Hooks Achieved 100% Agent Accuracy Where Prompts and Workflows Failed" (Clare Liguori): a library-book-renewal agent, 6 scenarios, 100 runs each, 5 agent variants, 3,000 runs total, scored with the Strands Evaluation SDK. Pass rates: no instructions 15.7%, simple prompt 82.5%, detailed SOP 99.8%, steering 100.0%, graph workflow 80.8%. Average input tokens: 1,870 / 2,329 / 9,879 / 3,346 / 3,116. Steering used 66% fewer input tokens than the SOP for similar accuracy. The graph workflow failed 98% of the informational-query scenario because the graph only covered renewals. The steering variant also relied on an AgentCore Policy Engine policy for the 30-day limit, not steering alone. This is Amazon's own benchmark on one synthetic agent.

Limits stated: block when the action must not happen at all (unauthorised payment, prohibited operation); steer when the intent is fine and only the shape is wrong. The Strands post adds that steering is complementary to enforcement outside the agent (policy engine at the gateway) and that where steering hooks are not available, "such as off-the-shelf AI assistants", an SOP gets 99.8% at about 3 times the input tokens, and it names "Kiro and Claude Code" as such tools.

Backing links: main repo, second repo, blog, Strands steering docs and the Strands steering benchmark post (both found by search, not linked from the materials page), Strands hooks-events page.

## Production patterns (demos 06 and 07, and the blog)

Hard block versus soft steer versus prompt rule. The blog gives one decision table: hard hook (`event.cancel_tool`) for financial, legal, compliance, "No, the LLM cannot bypass it"; soft steer for capacity limits, date adjustments, preferences ("the agent adapts and completes the task"); prompt rule for workflow order and communication style ("Yes, the LLM may ignore under ambiguous input"). Its lesson 1: mixing hard blocks and soft steers in one mechanism either blocks too much or steers too little.

Rules as data, not code. In production the steering rules live in a DynamoDB table, one row per rule, with a `fail_message` and a `steer_message`. A `validate_booking_rules` tool reads the rows before every booking action and returns PASS or `FAIL ... STEER: ...`. From the blog:

```json
{
    "rule_id": "max-guests",
    "action": "book",
    "condition_field": "guests",
    "operator": "gt",
    "threshold": 10,
    "fail_message": "Guest count exceeds maximum of 10",
    "steer_message": "Booking for 15 guests is not available, but you CAN book for up to 10. Adjust to 10 guests, proceed, and tell the user.",
    "enabled": true
}
```

Six default rules: max-guests, valid-dates, advance-booking, payment-before-confirm, cancellation-window (48 hours), already-cancelled. Changing a threshold is one `aws dynamodb update-item`, no redeploy. The system prompt tells the agent to call the validator before book/confirm/cancel (`SYSTEM_PROMPT` in `06-agentcore-boto3-demo/booking_agent.py`), so the soft layer still depends on the model calling the validator; the hard hook (`BookingGuardrailsHook`) covers payment-before-confirm independently.

Other production lessons from the blog (its list of 5): deploy stacks independently; test locally against the same data; keep tools as pure create/read/update/delete and put all business rules in the guardrail layers.

Tool routing: AgentCore Gateway exposes the Lambda tools over MCP and does semantic routing, replacing the FAISS index; the agent calls `list_tools_sync()` at start-up and has no hard-coded tool list.

Measured: Lambda tool latency over 10 consecutive invocations per function, from CloudWatch REPORT lines (blog). `validate_booking_rules`: cold start about 550 to 620 ms, warm median about 25 ms, warm p90 about 105 ms. `query_knowledge_graph` on Neo4j AuraDB Free: cold about 1.9 to 2.0 s, warm median about 13 ms, p90 about 75 ms. Ten invocations is a small sample.

Demo 07 (AgentCore Memory, main repo only): two memory strategies (`UserPreferences`, `UserFacts`), retrieval config `top_k=3, relevance_score=0.5` per namespace (`/users/{actor_id}/facts`, `/users/{actor_id}/preferences`), extraction is asynchronous (the notebook waits 60 s between session A and session B), actor id scopes the memory. This is AWS's managed memory, not Neo4j.

Observability: add `strands-agents[otel]` and `aws-opentelemetry-distro` and AgentCore traces tool calls and guardrail blocks in CloudWatch (blog).

## Tier A links

### 1. Presentation deck (events.elifuentes.tech/decks/deck-stop-agent-hallucinations-workshop.pdf)

Read in full (15 pages, 10 KB of text). It is a short slide deck titled "Stop AI Agent Hallucinations With Code, Not Prompts", presenters Elizabeth Fuentes Leone and Sandhya Subramani, PDF created 2026-10-03. Content: the four failures, the five fixes, seven hands-on modules (Graph-RAG vs RAG, semantic tool selection, multi-agent validation, neurosymbolic guardrails, agent steering, production on AgentCore, AgentCore Memory), a Strands overview, a six-line Strands agent example, AgentCore service list (Runtime, Memory, Gateway, Identity, Observability, Code Interpreter, Browser), account sign-in steps (a bit.ly link and a one-time password), and a resources link. No results, no numbers except "top 3 ... not all 31". Quality: marketing-level; it lags the repo (31 tools versus about 40, Executor/Validator/Critic versus consortium). Licence: copyright AWS 2026, no open licence stated.

### 2. aws-samples/sample-stop-ai-agent-hallucinations-workshop (main workshop repo)

Read in full: top README, 9 demo READMEs, 9 notebooks (markdown and code cells), 11 key `.py`/`.json` files. Commit `fe35610d6b6b9375c3e6f195920630ca2592c5b9`, 2026-10-08 05:24 -0700. Licence MIT-0 (AWS sample, no attribution needed). README stamps: Strands Agents 1.58, "Last updated: October 2026".

Modules: 00 getting started (agent, `@tool`, token metrics from `AgentResult.metrics.accumulated_usage`, `BeforeToolCallEvent` hook, `Swarm`); 01 Graph-RAG vs RAG; 02 semantic tool selection; 03 multi-agent validation (consortium); 04 neurosymbolic guardrails; 05 steering (native Strands steering); 06 AgentCore with boto3 notebook (8 Lambdas, 3 DynamoDB tables, Gateway, Runtime, no CDK); 07 AgentCore Memory; 08 cleanup. Defaults: Amazon Bedrock Claude, no external API key. Needs an AWS account with Bedrock model access and a Neo4j with APOC; in Workshop Studio the graph is restored from a dump. Strengths: coherent, honest about trade-offs (it says what does not work), real tools rather than mocks, fixed-schema graph build with a verification step. Weaknesses: notebooks ship without outputs, so no measured results are in the repo, and nothing here is a benchmark.

### 3. elizabethfuentes12/why-agents-fail-sample-for-amazon-agentcore (second repo)

Read in full with the same treatment (top README, demo READMEs, 11 notebooks, 8 key code files). Commit `cf44bd866dfbb7bb97b80c1a5c797c37392ce1d9`, 2026-10-08 05:06 -0700, so 18 minutes older than the main repo. Licence MIT-0.

How it differs from the main repo:
- It is the author's personal repo and the one the dev.to production blog points to; the main repo is the AWS-samples workshop version with a more complete flow.
- Demos 01 to 05 are the same code (the Python files I diffed for demos 01, 04 and 05 are identical); the READMEs differ only in punctuation and small edits. It lacks the main repo's demo 00 (primer), 07 (AgentCore Memory) and 08 (cleanup).
- Demo 02 has extra notebooks and scripts for decision-model tool selection: `strands-decider` (a local 2B model), "Jev" (hosted), and the OpenAI Decisions API, plus `tool_selection_decision.ipynb`, `model_routing_decision.ipynb`, `openai_decisions_demo.ipynb`.
- Demo 06 exists twice: a boto3 notebook version (as in the main repo) and a CDK version (`06-agentcore-production-demo`) with two independent stacks, a graph-builder Lambda, S3 and Step Functions for the 300-document build, which is what the blog describes. The main repo has no CDK.
- Its top README still says the default model is OpenAI GPT-4o-mini with an `OPENAI_API_KEY`; the demo READMEs and the main repo use Bedrock. Its Strands badge says 1.27+ (March 2026).
- The CDK graph-builder Lambda (`06-agentcore-production-demo/lambda_tools/build_graph/lambda_function.py`) calls `SimpleKGPipeline(... perform_entity_resolution=True)` with no `schema=` and its docstring says "to auto-discover schema". That is the opposite of the fixed-schema build in the main repo's demo 01, and the main repo README argues against it.
- It commits some run artefacts (`bookings.json`, `bookings_try.json`, `bookings_blocked.json`).
- Its top README claims "73% fewer hallucinations with knowledge graphs" (see technique 1: borrowed from another paper).

### 4. dev.to blog "5 Techniques to Stop AI Agent Hallucinations in Production"

Read in full (31 KB, published 2026-03-30, author Elizabeth Fuentes Leone, org aws). The last post of a six-part series. Covers the production hotel-booking stack: two CDK stacks (agent, GraphRAG), 6 DynamoDB steering rules, hard hooks versus soft steers, AgentCore Gateway semantic routing, GraphRAG on Neo4j AuraDB Free via `SimpleKGPipeline` (30 documents "lite" in about 15 minutes, 300 documents "full" in about 1 to 2 hours with Step Functions), a 7-scenario test notebook, Lambda latency table, five lessons, FAQ, and four cited papers (RAG-KG-IL, Internal Representations, Teaming LLMs, MetaRAG). Quality: practical and concrete; the blog's agent uses OpenAI GPT-4o-mini via Strands, while the workshop repo uses Bedrock. "Production" here means a demo deployment, not a load test. No licence stated on the post (the code is MIT-0).

The raw copy `blog.md` also contains, as appendices, the five earlier series posts (full text from the dev.to API: "RAG vs GraphRAG", "Reduce Agent Errors and Token Costs with Semantic Tool Selection", "AI Agent Guardrails: Rules That LLMs Cannot Bypass", "Runtime Guardrails for AI Agents - Steer, Don't Block", "How to Stop AI Agents from Hallucinating Silently with Multi-Agent Validation", plus the February overview "4 Essential Techniques") and the abstracts of the 8 papers they cite. The links to the series inside the blog use older slugs that do not all resolve; I found the posts by article id.

### 5. arXiv:2404.16130 "From Local to Global: A Graph RAG Approach to Query-Focused Summarization" (Microsoft Research, Edge et al.)

Read: abstract plus the method (3.1) and evaluation (4, 5, 6.1) sections of the PDF, v2 dated 2025-02-19 (first submitted 2024-04-24). It is the paper behind Microsoft's `graphrag` library, not a hallucination paper.

- Method: split documents into 600-token chunks (100 overlap); an LLM extracts entities, relationships and optional claims, each with a short description, using prompts that can be tailored with few-shot examples for the domain; duplicates become nodes and edges (the number of duplicate relationships becomes edge weight); Leiden community detection builds a hierarchy of communities (C0 root down to C3 leaf); an LLM writes a report-like summary per community bottom-up; at query time each community summary produces a partial answer in parallel (map) and the partial answers are combined into one (reduce).
- Entity matching: "our analysis uses exact string matching for entity matching ... However, softer matching approaches can be used ... GraphRAG is generally resilient to duplicate entities since duplicates are typically clustered together for summarization in subsequent steps."
- Evaluation: two corpora of about 1 million tokens (podcast transcripts: 1,669 chunks; news articles: 3,197 chunks), 125 LLM-generated sensemaking questions per comparison, 5 runs each, an LLM judge on comprehensiveness, diversity, empowerment and directness, against vector RAG ("SS") and a text-summarization baseline. Graph sizes: 8,564 nodes and 20,691 edges (podcast), 15,754 nodes and 19,520 edges (news). Indexing the podcast took 281 minutes on gpt-4-turbo.
- Results: GraphRAG beat vector RAG on comprehensiveness (72 to 83% win rate on podcasts, 72 to 80% on news) and diversity (75 to 82% and 62 to 71%); vector RAG won on directness; empowerment was mixed. Root-level summaries needed 97% or more fewer tokens than summarizing source texts. A claim-count check (47,075 unique claims) agreed with the LLM judge in 78% of non-tie comparisons for comprehensiveness.
- What it does not do: it does not measure hallucination or fabrication; section 6.1 says comparing fabrication rates "would also strengthen the current analysis". It answers "what are the main themes of the whole corpus", which is a different job from the workshop's exact aggregation over a structured graph. The workshop cites it as general backing for Graph-RAG; its method (community summaries) is not what the workshop builds (Text2Cypher over a typed graph).
- Licence: arXiv non-exclusive licence; the code is open source at github.com/microsoft/graphrag (MIT per the GitHub API).

### 6. AWS Workshop Studio (catalog.us-east-1.prod.workshops.aws/workshops/da54c705-...)

Unreachable. The URL returns a 923-byte JavaScript shell titled "Workshop Studio" with no content; six path variants return the same shell; `tavily extract` failed; `fcrawl` failed with "Insufficient credits". Visible: nothing beyond the title. The materials page describes it as "AWS Workshop Studio version with Event Engine accounts for independent learning". The deck and the main repo README say the live version is entered with an emailed one-time password. Inference (not stated): its content is the main repo's modules 00 to 08. Raw note in `workshop-studio.md`. No sign-in was attempted.

### 7. Neo4j Agent Memory (neo4j.com/labs/agent-memory/ and github.com/neo4j-labs/agent-memory)

Read the landing page plus the repo's README, the POLE+O model page, the entity resolution page, the ontology-driven extraction how-to, the multi-agent sharing page, the adopt-an-existing-graph page, backend capabilities and the changelog. Commit `4866fdc917f61899efcfd7fdebe459cbc2a02450`, 2026-10-07. Licence Apache-2.0. Maturity: Neo4j Labs, status Beta, "actively maintained, but not officially supported. There are no SLAs or guarantees around backwards compatibility and deprecation." Python 0.7.0 (released 2026-10-07; the same day as the commit) and TypeScript 0.5.0 are separate packages. GitHub: 585 stars, 103 open issues, created 2026-01-06, last push 2026-10-09.

What it is: a graph memory layer for agents with three memory types in one Neo4j graph. Short-term: `Conversation` and `Message` nodes (chained, searchable by text and vector). Long-term: `Entity` nodes classified with the POLE+O model (Person, Object, Location, Event, Organization, with subtypes) plus preferences and facts on the direct-database backend. Reasoning: `ReasoningTrace`, `ReasoningStep`, `ToolCall`, `Tool` nodes that record what the application supplies (it "does not expose a model's hidden reasoning").

Data model, as the docs state it: a managed entity carries the `:Entity` label and `type`/`subtype` properties, with labels added for type and known subtypes (for example `:Entity:Object:Vehicle`); `:Message` points to entities with `:MENTIONS`; extracted relations can be stored as `:RELATED_TO` with a property naming the relation ("Do not assume that a conceptual employment relation is always stored as a physical `:WORKS_AT` edge"); `INITIATED_BY`, `USES_TOOL`, `INSTANCE_OF` link reasoning to messages and tools; pending duplicates get `:SAME_AS` edges; audit edges are `:TOUCHED`. By default the library MERGEs entities on `(:Entity {name, type})`.

How an agent writes and reads: Python `MemoryClient` (`short_term.add_message`, `long_term.add_entity`, `get_context`), two backends (a hosted service called NAMS, or Bolt straight to your own Neo4j/Aura), a self-hosted MCP server (`uvx --from 'neo4j-agent-memory[mcp,openai]==0.7.0' neo4j-agent-memory mcp serve --backend bolt`, with a documented `claude mcp add` command; 16 tools on the Bolt profile, 20 on NAMS), and integrations for LangChain, Pydantic AI, Google ADK, Strands, CrewAI. Extraction on Bolt can use spaCy, GLiNER2.5 (a 407 MB local checkpoint that decodes entities and typed relations in one pass), or an LLM. Providers: native adapters for OpenAI, Anthropic, Bedrock, Vertex, sentence-transformers, and LiteLLM for the rest.

Schema constraint: you write an ontology (YAML or JSON) with `entity_types` (label, `pole_type`, `subtype`, description, optional aliases and threshold), and `relationships` (type, source, target, description, `unique_source`, `acyclic`, `inverse`). The docs say the description acts as an annotation guideline: write the positive case, then "rule things out" with negative cases ("Not the support engineer who answers"). Relationship endpoint types are enforced during decoding, not filtered afterwards, and relations the ontology does not permit are dropped on ingest. There is a CLI check (`neo4j-agent-memory ontology validate ontology.yaml`).

Duplicates (the page "Entity resolution and deduplication"): since 0.7.0 message ingestion resolves mentions on ingest by default (before that, "ingestion stored one node per distinct surface form"). Five stages: normalize the name (organisations lose legal suffixes), block candidates in Cypher (never across POLE+O types), score (exact normalized match and declared aliases score 1.0, acronym expansion 0.97 for organisations, otherwise 0.45 fuzzy + 0.40 embedding + 0.15 context), band (merge at or above 0.90 by default, a pending `:SAME_AS` edge between 0.85 and 0.90, otherwise create), and cluster unmatched mentions against each other. A whole-token prefix ("Apple" versus "Apple Bank") only merges if surrounding context agrees. A cross-typed duplicate (one company extracted as both Organization and Object) is never found; the docs say to fix the typing with a sharper ontology description rather than loosen the blocking. "Resolution is an enhancement, never a gate": if a blocking query fails, mentions are stored unresolved. The docs say thresholds should be chosen with labelled matches and non-matches from your own data.

Sharing between agents: several agents can use the same workspace or database; entities are shared across conversations; conversation ids organise records but "do not enforce access control"; "Resolution and deduplication help identify candidates, but they do not substitute for a concurrency policy"; decide who owns an update and keep source evidence. Also on the direct-database backend: `client.schema.adopt_existing_graph(...)` to layer the library on an existing Neo4j graph (limitation stated: automatic extraction does not link to adopted nodes by default, because a mention typed `OBJECT` creates a second node), `client.consolidation.dedupe_entities(...)`, a buffered-writes API, and `client.eval.run(suite)` plus a `benchmarks/` folder (not read in depth).

Quality: the most careful of the Neo4j materials; the docs state their own limits openly. Caveat: fast-moving (0.7.0 changed ingestion behaviour), Labs-level support, many open issues.

### 8. create-context-graph (github.com/neo4j-labs/create-context-graph)

Read the README, roadmap, the explanation docs (why context graphs, three memory types, decision traces, ontology YAML, memory backends, edge encoding), the Claude Code schema reference and the changelog. Commit `926e3b3e7a2d3318f94e8a2cc5196677046bbe6d`, 2026-10-09. Licence Apache-2.0. Maturity: "an experimental Neo4j Labs project and not part of Neo4j's supported product lineup". 732 stars, 11 open issues, 11 contributors listed, created 2026-03-22, last push 2026-10-09. The roadmap file is dated 2026-03-22 and describes the build as finished in 6 phases.

What it is: a scaffolding CLI (`uvx create-context-graph`) that generates a full-stack demo application for one of 27 industry domains (or a custom domain described in plain English): FastAPI backend with an agent in one of 8 frameworks (PydanticAI, Claude Agent SDK, OpenAI Agents SDK, LangGraph, CrewAI, Strands, Google ADK, Anthropic Tools), a Next.js chat plus graph-visualisation front end, a Neo4j schema, synthetic documents and decision traces, and SaaS importers (GitHub, Slack, Gmail, Jira, Notion, Calendar, Salesforce, Linear, Google Workspace, Claude Code, Claude AI, ChatGPT, local files). Memory is delegated to `neo4j-agent-memory` (its README says "v0.4", the current release is 0.7.0, so the README is stale on that point). The workshop page describes it as a "tool for building knowledge graphs from unstructured data (used in Graph-RAG demo)"; I searched both workshop repos and found no reference to it, so that description does not match the repos (the graph there is built with `neo4j-graphrag`).

Data model: each domain is one YAML ontology (`inherits: _base` for POLE+O, `entity_types` with label/`pole_type`/subtype/properties, `relationships`, agent tools, system prompt). On the hosted backend a documented workaround encodes relationships as `ccg-edges` YAML blocks inside an entity's `description`, because that service had no "add relationship" call at the time.

Parts that touch our setup: the Claude Code connector reads `~/.claude/projects/` session files with no API key and builds `Project`, `Session`, `Message`, `ToolCall`, `File`, `GitBranch`, `Error`, `Decision`, `Alternative`, `Preference` nodes with relationships such as `HAS_SESSION`, `NEXT`, `USED_TOOL`, `MODIFIED_FILE`, `READ_FILE`, `ENCOUNTERED_ERROR`, `MADE_DECISION`, `CHOSE`, `REJECTED`, `EXPRESSES_PREFERENCE`. Decisions are found by heuristics and carry a 0.0 to 1.0 confidence and a category (correction, architecture, error-fix, dependency); the docs call the confidence model "Heuristic". Duplicate handling is whatever `neo4j-agent-memory` does; this repo adds nothing of its own beyond its docs.

Quality: a code generator and showcase, not a library you embed; useful mainly as a source of ontology examples and the Claude Code session schema.

### 9. Strands Agents documentation (strandsagents.com/docs/)

Read only the pages the workshop uses. The `/docs/` root is a portal and returned a 470-byte shell; I read: the hooks-events reference (the event lifecycle: `BeforeInvocationEvent`, `BeforeModelCallEvent`, `AfterModelCallEvent`, `BeforeToolsEvent`, `BeforeToolCallEvent`, `AfterToolCallEvent`, `AfterToolsEvent`, `AfterInvocationEvent`, `MessageAddedEvent`), the multi-agent graph workflows lesson (Graph: each node a full agent, edges dependencies, parallel where possible; Swarm is in a sibling page I did not read), the Strands Decider 2B post (a 2-billion-parameter open model that picks between options with calibrated scores, median about 115 ms on an RTX 3090 and about 153 ms on an M3 laptop, as the post reports), and two pages found by search: the steering docs and the steering benchmark post (covered in technique 5). I did not read the custom-tools, metrics, model-providers or Swarm pages the repos link to. Strands Agents SDK for Python is Apache-2.0 (GitHub API). Quality: clear reference docs; the Strands blog benchmarks are the vendor's own.

## Tier B (portals, skimmed)

| Link | What it is | Note |
|---|---|---|
| neo4j.com/docs/ | Neo4j documentation landing page | Portal. The workshop uses it for Cypher and the `neo4j-graphrag` Python docs (linked from the blog). Nothing workshop-specific. |
| neo4j.com/blog/ | Neo4j engineering blog | Portal, 286 KB front page of general posts. Nothing specific to this workshop. |
| neo4j.com/developer/ | Developer centre | Guides, drivers (Python, Java, JavaScript, C#), "new to graph? start here". Portal. |
| github.com/neo4j-graphacademy | GraphAcademy GitHub organisation | Free self-paced Neo4j training; 47 repositories per the page. Portal. |
| deeplearning.ai/courses/knowledge-graphs-rag | "Knowledge Graphs for RAG" course | Intermediate, 2 h 4 min, 9 video lessons and 6 code examples, instructor Andreas Kollegger (Neo4j), updated 2025-10-07, free to enrol; the graded assignment is on the paid PRO tier. |
| neo4j.com/startup-program/ | Neo4j startup programme | "Up to $16K in Aura credits". Commercial, not technical. |
| repost.aws/knowledge-center/add-aws-promotional-code | AWS re:Post how-to | Explains where to enter a promotional code in the Billing console. I read the text only and did not redeem anything. Plain curl gets HTTP 403; text came via `tavily extract`. |
| elifuentes.tech | Presenter's site | Developer advocate at AWS, speaker, newsletter "Tech & AI Weekly by Eli". Personal portal. |

## Tier C (listed only, not opened, nothing submitted)

| Link | What it is |
|---|---|
| linkedin.com/in/lizfue/ | Presenter's LinkedIn profile |
| github.com/elizabethfuentes12 | Presenter's GitHub profile (the second repo lives here) |
| dev.to/elizabethfuentes12 | Presenter's dev.to profile (I used the dev.to public API for the series posts, not this page) |
| instagram.com/elifue.tech | Presenter's Instagram |
| twitter.com/ElizabethFue12 | Presenter's Twitter/X |
| youtube.com/channel/UCr0Gnc-t30m4xyrvsQpNp2Q | Presenter's YouTube channel |
| pulse.amazon/survey/M0S32FQB | Workshop feedback survey. Not opened, nothing filled in. |
| pulse.amazon/promotion/ZLLECZFL | AWS promotional credit link ("Do this first" on the page). Not opened, nothing redeemed. |

## Further sources read (not on the materials page)

- The six dev.to series posts by the same author (appendix of `blog.md`). They are the earlier, fuller write-ups of each technique and the source of the older numbers above.
- Eight papers cited by the blog and repos, abstracts only, via the arXiv API: 2503.13514 RAG-KG-IL, 2601.05214 Internal Representations in tool selection, 2510.19507 Teaming LLMs (consortium consistency), 2509.09360 MetaRAG, 2504.07640 neuro-symbolic integration with ontological reasoning, 2504.09823 RAKG (document-level knowledge-graph construction; reports 95.91% accuracy on its MINE dataset versus 89.71% for GraphRAG), 2406.03075 Markov-chain multi-agent debate, 2510.16381 ATA. Only RAG-KG-IL's results section was read beyond the abstract (to check the 73%).
- Same-author posts I saw in her dev.to list and did not use: "Graph Memory: When Vector Search Fails" (2026-08-27), "How to Stop RAG Hallucinations Poisoning Your Vector Store" (2026-07-10), "Stop AI Agent Hallucinations: Validate Before the Agent Writes to Memory" (2026-06-24). I fetched them into the scratchpad but did not read them; their titles suggest they are relevant to agent memory (inferred from titles only), worth a look if the brain-graph work needs write-time validation.

## What this means for our Neo4j memory graph

Only points the sources back. Our situation as briefed: the brain graph answered 0 of 10 test questions; causes named were duplicate entities, a graph split per writing agent, and free-form extraction; a duplicate merge has landed; schema-constrained extraction is next; retrieval gets re-measured on the same ten questions.

1. Fixed schema is the workshop's own answer to the free-form extraction problem, with the same symptoms. The main repo passes `schema=` to `SimpleKGPipeline` (typed node labels with typed properties, a list of relationship types, and a list of allowed `(source, relation, target)` patterns) and gives its reason: without it the model invents labels, duplicate relationship types and inconsistent property types. It is a stated rationale; the repo contains no before/after measurement. The same author's CDK production Lambda builds with no schema, so the materials are not consistent with themselves. The repo's `schema` has no per-type descriptions; the descriptions-plus-negative-cases approach comes from agent-memory's ontology format (below).
2. A post-build check is cheap and concrete. `build_graph.py` runs a query after the build that lists labels and relationship types, flags any outside the allowed set, and flags rooms with a missing numeric `rate`. That is a ready-made pattern for checking any extraction run against its schema.
3. Schema with descriptions and endpoint rules is what agent-memory offers beyond the workshop. Its ontology has a description per entity type that works like an annotation guideline, with negative cases, and relationship types with source and target types enforced while decoding; relations outside the ontology are dropped. That matches "fixed entity and relation types with descriptions, and patterns". Costs: a 407 MB local extractor checkpoint or an LLM extractor, Labs-level support, and a version (0.7.0) that changed ingestion behaviour a few days ago.
4. On duplicates, agent-memory gives the most detailed published design and the warnings are useful whichever tool we use. Resolve against existing entities at write time; never block across entity types (so a wrong type creates a duplicate nobody finds, and the fix is a sharper type description); use a middle "review" band with pending `SAME_AS` edges instead of a binary merge; treat a false merge as at least as costly as a missed one; pick thresholds from labelled pairs of our own data (the docs' 0.90 and 0.85 are defaults, not tuned values for us). The GraphRAG paper takes the opposite stance for its use: exact string matching, tolerating duplicates because duplicates cluster together at summary time; that only holds for its summarisation approach, not for exact lookup.
5. Against "one node per name, one shared graph, schema-constrained": agent-memory's default key is `(name, type)`, so the same name under two types is two nodes by design. It allows several agents on one database with shared entities, but says explicitly that conversation ids do not isolate agents, that concurrent writers are not guaranteed to merge correctly, and that a write-ownership and provenance policy is the application's job. Its `adopt_existing_graph` can layer onto an existing graph; the documented limit is that automatic extraction will not link to adopted nodes unless the label mapping preserves the type. create-context-graph adds no resolution of its own.
6. Retrieval grounded in the graph reduces fabricated answers only for structured, exact questions. The workshop's Text2Cypher tool (schema inside the tool description, read-only routing, "No results found." returned as a plain answer, 25-row cap) fixed fabricated counts and out-of-domain answers in the 4-test demo; the older post itself says to use plain RAG for semantic or fuzzy questions. If some of our ten questions are semantic or "why" questions, the workshop gives no evidence that the graph path helps them (inferred from the scope of its tests).
7. Re-measuring: the workshop's tests are too small to copy as a method (4 queries, 10 queries). The GraphRAG paper's method (125 questions per comparison, 5 runs each, LLM judge) is for open-ended summary questions, not for exact lookup. agent-memory ships an evaluation harness and a `benchmarks/` folder for extractors (not read in depth). For exact questions the workshop pattern is simply: ground truth from the data, then compare each approach's answer with it.
8. Checking an agent's answer against a curated graph (Mutora/Flectora): the material demonstrates checking tool inputs, not free-text answers. The guardrail hook in demo 04 queries a read-only graph (parameterised Cypher) for "does this hotel exist" and "what is its capacity" before a tool runs and blocks on a mismatch. For free text, the closest published method in the materials is MetaRAG (arXiv:2509.09360, abstract only): split an answer into atomic factoids and verify each against the retrieved context. The consortium (technique 3) measures agreement between models, not truth, and the README says so ("a signal to verify").
9. Mapping to Claude Code hooks: the materials never mention Claude Code hooks; the only mention of Claude Code is the Strands benchmark post saying steering hooks are not available in "off-the-shelf" tools like Claude Code and Kiro, so use an SOP there (99.8% in their test). My own reading (inferred, not from a source): `BeforeToolCallEvent` with `cancel_tool` is the same shape as a tool-call hook that can deny with a message, and the steering "Guide" is the same shape as a denial whose message tells the model what to do instead. The workshop's hard-versus-soft table and its "rules as data, not code" lesson (rules in a table you can change without redeploying) are portable ideas regardless of framework; the blog says LangGraph, AutoGen and CrewAI have similar extension points.
10. Candidate tools, what each is: agent-memory is a library and MCP server that stores conversation, entities (with its own resolution) and reasoning traces in one Neo4j graph, Beta, Apache-2.0, last release 2026-10-07. create-context-graph is a generator of demo apps that happens to include a Claude Code session importer and an ontology format, experimental. Neither is in the workshop's own demos.
11. Production caution from the materials: AWS-side tools in the workshop (AgentCore Memory with 60 s asynchronous extraction, Lambda cold starts around 0.6 to 2 s, Neo4j AuraDB Free at 200,000 nodes per the blog) are small-demo numbers on one example; the blog's "production" is a deployed demo.

## Decision models: Jev, Strands Decider and Laya compared (added 2026-10-10 by the media-pipeline session)

All three are "System One" decision models: they return a choice or a score with a calibrated probability, never free text. In the workshop the speaker demos Jev and names one open model; Alexandre added Laya for comparison. Sources: typesafe.ai/blog/introducing-system-one-models-and-jev (15 Sep 2026), github.com/strands-labs/strands-decider README (read 2026-10-10), huggingface.co/convaiinnovations/laya model card (read 2026-10-10).

| | Jev (TypeSafe AI) | Strands Decider (Strands Labs, AWS) | Laya (Convai Innovations) |
|---|---|---|---|
| Access | Hosted API, early access; the speaker reached it through OpenRouter | Open weights, Apache-2.0, Hugging Face `StrandsAgents/strands-decider-*`, `pip install strands-decider` | Open weights, Apache-2.0, Hugging Face `convaiinnovations/laya`, `pip install laya` |
| Size | Not published | 2B (Qwen3.5-2B-Base torso); an E4B Gemma 4 variant too | 421M (ModernBERT-large); multilingual checkpoint 322M (mmBERT-base) |
| Speed (vendor figures) | 70 to 500 ms end to end | Not measured here (a secondary article quotes about 106 to 115 ms on an RTX 3090) | About 33 ms per forward pass |
| Training | RLCD (TypeSafe's name) | Trained on rows from 25 public Hugging Face datasets; full retraining recipe published (about 11 h on one RTX 3090) | Card says RLCD against proper scoring rules; fine-tuning notebook on Kaggle's free 2x T4; the card does not say its training data is published |
| Calibration claim | Calibrated probabilities on every output | Confidence 0.9 or more right about 95% of the time on unseen short tasks (its own evaluation) | "Mathematically calibrated"; publishes a chart against Jev |
| Languages, context | Not stated in the post | Text, optional vision | 100+ languages; 512 tokens (English), up to 8,192 (multilingual) |
| Cost | $0.042 per million input tokens, output free | Free, local hardware | Free, local hardware |

Which one the speaker meant by the open local model: the captions say "strong decider model, completely open source, you can go to [Hugging Face] and download this model" (0:43:26) and "this new strand design model … they share all the data … the team used to train this model, so you can use that data to [retrain]" (0:47:08), and she says her travel laptop lacks the RAM to run it. "Strand design" / "strong decider" is Strands Decider, a 2B model from the framework she presents, whose training data is published. Laya fits "open, local, fine-tunable" but not the name, and at 421M the RAM remark fits it less. So the video's analysis names Strands Decider; Laya stays here as the comparison, not as something the speaker said.

For our fleet: dnd-solo already uses Jev as its retrieval classifier (memory d0f37a6e). For a local, no-data-leaves-the-box option, Laya is the lighter one (fits the gaming-PC beside the other models), Strands Decider the one with the reproducible training data. Neither has been measured on our data.
