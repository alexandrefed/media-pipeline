"""Folder platform code comes from the URL, never a hard-coded ``yt`` (task ebdfe7a3)."""

from src.pipeline.platform_code import platform_code


def test_known_hosts():
    assert platform_code("https://www.youtube.com/watch?v=abc") == "yt"
    assert platform_code("https://youtu.be/abc") == "yt"
    assert platform_code("https://www.instagram.com/reel/DeUJCGiAY6v/?mdxt=x") == "ig"
    assert platform_code("https://instagram.com/p/Db6qLt_CJdq/") == "ig"
    assert platform_code("https://www.tiktok.com/@a/video/1") == "tt"
    assert platform_code("https://x.com/a/status/1") == "x"
    assert platform_code("https://twitter.com/a/status/1") == "x"
    assert platform_code("https://vimeo.com/123") == "vm"


def test_unknown_or_lookalike_hosts_are_web():
    assert platform_code("https://neo4j.ondemand.goldcast.io/on-demand/x") == "web"
    assert platform_code("https://notyoutube.com/watch?v=abc") == "web"
    assert platform_code("not a url") == "web"
