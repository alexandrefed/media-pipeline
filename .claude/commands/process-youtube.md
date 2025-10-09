# Process YouTube Video - Complete End-to-End Workflow

**Purpose**: Process a YouTube video from URL to MCP KB Memory storage using the Scout-Plan-Build pattern inspired by agentic coding best practices.

**Pattern**: This command implements prompt composition by chaining three distinct phases:
1. **Scout**: Extract and enhance transcript
2. **Plan**: Analyze with specialized agent
3. **Build**: Store in knowledge base

## Usage

```
/process-youtube https://youtube.com/watch?v=VIDEO_ID
```

## Workflow

### Phase 1: Scout (Extract & Enhance)

Extract the raw transcript and automatically apply 174+ mapped corrections:

```bash
# Extract raw transcript
uv run python main.py extract "{{URL}}"

# Auto-enhance with corrections
uv run python -m src.processing.auto_enhancer raw_text_for_enhancement_*.txt
```

**Output**: Enhanced transcript ready for analysis

### Phase 2: Plan (Intelligent Analysis)

Use the orchestrator to select the appropriate specialized agent and analyze:

```bash
# Orchestrator detects video type and delegates to specialized agent
Use @youtube-processing-orchestrator to analyze the enhanced transcript
```

**Orchestrator will**:
- Detect channel (IndyDevDan, Sean Kochel, Liam Ottley, etc.)
- Select specialized analyzer if available
- Fall back to general @youtube-transcript-analyzer
- Generate structured JSON analysis

**Output**: High-quality JSON with tools, commands, concepts, workflows, takeaways

### Phase 3: Build (Store Knowledge)

Prepare content and store in MCP KB Memory:

```bash
# Prepare for MCP KB
uv run python scripts/store_in_mcp_kb.py [analysis_file].json

# Store in MCP KB Memory
Use mcp__mcp-kb-memory__store_memory with the prepared content
```

**Output**: Video knowledge stored and searchable

## Parameters

- **URL** (required): Full YouTube video URL

## Example

```
User: /process-youtube https://youtube.com/watch?v=nGhsgdQplHw
Claude: I'll process this IndyDevDan video using the Scout-Plan-Build workflow:

**Phase 1: Scout** - Extracting and enhancing transcript...
✅ Enhanced transcript with 18 corrections applied

**Phase 2: Plan** - Using @youtube-processing-orchestrator to select analyzer...
✅ Detected: IndyDevDan channel
✅ Using: @indydevdan-analyzer specialist
✅ Analysis complete with 16 tools, 12 commands, 16 concepts extracted

**Phase 3: Build** - Storing in MCP KB Memory...
✅ Content prepared and stored successfully

Video now searchable in knowledge base!
```

## Benefits

- **Consistency**: Same high-quality process every time
- **Efficiency**: Automated 3-phase workflow
- **Intelligence**: Channel-specific specialized analysis
- **Reusability**: Works for any YouTube video
- **Composability**: Can be used in other workflows

## Related Commands

- `/extract-youtube` - Just extract and enhance (Scout only)
- `/analyze-video` - Just analyze (Plan only)

## Notes

- Uses prompt composition pattern from agentic coding best practices
- Implements R&D framework (Reduce and Delegate) through orchestrator
- Maintains learning system for continuous improvement
- All extracted knowledge stored in MCP KB Memory for instant retrieval
