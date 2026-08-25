# Agent instructions

Scope: cross-repository governance, organization standards, and shared architecture.

Start with:

1. `governance/authority-and-work.md`;
2. the relevant file under `standards/`;
3. `architecture/runen-family.md` when repository boundaries or extraction order are involved;
4. the owning ADR, initiative, issue, and pull request.

Rules:

- do not implement product behavior in this repository;
- do not duplicate repository-local roadmaps, issue bodies, generated state, or validation output;
- do not mirror changing GitHub priority or branch state in durable Markdown;
- separate durable decisions from dated reports and operational Project state;
- cross-repository claims must identify the owning repository and evidence;
- historical paths remain historical; active links use the `dornglut/*` namespace;
- preserve bidirectional ADR supersession and initiative closure records;
- when authoring repository changes through GPT Web, follow the GPT Web repository publication rules in `standards/validation.md`;
- run `cargo validate` before proposing changes from a checked-out executor; when GPT Web cannot execute it locally, use the draft-PR exact-head CI path defined in `standards/validation.md`.
