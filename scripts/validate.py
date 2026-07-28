#!/usr/bin/env python3
"""Read-only authority validation for dornglut/engineering."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".yml", ".yaml", ".txt", ".py", ".toml"}
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
METADATA_RE = re.compile(r"^- ([A-Za-z][A-Za-z ]*):\s*(.*)$")
ADR_FILE_RE = re.compile(r"^(?P<number>\d{4})-[a-z0-9][a-z0-9-]*\.md$")
ADR_LINK_RE = re.compile(r"\((?P<path>\d{4}-[a-z0-9][a-z0-9-]*\.md)\)")
INITIATIVE_FILE_RE = re.compile(r"^[a-z0-9][a-z0-9-]*\.md$")

ALLOWED_ADR_STATUSES = {"proposed", "accepted", "superseded", "rejected"}
ALLOWED_INITIATIVE_STATUSES = {"proposed", "active", "completed", "cancelled"}

REQUIRED_ADR_METADATA = {"Status", "Date", "Owner", "Scope"}
FULL_ADR_SECTIONS = {
    "Context",
    "Decision",
    "Alternatives considered",
    "Consequences",
    "Affected repositories",
    "Adoption or migration",
    "Supersedes",
    "Superseded by",
}
LEGACY_ADR_SECTION_EXEMPTIONS = {
    1: {"Context", "Decision", "Consequences"},
}

EXPECTED_WORKFLOW_FILES = {Path(".github/workflows/validate.yml")}
EXPECTED_REUSABLE_WORKFLOW = (
    "dornglut/github-workflows/.github/workflows/"
    "reusable-python-repository-validate.yml@"
    "624cb41adeed21a6461eb838bc7330bd0a5079fd"
)
VERIFIED_HEAD_INITIATIVE = Path("initiatives/verified-head-validation.md")
VERIFIED_HEAD_REPOSITORIES = {
    "dornglut/github-workflows",
    "dornglut/engineering",
    "dornglut/runen-sdf",
    "dornglut/runenwerk",
    "dornglut/.github",
    "dornglut/runen-ui",
}

FORBIDDEN_PATHS = {
    "governance/README.md",
    "governance/authority-model.md",
    "governance/repository-lifecycle.md",
    "governance/decision-records.md",
    "architecture/README.md",
    "architecture/repository-system.md",
    "architecture/runen-framework-map.md",
    "portfolio/README.md",
}

ACTIVE_NAMESPACE_PATHS = (
    Path("README.md"),
    Path("AGENTS.md"),
    Path("governance"),
    Path("standards"),
    Path("architecture"),
)
VOLATILE_AUTHORITY_PATHS = (
    Path("README.md"),
    Path("AGENTS.md"),
    Path("governance"),
    Path("standards"),
    Path("architecture"),
)
VOLATILE_PATTERNS = {
    "refs/heads/": "mutable branch ref",
    "github.com/dornglut/engineering/pull/": "pull-request URL",
    "actions/runs/": "workflow-run URL",
    "workflow run:": "workflow-run state",
    "head sha:": "head SHA state",
}


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read(path: Path, failures: list[str]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        fail(f"{relative(path)}: failed to read UTF-8 text: {error}", failures)
        return None


def markdown_sections(text: str) -> dict[str, str]:
    sections: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            sections.setdefault(current, [])
        elif current is not None:
            sections[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in sections.items()}


def metadata(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        match = METADATA_RE.match(line)
        if match:
            values[match.group(1)] = match.group(2).strip()
    return values


def validate_text_file(path: Path, failures: list[str]) -> None:
    data = path.read_bytes()
    path_text = relative(path)

    if b"\x00" in data:
        fail(f"{path_text}: contains a NUL byte", failures)
        return

    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        fail(f"{path_text}: is not valid UTF-8", failures)
        return

    if text and not text.endswith("\n"):
        fail(f"{path_text}: must end with a newline", failures)

    for line_number, line in enumerate(text.splitlines(), start=1):
        if line.endswith((" ", "\t")):
            fail(f"{path_text}:{line_number}: trailing whitespace", failures)
        if "\t" in line:
            fail(f"{path_text}:{line_number}: tab character", failures)

    if path.suffix.lower() != ".md":
        return

    for match in LINK_RE.finditer(text):
        raw_target = match.group(1).strip()
        target = raw_target.split(maxsplit=1)[0].strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue

        target = unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not target:
            continue

        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT)
        except ValueError:
            fail(f"{path_text}: link escapes repository: {raw_target}", failures)
            continue

        if not resolved.exists():
            fail(f"{path_text}: broken relative link: {raw_target}", failures)


def validate_required_paths(failures: list[str]) -> None:
    manifest = ROOT / "validation-required-files.txt"
    if not manifest.is_file():
        fail("validation-required-files.txt: missing", failures)
        return

    for raw_line in manifest.read_text(encoding="utf-8").splitlines():
        required = raw_line.strip()
        if not required or required.startswith("#"):
            continue
        if not (ROOT / required).exists():
            fail(f"{required}: required path is missing", failures)

    for forbidden in sorted(FORBIDDEN_PATHS):
        if (ROOT / forbidden).exists():
            fail(f"{forbidden}: retired authority path must not exist", failures)


def validate_workflow_inventory(failures: list[str]) -> None:
    directory = ROOT / ".github/workflows"
    actual = {
        path.relative_to(ROOT)
        for path in directory.glob("*")
        if path.is_file() and path.suffix.lower() in {".yml", ".yaml"}
    }
    if actual != EXPECTED_WORKFLOW_FILES:
        expected = ", ".join(sorted(path.as_posix() for path in EXPECTED_WORKFLOW_FILES))
        found = ", ".join(sorted(path.as_posix() for path in actual)) or "none"
        fail(f"workflow inventory must be {expected}; found {found}", failures)


def validate_validation_workflow(failures: list[str]) -> None:
    path = ROOT / ".github/workflows/validate.yml"
    text = read(path, failures)
    if text is None:
        return

    if not text.startswith("name: Validate\n"):
        fail(".github/workflows/validate.yml: workflow name must be 'Validate'", failures)
    if not re.search(r"^  pull_request:\s*$", text, re.MULTILINE):
        fail(".github/workflows/validate.yml: pull_request trigger is required", failures)
    if "  push:\n    branches:\n      - main\n" not in text:
        fail(".github/workflows/validate.yml: push trigger must be restricted to main", failures)
    if "permissions:\n  contents: read\n\njobs:\n" not in text:
        fail(".github/workflows/validate.yml: permissions must be read-only contents", failures)

    uses = re.findall(r"^\s*uses:\s*(\S+)\s*$", text, re.MULTILINE)
    if uses != [EXPECTED_REUSABLE_WORKFLOW]:
        fail(
            ".github/workflows/validate.yml: must make exactly one call to the accepted "
            "reusable workflow revision",
            failures,
        )

    jobs_marker = "jobs:\n"
    jobs_body = text.split(jobs_marker, maxsplit=1)[1] if jobs_marker in text else ""
    jobs = re.findall(r"^  ([A-Za-z0-9_-]+):\s*$", jobs_body, re.MULTILINE)
    if jobs != ["validate"]:
        fail(".github/workflows/validate.yml: must define exactly one 'validate' job", failures)

    forbidden = {
        "workflow_dispatch:": "workflow_dispatch trigger",
        "with:": "workflow inputs",
        "secrets:": "workflow secrets",
        "steps:": "local job steps",
        "scripts/validate.py": "duplicated canonical validation command",
    }
    for token, label in forbidden.items():
        if token in text:
            fail(f".github/workflows/validate.yml: must not contain {label}", failures)


def require_markers(
    path: Path, markers: set[str], failures: list[str], description: str
) -> None:
    text = read(path, failures)
    if text is None:
        return
    lowered = text.lower()
    missing = sorted(marker for marker in markers if marker.lower() not in lowered)
    if missing:
        fail(f"{relative(path)}: missing {description}: {', '.join(missing)}", failures)


def validate_verified_head_standards(failures: list[str]) -> None:
    validate_path = ROOT / "standards/validation.md"
    require_markers(
        validate_path,
        {
            "reviewed feature head",
            "synthetic merge-result evidence",
            "github.event.pull_request.head.sha",
            "explicitly selects the expected revision",
            "git rev-parse head",
            "accepted squash merge",
            "accepted-main push evidence",
            "repository-owned canonical command",
            "compact",
            "bounded diagnostics",
        },
        failures,
        "verified-head evidence markers",
    )

    github_path = ROOT / "standards/github.md"
    github_text = read(github_path, failures)
    if github_text is not None:
        if "reviewed head or merge ref" in github_text.lower():
            fail(f"{relative(github_path)}: ambiguous reviewed-head wording is forbidden", failures)
        missing = sorted(
            marker
            for marker in {
                "accepted base",
                "reviewed feature head",
                "exact-head validation",
                "accepted squash merge",
            }
            if marker not in github_text.lower()
        )
        if missing:
            fail(
                f"{relative(github_path)}: missing pull-request evidence markers: "
                f"{', '.join(missing)}",
                failures,
            )

    require_markers(
        ROOT / "standards/repositories.md",
        {"accepted base", "reviewed feature head", "exact feature head", "post-merge revision"},
        failures,
        "development lifecycle markers",
    )


def validate_verified_head_initiative(failures: list[str]) -> None:
    path = ROOT / VERIFIED_HEAD_INITIATIVE
    text = read(path, failures)
    if text is None:
        return

    manifest = read(ROOT / "validation-required-files.txt", failures)
    if manifest is not None and manifest.splitlines().count(VERIFIED_HEAD_INITIATIVE.as_posix()) != 1:
        fail("validation-required-files.txt: verified-head initiative must be required once", failures)

    index_text = read(ROOT / "initiatives/README.md", failures)
    if index_text is not None:
        active = markdown_sections(index_text).get("Active", "")
        link = f"({VERIFIED_HEAD_INITIATIVE.name})"
        if index_text.count(link) != 1 or active.count(link) != 1:
            fail("initiatives/README.md: verified-head initiative must be indexed once under Active", failures)

    values = metadata(text)
    if values.get("Status", "").lower() != "active":
        fail("initiatives/verified-head-validation.md: status must be active", failures)
    if "engineering#20" not in values.get("Owning issue", "").lower():
        fail("initiatives/verified-head-validation.md: owning issue must be engineering#20", failures)
    if "624cb41adeed21a6461eb838bc7330bd0a5079fd" not in text:
        fail("initiatives/verified-head-validation.md: accepted shared revision is required", failures)
    missing_repositories = sorted(
        repository for repository in VERIFIED_HEAD_REPOSITORIES if repository not in text
    )
    if missing_repositories:
        fail(
            "initiatives/verified-head-validation.md: missing affected repositories: "
            f"{', '.join(missing_repositories)}",
            failures,
        )
    if "engineering#21" not in text.lower():
        fail("initiatives/verified-head-validation.md: engineering#21 link is required", failures)
    if markdown_sections(text).get("Closure record", "").strip() != "Open.":
        fail("initiatives/verified-head-validation.md: active closure record must be 'Open.'", failures)


def under(path: Path, candidates: tuple[Path, ...]) -> bool:
    rel = path.relative_to(ROOT)
    return any(rel == candidate or candidate in rel.parents for candidate in candidates)


def validate_authority_content(failures: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        text = read(path, failures)
        if text is None:
            continue
        lowered = text.lower()

        if under(path, ACTIVE_NAMESPACE_PATHS):
            for token in ("github.com/crystonix/", "`crystonix/", "crystonix/runen"):
                if token in lowered:
                    fail(
                        f"{relative(path)}: active authority contains historical owner token {token!r}",
                        failures,
                    )

        if under(path, VOLATILE_AUTHORITY_PATHS):
            for token, label in VOLATILE_PATTERNS.items():
                if token in lowered:
                    fail(
                        f"{relative(path)}: durable authority contains volatile {label}: {token!r}",
                        failures,
                    )


def validate_adrs(failures: list[str]) -> None:
    directory = ROOT / "adrs"
    index_path = directory / "README.md"
    index_text = read(index_path, failures)
    if index_text is None:
        return
    index_sections = markdown_sections(index_text)

    records: dict[str, tuple[Path, str, dict[str, str], dict[str, str], int]] = {}
    numbers: list[int] = []

    for path in sorted(directory.glob("*.md")):
        if path.name == "README.md":
            continue
        match = ADR_FILE_RE.match(path.name)
        if not match:
            fail(f"adrs/{path.name}: invalid ADR filename", failures)
            continue

        number = int(match.group("number"))
        numbers.append(number)
        text = read(path, failures)
        if text is None:
            continue

        expected_header = f"# ADR {number:04d}: "
        if not text.startswith(expected_header):
            fail(f"adrs/{path.name}: header must start with {expected_header!r}", failures)

        values = metadata(text)
        missing_metadata = sorted(REQUIRED_ADR_METADATA - values.keys())
        if missing_metadata:
            fail(
                f"adrs/{path.name}: missing metadata: {', '.join(missing_metadata)}",
                failures,
            )

        status = values.get("Status", "").lower()
        if status not in ALLOWED_ADR_STATUSES:
            fail(f"adrs/{path.name}: invalid status {status!r}", failures)

        sections = markdown_sections(text)
        required_sections = LEGACY_ADR_SECTION_EXEMPTIONS.get(number, FULL_ADR_SECTIONS)
        missing_sections = sorted(required_sections - sections.keys())
        if missing_sections:
            fail(
                f"adrs/{path.name}: missing sections: {', '.join(missing_sections)}",
                failures,
            )

        if index_text.count(f"({path.name})") != 1:
            fail(f"adrs/{path.name}: ADR index must link this file exactly once", failures)

        expected_index_section = {
            "accepted": "Current",
            "proposed": "Proposed",
            "superseded": "Superseded",
            "rejected": "Rejected",
        }.get(status)
        if expected_index_section and f"({path.name})" not in index_sections.get(
            expected_index_section, ""
        ):
            fail(
                f"adrs/{path.name}: status {status!r} does not match index section "
                f"{expected_index_section!r}",
                failures,
            )

        records[path.name] = (path, text, values, sections, number)

    if numbers:
        expected_numbers = list(range(1, max(numbers) + 1))
        if sorted(numbers) != expected_numbers:
            fail(
                f"adrs: numbering must be sequential; expected {expected_numbers}, "
                f"found {sorted(numbers)}",
                failures,
            )

    for filename, (_, _, values, sections, _) in records.items():
        status = values.get("Status", "").lower()
        supersedes = set(ADR_LINK_RE.findall(sections.get("Supersedes", "")))
        superseded_by = set(ADR_LINK_RE.findall(sections.get("Superseded by", "")))

        for target in supersedes | superseded_by:
            if target not in records:
                fail(f"adrs/{filename}: supersession target does not exist: {target}", failures)

        if status == "superseded" and not superseded_by:
            fail(f"adrs/{filename}: superseded ADR must name its replacement", failures)

        for target in supersedes:
            target_sections = records.get(target, (None, "", {}, {}, 0))[3]
            if filename not in set(
                ADR_LINK_RE.findall(target_sections.get("Superseded by", ""))
            ):
                fail(
                    f"adrs/{filename}: supersession link to {target} is not bidirectional",
                    failures,
                )

        for target in superseded_by:
            target_sections = records.get(target, (None, "", {}, {}, 0))[3]
            if filename not in set(ADR_LINK_RE.findall(target_sections.get("Supersedes", ""))):
                fail(
                    f"adrs/{filename}: replacement link to {target} is not bidirectional",
                    failures,
                )


def validate_initiatives(failures: list[str]) -> None:
    directory = ROOT / "initiatives"
    index_path = directory / "README.md"
    index_text = read(index_path, failures)
    if index_text is None:
        return
    index_sections = markdown_sections(index_text)

    for path in sorted(directory.glob("*.md")):
        if path.name == "README.md":
            continue
        if not INITIATIVE_FILE_RE.match(path.name):
            fail(f"initiatives/{path.name}: invalid initiative filename", failures)
            continue

        text = read(path, failures)
        if text is None:
            continue
        values = metadata(text)
        status = values.get("Status", "").lower()

        for key in ("Status", "Owner", "Owning issue"):
            if not values.get(key):
                fail(f"initiatives/{path.name}: missing metadata {key!r}", failures)

        if status not in ALLOWED_INITIATIVE_STATUSES:
            fail(f"initiatives/{path.name}: invalid status {status!r}", failures)

        if index_text.count(f"({path.name})") != 1:
            fail(
                f"initiatives/{path.name}: initiative index must link this file exactly once",
                failures,
            )

        expected_index_section = {
            "proposed": "Proposed",
            "active": "Active",
            "completed": "Closed",
            "cancelled": "Closed",
        }.get(status)
        if expected_index_section and f"({path.name})" not in index_sections.get(
            expected_index_section, ""
        ):
            fail(
                f"initiatives/{path.name}: status {status!r} does not match index section "
                f"{expected_index_section!r}",
                failures,
            )

        sections = markdown_sections(text)
        if status in {"completed", "cancelled"}:
            if not values.get("Opened") or not values.get("Closed"):
                fail(
                    f"initiatives/{path.name}: closed initiative requires Opened and Closed dates",
                    failures,
                )
            closure = sections.get("Closure record", "")
            if not closure or closure.strip().lower() in {"open.", "none."}:
                fail(
                    f"initiatives/{path.name}: closed initiative requires a closure record",
                    failures,
                )


def main() -> int:
    failures: list[str] = []

    validate_required_paths(failures)
    validate_workflow_inventory(failures)
    validate_validation_workflow(failures)

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"CODEOWNERS"}:
            validate_text_file(path, failures)

    validate_authority_content(failures)
    validate_adrs(failures)
    validate_initiatives(failures)
    validate_verified_head_standards(failures)
    validate_verified_head_initiative(failures)

    if failures:
        print("repository validation failed:", file=sys.stderr)
        for failure in sorted(set(failures)):
            print(f"- {failure}", file=sys.stderr)
        return 1

    print("repository validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
