#!/usr/bin/env python3
"""Capture an authenticated browser session for /prefill — once, manually.

You run this yourself, log in by hand, and the cookies persist in a gitignored browser
profile that the Playwright MCP later reuses. We NEVER script logins or handle passwords in
prompts (CLAUDE.md HARD RULES 2 & 4): you type your credentials directly into the real site.

How it works: opens a visible (headed) Chromium using a persistent profile at `.auth/pw-profile`
— the same `--user-data-dir` the Playwright MCP is configured with — navigates to the login URL
you pass, and waits for you to finish logging in and press Enter. The session then lives in the
profile (gitignored), so `/prefill` finds you already signed in.

One-time setup (only needed for sites that require a login; public application pages don't):
    pip install playwright && playwright install chromium

Usage:
    python scripts/save_session.py https://www.linkedin.com/login
    python scripts/save_session.py https://<ats-login-url>   [--profile .auth/pw-profile]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Repo root is the parent of scripts/; the profile dir matches .mcp.json's --user-data-dir.
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PROFILE = ROOT / ".auth" / "pw-profile"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Open a headed browser to capture a login session for /prefill (manual)."
    )
    parser.add_argument("url", help="login URL to open (you log in by hand)")
    parser.add_argument(
        "--profile",
        default=str(DEFAULT_PROFILE),
        help="persistent profile dir (default: .auth/pw-profile — must match .mcp.json)",
    )
    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "error: python-playwright is not installed. This one-time login-capture tool needs it:\n"
            "    pip install playwright && playwright install chromium\n"
            "(Only required for sites that need a login; public application pages don't.)",
            file=sys.stderr,
        )
        return 3

    profile = Path(args.profile)
    profile.mkdir(parents=True, exist_ok=True)

    print(f"Opening a visible browser with profile: {profile.relative_to(ROOT) if ROOT in profile.parents else profile}")
    print("→ Log in by hand in the window. Do NOT paste credentials here.")
    with sync_playwright() as pw:
        context = pw.chromium.launch_persistent_context(str(profile), headless=False)
        page = context.pages[0] if context.pages else context.new_page()
        try:
            page.goto(args.url)
        except Exception as exc:  # noqa: BLE001 - report, let the user still log in/navigate
            print(f"(note: could not auto-navigate to {args.url!r}: {exc})", file=sys.stderr)
        try:
            input("\nWhen you've finished logging in, press Enter here to save the session… ")
        except (EOFError, KeyboardInterrupt):
            print("\naborted — closing without an explicit save (profile may still hold cookies).")
        context.close()

    print(f"Session saved in {profile}. /prefill will reuse it (the dir is gitignored).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
