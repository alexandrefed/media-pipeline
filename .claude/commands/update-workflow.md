# Update Workflow Documentation

**Purpose**: Automatically update workflow documentation, learning system, and README index after discovering improvements or completing implementations.

**Inspired by**: AI Jason's /update-doc command for maintaining institutional knowledge

## Usage

```
/update-workflow
```

**Note**: Slash commands in Claude Code don't accept arguments. When you invoke this command, you'll be prompted to specify the update type and details.

## Your Task

**STEP 1: Ask the user what type of update**

Ask: "What type of update would you like to make?"

**Available types**:
- `correction` - Add new transcription correction
- `workflow` - Document workflow improvement
- `sop` - Update or create new SOP
- `learning` - Add insight to learning system
- `index` - Rebuild .claude/README.md index

**STEP 2: Get the details**

Based on the type selected, ask for the relevant details (correction mapping, description, SOP name, etc.)

**STEP 3: Execute the appropriate workflow**

Based on user input, follow the corresponding procedure below.

## Workflows by Type

### 1. Update Transcription Corrections

```
/update-workflow correction "incorrect phrase" → "Correct Phrase"
```

**What it does**:
1. Analyzes the correction pattern
2. Updates `learning/processing_knowledge_base.json`
3. Tests on recent transcripts to verify
4. Documents in `learning/processing_history.md`
5. Updates .claude/README.md if needed

**Example**:
```
/update-workflow correction "zero dot dev" → "v0.dev"
```

**Output**:
- ✅ Added to entity_corrections in knowledge base
- ✅ Tested on 3 recent transcripts
- ✅ No false positives detected
- ✅ Processing history updated

### 2. Document Workflow Improvements

```
/update-workflow workflow "Brief description of improvement"
```

**What it does**:
1. Analyzes current STREAMLINED_WORKFLOW.md
2. Incorporates the improvement
3. Updates version history
4. Regenerates index

**Example**:
```
/update-workflow workflow "Added automatic quality scoring based on implementation details density"
```

**Output**:
- ✅ STREAMLINED_WORKFLOW.md updated
- ✅ New section added: Quality Scoring
- ✅ Version bumped to 1.1
- ✅ README index refreshed

### 3. Create or Update SOP

```
/update-workflow sop <sop-name> "Purpose and key changes"
```

**What it does**:
1. Creates new SOP if doesn't exist
2. Updates existing SOP with new information
3. Maintains version history
4. Updates README index

**Example**:
```
/update-workflow sop "context-optimization" "Proactive /compact usage and MCP management"
```

**Output**:
- ✅ Created: .claude/SOPs/context-optimization.md
- ✅ Documented /compact best practices
- ✅ Linked to MCP optimization guide
- ✅ README index updated

### 4. Add Learning System Insight

```
/update-workflow learning "Insight or lesson learned"
```

**What it does**:
1. Adds insight to processing_history.md
2. Updates relevant SOPs if applicable
3. Suggests corrections or workflow changes
4. Maintains knowledge continuity

**Example**:
```
/update-workflow learning "IndyDevDan videos consistently have 'clawed code' error - added to channel patterns"
```

**Output**:
- ✅ Added to processing_history.md
- ✅ Updated channel_patterns in knowledge base
- ✅ Noted in youtube-video-processing SOP
- ✅ Improvement tracked for metrics

### 5. Rebuild Documentation Index

```
/update-workflow index
```

**What it does**:
1. Scans .claude/ directory structure
2. Counts agents, commands, SOPs, system docs
3. Generates comprehensive README.md
4. Creates quick-reference links

**Output**:
- ✅ .claude/README.md regenerated
- ✅ 4 agents indexed
- ✅ 2 commands indexed
- ✅ 3 SOPs indexed
- ✅ 3 system docs indexed

## Implementation Details

### Automatic Actions

The command automatically:
1. **Validates** changes against existing documentation
2. **Tests** corrections on sample transcripts
3. **Updates** all related documents
4. **Maintains** version history
5. **Rebuilds** indexes and cross-references

### Smart Detection

The command understands:
- **Entity corrections** → Updates knowledge base + tests
- **Workflow changes** → Updates STREAMLINED_WORKFLOW.md + SOPs
- **New patterns** → Updates channel_patterns + agent prompts
- **Quality insights** → Updates guidelines + standards

### Cross-Referencing

Automatically updates:
- .claude/README.md (master index)
- Related SOP documents
- Learning system files
- Changelog/version history

## Benefits

### 1. Institutional Knowledge

Build knowledge that persists across sessions:
- Corrections are never forgotten
- Workflows improve iteratively
- Best practices are documented
- Mistakes aren't repeated

### 2. Consistency

Ensure documentation stays current:
- Automatic cross-reference updates
- Version history maintained
- Index always accurate
- No orphaned documentation

### 3. Efficiency

Save time on manual updates:
- One command updates multiple files
- Automatic validation and testing
- Smart conflict resolution
- Instant index regeneration

### 4. Quality Improvement

Continuous improvement loop:
- Track what works
- Document what doesn't
- Share learnings across videos
- Measure progress over time

## Examples from Real Usage

### Example 1: New Correction Discovered

```
User: I noticed the transcript has "zero dot dev" which should be "v0.dev"

Claude: Let me add that correction.
/update-workflow correction "zero dot dev" → "v0.dev"

✅ Analysis complete:
   - Pattern: Tool name transcription
   - Frequency: Found in 3 recent transcripts
   - False positive risk: Low (specific phrase)

✅ Updates applied:
   - learning/processing_knowledge_base.json (correction #175)
   - learning/processing_history.md (logged discovery)
   - .claude/SOPs/learning-system-updates.md (example added)

✅ Testing:
   - Tested on raw_text_for_enhancement_ABC123.txt
   - 2 instances corrected successfully
   - No false positives detected

Ready for next video processing!
```

### Example 2: Workflow Improvement

```
User: We should run /compact after each video to keep context clean

Claude: Excellent insight! Let me document this.
/update-workflow workflow "Add /compact step after video processing"

✅ Updates applied:
   - STREAMLINED_WORKFLOW.md updated
   - Added Step 4: Clean Up Context
   - .claude/SOPs/youtube-video-processing.md updated
   - Added /compact to procedure checklist

✅ Documentation:
   - Rationale: Frees context window for next video
   - Timing: After MCP KB storage complete
   - Expected benefit: 5-10% context reclamation

✅ Index refreshed:
   - .claude/README.md updated
   - Cross-references validated

Workflow improvement documented and ready to use!
```

### Example 3: Creating New SOP

```
User: We need an SOP for batch processing multiple videos

Claude: I'll create that SOP.
/update-workflow sop "batch-video-processing" "Process multiple YouTube videos efficiently"

✅ Created new SOP:
   - .claude/SOPs/batch-video-processing.md
   - Sections: Purpose, Prerequisites, Procedure, Quality Checks
   - Links to youtube-video-processing.md
   - Version: 1.0

✅ Content includes:
   - Loop structure for multiple URLs
   - Error handling strategies
   - Progress tracking
   - Batch /compact optimization

✅ Index updated:
   - .claude/README.md now shows 4 SOPs
   - Cross-references added
   - Related documents linked

New SOP ready to use!
```

## Interactive Examples

### Quick Correction
```
User: /update-workflow
Claude: What type of update would you like to make?
User: correction
Claude: Please provide the correction in format "incorrect" → "correct"
User: "zero dot dev" → "v0.dev"
Claude: [Analyzes, tests, and updates learning system]
```

### Detailed Workflow Update
```
User: /update-workflow
Claude: What type of update would you like to make?
User: workflow
Claude: Please describe the workflow improvement
User: Added automatic quality scoring based on implementation details density
Claude: [Updates STREAMLINED_WORKFLOW.md and related docs]
```

### Quick Index Rebuild (No Details Needed)
```
User: /update-workflow
Claude: What type of update would you like to make?
User: index
Claude: [Rebuilds .claude/README.md immediately]
```

## Alternative: Natural Language

You can also describe your intent in natural language:
```
User: "Add this transcription correction: 'zero dot dev' should be 'v0.dev'"
Claude: [Recognizes intent and updates learning system]
```

## Integration with Existing Workflows

### After Processing a Video

```bash
# Standard workflow
uv run python main.py streamlined "VIDEO_URL"
# ... agent analysis ...
# ... MCP KB storage ...

# Document any learnings
/update-workflow learning "New correction discovered: X → Y"
/compact
```

### After Making Workflow Changes

```bash
# Made improvement to processing
# Document it immediately
/update-workflow workflow "Description of improvement"

# Rebuild index to reflect changes
/update-workflow index
```

### Regular Maintenance

```bash
# Weekly: Rebuild index to catch any manual edits
/update-workflow index

# Monthly: Review and update SOPs based on accumulated learnings
# Check learning/processing_history.md for patterns
```

## Related Commands

- `/process-youtube` - Main video processing workflow
- `/compact` - Clean conversation context
- `/context` - Check token usage

## Related Documents

- [YouTube Video Processing SOP](../SOPs/youtube-video-processing.md)
- [Learning System Updates SOP](../SOPs/learning-system-updates.md)
- [STREAMLINED_WORKFLOW.md](../../STREAMLINED_WORKFLOW.md)
- [.claude/README.md](../README.md) - Master index

## Notes

- Inspired by AI Jason's /update-doc command
- Implements "institutional knowledge" pattern
- Prevents repeated mistakes across sessions
- Builds on successful implementations
- Maintains documentation quality over time

## Version History

- v1.0 (Jan 2025): Initial command implementation based on AI Jason video insights
