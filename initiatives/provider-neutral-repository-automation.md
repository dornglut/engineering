# Provider-neutral repository automation

- Status: active
- Owner: Dornglut organization
- Owning issue: [engineering#2](https://github.com/dornglut/engineering/issues/2)
- Decision authority: [ADR 0002](../adrs/0002-provider-neutral-repository-automation.md)
- Architecture authority: [repository automation architecture](../architecture/repository-automation.md)

## Outcome

Dornglut can perform hands-off repository work through a web interface without requiring a maintainer-managed local agent, while ChatGPT, the current connector, GitHub, and any model provider remain replaceable adapters rather than architectural dependencies.

## Rationale

The organization bootstrap and shared-CI adoption established sound governance and validation boundaries, but Runenwerk pull request #138 exposed a missing execution and publication layer. A temporary source-export workflow bridged one connector limitation but added tool-specific transport to a product pull request and could not serve as a durable pattern.

The organization needs one provider-neutral implementation that can safely prepare deterministic changes, publish them atomically to task branches, and preserve independent exact-head validation across all product repositories.

## Affected repositories

| Repository | Responsibility |
|---|---|
| `dornglut/engineering` | decision, architecture, initiative, and operating policy |
| `dornglut/forgeops` | protocol, core implementation, conformance, workspaces, forge adapters, and CLI |
| `dornglut/github-workflows` | thin GitHub-specific orchestration and reusable validation integration |
| `dornglut/runenwerk` | first active defect motivating the boundary; later adoption consumer |
| `dornglut/runen-sdf` | intended bounded canary and later cutover consumer |
| `dornglut/runen-ui` | later consumer after protocol and canary proof |

## Dependency graph

```text
ADR and architecture acceptance
    -> Runenwerk PR #138 correction and temporary workflow deletion
    -> forgeops repository creation
    -> protocol and conformance foundation
    -> deterministic workspace and plain-Git proof
    -> GitHub publication adapter
    -> bounded canary adoption
    -> shared workflow integration
    -> optional model adapters
    -> RunenSDF clean cutover
```

Product adoption must not begin before the protocol, policy verification, and atomic publication proof are green in `forgeops`.

## Delivery sequence

### Phase A — Authority and immediate cleanup

Deliverables:

- accepted ADR 0002;
- repository automation architecture;
- this initiative;
- corrected Runenwerk pull request #138;
- deletion of `.github/workflows/temporary-source-export.yml`;
- exact-head Runenwerk validation success.

Completion evidence:

- merged `engineering` authority pull request;
- merged Runenwerk pull request #138 with no temporary transport workflow or retired roadmap authority.

### Phase B — ForgeOps repository foundation

Deliverables:

- public `dornglut/forgeops` repository;
- license, README, AGENTS, contribution and security pointers;
- Rust workspace and pinned toolchain;
- one canonical validation command;
- immutable shared Rust workflow caller;
- protocol versioning and compatibility policy;
- no model SDK or forge SDK in the core crate.

Completion evidence:

- repository bootstrap pull request merged;
- full validation green at exact head;
- dependency audit proving core independence.

### Phase C — Protocol and conformance

Deliverables:

- versioned `WorkOrder`, `RepositoryRevision`, `ChangeBundle`, `ExecutionEvidence`, and `PublicationReceipt` schemas;
- canonical serialization rules;
- content hashing and bundle digest rules;
- path normalization and traversal rejection;
- create, replace, delete, and rename semantics;
- text and binary payload support;
- policy profiles and protected-path handling;
- idempotency and stale-revision behavior;
- positive and negative conformance fixtures.

Completion evidence:

- schema tests;
- deterministic round-trip tests;
- malformed, stale, oversized, duplicate, and traversal bundles rejected;
- conformance package consumable without GitHub or a model provider.

### Phase D — Workspace and Git implementation

Deliverables:

- isolated filesystem workspace;
- exact-revision checkout contract;
- repository-owned named capability execution;
- bounded logs and evidence generation;
- plain-Git object and branch implementation;
- atomic bundle application;
- fast-forward-only publication;
- rollback and retry behavior.

Completion evidence:

- deterministic local test repositories prove all path operations;
- no partial publication under injected failures;
- stale branch movement rejects publication;
- identical bundle retries return the existing publication receipt.

### Phase E — GitHub adapter and canary

Deliverables:

- GitHub repository and immutable-object adapter;
- GitHub task-branch publication adapter;
- pull-request creation or update;
- least-privilege publisher identity design;
- exact-head status discovery;
- bounded public canary issue and change.

The canary must not be a workflow or governance-file change. It should be a deterministic documentation or fixture update with explicit prior hashes and a reversible outcome.

Completion evidence:

- one bundle published without connector-specific whole-file mutation;
- one task branch and pull request created;
- independent read-only CI passes;
- expected-head merge succeeds;
- branch cleanup is recorded.

### Phase F — GitHub workflow integration

Deliverables:

- thin reusable orchestration in `github-workflows`;
- structured work-order input and artifact output where required;
- no substantive protocol logic in YAML;
- no source-writing permission in validation workflows;
- separate publication authorization where unattended operation is enabled;
- consumer adoption documentation.

Completion evidence:

- workflow self-tests and canary consumer pass;
- consumers pin immutable workflow revisions;
- validation and publication identities are distinct.

### Phase G — Reasoner adapters

Deliverables:

- generic reasoner port;
- deterministic and human adapters as the baseline;
- one hosted-model adapter;
- one generic compatible-endpoint adapter;
- prompt and response handling isolated from the core;
- model output constrained by work-order and bundle policy.

Completion evidence:

- the same work order can be executed through deterministic, human, and model-assisted paths;
- removing the model adapter does not change protocol or publication tests;
- model failure cannot produce a partially published change.

### Phase H — Product adoption and cutover

Deliverables:

- RunenSDF adoption canary;
- Runenwerk adoption after the canary;
- RunenUI adoption after repository-specific review;
- removal of obsolete transport-specific automation;
- RunenSDF clean cutover resumed through the accepted path.

Completion evidence:

- each repository exposes a reviewed automation contract and one validation command;
- no product repository depends on ChatGPT-specific or connector-specific transport;
- cross-repository sequencing and releases remain explicit.

## Acceptance evidence

The initiative closes only when:

- ADR 0002 and the architecture are merged;
- `dornglut/forgeops` exists and owns the executable implementation;
- protocol conformance tests cover successful and rejected bundles;
- a publisher atomically creates, replaces, and deletes paths against exact prior hashes;
- stale revisions and unauthorized paths fail closed;
- the publisher cannot write the default branch under normal policy;
- independent validation passes at the exact published head;
- a non-GPT path completes the canary;
- a non-connector publication adapter completes the canary or equivalent conformance proof;
- GitHub-specific logic remains outside the core;
- no temporary source-export workflow remains in Runenwerk;
- the RunenSDF cutover resumes through the proven operating model.

## Sequencing constraints

- Runenwerk PR #138 cleanup precedes new product adoption work.
- `forgeops` protocol and conformance precede hosted-model integration.
- plain-Git behavior precedes GitHub publication behavior.
- GitHub canary success precedes RunenSDF cutover use.
- validation and publisher credentials remain separated throughout.
- workflow and governance changes use dedicated review scope.

## Risks and mitigations

### Scope expansion into a general autonomous platform

Mitigation: begin with deterministic bundles, exact Git publication, and conformance. Defer model orchestration, scheduling, portfolio automation, and multi-forge deployment until the core proof is complete.

### Recreating GitHub Actions semantics in the core

Mitigation: require plain-Git and filesystem conformance before GitHub adapters; keep YAML thin.

### Credential concentration

Mitigation: executor has no write credential, publisher does not execute proposed source, validator remains read-only, and merge remains separately authorized.

### Protocol overdesign

Mitigation: version only fields required for the first deterministic vertical proof; add capabilities through explicit compatible versions and conformance fixtures.

### Free-tier dependency

Mitigation: treat included GitHub-hosted execution as an initial deployment choice. Preserve portable executables and runner-independent commands so self-hosting or another forge remains possible.

### Model-quality dependence

Mitigation: deterministic and human adapters remain first-class; validation and publication safety never depend on model confidence.

### Product delivery delay

Mitigation: Phase A completes the current CI migration first. Later phases use a bounded canary and do not require all future adapters before RunenSDF work resumes.

## Rollback

Before product adoption, rollback consists of closing the initiative and archiving an unconsumed `forgeops` repository; product behavior is unaffected.

After adoption, each product repository can return to human-authored branches and existing read-only validation because the automation protocol does not replace Git or repository validation. Publisher credentials can be revoked independently. No product repository may require the reasoner service to build, test, release, or consume the product.

## Linked local work

- [engineering#2](https://github.com/dornglut/engineering/issues/2) — organization authority and initiative
- [runenwerk#137](https://github.com/dornglut/runenwerk/issues/137) — shared Rust validation adoption
- [runenwerk#138](https://github.com/dornglut/runenwerk/pull/138) — active CI adoption pull request
- [runenwerk#133](https://github.com/dornglut/runenwerk/issues/133) — RunenSDF clean cutover

Additional implementation issues will be created in their owning repositories after the relevant repository exists and the preceding phase is accepted.

## Closure record

Open. Record final merged revisions, canary evidence, adopted repositories, residual risks, and any superseding decisions here when all acceptance evidence is satisfied.
