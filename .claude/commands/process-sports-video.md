# Process Sports Training Video

Complete automated workflow for processing sports training and exercise science YouTube videos into knowledge base entries with scientific evidence, protocols, and biomechanical analysis.

## Purpose

Process sports/training videos with specialized extraction of:
- Exercise protocols (volume, frequency, intensity)
- Scientific evidence (citations, evidence tiers)
- Biomechanical principles (movement mechanics, muscle activation)
- WHY reasoning (physiological rationale)
- Injury considerations and modifications

## Variables

- `$youtube_url`: YouTube video URL (required)
- `$sport`: Sport discipline (optional: "ultra-running", "hyrox", "strength-training", etc.)
- `$evidence_tier`: Expected evidence quality 1-4 (optional, auto-detected if not provided)

## Workflow Steps

### Step 1: Extract & Auto-Enhance Transcript

```bash
# Extract transcript from YouTube
uv run python main.py extract "$youtube_url"

# This creates:
# - raw_text_for_enhancement_{VIDEO_ID}.txt

# Auto-enhancement with 174+ corrections happens automatically
# Creates: raw_text_for_enhancement_{VIDEO_ID}_auto_enhanced.txt
```

### Step 2: Analyze with Sports-Specific Agent

```
Use @sports-transcript-analyzer to analyze the auto-enhanced transcript at:
workspace/transcripts/enhanced/raw_text_for_enhancement_{VIDEO_ID}_auto_enhanced.txt

Save the JSON output to:
workspace/analysis/{VIDEO_ID}_sports_analysis.json

The agent will extract:
- Exercise protocols with volume/frequency/intensity
- Scientific citations with evidence tiers
- Biomechanical principles with quantification
- WHY reasoning (biomechanical, physiological, tactical)
- Implementation details (setup, execution, common errors)
- Injury considerations and modifications
- Equipment specifications and alternatives
- Progression systems and criteria
```

### Step 3: Generate Sports Summary (LLM-written)

The @media-ingestion-agent writes `summary.md` directly from `analysis_sports.json`. No Python script needed.

The summary adapts the standard structure for sports content:
- Exercise Protocols (sets, reps, intensity, tempo, rest)
- Scientific Evidence & Research Citations
- Biomechanical Principles
- WHY Reasoning
- Programming Logic & Progression
- Equipment Requirements & Alternatives
- Injury Considerations

Output: `workspace/videos/{folder}/summary.md`

### Step 4: Prepare for MCP KB Storage + Auto-Notify

```bash
# Process analysis JSON, prepare MCP-ready content, and automatically sync to n8n
uv run python scripts/store_sports_in_mcp_kb.py workspace/analysis/{VIDEO_ID}_sports_analysis.json

# This creates:
# workspace/mcp_ready/{VIDEO_ID}_sports_mcp_ready.txt
#
# With sport-specific tags:
# - sport-{discipline}
# - evidence-tier-{1-4}
# - content-{type}
#
# AUTOMATICALLY:
# - Calls n8n webhook with video data + sports insights
# - Syncs to VPS PostgreSQL for notifications
# - Sends immediate Telegram notification (🏋️ Sports format)
# - Schedules spaced repetition reminders
# - Enables weekly digest tracking
```

**Automatic Notifications Include**:
- 🏋️ Sports science header
- Executive summary
- Evidence tier classification
- Top 5 key findings
- Protocol details (volume, frequency, intensity)
- WHY reasoning summary
- Link to watch video

**Check Telegram**: You should receive the notification within seconds!

### Step 5: Store in MCP KB Memory

```
Read the MCP-ready content from:
workspace/mcp_ready/{VIDEO_ID}_sports_mcp_ready.txt

Use mcp__unified-memory__memory_store with the content, tags, and namespace provided in the file.

The content will be tagged with:
- youtube-knowledge-base
- video-{VIDEO_ID}
- channel-{channel-name}
- content-type-sports
- sport-{discipline} (e.g., sport-ultra-running, sport-hyrox)
- evidence-tier-{1-4}
- content-{type} (e.g., content-exercise-technique, content-programming-protocol)
```

**Dual Storage Architecture**:
- **Local (MCP KB Memory)**: Primary knowledge storage for instant retrieval
- **VPS (PostgreSQL)**: Secondary storage for notifications & workflows

### Step 6: Clean Up Context (Optional)

```
/compact

Frees up 5-10% of context window for next video processing.
Recommended after successful storage.
```

## Sport Discipline Detection

If `$sport` variable not provided, the workflow will auto-detect from:
- Video title keywords
- Channel name
- Transcript content analysis

**Common Sport Values**:
- `ultra-running` - Ultra marathon training
- `hyrox` - Hyrox competition training
- `strength-training` - General strength/resistance training
- `crossfit` - CrossFit methodology
- `hybrid-athlete` - Concurrent strength + endurance
- `powerlifting` - Powerlifting-specific
- `olympic-lifting` - Olympic weightlifting
- `calisthenics` - Bodyweight training
- `triathlon` - Triathlon training

## Evidence Tier Classification

**Tier 1** (Strongest): Meta-analyses, systematic reviews
**Tier 2** (Strong): Randomized controlled trials (RCTs)
**Tier 3** (Moderate): Case studies, cohort studies, observational
**Tier 4** (Weakest): Expert opinion, anecdotal, consensus

The sports analyzer will auto-classify based on study type mentioned in video.

## Example Usage

### Example 1: Ultra-Running Training Video

```
/process-sports-video youtube_url="https://youtube.com/watch?v=abc123" sport="ultra-running"

# Workflow executes:
# 1. Extract transcript
# 2. Analyze with @sports-transcript-analyzer
# 3. Generate sports summary
# 4. Prepare MCP storage with tags: sport-ultra-running, content-exercise-technique
# 5. Store in KB memory
# 6. Clean context
```

### Example 2: Evidence-Based Strength Training

```
/process-sports-video youtube_url="https://youtube.com/watch?v=xyz789" sport="strength-training" evidence_tier=2

# Expects Tier 2 evidence (RCTs)
# Tags will include: sport-strength-training, evidence-tier-2, content-evidence-based
```

### Example 3: Auto-Detection

```
/process-sports-video youtube_url="https://youtube.com/watch?v=def456"

# Sport and evidence tier auto-detected from content
```

## Output Files

After successful processing, you'll have:

```
workspace/
├── transcripts/
│   ├── raw/
│   │   └── raw_text_for_enhancement_{VIDEO_ID}.txt
│   └── enhanced/
│       └── raw_text_for_enhancement_{VIDEO_ID}_auto_enhanced.txt
├── analysis/
│   └── {VIDEO_ID}_sports_analysis.json
├── summaries/
│   └── {VIDEO_ID}_sports_summary.md
└── mcp_ready/
    └── {VIDEO_ID}_sports_mcp_ready.txt
```

## Quality Checks

Before marking complete, verify:

**✅ Exercise Protocols**:
- [ ] Volume specified (sets x reps)
- [ ] Frequency specified (times per week)
- [ ] Intensity specified (load, RPE, zones)
- [ ] Progression criteria clear

**✅ Scientific Evidence**:
- [ ] Citations include author + year
- [ ] Study type identified
- [ ] Evidence tier assigned
- [ ] Key findings extracted

**✅ Biomechanics**:
- [ ] Movement mechanics explained
- [ ] Quantification provided (degrees, %, force)
- [ ] Muscle activation identified

**✅ WHY Reasoning**:
- [ ] Biomechanical rationale present
- [ ] Physiological rationale present
- [ ] Tactical rationale present

**✅ Implementation**:
- [ ] Setup instructions complete
- [ ] Execution cues actionable
- [ ] Common errors with fixes
- [ ] Safety considerations noted

## Troubleshooting

### Agent Not Found

```bash
# Verify sports agent exists
ls -la .claude/agents/sports-transcript-analyzer.md

# Check Claude Code can see it
# In Claude Code, type: "list agents"
```

### Poor Quality Output

- Ensure transcript is auto-enhanced first
- Check video is actually about sports/training (not AI tools)
- Verify video contains specific protocols (not just general discussion)
- Review agent's quality standards in `.claude/agents/sports-transcript-analyzer.md`

### Missing Evidence Citations

- Some videos don't cite research - this is normal
- Evidence tier will default to 4 (expert opinion)
- Tag will be: evidence-tier-4

### Neo4j Integration (Future)

Analysis JSON includes `neo4j_mapping` section for future graph database integration:
- Exercise nodes
- WhyReasoning nodes (4-tier structure)
- ScientificPaper nodes
- Equipment nodes

This enables direct import to Neo4j knowledge graph when ready.

## Related Commands

- `/process-youtube` - General YouTube processing (AI tools)
- `/scout-papers` - Find scientific papers for exercise
- `/plan-why-nodes` - Design WHY reasoning for Neo4j
- `/compact` - Clean up context after processing

## Success Report

After completion, you should see:

```
✅ Sports Video Processing Complete

Video: {VIDEO_ID}
Channel: {CHANNEL_NAME}
Sport: {SPORT_DISCIPLINE}

Extracted:
- {N} exercises with complete protocols
- {M} scientific citations (Evidence Tier: {TIER})
- {X} biomechanical principles
- WHY reasoning (biomechanical, physiological, tactical)

Stored in MCP KB with tags:
- sport-{discipline}
- evidence-tier-{tier}
- content-{types}

Files created:
- workspace/analysis/{VIDEO_ID}_sports_analysis.json
- workspace/summaries/{VIDEO_ID}_sports_summary.md
- workspace/mcp_ready/{VIDEO_ID}_sports_mcp_ready.txt

Query with:
mcp__unified-memory__memory_search query: "{discipline}" tags: ["sport-{discipline}"]
mcp__unified-memory__memory_search query: "{exercise name} protocol"
```

---

**Version**: 1.0
**Last Updated**: 2025-01-18
**Template**: src/templates/sports_summary_template.md
**Agent**: @sports-transcript-analyzer
