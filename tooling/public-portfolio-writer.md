# Approval-controlled Engineering Portfolio writer

The [public Engineering Portfolio](https://github.com/orgs/dornglut/projects/1)
owns current priority and status. This writer is a **manual, explicit approval path**
for the already accepted Governance contract; it is not another operational database,
priority recommendation engine or background mutator.

Its actor restrictions and bounded GitHub Projects v2 GraphQL operations are deliberately
different from the read-only [snapshot](public-portfolio-snapshot.md) workflow.

## Security and authorization

1. Use a **separate** organization Projects **read/write** token for
   `DORNGLUT_PROJECTS_WRITE_TOKEN`, created by the owner in the
   [Engineering repository's Actions secrets](https://github.com/dornglut/engineering/settings/secrets/actions).
   Do not reuse or replace the read-only `DORNGLUT_PROJECTS_READ_TOKEN`.
   No repository Contents write or other org permissions are needed.
2. The writer has **no scheduled, issue, label or comment triggers**. Only
   `workflow_dispatch` from accepted `main` by the GitHub account
   `aschenrot` can run the credentialed job.
3. The operator explicitly enters an open issue number, a **SHA-256 digest** of the
   exact canonical request JSON, and `plan` or `apply`. A changed request cannot
   be applied under the old digest. The issue must be an ordinary **open** issue in
   `dornglut/engineering`.
4. The workflow uses its read-only repository `GITHUB_TOKEN` to read the
   request issue, and the separate Projects writer token only for GraphQL. It never
   grants GitHub contents, issues or PRs write permission to the workflow.
5. The request issue is an **approval/audit artifact**, not accepted work, a second
   portfolio authority, or automatically added to the Project. The user reviews the
   exact proposed values; no requested priority is inferred from GitHub issue order.
6. `plan` verifies public Project identity, existing fields and options, source
   issue/PR identity and state, current Project item presence and expected values.
   `plan` does **not** modify GitHub Projects. `apply` repeats preflight
   before mutating, serializes writers and verifies all resulting target values.
7. Changes that race with external Project edits cannot be fully prevented: GitHub
   exposes no atomic compare-and-swap for a multi-field batch. Each update is
   non-transactional. An error can leave a **partially applied batch**, whose exact
   result must be inspected and reconciled before retrying with a new request.
   A guarded, normal user authorization is not a claim of atomicity.

## Request format

Create an ordinary temporary issue in `dornglut/engineering` with a short title
such as `Portfolio request: native UI critical path`. The **entire issue body**
must consist of exactly one fenced JSON block, with no other text. For example:

```json
{
  "schema": 1,
  "project": "dornglut/1",
  "ensure_kind": false,
  "operations": [
    {
      "url": "https://github.com/dornglut/runenwerk/issues/1276",
      "status": "Blocked",
      "priority": "P1",
      "kind": "Delivery",
      "expected": {
        "present": false
      }
    }
  ]
}
```

The example is **not an approved prioritization**; it demonstrates syntax only.

The digest is calculated from the parsed request JSON, sorted-key compact JSON,
ASCII escaped, without the Markdown fence. For a local issue body saved in
`request-body.md`, calculate:

```sh
python3 - request-body.md <<'PY'
import hashlib
import json
import pathlib
import re
import sys
body = pathlib.Path(sys.argv[1]).read_text()
match = re.fullmatch(r'\s*```json\s*\n([\s\S]*?)\n```\s*', body)
if match is None:
    raise SystemExit('invalid request fence')
request = json.loads(match.group(1))
encoded = json.dumps(request, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode()
print(hashlib.sha256(encoded).hexdigest())
PY
```

ChatGPT may generate the request issue and the digest for review; the human must still
inspect the exact issue contents and manually dispatch the workflow. A request is
limited to **20 distinct public Dornglut issues or PRs**. Allowed fields are:

| Field | Allowed desired values |
| --- | --- |
| `Status` | `Ready`, `In progress`, `Blocked`, `Done` |
| `Priority` | `P0`, `P1`, `P2`, `P3` or `null` (clear) |
| `Kind` | `Decision`, `Investigation`, `Delivery`, `Maintenance` or `null` (clear) |

When an item is already in the Project, its `expected` MUST contain all four
keys `present: true`, `status`, `priority`, `kind`, matching the **live**
Project exactly (use JSON `null` for currently blank). A new item has
`expected: {"present": false}`. The request fails without writes if expected
values no longer match, if the source issue/PR identity is invalid, or if a
non-Done requested status contradicts a closed source issue/PR. Existing items
may not be archived or belong to private repositories.

A separate **one-time** request can create the missing governance-required
single-select `Kind` field (and nothing else):

```json
{"schema":1,"project":"dornglut/1","ensure_kind":true,"operations":[]}
```

If `Kind` already exists with exactly the accepted four options, this is a
no-op. It does **not** edit, delete or overwrite any existing field or options.
If Status or Priority is missing a desired option, the writer stops and reports
the discrepancy rather than silently changing its configuration.

## Approval workflow

1. Read the request issue and confirm every proposed change, especially Priority,
   expected state and the absence of private data.
2. Open [Actions → Public portfolio writer](https://github.com/dornglut/engineering/actions/workflows/public-portfolio-writer.yml),
   click **Run workflow**, select `main`, and enter the **request issue number** and
   its **exact SHA-256**; choose `plan` (default).
3. Review the successful `PORTFOLIO_PREFLIGHT` and each `PORTFOLIO_CHANGE`
   record in the **Manually approved portfolio request** job logs. This is the
   verified proposed diff, not a mutation or user approval of a different request.
4. Re-dispatch with the same number and SHA-256, selecting **`apply`** to approve
   this exact batch. The writer repeats preflight, applies only planned changes
   and re-reads the Project. Require `PORTFOLIO_APPLY_VERIFIED=TRUE`.
5. Run or await the independent [read-only portfolio snapshot](https://github.com/dornglut/engineering/actions/workflows/public-portfolio-snapshot.yml),
   read its dated markers/fields in GPT Web, and reconcile actual values against
   the approved request. Close the temporary request issue after verification if
   its audit history is complete. Do not mistake a dry-run for a completed write.

A failed `apply` may have written **some** operations. Never blindly retry after
failure: inspect live fields, create a new request with updated expectations, and
require a new digest and explicit operator approval.

## Local test

```sh
python3 -m unittest discover -s tests -p test_portfolio_writer.py -v
```

`cargo validate` remains the separate canonical Engineering validation.
Unit tests use mocked GraphQL and **cannot** qualify production write permission,
real token scopes, schema evolution, or the first authenticated mutation.
