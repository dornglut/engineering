# ADR 0008: Adopt bounded source-authority handoffs for cross-repository transfers

- Status: accepted
- Date: 2026-09-05
- Owner: Dornglut organization
- Scope: Cross-repository source extraction and consumer cutover

## Context

Dornglut requires extracted frameworks to become independently accepted repositories while downstream consumers migrate away from the predecessor implementation without moving-branch dependencies, compatibility facades, source mirrors, or duplicate long-term implementation authority.

A literal rule that no accepted intermediate state may contain both the newly accepted implementation and the predecessor source copy is not implementable with ordinary independent-repository acceptance. Accepting the successor first necessarily leaves the predecessor copy present until downstream cutover. Accepting the downstream first would require an accepted dependency on an unaccepted successor revision.

The existing repository transfer sequence already requires accepting the transferred implementation before consumer migration and predecessor-source deletion. The missing distinction is between physical source presence and semantic source authority.

## Decision

Dornglut adopts an **external-first bounded source-authority handoff** for cross-repository source transfers with live downstream consumers.

### Source authority

At every point there is exactly one **semantic source authority** for the transferred behavior: the repository in which semantic, API, capability, correctness, and implementation changes may be accepted.

A predecessor repository may temporarily retain a **frozen predecessor copy** after successor acceptance solely so current consumers remain buildable until the already-authorized cutover completes. A frozen predecessor copy is not semantic authority and must not receive independent behavior, API, capability, correctness, or implementation changes.

Physical duplication during this bounded interval is therefore not equivalent to dual authority. The final accepted state still requires one implementation copy and no forwarding or compatibility path.

### Handoff sequence

The canonical sequence is:

1. Correct and census the source boundary in the current owning repository.
2. Build the successor repository candidate on an unmerged branch while the predecessor remains the sole semantic source authority.
3. Validate and accept the successor through its normal repository workflow.
4. The accepted successor default-branch revision becomes the sole semantic source authority immediately on acceptance. The predecessor copy becomes frozen.
5. Migrate downstream consumers to an exact accepted successor revision or exact accepted release and delete the predecessor source/namespace in the same downstream cutover boundary.
6. Prove the final state contains no predecessor implementation, forwarding package/module, alias, source include, submodule, moving-branch dependency, backend/private reach-through, or other duplicate authority.
7. Close provenance, release, and cross-repository coordination authority.

The downstream dependency pins the **accepted successor revision** created by repository acceptance, not the previously reviewed feature-head revision. Squash merge therefore remains compatible with this handoff. A tag, pre-release, or repository-specific merge-mode exception is optional only when independently required for release policy; it is not required merely to make the transfer reachable.

### Publication-overlap rules

After successor acceptance and before downstream cutover acceptance:

- no new semantic or implementation work may be accepted against the predecessor copy;
- predecessor changes are limited to consumer migration, integration adaptation, source deletion, and evidence required to complete the cutover;
- a missing reusable contract or extraction defect is corrected in the successor repository, accepted there, and the downstream cutover is repinned to the new exact accepted successor revision;
- successor changes to the transferred boundary are limited to cutover-blocking extraction corrections, urgent security/correctness fixes to the accepted contract, or validation/release corrections required to finish the transfer;
- unrelated successor feature or capability evolution for the transferred boundary waits until predecessor deletion is accepted;
- unrelated predecessor work may continue only when it does not modify the frozen transferred source or undermine the cutover assumptions;
- the cutover remains the next source-authority transition for that transferred boundary.

This bounded publication overlap is one transfer interval: successor acceptance to downstream cutover acceptance or explicit transfer reversal. It may not span ordinary feature evolution of the transferred boundary and must not become a maintenance mode or mirror.

### Failure and rollback

Before successor acceptance, rollback is ordinary abandonment of the unmerged successor candidate.

After successor acceptance, the successor remains semantic source authority. Correct defects there and continue the downstream cutover. Do not patch the frozen predecessor as an alternate implementation.

If the transfer must be cancelled after successor acceptance, cancellation requires a separately accepted reversal that retires the successor implementation authority before the predecessor may resume semantic source changes. A stalled cutover is marked blocked rather than silently restoring dual writable authority.

### Cross-repository coordination

When the existing Engineering initiative criteria are satisfied, activate one Engineering initiative before successor source acceptance. It links the repository-local transfer and cutover issues and owns cross-repository sequencing, failure/rollback disposition, and closure evidence. Repository-local issues continue to own implementation and validation.

## Alternatives considered

### Require zero physical overlap at every accepted intermediate state

Rejected. Independent repository acceptance cannot both accept the successor implementation and migrate a downstream consumer to that accepted revision atomically. The rule would force either an unaccepted dependency or an impossible cross-repository transaction.

### Accept the downstream cutover against an unmerged successor head

Rejected. This makes an unaccepted feature head dependency authority and conflicts with exact accepted dependency rules.

### Use a moving branch during handoff

Rejected. Moving branch dependencies weaken reproducibility and exact-revision review.

### Require merge commits or permanent tags for every transfer

Rejected as a universal requirement. The accepted squash commit itself is immutable accepted repository history and can be pinned exactly. Tags or alternate merge modes remain available only when a repository's release policy independently requires them.

### Keep both implementations writable until migration finishes

Rejected. That is genuine dual authority and creates semantic drift, review ambiguity, and long-lived mirror risk.

## Consequences

- Cross-repository transfers become implementable with ordinary GitHub pull-request and squash-merge workflow.
- A short accepted interval may contain both the new implementation and a frozen predecessor copy, but only the successor is writable semantic authority.
- The transferred boundary is serialized during the publication-overlap interval; ordinary successor feature evolution resumes only after predecessor deletion.
- The predecessor cutover is intentionally serialized with successor acceptance and may not be deferred into ordinary feature maintenance.
- Missing contracts discovered during migration are fixed in the successor rather than preserving or evolving the predecessor implementation.
- Final-state clean-cutover guarantees remain unchanged.

## Affected repositories

This rule applies to Dornglut repository extractions and source-authority transfers where a successor repository becomes the reusable implementation owner while one or more predecessor consumers still contain the old implementation. It applies immediately to planned RunenGPU extraction and to future RunenRender, RunenECS, or equivalent transfers unless a later accepted decision defines a more specific mechanism.

## Adoption or migration

1. Treat `governance/authority-and-work.md` initiative criteria as sufficient; no initiative-policy change is required.
2. Treat `standards/github.md` exact-head and accepted-squash definitions as sufficient; downstream pins the accepted successor revision, so no merge-mode exception is required.
3. Treat `standards/repositories.md` transfer ordering as the base lifecycle and interpret its accepted-transfer-before-consumer-migration sequence through this ADR's semantic-authority/frozen-copy distinction.
4. Treat `architecture/runen-family.md` extraction order as consistent with this decision; repository-local cutover authority must be reconciled before source movement.
5. Do not weaken final-state duplicate-source, forwarding, compatibility, or moving-branch prohibitions.

## Supersedes

None.

## Superseded by

None.
