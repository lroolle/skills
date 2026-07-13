#!/usr/bin/env python3
"""llms_txt_check.py -- validate an llms.txt map and detect drift.

Stdlib only. Usage:
    llms_txt_check.py <llms.txt> [--root DIR] [--verbose]

--root DIR resolves local links against DIR and reports entry-point
files under DIR that the map misses (drift; entry points are files
named README.md, SKILL.md, or index.md, files directly under DIR,
and files under a docs/ directory). Remote http(s) links are checked
for shape, not fetched; raw.githubusercontent.com URLs are mapped
back to repo paths for existence and drift checks.

Exit codes: 0 clean (warnings allowed), 1 errors found, 2 bad usage.
"""

import argparse
import os
import re
import sys

ENTRY = re.compile(r"^\s*[-*]\s*\[([^\]]+)\]\(([^)\s]+)\)\s*(?:[:\-]\s*(.*))?$")
RAW_GH = re.compile(r"^https://raw\.githubusercontent\.com/[^/]+/[^/]+/[^/]+/(.+)$")
SKIP_DIRS = {".git", ".github", ".agents", "node_modules", "reference",
             "archived", "vendor", "dist", "build"}


def is_entry_point(rel):
    base = os.path.basename(rel)
    if base in ("README.md", "SKILL.md", "index.md"):
        return True
    parts = rel.split(os.sep)
    return len(parts) == 1 or "docs" in parts[:-1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--root", default=None)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    if not os.path.isfile(args.file):
        sys.exit(2)
    with open(args.file, encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()

    errors, warnings, infos = [], [], []
    h1s = [i for i, l in enumerate(lines) if re.match(r"^#\s+\S", l)]
    if not h1s:
        errors.append("no H1 title")
    else:
        if h1s[0] != next((i for i, l in enumerate(lines) if l.strip()), 0):
            errors.append(f"line {h1s[0]+1}: H1 is not the first content line")
        for i in h1s[1:]:
            errors.append(f"line {i+1}: second H1 -- one file, one title")
        after = next((l for l in lines[h1s[0]+1:] if l.strip()), "")
        if not after.startswith(">"):
            warnings.append("no blockquote summary directly after the H1")

    sections, entries = [], []
    current = None
    for i, l in enumerate(lines):
        if l.startswith("## "):
            current = l[3:].strip()
            sections.append(current)
            continue
        m = ENTRY.match(l)
        if m:
            title, target, desc = m.group(1), m.group(2), m.group(3)
            entries.append((i + 1, current, title, target, desc))
            if not (desc or "").strip():
                infos.append(f"line {i+1}: entry '{title}' has no description")

    if not sections:
        warnings.append("no H2 sections -- a map with no sections is a README")

    seen = {}
    local_targets = set()
    for ln, _sec, title, target, _desc in entries:
        if target in seen:
            warnings.append(f"line {ln}: duplicate target {target} (also line {seen[target]})")
        seen.setdefault(target, ln)
        if target.startswith(("http://", "https://")):
            if target.startswith("http://"):
                infos.append(f"line {ln}: http (not https) link {target}")
            m = RAW_GH.match(target)
            if m:
                local_targets.add(m.group(1))
        elif target.startswith(("mailto:", "#")):
            pass
        else:
            local_targets.add(target.lstrip("/").split("#")[0])

    if args.root:
        root = os.path.abspath(args.root)
        if not os.path.isdir(root):
            sys.exit(2)
        for t in sorted(local_targets):
            if t.endswith("/"):
                if not os.path.isdir(os.path.join(root, t)):
                    errors.append(f"map lists missing directory: {t}")
            elif not os.path.isfile(os.path.join(root, t)):
                errors.append(f"map lists missing file: {t}")
        unmapped = []
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames
                           if d not in SKIP_DIRS and not d.startswith(".")]
            for fn in filenames:
                if not fn.endswith(".md"):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, fn), root)
                if rel not in local_targets and is_entry_point(rel):
                    unmapped.append(rel)
        shown = unmapped if args.verbose else unmapped[:15]
        for rel in shown:
            infos.append(f"entry point not in map: {rel}")
        if len(unmapped) > len(shown):
            infos.append(f"...and {len(unmapped) - len(shown)} more unmapped (--verbose)")

    for label, items in (("ERROR", errors), ("WARN", warnings), ("INFO", infos)):
        for line in items:
            print(f"{label}: {line}")
    print(f"\n{len(entries)} entries in {len(sections)} section(s) | "
          f"{len(errors)} errors, {len(warnings)} warnings, {len(infos)} info")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
