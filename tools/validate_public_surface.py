#!/usr/bin/env python3
"""Deterministic validation for HYDRA's recruiter-facing public surface."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_PATHS = (
    "README.md",
    "index.html",
    "architecture.html",
    "constraint.html",
    "case-study.html",
    "constraint-case-study-v2.html",
    "lab.html",
    "proof.html",
    "roadmap.html",
    "repository.html",
    "docs/ARCHITECTURE.md",
    "docs/EVIDENCE_INDEX.md",
    "docs/REAL_VS_SYNTHETIC.md",
    "docs/PUBLIC_CLAIM_BOUNDARIES.md",
    "evidence/CI_TEST_004_PUBLIC_EXCERPT.json",
    "evidence/CI_TEST_006_PUBLIC_EXCERPT.txt",
    "evidence/CI_TEST_008_PUBLIC_EXCERPT.json",
)

REQUIRED_PUBLIC_REFERENCES = {
    "proof.html": (
        "https://github.com/HYDRADATAAI/Hydra/blob/main/market-data-pipeline-sample/src/hydra_market_pipeline/operations.py",
        "https://github.com/HYDRADATAAI/Hydra/blob/main/market-data-pipeline-sample/config/backfill_plan.json",
        "https://github.com/HYDRADATAAI/Hydra/blob/main/market-data-pipeline-sample/tests/test_operations.py",
        "https://github.com/HYDRADATAAI/Hydra/tree/main/sql-data-quality-sample",
        "https://github.com/HYDRADATAAI/Hydra/blob/main/sql-data-quality-sample/sql/02_quality.sql",
        "https://github.com/HYDRADATAAI/Hydra/blob/main/sql-data-quality-sample/tests/test_sql_sample.py",
        "https://github.com/HYDRADATAAI/Hydra/actions/workflows/sql-data-quality-sample.yml",
    ),
    "docs/EVIDENCE_INDEX.md": (
        "https://github.com/HYDRADATAAI/Hydra/blob/main/market-data-pipeline-sample/src/hydra_market_pipeline/operations.py",
        "https://github.com/HYDRADATAAI/Hydra/blob/main/market-data-pipeline-sample/config/backfill_plan.json",
        "https://github.com/HYDRADATAAI/Hydra/blob/main/market-data-pipeline-sample/tests/test_operations.py",
        "https://github.com/HYDRADATAAI/Hydra/tree/main/sql-data-quality-sample",
        "https://github.com/HYDRADATAAI/Hydra/blob/main/sql-data-quality-sample/run_demo.py",
        "https://github.com/HYDRADATAAI/Hydra/blob/main/sql-data-quality-sample/tests/test_sql_sample.py",
        "https://github.com/HYDRADATAAI/Hydra/actions/workflows/sql-data-quality-sample.yml",
    ),
}

STALE_PUBLIC_PHRASES = (
    "market intelligence data platform",
    "ai-driven quantitative trading",
    "github=unbound",
    "linkedin=unbound",
    "contact=unbound",
    "external destination not yet bound",
    "repo/readme.md",
    "thread f",
    "cross-thread",
)

ROOT_FORBIDDEN_PATTERNS = (
    re.compile(r"^CHANGELOG_V\d+\.md$", re.IGNORECASE),
    re.compile(r"^VERIFICATION_V\d+\.json$", re.IGNORECASE),
    re.compile(r"^W\d+_BUILD_REPORT\.md$", re.IGNORECASE),
    re.compile(r".*RELEASE_SEAL.*", re.IGNORECASE),
    re.compile(r"^RECRUITER_SCAN_.*", re.IGNORECASE),
    re.compile(r"^PUBLIC_CLAIM_CONSISTENCY_AUDIT.*", re.IGNORECASE),
    re.compile(r"^PACKAGE_MANIFEST_SHA256\.txt$", re.IGNORECASE),
    re.compile(r"^PATCH_NOTES\.md$", re.IGNORECASE),
    re.compile(r"^HYDRA_GITHUB_PAGES_DISCOVERY_RESULT\.txt$", re.IGNORECASE),
    re.compile(r"^(?:OPEN|TEST)_HYDRA_SITE\.ps1$", re.IGNORECASE),
    re.compile(r"^RUN_HYDRA_GITHUB_PAGES_DISCOVERY\.ps1$", re.IGNORECASE),
    re.compile(r"^WEBSITE_COPY_PATCHES\.md$", re.IGNORECASE),
    re.compile(r"^WEBSITE_PUBLIC_PROOF_AUTHORITY_MAP\.(?:md|csv)$", re.IGNORECASE),
)

MARKDOWN_LINK = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
CSS_URL = re.compile(r"url\(([^)]+)\)", re.IGNORECASE)


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del tag
        for key, value in attrs:
            if key.lower() in {"href", "src"} and value:
                self.links.append(value.strip())


def active_files(*patterns: str) -> list[Path]:
    files: set[Path] = set()
    for pattern in patterns:
        for path in ROOT.glob(pattern):
            if path.is_file() and "archive" not in path.relative_to(ROOT).parts:
                files.add(path)
    return sorted(files)


def clean_reference(reference: str) -> str:
    value = reference.strip().strip("'\"")
    if value.startswith("<") and ">" in value:
        value = value[1 : value.index(">")]
    elif re.search(r"\s+[\"']", value):
        value = re.split(r"\s+[\"']", value, maxsplit=1)[0]
    return value.strip()


def local_target(source: Path, reference: str) -> Path | None:
    reference = clean_reference(reference)
    if not reference or reference.startswith(("#", "//")):
        return None

    parsed = urlsplit(reference)
    if parsed.scheme or parsed.netloc:
        return None

    path_text = unquote(parsed.path)
    if not path_text:
        return None

    if path_text.startswith("/Hydra-Website/"):
        candidate = ROOT / path_text.removeprefix("/Hydra-Website/")
    elif path_text.startswith("/"):
        candidate = ROOT / path_text.lstrip("/")
    else:
        candidate = source.parent / path_text

    return candidate.resolve()


def validate_required_paths(errors: list[str]) -> None:
    for relative in REQUIRED_PATHS:
        if not (ROOT / relative).exists():
            errors.append(f"required path missing: {relative}")


def validate_root_hygiene(errors: list[str]) -> None:
    for path in ROOT.iterdir():
        if not path.is_file():
            continue
        for pattern in ROOT_FORBIDDEN_PATTERNS:
            if pattern.fullmatch(path.name):
                errors.append(f"historical/build artifact returned to repository root: {path.name}")
                break


def validate_required_public_references(errors: list[str]) -> None:
    for relative, references in REQUIRED_PUBLIC_REFERENCES.items():
        text = (ROOT / relative).read_text(encoding="utf-8-sig")
        for reference in references:
            if reference not in text:
                errors.append(f"required public reference missing from {relative}: {reference}")


def validate_public_language(errors: list[str]) -> None:
    presentation_files = active_files("*.html", "README.md", "docs/*.md")
    config = ROOT / "site.config.js"
    if config.is_file():
        presentation_files.append(config)

    for path in sorted(set(presentation_files)):
        text = path.read_text(encoding="utf-8-sig").casefold()
        relative = path.relative_to(ROOT).as_posix()
        for phrase in STALE_PUBLIC_PHRASES:
            if phrase.casefold() in text:
                errors.append(f"stale public phrase {phrase!r} in {relative}")


def validate_html_links(errors: list[str]) -> None:
    for path in active_files("**/*.html"):
        parser = LinkParser()
        try:
            parser.feed(path.read_text(encoding="utf-8-sig"))
        except Exception as exc:  # pragma: no cover - defensive reporting
            errors.append(f"unable to parse HTML {path.relative_to(ROOT)}: {exc}")
            continue

        for reference in parser.links:
            target = local_target(path, reference)
            if target is not None and not target.exists():
                errors.append(
                    f"broken HTML link: {path.relative_to(ROOT).as_posix()} -> {reference}"
                )


def validate_markdown_links(errors: list[str]) -> None:
    for path in active_files("**/*.md"):
        text = path.read_text(encoding="utf-8-sig")
        for match in MARKDOWN_LINK.finditer(text):
            reference = match.group(1)
            target = local_target(path, reference)
            if target is not None and not target.exists():
                errors.append(
                    f"broken Markdown link: {path.relative_to(ROOT).as_posix()} -> {reference}"
                )


def validate_css_links(errors: list[str]) -> None:
    for path in active_files("**/*.css"):
        text = path.read_text(encoding="utf-8-sig")
        for match in CSS_URL.finditer(text):
            reference = match.group(1)
            target = local_target(path, reference)
            if target is not None and not target.exists():
                errors.append(
                    f"broken CSS url(): {path.relative_to(ROOT).as_posix()} -> {reference}"
                )


def main() -> int:
    errors: list[str] = []

    validate_required_paths(errors)
    validate_root_hygiene(errors)
    validate_required_public_references(errors)
    validate_public_language(errors)
    validate_html_links(errors)
    validate_markdown_links(errors)
    validate_css_links(errors)

    if errors:
        print("PUBLIC_SURFACE_VALIDATION=FAIL")
        for error in sorted(set(errors)):
            print(f"ERROR: {error}")
        return 1

    print("PUBLIC_SURFACE_VALIDATION=PASS")
    print(f"REQUIRED_PATHS={len(REQUIRED_PATHS)}")
    print(f"HTML_FILES={len(active_files('**/*.html'))}")
    print(f"MARKDOWN_FILES={len(active_files('**/*.md'))}")
    print(f"CSS_FILES={len(active_files('**/*.css'))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
