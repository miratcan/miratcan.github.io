#!/usr/bin/env python3
"""
Utility to scrub non-ASCII characters from content files.

The script walks the content tree (or a user-supplied directory), replaces
common Unicode characters with ASCII-friendly equivalents, and falls back to
Unicode decomposition for the rest. Files are only rewritten when the cleaned
version differs, and a short report lists the files that were touched.
"""

from __future__ import annotations

import argparse
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, Tuple

# Extensions treated as text sources by default.
DEFAULT_EXTENSIONS = {".lr", ".md", ".html", ".txt", ".rst"}

# Explicit replacements take precedence over generic Unicode decomposition.
CHAR_REPLACEMENTS: Dict[str, str] = {
    # Quotes and apostrophes
    "‘": "'",
    "’": "'",
    "‚": "'",
    "‛": "'",
    "“": '"',
    "”": '"',
    "„": '"',
    "«": '"',
    "»": '"',
    # Dashes, hyphens, ellipsis
    "—": "--",
    "–": "-",
    "−": "-",
    "‑": "-",
    "‒": "-",
    "…": "...",
    # Bullets and similar symbols
    "•": "*",
    "·": "*",
    "●": "*",
    "○": "o",
    # Spaces
    "\u00a0": " ",  # non-breaking space
    "\u2009": " ",
    "\u200a": " ",
    "\u200b": "",  # zero-width space
    "\u202f": " ",
    "\u205f": " ",
    # Arrows and math symbols
    "→": "->",
    "←": "<-",
    "↔": "<->",
    "⇒": "=>",
    "×": "x",
    "÷": "/",
    "✓": "OK",
    # Emoji and pictographs (keep short ASCII hints)
    "🙂": ":)",
    "😅": ":)",
    "😏": ";)",
    "🐍": ":snake:",
    "💡": "(idea)",
    "🔹": "*",
    # Turkish alphabet specifics
    "Ç": "C",
    "Ö": "O",
    "Ü": "U",
    "Ğ": "G",
    "İ": "I",
    "Ş": "S",
    "ç": "c",
    "ö": "o",
    "ü": "u",
    "ğ": "g",
    "ı": "i",
    "ş": "s",
}


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Replace non-ASCII characters in content files."
    )
    parser.add_argument(
        "root",
        nargs="?",
        default="content",
        help="Root directory to scan (default: content)",
    )
    parser.add_argument(
        "--ext",
        action="append",
        dest="extensions",
        help=(
            "File extension to include (e.g., --ext .txt). "
            "May be passed multiple times. "
            "Defaults to .lr, .md, .html, .txt, .rst."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Scan and report changes without rewriting files.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress per-file logs; useful when only the exit status matters.",
    )
    return parser.parse_args(list(argv))


def build_extension_set(args: argparse.Namespace) -> set[str]:
    if args.extensions:
        return {ext if ext.startswith(".") else f".{ext}" for ext in args.extensions}
    return DEFAULT_EXTENSIONS.copy()


def clean_text(text: str) -> Tuple[str, Counter]:
    """
    Replace non-ASCII characters with ASCII equivalents.

    Returns the cleaned text and a Counter detailing which characters changed.
    """
    replacements = Counter()
    out_fragments = []

    for ch in text:
        if ord(ch) < 128:
            out_fragments.append(ch)
            continue

        if ch in CHAR_REPLACEMENTS:
            replacement = CHAR_REPLACEMENTS[ch]
        else:
            normalized = unicodedata.normalize("NFKD", ch)
            replacement = normalized.encode("ascii", "ignore").decode("ascii")

        if replacement != ch:
            replacements[ch] += 1

        out_fragments.append(replacement)

    return "".join(out_fragments), replacements


def iter_files(root: Path, extensions: set[str]) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if extensions and path.suffix.lower() not in extensions:
            continue
        yield path


def main(argv: Iterable[str]) -> int:
    args = parse_args(argv)
    root = Path(args.root)

    if not root.exists():
        print(f"Error: {root} does not exist.", file=sys.stderr)
        return 2

    extensions = build_extension_set(args)
    edited = []
    all_changes = defaultdict(Counter)

    for path in iter_files(root, extensions):
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            # Skip files that are not UTF-8 decodable.
            continue

        cleaned, changes = clean_text(text)
        if not changes:
            continue

        edited.append(path)
        all_changes[path].update(changes)

        if not args.dry_run:
            path.write_text(cleaned)

        if not args.quiet:
            replaced = ", ".join(
                f"{repr(char)}×{count}" for char, count in sorted(changes.items())
            )
            marker = "[DRY]" if args.dry_run else "[WRITE]"
            print(f"{marker} {path}: {replaced}")

    if not edited and not args.quiet:
        print("No non-ASCII characters found.")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
