# Software design standard

This standard is Dornglut's organization-wide default for project-neutral software design.
It applies when an owning repository has no more specific accepted authority for the
question. Repository code and tests still own current behavior, repository ADRs own
local durable architecture, and organization ADRs own accepted cross-repository
architecture. More specific accepted authority may specialize this standard.

This document is not a product architecture, roadmap, implementation plan, or catalog
of mandatory patterns. It defines the boundary and ownership questions that should be
answered before choosing a concrete implementation pattern.

## Core model

Design from boundary pressure rather than pattern preference:

```text
authority
+ invariants
+ contracts
+ flows
+ policy
+ time
+ consistency
+ storage
+ execution
+ failure
+ observation
+ evolution
+ cost
```

A useful short form is:

```text
Local code can be simple.
Boundary code must be explicit.
Authority code must protect invariants.
Persistent contracts must evolve deliberately.
Failure must be observable.
```

## 1. Authority and invariants

An authority is the owner that decides what is valid for one semantic invariant set.
Usage, storage, presentation, transport, or execution does not by itself create
authority.

Prefer:

```text
one semantic invariant set -> one authority
```

An invariant that matters must be enforced by its owning authority or an explicit
validation boundary, not only by UI, callers, documentation, or convention.

Different representations may coexist when they own different invariants. Their
correspondence must be explicit rather than inferred from one universal identity or
one global object model.

Avoid inventing an authority for helpers that own no semantic invariant. A formatter,
button renderer, serializer helper, or cache does not become an authority merely
because it is reusable.

## 2. Boundary contracts and flows

Boundaries speak contracts rather than foreign internals. Contracts may include:

- function or interface signatures;
- commands and queries;
- events;
- DTOs and immutable snapshots;
- schemas and persisted formats;
- protocol messages;
- products and projections;
- status and diagnostic records.

Use the flow vocabulary according to meaning:

```text
Command     request to change state
Query       request to read state
Event       accepted fact that happened
Product     owner-defined formed or derived output
Projection  derived read or view model
Status      observed current condition
Diagnostic  explanation of a failure, warning, or rejection
```

Important mutations cross a named change boundary and are validated near the
invariants they affect. Do not create one universal command model for unrelated
semantic owners.

Reads across an authority boundary use an owner-defined contract rather than private
mutable state. A query result, immutable snapshot, product, projection, prepared input,
or stream may all be valid depending on the owner contract.

## 3. Dependency direction and representation

Keep stable semantic rules independent from outer wiring where practical. A common
shape is:

```text
shared vocabulary -> domain/core semantics -> orchestration/runtime -> apps/adapters/tools
```

Concrete repository structure may differ. The invariant is that stable semantic
contracts should not depend on incidental UI, transport, persistence, vendor, or host
implementation details without an explicit reason.

Do not use dependency inversion as an excuse for universal registries, global service
locators, vague extension points, or a shared meta-model that erases distinct owners.

When an editable or persistent description and an optimized executable realization
have different responsibilities, keep them distinct. Examples include a document and
its loaded runtime form, a graph and its prepared plan, or a build description and its
job execution state.

## 4. Authoritative and derived state

Caches, projections, indexes, view models, render packets, diagnostics tables, preview
products, and similar read-oriented structures are derived unless an accepted design
explicitly promotes them to authority.

Derived state should be rebuildable from owned source contracts. Allowing a mutable
projection or cache to become source truth accidentally creates competing authorities
and drift.

Generated, imported, migrated, projected, AI-assisted, or externally modified state is
a candidate until the owning authority accepts it through its validation or
ratification boundary.

## 5. Policy, capability, and validity

Keep these questions distinct:

```text
support/capability  what can this implementation or host do?
requirement         what does this consumer need?
policy              what is this actor or environment allowed to request?
validity            is the proposed state semantically valid?
authority           who may decide or mutate the governed truth?
```

Capability does not imply permission. Permission does not imply semantic validity.
Policy should fail closed when uncertainty would make an unsafe operation appear
allowed.

## 6. Time and consistency

Every nontrivial operation has a temporal model. State whether work is synchronous,
asynchronous, scheduled, streaming, batch, tick-based, eventual, transactional, or
otherwise ordered in a way that affects semantics.

Every authority also needs an explicit consistency model appropriate to its invariants,
for example single-writer, strong transaction, optimistic concurrency, eventual
consistency, append-only history, snapshot plus replay, or an authoritative tick.

Cross-authority composition requires its own admission rule. Do not assume one global
transaction, identity, revision, or "latest" state. A combining boundary may need to
reason about owner-local revision, time, scope, completeness, freshness, availability,
provenance, correspondence, or a legal fallback. Admit only the facts the consumer
actually requires.

## 7. Storage and execution

Storage persists state; execution runs work; neither automatically owns semantic truth.

```text
Storage persists.
Execution realizes work.
Authority decides validity.
```

Storage and authority may be colocated, and an authority may execute in-process, in a
job, system, actor, service, process, or remote component. Choose execution and
deployment form after ownership and contract boundaries are understood.

A semantic contract should not change merely because an implementation moves from a
function to a worker or from an in-process component to a service, unless the move
changes the contract's actual semantics.

## 8. Failure, diagnostics, and observation

Failure behavior is part of a boundary contract. State whether failure rejects,
retries, rolls back, compensates, degrades, queues, preserves last-good state, fails
closed, or terminates because an internal invariant was violated.

Do not return success-shaped results for rejected, stale, partial, or degraded work.
Callers must be able to distinguish meaningful outcomes.

Diagnostics and operational observation are product surfaces for humans, tests, tools,
and automation. Prefer stable subjects and codes, severity, useful context, and
actionable messages where the boundary is durable enough to justify them.

A design with important failure modes but no way to observe them is incomplete.

## 9. Durable contracts and evolution

Version durable shared contracts deliberately: persisted formats, schemas, protocols,
public command/query contracts, and generated product formats should have stable
identity before broad use.

Design for replacement and deletion as well as growth. Valid evolution operations
include:

```text
promote  demote  split  merge  inline  extract  replace  delete  migrate
```

Migration strategy depends on the owning boundary. Use compatibility stages only when
real consumers require them, with an explicit removal condition. Do not preserve a
forwarding surface merely because deleting it would require consumer edits.

## 10. Abstraction, patterns, and boundary cost

Choose the lightest implementation form that protects the actual boundary. Functions,
modules, components, domain authorities, ECS, actors, event sourcing, jobs, services,
and cells are tools, not universal architecture layers.

Introduce a boundary or abstraction when it buys a concrete property such as semantic
ownership, isolation, security, independent scale, deployment independence,
reusability, or material reduction in drift.

Every boundary also costs code, tests, latency, versioning, debugging, observability,
coordination, and cognitive load. Reuse existing local patterns before inventing a new
abstraction, and simplify or delete abstractions whose cost is no longer justified.

## 11. Tests, fitness functions, and public surfaces

Tests should protect semantic invariants and boundary behavior, not only examples of
current implementation. Depending on the boundary, useful coverage may include domain
invariant tests, command behavior, validation/ratification, migration, schema
compatibility, projection equivalence, architecture guards, smoke tests, and
end-to-end evidence.

When an important architectural rule can be checked mechanically, prefer a fitness
function such as a test, lint, metadata check, schema validator, dependency-direction
check, or CI gate over prose alone. Validation policy and exact-head acceptance remain
owned by the [validation standard](validation.md).

A public API is also a usability surface. Normal consumers should be able to discover
and compose the supported path from package exports, documentation, examples, and
diagnostics without depending on private internals.

## 12. Automation is a caller, not an authority

Agents, scripts, generators, and workflow automation should use the same public
contracts, policy gates, validation, diagnostics, and acceptance boundaries as other
callers.

Automation may inspect, propose, generate candidates, and run validation. It must not
turn generated output into accepted truth by bypassing the authority that owns the
invariants.

## Design checklist

For a significant boundary, answer only the questions that materially apply:

1. **Authority** — who owns the truth?
2. **Invariants** — what must not be violated?
3. **Contract** — what crosses the boundary?
4. **Flow** — is it a command, query, event, product, projection, status, or diagnostic?
5. **Policy and validity** — who may request it, and who decides whether it is valid?
6. **Time** — what ordering or temporal model affects meaning?
7. **Consistency** — what consistency is required, including cross-owner admission?
8. **Storage** — what persists state, and is it distinct from authority?
9. **Execution** — where and how does work run?
10. **Failure and observation** — how does it fail, recover, and become observable?
11. **Evolution** — how is it versioned, migrated, replaced, simplified, or deleted?
12. **Cost** — is the boundary worth maintaining?

## Common anti-patterns

Avoid:

- UI, transport, storage, or caches silently becoming domain authority;
- direct mutation of foreign authoritative state;
- events emitted before the owning change is accepted;
- mutable projections becoming source truth;
- capability facts treated as permission;
- policy documented but not enforced;
- silent latest-of-every-source composition without an admission rule;
- unversioned durable formats that become de facto public contracts;
- universal object, command, registry, or extension models that erase ownership;
- services or other deployment boundaries created only for code organization;
- generated or automated output bypassing validation;
- compatibility surfaces retained without a proven consumer and removal condition.

## Related organization authority

This standard owns project-neutral software-design defaults only. Use the other
Engineering authorities for their own questions:

- [Authority and work](../governance/authority-and-work.md) for work state, durable versus operational authority, evidence, and document/work lifecycle;
- [Repository standard](repositories.md) for repository profiles, extraction, root contracts, and repository lifecycle;
- [Validation standard](validation.md) for canonical validation and exact-head acceptance;
- [GitHub standard](github.md) for repository settings and contribution workflow;
- [Runen family architecture](../architecture/runen-family.md) for current organization repository roles and cross-repository dependency direction;
- [Organization ADRs](../adrs/README.md) for accepted durable cross-repository decisions.

Repository-specific architecture, public contracts, runtime behavior, product policy,
and roadmap sequence remain owned by the repository responsible for them.
