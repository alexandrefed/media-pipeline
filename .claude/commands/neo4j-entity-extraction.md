# Neo4j Entity Extraction - Knowledge Graph Integration

Add entity extraction to video processing workflows to build a searchable knowledge graph in Neo4j.

## Architecture Overview

| System | Purpose | MCP Tools |
|--------|---------|-----------|
| **unified-memory** | Document chunks + semantic RAG | `ingest_document`, `retrieve_memory`, `store_memory` |
| **Neo4j** | Entity/relationship knowledge graph | `create_entities`, `create_relations`, `search_memories` |

```
Video → Transcript → Analysis → unified-memory (RAG)
                            ↓
                    Entity Extraction (Haiku)
                            ↓
                    Neo4j Knowledge Graph
```

**Why both?**
- **unified-memory**: "Find content about X" (semantic similarity)
- **Neo4j**: "What entities exist? How do they relate?" (structured graph)

## Integration with Existing Workflows

Add this as **Phase 5** after storing in MCP KB Memory:

### For `/process-youtube`

After Phase 4 (Build), add:

```
### Phase 5: Entity Extraction → Neo4j Knowledge Graph

Extract key entities and relationships from the analysis, then store in Neo4j for graph-based querying.
```

### For `/process-sports-video`

Replace the "Neo4j Integration (Future)" section with this working implementation.

## Phase 5 Implementation

### Step 1: Extract Entities with Haiku Agent

Use Claude's Task tool with Haiku for cost-efficient extraction:

```
Task(
  description="Extract entities from video analysis",
  prompt="""Extract key entities and relationships from this video analysis.

VIDEO ANALYSIS:
{paste analysis JSON or summary here}

Return ONLY valid JSON with:
{
  "entities": [
    {
      "name": "Entity Name",
      "type": "person|technology|concept|organization|topic",
      "observations": ["Key fact 1", "Key fact 2", "Usage context"]
    }
  ],
  "relationships": [
    {
      "source": "Entity1",
      "target": "Entity2",
      "relationType": "USES|RELATES_TO|CREATED_BY|PART_OF|BUILDS_ON"
    }
  ]
}

Entity Types:
- person: Named individuals (speakers, researchers, developers)
- technology: Tools, frameworks, languages, libraries
- concept: Abstract ideas, methodologies, patterns
- organization: Companies, institutions, communities
- topic: Subject areas, domains

Relationship Types:
- USES: Technology dependency (Tool A USES Library B)
- RELATES_TO: General association
- CREATED_BY: Attribution (Tool CREATED_BY Person)
- PART_OF: Containment (Feature PART_OF System)
- BUILDS_ON: Conceptual foundation (Concept A BUILDS_ON Concept B)

Focus on:
1. Main technologies and tools mentioned
2. Key people (speakers, creators)
3. Important concepts and methodologies
4. How things connect to each other""",
  model="haiku",
  subagent_type="general-purpose"
)
```

### Step 2: Store Entities in Neo4j

Parse the Haiku response and store entities:

```
mcp__unified-memory__enrichment_create(
  entities=[
    {
      "name": "Claude Code",
      "type": "technology",
      "observations": [
        "CLI tool for AI-assisted coding",
        "Uses MCP for tool integration",
        "Supports subagents for delegation"
      ]
    },
    {
      "name": "MCP",
      "type": "technology",
      "observations": [
        "Model Context Protocol",
        "Enables tool integration",
        "Supports multiple servers"
      ]
    }
  ]
)
```

### Step 3: Store Relationships

```
mcp__unified-memory__enrichment_create(
  relations=[
    {
      "source": "Claude Code",
      "target": "MCP",
      "relationType": "USES"
    },
    {
      "source": "Claude Code",
      "target": "Anthropic",
      "relationType": "CREATED_BY"
    }
  ]
)
```

### Step 4: Verify Storage

```
# Check entities exist
mcp__unified-memory__memory_search(query="Claude Code")

# View all relationships
mcp__unified-memory__graph_search(
  query="MATCH (e)-[r]->(t) RETURN e.name, type(r), t.name LIMIT 20"
)
```

## Entity Type Guidelines

### For Tech/AI Videos (`/process-youtube`)

| Type | Examples |
|------|----------|
| `technology` | Claude Code, MCP, Neo4j, Cursor, VS Code |
| `person` | IndyDevDan, Anthropic team members |
| `concept` | Agentic coding, RAG, prompt engineering |
| `organization` | Anthropic, OpenAI, Microsoft |
| `topic` | AI development, automation, productivity |

### For Sports Videos (`/process-sports-video`)

| Type | Examples |
|------|----------|
| `technology` | Training equipment, apps, devices |
| `person` | Researchers, coaches, athletes mentioned |
| `concept` | Periodization, progressive overload, HIIT |
| `organization` | Research institutions, sports bodies |
| `topic` | Ultra-running, strength training, recovery |

## Querying the Knowledge Graph

### Find Related Technologies

```cypher
MATCH (t:technology)-[r]->(related)
WHERE t.name CONTAINS 'Claude'
RETURN t.name, type(r), related.name
```

### Find All Tools by Creator

```cypher
MATCH (tool)-[:CREATED_BY]->(org:organization)
WHERE org.name = 'Anthropic'
RETURN tool.name, tool.observations
```

### Find Concepts and What Uses Them

```cypher
MATCH (tech)-[:USES]->(concept:concept)
RETURN concept.name, collect(tech.name) as used_by
```

### Combined RAG + Graph Query

```
# 1. Semantic search for relevant content
mcp__unified-memory__memory_search(query="MCP server setup")

# 2. Graph expansion for related entities
mcp__unified-memory__graph_search(
  query="MATCH (e {name: 'MCP'})-[r]-(related) RETURN e, r, related"
)
```

## Cost Efficiency

| Component | Model | Cost |
|-----------|-------|------|
| Entity extraction | Haiku | ~$0.001 per video |
| Neo4j storage | MCP | Free (local) |
| Orchestration | Sonnet/Opus | Main conversation |

Using Haiku for extraction is ~10x cheaper than using Sonnet.

## Example Output

After processing a Claude Code tutorial video:

```
Entities Created:
- Claude Code (technology): CLI for AI coding, MCP integration, subagents
- MCP (technology): Model Context Protocol, tool integration
- Anthropic (organization): Created Claude, AI safety focus
- Agentic Coding (concept): AI-assisted development, autonomous tasks
- IndyDevDan (person): Content creator, Claude Code tutorials

Relationships:
- Claude Code -[USES]-> MCP
- Claude Code -[CREATED_BY]-> Anthropic
- Claude Code -[ENABLES]-> Agentic Coding
- IndyDevDan -[TEACHES]-> Claude Code
```

## Troubleshooting

### Haiku Returns Invalid JSON

- Ensure prompt explicitly says "Return ONLY valid JSON"
- Check for trailing commas or missing quotes
- Parse response and retry if needed

### Entities Not Found After Creation

- Entity names are case-sensitive
- Use `search_memories` with partial name
- Check with Cypher: `MATCH (n) RETURN labels(n), n.name LIMIT 50`

### Duplicate Entities

- Neo4j `create_entities` uses MERGE (no duplicates)
- Observations are appended to existing entities
- Use consistent naming (e.g., "Claude Code" not "claude-code")

## Related Documentation

- `/Users/alex/Desktop/ClaudeMCP/mcp-library/neo4j-memory/` - Neo4j setup and config
- `unified-memory` - Semantic RAG storage
- `neo4j-memory` MCP - Entity/relation operations

---

**Version**: 1.0
**Created**: 2025-12-03
**Architecture**: unified-memory (RAG) + Neo4j (Knowledge Graph)
