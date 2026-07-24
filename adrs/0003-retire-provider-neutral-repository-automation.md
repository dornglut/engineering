# ADR 0003: Retire provider-neutral repository automation

- Status: accepted
- Date: 2026-07-24
- Owner: Dornglut organization
- Scope: organization-wide repository execution and automation

## Context

ADR 0002 authorized a dedicated `dornglut/forgeops` repository and a provider-neutral protocol for preparing and publishing repository changes. The proposal was created in response to a temporary limitation encountered during one Runenwerk pull request.

Subsequent work showed that this program would create a large permanent platform before Dornglut had a sustained need for one. It would add protocol, conformance, adapter, credential, publication, and operational responsibilities while delaying product work. The repository was never created and no product adopted the proposed protocol.

Dornglut now has a simpler working model:

- GitHub issues and pull requests own reviewable work and delivery evidence;
- each repository owns its code, tests, validation semantics, releases, and local decisions;
- `dornglut/github-workflows` provides reusable read-only CI orchestration;
- ChatGPT web with the GitHub connector handles structured GitHub operations and bounded repository edits;
- a checked-out local coding agent handles broad source transformations and local validation;
- the GitHub interface handles native organization settings and Projects that are not exposed through the connector.

These tools are execution choices, not durable architectural authorities. Replacing one tool does not require a new organization-wide repository protocol.

## Decision

Dornglut retires the provider-neutral repository automation program established by ADR 0002.

The organization will not create `dornglut/forgeops`, require a change-bundle protocol, or block product delivery on an automation-platform canary.

Repository work uses the smallest suitable execution path:

1. structured GitHub state changes and bounded text edits may use the connected GitHub interface;
2. broad, generated, binary, or validation-heavy changes use a checked-out repository executor;
3. organization settings and Project configuration use the native GitHub interface when no reviewed automation surface exists;
4. all implementation is delivered through ordinary task branches and pull requests;
5. repository-owned validation and exact-head CI remain independent of the authoring tool.

The following safety rules remain mandatory:

- validation workflows remain read-only and do not author source;
- proposed work does not push directly to a protected default branch;
- merges use reviewed exact-head evidence;
- issue text or model output does not grant arbitrary command or repository authority;
- temporary transport or source-export workflows are not introduced to compensate for an authoring-tool limitation;
- product repositories do not depend on ChatGPT, a connector, a local agent, or another authoring tool to build, test, release, or consume the product.

A future automation platform requires a new organization ADR supported by repeated operational evidence, a bounded first use case, an explicit maintenance owner, and proof that ordinary repository tooling is insufficient.

## Alternatives considered

### Continue ADR 0002 as planned

Rejected. The planned platform is disproportionate to current organization scale and would create a new critical path unrelated to product outcomes.

### Keep ForgeOps as a deferred plan

Rejected. A deferred accepted authority would continue to distort sequencing and imply that product work depends on a repository that does not exist.

### Standardize on one permanent authoring tool

Rejected. Authoring tools remain replaceable execution choices. Durability comes from Git, repository-owned validation, pull-request evidence, and explicit authority boundaries.

### Permit source-writing validation workflows

Rejected. Validation must remain independent from authorship and publication.

## Consequences

- product work is no longer blocked by a ForgeOps protocol, repository, adapter, or canary;
- Dornglut keeps a mixed execution model selected by task characteristics;
- repository-local validation remains the merge baseline;
- `github-workflows` remains narrowly read-only;
- authoring-tool limitations must be handled by choosing another executor rather than changing product architecture;
- the detailed ForgeOps architecture is removed from active engineering architecture and remains available through Git history;
- future automation work must justify itself through a new decision rather than reviving ADR 0002 implicitly.

## Affected repositories

- `dornglut/engineering`
- `dornglut/github-workflows`
- all maintained Dornglut product and framework repositories

No `dornglut/forgeops` repository exists or is required.

## Adoption or migration

1. Mark ADR 0002 as superseded by this ADR.
2. Cancel and close the provider-neutral repository automation initiative.
3. Remove the repository-automation document from active architecture.
4. Reclassify engineering issue #2 as not planned because its implementation program was retired.
5. Continue RunenSDF, RunenGPU, RunenRender, RunenECS, and organization-normalization work through their owning repositories and ordinary pull requests.

## Supersedes

[ADR 0002 — Provider-neutral repository automation](0002-provider-neutral-repository-automation.md)

## Superseded by

None.
