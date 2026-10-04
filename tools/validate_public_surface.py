#!/usr/bin/env python3
"""Deterministic validation for HYDRA's recruiter-facing public surface."""

from __future__ import annotations

import base64
import binascii
import html
import json
import posixpath
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
CORE_PROOF_SHA = "6dd79a85cdba1f2cd90c2e8815f6d881ac73efad"
CORE_PROOF_RUN = (
    "https://github.com/HYDRADATAAI/Hydra/actions/runs/37170895042/attempts/1"
)
PROOF_BUNDLE_SHA256 = "2b52498e8dfba5f86cf694b08833bbbd67464c91e5cbf6fbd49cd37b1a0698a6"
CORE_PROOF_TREE = (
    f"https://github.com/HYDRADATAAI/Hydra/tree/{CORE_PROOF_SHA}/"
    "governed-intelligence-sample"
)
CORE_PROOF_BLOB = f"https://github.com/HYDRADATAAI/Hydra/blob/{CORE_PROOF_SHA}"
CORE_REPOSITORY_URL = "https://github.com/HYDRADATAAI/Hydra"


def core_proof_file(relative: str) -> str:
    return f"{CORE_PROOF_BLOB}/governed-intelligence-sample/{relative}"

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
        CORE_PROOF_TREE,
        core_proof_file("src/hydra_governed_intelligence/retrieval.py"),
        core_proof_file("src/hydra_governed_intelligence/grounding.py"),
        core_proof_file("fixtures/retrieval_qrels.json"),
        core_proof_file("fixtures/grounding_cases.json"),
        CORE_PROOF_RUN,
    ),
    "README.md": (
        CORE_PROOF_TREE,
        core_proof_file("src/hydra_governed_intelligence/retrieval.py"),
        core_proof_file("src/hydra_governed_intelligence/retrieval_evaluation.py"),
        core_proof_file("fixtures/retrieval_cases.json"),
        core_proof_file("fixtures/retrieval_qrels.json"),
        core_proof_file("src/hydra_governed_intelligence/grounding.py"),
        core_proof_file("fixtures/grounding_cases.json"),
        core_proof_file("src/hydra_governed_intelligence/pre_upload_verifier.py"),
        core_proof_file("tests/test_pre_upload_verifier.py"),
        f"{CORE_PROOF_BLOB}/.github/workflows/governed-intelligence-sample.yml",
        CORE_PROOF_RUN,
    ),
    "docs/EVIDENCE_INDEX.md": (
        "https://github.com/HYDRADATAAI/Hydra/blob/main/market-data-pipeline-sample/src/hydra_market_pipeline/operations.py",
        "https://github.com/HYDRADATAAI/Hydra/blob/main/market-data-pipeline-sample/config/backfill_plan.json",
        "https://github.com/HYDRADATAAI/Hydra/blob/main/market-data-pipeline-sample/tests/test_operations.py",
        "https://github.com/HYDRADATAAI/Hydra/tree/main/sql-data-quality-sample",
        "https://github.com/HYDRADATAAI/Hydra/blob/main/sql-data-quality-sample/run_demo.py",
        "https://github.com/HYDRADATAAI/Hydra/blob/main/sql-data-quality-sample/tests/test_sql_sample.py",
        "https://github.com/HYDRADATAAI/Hydra/actions/workflows/sql-data-quality-sample.yml",
        CORE_PROOF_TREE,
        core_proof_file("src/hydra_governed_intelligence/retrieval.py"),
        core_proof_file("src/hydra_governed_intelligence/retrieval_evaluation.py"),
        core_proof_file("fixtures/retrieval_cases.json"),
        core_proof_file("fixtures/retrieval_qrels.json"),
        core_proof_file("src/hydra_governed_intelligence/grounding.py"),
        core_proof_file("fixtures/grounding_cases.json"),
        core_proof_file("src/hydra_governed_intelligence/pre_upload_verifier.py"),
        core_proof_file("tests/test_pre_upload_verifier.py"),
        f"{CORE_PROOF_BLOB}/.github/workflows/governed-intelligence-sample.yml",
        CORE_PROOF_RUN,
    ),
    "repository.html": (
        CORE_PROOF_TREE,
        CORE_PROOF_RUN,
    ),
}

RETRIEVAL_CLAIMS = (
    "13 retrieval cases",
    "4 `ADMIT` / 6 `ABSTAIN` / 3 `REFUSE`",
    "0.444444 micro Recall@k",
    "0.583333 macro Recall@k",
    "0.666667 MRR",
)
GROUNDING_CLAIMS = (
    "8 grounding cases",
    "1 `ADMIT` / 5 `QUARANTINE` / 1 `ABSTAIN` / 1 `REFUSE`",
)
PACKAGE_CLAIMS = (
    "9 manifested outputs",
    "26 receipts",
    "2 verified input snapshots",
    "7 independently replayed source rows",
    "15 bundle members",
    "41,833 bytes",
    PROOF_BUNDLE_SHA256,
)
PROVENANCE_CLAIMS = (
    "source_snapshot.csv",
    "resolved_symbol_aliases.json",
    "all seven synthetic rows",
    "quarantine-designed rows",
    "Governed contexts and receipts remain accepted-only or aggregate-only",
    "do not expose quarantined row payloads",
)
BOUNDARY_CLAIMS = (
    "Candidate responses are committed synthetic fixtures, not model output.",
    "Retrieval is lexical, not semantic or embedding retrieval.",
    "There is no model or agent execution and no external action.",
    "repository-controlled evidence",
    "not independent attestation or a trust anchor",
)
REQUIRED_PUBLIC_CLAIMS = {
    "README.md": (
        RETRIEVAL_CLAIMS
        + GROUNDING_CLAIMS
        + PACKAGE_CLAIMS
        + PROVENANCE_CLAIMS
        + BOUNDARY_CLAIMS
    ),
    "docs/EVIDENCE_INDEX.md": (
        RETRIEVAL_CLAIMS
        + GROUNDING_CLAIMS
        + PACKAGE_CLAIMS
        + PROVENANCE_CLAIMS
        + BOUNDARY_CLAIMS
    ),
    "docs/PUBLIC_CLAIM_BOUNDARIES.md": (
        RETRIEVAL_CLAIMS
        + GROUNDING_CLAIMS
        + PACKAGE_CLAIMS
        + PROVENANCE_CLAIMS
        + BOUNDARY_CLAIMS
    ),
    "docs/REAL_VS_SYNTHETIC.md": (
        RETRIEVAL_CLAIMS
        + GROUNDING_CLAIMS
        + PACKAGE_CLAIMS
        + PROVENANCE_CLAIMS
        + BOUNDARY_CLAIMS
    ),
    "proof.html": PACKAGE_CLAIMS + PROVENANCE_CLAIMS,
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
    "governed intelligence context and lexical retrieval proof",
    "six retrieval cases",
    "six retrieval citation checks",
    "three admits, two abstentions, one refusal",
    "1.000000 recall@k and mrr",
    "deterministic pre-model grounding",
    "0c227ea14c1e5b1fb7a5588e301a9b201e3aa504",
    "37165170935",
    "e3c8aa581a9329e93620546eb16712bc47cb9dd00c9747830cfed7086192bdcd",
    "13 bundle members",
    "40,377 bytes",
)

MUTABLE_NAVIGATION_NOTICE = (
    "The pipeline, recovery, and SQL links in sections 05-07 navigate to the current "
    "repository state; they are not immutable proof references."
)
ALLOWED_EXTERNAL_SCHEMES = frozenset({"https", "mailto", "tel"})
ALLOWED_HTTP_HOSTS = frozenset(
    {
        "github.com",
        "hydradataai.github.io",
        "linkedin.com",
        "www.linkedin.com",
    }
)
ALLOWED_CSS_DATA_IMAGE_TYPES = frozenset(
    {"image/gif", "image/jpeg", "image/png", "image/svg+xml", "image/webp"}
)
HTML_URL_ATTRIBUTES = frozenset(
    {
        "href",
        "xlink:href",
        "src",
        "srcset",
        "imagesrcset",
        "poster",
        "action",
        "formaction",
    }
)
MARKDOWN_AUTOLINK_RE = re.compile(
    r"<(?P<target>(?:[A-Za-z][A-Za-z0-9+.-]{1,31}:[^<>\x00-\x20]*|"
    r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9.-]{0,253}[A-Za-z0-9])?))>"
)
NON_RENDERED_ELEMENTS = frozenset({"script", "style", "template", "noscript"})
VOID_ELEMENTS = frozenset(
    {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
)
GOVERNED_WORKFLOW_PATH = ".github/workflows/governed-intelligence-sample.yml"
NUMBER_TOKEN = (
    r"(?:\d[\d,]*|zero|one|two|three|four|five|six|seven|eight|nine|ten|"
    r"eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|"
    r"nineteen|twenty(?:[- ](?:one|two|three|four|five|six|seven|eight|nine))?)"
)
NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
}

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

CSS_URL = re.compile(
    r"url\(\s*(?:\"((?:\\.|[^\"\\])*)\"|'((?:\\.|[^'\\])*)'|([^)]*))\s*\)",
    re.IGNORECASE,
)
CSS_STRING_IMPORT = re.compile(
    r"@import(?![\w-])\s*(?!url\s*\()(?:\"((?:\\.|[^\"\\])*)\"|'((?:\\.|[^'\\])*)')",
    re.IGNORECASE,
)
CSS_COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
DISCLAIMER_PREFIX = re.compile(
    r"(?:"
    r"\b(?:false|incorrect|inaccurate|untrue|unsupported|unverified|unproven|disclaimed)\b"
    r"|\b(?:cannot|can't|could\s+not|do\s+not|don't|does\s+not|doesn't|did\s+not|fails?\s+to|"
    r"unable\s+to)\s+(?:establish|prove|show|verify|demonstrate|support|confirm|"
    r"substantiate|assert|claim|say)\b"
    r"|\b(?:no|not|never)\b[^.!?]{0,80}\b(?:evidence|proof|verified|established)\b"
    r")[^.!?]{0,120}$",
    re.IGNORECASE,
)
DISCLAIMER_SUFFIX = re.compile(
    r"^\s*(?:(?:that|this|it)(?:\s+(?:claim|statement|evidence))?|"
    r"the\s+(?:claim|statement|evidence))?\s*"
    r"(?:is|was|does|did|can|could|has|had|fails?)?\s*"
    r"(?:false|incorrect|inaccurate|untrue|unsupported|unverified|unproven|disclaimed|"
    r"not\s+true|"
    r"not\s+(?:prove|show|verify|demonstrate|support|confirm|establish)|"
    r"cannot\s+(?:prove|show|verify|demonstrate|support|confirm|establish))\b",
    re.IGNORECASE,
)


class LinkParser(HTMLParser):
    def __init__(self, *, nesting_depth: int = 0) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.base_tags = 0
        self.issues: list[str] = []
        self.style_depth = 0
        self.nesting_depth = nesting_depth

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.casefold()
        attributes = {key.casefold(): value for key, value in attrs}
        if tag == "base":
            self.base_tags += 1
        if tag == "style":
            self.style_depth += 1
        if tag == "meta" and (attributes.get("http-equiv") or "").strip().casefold() == "refresh":
            destination = parse_meta_refresh(attributes.get("content") or "")
            if destination is None:
                self.issues.append("malformed meta refresh")
            else:
                self.links.append(destination)
        if tag == "object" and attributes.get("data"):
            self.links.append((attributes["data"] or "").strip())
        if tag == "iframe" and attributes.get("srcdoc"):
            if self.nesting_depth >= 4:
                self.issues.append("iframe srcdoc nesting exceeds four levels")
            else:
                nested = LinkParser(nesting_depth=self.nesting_depth + 1)
                nested.feed(attributes["srcdoc"] or "")
                nested.close()
                self.links.extend(nested.links)
                self.base_tags += nested.base_tags
                self.issues.extend(f"iframe srcdoc: {issue}" for issue in nested.issues)
        ping = attributes.get("ping")
        if ping:
            self.links.extend(ping.split())
        inline_style = attributes.get("style")
        if inline_style:
            self.links.extend(extract_css_links(inline_style))
        for key, value in attrs:
            key = key.casefold()
            if key not in HTML_URL_ATTRIBUTES or not value:
                continue
            if key in {"srcset", "imagesrcset"}:
                self.links.extend(parse_srcset(value))
            else:
                self.links.append(value.strip())

    handle_startendtag = handle_starttag

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() == "style" and self.style_depth:
            self.style_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.style_depth:
            self.links.extend(extract_css_links(data))


class TextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.links: list[str] = []
        self.ignored_depth = 0
        self.element_stack: list[tuple[str, bool]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_starttag(tag, attrs, self_closing=False)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._handle_starttag(tag, attrs, self_closing=True)

    def _handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]], *, self_closing: bool
    ) -> None:
        tag = tag.casefold()
        attributes = {key.casefold(): value for key, value in attrs}
        starts_ignored_region = (
            tag in NON_RENDERED_ELEMENTS
            or _element_is_hidden(attributes)
        )
        if starts_ignored_region:
            self.ignored_depth += 1
        if not self.ignored_depth:
            for key, value in attrs:
                if key.casefold() in {"href", "xlink:href"} and value:
                    self.links.append(value.strip())
        if not self_closing and tag not in VOID_ELEMENTS:
            self.element_stack.append((tag, starts_ignored_region))
        elif starts_ignored_region:
            self.ignored_depth -= 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.casefold()
        for index in range(len(self.element_stack) - 1, -1, -1):
            if self.element_stack[index][0] != tag:
                continue
            closed = self.element_stack[index:]
            del self.element_stack[index:]
            self.ignored_depth -= sum(1 for _, ignored in closed if ignored)
            break

    def handle_data(self, data: str) -> None:
        if not self.ignored_depth:
            self.parts.append(data)


class AnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = {key.casefold(): value for key, value in attrs}
        identifier = attributes.get("id")
        if identifier:
            self.anchors.add(identifier)
        if tag.casefold() == "a" and attributes.get("name"):
            self.anchors.add(attributes["name"] or "")

    handle_startendtag = handle_starttag


def parse_meta_refresh(content: str) -> str | None:
    match = re.fullmatch(
        r"\s*\d+(?:\.\d+)?\s*;\s*url\s*=\s*(.+?)\s*", content, re.IGNORECASE
    )
    if not match:
        return None
    destination = match.group(1).strip()
    if len(destination) >= 2 and destination[0] == destination[-1] and destination[0] in "\"'":
        destination = destination[1:-1].strip()
    return destination or None


def parse_srcset(value: str) -> list[str]:
    references: list[str] = []
    index = 0
    while index < len(value):
        while index < len(value) and (value[index].isspace() or value[index] == ","):
            index += 1
        if index >= len(value):
            break

        start = index
        is_data = value[index : index + 5].casefold() == "data:"
        while index < len(value) and not value[index].isspace():
            if value[index] == "," and not is_data:
                break
            index += 1
        reference = value[start:index].strip()
        if reference:
            references.append(reference)

        while index < len(value) and value[index] != ",":
            index += 1
        if index < len(value):
            index += 1
    return references


def active_files(*patterns: str) -> list[Path]:
    files: set[Path] = set()
    for pattern in patterns:
        for path in ROOT.glob(pattern):
            if path.is_file() and "archive" not in path.relative_to(ROOT).parts:
                files.add(path)
    return sorted(files)


def _decode_repeated(value: str, *, percent: bool = True) -> str:
    for _ in range(4):
        decoded = html.unescape(value)
        if percent:
            decoded = unquote(decoded)
        if decoded == value:
            break
        value = decoded
    return value


def clean_reference(reference: str) -> str:
    value = html.unescape(reference).strip().strip("'\"")
    if value.startswith("<") and ">" in value:
        value = value[1 : value.index(">")]
    elif re.search(r"\s+[\"']", value):
        value = re.split(r"\s+[\"']", value, maxsplit=1)[0]
    return value.strip()


def _replace_inline_code(text: str, *, keep_content: bool) -> str:
    output: list[str] = []
    index = 0
    while index < len(text):
        if text[index] != "`":
            output.append(text[index])
            index += 1
            continue
        end_run = index
        while end_run < len(text) and text[end_run] == "`":
            end_run += 1
        marker = text[index:end_run]
        closing = text.find(marker, end_run)
        if closing < 0:
            output.append(marker)
            index = end_run
            continue
        content = text[end_run:closing]
        output.append(content if keep_content else " " * (closing + len(marker) - index))
        index = closing + len(marker)
    return "".join(output)


def strip_markdown_nonrendered(text: str, *, keep_inline_code: bool) -> str:
    text = HTML_COMMENT.sub("", text)
    output: list[str] = []
    fence_character = ""
    fence_length = 0
    for line in text.splitlines(keepends=True):
        match = re.match(r"^[ ]{0,3}(`{3,}|~{3,})", line)
        if fence_character:
            if (
                match
                and match.group(1)[0] == fence_character
                and len(match.group(1)) >= fence_length
            ):
                fence_character = ""
                fence_length = 0
            output.append("\n" if line.endswith("\n") else "")
            continue
        if match:
            fence_character = match.group(1)[0]
            fence_length = len(match.group(1))
            output.append("\n" if line.endswith("\n") else "")
            continue
        output.append(line)
    return _replace_inline_code("".join(output), keep_content=keep_inline_code)


def _find_balanced(text: str, start: int, opening: str, closing: str) -> int:
    depth = 1
    index = start + 1
    while index < len(text):
        if text[index] == "\\":
            index += 2
            continue
        if text[index] == opening:
            depth += 1
        elif text[index] == closing:
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return -1


def _normalize_reference_label(label: str) -> str:
    label = re.sub(r"\\([\\`*_{}\[\]()#+.!<>-])", r"\1", label)
    return " ".join(label.split()).casefold()


def _definition_destination(remainder: str) -> str | None:
    remainder = remainder.lstrip()
    if not remainder:
        return None
    if remainder.startswith("<"):
        closing = remainder.find(">", 1)
        return remainder[1:closing] if closing >= 0 else None

    index = 0
    parentheses = 0
    while index < len(remainder):
        character = remainder[index]
        if character == "\\":
            index += 2
            continue
        if character == "(" :
            parentheses += 1
        elif character == ")" and parentheses:
            parentheses -= 1
        elif character.isspace() and parentheses == 0:
            break
        index += 1
    return remainder[:index] or None


def extract_markdown_definitions(text: str) -> tuple[dict[str, str], list[str], str]:
    definitions: dict[str, str] = {}
    destinations: list[str] = []
    retained_lines: list[str] = []
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip(" ")
        indent = len(line) - len(stripped)
        if indent > 3 or not stripped.startswith("["):
            retained_lines.append(line)
            continue
        closing = _find_balanced(stripped, 0, "[", "]")
        if closing < 0 or stripped[closing + 1 : closing + 2] != ":":
            retained_lines.append(line)
            continue
        destination = _definition_destination(stripped[closing + 2 :])
        if destination is None:
            retained_lines.append(line)
            continue
        label = _normalize_reference_label(stripped[1:closing])
        definitions.setdefault(label, destination)
        destinations.append(destination)
        retained_lines.append("\n" if line.endswith("\n") else "")
    return definitions, destinations, "".join(retained_lines)


def _inline_destination(text: str, opening: int) -> tuple[str, int] | None:
    closing = _find_balanced(text, opening, "(", ")")
    if closing < 0:
        return None
    content = text[opening + 1 : closing].lstrip()
    if not content:
        return None
    if content.startswith("<"):
        end = content.find(">", 1)
        if end < 0:
            return None
        destination = content[1:end]
    else:
        index = 0
        parentheses = 0
        while index < len(content):
            character = content[index]
            if character == "\\":
                index += 2
                continue
            if character == "(":
                parentheses += 1
            elif character == ")" and parentheses:
                parentheses -= 1
            elif character.isspace() and parentheses == 0:
                break
            index += 1
        destination = content[:index]
    return (destination, closing + 1) if destination else None


def markdown_links_and_spans(
    text: str, definitions: dict[str, str]
) -> list[tuple[int, int, str, str]]:
    links: list[tuple[int, int, str, str]] = []
    index = 0
    while index < len(text):
        image_start = text[index] == "!" and index + 1 < len(text) and text[index + 1] == "["
        opening = index + 1 if image_start else index
        if text[opening : opening + 1] != "[" or (
            opening and text[opening - 1] == "\\" and not image_start
        ):
            index += 1
            continue
        closing = _find_balanced(text, opening, "[", "]")
        if closing < 0:
            index += 1
            continue
        label = text[opening + 1 : closing]
        cursor = closing + 1
        while cursor < len(text) and text[cursor] in " \t\r\n":
            cursor += 1

        parsed: tuple[str, int] | None = None
        if cursor < len(text) and text[cursor] == "(":
            parsed = _inline_destination(text, cursor)
        elif cursor < len(text) and text[cursor] == "[":
            reference_end = _find_balanced(text, cursor, "[", "]")
            if reference_end >= 0:
                reference_label = text[cursor + 1 : reference_end] or label
                destination = definitions.get(_normalize_reference_label(reference_label))
                if destination is not None:
                    parsed = destination, reference_end + 1
        else:
            destination = definitions.get(_normalize_reference_label(label))
            if destination is not None:
                parsed = destination, closing + 1

        if parsed is None:
            index = closing + 1
            continue
        destination, end = parsed
        links.append((index, end, label, destination))
        index = end
    return links


def extract_markdown_links(text: str) -> tuple[list[str], LinkParser]:
    stripped = strip_markdown_nonrendered(text, keep_inline_code=False)
    definitions, definition_destinations, body = extract_markdown_definitions(stripped)
    links = [item[3] for item in markdown_links_and_spans(body, definitions)]
    autolinks = []
    for match in MARKDOWN_AUTOLINK_RE.finditer(body):
        target = html.unescape(match.group("target"))
        autolinks.append(target if ":" in target else f"mailto:{target}")
    parser = LinkParser()
    parser.feed(body)
    return definition_destinations + links + autolinks + parser.links, parser


def _decode_css_escapes(text: str) -> str:
    def decode_hex(match: re.Match[str]) -> str:
        value = int(match.group(1), 16)
        if value == 0 or value > 0x10FFFF:
            return "\N{REPLACEMENT CHARACTER}"
        return chr(value)

    text = re.sub(r"\\([0-9a-fA-F]{1,6})(?:\r\n|[\t\n\r\f ])?", decode_hex, text)
    return re.sub(r"\\([^\r\n\f])", r"\1", text)


def _css_declarations_hide(text: str) -> bool:
    normalized = _decode_css_escapes(CSS_COMMENT.sub("", text))
    for declaration in normalized.split(";"):
        if ":" not in declaration:
            continue
        property_name, value = declaration.split(":", maxsplit=1)
        property_name = property_name.strip().casefold()
        value = re.sub(r"\s*!important\s*$", "", value, flags=re.IGNORECASE).strip().casefold()
        if property_name == "display" and value == "none":
            return True
        if property_name == "visibility" and value in {"hidden", "collapse"}:
            return True
        if property_name == "content-visibility" and value == "hidden":
            return True
    return False


_SITE_HIDDEN_CLASS_GROUPS: tuple[frozenset[str], ...] | None = None


def _css_block_end(text: str, opening: int) -> int:
    depth = 1
    quote = ""
    index = opening + 1
    while index < len(text):
        character = text[index]
        if quote:
            if character == "\\":
                index += 2
                continue
            if character == quote:
                quote = ""
        elif character in "\"'":
            quote = character
        elif character == "{":
            depth += 1
        elif character == "}":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return -1


def _top_level_css_rules(text: str) -> list[tuple[str, str]]:
    rules: list[tuple[str, str]] = []
    statement_start = 0
    quote = ""
    index = 0
    while index < len(text):
        character = text[index]
        if quote:
            if character == "\\":
                index += 2
                continue
            if character == quote:
                quote = ""
            index += 1
            continue
        if character in "\"'":
            quote = character
            index += 1
            continue
        if character == ";":
            statement_start = index + 1
        elif character == "{":
            block_end = _css_block_end(text, index)
            if block_end < 0:
                break
            selectors = text[statement_start:index].strip()
            if selectors and not selectors.startswith("@"):
                rules.append((selectors, text[index + 1 : block_end]))
            statement_start = block_end + 1
            index = block_end
        index += 1
    return rules


def _hidden_class_groups_from_css(text: str) -> set[frozenset[str]]:
    normalized = _decode_css_escapes(CSS_COMMENT.sub("", text))
    groups: set[frozenset[str]] = set()
    for selectors, body in _top_level_css_rules(normalized):
        if not _css_declarations_hide(body):
            continue
        for selector in selectors.split(","):
            selector = selector.strip()
            if not re.fullmatch(r"(?:\.[A-Za-z_][A-Za-z0-9_-]*)+", selector):
                continue
            groups.add(frozenset(re.findall(r"\.([A-Za-z_][A-Za-z0-9_-]*)", selector)))
    return groups


def _site_hidden_class_groups() -> tuple[frozenset[str], ...]:
    global _SITE_HIDDEN_CLASS_GROUPS
    if _SITE_HIDDEN_CLASS_GROUPS is not None:
        return _SITE_HIDDEN_CLASS_GROUPS

    groups: set[frozenset[str]] = set()
    for relative in ("styles.css", "assets/site.css"):
        css_path = ROOT / relative
        if not css_path.is_file():
            continue
        groups.update(
            _hidden_class_groups_from_css(css_path.read_text(encoding="utf-8-sig"))
        )
    _SITE_HIDDEN_CLASS_GROUPS = tuple(sorted(groups, key=lambda item: tuple(sorted(item))))
    return _SITE_HIDDEN_CLASS_GROUPS


def _element_is_hidden(attributes: dict[str, str | None]) -> bool:
    if "hidden" in attributes:
        return True
    if _css_declarations_hide(attributes.get("style") or ""):
        return True
    classes = frozenset((attributes.get("class") or "").split())
    return any(group.issubset(classes) for group in _site_hidden_class_groups())


def _css_function_bodies(text: str, function_name: str) -> list[str]:
    bodies: list[str] = []
    pattern = re.compile(rf"(?<![\w-])(?:-webkit-)?{function_name}\s*\(", re.IGNORECASE)
    for match in pattern.finditer(text):
        opening = match.end() - 1
        depth = 1
        quote = ""
        index = opening + 1
        while index < len(text):
            character = text[index]
            if quote:
                if character == "\\":
                    index += 2
                    continue
                if character == quote:
                    quote = ""
            elif character in "\"'":
                quote = character
            elif character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    bodies.append(text[opening + 1 : index])
                    break
            index += 1
    return bodies


def _top_level_css_strings(text: str) -> list[str]:
    strings: list[str] = []
    depth = 0
    index = 0
    while index < len(text):
        character = text[index]
        if character in "\"'":
            quote = character
            start = index + 1
            index += 1
            while index < len(text):
                if text[index] == "\\":
                    index += 2
                    continue
                if text[index] == quote:
                    if depth == 0:
                        strings.append(text[start:index])
                    break
                index += 1
        elif character == "(":
            depth += 1
        elif character == ")" and depth:
            depth -= 1
        index += 1
    return strings


def extract_css_links(text: str) -> list[str]:
    text = _decode_css_escapes(CSS_COMMENT.sub("", text))
    references = [
        next(group for group in match.groups() if group is not None).strip()
        for match in CSS_URL.finditer(text)
    ]
    references.extend(
        next(group for group in match.groups() if group is not None).strip()
        for match in CSS_STRING_IMPORT.finditer(text)
    )
    for body in _css_function_bodies(text, "image-set"):
        references.extend(_top_level_css_strings(body))
    return references


def _renderable_markdown_html(
    text: str, *, keep_inline_code: bool, preserve_links: bool
) -> str:
    stripped = strip_markdown_nonrendered(text, keep_inline_code=keep_inline_code)
    definitions, _, body = extract_markdown_definitions(stripped)
    spans = markdown_links_and_spans(body, definitions)
    rendered: list[str] = []
    cursor = 0
    for start, end, label, destination in spans:
        rendered.append(body[cursor:start])
        if preserve_links:
            rendered.append(
                f'<a href="{html.escape(destination, quote=True)}">'
                f"{html.escape(label)}</a>"
            )
        else:
            rendered.append(label)
        cursor = end
    rendered.append(body[cursor:])
    return "".join(rendered)


def rendered_markdown_prose(text: str) -> str:
    parser = TextParser()
    parser.feed(
        _renderable_markdown_html(text, keep_inline_code=True, preserve_links=False)
    )
    return " ".join(" ".join(parser.parts).split())


def rendered_html_prose(text: str) -> str:
    parser = TextParser()
    parser.feed(text)
    return " ".join(" ".join(parser.parts).split())


def rendered_prose(path: Path) -> str:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.casefold() == ".md":
        return rendered_markdown_prose(text)
    if path.suffix.casefold() == ".html":
        return rendered_html_prose(text)
    return " ".join(text.split())


def _canonical_http_url(reference: str) -> tuple[str | None, str | None]:
    value = _decode_repeated(clean_reference(reference))
    if value.startswith("//"):
        value = "https:" + value
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError as exc:
        return None, f"malformed external URL: {exc}"
    scheme = parsed.scheme.casefold()
    if scheme != "https" or not parsed.netloc:
        return None, "external URLs must use HTTPS"
    if parsed.username is not None or parsed.password is not None:
        return None, "credentials are not allowed in external URLs"
    host = (parsed.hostname or "").casefold().rstrip(".")
    if host not in ALLOWED_HTTP_HOSTS:
        return None, f"external host is not allowlisted: {host or '<missing>'}"
    if port not in {None, 443}:
        return None, f"external port is not allowlisted: {port}"
    netloc = host if port is None else f"{host}:{port}"
    had_trailing_slash = parsed.path.endswith("/")
    normalized_path = posixpath.normpath(parsed.path or "/")
    if not normalized_path.startswith("/"):
        normalized_path = "/" + normalized_path
    if had_trailing_slash and normalized_path != "/":
        normalized_path += "/"
    canonical = urlunsplit((scheme, netloc, normalized_path, parsed.query, parsed.fragment))
    return canonical, None


def _repository_url_problem(reference: str) -> str | None:
    value = _decode_repeated(clean_reference(reference))
    try:
        original = urlsplit(value)
    except ValueError as exc:
        return f"malformed repository URL: {exc}"
    canonical, problem = _canonical_http_url(value)
    if problem:
        return problem
    assert canonical is not None
    parsed = urlsplit(canonical)
    if (original.hostname or "").casefold() != "github.com":
        return "repositoryUrl must use github.com exactly"
    if parsed.path != "/HYDRADATAAI/Hydra":
        return "repositoryUrl must target HYDRADATAAI/Hydra exactly"
    if parsed.query or parsed.fragment:
        return "repositoryUrl must not contain a query or fragment"
    return None


def _linkedin_url_problem(reference: str) -> str | None:
    value = _decode_repeated(clean_reference(reference))
    try:
        original = urlsplit(value)
    except ValueError as exc:
        return f"malformed LinkedIn URL: {exc}"
    canonical, problem = _canonical_http_url(value)
    if problem:
        return problem
    assert canonical is not None
    parsed = urlsplit(canonical)
    host = (original.hostname or "").casefold()
    if host not in {"linkedin.com", "www.linkedin.com"}:
        return "linkedinUrl must use linkedin.com or www.linkedin.com exactly"
    if not re.fullmatch(r"/(?:in|company)/[^/\s]+/?", parsed.path):
        return "linkedinUrl must target one profile or company path"
    if parsed.query or parsed.fragment:
        return "linkedinUrl must not contain a query or fragment"
    return None


def _is_governed_github_url(canonical: str) -> bool:
    parsed = urlsplit(canonical)
    path = parsed.path.casefold()
    return (
        parsed.hostname == "github.com"
        and path.startswith("/hydradataai/hydra/")
        and (
            "/governed-intelligence-sample" in path
            or path.endswith("/" + GOVERNED_WORKFLOW_PATH.casefold())
        )
    )


def _governed_url_is_pinned(canonical: str) -> bool:
    parts = [part for part in urlsplit(canonical).path.split("/") if part]
    if len(parts) < 5 or [part.casefold() for part in parts[:2]] != [
        "hydradataai",
        "hydra",
    ]:
        return False
    return parts[2].casefold() in {"blob", "raw", "tree"} and parts[3] == CORE_PROOF_SHA


def _validate_css_data_image(reference: str) -> str | None:
    value = _decode_repeated(reference)
    if len(value) > 262_144:
        return "CSS data image exceeds 256 KiB"
    match = re.fullmatch(r"data:([^;,]+)((?:;[^,]*)?),(.*)", value, re.DOTALL | re.IGNORECASE)
    if not match:
        return "malformed CSS data image"
    media_type = match.group(1).casefold()
    parameters = match.group(2).casefold()
    payload = match.group(3)
    if media_type not in ALLOWED_CSS_DATA_IMAGE_TYPES:
        return f"CSS data image type is not allowlisted: {media_type}"
    if ";base64" in parameters:
        try:
            decoded = base64.b64decode(payload, validate=True)
        except (binascii.Error, ValueError):
            return "malformed base64 CSS data image"
        inspectable = decoded.decode("utf-8", errors="ignore")
    elif media_type == "image/svg+xml":
        inspectable = payload
        if "<svg" not in inspectable.casefold():
            return "non-base64 SVG data image has no SVG root"
    else:
        return "non-SVG CSS data images must use base64"
    if re.search(
        r"<(?:script|foreignobject|style)\b|@import\b|\bon(?:error|load)\s*=|"
        r"javascript\s*:|(?:href|xlink:href)\s*=\s*['\"]\s*(?!#)|"
        r"url\s*\(\s*['\"]?\s*(?!#)",
        inspectable,
        re.IGNORECASE,
    ):
        return "active content is not allowed in CSS data images"
    return None


def _parse_number(value: str) -> int:
    normalized = value.casefold().replace(",", "")
    if normalized.isdigit():
        return int(normalized)
    if "-" in normalized or " " in normalized:
        first, second = re.split(r"[- ]", normalized, maxsplit=1)
        return NUMBER_WORDS[first] + NUMBER_WORDS[second]
    return NUMBER_WORDS[normalized]


def _has_trailing_dot_or_space_segment(path_text: str) -> bool:
    return any(
        segment not in {".", ".."} and segment.endswith((".", " "))
        for segment in path_text.split("/")
        if segment
    )


def _validate_local_fragment(
    errors: list[str], source_name: str, target: Path, fragment: str, link_kind: str
) -> None:
    decoded_fragment = _decode_repeated(fragment)
    if not decoded_fragment:
        return
    if target.suffix.casefold() not in {".html", ".htm"}:
        errors.append(
            f"local {link_kind} fragment target is not HTML: "
            f"{source_name} -> {target.relative_to(ROOT).as_posix()}#{fragment}"
        )
        return
    parser = AnchorParser()
    try:
        parser.feed(target.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError) as exc:
        errors.append(
            f"unable to inspect local fragment target from {source_name}: "
            f"{target.relative_to(ROOT).as_posix()}: {exc}"
        )
        return
    if decoded_fragment not in parser.anchors:
        errors.append(
            f"broken local {link_kind} fragment: {source_name} -> "
            f"{target.relative_to(ROOT).as_posix()}#{fragment}"
        )


def extract_file_references(path: Path) -> tuple[list[str], int, list[str]]:
    text = path.read_text(encoding="utf-8-sig")
    suffix = path.suffix.casefold()
    if suffix == ".html":
        parser = LinkParser()
        parser.feed(text)
        return parser.links, parser.base_tags, parser.issues
    if suffix == ".md":
        links, parser = extract_markdown_links(text)
        return links, parser.base_tags, parser.issues
    if suffix == ".css":
        return extract_css_links(text), 0, []
    return [], 0, []


def extract_rendered_link_destinations(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.casefold() == ".md":
        text = _renderable_markdown_html(
            text, keep_inline_code=False, preserve_links=True
        )
    parser = TextParser()
    parser.feed(text)
    parser.close()
    return parser.links


def validate_reference(
    errors: list[str], source: Path, reference: str, link_kind: str
) -> str | None:
    source_name = source.relative_to(ROOT).as_posix()
    original = clean_reference(reference)
    value = _decode_repeated(original)
    if not value:
        return None
    if any(ord(character) < 32 or ord(character) == 127 for character in value):
        errors.append(f"control character in {link_kind} link: {source_name} -> {reference}")
        return None
    if re.match(r"^[A-Za-z]:[\\/]", value):
        errors.append(f"drive-style {link_kind} link is forbidden: {source_name} -> {reference}")
        return None
    if "\\" in value:
        errors.append(f"backslash in {link_kind} link is forbidden: {source_name} -> {reference}")
        return None

    scheme = urlsplit(value).scheme.casefold()
    if value.startswith("//") or scheme in {"http", "https"}:
        canonical, problem = _canonical_http_url(value)
        if problem:
            errors.append(f"invalid {link_kind} link: {source_name} -> {reference}: {problem}")
            return None
        assert canonical is not None
        if _is_governed_github_url(canonical) and not _governed_url_is_pinned(canonical):
            errors.append(
                f"governed-proof URL is not pinned to {CORE_PROOF_SHA}: "
                f"{source_name} -> {reference}"
            )
        return canonical

    if scheme == "data":
        if link_kind != "CSS url()" or not value.casefold().startswith("data:image/"):
            errors.append(f"data URL is forbidden in {link_kind}: {source_name} -> {reference}")
            return None
        problem = _validate_css_data_image(original)
        if problem:
            errors.append(f"unsafe CSS data image: {source_name}: {problem}")
        return None

    if scheme == "mailto":
        if not re.fullmatch(r"mailto:[^@\s?]+@[^@\s?]+\.[^@\s?]+", value, re.IGNORECASE):
            errors.append(f"invalid mailto link: {source_name} -> {reference}")
        return value
    if scheme == "tel":
        if not re.fullmatch(r"tel:\+?[0-9(). -]+", value, re.IGNORECASE):
            errors.append(f"invalid tel link: {source_name} -> {reference}")
        return value
    if scheme:
        if scheme not in ALLOWED_EXTERNAL_SCHEMES:
            errors.append(
                f"active, local, or unsupported scheme in {link_kind} link: "
                f"{source_name} -> {reference}"
            )
        else:  # pragma: no cover - all allowlisted schemes are handled above
            errors.append(f"invalid {link_kind} link: {source_name} -> {reference}")
        return None

    parsed = urlsplit(value)
    if parsed.netloc:
        errors.append(f"network-path {link_kind} link is malformed: {source_name} -> {reference}")
        return None
    path_text = parsed.path
    if path_text and _has_trailing_dot_or_space_segment(path_text):
        errors.append(
            f"URL segment has a trailing dot or space in {link_kind}: "
            f"{source_name} -> {reference}"
        )
        return None

    if not path_text:
        candidate = source
    elif path_text.startswith("/Hydra-Website/"):
        project_relative = path_text.removeprefix("/Hydra-Website/")
        if project_relative.startswith("/"):
            errors.append(
                f"malformed project-root {link_kind} link: {source_name} -> {reference}"
            )
            return None
        candidate = ROOT / project_relative
    elif path_text.startswith("/"):
        errors.append(
            f"domain-root {link_kind} link must start with /Hydra-Website/: "
            f"{source_name} -> {reference}"
        )
        return None
    else:
        candidate = source.parent / path_text
    target = candidate.resolve()
    try:
        target.relative_to(ROOT)
    except ValueError:
        errors.append(
            f"local {link_kind} link escapes repository root: {source_name} -> {reference}"
        )
        return None
    if not target.exists():
        errors.append(f"broken {link_kind} link: {source_name} -> {reference}")
    elif parsed.fragment:
        _validate_local_fragment(errors, source_name, target, parsed.fragment, link_kind)
    return None


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


def parse_site_config_text(text: str, errors: list[str]) -> dict[str, str]:
    assignment = re.fullmatch(
        r"\s*window\.HYDRA_CONFIG\s*=\s*\{(?P<body>.*)\}\s*;\s*",
        text,
        re.DOTALL,
    )
    if not assignment:
        errors.append("site.config.js must be one declarative window.HYDRA_CONFIG object")
        return {}

    body = assignment.group("body")
    values: dict[str, str] = {}
    cursor = 0
    entry = re.compile(
        r'\s*(?P<key>[A-Za-z_$][A-Za-z0-9_$]*)\s*:\s*'
        r'(?P<value>"(?:\\.|[^"\\])*")\s*',
        re.DOTALL,
    )
    while cursor < len(body):
        if not body[cursor:].strip():
            break
        match = entry.match(body, cursor)
        if not match:
            errors.append("site.config.js contains a non-declarative or non-string entry")
            return {}
        key = match.group("key")
        if key in values:
            errors.append(f"site.config.js contains duplicate key: {key}")
            return {}
        try:
            values[key] = json.loads(match.group("value"))
        except json.JSONDecodeError as exc:
            errors.append(f"site.config.js contains an invalid string for {key}: {exc}")
            return {}
        cursor = match.end()
        if cursor >= len(body) or not body[cursor:].strip():
            break
        if body[cursor] != ",":
            errors.append("site.config.js entries must be comma-separated")
            return {}
        cursor += 1
        if not body[cursor:].strip():
            break
    return values


def parse_site_config(path: Path, errors: list[str]) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        errors.append(f"unable to read site.config.js: {exc}")
        return {}
    return parse_site_config_text(text, errors)


def validate_site_config(errors: list[str]) -> None:
    path = ROOT / "site.config.js"
    if not path.is_file():
        errors.append("required path missing: site.config.js")
        return
    config = parse_site_config(path, errors)
    repository = config.get("repositoryUrl", "")
    if repository:
        problem = _repository_url_problem(repository)
        if problem:
            errors.append(f"invalid site.config.js repositoryUrl: {problem}")
    linkedin = config.get("linkedinUrl", "")
    if linkedin:
        problem = _linkedin_url_problem(linkedin)
        if problem:
            errors.append(f"invalid site.config.js linkedinUrl: {problem}")
    contact = config.get("contactEmail", "")
    if contact:
        validate_reference(errors, path, f"mailto:{contact}", "site.config.js contactEmail")


def _manifest_references(manifest: object) -> list[str]:
    if not isinstance(manifest, dict):
        raise ValueError("root must be an object")
    references: list[str] = []
    for key in ("start_url", "scope", "id"):
        value = manifest.get(key)
        if value is not None:
            if not isinstance(value, str):
                raise ValueError(f"{key} must be a string")
            references.append(value)
    for key in ("icons", "screenshots"):
        entries = manifest.get(key, [])
        if not isinstance(entries, list):
            raise ValueError(f"{key} must be an array")
        for index, item in enumerate(entries):
            if not isinstance(item, dict) or not isinstance(item.get("src"), str):
                raise ValueError(f"{key}[{index}].src must be a string")
            references.append(item["src"])
    shortcuts = manifest.get("shortcuts", [])
    if not isinstance(shortcuts, list):
        raise ValueError("shortcuts must be an array")
    for index, shortcut in enumerate(shortcuts):
        if not isinstance(shortcut, dict) or not isinstance(shortcut.get("url"), str):
            raise ValueError(f"shortcuts[{index}].url must be a string")
        references.append(shortcut["url"])
        icons = shortcut.get("icons", [])
        if not isinstance(icons, list):
            raise ValueError(f"shortcuts[{index}].icons must be an array")
        for icon_index, icon in enumerate(icons):
            if not isinstance(icon, dict) or not isinstance(icon.get("src"), str):
                raise ValueError(
                    f"shortcuts[{index}].icons[{icon_index}].src must be a string"
                )
            references.append(icon["src"])
    share_target = manifest.get("share_target")
    if share_target is not None:
        if not isinstance(share_target, dict) or not isinstance(
            share_target.get("action"), str
        ):
            raise ValueError("share_target.action must be a string")
        references.append(share_target["action"])
    protocol_handlers = manifest.get("protocol_handlers", [])
    if not isinstance(protocol_handlers, list):
        raise ValueError("protocol_handlers must be an array")
    for index, handler in enumerate(protocol_handlers):
        if not isinstance(handler, dict) or not isinstance(handler.get("url"), str):
            raise ValueError(f"protocol_handlers[{index}].url must be a string")
        references.append(handler["url"])
    related_applications = manifest.get("related_applications", [])
    if not isinstance(related_applications, list):
        raise ValueError("related_applications must be an array")
    for index, application in enumerate(related_applications):
        if not isinstance(application, dict):
            raise ValueError(f"related_applications[{index}] must be an object")
        url = application.get("url")
        if url is not None:
            if not isinstance(url, str):
                raise ValueError(f"related_applications[{index}].url must be a string")
            references.append(url)
    file_handlers = manifest.get("file_handlers", [])
    if not isinstance(file_handlers, list):
        raise ValueError("file_handlers must be an array")
    for index, handler in enumerate(file_handlers):
        if not isinstance(handler, dict) or not isinstance(handler.get("action"), str):
            raise ValueError(f"file_handlers[{index}].action must be a string")
        references.append(handler["action"])
    return references


def validate_webmanifest_links(errors: list[str]) -> None:
    for path in active_files("**/*.webmanifest"):
        relative = path.relative_to(ROOT).as_posix()
        try:
            manifest = json.loads(path.read_text(encoding="utf-8-sig"))
            references = _manifest_references(manifest)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
            errors.append(f"unable to parse web manifest {relative}: {exc}")
            continue
        for reference in references:
            validate_reference(errors, path, reference, "web manifest")


def validate_accessibility_contracts(errors: list[str]) -> None:
    css = (ROOT / "styles.css").read_text(encoding="utf-8-sig")
    if not re.search(
        r"\[hidden\]\s*\{[^}]*\bdisplay\s*:\s*none\s*!important\s*;?[^}]*\}",
        css,
        re.IGNORECASE | re.DOTALL,
    ):
        errors.append("styles.css must make [hidden] display:none !important")
    for relative in ("proof.html", "roadmap.html"):
        text = (ROOT / relative).read_text(encoding="utf-8-sig")
        if not re.search(
            r"<main\b(?=[^>]*\bid=[\"']main[\"'])(?=[^>]*\btabindex=[\"']-1[\"'])",
            text,
            re.IGNORECASE,
        ):
            errors.append(f"skip-link target must be programmatically focusable: {relative}")
        if not re.search(
            r"<a\b(?=[^>]*\bclass=[\"'][^\"']*\bis-active\b)(?=[^>]*\baria-current=[\"']page[\"'])",
            text,
            re.IGNORECASE,
        ):
            errors.append(f"active navigation must expose aria-current=page: {relative}")
    proof = (ROOT / "proof.html").read_text(encoding="utf-8-sig")
    if MUTABLE_NAVIGATION_NOTICE not in rendered_html_prose(proof):
        errors.append("proof.html must label current-main pipeline and SQL links as navigation")


def validate_required_public_references(errors: list[str]) -> None:
    for relative, references in REQUIRED_PUBLIC_REFERENCES.items():
        path = ROOT / relative
        extracted = extract_rendered_link_destinations(path)
        destinations = {
            canonical
            for reference in extracted
            for canonical in [_canonical_http_url(reference)[0]]
            if canonical is not None
        }
        for reference in references:
            expected, problem = _canonical_http_url(reference)
            if problem:  # pragma: no cover - programmer-owned constants
                errors.append(f"invalid required public reference constant: {reference}: {problem}")
            elif expected not in destinations:
                errors.append(f"required public reference missing from {relative}: {reference}")


def _claim_is_affirmed(prose: str, claim: str, *, reject_negation: bool) -> bool:
    normalized_claim = rendered_markdown_prose(claim)
    start = 0
    while True:
        index = prose.find(normalized_claim, start)
        if index < 0:
            return False
        sentence_start = max(
            prose.rfind(".", 0, index),
            prose.rfind("!", 0, index),
            prose.rfind("?", 0, index),
        )
        prefix = prose[sentence_start + 1 : index]
        claim_end = index + len(normalized_claim)
        following_stops = [
            position
            for marker in ".!?"
            for position in [prose.find(marker, claim_end)]
            if position >= 0
        ]
        suffix_end = min(following_stops) + 1 if following_stops else claim_end + 160
        suffix = prose[claim_end:suffix_end]
        disclaimed = bool(
            DISCLAIMER_PREFIX.search(prefix) or DISCLAIMER_SUFFIX.search(suffix)
        )
        if not reject_negation or not disclaimed:
            return True
        start = index + 1


def validate_required_public_claims(errors: list[str]) -> None:
    for relative, claims in REQUIRED_PUBLIC_CLAIMS.items():
        prose = rendered_prose(ROOT / relative)
        for claim in claims:
            if not _claim_is_affirmed(prose, claim, reject_negation=True):
                errors.append(f"required public claim missing from {relative}: {claim}")


def _validate_expected_count(
    errors: list[str], relative: str, prose: str, pattern: str, expected: int, label: str
) -> None:
    for match in re.finditer(pattern, prose, re.IGNORECASE):
        observed = _parse_number(match.group("value"))
        if observed != expected:
            errors.append(
                f"contradictory {label} in {relative}: expected {expected}, found {match.group(0)!r}"
            )


def _validate_expected_decimal(
    errors: list[str], relative: str, prose: str, patterns: tuple[str, ...], expected: str, label: str
) -> None:
    for pattern in patterns:
        for match in re.finditer(pattern, prose, re.IGNORECASE):
            observed = match.group("value")
            if observed != expected:
                errors.append(
                    f"contradictory {label} in {relative}: expected {expected}, "
                    f"found {match.group(0)!r}"
                )


def _bundle_digests(prose: str) -> list[str]:
    label = (
        r"(?:(?:proof\s+)?(?:bundle|package|ZIP)(?:\s+[A-Za-z0-9_-]+){0,5}\s+"
        r"(?:SHA-?256|digest)|(?:inner|its)\s+(?:SHA-?256|digest))"
    )
    return [
        match.group("digest")
        for match in re.finditer(
            rf"{label}\s*(?:is|of|:|=)?\s*`?(?P<digest>[0-9a-f]{{64}})\b",
            prose,
            re.IGNORECASE,
        )
    ]


def validate_metric_consistency(errors: list[str], path: Path, prose: str) -> None:
    relative = path.relative_to(ROOT).as_posix()
    _validate_expected_count(
        errors,
        relative,
        prose,
        rf"(?P<value>{NUMBER_TOKEN})\s+(?:(?:lexical[- ]?)?retrieval|benchmark)\s+cases?\b",
        13,
        "retrieval case count",
    )
    _validate_expected_count(
        errors,
        relative,
        prose,
        rf"\bretrieval\s+benchmark\b[^.!?]{{0,80}}\b(?P<value>{NUMBER_TOKEN})\s+cases?\b",
        13,
        "retrieval benchmark case count",
    )
    _validate_expected_count(
        errors,
        relative,
        prose,
        rf"(?P<value>{NUMBER_TOKEN})\s+(?:structured[- ]grounding|grounding)\s+cases?\b",
        8,
        "grounding case count",
    )
    _validate_expected_decimal(
        errors,
        relative,
        prose,
        (
            r"\bmicro\s+Recall@k\s*(?:[:=]|is|of)?\s*(?P<value>\d+(?:\.\d+)?)",
            r"(?P<value>\d+(?:\.\d+)?)\s+micro\s+Recall@k\b",
        ),
        "0.444444",
        "micro Recall@k",
    )
    _validate_expected_decimal(
        errors,
        relative,
        prose,
        (
            r"\bmacro\s+Recall@k\s*(?:[:=]|is|of)?\s*(?P<value>\d+(?:\.\d+)?)",
            r"(?P<value>\d+(?:\.\d+)?)\s+macro\s+Recall@k\b",
        ),
        "0.583333",
        "macro Recall@k",
    )
    _validate_expected_decimal(
        errors,
        relative,
        prose,
        (
            r"\bMRR\s*(?:[:=]|is|of)?\s*(?P<value>\d+(?:\.\d+)?)",
            r"(?P<value>\d+(?:\.\d+)?)\s+MRR\b",
        ),
        "0.666667",
        "MRR",
    )

    if re.search(
        r"(?:1(?:\.0+)?\s+Recall@k\s+and\s+MRR|"
        r"Recall@k\s+and\s+MRR\s*(?:[:=]|is|of)?\s*1(?:\.0+)?)",
        prose,
        re.IGNORECASE,
    ):
        errors.append(f"contradictory perfect Recall@k/MRR claim in {relative}")
    if re.search(
        r"(?:\bRecall@k\s*(?:[:=]|is|of)?\s*1(?:\.0+)?\b|"
        r"\b1(?:\.0+)?\s+Recall@k\b)",
        prose,
        re.IGNORECASE,
    ):
        errors.append(f"contradictory perfect Recall@k claim in {relative}")

    units = re.split(r"(?<=[.!?])\s+", prose)
    expected_outcomes = {
        "retrieval": {"admit": 4, "abstain": 6, "refuse": 3},
        "grounding": {"admit": 1, "quarantine": 5, "abstain": 1, "refuse": 1},
    }
    for unit in units:
        folded = unit.casefold()
        for category, expected in expected_outcomes.items():
            if category not in folded or not all(status in folded for status in expected):
                continue
            observed: dict[str, int] = {}
            for match in re.finditer(
                rf"(?P<value>{NUMBER_TOKEN})\s+(?P<status>ADMIT|QUARANTINE|ABSTAIN|REFUSE)\b",
                unit,
                re.IGNORECASE,
            ):
                observed[match.group("status").casefold()] = _parse_number(match.group("value"))
            for status, expected_value in expected.items():
                if status in observed and observed[status] != expected_value:
                    errors.append(
                        f"contradictory {category} {status.upper()} count in {relative}: "
                        f"expected {expected_value}, found {observed[status]}"
                    )

        if not re.search(r"\b(?:bundle|package|ZIP|manifested)\b", unit, re.IGNORECASE):
            continue
        for pattern, expected, label in (
            (rf"(?P<value>{NUMBER_TOKEN})\s+(?:manifested\s+)?outputs?\b", 9, "manifested outputs"),
            (rf"(?P<value>{NUMBER_TOKEN})\s+receipts?\b", 26, "receipt count"),
            (rf"(?P<value>{NUMBER_TOKEN})\s+(?:bundle|ZIP)\s+members?\b", 15, "bundle member count"),
            (r"(?P<value>\d[\d,]*)\s+bytes\b", 41_833, "bundle byte count"),
        ):
            _validate_expected_count(errors, relative, unit, pattern, expected, label)
        for digest in _bundle_digests(unit):
            if digest.casefold() != PROOF_BUNDLE_SHA256:
                errors.append(
                    f"contradictory proof bundle SHA-256 in {relative}: {digest}"
                )


def validate_public_language(errors: list[str]) -> None:
    presentation_files = active_files("*.html", "README.md", "docs/*.md")
    config = ROOT / "site.config.js"
    if config.is_file():
        presentation_files.append(config)

    for path in sorted(set(presentation_files)):
        prose = rendered_prose(path)
        text = prose.casefold()
        relative = path.relative_to(ROOT).as_posix()
        for phrase in STALE_PUBLIC_PHRASES:
            if phrase.casefold() in text:
                errors.append(f"stale public phrase {phrase!r} in {relative}")
        validate_metric_consistency(errors, path, prose)


def validate_html_links(errors: list[str]) -> None:
    for path in active_files("**/*.html"):
        try:
            references, base_tags, parser_issues = extract_file_references(path)
        except Exception as exc:  # pragma: no cover - defensive reporting
            errors.append(f"unable to parse HTML {path.relative_to(ROOT)}: {exc}")
            continue
        if base_tags:
            errors.append(f"HTML base tag is forbidden: {path.relative_to(ROOT).as_posix()}")
        for issue in parser_issues:
            errors.append(f"invalid HTML navigation in {path.relative_to(ROOT).as_posix()}: {issue}")
        for reference in references:
            validate_reference(errors, path, reference, "HTML")


def validate_markdown_links(errors: list[str]) -> None:
    for path in active_files("**/*.md"):
        try:
            references, base_tags, parser_issues = extract_file_references(path)
        except Exception as exc:  # pragma: no cover - defensive reporting
            errors.append(f"unable to parse Markdown {path.relative_to(ROOT)}: {exc}")
            continue
        if base_tags:
            errors.append(f"HTML base tag is forbidden in Markdown: {path.relative_to(ROOT).as_posix()}")
        for issue in parser_issues:
            errors.append(
                f"invalid HTML navigation in Markdown {path.relative_to(ROOT).as_posix()}: {issue}"
            )
        for reference in references:
            validate_reference(errors, path, reference, "Markdown")


def validate_css_links(errors: list[str]) -> None:
    for path in active_files("**/*.css"):
        for reference in extract_css_links(path.read_text(encoding="utf-8-sig")):
            validate_reference(errors, path, reference, "CSS url()")


def validate_internal_self_checks(errors: list[str]) -> None:
    markdown = r"""
[nested escaped label\]](../inline-outside)
[reference link][outside]
[outside]: ../reference-outside
<a href="../raw-html-outside">raw HTML</a>
<https://evil.example/autolink>
<person@example.com>
<!-- [comment](../ignored-comment) -->
```markdown
[fenced](../ignored-fence)
```
"""
    references, parser = extract_markdown_links(markdown)
    expected_references = {
        "../inline-outside",
        "../reference-outside",
        "../raw-html-outside",
        "https://evil.example/autolink",
        "mailto:person@example.com",
    }
    if not expected_references.issubset(references):
        errors.append("internal self-check failed: Markdown link extraction")
    if {"../ignored-comment", "../ignored-fence"}.intersection(references):
        errors.append("internal self-check failed: non-rendered Markdown was parsed")
    if parser.base_tags:
        errors.append("internal self-check failed: unexpected Markdown base tag")

    html_parser = LinkParser()
    html_parser.feed(
        '<base href="/"><img src="a.png" srcset="b.png 1x, c.png 2x" '
        'poster="p.png" style="background:url(inline.png)"><form action="submit">'
        '<button formaction="alternate" ping="audit-one audit-two">'
        '<meta http-equiv="refresh" content="0; url=refresh.html#ready">'
        '<link rel="manifest" href="app.webmanifest" '
        'imagesrcset="preload-1.png 1x, preload-2.png 2x">'
        '<object data="object.html"></object>'
        '<svg><a xlink:href="vector-target.html">vector</a></svg>'
        '<iframe srcdoc="&lt;a href=&quot;nested.html&quot;&gt;nested&lt;/a&gt;">'
        '</iframe>'
        '<style>@import "theme.css"; .hero{background:url(hero.png)}</style>'
    )
    expected_attributes = {
        "a.png",
        "b.png",
        "c.png",
        "p.png",
        "inline.png",
        "submit",
        "alternate",
        "audit-one",
        "audit-two",
        "refresh.html#ready",
        "app.webmanifest",
        "preload-1.png",
        "preload-2.png",
        "object.html",
        "vector-target.html",
        "nested.html",
        "theme.css",
        "hero.png",
    }
    if (
        html_parser.base_tags != 1
        or html_parser.issues
        or not expected_attributes.issubset(html_parser.links)
    ):
        errors.append("internal self-check failed: HTML URL attribute extraction")

    css_references = extract_css_links(
        '@import "layout.css"; @import url("print.css"); '
        '@import/**/"comment-split.css"; @\\69mport "escaped-import.css"; '
        'main{background:url("surface.png");mask:u\\72l("escaped-url.svg");'
        'background-image:image-set("https://evil.example/density-one.png" 1x, '
        'url("density-two.png") 2x, '
        'type("image/png"))} '
        '/* @import "ignored.css"; */'
    )
    if set(css_references) != {
        "layout.css",
        "print.css",
        "comment-split.css",
        "escaped-import.css",
        "surface.png",
        "escaped-url.svg",
        "https://evil.example/density-one.png",
        "density-two.png",
    }:
        errors.append("internal self-check failed: CSS URL/import extraction")
    image_set_errors: list[str] = []
    validate_reference(
        image_set_errors,
        ROOT / "styles.css",
        "https://evil.example/density-one.png",
        "self-check image-set()",
    )
    if not image_set_errors:
        errors.append("internal self-check failed: external image-set() URL accepted")

    conditional_hidden_groups = _hidden_class_groups_from_css(
        ".always-hidden{display:none}"
        "@media(max-width:40rem){.responsive-only{display:none}}"
    )
    if conditional_hidden_groups != {frozenset({"always-hidden"})}:
        errors.append("internal self-check failed: conditional CSS hidden-class handling")

    encoded_floating = (
        "//github.com/HYDRADATAAI/Hydra/blob/refs%2Fheads%2Fmain/"
        "governed-intelligence-sample/readme.md"
    )
    canonical, problem = _canonical_http_url(encoded_floating)
    if problem or canonical is None or not _is_governed_github_url(canonical):
        errors.append("internal self-check failed: governed URL canonicalization")
    elif _governed_url_is_pinned(canonical):
        errors.append("internal self-check failed: floating governed URL accepted")

    if _canonical_http_url("http://github.com/HYDRADATAAI/Hydra")[1] is None:
        errors.append("internal self-check failed: non-HTTPS external URL accepted")

    dot_segment = (
        f"https://github.com/HYDRADATAAI/Hydra/blob/{CORE_PROOF_SHA}/../main/"
        "governed-intelligence-sample/readme.md"
    )
    canonical, problem = _canonical_http_url(dot_segment)
    if problem or canonical is None or _governed_url_is_pinned(canonical):
        errors.append("internal self-check failed: governed dot-segment URL accepted")

    safe_image = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg'%3E%3C/svg%3E"
    unsafe_image = "data:image/svg+xml,%3Csvg onload='alert(1)'%3E%3C/svg%3E"
    if _validate_css_data_image(safe_image) is not None:
        errors.append("internal self-check failed: safe CSS data image rejected")
    if _validate_css_data_image(unsafe_image) is None:
        errors.append("internal self-check failed: active CSS data image accepted")

    prose = rendered_markdown_prose(
        "<!-- 6 benchmark cases -->\n```text\nRecall@k 1.0\n```\n13 retrieval cases"
    )
    if "6 benchmark cases" in prose or "Recall@k 1.0" in prose or "13 retrieval cases" not in prose:
        errors.append("internal self-check failed: rendered Markdown prose filtering")

    visible_prose = rendered_html_prose(
        '<p>Visible claim</p><div hidden>Hidden claim</div>'
        '<div aria-hidden="true"><span>ARIA-hidden claim</span></div>'
        '<div class="site-nav">Responsive-only claim</div>'
        '<div style="display:none">CSS-hidden claim</div>'
        '<div style="display:none!important">Important-hidden claim</div>'
        '<div class="public-profile-actions">Class-hidden claim</div>'
        '<script>Script claim</script><style>Style claim</style>'
        '<template>Template claim</template><noscript>No-script claim</noscript>'
    )
    if visible_prose != "Visible claim ARIA-hidden claim Responsive-only claim":
        errors.append("internal self-check failed: rendered HTML prose filtering")

    boundary_claim = "Candidate responses are committed synthetic fixtures, not model output."
    disclaimed_claims = (
        f"False: {boundary_claim}",
        f"It is untrue that {boundary_claim}",
        f"We cannot establish that {boundary_claim}",
        f"We do not assert that {boundary_claim}",
        f"This does not prove that {boundary_claim}",
        f"{boundary_claim} That statement is false.",
        f"{boundary_claim} This claim is not true.",
        f"{boundary_claim} This does not verify the claim.",
    )
    if any(
        _claim_is_affirmed(value, boundary_claim, reject_negation=True)
        for value in disclaimed_claims
    ) or not _claim_is_affirmed(boundary_claim, boundary_claim, reject_negation=True):
        errors.append("internal self-check failed: required-claim negation handling")

    visible_link_parser = TextParser()
    visible_link_parser.feed(
        '<a href="visible.html">visible</a>'
        '<div hidden><a href="hidden.html">hidden</a></div>'
        '<div style="display:none!important"><a href="important-hidden.html">hidden</a></div>'
        '<div class="public-profile-actions"><a href="class-hidden.html">hidden</a></div>'
    )
    if visible_link_parser.links != ["visible.html"]:
        errors.append("internal self-check failed: hidden required-link filtering")

    config_errors: list[str] = []
    config = parse_site_config_text(
        f'window.HYDRA_CONFIG = {{repositoryUrl: "{CORE_REPOSITORY_URL}", '
        'linkedinUrl: "", contactEmail: ""};',
        config_errors,
    )
    unsafe_config_errors: list[str] = []
    parse_site_config_text(
        'window.HYDRA_CONFIG = {repositoryUrl: alert("unsafe")};', unsafe_config_errors
    )
    if config_errors or config.get("repositoryUrl") != CORE_REPOSITORY_URL:
        errors.append("internal self-check failed: declarative site config parsing")
    if not unsafe_config_errors:
        errors.append("internal self-check failed: executable site config accepted")
    if (
        _repository_url_problem(CORE_REPOSITORY_URL) is not None
        or _repository_url_problem(f"{CORE_REPOSITORY_URL}/") is None
        or _repository_url_problem("https://github.com/HYDRADATAAI/Hydra-Website") is None
        or _repository_url_problem("https://github.com/attacker/phish") is None
        or _repository_url_problem("https://github.com/HYDRADATAAI/Hydra?tab=readme")
        is None
        or _linkedin_url_problem("https://www.linkedin.com/in/example-profile/") is not None
        or _linkedin_url_problem("https://linkedin.com/company/example-company") is not None
        or _linkedin_url_problem("https://linkedin.com/jobs/example") is None
    ):
        errors.append("internal self-check failed: key-specific configured URL policy")

    digest_errors: list[str] = []
    manifest_digest = "a" * 64
    validate_metric_consistency(
        digest_errors,
        ROOT / "README.md",
        f"Verified package facts: inner SHA-256 {PROOF_BUNDLE_SHA256}; "
        f"manifest SHA-256 {manifest_digest}.",
    )
    incorrect_digest_errors: list[str] = []
    validate_metric_consistency(
        incorrect_digest_errors,
        ROOT / "README.md",
        f"Verified package facts: inner SHA-256 {'b' * 64}.",
    )
    if digest_errors or not any(
        "contradictory proof bundle SHA-256" in error
        for error in incorrect_digest_errors
    ):
        errors.append("internal self-check failed: proof bundle digest scoping")

    fragment_errors: list[str] = []
    validate_reference(
        fragment_errors, ROOT / "constraint-case-study-v2.html", "index.html#proof", "self-check"
    )
    missing_fragment_errors: list[str] = []
    validate_reference(
        missing_fragment_errors,
        ROOT / "constraint-case-study-v2.html",
        "index.html#definitely-missing",
        "self-check",
    )
    if fragment_errors or not missing_fragment_errors:
        errors.append("internal self-check failed: local fragment validation")

    project_root_errors: list[str] = []
    validate_reference(
        project_root_errors, ROOT / "proof.html", "/Hydra-Website/proof.html", "self-check"
    )
    domain_root_errors: list[str] = []
    validate_reference(domain_root_errors, ROOT / "proof.html", "/proof.html", "self-check")
    if project_root_errors or not domain_root_errors:
        errors.append("internal self-check failed: project Pages root-link validation")

    try:
        manifest_references = _manifest_references(
            {
                "start_url": "index.html",
                "icons": [{"src": "icon.svg"}],
                "shortcuts": [{"url": "proof.html", "icons": []}],
                "related_applications": [
                    {"platform": "webapp", "url": "related-app.html"}
                ],
                "file_handlers": [
                    {"action": "open-file.html", "accept": {"text/plain": [".txt"]}}
                ],
            }
        )
    except ValueError:
        manifest_references = []
    if set(manifest_references) != {
        "index.html",
        "icon.svg",
        "proof.html",
        "related-app.html",
        "open-file.html",
    }:
        errors.append("internal self-check failed: web manifest URL extraction")


def main() -> int:
    errors: list[str] = []

    validate_internal_self_checks(errors)
    validate_required_paths(errors)
    validate_root_hygiene(errors)
    validate_site_config(errors)
    validate_webmanifest_links(errors)
    validate_accessibility_contracts(errors)
    validate_required_public_references(errors)
    validate_required_public_claims(errors)
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
