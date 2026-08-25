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
- for agent-mediated repository changes, follow `standards/github.md`;
- when operating through GPT Web with the GitHub connector, also follow `tooling/gpt-web-github.md`;
- run `cargo validate` before proposing changes from a checked-out executor; when the selected procedure lacks local execution, use the exact-head CI path in `standards/validation.md`.
