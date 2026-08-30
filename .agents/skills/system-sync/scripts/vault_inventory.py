#!/usr/bin/env python3
"""Return a deterministic, cross-platform inventory of this Obsidian vault."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path


def relative_paths(paths: list[Path], root: Path) -> list[str]:
    return sorted(path.relative_to(root).as_posix() for path in paths)


def frontmatter_value(path: Path, key: str) -> str | None:
    text = path.read_text(encoding="utf-8-sig")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    match = re.search(rf"^{re.escape(key)}:\s*['\"]?([^'\"\n]+)", parts[1], re.MULTILINE)
    return match.group(1).strip() if match else None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", default=".", help="Vault root; defaults to the current directory.")
    args = parser.parse_args()

    root = Path(args.vault).resolve()
    card_root = root / "03_Knowledge" / "00_Cards"
    card_files = sorted(
        path
        for path in card_root.glob("*.md")
        if path.name != "README.md" and not path.name.startswith("_EXAMPLE_")
    )
    cards = [path for path in card_files if frontmatter_value(path, "type") == "card"]
    card_types = Counter(
        value
        for path in cards
        if (value := frontmatter_value(path, "card_type")) is not None
    )

    templates = list((root / "Templates" / "Cards").glob("*_Card.md"))
    skills = list((root / ".agents" / "skills").glob("*/SKILL.md"))
    readmes = [path for path in root.rglob("README.md") if ".git" not in path.parts]
    bases = list((root / "Bases").glob("*.base"))
    canvases = [path for path in root.rglob("*.canvas") if ".git" not in path.parts]
    mocs = list(card_root.glob("moc_*.md"))
    attachments = [
        path
        for path in root.rglob("*")
        if path.is_file()
        and "Attachments" in path.parts
        and path.name != ".gitkeep"
        and ".git" not in path.parts
        and ".obsidian" not in path.parts
    ]

    result = {
        "vault": str(root),
        "git_repository": (root / ".git").exists(),
        "entrypoints": {
            "agent.md": (root / "agent.md").exists(),
            "AGENTS.md": (root / "AGENTS.md").exists(),
            "CLAUDE.md": (root / "CLAUDE.md").exists(),
        },
        "counts": {
            "cards": len(cards),
            "card_types": len(card_types),
            "card_templates": len(templates),
            "skills": len(skills),
            "readmes": len(readmes),
            "bases": len(bases),
            "canvases": len(canvases),
            "mocs": len(mocs),
            "attachments": len(attachments),
        },
        "card_type_distribution": dict(sorted(card_types.items())),
        "card_templates": relative_paths(templates, root),
        "skills": relative_paths(skills, root),
        "readmes": relative_paths(readmes, root),
        "bases": relative_paths(bases, root),
        "canvases": relative_paths(canvases, root),
        "mocs": relative_paths(mocs, root),
        "attachments": relative_paths(attachments, root),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
