# Public Dornglut Engineering Portfolio snapshot

This is a **derived, read-only observation**, never an issue, PR, roadmap, priority, or
Project authority. Source of truth: [Engineering Portfolio](https://github.com/orgs/dornglut/projects/1)
and the owned repository issues and PRs. A snapshot is dated; do not assume it is live.

## Purpose and boundaries

- Observe only organization project `dornglut/1` **when the GraphQL API verifies it is public**.
- Export Project view **names, numbers and layouts**, and three management fields:
  `Status`, `Priority`, `Kind`. Do not export view filters or free-form notes.
- Export only issues and PRs from repositories GitHub reports as public; never
  publish draft Project items, redacted items, or private repository content.
- Query all item pages. Fail instead of publishing partial pages or a false total.
- Publish a timestamped snapshot as structured log records, not repository commits,
  persistent generated markdown, a new PM database, or an automatically authoritative state.
- No Github API mutations, repository write permission, or automatic prioritization.
- The action logs are visible to people allowed to read workflow logs. Treat this
  as **public publication**, even though the source Project is already public.

## One-time credential (must be configured by an organization owner)

The ordinary Actions `GITHUB_TOKEN` cannot read org-level Projects v2. GitHub documents
an organization GitHub App with **organization Projects: read** as the preferred
machine credential. Alternatively, a suitably scoped personal token with read-only
Projects access can be used, subject to the organization's approval policy.

1. Obtain a token with **read-only organization Projects** permission for `dornglut`.
   Do not grant Projects write permission or repository Contents write permission.
2. Store its value as an **Actions secret**, named `DORNGLUT_PROJECTS_READ_TOKEN`, in the
   `dornglut/engineering` repository's **Settings → Secrets and variables → Actions**.
   Never paste the token in an issue, PR, chat, or workflow file.
3. After this PR is accepted and merged, open
   [Actions → Public portfolio snapshot](https://github.com/dornglut/engineering/actions/workflows/public-portfolio-snapshot.yml),
   select `Run workflow`, and inspect the `Read public Engineering Portfolio` job.
4. The workflow runs every six hours (UTC) and may be manually dispatched. Scheduled
   workflows on public GitHub repositories can be disabled after prolonged inactivity;
   check freshness before depending on a scheduled snapshot.

The first live authenticated run must establish that the token is authorized for
project 1 and that the graph/schema still matches GitHub's current API. Before that,
unit tests and CI alone **do not** qualify the export as operational.

## How ChatGPT reads it

Using the connected GitHub integration, fetch the most recent **successful** run of
`public-portfolio-snapshot.yml` via the repository Actions workflow-run API, then
fetch its `Read public Engineering Portfolio` job logs. Parse the records:

- `DORNGLUT_PORTFOLIO_START=`: source URL, timestamp, coverage, field names.
- `DORNGLUT_PORTFOLIO_VIEW=`: saved view identity/layout (not its complete filters).
- `DORNGLUT_PORTFOLIO_ITEM=`: one public issue or PR and its selected Project fields.
- `DORNGLUT_PORTFOLIO_END=`: item/view counts and SHA-256 of the canonical snapshot.

Only trust an observation when its matching end marker and counts are present. Recompute
SHA-256 after reconstructing `{ "meta": ..., "views": [...], "items": [...] }` with
sorted JSON keys and compact separators, or mark the snapshot unverified. Compare item
references against current live issue/PR data before asserting current acceptance.

The workflow intentionally avoids source pushes and GitHub Projects mutations. It
cannot edit custom Project fields or detect real-time changes between runs. It does
not represent private Inbox items. If a credential or schema check fails, there is no
new snapshot; previous observations must be reported with their original timestamp.

## Local validation

```sh
python3 -m unittest discover -s tests -p test_portfolio_snapshot.py -v
```

Full repository readiness remains owned by `cargo validate`. Tests use mocked GraphQL
data and do not exercise the real authenticated Projects API.
