#!/usr/bin/env python3
"""Check the integrity and portability contract of an htmlize briefing site."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}
IDREF_ATTRIBUTES = {"aria-controls", "aria-describedby", "aria-labelledby", "for"}
TEXT_SUFFIXES = {".html", ".css", ".js", ".json", ".md", ".txt", ".dot", ".d2", ".mmd"}
UNSAFE_JS = {
    r"\.innerHTML\s*=": "assignment to innerHTML",
    r"\blocalStorage\b": "localStorage",
    r"\bsessionStorage\b": "sessionStorage",
}


@dataclass
class Anchor:
    href: str
    text_parts: list[str] = field(default_factory=list)
    aria_current: str | None = None

    @property
    def text(self) -> str:
        return " ".join(" ".join(self.text_parts).split())


class PageParser(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.path = path
        self.ids: list[str] = []
        self.idrefs: list[tuple[str, str]] = []
        self.links: list[str] = []
        self.subresources: list[tuple[str, str]] = []
        self.primary_navs: list[list[Anchor]] = []
        self._primary: list[Anchor] | None = None
        self._primary_depth = 0
        self._anchor: Anchor | None = None
        self._head_depth = 0
        self._title_depth = 0
        self._title_parts: list[str] = []
        self.title_count = 0
        self.h1_count = 0
        self.h2_without_id: list[str] = []
        self._h2_depth = 0
        self._h2_parts: list[str] = []
        self.main_count = 0
        self.main_ids: list[str] = []
        self.skip_targets: list[str] = []
        self.lang = ""
        self.description = ""
        self.body_page = ""
        self.site_names: list[str] = []
        self.site_purposes: list[str] = []
        self._site_field = ""
        self._site_parts: list[str] = []
        self.stylesheets: list[str] = []
        self.scripts: list[str] = []

    @property
    def title(self) -> str:
        return " ".join(" ".join(self._title_parts).split())

    def handle_starttag(self, tag: str, attrs_raw: list[tuple[str, str | None]]) -> None:
        attrs = {key: value or "" for key, value in attrs_raw}
        tag = tag.lower()

        classes = attrs.get("class", "").split()
        if "site-name" in classes:
            self._site_field = "name"
            self._site_parts = []
        elif "site-purpose" in classes:
            self._site_field = "purpose"
            self._site_parts = []

        element_id = attrs.get("id")
        if element_id:
            self.ids.append(element_id)
        for name in IDREF_ATTRIBUTES:
            for token in attrs.get(name, "").split():
                self.idrefs.append((name, token))

        if tag == "html":
            self.lang = attrs.get("lang", "").strip()
        elif tag == "head":
            self._head_depth += 1
        elif tag == "body":
            self.body_page = attrs.get("data-page", "").strip()
        elif tag == "title" and self._head_depth:
            self.title_count += 1
            self._title_depth += 1
        elif tag == "meta" and attrs.get("name", "").lower() == "description":
            self.description = attrs.get("content", "").strip()
        elif tag == "main":
            self.main_count += 1
            self.main_ids.append(attrs.get("id", ""))
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "h2":
            self._h2_depth += 1
            self._h2_parts = []
            if not element_id:
                self.h2_without_id.append("")

        if tag == "nav" and attrs.get("aria-label", "").lower() == "primary":
            self._primary = []
            self._primary_depth = 1
        elif self._primary is not None and tag == "nav":
            self._primary_depth += 1

        if tag == "a":
            href = attrs.get("href", "").strip()
            if href:
                self.links.append(href)
            if "skip-link" in attrs.get("class", "").split():
                self.skip_targets.append(href)
            if self._primary is not None:
                self._anchor = Anchor(href=href, aria_current=attrs.get("aria-current") or None)

        if tag == "script" and attrs.get("src"):
            src = attrs["src"].strip()
            self.scripts.append(src)
            self.subresources.append(("script", src))
        elif tag == "link" and "stylesheet" in attrs.get("rel", "").lower().split():
            href = attrs.get("href", "").strip()
            self.stylesheets.append(href)
            self.subresources.append(("stylesheet", href))
        elif tag in {"img", "source", "audio", "video", "iframe", "embed"} and attrs.get("src"):
            self.subresources.append((tag, attrs["src"].strip()))
        elif tag == "video" and attrs.get("poster"):
            self.subresources.append(("video poster", attrs["poster"].strip()))
        elif tag == "object" and attrs.get("data"):
            self.subresources.append(("object", attrs["data"].strip()))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in VOID_ELEMENTS:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "head" and self._head_depth:
            self._head_depth -= 1
        elif tag == "title" and self._title_depth:
            self._title_depth -= 1
        elif tag == "h2" and self._h2_depth:
            if self.h2_without_id and self.h2_without_id[-1] == "":
                self.h2_without_id[-1] = " ".join(" ".join(self._h2_parts).split()) or "(empty h2)"
            self._h2_depth -= 1
        elif tag == "a" and self._anchor is not None:
            assert self._primary is not None
            self._primary.append(self._anchor)
            self._anchor = None
        elif tag == "nav" and self._primary is not None:
            self._primary_depth -= 1
            if self._primary_depth == 0:
                self.primary_navs.append(self._primary)
                self._primary = None
        if tag == "span" and self._site_field:
            value = " ".join(" ".join(self._site_parts).split())
            if self._site_field == "name":
                self.site_names.append(value)
            else:
                self.site_purposes.append(value)
            self._site_field = ""
            self._site_parts = []

    def handle_data(self, data: str) -> None:
        if self._title_depth:
            self._title_parts.append(data)
        if self._h2_depth:
            self._h2_parts.append(data)
        if self._anchor is not None:
            self._anchor.text_parts.append(data)
        if self._site_field:
            self._site_parts.append(data)


def inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


def local_target(root: Path, page: Path, url: str) -> tuple[Path | None, str, str | None]:
    """Return target, fragment, error. External URLs return (None, fragment, None)."""
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or url.startswith("//"):
        return None, parsed.fragment, None
    if parsed.path.startswith("/"):
        return None, parsed.fragment, "root-relative URL is not portable"
    raw_path = unquote(parsed.path)
    target = page if not raw_path else page.parent / raw_path
    target = target.resolve()
    if not inside(root, target):
        return None, parsed.fragment, "URL escapes the site bundle"
    if target.is_dir():
        target = target / "index.html"
    return target, parsed.fragment, None


def parse_page(path: Path, errors: list[str]) -> PageParser:
    parser = PageParser(path)
    try:
        parser.feed(path.read_text(encoding="utf-8"))
        parser.close()
    except (OSError, UnicodeError) as exc:
        errors.append(f"{path.name}: cannot read HTML: {exc}")
    return parser


def check_text_files(root: Path, allow_slots: bool, errors: list[str]) -> None:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{path.relative_to(root)}: cannot read text: {exc}")
            continue
        label = path.relative_to(root)
        if not allow_slots and "SLOT:" in text:
            errors.append(f"{label}: unfinished SLOT marker")
        if re.search(r"\blorem\s+ipsum\b", text, re.IGNORECASE):
            errors.append(f"{label}: lorem ipsum placeholder")
        if path.suffix.lower() == ".js":
            for pattern, name in UNSAFE_JS.items():
                if re.search(pattern, text):
                    errors.append(f"{label}: unsafe browser API ({name})")
            if re.search(r"\bfetch\s*\(", text):
                errors.append(f"{label}: runtime fetch makes local-file behavior unreliable")
        if path.suffix.lower() == ".css":
            if re.search(r"@import\b", text, re.IGNORECASE):
                errors.append(f"{label}: CSS @import is an external dependency seam")
            if re.search(r"url\(\s*['\"]?(?:https?:)?//", text, re.IGNORECASE):
                errors.append(f"{label}: external CSS resource")


def load_manifest(root: Path, allow_slots: bool, errors: list[str]) -> dict:
    path = root / "site.json"
    if not path.is_file():
        errors.append("site.json: missing canonical site map")
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"site.json: invalid JSON: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append("site.json: root must be an object")
        return {}
    for key in ("title", "purpose", "source"):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"site.json: {key} must be a non-empty string")
        elif not allow_slots and "SLOT:" in value:
            errors.append(f"site.json: unfinished {key}")
    pages = data.get("pages")
    if not isinstance(pages, list):
        errors.append("site.json: pages must be a list")
        data["pages"] = []
        return data
    if not 3 <= len(pages) <= 7:
        errors.append(f"site.json: site mode requires 3-7 primary pages, found {len(pages)}")
    seen: set[str] = set()
    seen_labels: set[str] = set()
    for index, item in enumerate(pages, 1):
        if not isinstance(item, dict):
            errors.append(f"site.json: page {index} must be an object")
            continue
        for key in ("file", "label", "question"):
            value = item.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"site.json: page {index} {key} must be a non-empty string")
        filename = item.get("file", "")
        if isinstance(filename, str) and filename:
            candidate = Path(filename)
            if candidate.name != filename or candidate.suffix.lower() != ".html":
                errors.append(f"site.json: page file must be a flat .html filename: {filename}")
            if filename in seen:
                errors.append(f"site.json: duplicate page file: {filename}")
            seen.add(filename)
        label = item.get("label", "")
        if isinstance(label, str) and label:
            if label in seen_labels:
                errors.append(f"site.json: duplicate page label: {label}")
            seen_labels.add(label)
    return data


def main() -> int:
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument("site", type=Path, help="briefing site directory")
    argp.add_argument("--allow-slots", action="store_true", help="validate the bundled template before content is filled")
    args = argp.parse_args()

    root = args.site.resolve()
    errors: list[str] = []
    if not root.is_dir():
        print(f"site check failed: not a directory: {args.site}", file=sys.stderr)
        return 1

    manifest = load_manifest(root, args.allow_slots, errors)
    check_text_files(root, args.allow_slots, errors)
    manifest_pages = [item for item in manifest.get("pages", []) if isinstance(item, dict)]
    expected_files = [item.get("file", "") for item in manifest_pages if isinstance(item.get("file"), str)]
    expected_set = {name for name in expected_files if name}

    if "index.html" not in expected_set:
        errors.append("site.json: pages must include index.html")
    actual_set = {path.name for path in root.glob("*.html") if path.is_file()}
    if actual_set != expected_set:
        missing = sorted(expected_set - actual_set)
        extra = sorted(actual_set - expected_set)
        if missing:
            errors.append("site.json: missing page files: " + ", ".join(missing))
        if extra:
            errors.append("site.json: unregistered root HTML files: " + ", ".join(extra))

    source_value = manifest.get("source", "")
    if isinstance(source_value, str) and source_value:
        source = (root / source_value).resolve()
        if not inside(root, source):
            errors.append("site.json: source escapes the site bundle")
        elif not source.is_file():
            errors.append(f"site.json: source does not exist: {source_value}")

    for asset in (
        root / "assets/site.css",
        root / "assets/diagram-viewer.js",
        root / "assets/site.js",
    ):
        if not asset.is_file():
            errors.append(f"{asset.relative_to(root)}: missing shared site asset")

    parsers: dict[Path, PageParser] = {}
    for name in sorted(actual_set):
        page = (root / name).resolve()
        parsers[page] = parse_page(page, errors)

    manifest_nav = [(item.get("file", ""), item.get("label", "")) for item in manifest_pages]
    manifest_title = manifest.get("title", "")
    manifest_purpose = manifest.get("purpose", "")
    fragment_parsers = dict(parsers)

    for page, parser in parsers.items():
        label = page.name
        if not parser.lang:
            errors.append(f"{label}: html element needs a lang attribute")
        if parser.title_count != 1 or not parser.title:
            errors.append(f"{label}: expected exactly one non-empty title")
        elif isinstance(manifest_title, str) and manifest_title not in parser.title:
            errors.append(f"{label}: document title does not include site.json title")
        if not parser.description:
            errors.append(f"{label}: missing meta description")
        if parser.h1_count != 1:
            errors.append(f"{label}: expected exactly one h1, found {parser.h1_count}")
        if parser.main_count != 1 or parser.main_ids != ["main"]:
            errors.append(f"{label}: expected exactly one <main id=\"main\">")
        if "#main" not in parser.skip_targets:
            errors.append(f"{label}: missing skip link to #main")
        if parser.body_page != label:
            errors.append(f"{label}: body data-page must equal {label}")
        if parser.site_names != [manifest_title]:
            errors.append(f"{label}: site-name must match site.json title exactly once")
        if parser.site_purposes != [manifest_purpose]:
            errors.append(f"{label}: site-purpose must match site.json purpose exactly once")
        if parser.h2_without_id:
            errors.append(f"{label}: h2 headings need stable IDs: {', '.join(parser.h2_without_id)}")
        duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
        if duplicates:
            errors.append(f"{label}: duplicate DOM IDs: {', '.join(duplicates)}")
        id_set = set(parser.ids)
        for attr, token in parser.idrefs:
            if token not in id_set:
                errors.append(f"{label}: {attr} references missing ID: {token}")

        if len(parser.primary_navs) != 1:
            errors.append(f"{label}: expected one primary nav, found {len(parser.primary_navs)}")
        else:
            nav = parser.primary_navs[0]
            actual_nav = [(anchor.href.removeprefix("./"), anchor.text) for anchor in nav]
            if actual_nav != manifest_nav:
                errors.append(f"{label}: primary nav does not match site.json page order and labels")
            current = [anchor for anchor in nav if anchor.aria_current == "page"]
            if len(current) != 1 or current[0].href.removeprefix("./") != label:
                errors.append(f"{label}: aria-current must mark this page exactly once")

        if "assets/site.css" not in parser.stylesheets:
            errors.append(f"{label}: must use shared assets/site.css")
        if "assets/diagram-viewer.js" not in parser.scripts:
            errors.append(f"{label}: must use shared assets/diagram-viewer.js")
        if "assets/site.js" not in parser.scripts:
            errors.append(f"{label}: must use shared assets/site.js")

        for kind, url in parser.subresources:
            parsed = urlsplit(url)
            if parsed.scheme == "data":
                continue
            if parsed.scheme or parsed.netloc or url.startswith("//"):
                errors.append(f"{label}: external {kind} resource: {url}")
                continue
            target, _, problem = local_target(root, page, url)
            if problem:
                errors.append(f"{label}: {problem}: {url}")
            elif target is not None and not target.exists():
                errors.append(f"{label}: broken local {kind} resource: {url}")

        for href in parser.links:
            parsed = urlsplit(href)
            if parsed.scheme.lower() == "javascript":
                errors.append(f"{label}: javascript URL is not an accessible link: {href}")
                continue
            if parsed.scheme.lower() == "file":
                errors.append(f"{label}: file URL exposes a machine-local path: {href}")
                continue
            target, fragment, problem = local_target(root, page, href)
            if problem:
                errors.append(f"{label}: {problem}: {href}")
                continue
            if target is None:
                continue
            if not target.exists():
                errors.append(f"{label}: broken local link: {href}")
                continue
            if fragment and target.suffix.lower() == ".html":
                target_parser = fragment_parsers.get(target)
                if target_parser is None:
                    target_parser = parse_page(target, errors)
                    fragment_parsers[target] = target_parser
                if unquote(fragment) not in set(target_parser.ids):
                    errors.append(f"{label}: broken fragment link: {href}")

    if errors:
        print(f"site check failed ({len(errors)} issue{'s' if len(errors) != 1 else ''}):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"site check: ok ({len(actual_set)} pages, {sum(len(p.ids) for p in parsers.values())} IDs, "
        f"{sum(len(p.links) for p in parsers.values())} links)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
