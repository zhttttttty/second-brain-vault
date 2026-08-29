#!/usr/bin/env python3
"""Validate structural contracts that should not depend on an AI review."""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised by installation state
    raise SystemExit(
        "Missing dependency: PyYAML. Run: "
        "python -m pip install -r requirements-dev.txt"
    ) from exc


WIKILINK_RE = re.compile(r"^\[\[([^\]]+)\]\]$")
SKILL_HEADING_RE = re.compile(r"^### `([^`]+)`\s*$", re.MULTILINE)


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def read_frontmatter(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    text = path.read_text(encoding="utf-8-sig")
    if not text.startswith("---"):
        return None, None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None, "frontmatter is not closed with ---"
    try:
        data = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        return None, f"invalid YAML: {str(exc).splitlines()[0]}"
    if not isinstance(data, dict):
        return None, "frontmatter must be a YAML mapping"
    return data, None


def registered_tags(root: Path) -> set[str]:
    schema = (root / "00_System" / "Vault_Schema.md").read_text(encoding="utf-8-sig")
    taxonomy = schema.split("## 主题标签分类法", 1)[1].split("## 使用规则", 1)[0]
    tags: set[str] = set()
    for line in taxonomy.splitlines():
        if "不再并存" in line:
            continue
        for token in re.findall(r"`([^`]+/[^`]+)`", line):
            if " " not in token and "、" not in token:
                tags.add(token)
    return tags


def check_entrypoints(root: Path, errors: list[str], warnings: list[str]) -> None:
    agent = root / "agent.md"
    agents = root / "AGENTS.md"
    claude_skills = root / ".claude" / "skills"
    canonical_skills = root / ".agents" / "skills"

    if not agent.is_file():
        errors.append("agent.md is missing")

    if not agents.exists() and not agents.is_symlink():
        errors.append("AGENTS.md is missing")
    elif agents.is_symlink():
        if not agents.resolve().is_file():
            errors.append("AGENTS.md is a broken symbolic link")
    elif agents.is_file():
        content = agents.read_text(encoding="utf-8-sig").strip()
        if content == "agent.md":
            errors.append(
                "AGENTS.md was checked out as a symlink stub; enable Git symlinks and clone again"
            )
        elif agent.is_file() and agents.read_bytes() != agent.read_bytes():
            warnings.append("AGENTS.md is a regular fallback copy and has drifted from agent.md")
        else:
            warnings.append("AGENTS.md is a regular fallback copy; keep it synchronized with agent.md")

    if not claude_skills.exists() and not claude_skills.is_symlink():
        errors.append(".claude/skills is missing")
    elif claude_skills.is_symlink():
        if not claude_skills.resolve().is_dir():
            errors.append(".claude/skills is a broken symbolic link")
    elif claude_skills.is_file():
        errors.append(
            ".claude/skills was checked out as a symlink stub; enable Git symlinks and clone again"
        )
    elif claude_skills.is_dir():
        canonical = {path.parent.name for path in canonical_skills.glob("*/SKILL.md")}
        fallback = {path.parent.name for path in claude_skills.glob("*/SKILL.md")}
        if canonical != fallback:
            errors.append(".claude/skills fallback copy differs from .agents/skills")
        else:
            warnings.append(".claude/skills is a fallback copy; it must be synchronized manually")


def check_broken_symlinks(root: Path, errors: list[str]) -> None:
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = [name for name in dirnames if name != ".git"]
        base = Path(directory)
        for name in [*dirnames, *filenames]:
            path = base / name
            if path.is_symlink() and not path.exists():
                errors.append(f"{rel(path, root)}: broken symbolic link")


def check_markdown(root: Path, errors: list[str]) -> None:
    names: dict[str, list[Path]] = {}
    markdown = [path for path in root.rglob("*.md") if ".git" not in path.parts]
    for path in markdown:
        names.setdefault(path.stem, []).append(path)

    allowed_tags = registered_tags(root)
    for path in markdown:
        data, error = read_frontmatter(path)
        if error:
            errors.append(f"{rel(path, root)}: {error}")
            continue
        if data is None:
            continue

        tags = data.get("tags")
        if tags is not None:
            if not isinstance(tags, list) or any(not isinstance(tag, str) for tag in tags):
                errors.append(f"{rel(path, root)}: tags must be a list of strings")
            elif ".templates" not in path.parts:
                for tag in tags:
                    if tag not in allowed_tags:
                        errors.append(f"{rel(path, root)}: unregistered tag: {tag}")

        related = data.get("related")
        if related is not None:
            if not isinstance(related, list) or any(not isinstance(item, str) for item in related):
                errors.append(f"{rel(path, root)}: related must be a flat list of strings")
            else:
                for item in related:
                    if "{{" in item:
                        continue
                    match = WIKILINK_RE.match(item)
                    if not match:
                        errors.append(
                            f"{rel(path, root)}: related item must be a quoted wikilink: {item!r}"
                        )
                        continue
                    target = match.group(1).split("|", 1)[0].split("#", 1)[0]
                    if ".templates" not in path.parts and Path(target).name not in names:
                        errors.append(f"{rel(path, root)}: unresolved related link: {item}")

        is_card = path.parent == root / "04_Knowledge" / "00_Cards"
        is_real_card = is_card and path.name != "README.md" and not path.name.startswith("_EXAMPLE_")
        if is_real_card:
            if data.get("type") != "card":
                errors.append(f"{rel(path, root)}: formal card must use type: card")
            if not isinstance(data.get("card_type"), str):
                errors.append(f"{rel(path, root)}: formal card is missing card_type")
            if "{{" in path.read_text(encoding="utf-8-sig"):
                errors.append(f"{rel(path, root)}: formal card still contains template placeholders")


def check_templates(root: Path, errors: list[str]) -> None:
    template_root = root / "04_Knowledge" / "00_Cards" / ".templates"
    templates = {path.name for path in template_root.glob("*_Card.md")}
    type_map = (
        root / ".agents" / "skills" / "card-creator" / "references" / "card-type-map.md"
    ).read_text(encoding="utf-8-sig")
    mapped = set(re.findall(r"\| `[^`]+` \|[^\n]+\| `([^`]+_Card\.md)` \|", type_map))
    for missing in sorted(templates - mapped):
        errors.append(f"card-type-map.md does not register template: {missing}")
    for missing in sorted(mapped - templates):
        errors.append(f"card-type-map.md references missing template: {missing}")


def check_documented_counts(root: Path, errors: list[str]) -> None:
    skills = {path.parent.name for path in (root / ".agents" / "skills").glob("*/SKILL.md")}
    templates = list((root / "04_Knowledge" / "00_Cards" / ".templates").glob("*_Card.md"))
    examples = list((root / "04_Knowledge" / "00_Cards").glob("_EXAMPLE_*.md"))
    readme = (root / "README.md").read_text(encoding="utf-8-sig")
    manual = (root / "Skills_Manual.md").read_text(encoding="utf-8-sig")

    claims = (
        (readme, r"\*\*(\d+) 种(?:原子化|标准化)卡片模板\*\*", len(templates), "README card templates"),
        (readme, r"\*\*(\d+) 个开箱即用的 AI 技能", len(skills), "README skills"),
        (manual, r"当前本地技能数量：(\d+) 个", len(skills), "Skills_Manual skills"),
    )
    for text, pattern, actual, label in claims:
        match = re.search(pattern, text)
        if match and int(match.group(1)) != actual:
            errors.append(f"{label} claims {match.group(1)}, actual is {actual}")

    tree_claim = re.search(r"00_Cards/\s+# (\d+) 种[^\n]+\+ (\d+) 张示例", readme)
    if tree_claim and (int(tree_claim.group(1)), int(tree_claim.group(2))) != (
        len(templates),
        len(examples),
    ):
        errors.append(
            "README directory tree card counts differ from the filesystem: "
            f"templates={len(templates)}, examples={len(examples)}"
        )

    manual_skills = set(SKILL_HEADING_RE.findall(manual))
    if manual_skills != skills:
        missing = ", ".join(sorted(skills - manual_skills)) or "none"
        extra = ", ".join(sorted(manual_skills - skills)) or "none"
        errors.append(f"Skills_Manual skill sections differ: missing={missing}; extra={extra}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", default=".", help="Vault root; defaults to current directory")
    parser.add_argument("--strict", action="store_true", help="Treat portability warnings as failures")
    args = parser.parse_args()

    root = Path(args.vault).resolve()
    required = (root / "agent.md", root / "00_System" / "Vault_Schema.md")
    if not all(path.exists() for path in required):
        raise SystemExit("Error: --vault must point to the Vault root")

    errors: list[str] = []
    warnings: list[str] = []
    check_broken_symlinks(root, errors)
    check_entrypoints(root, errors, warnings)
    check_markdown(root, errors)
    check_templates(root, errors)
    check_documented_counts(root, errors)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors or (args.strict and warnings):
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        raise SystemExit(1)
    print(f"OK: vault validation passed with {len(warnings)} warning(s)")


if __name__ == "__main__":
    main()
