# Repository automation architecture

## Purpose

This document defines the organization-wide architecture for hands-off repository work. It allows Dornglut to use ChatGPT web and GitHub today while keeping the execution, publication, model, and forge layers replaceable.

The architecture applies to source changes, documentation changes, generated outputs, dependency updates, cross-repository cutovers, and repository maintenance. Product repositories remain authoritative for their own behavior and validation semantics.

## Goals

- operate without requiring a maintainer-managed local agent or checkout;
- preserve exact-base, exact-content, and exact-head safety;
- keep validation independently read-only;
- support deterministic and AI-assisted changes through one protocol;
- avoid coupling the core domain to ChatGPT, a model provider, GitHub, or a connector;
- support public GitHub repositories with no mandatory infrastructure subscription;
- permit later migration to another forge or self-hosted execution environment;
- produce auditable evidence for every proposed and published change.

## Non-goals

- replacing product-repository validation commands;
- allowing model output or issue text to execute arbitrary commands;
- pushing directly to a protected default branch;
- granting an executor repository write credentials;
- making workflow YAML the location of substantive automation logic;
- guaranteeing permanently free hosted model inference;
- providing an unreviewed autonomous merge path.

## System context

```text
work source
    |
    v
WorkOrder
    |
    v
reasoner adapter -------- optional
    |
    v
isolated executor
    |
    +----> ExecutionEvidence
    |
    +----> ChangeBundle
              |
              v
        policy verifier
              |
              v
          publisher
              |
              v
        task branch + PR
              |
              v
     independent validator
              |
              v
        reviewer / merger
```

A deployment may combine some adapters in one process, but the permissions and domain boundaries remain distinct.

## Authority model

| Surface | Owns | Must not own |
|---|---|---|
| `engineering` | organization policy, architecture, protocol decisions | executable product automation or product behavior |
| `forgeops` | protocol schemas, core implementation, conformance, adapters | product validation semantics or live portfolio state |
| `github-workflows` | thin GitHub Actions callers and reusable orchestration | provider-neutral domain logic or source authorship policy |
| product repository | implementation, tests, validation command, local ADRs, releases | cross-organization automation authority |
| forge project or issue system | live work status and review state | durable architecture or source behavior |

## Core domain

### WorkOrder

A `WorkOrder` authorizes one bounded outcome.

Required information:

- stable work-order identifier;
- repository target or ordered repository targets;
- immutable base revision for every target;
- outcome and current evidence;
- allowed paths or areas;
- explicitly forbidden paths or areas;
- non-goals;
- acceptance criteria;
- named validation requirements;
- migration and deletion requirements;
- stop conditions;
- risk classification;
- authorization provenance.

A work order does not contain executable shell text. It may reference named repository capabilities from a checked-in repository automation contract.

### RepositoryRevision

A `RepositoryRevision` contains:

- forge-neutral repository identifier;
- immutable commit or revision identifier;
- optional branch reference used only for discovery or publication;
- content algorithm and object identity information required for verification.

Branch names are mutable navigation aids. They are never accepted as immutable inputs without first resolving and recording their exact revision.

### ChangeBundle

A `ChangeBundle` is a deterministic proposal against one exact repository revision.

Each operation is one of:

- create a path that is confirmed absent;
- replace a path whose previous content and mode match expected values;
- delete a path whose previous content and mode match expected values;
- rename a path represented as verified deletion plus verified creation with provenance.

Every operation records:

- normalized repository-relative path;
- expected prior state;
- resulting state;
- content object hash when content exists;
- file mode;
- text or binary classification;
- optional human-readable diff;
- generator or transformation provenance.

Bundle-wide metadata records:

- protocol version;
- work-order identifier;
- repository revision;
- creation time;
- producing adapter identity;
- operation count and payload sizes;
- deterministic bundle digest;
- required policy profile.

A bundle never contains repository credentials, model credentials, arbitrary command strings, or a request to merge.

### ExecutionEvidence

`ExecutionEvidence` records what occurred in an isolated workspace:

- exact source revision;
- workspace implementation and version;
- operating system and architecture;
- toolchain identities;
- named repository capabilities invoked;
- command exit status and bounded logs;
- generated or modified path inventory;
- input and output hashes;
- test, formatter, linter, and generator results;
- reasoner identity when a reasoner was used;
- timestamps and duration;
- evidence digest.

Evidence is descriptive. It does not override the independent validator.

### PublicationReceipt

A `PublicationReceipt` records:

- verified input bundle digest;
- publisher implementation and identity;
- repository and prior revision;
- created or updated task branch;
- resulting revision;
- forge pull-request or change-request reference;
- verification decisions;
- rejected operations, when publication fails;
- publication timestamp.

## Ports and adapters

### Work-source port

Supplies authorized work orders from:

- GitHub issues;
- Forgejo or GitLab issues;
- checked-in work-order files;
- a project-management system;
- a human or chat interface.

The adapter maps source-specific fields into the canonical work order. Source-specific labels and issue types do not enter the core model.

### Reasoner port

May be implemented by:

- OpenAI-hosted models;
- another hosted provider;
- an OpenAI-compatible endpoint;
- an Ollama-compatible endpoint;
- a deterministic program;
- a human-authored transformation.

The reasoner has no publication credential. Model-specific prompts, tool calls, and response formats remain inside the adapter.

### Workspace port

Provides an isolated exact checkout or equivalent content view.

Possible adapters:

- ephemeral container;
- GitHub-hosted runner;
- Forgejo runner;
- remote development sandbox;
- ChatGPT-managed sandbox;
- local checkout.

The workspace receives read-only source access and the named repository capabilities permitted by the work order. It emits evidence and a bundle, not a push.

### Forge port

Provides repository discovery and immutable object access for:

- GitHub;
- Forgejo;
- GitLab;
- plain Git over supported transports.

Forge API object types are converted at the adapter boundary.

### Publisher port

Verifies and applies a bundle to a task branch. Implementations may use:

- normal Git object creation and push;
- GitHub Git database APIs;
- Forgejo or GitLab APIs;
- a connector capable of equivalent atomic operations.

The publisher does not execute source from the bundle.

### Validator port

Invokes the repository-owned validation contract against the resulting exact head. The initial GitHub deployment uses the reusable workflows in `github-workflows`; another forge may use a different runner while invoking the same repository command.

## Repository automation contract

Every adopting repository exposes a small checked-in contract, provisionally `automation.toml`.

It declares named capabilities rather than accepting arbitrary commands from external work orders.

Example shape:

```toml
version = 1

[repository]
validation = "validate"

[capabilities.validate]
command = ["cargo", "validate"]
read_only = true

[capabilities.format]
command = ["cargo", "fmt", "--all"]
read_only = false
allowed_outputs = ["**/*.rs"]

[policy]
protected_paths = [
  ".github/workflows/**",
  ".github/dependabot.yml",
  "CODEOWNERS",
]
max_changed_files = 200
max_payload_bytes = 10485760
```

The executable command array is repository-owned and reviewed. A work order refers to `validate` or `format`; it cannot replace the command.

The final file name and schema are owned by `forgeops` and may change before the first stable protocol release.

## Trust boundaries

### Executor

The executor may:

- read the authorized repository revision;
- run allowed repository capabilities in isolation;
- transform workspace content;
- emit a bundle and evidence.

It must not:

- possess the publisher credential;
- mutate forge branches or pull requests;
- access unrelated repositories;
- merge changes;
- alter its work order.

### Publisher

The publisher may:

- read immutable repository objects and current branch state;
- verify bundles and policy;
- create or fast-forward authorized task branches;
- create or update change requests;
- emit a publication receipt.

It must not:

- execute proposed source;
- accept arbitrary shell commands;
- force-push unless a separately accepted recovery policy permits it;
- write protected default branches;
- approve or merge its own output.

A GitHub deployment should ultimately use a narrowly scoped GitHub App installation identity rather than a personal access token.

### Validator

The validator may:

- check out the published exact head;
- run repository-owned read-only validation;
- publish bounded diagnostics and status.

It must not:

- author source;
- commit fixes;
- alter the task branch;
- use model output as proof of correctness.

### Reviewer and merger

The reviewer evaluates scope, architecture, evidence, and exact-head validation. Merge is a separate authorized action protected by expected-head matching.

## Lifecycle

### 1. Intake

The work-source adapter resolves an authorized work item into a versioned work order. The system records exact repository revisions before any reasoning or execution.

### 2. Planning

A reasoner or human may inspect source and produce a plan. Planning does not mutate the repository. Stop conditions are evaluated before execution.

### 3. Execution

An isolated workspace is prepared at the exact recorded revision. Only named repository capabilities and explicitly permitted tooling are available. The executor emits evidence and a content-addressed change bundle.

### 4. Verification before publication

The publisher verifies:

1. schema and protocol compatibility;
2. bundle digest;
3. work-order authorization;
4. repository identity;
5. exact base revision;
6. path normalization and traversal safety;
7. allowed and protected path policy;
8. expected prior content and modes;
9. payload and operation limits;
10. branch namespace and update mode.

Any mismatch rejects the complete bundle. Partial publication is prohibited.

### 5. Atomic publication

The publisher creates one repository tree and one commit for the coherent bundle, then creates or fast-forwards the authorized task branch. If the branch moved after verification, publication fails and the bundle must be regenerated or explicitly rebased through a new work order revision.

### 6. Independent validation

The forge triggers validation for the resulting exact head. Validation invokes the repository-owned command and records status against that revision.

### 7. Review and merge

Review confirms that:

- the diff matches the work order;
- durable decisions are followed;
- evidence is complete but not substituted for CI;
- required checks passed at the current head;
- obsolete paths are deleted or have an accepted removal condition.

Merge uses expected-head protection. The task branch is deleted after merge when the forge supports it.

## Multi-repository work

A cross-repository initiative produces one ordered work order per owning repository. Bundles and commits remain repository-local.

Dependencies are explicit:

```text
repository A publication and release
    -> repository B dependency adoption
    -> repository B source deletion
```

The system must not simulate a distributed transaction across forges. Instead it records sequencing, compatibility windows, and rollback points. Clean cutovers remain preferred where compatibility permits them.

## Generated outputs and formatting

Generated files and formatter output are produced inside an executor through named repository capabilities. The resulting paths are captured in the bundle with evidence identifying the generating capability and toolchain.

The publisher treats generated output exactly like other content and never regenerates it. Independent validation confirms that the committed generated state is current.

## Protected changes

Changes to workflow files, publisher policy, credentials, CODEOWNERS, repository rules, and organization governance require a higher policy profile.

The initial implementation must support at least:

- normal source and documentation profile;
- automation and workflow profile;
- organization-governance profile.

Policy profiles may require different reviewers or may prohibit autonomous publication entirely.

## Failure behavior

The system fails closed for:

- stale revisions;
- missing expected paths;
- hash mismatches;
- unsupported protocol versions;
- policy violations;
- excessive payloads;
- malformed paths;
- publisher identity or permission failures;
- validation failures.

A failed publication leaves no partial commit or branch update. A failed validation leaves the published task branch intact for correction and records exact-head diagnostics.

Retries must be idempotent by bundle digest and target revision. The publisher must detect an already published identical bundle and return the existing receipt rather than creating duplicate commits.

## Observability and audit

Every run records stable identifiers linking:

```text
work order
    -> execution evidence
    -> change bundle
    -> publication receipt
    -> repository commit
    -> pull request
    -> validation run
    -> merge commit
```

Logs exclude credentials and are bounded by retention and size policy. Durable decisions stay in repository documents; live execution status stays in the forge or project system.

## Portability

Provider-neutral logic lives in `forgeops`, not workflow YAML.

GitHub Actions callers should:

- check out the exact requested revision;
- invoke a versioned `forgeops` command or repository capability;
- pass structured inputs;
- upload structured outputs or diagnostics;
- declare least-privilege permissions.

Forgejo, GitLab, or another runner can replace those callers without changing the domain protocol.

## Cost model

The architecture distinguishes monetary cost from operational cost.

Possible zero-marginal-cost deployment:

- public GitHub repositories;
- included standard hosted Actions execution;
- open-source `forgeops` implementation;
- current ChatGPT subscription or a human reasoner;
- no separate always-on service.

This does not guarantee free model inference. Model adapters are optional and replaceable. A future open-model deployment trades provider fees for hardware, electricity, maintenance, and availability responsibility.

Self-hosting a forge or runner increases sovereignty but also introduces patching, isolation, backups, monitoring, and credential-management obligations. It is not required for the initial design.

## Initial implementation shape

The dedicated `forgeops` repository should begin as a Rust workspace:

```text
forgeops/
├── Cargo.toml
├── rust-toolchain.toml
├── crates/
│   ├── forgeops-core/
│   ├── forgeops-protocol/
│   ├── forgeops-policy/
│   ├── forgeops-workspace/
│   ├── forgeops-git/
│   ├── forgeops-github/
│   └── forgeops-cli/
├── schemas/
├── conformance/
├── docs/
├── examples/
├── xtask/
└── .github/workflows/ci.yml
```

Initial dependency direction:

```text
forgeops-core
    <- forgeops-protocol
    <- forgeops-policy
    <- forgeops-workspace
    <- forgeops-git
    <- forgeops-github
    <- forgeops-cli
```

`forgeops-core` must not depend on GitHub, a model SDK, an async HTTP client, a workflow runtime, or a concrete workspace implementation.

The first vertical proof is deterministic rather than AI-driven:

1. read a work order and exact local Git revision;
2. create a verified text-file change bundle;
3. reject stale or mismatched prior content;
4. publish atomically to a task branch through a GitHub adapter;
5. emit a publication receipt;
6. validate the resulting branch through existing read-only CI.

Model-assisted execution is added only after that protocol is conformance-tested.

## Adoption sequence

1. Accept ADR 0002 and this architecture.
2. Complete Runenwerk pull request #138 and remove its temporary export workflow.
3. Create and bootstrap `dornglut/forgeops`.
4. Implement protocol schemas, hashes, path safety, policy, and conformance fixtures.
5. Implement filesystem workspace and plain-Git adapters.
6. Implement GitHub read and publication adapters.
7. Prove a bounded public-repository canary.
8. Add thin GitHub workflow integration.
9. Add optional reasoner adapters.
10. Use the proven path for RunenSDF and later cross-repository cutovers.

## Acceptance criteria

The architecture is operational when:

- a non-model deterministic executor can produce a valid bundle;
- two independent implementations can consume the protocol conformance fixtures;
- stale content and stale branch heads are rejected;
- a publisher can atomically apply creation, replacement, and deletion operations;
- the publisher cannot write the default branch under its normal policy;
- validation remains read-only and exact-head scoped;
- ChatGPT can be removed without changing the protocol;
- GitHub can be replaced by another forge adapter without changing the protocol;
- product repositories retain one canonical validation command and do not contain transport-specific source-export workflows.
