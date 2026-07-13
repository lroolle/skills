#!/usr/bin/env python3
"""Convert a Logseq vault (flat pages/ with ___ namespaces, property:: syntax,
[[wikilinks]]) into an OKF bundle (directory tree, YAML frontmatter, relative
markdown .md links) so it can be consumed by any OKF tool -- including the
reference graph viewer at GoogleCloudPlatform/knowledge-catalog/okf.

Why this exists: the "Logseq variant" of a knowledge vault is NOT OKF-native.
Logseq uses `property:: value` (not YAML), `[[Page/Name]]` wikilinks (not
markdown `.md` links), and a flat `pages/` dir with `A___B___C.md` naming (not
a directory tree). The OKF viewer parses none of that -- it produces a graph of
disconnected "Unknown" nodes. This converter bridges the two formats.

Usage:
    python logseq_to_okf.py <logseq_pages_dir> <okf_out_dir>

Then view with the OKF reference viewer:
    python -m enrichment_agent visualize --bundle <okf_out_dir>
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

# Logseq property line: `- key:: value` (top-of-file block, before body content)
_PROP_RE = re.compile(r"^\s*-\s+([A-Za-z][\w-]*)::\s*(.*)$")
# Logseq wikilink: [[Namespace/Page Name]] with optional |alias
_WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
# Leading outliner marker: optional indent then `- `
_BULLET_RE = re.compile(r"^\s*-\s?")


def page_name_from_filename(filename: str) -> str:
    """Music___Composers___Bach.md -> Music/Composers/Bach (the Logseq page name)."""
    stem = filename[:-3] if filename.endswith(".md") else filename
    return stem.replace("___", "/")


def okf_path_from_page_name(page_name: str) -> str:
    """Music/Works/Bach - Brandenburg -> Music/Works/Bach_-_Brandenburg.md

    Spaces become underscores: the OKF viewer's link regex rejects whitespace
    in link targets, so paths and link hrefs must be space-free to form edges.
    """
    parts = [seg.strip().replace(" ", "_") for seg in page_name.split("/")]
    return "/".join(parts) + ".md"


def parse_page(text: str) -> tuple[dict[str, str], str]:
    """Split a Logseq page into (properties, body)."""
    lines = text.splitlines()
    props: dict[str, str] = {}
    body_start = 0
    for i, line in enumerate(lines):
        if not line.strip():
            body_start = i + 1
            continue
        m = _PROP_RE.match(line)
        if m:
            props[m.group(1)] = m.group(2).strip()
            body_start = i + 1
        else:
            body_start = i
            break
    body = "\n".join(lines[body_start:])
    return props, body


def clean_body_line(line: str) -> str:
    """Flatten one Logseq outliner line into plain markdown.

    `- ## Heading` -> `## Heading`; `  - text` -> `- text`; headings kept.
    """
    stripped = _BULLET_RE.sub("", line, count=1)
    return stripped


def yaml_escape(value: str) -> str:
    if value == "" or re.search(r"[:#\[\]{}&*!|>'\"%@`,]", value) or value != value.strip():
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def derive_description(body: str) -> str:
    """First prose paragraph, truncated -- powers OKF search/detail panels."""
    for raw in body.splitlines():
        line = clean_body_line(raw).strip()
        if not line or line.startswith("#") or line.startswith("- "):
            continue
        # strip wikilinks to bare text for the summary
        line = _WIKILINK_RE.sub(lambda m: (m.group(2) or m.group(1).split("/")[-1]), line)
        return line[:200].rstrip()
    return ""


def convert(pages_dir: Path, out_dir: Path) -> dict[str, int]:
    pages_dir = Path(pages_dir)
    out_dir = Path(out_dir)
    files = sorted(pages_dir.glob("*.md"))

    # Pass 1: build page_name -> okf_path map for link resolution.
    name_to_okf: dict[str, str] = {}
    parsed: list[tuple[str, dict[str, str], str]] = []
    for f in files:
        page_name = page_name_from_filename(f.name)
        props, body = parse_page(f.read_text(encoding="utf-8"))
        name_to_okf[page_name] = okf_path_from_page_name(page_name)
        parsed.append((page_name, props, body))

    edges = 0
    written = 0
    for page_name, props, body in parsed:
        okf_path = name_to_okf[page_name]
        src_dir = os.path.dirname(okf_path)

        def repl(m: re.Match) -> str:
            nonlocal edges
            target_page = m.group(1).strip()
            alias = m.group(2)
            display = alias or target_page.split("/")[-1]
            target_okf = name_to_okf.get(target_page)
            if target_okf is None:
                # Not-yet-written page: leave bracketed text (OKF tolerates).
                return display
            rel = os.path.relpath(target_okf, start=src_dir or ".")
            edges += 1
            return f"[{display}]({rel})"

        clean_lines = [clean_body_line(ln) for ln in body.splitlines()]
        new_body = _WIKILINK_RE.sub(repl, "\n".join(clean_lines))

        # Frontmatter
        ctype = props.get("type", "Concept").strip() or "Concept"
        title = props.get("complete-name") or props.get("title") or page_name.split("/")[-1]
        description = props.get("description") or derive_description(body)
        fm_lines = [f"type: {yaml_escape(ctype.title() if ctype.islower() else ctype)}",
                    f"title: {yaml_escape(title)}"]
        if description:
            fm_lines.append(f"description: {yaml_escape(description)}")
        # carry remaining scalar properties through as extra frontmatter
        for k, v in props.items():
            if k in ("type", "title", "complete-name", "description"):
                continue
            fm_lines.append(f"{k}: {yaml_escape(v)}")

        out_file = out_dir / okf_path
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(
            "---\n" + "\n".join(fm_lines) + "\n---\n\n" + new_body.strip() + "\n",
            encoding="utf-8",
        )
        written += 1

    return {"pages": written, "links": edges}


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2
    stats = convert(Path(argv[1]), Path(argv[2]))
    print(f"Converted {stats['pages']} pages, {stats['links']} resolved links -> {argv[2]}",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
