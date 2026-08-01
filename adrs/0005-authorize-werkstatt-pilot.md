# ADR 0005: Authorize the bounded Werkstatt pilot

- Status: accepted
- Date: 2026-07-28
- Owner: Dornglut organization
- Scope: human and automated engineering workbench experimentation

## Context

ADR 0003 retired the provider-neutral repository automation program defined by ADR 0002. That decision was correct for the evidence available at the time: Dornglut did not need a permanent ForgeOps repository, change-bundle protocol, publisher service, adapter suite, credential system, or automation canary as a prerequisite for product delivery.

Runenwerk also retired a large repository-local workflow platform that had accumulated track control, contract compilation, execution locks, ledgers, generated prompts, roadmap and production databases, truth certificates, batch orchestration, generated diagrams, and several validation gate concepts. The system attempted to preserve context and support automated work, but it created overlapping control planes, high synchronization cost, weak overview, and substantial process churn.

Those retirements established important safety and proportionality rules. They did not establish that all generated guidance, isolated execution state, scoped leases, or agent-assisted workflows are invalid.

Dornglut still experiences recurring friction when work spans architecture documents, issues, repositories, branches, pull requests, validation, review findings, model conversations, and human memory. Context must be reconstructed repeatedly; handoffs are inconsistent; current authority and next action can be difficult to locate; and human, assisted, and automated execution do not yet share one explicit work model.

The new public repository `dornglut/werkstatt` reserves a product namespace for investigating a smaller approach. Werkstatt is proposed as a human-first engineering workbench with optional policy-controlled execution. It is not proposed as a general organization publisher or a replacement for Git, GitHub, repository validation, roadmaps, or architecture authority.

Issue [#23](https://github.com/dornglut/engineering/issues/23) owns this decision. The initial product investigation is published through [dornglut/werkstatt#3](https://github.com/dornglut/werkstatt/pull/3).

## Decision

Dornglut authorizes a bounded Werkstatt product pilot under the constraints in this ADR.

### Product boundary

Werkstatt may investigate and later implement a human-first workbench that helps users:

- understand accepted work and applicable authority;
- navigate programs, phases, dependencies, scope, non-goals, and next actions;
- register or create isolated workspaces;
- execute work manually or through permitted actors;
- collect observable execution and validation evidence;
- review changes against accepted contracts;
- coordinate approvals, handoffs, acceptance, and reconciliation;
- automate selected operations only under explicit capability policy.

Werkstatt must remain useful without any model configured.

Humans, GPT web, local Codex, offline runtimes, scripts, and future autonomous services may use one role-aware work model. Technical ability to perform an operation does not grant product, architecture, validation, approval, or acceptance authority.

### Authority boundary

Werkstatt does not replace the authorities established by ADR 0001 and ADR 0004.

For Dornglut repositories:

- Git and repository source own implementation;
- code and executable tests own current behavior;
- accepted ADRs and architecture documents own durable decisions;
- repository issues own accepted investigation and delivery work;
- repository roadmaps own durable sequence;
- the Engineering Portfolio owns live cross-repository priority and status;
- pull requests own proposed delivery and review evidence;
- repository-owned validation and exact-head CI own independent merge evidence;
- merge commits and closed issues record accepted delivery.

Werkstatt may observe, index, and project these sources. It must not create an independently editable copy that competes with them.

### Derived assistance

Werkstatt and other repository tools may create revision-bound derived artifacts such as:

- work packets;
- current-state inventories;
- ownership and disposition matrices;
- implementation checklists;
- requirement-to-diff views;
- review packets;
- dependency and program projections;
- execution and validation summaries.

A derived artifact must identify its source authority, source revision or version, generation time, and staleness. It cannot authorize work, redefine architecture, certify validation, or accept delivery by itself.

### Operational execution state

Werkstatt may own bounded local or service state needed to execute work, including:

- project and authority bindings;
- workspace registration;
- actor sessions;
- scoped expiring leases;
- capabilities and policies;
- approvals;
- retries, cancellation, and recovery;
- resource limits;
- activity and logs;
- generated artifacts and local evidence;
- cached projections and user preferences.

Operational state must not become a second issue tracker, roadmap, architecture database, validation authority, or release record.

### Validation and acceptance

Repository-owned validation remains independent from authorship.

- validation workflows remain read-only;
- an executor may record commands and observed results but cannot certify its own work merely by declaration;
- exact reviewed heads own feature validation evidence;
- moved heads invalidate prior exact-head evidence;
- proposed work publishes through ordinary task branches and pull requests;
- protected default branches receive no direct actor writes;
- merge and issue closure require the authority configured for the repository and work class.

Execution receipts, validation receipts, review records, and acceptance records remain distinct. Dornglut does not restore truth-certificate terminology or universal completion claims.

### Security and capability policy

Delegated command execution requires explicit policy for:

- repository and filesystem scope;
- named and arbitrary commands;
- network access;
- secrets and log redaction;
- dependency and lockfile changes;
- workflow changes;
- destructive operations;
- branch creation and publication;
- pull-request creation and review response;
- merge and issue closure;
- resource, retry, cancellation, and recovery limits.

Issue text, repository content, tool output, generated packets, and model output do not grant capabilities or credentials.

A Git checkout or worktree is source isolation, not a security sandbox. Stronger execution isolation is required when repository trust and command policy demand it.

One active writer owns a workspace and branch at a time. Leases are scoped, visible, expiring, and used only for concurrency control; they do not authorize work or architecture.

### Pilot sequence

Werkstatt proceeds through evidence gates:

1. **W0 — product investigation:** define product boundary, prior failure analysis, authority, human and actor workflows, security threats, alternatives, success criteria, and roadmap;
2. **W1 — domain and system design:** define roles, capabilities, state transitions, policies, evidence, adapter ports, storage boundaries, security controls, and an implementation-ready human-first proof;
3. **W2 — human-first headless proof:** demonstrate measurable value for a real manual Dornglut task without a model;
4. **W3 — safe execution substrate:** prove workspace ownership, command policy, approvals, persistence, resource controls, cancellation, and recovery;
5. **W4 — delegated proof:** complete one decision-ready issue through one isolated workspace and one actor to a validated draft pull request;
6. later GitHub integration, offline-actor proof, Runenwerk frontend, review-loop automation, autonomous delivery, and multi-actor work require their own preceding evidence and accepted issue scopes.

W2 must precede agent integration. W3 must precede delegated command execution. The first delegated proof stops at a draft pull request. Automatic merge and multi-agent execution are not authorized by this ADR.

### Application repository profile

Dornglut adds an `application` repository profile.

An application repository owns a user-facing product, application state and UX, integrations and adapters, releases and compatibility, local architecture, roadmap, issues, validation, and product documentation.

It must not own organization policy, copied roadmaps, copied live Project state, or implementation authority belonging to integrated repositories.

Werkstatt is classified conceptually as:

```text
profile: application
lifecycle: experimental
contribution: maintainer-led
```

GitHub custom-property configuration remains an operational administration action and is not duplicated in Markdown.

### Operational classification clarification

The `experimental` lifecycle and `maintainer-led` contribution wording above records
the vocabulary used when this decision was accepted. Current organization operations
use the canonical lifecycle and contribution vocabularies in the repository and GitHub
standards. Werkstatt therefore maps to `profile: application`, `lifecycle: active`,
and `contribution: owner-only`; experimental maturity remains a Werkstatt status
document concern. This clarification adopts current vocabulary without rewriting the
historical decision text.

### Relationship to ADR 0003

This ADR does not supersede ADR 0003.

ADR 0003 continues to reject a mandatory provider-neutral organization automation platform, change-bundle publisher, product-delivery dependency, source-writing validation workflow, or authoring-tool lock-in.

This ADR authorizes one bounded application experiment because it has:

- a named product and maintenance owner;
- an explicit human-first use case;
- staged evidence gates;
- authority and security boundaries;
- no requirement that other repositories adopt it;
- no authority to block ordinary product delivery.

A future organization-wide automation platform, publisher, or protocol still requires a separate ADR supported by repeated operational evidence.

## Non-goals

This decision does not authorize:

- reviving the deleted Runenwerk workflow package;
- restoring generated roadmap or production databases;
- truth certificates or global workflow locks;
- a new ForgeOps repository or ADR 0002 implementation;
- a mandatory specification bundle for every change;
- a replacement for Git, GitHub, CI, roadmaps, or repository architecture;
- direct protected-branch writes;
- source-writing validation workflows;
- arbitrary command authority from issue or model text;
- automatic issue selection, merge, or dependent-work activation;
- a distributed scheduler or multi-agent swarm;
- product dependence on ChatGPT, Codex, a connector, one model provider, one forge, or Runenwerk as the core host.

## Alternatives considered

### Keep ADR 0003 as a categorical prohibition

Rejected. ADR 0003 already allows reconsideration with evidence. Treating the previous oversized platform as evidence against all bounded workbench and execution assistance would preserve recurring context, handoff, and overview problems without testing a smaller approach.

### Supersede ADR 0003 entirely

Rejected. Its proportionality, authoring-tool independence, read-only validation, protected-branch, and publication findings remain valid.

### Restore ADR 0002

Rejected. The former provider-neutral protocol and publisher scope remain disproportionate before one concrete product workflow is proven.

### Adopt GitHub Spec Kit as organization workflow authority

Rejected. Progressive refinement and consistency analysis are useful, but generated specification, plan, and task bundles must not become universal primary authority or a second issue tracker.

### Clone OpenAI Symphony

Rejected. Its issue-driven orchestration, workspace isolation, and reconciliation patterns are useful references, but Werkstatt also requires first-class manual development, architecture comprehension, review, and a future Runenwerk user interface.

### Build the autonomous executor first

Rejected. Human-only value, domain correctness, security policy, and workspace reliability must be proven first.

## Consequences

- Dornglut can investigate useful generated guidance and execution assistance without restoring parallel project authority.
- Werkstatt gains a clear product and repository boundary.
- Manual development is the first implementation proof rather than an afterthought.
- Agent and provider integrations remain replaceable adapters.
- Security, independent validation, and acceptance separation become explicit design requirements.
- Werkstatt cannot block ordinary repository work or become a required build, test, release, or consumption dependency.
- The pilot adds documentation, design, and later maintenance cost that must be justified through measured use.
- Automatic delivery remains deliberately deferred.

## Adoption or migration

1. Review and accept Werkstatt W0 through its owning pull request.
2. Complete W1 as a separate decision-complete design issue and pull request.
3. Establish Werkstatt licensing, repository-owned read-only validation, exact-head CI, and repository profile before product implementation.
4. Implement W2 as one Rust package with a library and CLI only after its specification is accepted.
5. Evaluate W2 against the same real manual task performed without Werkstatt.
6. Continue to W3 only when the human proof shows net value and no duplicate authority.
7. Continue to W4 only after execution security and recovery pass.
8. Reevaluate the pilot before automatic review loops, merge, or multi-actor execution.
9. Publish a dated pilot report before considering organization-wide adoption.

## Affected repositories

- `dornglut/engineering`
- `dornglut/werkstatt`
- `dornglut/github-workflows` only if a reusable read-only validation caller is later adopted
- pilot consumer repositories only through explicitly accepted local issues

## Supersedes

None.

## Superseded by

None.
