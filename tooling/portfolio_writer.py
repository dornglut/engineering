#!/usr/bin/env python3
"""Manual, exact-request-approved writer for public dornglut/1 GitHub Projects v2.

No issue, label, PR or schedule automatically invokes this code. It only accepts a
bounded JSON issue request and manual workflow_dispatch with its immutable SHA-256.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ORGANIZATION = "dornglut"
PROJECT_NUMBER = 1
APPROVER = "aschenrot"
MAX_OPERATIONS = 20
MAX_PROJECT_ITEMS = 5000
STATUSES = ("Ready", "In progress", "Blocked", "Done")
PRIORITIES = ("P0", "P1", "P2", "P3")
KINDS = ("Decision", "Investigation", "Delivery", "Maintenance")
URL_PATTERN = re.compile(r"^https://github\.com/dornglut/([a-zA-Z0-9_.-]+)/(issues|pull)/(\d+)$")
HEX_PATTERN = re.compile(r"^[0-9a-f]{64}$")
FENCE_PATTERN = re.compile(r"\A\s*```json\s*\n([\s\S]*?)\n```\s*\Z")

PROJECT_QUERY = """
query Portfolio($cursor: String) {
  organization(login: "dornglut") {
    projectV2(number: 1) {
      id number public url
      fields(first: 100) {
        pageInfo { hasNextPage }
        nodes {
          __typename
          ... on ProjectV2Field { id name }
          ... on ProjectV2SingleSelectField { id name options { id name } }
          ... on ProjectV2IterationField { id name }
          ... on ProjectV2MultiSelectField { id name }
        }
      }
      items(first: 100, after: $cursor) {
        totalCount
        pageInfo { hasNextPage endCursor }
        nodes {
          id type isArchived
          content {
            __typename
            ... on Issue { url state repository { nameWithOwner isPrivate } }
            ... on PullRequest { url state repository { nameWithOwner isPrivate } }
          }
          fieldValues(first: 100) {
            pageInfo { hasNextPage }
            nodes {
              __typename
              ... on ProjectV2ItemFieldSingleSelectValue {
                name field { ... on ProjectV2SingleSelectField { name } }
              }
            }
          }
        }
      }
    }
  }
}
"""

TARGET_QUERY = """
query Target($repo: String!, $number: Int!) {
  repository(owner: "dornglut", name: $repo) {
    isPrivate
    issue(number: $number) { id url state }
    pullRequest(number: $number) { id url state }
  }
}
"""

ADD_ITEM = """
mutation Add($project: ID!, $content: ID!) {
  addProjectV2ItemById(input: {projectId: $project, contentId: $content}) {
    item { id }
  }
}
"""

SET_FIELD = """
mutation Set($project: ID!, $item: ID!, $field: ID!, $option: String!) {
  updateProjectV2ItemFieldValue(input: {
    projectId: $project, itemId: $item, fieldId: $field,
    value: { singleSelectOptionId: $option }
  }) { projectV2Item { id } }
}
"""

CLEAR_FIELD = """
mutation Clear($project: ID!, $item: ID!, $field: ID!) {
  clearProjectV2ItemFieldValue(input: {
    projectId: $project, itemId: $item, fieldId: $field
  }) { projectV2Item { id } }
}
"""

CREATE_KIND = """
mutation CreateKind($project: ID!, $options: [ProjectV2SingleSelectFieldOptionInput!]!) {
  createProjectV2Field(input: {
    projectId: $project, name: "Kind", dataType: SINGLE_SELECT,
    singleSelectOptions: $options
  }) { projectV2Field { ... on ProjectV2SingleSelectField { id name } } }
}
"""


def reject(message: str) -> None:
    raise ValueError(message)


def exact_keys(obj: object, allowed: set[str], required: set[str], label: str) -> None:
    if not isinstance(obj, dict) or set(obj) - allowed or required - set(obj):
        reject(f"{label}: unexpected or missing keys")


def without_duplicates(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            reject("Duplicate JSON object property")
        result[key] = value
    return result


def canonical_json(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def parse_request(body: str, digest: str) -> dict:
    match = FENCE_PATTERN.fullmatch(body)
    if not match:
        reject("Request body must be exactly one fenced json block, with no extra prose")
    if len(match.group(1).encode("utf-8")) > 16_384:
        reject("Request body exceeds 16 KiB")
    request = json.loads(match.group(1), object_pairs_hook=without_duplicates)
    exact_keys(request, {"schema", "project", "ensure_kind", "operations"},
               {"schema", "project", "ensure_kind", "operations"}, "request")
    if type(request["schema"]) is not int or request["schema"] != 1:
        reject("Unsupported schema version")
    if request["project"] != "dornglut/1" or type(request["ensure_kind"]) is not bool:
        reject("Unexpected project or ensure_kind flag")
    operations = request["operations"]
    if not isinstance(operations, list) or len(operations) > MAX_OPERATIONS:
        reject("Invalid or oversized operation inventory")
    if request["ensure_kind"] and operations:
        reject("Kind schema creation must use a separate request with zero operations")
    if not request["ensure_kind"] and not operations:
        reject("Request must contain at least one operation")
    seen_urls = set()
    for i, operation in enumerate(operations):
        exact_keys(operation, {"url", "status", "priority", "kind", "expected"},
                   {"url", "status", "priority", "kind", "expected"}, f"operation {i}")
        url = operation["url"]
        if not isinstance(url, str) or not URL_PATTERN.fullmatch(url) or url in seen_urls:
            reject("Invalid or duplicate public Dornglut issue/PR URL")
        seen_urls.add(url)
        if operation["status"] not in STATUSES:
            reject("Unsupported Status option")
        if operation["priority"] is not None and operation["priority"] not in PRIORITIES:
            reject("Unsupported Priority option")
        if operation["kind"] is not None and operation["kind"] not in KINDS:
            reject("Unsupported Kind option")
        expected = operation["expected"]
        exact_keys(expected, {"present", "status", "priority", "kind"}, {"present"}, "expected")
        if type(expected["present"]) is not bool:
            reject("expected.present must be boolean")
        if expected["present"]:
            if set(expected) != {"present", "status", "priority", "kind"}:
                reject("Existing item requires exact status/priority/kind expected values")
            if (expected["status"] not in STATUSES and expected["status"] is not None) or (
                expected["priority"] not in PRIORITIES and expected["priority"] is not None
            ) or (expected["kind"] not in KINDS and expected["kind"] is not None):
                reject("Invalid expected field values")
        elif set(expected) != {"present"}:
            reject("Absent item cannot specify expected fields")
    if not HEX_PATTERN.fullmatch(digest):
        reject("Approval digest must be 64 lowercase hex digits")
    actual = hashlib.sha256(canonical_json(request)).hexdigest()
    if actual != digest:
        reject("Request digest mismatch: request was edited or incorrect approval")
    return request


def https_json(url: str, token: str, body: dict | None = None) -> dict:
    headers = {"Accept": "application/vnd.github+json",
               "Authorization": f"Bearer {token}", "User-Agent": "dornglut-portfolio-writer"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = Request(url, headers=headers, data=canonical_json(body) if body is not None else None)
    try:
        with urlopen(request, timeout=30) as response:
            result = json.load(response)
    except (HTTPError, URLError, TimeoutError):
        raise RuntimeError("GitHub API request failed; credentials or endpoint may be unavailable") from None
    if not isinstance(result, dict) or result.get("errors"):
        raise RuntimeError("GitHub API returned invalid data or GraphQL errors")
    return result


def graph(token: str, query: str, variables: dict) -> dict:
    result = https_json("https://api.github.com/graphql", token, {"query": query, "variables": variables})
    if not isinstance(result.get("data"), dict):
        raise RuntimeError("GitHub GraphQL response has no data")
    return result["data"]


def issue_request(repo_token: str, number: int) -> str:
    issue = https_json(f"https://api.github.com/repos/dornglut/engineering/issues/{number}", repo_token)
    if issue.get("state") != "open" or "pull_request" in issue or not isinstance(issue.get("body"), str):
        reject("Request must be an open, ordinary Engineering issue")
    return issue["body"]


def read_project(api) -> tuple[dict, dict, dict]:
    cursor, seen, items, project_id, fields, total = None, set(), {}, None, None, None
    while True:
        data = api(PROJECT_QUERY, {"cursor": cursor})
        project = (data.get("organization") or {}).get("projectV2")
        if not isinstance(project, dict) or project.get("number") != 1 or project.get("public") is not True:
            reject("Project 1 absent or not public; do not mutate")
        if project_id is None:
            project_id = project["id"]
            if not project["url"].rstrip("/") == "https://github.com/orgs/dornglut/projects/1":
                reject("Unexpected project URL")
            config = project["fields"]
            if config["pageInfo"]["hasNextPage"]:
                reject("Field configuration not completely available")
            fields = {}
            for f in config["nodes"]:
                if f.get("name") not in {"Status", "Priority", "Kind"}:
                    continue
                if f["name"] in fields:
                    reject("Ambiguous duplicate field")
                if f["__typename"] != "ProjectV2SingleSelectField":
                    reject(f"{f['name']} must be single-select")
                options = f["options"]
                by_name = {o["name"]: o["id"] for o in options}
                if len(by_name) != len(options):
                    reject("Duplicate field option")
                fields[f["name"]] = {"id": f["id"], "options": by_name}
        elif project["id"] != project_id:
            reject("Project identity changed")
        connection = project["items"]
        if total is None:
            total = connection["totalCount"]
            if type(total) is not int or total > MAX_PROJECT_ITEMS or total < 0:
                reject("Project exceeds bounded item inventory")
        elif connection["totalCount"] != total:
            reject("Project changed size during pagination")
        for node in connection["nodes"]:
            if node["id"] in seen:
                reject("Repeated project item")
            seen.add(node["id"])
            values = node["fieldValues"]
            if values["pageInfo"]["hasNextPage"]:
                reject("Incomplete per-item field inventory")
            content = node.get("content")
            if not content:
                continue
            url = content.get("url")
            if isinstance(url, str) and url in items:
                reject("Duplicate content URL in project")
            if isinstance(url, str):
                fields_now = {"status": None, "priority": None, "kind": None}
                for f in values["nodes"]:
                    name = (f.get("field") or {}).get("name")
                    if name in {"Status", "Priority", "Kind"}:
                        if f["__typename"] != "ProjectV2ItemFieldSingleSelectValue":
                            reject("Unexpected field value type")
                        fields_now[name.lower()] = f.get("name")
                items[url] = {
                    "id": node["id"], "type": node["type"], "archived": node["isArchived"],
                    "private": (content.get("repository") or {}).get("isPrivate"),
                    "fields": fields_now,
                }
        info = connection["pageInfo"]
        if not info["hasNextPage"]:
            break
        next_cursor = info.get("endCursor")
        if not next_cursor or next_cursor == cursor or len(seen) >= MAX_PROJECT_ITEMS:
            reject("Non-advancing/incomplete pagination")
        cursor = next_cursor
    if len(seen) != total:
        reject("Project item count mismatch")
    return {"id": project_id, "total": total}, fields, items


def validate_target(api, url: str, desired_status: str) -> str:
    repo, kind, number = URL_PATTERN.fullmatch(url).groups()
    data = api(TARGET_QUERY, {"repo": repo, "number": int(number)})
    target_repo = data.get("repository")
    if not target_repo or target_repo.get("isPrivate") is not False:
        reject("Target must be in an existing public dornglut repository")
    obj = target_repo.get("issue" if kind == "issues" else "pullRequest")
    if not obj or obj.get("url") != url:
        reject("Target issue/PR not found or identity mismatch")
    if (obj["state"] == "OPEN") != (desired_status != "Done"):
        reject("Requested Status contradicts current issue/PR open state")
    return obj["id"]


def plan_changes(api, request: dict) -> dict:
    project, fields, items = read_project(api)
    if request["ensure_kind"]:
        if "Kind" in fields and set(fields["Kind"]["options"]) != set(KINDS):
            reject("Existing Kind options differ from governed contract")
        return {"project": project, "fields": fields, "changes": [],
                "create_kind": "Kind" not in fields}
    if "Status" not in fields or "Priority" not in fields:
        reject("Status and Priority must already be configured as single-select fields")
    changes = []
    for op in request["operations"]:
        content_id = validate_target(api, op["url"], op["status"])
        present = items.get(op["url"])
        expected = op["expected"]
        if (present is not None) != expected["present"]:
            reject(f"Project presence precondition failed: {op['url']}")
        if present is not None:
            if present["archived"] or present["private"] is not False:
                reject("Archived or private Project item cannot be modified")
            if present["type"] != ("ISSUE" if "/issues/" in op["url"] else "PULL_REQUEST"):
                reject("Project item type mismatch")
            if present["fields"] != {k: expected[k] for k in ("status", "priority", "kind")}:
                reject(f"Project field precondition failed: {op['url']}")
        for key in ("status", "priority", "kind"):
            val = op[key]
            field = fields.get(key.capitalize())
            if val is not None and (not field or val not in field["options"]):
                reject(f"Missing configured {key} option: {val}")
            if val is None and field is None and key != "kind":
                reject("Missing expected field")
        changes.append({"url": op["url"], "content_id": content_id,
                        "item_id": present["id"] if present else None,
                        "before": present["fields"] if present else None,
                        "after": {k: op[k] for k in ("status", "priority", "kind")}})
    return {"project": project, "fields": fields, "changes": changes, "create_kind": False}


def execute(api, request: dict, plan: dict, emit=print) -> None:
    project_id = plan["project"]["id"]
    if plan["create_kind"]:
        options = [{"name": name, "color": "GRAY", "description": name} for name in KINDS]
        result = api(CREATE_KIND, {"project": project_id, "options": options})
        if not (result.get("createProjectV2Field") or {}).get("projectV2Field", {}).get("id"):
            raise RuntimeError("Kind creation did not return an ID")
        emit("PORTFOLIO_WRITE_APPLIED: Kind field created")
    for index, change in enumerate(plan["changes"], 1):
        url = change["url"]
        item = change["item_id"]
        if item is None:
            added = api(ADD_ITEM, {"project": project_id, "content": change["content_id"]})
            item = ((added.get("addProjectV2ItemById") or {}).get("item") or {}).get("id")
            if not item:
                raise RuntimeError(f"Item add returned no identity: {url}")
        emit(f"PORTFOLIO_WRITE_BEGIN: {index}/{len(plan['changes'])} {url}")
        for name, value in change["after"].items():
            if change["before"] is not None and change["before"][name] == value:
                continue
            field = plan["fields"].get(name.capitalize())
            if field is None:
                if value is None:
                    continue
                raise RuntimeError(f"Configured field missing: {name}")
            if value is None:
                response = api(CLEAR_FIELD, {"project": project_id, "item": item, "field": field["id"]})
                if not (response.get("clearProjectV2ItemFieldValue") or {}).get("projectV2Item", {}).get("id"):
                    raise RuntimeError("Field clear returned no item")
            else:
                response = api(SET_FIELD, {"project": project_id, "item": item,
                                          "field": field["id"], "option": field["options"][value]})
                if not (response.get("updateProjectV2ItemFieldValue") or {}).get("projectV2Item", {}).get("id"):
                    raise RuntimeError("Field update returned no item")
        emit(f"PORTFOLIO_WRITE_APPLIED: {index}/{len(plan['changes'])} {url}")


def verify(api, plan: dict) -> None:
    _, fields, items = read_project(api)
    if plan["create_kind"]:
        if "Kind" not in fields or set(fields["Kind"]["options"]) != set(KINDS):
            raise RuntimeError("Kind creation verification failed")
    for change in plan["changes"]:
        item = items.get(change["url"])
        if not item or item["fields"] != change["after"]:
            raise RuntimeError(f"Post-write verification failed: {change['url']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue-number", type=int, required=True)
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--mode", choices=("plan", "apply"), required=True)
    args = parser.parse_args()
    if args.issue_number < 1 or os.getenv("GITHUB_ACTOR") != APPROVER:
        print("Writer rejected: unauthorized workflow actor or issue number", file=sys.stderr)
        return 2
    project_token = os.getenv("DORNGLUT_PROJECTS_WRITE_TOKEN", "")
    repo_token = os.getenv("GITHUB_TOKEN", "")
    if not project_token or not repo_token:
        print("Writer requires separate Projects write and repository read secrets", file=sys.stderr)
        return 2
    try:
        request = parse_request(issue_request(repo_token, args.issue_number), args.sha256)
        api = lambda query, vars: graph(project_token, query, vars)
        planned = plan_changes(api, request)
        print(f"PORTFOLIO_REQUEST_SHA256={args.sha256}")
        print(f"PORTFOLIO_MODE={args.mode}")
        print(f"PORTFOLIO_PREFLIGHT=PASS total_items={planned['project']['total']} "
              f"changes={len(planned['changes'])} create_kind={planned['create_kind']}")
        for op in planned["changes"]:
            print("PORTFOLIO_CHANGE=" + canonical_json({
                "url": op["url"], "before": op["before"], "after": op["after"]
            }).decode("ascii"))
        if args.mode == "plan":
            print("PORTFOLIO_NO_MUTATIONS=TRUE")
            return 0
        # Re-read entire Project and targets directly before the first mutation.
        planned = plan_changes(api, request)
        execute(api, request, planned)
        verify(api, planned)
        print("PORTFOLIO_APPLY_VERIFIED=TRUE")
        return 0
    except (RuntimeError, ValueError, KeyError, TypeError, IndexError) as error:
        # May be a partially applied remote batch. Never claim rollback or success.
        print(f"PORTFOLIO_ABORTED: {error}; if apply began, inspect the Project for partial writes",
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
