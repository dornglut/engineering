# Dornglut documentation and validation authority audit

- Date: 2026-08-01
- Scope: organization documentation, validation entrypoint, and repository-family evidence
- Policy authority: the linked standards, ADRs, and architecture documents; this report is evidence only

## Evidence classes

- **Source-inspected fact**: observed in the accepted repository source or documentation.
- **Connected GitHub observation**: observed through the connected GitHub account on this date.
- **Historical evidence**: accepted issue, pull request, or immutable revision recorded for context.
- **Inference**: a conclusion drawn from the scoped evidence, not a claim of uninspected runtime behavior.
- **Unavailable evidence**: native state not exposed or not inspected for this audit.

## Coverage

| Repository | Evidence | Current observation | Disposition |
|---|---|---|---|
| `dornglut/.github` | Connected GitHub observation | Maintained organization repository exists | No source change in this work |
| `dornglut/engineering` | Source-inspected fact | Python-specific validator was the canonical entrypoint; issue #20 was closed while its initiative remained active | Replace with local `cargo validate`; reconcile initiative lifecycle |
| `dornglut/github-workflows` | Source-inspected fact | Immutable Rust reusable workflow selects and proves the caller head, remains read-only, and invokes fixed Cargo validation | Engineering caller can adopt it without a workflow-library change |
| `dornglut/runenwerk` | Source-inspected fact and connected GitHub observation | Accepted source has no tracked `domain/sdf` package or workspace member; issue #133 and PR #157 record retirement | Treat RunenSDF clean cutover as complete |
| `dornglut/runen-ui` | Connected GitHub observation | Maintained peer repository | No source change in this work |
| `dornglut/runen-sdf` | Source-inspected fact | Standalone Rust framework uses the shared Rust-validation profile | Retain standalone ownership |
| `dornglut/runen-spatial` | Source-inspected fact | Host-neutral Rust framework for neutral spatial mechanics; Runenwerk cutover is not complete | Add to organization family inventory |
| `dornglut/werkstatt` | Source-inspected fact | Experimental human-first workbench product pilot; W2B remains bounded read-only observation | Classify as application; keep maturity in product documentation |

## Validation migration parity

| Former Python check | Disposition |
|---|---|
| Required and forbidden paths; UTF-8, newline, whitespace, tabs, and repository-relative links | Ported unchanged |
| Workflow inventory, read-only caller shape, and immutable reusable-workflow pin | Ported unchanged, with the Rust caller pin |
| Historical owner and volatile authority restrictions | Ported unchanged |
| ADR filename, metadata, sections, numbering, index, status, and bidirectional supersession | Ported unchanged |
| Initiative filename, metadata, status, index, and closure validation | Corrected to generic lifecycle validation |
| Named verified-head initiative status, closure phrase, repository set, and revision | Removed because each encoded one historical state |

The Engineering interface is now `cargo validate`, backed by a repository-local Rust
`xtask`. Its shared workflow is a read-only caller; it does not receive validation
policy, arbitrary commands, paths, secrets, or toolchain inputs.

## Promoted corrections

- The verified-head initiative closure is reconciled with closed engineering issue #20.
- Repository taxonomy adds the accepted `application` profile and maps current
  Werkstatt operational vocabulary without rewriting ADR 0005 history.
- Repository-family architecture records RunenSpatial and Werkstatt, and records the
  RunenSDF retirement only after source inspection corroborated the closed issue.
- Material review reconciliation, post-merge closure reconciliation, and maintained
  repository admission reconciliation are promoted into organization standards.

## Inferences and repository-local follow-up

The fixed shared Rust workflow's `cargo +stable validate` invocation is compatible
with Engineering's `stable` toolchain and `cargo validate` alias; it does not alter
Engineering validation semantics. The initial audit could not verify native ruleset
state. Direct native Engineering repository administration subsequently verified only
the active `Protect main` ruleset and migrated its required context from
`validate / validate` to `validate / Repository baseline`, preserving its remaining
rules. This is repository-specific migration evidence, not an organization-wide
ruleset claim.

No product or framework repository is modified here. Any repository-local adoption of
the new Engineering documentation contracts, status naming, or validation interface is
separate work owned by that repository.

## Unavailable evidence

This audit did not verify organization-wide rulesets, actual custom-property values,
private Project configuration, secrets, local unpushed branches, or unexercised runtime
behavior. It also does not claim accepted-main CI evidence for this unmerged Engineering
change.
