#!/usr/bin/env python3
"""Preview or capture one webpage into the Vault reference Inbox using Defuddle."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


def run_defuddle(command: str, url: str, *extra: str) -> str:
    result = subprocess.run(
        [command, "parse", url, *extra],
        check=False,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown error"
        raise RuntimeError(f"Defuddle failed: {detail}")
    return result.stdout.strip()


def safe_name(title: str, url: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "", title)
    cleaned = re.sub(r"\s+", "_", cleaned).strip(" ._")
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:8]
    return f"{(cleaned[:72] or 'web_capture')}_{digest}.md"


def build_note(title: str, url: str, markdown: str) -> str:
    quoted_url = json.dumps(url, ensure_ascii=False)
    quoted_date = json.dumps(date.today().isoformat())
    return (
        "---\n"
        "type: reference\n"
        "source_kind: web\n"
        f"source: {quoted_url}\n"
        f"clipped: {quoted_date}\n"
        "extraction_tool: defuddle\n"
        "tags: []\n"
        "---\n\n"
        f"# {title}\n\n"
        f"## 来源\n\n[{title}]({url})\n\n"
        "## 网页正文\n\n"
        f"{markdown.strip()}\n"
    )


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", default=".", help="Vault root")
    parser.add_argument("--url", required=True, help="One public HTTP(S) URL")
    parser.add_argument("--write", action="store_true", help="Write after user confirmation")
    args = parser.parse_args()

    parsed = urlparse(args.url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise SystemExit("Error: --url must be one public HTTP(S) URL")
    if parsed.username or parsed.password:
        raise SystemExit("Error: URLs containing credentials are not accepted")
    hostname = parsed.hostname or ""
    if hostname.lower() == "localhost":
        raise SystemExit("Error: local or private network URLs are not accepted")
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        pass
    else:
        if not address.is_global:
            raise SystemExit("Error: local or private network URLs are not accepted")
    if parsed.path.lower().endswith(".md"):
        raise SystemExit("Error: .md URLs are already Markdown; do not process them with Defuddle")

    root = Path(args.vault).resolve()
    inbox = root / "04_References" / "01_Inbox"
    if not (root / "agent.md").is_file() or not inbox.is_dir():
        raise SystemExit("Error: --vault must point to this Vault root")

    command = shutil.which("defuddle")
    if not command:
        raise SystemExit("Error: defuddle command is unavailable; install the upstream defuddle tool first")

    try:
        markdown = run_defuddle(command, args.url, "--md")
        title = run_defuddle(command, args.url, "-p", "title").strip().splitlines()[0]
    except RuntimeError as exc:
        raise SystemExit(f"Error: {exc}") from exc

    if not markdown:
        raise SystemExit("Error: Defuddle returned empty Markdown")
    title = title or parsed.netloc
    note = build_note(title, args.url, markdown)
    target = inbox / safe_name(title, args.url)

    if target.exists():
        raise SystemExit(f"Error: target already exists; refusing to overwrite: {target}")

    print(f"Title: {title}")
    print(f"Target: {target}")
    if not args.write:
        preview = note[:1600]
        print("Mode: preview only (nothing written)")
        print("--- PREVIEW ---")
        print(preview)
        if len(note) > len(preview):
            print("... [preview truncated]")
        return

    target.write_text(note, encoding="utf-8", newline="\n")
    print("Mode: wrote one Inbox clipping")
    print("Next: run digest on the exact target path")


if __name__ == "__main__":
    main()
