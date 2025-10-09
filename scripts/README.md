# Scripts Directory

This directory contains active utility scripts for the Phase 1 Agentic Workflow.

## Active Scripts

### `streamlined_process.py`
**Purpose**: Automates the complete video processing pipeline

**Usage**:
```bash
uv run python scripts/streamlined_process.py <youtube_url>
```

**What it does**:
1. Extracts raw transcript from YouTube video
2. Applies auto-enhancement (174+ transcription corrections)
3. Prepares for agent analysis
4. Guides next steps in the workflow

**When to use**: For quick, automated video processing

---

### `store_in_mcp_kb.py`
**Purpose**: Prepares agent analysis JSON for MCP KB Memory storage

**Usage**:
```bash
uv run python scripts/store_in_mcp_kb.py <analysis_file>.json
```

**What it does**:
1. Reads agent analysis JSON
2. Formats content for MCP KB Memory
3. Creates `_mcp_kb_ready.txt` file
4. Provides instructions for final storage

**When to use**: After agent analysis, before storing in MCP KB

---

## Deprecated Scripts

All deprecated scripts from the PostgreSQL VPS phase have been moved to:
- `../archive/deprecated_scripts/chunkers/` - 18 video-specific manual chunkers
- `../archive/deprecated_scripts/postgresql_imports/` - 21 PostgreSQL import scripts
- `../archive/deprecated_scripts/experimental/` - 6 experimental/one-off scripts

See `../archive/deprecated_scripts/README.md` for details on deprecated scripts.

---

## Adding New Scripts

If you need to add a new utility script:

1. **Create the script** in this directory
2. **Add documentation** to this README
3. **Follow naming convention**: `descriptive_name.py`
4. **Include docstring** at the top of the file
5. **Test thoroughly** before committing

## Script Guidelines

- **Keep it simple**: Scripts should do one thing well
- **Use uv**: Always prefix with `uv run python` for consistency
- **Document usage**: Include clear usage examples
- **Handle errors**: Provide helpful error messages
- **Clean output**: Use clear, informative print statements

---

**Last Updated**: January 2025 (Phase 1 Cleanup)
