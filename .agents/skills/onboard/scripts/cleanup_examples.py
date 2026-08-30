#!/usr/bin/env python3
"""Cross-platform, confirmation-gated cleanup helper for /onboard."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


EXAMPLE_ROOTS = (
    Path("01_Daily"),
    Path("03_Knowledge/00_Cards"),
    Path("03_Knowledge/01_Topics"),
    Path("04_References/01_Inbox"),
)
README_CANDIDATES = (
    Path("README.md"),
    Path("02_Projects/README.md"),
    Path("03_Knowledge/00_Cards/README.md"),
    Path("03_Knowledge/01_Topics/README.md"),
)
PROJECT_EXAMPLE = Path("02_Projects/_Example_Project")


def ensure_vault_root(root: Path) -> None:
    required = (root / "AGENTS.md", root / "Templates/Cards")
    if not all(path.exists() for path in required):
        raise SystemExit("Error: run this helper from the Vault root directory.")


def within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def find_examples(root: Path) -> list[Path]:
    targets: list[Path] = []
    for relative_root in EXAMPLE_ROOTS:
        base = root / relative_root
        if not base.is_dir():
            continue
        for target in base.rglob("_EXAMPLE_*"):
            if within(target, base):
                targets.append(target)
    project = root / PROJECT_EXAMPLE
    if project.is_dir():
        targets.append(project)
    return sorted(set(targets), key=lambda path: path.as_posix())


def find_readmes(root: Path) -> list[Path]:
    targets = []
    for relative in README_CANDIDATES:
        path = root / relative
        if path.is_file() and ("_EXAMPLE_" in path.read_text(encoding="utf-8-sig") or "_Example_Project" in path.read_text(encoding="utf-8-sig")):
            targets.append(path)
    return targets


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def print_targets(examples: list[Path], readmes: list[Path], root: Path) -> None:
    for target in examples:
        print(f"DELETE={rel(target, root)}")
    for target in readmes:
        print(f"UPDATE={rel(target, root)}")
    print(f"EXAMPLE_TOTAL={len(examples)}")
    print(f"README_TOTAL={len(readmes)}")
    print(f"TOTAL={len(examples) + len(readmes)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--list", action="store_true")
    mode.add_argument("--clean", action="store_true")
    parser.add_argument("--yes", action="store_true", help="Required with --clean after explicit user confirmation.")
    args = parser.parse_args()

    root = Path.cwd().resolve()
    ensure_vault_root(root)
    examples = find_examples(root)
    readmes = find_readmes(root)

    if args.list:
        print_targets(examples, readmes, root)
        return
    if not args.yes:
        raise SystemExit("Error: cleanup requires prior user confirmation and the --yes flag.")

    removed = 0
    for target in examples:
        if not any(within(target, root / allowed) for allowed in EXAMPLE_ROOTS) and target != root / PROJECT_EXAMPLE:
            raise SystemExit(f"Refusing out-of-scope target: {target}")
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists():
            target.unlink()
        else:
            continue
        removed += 1
        print(f"REMOVED={rel(target, root)}")

    readme_script = Path(__file__).with_name("cleanup_readme_refs.py")
    if readmes:
        subprocess.run([sys.executable, str(readme_script)], cwd=root, check=True)

    remaining_examples = find_examples(root)
    remaining_readmes = find_readmes(root)
    print(
        "SUMMARY "
        f"examples_found={len(examples)} examples_removed={removed} "
        f"examples_remaining={len(remaining_examples)} "
        f"readmes_updated={len(readmes)} readmes_remaining={len(remaining_readmes)}"
    )
    if remaining_examples or remaining_readmes:
        print_targets(remaining_examples, remaining_readmes, root)
        raise SystemExit("Error: example files or related README references remain after cleanup.")


if __name__ == "__main__":
    main()
