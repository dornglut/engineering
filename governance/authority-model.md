# Authority model

Dornglut uses explicit authorities so planning documents, issue trackers, automation, and implementation do not compete as parallel sources of truth.

## Authority by question

| Question | Authority |
|---|---|
| What does the software currently do? | Code and tests in the owning repository |
| What must pass before merge? | The owning repository's canonical validation command |
| What implementation work is active? | A local issue in the owning repository |
| What local architecture is durable? | An accepted repository decision record |
| What cross-repository decision is durable? | An accepted ADR in this repository |
| What outcome spans repositories? | An initiative in this repository with linked local issues |
| What is currently prioritized or scheduled? | Local issues and explicit initiative sequencing until the Engineering Portfolio is activated; the portfolio afterward |
| What changed in a delivery? | The pull request and its validation evidence |
| What defaults apply when a repository is silent? | `dornglut/.github` |
| How is shared CI orchestrated? | `dornglut/github-workflows` |

## Portfolio activation

The Dornglut Engineering Portfolio becomes the live authority for priority, status, sequencing, and dates only after the GitHub Project exists, its field model is accepted, and active repository issues are linked. Until then, local issues and explicit initiative sequencing remain authoritative.

## Precedence

More specific accepted authority overrides a broader default. Implementation cannot be overruled by a stale plan, and a live project board cannot silently change a durable architectural decision.

When authorities disagree:

1. stop work that depends on the conflict;
2. identify whether behavior, validation, local architecture, or organization policy is disputed;
3. correct the authority that owns that question;
4. record migration consequences;
5. resume implementation from an explicit accepted base.

## Historical evidence

Old owner paths, superseded decisions, and completed work may remain in provenance and reports. They must be labeled as historical and must not be used for new active links or implementation bases.
