#!/usr/bin/env python3
"""Publish a narrow, read-only public GitHub Projects v2 observation to job logs.

There are deliberately no GitHub write mutations, local snapshot files, or fallbacks
that silently omit incomplete API pages. Run only for a verified public project.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


# Only these non-sensitive operational fields leave the GraphQL response.
EXPORTED_FIELDS = frozenset({"Status", "Priority", "Kind"})
PAGE_SIZE = 50
MAX_ITEMS = 5000

PROJECT_QUERY = """
query PublicPortfolio($org: String!, $number: Int!, $cursor: String) {
  organization(login: $org) {
    projectV2(number: $number) {
      id number title url public updatedAt
      views(first: 100) {
        pageInfo { hasNextPage }
        nodes { number name layout }
      }
      fields(first: 100) {
        pageInfo { hasNextPage }
        nodes {
          __typename
          ... on ProjectV2Field { name }
          ... on ProjectV2SingleSelectField { name }
          ... on ProjectV2IterationField { name }
          ... on ProjectV2MultiSelectField { name }
        }
      }
      items(first: 50, after: $cursor) {
        totalCount
        pageInfo { hasNextPage endCursor }
        nodes {
          id type isArchived updatedAt
          content {
            __typename
            ... on Issue {
              title url number state
              repository { nameWithOwner isPrivate }
            }
            ... on PullRequest {
              title url number state isDraft
              repository { nameWithOwner isPrivate }
            }
          }
          fieldValues(first: 100) {
            pageInfo { hasNextPage }
            nodes {
              __typename
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field {
                  ... on ProjectV2Field { name }
                  ... on ProjectV2SingleSelectField { name }
                  ... on ProjectV2IterationField { name }
                  ... on ProjectV2MultiSelectField { name }
                }
              }
              ... on ProjectV2ItemFieldTextValue {
                text
                field {
                  ... on ProjectV2Field { name }
                  ... on ProjectV2SingleSelectField { name }
                  ... on ProjectV2IterationField { name }
                  ... on ProjectV2MultiSelectField { name }
                }
              }
              ... on ProjectV2ItemFieldNumberValue {
                number
                field {
                  ... on ProjectV2Field { name }
                  ... on ProjectV2SingleSelectField { name }
                  ... on ProjectV2IterationField { name }
                  ... on ProjectV2MultiSelectField { name }
                }
              }
            }
          }
        }
      }
    }
  }
}
"""


def graphql_request(token: str, query: str, variables: dict) -> dict:
    body = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "User-Agent": "dornglut-public-portfolio-observer",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError):
        # Don't print the untrusted response, token-bearing request, or API fields.
        raise RuntimeError("GitHub GraphQL request failed; check credential and permissions") from None
    if not isinstance(payload, dict) or payload.get("errors") or not isinstance(payload.get("data"), dict):
        raise RuntimeError("GitHub GraphQL returned an error or invalid data; no snapshot published")
    return payload["data"]


def observe(api, org: str, number: int, observed_at: str) -> dict:
    """API accepts (GraphQL query, variables) and returns the GraphQL `data` object."""
    items = []
    seen = set()
    cursor = None
    project_metadata = None
    views = []
    fields = []
    total = None
    while True:
        data = api(PROJECT_QUERY, {"org": org, "number": number, "cursor": cursor})
        project = (data.get("organization") or {}).get("projectV2")
        if not isinstance(project, dict):
            raise ValueError("Specified organization Project was not accessible")
        if project.get("public") is not True:
            raise ValueError("Project is not public; refusing to publish any field values to logs")
        if project.get("number") != number:
            raise ValueError("Unexpected project identity")
        identity = (project.get("id"), project.get("url"), project.get("title"))
        if project_metadata is None:
            project_metadata = identity
            for collection_name in ("views", "fields"):
                collection = project[collection_name]
                if collection["pageInfo"]["hasNextPage"]:
                    raise ValueError(f"Project {collection_name} exceeds the bounded first page")
            views = sorted(
                ({"number": v["number"], "name": v["name"], "layout": v["layout"]}
                 for v in project["views"]["nodes"]),
                key=lambda view: view["number"],
            )
            fields = sorted({v["name"] for v in project["fields"]["nodes"] if v.get("name") in EXPORTED_FIELDS})
        elif identity != project_metadata:
            raise ValueError("Project changed during pagination")
        connection = project["items"]
        if total is None:
            total = connection["totalCount"]
            if not isinstance(total, int) or not 0 <= total <= MAX_ITEMS:
                raise ValueError("Project item count outside bounded export limit")
        elif total != connection["totalCount"]:
            raise ValueError("Project changed size during pagination; retry a fresh run")
        nodes = connection["nodes"]
        if not isinstance(nodes, list):
            raise ValueError("Missing Project items page")
        for node in nodes:
            item_id = node["id"]
            if item_id in seen:
                raise ValueError("Duplicate item encountered during pagination")
            seen.add(item_id)
            values = node["fieldValues"]
            if values["pageInfo"]["hasNextPage"]:
                raise ValueError("Item has more than 100 fields; refusing incomplete export")
            content = node.get("content")
            # REDACTED and draft items are never published. Likewise private repos.
            if node.get("type") not in {"ISSUE", "PULL_REQUEST"}:
                continue
            if not content or content.get("__typename") not in {"Issue", "PullRequest"}:
                continue
            repository = content.get("repository") or {}
            if repository.get("isPrivate") is not False:
                continue
            result_fields = {}
            for value in values["nodes"]:
                field_name = (value.get("field") or {}).get("name")
                if field_name not in EXPORTED_FIELDS:
                    continue
                ty = value["__typename"]
                if ty == "ProjectV2ItemFieldSingleSelectValue":
                    result_fields[field_name] = value.get("name")
                elif ty == "ProjectV2ItemFieldTextValue":
                    result_fields[field_name] = value.get("text")
                elif ty == "ProjectV2ItemFieldNumberValue":
                    result_fields[field_name] = value.get("number")
                else:
                    raise ValueError(f"Unsupported type for exported field: {field_name}")
            items.append({
                "project_item_id": item_id,
                "type": node["type"],
                "archived": node["isArchived"],
                "project_item_updated_at": node["updatedAt"],
                "repository": repository["nameWithOwner"],
                "number": content["number"],
                "title": content["title"],
                "url": content["url"],
                "state": content["state"],
                "draft_pr": content.get("isDraft") if node["type"] == "PULL_REQUEST" else None,
                "fields": result_fields,
            })
        page = connection["pageInfo"]
        if not page["hasNextPage"]:
            break
        next_cursor = page.get("endCursor")
        if not next_cursor or next_cursor == cursor or len(seen) >= MAX_ITEMS:
            raise ValueError("Project pagination is incomplete or not advancing")
        cursor = next_cursor
    if len(seen) != total:
        raise ValueError("Project item total mismatch; refusing a partial snapshot")
    items.sort(key=lambda item: (item["repository"], item["number"], item["type"]))
    return {
        "meta": {
            "schema_version": 1,
            "observed_at_utc": observed_at,
            "organization": org,
            "project_number": number,
            "project_title": project_metadata[2],
            "project_url": project_metadata[1],
            "project_public": True,
            "total_project_items": total,
            "exported_public_issue_pr_count": len(items),
            "excluded_draft_private_redacted_count": total - len(items),
            "exported_project_fields": fields,
            "source": "GitHub Projects v2 GraphQL; non-authoritative read-only observation",
        },
        "views": views,
        "items": items,
    }


def emit_log(snapshot: dict, output) -> None:
    """Each record is single-line bounded JSON, readable from GitHub job logs."""
    encode = lambda obj: json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    digest = hashlib.sha256(encode(snapshot).encode("utf-8")).hexdigest()
    print("DORNGLUT_PORTFOLIO_START=" + encode(snapshot["meta"]), file=output)
    for view in snapshot["views"]:
        print("DORNGLUT_PORTFOLIO_VIEW=" + encode(view), file=output)
    for item in snapshot["items"]:
        print("DORNGLUT_PORTFOLIO_ITEM=" + encode(item), file=output)
    print("DORNGLUT_PORTFOLIO_END=" + encode({
        "views": len(snapshot["views"]), "items": len(snapshot["items"]), "sha256": digest,
    }), file=output)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--organization", default="dornglut")
    parser.add_argument("--project", type=int, default=1)
    args = parser.parse_args()
    token = os.environ.get("DORNGLUT_PROJECTS_READ_TOKEN", "")
    if not token:
        print("Missing DORNGLUT_PROJECTS_READ_TOKEN Actions secret; no snapshot generated", file=sys.stderr)
        return 2
    try:
        snapshot = observe(
            lambda query, variables: graphql_request(token, query, variables),
            org=args.organization,
            number=args.project,
            observed_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )
        emit_log(snapshot, sys.stdout)
    except (ValueError, RuntimeError, KeyError, TypeError) as exc:
        print(f"Portfolio snapshot aborted: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
