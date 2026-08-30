#!/usr/bin/env python3
"""Validate structural contracts that should not depend on an AI review."""

from __future__ import annotations

import argparse
import json
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
HEX_ID_RE = re.compile(r"^[0-9a-fA-F]{16}$")
BASE_TEMPLATE_MAP = {
    "Books.base": ("book", "Book_Card.md"),
    "Persons.base": ("person", "Person_Card.md"),
    "Resources.base": ("resource", "Resource_Card.md"),
    "Opensource.base": ("opensource", "Opensource_Card.md"),
    "Subscriptions.base": ("subscription", "Subscription_Card.md"),
}


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
    schema = (root / "System" / "Vault_Schema.md").read_text(encoding="utf-8-sig")
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
            elif "Templates" not in path.parts:
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
                    if "Templates" not in path.parts and Path(target).name not in names:
                        errors.append(f"{rel(path, root)}: unresolved related link: {item}")

        is_card = path.parent == root / "03_Knowledge" / "00_Cards"
        is_real_card = is_card and path.name != "README.md" and not path.name.startswith("_EXAMPLE_")
        if is_real_card:
            if data.get("type") != "card":
                errors.append(f"{rel(path, root)}: formal card must use type: card")
            if not isinstance(data.get("card_type"), str):
                errors.append(f"{rel(path, root)}: formal card is missing card_type")
            if "{{" in path.read_text(encoding="utf-8-sig"):
                errors.append(f"{rel(path, root)}: formal card still contains template placeholders")


def check_templates(root: Path, errors: list[str]) -> None:
    templates_root = root / "Templates"
    template_root = templates_root / "Cards"
    templates = {path.name for path in template_root.glob("*_Card.md")}
    for required in (templates_root / "Daily_Note.md", templates_root / "Project.md"):
        if not required.is_file():
            errors.append(f"{rel(required, root)} is missing")
    legacy_directories = [
        path
        for path in root.rglob(".templates")
        if ".git" not in path.parts and path.is_dir()
    ]
    for path in legacy_directories:
        errors.append(f"{rel(path, root)}: legacy template directory must be migrated to Templates/")

    config_expectations = {
        root / ".obsidian" / "templates.json": {"folder": "Templates"},
        root / ".obsidian" / "daily-notes.json": {
            "folder": "01_Daily",
            "template": "Templates/Daily_Note",
        },
    }
    for path, expected in config_expectations.items():
        try:
            config = json.loads(path.read_text(encoding="utf-8-sig"))
        except (FileNotFoundError, json.JSONDecodeError) as exc:
            errors.append(f"{rel(path, root)}: cannot read Obsidian template config: {exc}")
            continue
        for key, value in expected.items():
            if config.get(key) != value:
                errors.append(f"{rel(path, root)}: {key} must be {value!r}")
    type_map = (
        root / ".agents" / "skills" / "card-creator" / "references" / "card-type-map.md"
    ).read_text(encoding="utf-8-sig")
    mapped = set(re.findall(r"\| `[^`]+` \|[^\n]+\| `([^`]+_Card\.md)` \|", type_map))
    for missing in sorted(templates - mapped):
        errors.append(f"card-type-map.md does not register template: {missing}")
    for missing in sorted(mapped - templates):
        errors.append(f"card-type-map.md references missing template: {missing}")


def scalar_strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [item for child in value.values() for item in scalar_strings(child)]
    if isinstance(value, list):
        return [item for child in value for item in scalar_strings(child)]
    return []


def check_bases(root: Path, errors: list[str]) -> None:
    base_root = root / "Bases"
    template_root = root / "Templates" / "Cards"
    legacy_view_keys = {"columns", "sort", "image", "imageFit", "title", "body"}
    allowed_view_types = {"table", "cards", "list", "map"}

    for path in sorted(base_root.glob("*.base")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8-sig")) or {}
        except yaml.YAMLError as exc:
            errors.append(f"{rel(path, root)}: invalid YAML: {str(exc).splitlines()[0]}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel(path, root)}: Base must be a YAML mapping")
            continue

        formulas = data.get("formulas", {}) or {}
        if not isinstance(formulas, dict):
            errors.append(f"{rel(path, root)}: formulas must be a mapping")
            formulas = {}
        referenced_formulas = {
            name
            for text in scalar_strings(data)
            for name in re.findall(r"\bformula\.([A-Za-z0-9_-]+)\b", text)
        }
        undefined = referenced_formulas - set(formulas)
        for name in sorted(undefined):
            errors.append(f"{rel(path, root)}: references undefined formula.{name}")

        views = data.get("views")
        if not isinstance(views, list) or not views:
            errors.append(f"{rel(path, root)}: views must be a non-empty list")
            views = []
        for index, view in enumerate(views, 1):
            if not isinstance(view, dict):
                errors.append(f"{rel(path, root)}: view {index} must be a mapping")
                continue
            legacy = legacy_view_keys & set(view)
            if legacy:
                errors.append(
                    f"{rel(path, root)}: view {index} uses legacy keys: "
                    + ", ".join(sorted(legacy))
                )
            if view.get("type") not in allowed_view_types:
                errors.append(f"{rel(path, root)}: view {index} has unsupported type")
            order = view.get("order")
            if not isinstance(order, list) or any(not isinstance(item, str) for item in order):
                errors.append(f"{rel(path, root)}: view {index} order must be a list of properties")

        mapping = BASE_TEMPLATE_MAP.get(path.name)
        if mapping is None:
            continue
        card_type, template_name = mapping
        template_data, template_error = read_frontmatter(template_root / template_name)
        if template_error or template_data is None:
            errors.append(f"{rel(path, root)}: cannot read mapped template {template_name}")
            continue
        valid_properties = set(template_data) | {
            "file.name",
            "file.basename",
            "file.path",
            "file.mtime",
            "file.ctime",
            "file.size",
        }
        configured = data.get("properties", {}) or {}
        if not isinstance(configured, dict):
            errors.append(f"{rel(path, root)}: properties must be a mapping")
            configured = {}
        used = set(configured)
        for view in views:
            if isinstance(view, dict) and isinstance(view.get("order"), list):
                used.update(item for item in view["order"] if isinstance(item, str))
        for prop in sorted(used):
            if prop.startswith("formula.") or prop in valid_properties:
                continue
            errors.append(
                f"{rel(path, root)}: property {prop!r} is not defined by {template_name}"
            )

        filter_text = "\n".join(scalar_strings(data.get("filters", {})))
        if "file.name.startsWith" in filter_text:
            errors.append(f"{rel(path, root)}: use Properties rather than filename-prefix filters")
        if not re.search(r'type\s*==\s*["\']card["\']', filter_text):
            errors.append(f"{rel(path, root)}: global filter must require type == card")
        if not re.search(
            rf'card_type\s*==\s*["\']{re.escape(card_type)}["\']', filter_text
        ):
            errors.append(
                f"{rel(path, root)}: global filter must require card_type == {card_type}"
            )


def check_canvases(root: Path, errors: list[str]) -> None:
    node_types = {"text", "file", "link", "group"}
    sides = {"top", "right", "bottom", "left"}
    ends = {"none", "arrow"}

    for path in sorted(p for p in root.rglob("*.canvas") if ".git" not in p.parts):
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            errors.append(f"{rel(path, root)}: invalid JSON Canvas: {exc}")
            continue
        if not isinstance(data, dict):
            errors.append(f"{rel(path, root)}: Canvas must be a JSON object")
            continue
        nodes = data.get("nodes", [])
        edges = data.get("edges", [])
        if not isinstance(nodes, list) or not isinstance(edges, list):
            errors.append(f"{rel(path, root)}: nodes and edges must be arrays")
            continue

        seen: set[str] = set()
        node_ids: set[str] = set()
        for index, node in enumerate(nodes, 1):
            if not isinstance(node, dict):
                errors.append(f"{rel(path, root)}: node {index} must be an object")
                continue
            node_id = node.get("id")
            if not isinstance(node_id, str) or not HEX_ID_RE.fullmatch(node_id):
                errors.append(f"{rel(path, root)}: node {index} needs a 16-character hex id")
            elif node_id in seen:
                errors.append(f"{rel(path, root)}: duplicate id {node_id}")
            else:
                seen.add(node_id)
                node_ids.add(node_id)
            node_type = node.get("type")
            if node_type not in node_types:
                errors.append(f"{rel(path, root)}: node {index} has unsupported type")
            for key in ("x", "y", "width", "height"):
                if not isinstance(node.get(key), int) or isinstance(node.get(key), bool):
                    errors.append(f"{rel(path, root)}: node {index} requires integer {key}")
            required_field = {"text": "text", "file": "file", "link": "url"}.get(node_type)
            if required_field and not isinstance(node.get(required_field), str):
                errors.append(f"{rel(path, root)}: node {index} requires {required_field}")
            if node_type == "file" and isinstance(node.get("file"), str):
                target = (root / node["file"].split("#", 1)[0]).resolve()
                try:
                    target.relative_to(root)
                except ValueError:
                    errors.append(f"{rel(path, root)}: file node escapes the Vault: {node['file']}")
                else:
                    if not target.is_file():
                        errors.append(f"{rel(path, root)}: missing file node target: {node['file']}")

        for index, edge in enumerate(edges, 1):
            if not isinstance(edge, dict):
                errors.append(f"{rel(path, root)}: edge {index} must be an object")
                continue
            edge_id = edge.get("id")
            if not isinstance(edge_id, str) or not HEX_ID_RE.fullmatch(edge_id):
                errors.append(f"{rel(path, root)}: edge {index} needs a 16-character hex id")
            elif edge_id in seen:
                errors.append(f"{rel(path, root)}: duplicate id {edge_id}")
            else:
                seen.add(edge_id)
            for key in ("fromNode", "toNode"):
                if edge.get(key) not in node_ids:
                    errors.append(f"{rel(path, root)}: edge {index} has invalid {key}")
            for key in ("fromSide", "toSide"):
                if key in edge and edge[key] not in sides:
                    errors.append(f"{rel(path, root)}: edge {index} has invalid {key}")
            for key in ("fromEnd", "toEnd"):
                if key in edge and edge[key] not in ends:
                    errors.append(f"{rel(path, root)}: edge {index} has invalid {key}")
            color = edge.get("color")
            if color is not None and not (
                color in {"1", "2", "3", "4", "5", "6"}
                or isinstance(color, str) and re.fullmatch(r"#[0-9a-fA-F]{6}", color)
            ):
                errors.append(f"{rel(path, root)}: edge {index} has invalid color")


def check_upstream_skills(root: Path, errors: list[str]) -> None:
    path = root / ".agents" / "upstream-skills.yaml"
    if not path.is_file():
        errors.append(".agents/upstream-skills.yaml is missing")
        return
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8-sig")) or {}
    except yaml.YAMLError as exc:
        errors.append(f"{rel(path, root)}: invalid YAML: {str(exc).splitlines()[0]}")
        return
    if not isinstance(data, dict):
        errors.append(f"{rel(path, root)}: manifest must be a YAML mapping")
        return
    source = data.get("source")
    if not isinstance(source, dict):
        errors.append(f"{rel(path, root)}: source must be a mapping")
    else:
        if source.get("repository") != "https://github.com/kepano/obsidian-skills":
            errors.append(f"{rel(path, root)}: unexpected upstream repository")
        if not isinstance(source.get("ref"), str) or not re.fullmatch(
            r"[0-9a-f]{40}", source.get("ref", "")
        ):
            errors.append(f"{rel(path, root)}: source.ref must pin a 40-character commit")
    skills = data.get("skills")
    if not isinstance(skills, list) or any(not isinstance(item, dict) for item in skills):
        errors.append(f"{rel(path, root)}: skills must be a list of mappings")
        return
    names: set[str] = set()
    for index, item in enumerate(skills, 1):
        name = item.get("name")
        if not isinstance(name, str):
            errors.append(f"{rel(path, root)}: skill {index} needs a string name")
            continue
        if name in names:
            errors.append(f"{rel(path, root)}: duplicate platform skill {name}")
        names.add(name)
        if item.get("requirement") not in {"required", "optional"}:
            errors.append(f"{rel(path, root)}: skill {name} has invalid requirement")
    expected = {
        "obsidian-markdown",
        "obsidian-bases",
        "json-canvas",
        "obsidian-cli",
        "defuddle",
    }
    if names != expected:
        errors.append(
            f"{rel(path, root)}: platform skill set differs: "
            f"missing={sorted(expected - names)}; extra={sorted(names - expected)}"
        )


def check_documented_counts(root: Path, errors: list[str]) -> None:
    skills = {path.parent.name for path in (root / ".agents" / "skills").glob("*/SKILL.md")}
    templates = list((root / "Templates" / "Cards").glob("*_Card.md"))
    examples = list((root / "03_Knowledge" / "00_Cards").glob("_EXAMPLE_*.md"))
    readme = (root / "README.md").read_text(encoding="utf-8-sig")
    manual = (root / "Skills_Manual.md").read_text(encoding="utf-8-sig")

    claims = (
        (readme, r"\*\*(\d+) 种(?:原子化|标准化)卡片模板\*\*", len(templates), "README card templates"),
        (
            readme,
            r"\*\*(\d+) 个(?:开箱即用的 AI 技能|Vault 工作流 Skills)",
            len(skills),
            "README skills",
        ),
        (manual, r"当前本地技能数量：(\d+) 个", len(skills), "Skills_Manual skills"),
    )
    for text, pattern, actual, label in claims:
        match = re.search(pattern, text)
        if match and int(match.group(1)) != actual:
            errors.append(f"{label} claims {match.group(1)}, actual is {actual}")

    example_claim = re.search(r"00_Cards/\s+# [^\n]*?(\d+) 张示例", readme)
    if example_claim and int(example_claim.group(1)) != len(examples):
        errors.append(
            "README directory tree example count differs from the filesystem: "
            f"examples={len(examples)}"
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
    required = (root / "agent.md", root / "System" / "Vault_Schema.md")
    if not all(path.exists() for path in required):
        raise SystemExit("Error: --vault must point to the Vault root")

    errors: list[str] = []
    warnings: list[str] = []
    check_broken_symlinks(root, errors)
    check_entrypoints(root, errors, warnings)
    check_markdown(root, errors)
    check_templates(root, errors)
    check_bases(root, errors)
    check_canvases(root, errors)
    check_upstream_skills(root, errors)
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
