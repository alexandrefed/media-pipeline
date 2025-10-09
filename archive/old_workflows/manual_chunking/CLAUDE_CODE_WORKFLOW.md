# Manual Chunking Workflow for AI Knowledge Base

## Overview

This document describes the manual workflow for processing YouTube videos using Claude Code to create high-quality knowledge base entries. This approach creates semantically coherent chunks with proper token sizes.

## Key Insight: Manual Chunking Benefits

**Problem**: Algorithmic chunking created 222 tiny fragments (29 tokens average) with poor semantic boundaries.

**Solution**: Manual chunking with Claude Code creates 17 high-quality chunks (378 tokens average) with complete thoughts and proper context.

## Workflow Steps

### 1. Extract Raw Transcript

```bash
uv run python main.py extract "https://www.youtube.com/watch?v=VIDEO_ID"
```

This creates `raw_text_for_enhancement_VIDEO_ID.txt` with:
- Video metadata
- Clean transcript text
- Timestamp information

### 2. Enhance Transcript in Claude Code

1. Open the raw text file in Claude Code
2. Fix transcription errors:
   - "mate and" → "n8n"
   - "Curser" → "Cursor"
   - "zero" → "v0"
   - "Make dot com" → "Make.com"
3. Improve sentence flow and technical accuracy
4. Save enhanced version

### 3. Manual Chunking

Use the `manual_chunker.py` script to create high-quality chunks:

```bash
uv run python manual_chunker.py
```

### 4. Database Storage

The system stores chunks in PostgreSQL with pgvector and generates embeddings for semantic search.

## Quality Improvement Results

Manual chunking shows significant improvements:

| Metric | Algorithmic Chunking | Manual Chunking |
|--------|---------------------|-----------------|
| Total Chunks | 222 | 17 |
| Average Tokens | 29 | 378 |
| Usable Chunks | 0% | 100% |
| Semantic Coherence | Poor | Excellent |

## Manual Chunking Details

### Chunk Creation Process

The `manual_chunker.py` script creates chunks by:

1. **Analyzing Content Structure**: Understanding natural topic boundaries
2. **Defining Semantic Sections**: Creating chunks around complete concepts
3. **Calculating Timestamps**: Distributing time proportionally across chunks
4. **Validating Token Counts**: Ensuring proper size ranges (200-800 tokens)

### Example Chunk Quality

**Good Chunk Example:**
```
Title: "Model Pricing Analysis and Recommendations"
Tokens: 302
Content: Complete discussion of o3 pricing, comparisons with other models, and recommendations for different use cases.
Time: 4:18 - 6:18
```

### Common Transcription Corrections

| Transcription Error | Corrected To |
|--------------------|--------------|
| "mate and" | "n8n" |
| "Curser" | "Cursor" |
| "zero" / "the zero" | "v0" |
| "Make dot com" | "Make.com" |
| "clawed code" | "Claude Code" |

## Usage Instructions

1. **Extract transcript**:
   ```bash
   uv run python main.py extract <youtube_url>
   ```

2. **Enhance in Claude Code**:
   - Open the raw text file
   - Fix transcription errors
   - Improve readability
   - Save enhanced version

3. **Create manual chunks**:
   ```bash
   uv run python manual_chunker.py
   ```

4. **Import to database**:
   
   First, ensure the video source exists in the database:
   ```bash
   # Add the video source (if not already added)
   uv run python scripts/add_missing_sources.py
   ```
   
   Then import the manual chunks:
   ```bash
   # For a specific video
   uv run python scripts/import_manual_chunks.py
   
   # Or use the specific import script for the video
   uv run python scripts/import_[video_name]_chunks.py
   ```
   
   The import process will:
   - Generate embeddings for each chunk (384-dim vectors)
   - Extract mentioned tools automatically
   - Set quality score to 0.9 (high quality for manual chunks)
   - Upload to PostgreSQL with pgvector
   
5. **Verify import**:
   ```bash
   # Check database status
   uv run python main.py status
   
   # Test search for the new content
   uv run python main.py query "content from your video"
   ```

## Complete Workflow Example

Here's a complete example for processing a new video:

```bash
# 1. Extract transcript
uv run python main.py extract "https://www.youtube.com/watch?v=xf2i6Acs1mI"

# 2. Enhance in Claude Code (manual step)
# Open raw_text_for_enhancement_xf2i6Acs1mI.txt
# Fix errors, save as enhanced version

# 3. Create chunks
uv run python manual_chunker.py
# This creates manual_chunks_[video_name].json

# 4. Add source to database
uv run python scripts/add_missing_sources.py

# 5. Import chunks
uv run python scripts/import_manual_chunks.py

# 6. Verify
uv run python main.py query "n8n MCP automation"
```

## Benefits

### Quality Improvements
- **93% fewer chunks**: 17 vs 222 chunks
- **13x larger chunks**: 378 vs 29 tokens average
- **Complete thoughts**: No mid-sentence breaks
- **Semantic coherence**: Related concepts stay together

### Cost Efficiency
- **Reduced storage**: Less database overhead
- **Faster queries**: Fewer embeddings to search
- **Better retrieval**: More relevant results

## Best Practices

1. **Review transcript quality** before enhancement
2. **Fix tool names** during enhancement phase
3. **Validate chunk boundaries** for semantic coherence
4. **Check token counts** to ensure proper sizing
5. **Test search results** to verify chunk quality

## Future Enhancements

- Database import functionality
- Batch processing for multiple videos
- Automated chunk boundary suggestions
- Quality scoring for chunks
- Template system for different content types