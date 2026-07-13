#!/usr/bin/env python3
"""vault_lint.py -- lint a knowledge vault and generate its review queue.

Stdlib only. Usage:
    vault_lint.py <vault-dir> [--format yaml|logseq|auto] [--queue-out PATH]
                  [--no-queue] [--verbose]

Exit codes: 0 clean (warnings allowed), 1 errors found, 2 bad invocation.
"""

import argparse
import datetime
import os
import re
import sys
from collections import defaultdict

RESERVED = {"agents.md", "readme.md", "review.md", "log.md", "llms.txt",
            "schema.md", "contents.md", "claude.md"}
SKIP_DIRS = {".git", ".logseq", "logseq", "journals", "reference",
             ".reference", "assets", "node_modules"}

CRED_PATTERNS = [
    re.compile(r"(?i)\b(api[_-]?key|secret|token|passwd|password)\b\s*[:=]{1,2}\s*['\"]?[A-Za-z0-9_\-/+]{16,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bghp_[A-Za-z0-9]{36}\b"),
    re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]

STALE_DAYS = {"hot": 30, "warm": 90, "cold": 365, "frozen": None}
ORIGINS = {"data", "editorial", "human"}


class Page:
    def __init__(self, path, rel, name):
        self.path = path
        self.rel = rel            # path relative to vault root
        self.name = name          # canonical id: rel minus .md, ___ -> /
        self.props = {}
        self.body = ""
        self.raw = ""
        self.is_hub = False
        self.outgoing = set()
        self.incoming = 0
        self.editorial_marks = 0


def parse_yaml_frontmatter(text):
    props, body = {}, text
    if text.startswith("---"):
        parts = text.split("\n---", 2)
        if len(parts) >= 2:
            for line in parts[0].splitlines()[1:]:
                m = re.match(r"^([A-Za-z0-9_-]+)\s*:\s*(.*)$", line)
                if m:
                    props[m.group(1).strip().lower()] = m.group(2).strip()
            body = parts[1]
            if len(parts) == 3:
                body += parts[2]
    return props, body


def parse_logseq_props(text):
    props, body_lines = {}, []
    in_props = True
    for line in text.splitlines():
        m = re.match(r"^\s*-?\s*([A-Za-z0-9_-]+)::\s*(.*)$", line) if in_props else None
        if m:
            props[m.group(1).strip().lower()] = m.group(2).strip()
        else:
            if line.strip():
                in_props = False
            body_lines.append(line)
    return props, "\n".join(body_lines)


def detect_format(root):
    pages_dir = os.path.join(root, "pages")
    if os.path.isdir(pages_dir):
        for f in os.listdir(pages_dir):
            if "___" in f or f.endswith(".md"):
                return "logseq"
    return "yaml"


def collect_pages(root, fmt):
    pages = []
    if fmt == "logseq":
        pages_dir = os.path.join(root, "pages")
        if not os.path.isdir(pages_dir):
            sys.exit("no pages/ directory in logseq vault: " + root)
        for fn in sorted(os.listdir(pages_dir)):
            if not fn.endswith(".md") or fn.lower() in RESERVED:
                continue
            path = os.path.join(pages_dir, fn)
            name = fn[:-3].replace("___", "/")
            pages.append(Page(path, os.path.join("pages", fn), name))
    else:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fn in sorted(filenames):
                if not fn.endswith(".md"):
                    continue
                rel = os.path.relpath(os.path.join(dirpath, fn), root)
                if fn.lower() in RESERVED and os.path.dirname(rel) == "":
                    continue
                pages.append(Page(os.path.join(dirpath, fn), rel, rel[:-3]))
    return pages


def load(page, fmt):
    with open(page.path, encoding="utf-8", errors="replace") as f:
        page.raw = f.read()
    parser = parse_logseq_props if fmt == "logseq" else parse_yaml_frontmatter
    page.props, page.body = parser(page.raw)
    base = os.path.basename(page.rel).lower()
    page.is_hub = (page.props.get("type") == "hub" or base == "index.md")
    if fmt == "logseq" and "/" in page.name:
        # namespace page with children acts as hub; resolved later
        pass
    page.editorial_marks = page.raw.count("(editorial)")
    for m in re.finditer(r"\[\[([^\]|#]+?)(?:\|[^\]]*)?\]\]", page.raw):
        page.outgoing.add(m.group(1).strip())
    for m in re.finditer(r"\]\(([^)]+\.md)(?:#[^)]*)?\)", page.raw):
        target = m.group(1)
        if not target.startswith(("http://", "https://")):
            joined = os.path.normpath(os.path.join(os.path.dirname(page.rel), target))
            page.outgoing.add(joined[:-3].replace("___", "/"))


def build_index(pages):
    idx = {}
    for p in pages:
        keys = {p.name.lower(), os.path.basename(p.name).lower()}
        title = p.props.get("title")
        if title:
            keys.add(title.lower())
        aliases = p.props.get("aliases", "")
        for a in re.split(r"[,\[\]]", aliases):
            if a.strip():
                keys.add(a.strip().lower())
        for k in keys:
            idx.setdefault(k, p)
    return idx


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vault")
    ap.add_argument("--format", choices=["yaml", "logseq", "auto"], default="auto")
    ap.add_argument("--queue-out", default=None)
    ap.add_argument("--no-queue", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    root = os.path.abspath(args.vault)
    if not os.path.isdir(root):
        sys.exit(2)
    fmt = detect_format(root) if args.format == "auto" else args.format

    pages = collect_pages(root, fmt)
    for p in pages:
        load(p, fmt)
    idx = build_index(pages)

    # resolve incoming links; namespace parents count as hubs in logseq
    children = defaultdict(list)
    for p in pages:
        if "/" in p.name:
            children[p.name.rsplit("/", 1)[0]].append(p)
    for p in pages:
        if fmt == "logseq" and children.get(p.name):
            p.is_hub = True
        for target in p.outgoing:
            hit = idx.get(target.lower())
            if hit and hit is not p:
                hit.incoming += 1

    errors, warnings, infos = [], [], []
    today = datetime.date.today()
    titles = defaultdict(list)

    for p in pages:
        loc = p.rel
        if p.is_hub:
            if fmt == "yaml" and os.path.basename(p.rel) == "index.md" and p.props:
                infos.append(f"{loc}: index.md carries frontmatter (rule 10)")
            listed = {t.lower() for t in p.outgoing}
            for c in children.get(p.name if fmt == "logseq" else os.path.dirname(p.rel), []):
                names = {c.name.lower(), os.path.basename(c.name).lower()}
                if not (names & listed) and not c.is_hub:
                    warnings.append(f"{loc}: hub missing child '{c.name}' (rule 6)")
            continue

        if "type" not in p.props:
            errors.append(f"{loc}: missing 'type' (rule 1)")
        origin = p.props.get("origin")
        if origin is None:
            errors.append(f"{loc}: missing 'origin' (rule 2)")
        elif origin not in ORIGINS:
            errors.append(f"{loc}: invalid origin '{origin}' (rule 2)")
        if origin == "editorial" and "reviewed" not in p.props:
            errors.append(f"{loc}: editorial page missing 'reviewed' (rule 3, fix: reviewed: false)")

        for pat in CRED_PATTERNS:
            if pat.search(p.raw):
                errors.append(f"{loc}: credential-like pattern (rule 4) -- remove and rotate")
                break

        for target in sorted(p.outgoing):
            if target.lower() not in idx:
                warnings.append(f"{loc}: broken link '{target}' (rule 5)")

        if p.incoming == 0:
            warnings.append(f"{loc}: orphan -- no incoming links (rule 7)")
        if not p.body.strip():
            warnings.append(f"{loc}: empty body (rule 8)")
        body_lines = len(p.body.splitlines())
        if body_lines > 200:
            warnings.append(f"{loc}: body {body_lines} lines, split past ~200 (rule 12)")
        if str(p.props.get("contested", "")).lower() == "true":
            infos.append(f"{loc}: contested -- unresolved contradiction awaits a human (rule 13)")

        t = (p.props.get("title") or os.path.basename(p.name)).lower()
        titles[t].append(p.rel)

        vol = p.props.get("volatility", "cold")
        horizon = STALE_DAYS.get(vol, 365)
        stamp = p.props.get("updated") or p.props.get("timestamp") or p.props.get("created")
        if horizon and stamp:
            m = re.match(r"(\d{4})-(\d{2})-(\d{2})", str(stamp))
            if m:
                age = (today - datetime.date(*map(int, m.groups()))).days
                if age > horizon:
                    infos.append(f"{loc}: stale -- {age}d old, {vol} horizon {horizon}d (rule 11)")

    for t, locs in titles.items():
        if len(locs) > 1:
            warnings.append(f"duplicate title '{t}': {', '.join(locs)} (rule 9)")

    # review queue: unreviewed non-data pages; contested first, then gravity
    queue = [p for p in pages if not p.is_hub
             and p.props.get("origin") not in ("data", "human")
             and str(p.props.get("reviewed", "false")).lower() != "true"]
    queue.sort(key=lambda p: (
        -(str(p.props.get("contested", "")).lower() == "true"),
        -p.incoming, -p.editorial_marks, p.name))

    # WIP limit declared in the vault's AGENTS.md (rule 14)
    agents_md = os.path.join(root, "AGENTS.md")
    if os.path.isfile(agents_md):
        with open(agents_md, encoding="utf-8", errors="replace") as f:
            m = re.search(r"WIP limit:\s*(\d+)", f.read())
        if m and len(queue) > int(m.group(1)):
            warnings.append(f"queue {len(queue)} exceeds WIP limit {m.group(1)} "
                            f"(rule 14) -- stop editorial writing, work the queue")

    if not args.no_queue:
        out = args.queue_out or os.path.join(root, "review.md")
        with open(out, "w", encoding="utf-8") as f:
            f.write("# Review Queue\n\n")
            f.write(f"Generated by vault_lint.py -- {len(queue)} page(s) awaiting review, "
                    f"est. {max(1, len(queue) // 2)} min. Do not hand-edit; regenerate.\n\n")
            for p in queue[:50]:
                desc = p.props.get("description", "(no description)")
                f.write(f"- [ ] **{p.props.get('title', os.path.basename(p.name))}** "
                        f"({p.name}) -- {desc} -- {p.editorial_marks} unsourced claim(s), "
                        f"{p.incoming} incoming link(s)\n")
            if len(queue) > 50:
                f.write(f"\n...and {len(queue) - 50} more. Work the top; regenerate after promotions.\n")
        print(f"queue: {len(queue)} unreviewed page(s) -> {out}")

    for label, items in (("ERROR", errors), ("WARN", warnings), ("INFO", infos)):
        shown = items if (args.verbose or label == "ERROR") else items[:15]
        for line in shown:
            print(f"{label}: {line}")
        if len(items) > len(shown):
            print(f"{label}: ...and {len(items) - len(shown)} more (--verbose to see all)")

    print(f"\n{len(pages)} pages | {len(errors)} errors, {len(warnings)} warnings, "
          f"{len(infos)} info | format={fmt}")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
