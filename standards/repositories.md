# Repository standard

This standard defines the minimum common shape of Dornglut repositories without forcing unrelated products into one physical layout.

## Operating rule

> Centralize organization policy, shared architecture, defaults, and CI orchestration. Localize implementation, validation semantics, public contracts, releases, local architecture, roadmaps, and issues.

Consistency applies to the meaning of entrypoints and ownership boundaries. It does not require identical internal trees.

## Repository profiles

The canonical profile vocabulary is `organization-defaults`, `engineering`,
`workflow-library`, `rust-framework`, `integration-product`, `application`, and
`template`. Lifecycle values are `planned`, `active`, `maintenance`, and `archived`;
contribution values are `owner-only`, `discussion`, and `open`.

### Organization defaults

Used by `dornglut/.github`.

Owns:

- the public organization profile;
- inherited community-health files;
- generic issue forms;
- pull-request guidance;
- workflow templates.

Must not own product roadmaps, implementation architecture, release state, or product validation semantics.

### Engineering

Used by `dornglut/engineering`.

Owns:

- organization governance and standards;
- cross-repository architecture;
- organization ADRs;
- qualifying initiatives;
- dated cross-repository audits.

Must not own product implementation, copied repository roadmaps, or live Project state.

### Workflow library

Used by `dornglut/github-workflows`.

Owns reusable read-only CI orchestration and its compatibility contract.

Must not recreate product validation logic, author source, or own product releases.

### Rust framework

Used by standalone framework repositories such as RunenUI, RunenSDF, and future RunenGPU, RunenRender, and RunenECS repositories.

Expected root entrypoints:

- `README.md`;
- `AGENTS.md`;
- `ARCHITECTURE.md`;
- `TESTING.md`;
- Cargo workspace or package metadata;
- toolchain declaration;
- license files;
- one thin CI caller.

A repository may omit an entrypoint only when the same information has one obvious canonical location and the omission is explicit.

### Integration product

Used by Runenwerk.

It follows the same entrypoint semantics as a Rust framework but may contain applications, adapters, multiple domains, and a documentation site as the canonical long-form authority.

### Application

Used by repositories that own a user-facing product such as Werkstatt.

Owns:

- application behavior, state, and user experience;
- product-specific integrations and adapters;
- releases and compatibility;
- local architecture, roadmap, issues, and validation;
- product documentation and operational requirements.

Expected root entrypoints:

- `README.md`;
- `AGENTS.md`;
- `ARCHITECTURE.md`;
- `TESTING.md`;
- product build or package metadata when implementation exists;
- toolchain declarations required by the implementation;
- license files;
- one canonical read-only validation command;
- one thin CI caller when executable validation exists.

An application may provide headless libraries, command-line tools, graphical frontends, services, or adapters when they serve the product boundary. It must not own organization policy, copied repository roadmaps, copied live Project state, or implementation authority belonging to integrated repositories.

### Template

Used only for a repository that bootstraps new repositories.

A template is a one-time starting point. It must not become an ongoing synchronization authority for repositories created from it.

## Root documentation

### README

The public landing page states:

- purpose and boundary;
- maturity;
- major capabilities and decisive limitations;
- canonical validation;
- links to architecture, testing, contribution, security, and license information.

It must not contain current branch, PR, exact head, CI run, temporary blocker, or live priority state.

### AGENTS

`AGENTS.md` is an executor contract:

- where to start;
- ownership constraints;
- prohibited operations;
- canonical validation;
- required delivery evidence.

It must not duplicate the full architecture or roadmap.

### ARCHITECTURE

`ARCHITECTURE.md` is a concise root map of the system boundary, dependency direction, and canonical long-form architecture.

### TESTING

`TESTING.md` is a concise root map of focused checks, the canonical baseline, CI relationship, and evidence rules.

### docs

Use only directories that contain real material. Common semantic locations are:

- `architecture/` for durable system contracts;
- `adr/` for repository-local decisions;
- `roadmap.md` for durable outcome sequence;
- `status.md` for maturity;
- `tooling/` for maintained procedures;
- `reports/` for dated evidence;
- `history/` for retired systems;
- `provenance/` for extraction and origin evidence.

Do not add empty taxonomy directories merely for symmetry.

## Repository lifecycle

### Create

A new repository requires:

- a named purpose and owning domain;
- an explicit relationship to existing repositories;
- a visibility decision;
- default branch `main`;
- one canonical read-only validation command;
- a README and `AGENTS.md`;
- ownership of issues, decisions, releases, and compatibility;
- no duplicate source authority.

Skeleton repositories may reserve a namespace but must not imply a completed extraction or public contract.

### Develop

Nontrivial work is issue-owned, begins from the current accepted default branch, records the accepted base and reviewed feature head, validates the exact feature head, and records the accepted post-merge revision when closing delivery. Pull requests remain bounded and document scope, non-scope, migration, and next action. [Validation standard](validation.md) defines the evidence contract; repositories retain ownership of validation semantics.

When an executor must select follow-on work, selection follows the continuation and work-selection rules in [Authority and work](../governance/authority-and-work.md); a previously stated next action does not by itself authorize new work.

Shared defaults and workflows do not replace repository-local authority.

### Extract or transfer

Before moving a subsystem into a standalone repository:

1. correct the source boundary in the current owner;
2. transfer one accepted implementation authority;
3. prove standalone validation and downstream conformance;
4. migrate real consumers;
5. delete the old source and workspace authority;
6. prove no forwarding package, alias, include, branch dependency, submodule, or duplicate implementation remains;
7. close provenance and release policy.

A planned repository name does not authorize source movement.

### Archive

Archive only when active consumers, issues, releases, security obligations, and replacement authority are documented. Archived repositories are historical evidence, not active dependencies.

## Maintained-repository admission and reconciliation

When a maintained repository is created, transferred, or changes profile, reconcile
its purpose and ownership boundary; README and AGENTS; profile-required architecture
and testing entrypoints; canonical read-only validation and a thin immutable CI caller;
profile, lifecycle, and contribution classification; public organization profile where
relevant; repository-family architecture; Project area vocabulary only when genuinely
needed; initiative inclusion or explicit exclusion; security and contribution routing;
and source-transfer and duplicate-authority status.

This is a bounded reconciliation checklist, not a repository generator, bootstrap
platform, or second lifecycle database.

## Identity and history

Active repository metadata and links use the `dornglut/*` namespace.

Historical owners may remain only where they are necessary provenance or decision history. Validators should reject historical owner identities in active README, governance, standards, and architecture surfaces.
