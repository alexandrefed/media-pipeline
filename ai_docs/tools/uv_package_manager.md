# uv - Modern Python Package Manager

## Overview

`uv` is an extremely fast Python package and project manager written in Rust. It replaces pip, pip-tools, pipx, and poetry with 10-100x faster performance. This project uses `uv` for all Python dependency management in project mode.

## Key Benefits

- **Speed**: 10-100x faster than pip
- **Project Management**: Built-in `pyproject.toml` support
- **Automatic Virtual Environments**: No need for separate virtualenv commands
- **Reproducible builds**: Built-in lock file support
- **No Python required**: Written in Rust, works without Python installed

## Installation

### macOS/Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Project-Based Development Workflow

Since the AI Knowledge Base is a proper Python project with `pyproject.toml`, we use uv's project management commands exclusively.

### Core Project Commands

```bash
# Initialize a new project
uv init

# Add dependencies to the project
uv add psycopg2-binary
uv add sentence-transformers
uv add yt-dlp

# Install all dependencies (creates/updates .venv automatically)
uv sync

# Run scripts in the project environment
uv run python src/ingest_video.py
```

## AI Knowledge Base Project Setup

### Initial Project Setup
```bash
# 1. Initialize project (if not already done)
uv init

# 2. Add core dependencies
uv add psycopg2-binary asyncpg pydantic python-dotenv

# 3. Add processing libraries
uv add yt-dlp rapidfuzz sentence-transformers

# 4. Add development tools
uv add pytest black ruff --dev

# 5. Install all dependencies
uv sync
```

### Working with Dependencies

```bash
# Add a new dependency
uv add requests

# Add a development dependency
uv add pytest --dev

# Remove a dependency
uv remove requests

# Upgrade all dependencies
uv lock --upgrade
uv sync

# Install dependencies for existing project
uv sync
```

### Running Code

```bash
# Run a Python script
uv run python src/main.py

# Run tests
uv run pytest

# Run with specific arguments
uv run python src/ingest_video.py "https://youtube.com/watch?v=example"
```

## Performance Comparison

| Operation | Traditional | uv |
|-----------|-------------|-----|
| Install NumPy | 1.5s | 0.1s |
| Install Django | 2.8s | 0.2s |
| Create environment | 3.0s | 0.01s |
| Install from lock | 45s | 0.8s |

## Best Practices

1. **Always use uv project commands** for the AI Knowledge Base
2. **Commit uv.lock** to version control for reproducible builds
3. **Use `uv sync`** to ensure consistent environments
4. **Run scripts with `uv run`** to ensure proper environment

## Project Structure

When using uv project mode, your directory structure should be:

```
ai-knowledge-base/
├── pyproject.toml          # Project configuration and dependencies
├── uv.lock                 # Locked dependency versions
├── .venv/                  # Virtual environment (auto-created)
├── src/                    # Source code
└── README.md
```

## Common Commands for AI Knowledge Base

### Development Workflow
```bash
# Start working on the project
uv sync

# Add a new library for processing
uv add beautifulsoup4

# Run the ingestion pipeline
uv run python src/pipeline/ingest.py

# Run tests
uv run pytest tests/

# Format code
uv run black src/
```

### Dependency Management
```bash
# Check what's installed
uv tree

# Update dependencies
uv lock --upgrade
uv sync

# Add optional dependency group
uv add --group docs mkdocs mkdocs-material
```

## Configuration

The project configuration is stored in `pyproject.toml`:

```toml
[project]
name = "ai-knowledge-base"
version = "0.1.0"
dependencies = [
    "psycopg2-binary",
    "sentence-transformers",
    "yt-dlp",
    "rapidfuzz",
]

[tool.uv]
dev-dependencies = [
    "pytest",
    "black",
    "ruff",
]
```

## Project-Specific Notes

- Use Python 3.11+ for compatibility with all ML libraries
- The 384-dimensional embeddings require `sentence-transformers` with model `all-MiniLM-L6-v2`
- Database connections use `psycopg2-binary` for simplicity
- All scripts should be run with `uv run` to ensure proper environment