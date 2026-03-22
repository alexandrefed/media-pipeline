"""Placeholder test to verify CI pipeline works."""


def test_project_structure():
    """Verify core modules are importable."""
    from src.storage import unified_memory_client  # noqa: F401
    from src.pipeline import youtube_processor  # noqa: F401
