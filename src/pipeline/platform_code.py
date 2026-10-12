"""The platform code that goes in a video folder name, read from the URL.

Folder names are ``{date}--{id}--{platform}--{channel}--{title}`` (CLAUDE.md,
"Video Folder Convention"). Both writers of that name used to hard-code ``yt``,
so an Instagram reel sent through ``main.py streamlined`` produced a ``--yt--``
folder holding only metadata.json beside the real ``--ig--`` one: 53 such twins
on the gaming-PC by 2026-10-12 (task ebdfe7a3).
"""

from urllib.parse import urlparse

_HOSTS = {
    "youtube.com": "yt",
    "youtu.be": "yt",
    "instagram.com": "ig",
    "tiktok.com": "tt",
    "x.com": "x",
    "twitter.com": "x",
    "vimeo.com": "vm",
}


def platform_code(url: str) -> str:
    """``yt``/``ig``/``tt``/``x``/``vm`` from the URL's host, ``web`` for anything else."""
    host = (urlparse(url).netloc or "").lower().split(":")[0]
    for domain, code in _HOSTS.items():
        if host == domain or host.endswith("." + domain):
            return code
    return "web"
