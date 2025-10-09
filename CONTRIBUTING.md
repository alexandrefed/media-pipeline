# Contributing to AI Knowledge Base

First off, thank you for considering contributing to AI Knowledge Base! It's people like you that make this project better.

## Code of Conduct

This project and everyone participating in it is governed by respect, professionalism, and collaboration. By participating, you are expected to uphold these values.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples** (code snippets, commands, etc.)
- **Describe the behavior you observed and what you expected**
- **Include screenshots or error messages** if applicable
- **Specify your environment** (OS, Python version, uv version)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the suggested enhancement**
- **Explain why this enhancement would be useful**
- **List any alternative solutions or features you've considered**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Set up your environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   uv sync
   ```

3. **Make your changes**:
   - Write clear, descriptive commit messages
   - Follow the existing code style
   - Add tests if applicable
   - Update documentation as needed

4. **Test your changes**:
   ```bash
   # Run tests
   uv run pytest tests/

   # Run linting
   uv run ruff check src/

   # Format code
   uv run black src/
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `refactor:` for code refactoring
   - `test:` for adding tests
   - `chore:` for maintenance tasks

6. **Push to your fork** and submit a pull request

## Development Guidelines

### Project Structure

```
ai-knowledge-base/
├── src/                    # Core application code
├── workspace/              # Active work area (gitignored)
├── .claude/                # Claude Code configuration
│   ├── agents/             # Specialized agents
│   └── commands/           # Custom slash commands
├── learning/               # AI learning system (gitignored)
├── scripts/                # Utility scripts
├── docs/                   # Documentation
└── tests/                  # Test files
```

### Coding Standards

- **Python 3.11+** required
- **Use uv** for package management (not pip)
- **Type hints** encouraged
- **Docstrings** for public functions and classes
- **Follow PEP 8** (enforced by black and ruff)

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for meaningful test coverage

### Documentation

- Update README.md if adding user-facing features
- Update CLAUDE.md for Claude Code-specific changes
- Document new environment variables in .env.example
- Add docstrings to new functions/classes

## Specialized Agent Contributions

If you're contributing new specialized agents:

1. **Create agent file** in `.claude/agents/`
2. **Follow naming convention**: `channel-name-analyzer.md`
3. **Include**:
   - Channel expertise description
   - Teaching style patterns
   - Common terminology
   - Transcription error patterns
   - Enhanced extraction guidelines
4. **Test thoroughly** with real video transcripts
5. **Document** in DOCUMENTATION_INDEX.md

## Adding Specialized Analyzers

To add a new channel-specific analyzer:

1. Study the existing analyzers:
   - `.claude/agents/indydevdan-analyzer.md`
   - `.claude/agents/seankochel-analyzer.md`

2. Identify channel patterns:
   - Content style and structure
   - Common terminology
   - Transcription error patterns
   - Domain-specific knowledge

3. Create new analyzer file following the template

4. Update the orchestrator to detect and route to your analyzer

5. Test with multiple videos from the channel

## Learning System Contributions

If updating the learning system (`learning/processing_knowledge_base.json`):

- Add new transcription corrections with examples
- Document channel-specific patterns
- Include content type guidelines
- Provide quality improvement insights

**Note**: Your personal `processing_knowledge_base.json` and `processing_history.md` are gitignored. Contribute by updating the template/documentation, not personal data.

## Questions?

Feel free to:
- Open an issue for discussion
- Ask questions in pull request comments
- Reach out to maintainers

## Recognition

Contributors will be recognized in the project README and release notes.

---

Thank you for contributing to AI Knowledge Base! 🎉
