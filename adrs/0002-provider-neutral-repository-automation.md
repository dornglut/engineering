# ADR 0002: Provider-neutral repository automation

- Status: superseded
- Date: 2026-07-22
- Owner: Dornglut organization
- Scope: organization-wide repository automation

## Context

Dornglut needs repository work to remain hands-off for the maintainer without requiring a local coding agent. The first connector-driven organization bootstrap proved that GitHub inspection, issue and pull-request management, and bounded file changes can be performed remotely. Runenwerk pull request #138 then exposed the missing boundary: the current connector is not a complete checked-out repository executor and a temporary source-export workflow was introduced to transport one large file.

That workaround preserved read-only CI but mixed product delivery with tool-specific transport, added an invalid intermediate file to the product pull request, and made ChatGPT plus the current connector an implicit architectural dependency.

Dornglut requires a system that can use ChatGPT today while remaining replaceable at the model, workspace, forge, and publication layers. It must support GitHub-hosted public repositories at zero mandatory infrastructure subscription, but it must not assume permanently free model inference or permanent GitHub availability.

## Decision

Dornglut will establish a dedicated public repository named `forgeops` for provider-neutral repository automation.

The authority boundaries are:

- `engineering` owns organization-wide policy, architecture, protocols, and accepted decisions;
- `forgeops` owns executable provider-neutral automation, protocol schemas, conformance tests, and forge adapters;
- `github-workflows` owns thin GitHub Actions orchestration and reusable validation callers;
- product repositories own implementation, tests, public APIs, repository-local decisions, releases, and the meaning of their canonical validation command.

The provider-neutral core will model these concepts:

- `WorkOrder`: authorized outcome, scope, constraints, acceptance criteria, and stop conditions;
- `RepositoryRevision`: forge-neutral repository identity plus immutable base revision;
- `ChangeBundle`: deterministic path operations against exact expected prior content;
- `ExecutionEvidence`: commands, environment, inputs, outputs, and hashes produced by an executor;
- `PublicationReceipt`: the resulting revision, branch, forge references, and verification result.

The system will separate five capabilities:

1. a work source supplies an authorized `WorkOrder`;
2. an optional reasoner proposes decisions or transformations;
3. an executor operates in an isolated workspace and emits a `ChangeBundle` plus `ExecutionEvidence`;
4. a publisher verifies and applies the bundle only to an authorized task branch;
5. an independent validator checks the published exact head through the repository-owned validation contract.

A reasoner may be GPT, another hosted model, an open model, a deterministic transformer, or a human. No model-provider concept may appear in the provider-neutral core domain.

A forge may be GitHub, Forgejo, GitLab, or plain Git. GitHub API objects and workflow events may appear only in adapters.

Validation workflows remain read-only. A separately authorized publisher may write task branches, but it must not execute proposed repository code, push directly to a protected default branch, or merge its own output.

Every publication must fail closed unless all of the following hold:

- repository identity and target branch are authorized;
- the current base revision equals the work order and bundle base revision;
- every changed path is allowed;
- every expected previous content hash matches;
- the bundle schema and protocol version are supported;
- file count and payload size limits are respected;
- the result can be published as a fast-forward update or a newly created task branch;
- no protected path requires an approval that has not been supplied.

A `ChangeBundle` is the canonical transport. Full-repository artifacts are optional compatibility adapters, not the standard protocol. Arbitrary shell commands from issue text, model output, or bundle content are prohibited. Repositories expose named, maintained commands that executors and validators may invoke.

The initial deployment may use GitHub-hosted Actions for public repositories and the current ChatGPT or connector capabilities as adapters. These are replaceable deployment choices rather than authorities.

## Alternatives considered

### ChatGPT and connector as the permanent orchestrator

Rejected. It solves the immediate workflow but makes one product interface and connector capability set part of the architecture.

### GitHub Actions as both executor and source author

Rejected. It combines proposed-code execution, repository credentials, and publication authority, weakens independent validation, and increases workflow-specific lock-in.

### Require a local developer agent

Rejected as the mandatory operating model. Local executors may be supported, but the maintainer must be able to operate the system through a web interface without maintaining a local checkout or runner.

### Build a self-hosted autonomous service first

Deferred. It maximizes control but adds hosting, patching, backup, credential, and availability obligations before the portable protocol is proven.

### Continue ad hoc whole-file connector replacement

Rejected. It is not atomic across paths, does not scale to generated or binary content, and encourages tool limitations to shape repository structure.

## Consequences

- Dornglut gains replaceable model, forge, workspace, and publication adapters.
- GitHub and ChatGPT can remain the first implementation without becoming permanent dependencies.
- Initial implementation is larger than another temporary workflow, but it removes repeated integration work from every product repository.
- Product CI stays small and independently read-only.
- A separate publisher identity and least-privilege credential strategy will eventually be required for fully unattended publication.
- Zero mandatory infrastructure subscription is achievable while public repositories use included hosted automation, but model inference and future private workloads may incur cost.
- Forge migration becomes an adapter change rather than a rewrite of the automation domain.

## Affected repositories

- `dornglut/engineering`
- `dornglut/forgeops`
- `dornglut/github-workflows`
- all maintained Dornglut product repositories adopting automated delivery

## Adoption or migration

1. Publish this ADR, the repository-automation architecture, and the owning initiative.
2. Remove the temporary source-export workflow from Runenwerk pull request #138 and complete that pull request under exact-head validation.
3. Create `dornglut/forgeops` with the provider-neutral protocol, filesystem workspace, plain-Git implementation, and conformance tests.
4. Add GitHub as the first forge and publication adapter.
5. Add thin GitHub workflow adapters only after the core contract exists.
6. Prove the system in a bounded canary repository before using it for the RunenSDF cutover.
7. Add optional hosted-model, open-model, ChatGPT-assisted, and human adapters without changing the protocol.

No new product pull request may introduce a temporary full-source export or self-authoring validation workflow as a substitute for this migration.

## Supersedes

None.

## Superseded by

[ADR 0003 — Retire provider-neutral repository automation](0003-retire-provider-neutral-repository-automation.md)
