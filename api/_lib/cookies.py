"""
YouTube cookies helper for yt-dlp.
Reads cookies from YOUTUBE_COOKIES env var and writes to /tmp/yt_cookies.txt.
This is needed because YouTube blocks datacenter IPs (Vercel, etc).
"""
import os

COOKIE_FILE = "/tmp/yt_cookies.txt"

def get_ytdlp_cookie_opts() -> dict:
    """Return yt-dlp options dict with cookiefile if YOUTUBE_COOKIES env var is set."""
    cookies_content = os.environ.get("YOUTUBE_COOKIES", "").strip()
    if not cookies_content:
        return {}

    # Write cookies to temp file (Vercel only allows /tmp)
    try:
        with open(COOKIE_FILE, "w", encoding="utf-8") as f:
            f.write(cookies_content)
        return {"cookiefile": COOKIE_FILE}
    except Exception:
        return {}
