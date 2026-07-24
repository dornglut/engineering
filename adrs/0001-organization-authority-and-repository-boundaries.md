# ADR 0001: Organization authority and repository boundaries

- Status: accepted
- Date: 2026-07-22
- Owner: Dornglut organization
- Scope: organization-wide

## Context

Dornglut owns multiple related framework repositories and expects additional extractions. Repository-local implementation, cross-repository architecture, shared contribution defaults, and CI orchestration require distinct authorities to avoid duplicated planning and hidden ownership.

## Decision

Dornglut adopts three organization repositories:

- `.github` for inherited contribution and community defaults;
- `engineering` for cross-repository governance, architecture, initiatives, and ADRs;
- `github-workflows` for reusable CI orchestration.

Product repositories retain implementation, validation semantics, releases, compatibility, local decisions, and issue ownership.

Dornglut will establish an Engineering Portfolio for live priority, status, sequencing, and dates. It becomes authoritative only after the GitHub Project exists and the activation criteria in [Authority and work](../governance/authority-and-work.md) are satisfied. It never replaces durable ADRs or repository-local issues.

## Consequences

- shared defaults cannot redefine product behavior;
- shared workflows invoke repository commands rather than duplicate validation logic;
- cross-repository outcomes link to local implementation issues;
- historical owner paths remain provenance only;
- new repositories must declare ownership and avoid duplicate source authority;
- portfolio state is not treated as active authority before explicit activation.
