#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Tuple
import fnmatch
import logging

# ----- Config -----
DEFAULT_ROOTS = ["src", "tests", "notebooks", "apps", "scripts", "docs"]
EXCLUDE_DIRS = {
    ".git", ".idea", ".vscode", ".DS_Store", "__pycache__", ".mypy_cache",
    ".pytest_cache", ".ruff_cache", ".tox", ".venv", "venv", "dist", "build",
    "coverage", "node_modules", ".next", ".turbo", "out", ".ipynb_checkpoints",
}
EXCLUDE_FILES = {".DS_Store"}
TARGET_DOC = Path("docs/references/file_structure.md")

STATUS_MAP = {
    "done": "✅", "verified": "✅",
    "wip": "🔄",
    "planned": "📝",
    "removed": "❌", "deprecated": "❌",
}
GLOB_CHARS = set("*?[]")

@dataclass
class StatusEntry:
    status: str = ""
    note: str = ""

def _normalize_key(k: str, repo_root: Path) -> str:
    # support absolute paths, ./prefixes, backslashes, trailing slashes
    try:
        p = Path(k)
        if p.is_absolute():
            try:
                k = str(p.resolve().relative_to(repo_root))
            except Exception:
                k = str(p).lstrip("/\\")
    except Exception:
        pass
    k = k.replace("\\", "/").lstrip("./")
    if k.endswith("/") and len(k) > 1:
        k = k[:-1]
    return k

def load_status_map(path: Path | None, repo_root: Path) -> tuple[dict[str, StatusEntry], list[tuple[str, StatusEntry]]]:
    """
    Returns (exact_map, glob_list). Keys in exact_map are normalized, relative, posix.
    Keys containing glob chars go into glob_list as (pattern, StatusEntry).
    """
    if not path:
        return {}, []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}, []
    except Exception:
        # Malformed JSON — ignore rather than break the pipeline.
        return {}, []

    exact: dict[str, StatusEntry] = {}
    globs: list[tuple[str, StatusEntry]] = []

    def to_entry(v) -> StatusEntry:
        if isinstance(v, str):
            return StatusEntry(status=v, note="")
        if isinstance(v, dict):
            return StatusEntry(status=v.get("status", ""), note=v.get("note", ""))
        return StatusEntry()

    for k, v in raw.items():
        entry = to_entry(v)
        norm = _normalize_key(k, repo_root)
        if any(ch in norm for ch in GLOB_CHARS):
            globs.append((norm, entry))
        else:
            exact[norm] = entry
            # Accept trailing-slash form too
            exact[norm + "/"] = entry

    return exact, globs

def _decorate(entry: StatusEntry) -> str:
    icon = STATUS_MAP.get(entry.status, entry.status if entry.status in {"✅","🔄","📝","❌"} else "")
    if icon and entry.note: return f"  {icon} {entry.note}"
    if icon: return f"  {icon}"
    if entry.note: return f"  {entry.note}"
    return ""

def status_suffix(rel_path: str, exact: dict[str, StatusEntry], globs: list[tuple[str, StatusEntry]], *, debug: bool=False) -> str:
    key = rel_path.replace("\\", "/")
    # exact match first (supports dir with/without trailing slash)
    if key in exact:
        return _decorate(exact[key])
    if key + "/" in exact:
        return _decorate(exact[key + "/"])

    # glob patterns (pick most specific = longest pattern)
    matches: list[tuple[int, StatusEntry]] = []
    for pat, entry in globs:
        if fnmatch.fnmatch(key, pat) or fnmatch.fnmatch(key + "/", pat):
            matches.append((len(pat), entry))
    if matches:
        matches.sort(key=lambda t: t[0], reverse=True)
        return _decorate(matches[0][1])

    if debug:
        logging.getLogger(__name__).debug("No status for %s", key)
    return ""

def list_entries(dir_path: Path) -> List[Tuple[str, Path, bool]]:
    try:
        names = os.listdir(dir_path)
    except FileNotFoundError:
        return []
    entries: List[Tuple[str, Path, bool]] = []
    for name in names:
        if name in EXCLUDE_FILES:
            continue
        path = dir_path / name
        if path.is_dir():
            if name in EXCLUDE_DIRS or name.startswith("."):
                continue
            entries.append((name, path, True))
        else:
            if name.startswith("."):
                continue
            entries.append((name, path, False))
    # directories first, then files; both alphabetically
    entries.sort(key=lambda t: (not t[2], t[0].lower()))
    return entries

def build_tree(root: Path, base: Path, exact: dict[str, StatusEntry], globs: list[tuple[str, StatusEntry]], debug: bool) -> List[str]:
    lines: List[str] = []

    def rec(dir_path: Path, prefix: str) -> None:
        entries = list_entries(dir_path)
        for i, (name, path, is_dir) in enumerate(entries):
            last = (i == len(entries) - 1)
            connector = "└── " if last else "├── "
            rel = path.relative_to(base).as_posix()
            suffix = status_suffix(rel, exact, globs, debug=debug)
            lines.append(f"{prefix}{connector}{name}{'/' if is_dir else ''}{suffix}")
            if is_dir:
                rec(path, prefix + ("    " if last else "│   "))

    root_rel = root.relative_to(base).as_posix()
    suffix = status_suffix(root_rel, exact, globs, debug=debug)
    lines.append(f"{root.name}/" + (f"{suffix}" if suffix else ""))
    rec(root, "")
    return lines

def generate(repo_root: Path, roots: Iterable[str], status_file: Path | None, debug: bool=False) -> str:
    exact, globs = load_status_map(status_file, repo_root)
    lines: List[str] = []
    for r in roots:
        p = repo_root / r
        if p.exists():
            lines.extend(build_tree(p, repo_root, exact, globs, debug))
            lines.append("")  # blank line between sections

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = (
        f"# Repository File Structure (generated)\n\n"
        f"_Last updated: {timestamp}_\n\n"
        "```\n"
    )
    footer = (
        "```\n\n"
        "## Status Indicators Legend\n"
        "- `✅` Implemented & verified\n"
        "- `🔄` In progress\n"
        "- `📝` Planned\n"
        "- `❌` Deprecated/removed\n"
    )
    body = "\n".join(lines).rstrip() + "\n"
    return header + body + footer

def _pick_docs_dir(repo_root: Path) -> Path:
    for candidate in ("docs/references", "doc/references"):
        d = repo_root / candidate
        if d.exists():
            return d
    return repo_root / "docs/references"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate repo directory tree into docs/references/file_structure.md")
    parser.add_argument("--root", default=".", help="Repository root (default: .)")
    parser.add_argument("--stdout", action="store_true", help="Print to stdout instead of writing the file")
    parser.add_argument("--write", action="store_true", help="Write to docs/references/file_structure.md")
    parser.add_argument("--status", default="docs/references/file_status.json",
                        help="Optional JSON mapping of path -> {status, note}")
    parser.add_argument("--include", nargs="*", default=DEFAULT_ROOTS,
                        help=f"Top-level directories to include (default: {', '.join(DEFAULT_ROOTS)})")
    parser.add_argument("--debug", action="store_true", help="Enable debug logs for status matching")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")

    repo_root = Path(args.root).resolve()
    status_file = Path(args.status).resolve() if args.status else None

    output = generate(repo_root, args.include, status_file, debug=args.debug)

    if args.stdout and not args.write:
        print(output); return

    target_dir = _pick_docs_dir(repo_root)
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "file_structure.md"
    target.write_text(output, encoding="utf-8")

    if args.stdout:
        print(output)

if __name__ == "__main__":
    main()
