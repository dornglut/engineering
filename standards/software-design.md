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

## Strategic design posture

Dornglut optimizes for long-term code health and conceptual simplicity, not minimum
initial code volume. Additional modules, types, boundaries, validation, diagnostics,
or tooling are justified when they materially buy durable properties such as:

- correctness and invariant protection;
- explicit ownership, information hiding, and lower coupling;
- type safety and clear contracts;
- observability, diagnosability, and testability;
- efficient or scalable algorithms, data representation, and execution;
- evolvability, replaceability, and deletion;
- reusable framework quality when reuse is an actual repository purpose.

More structure is not automatically more complexity. A larger decomposition can reduce
apparent complexity when it lowers cognitive load, change amplification, hidden
dependencies, or the amount of foreign knowledge a maintainer must hold at once.
Conversely, a small file or short implementation can still be architecturally complex
when it concentrates unrelated responsibilities or leaks decisions across boundaries.

Deliberate design investment may precede an immediate feature when the pressure is
structurally predictable: for example durable public-contract evolution, a known
cross-owner boundary, a foundational reusable-framework role, or an asymptotic scaling
constraint. Future-proof the stable seam and preserve implementation freedom; do not
pre-build speculative product behavior whose requirements are still unknown.

Prefer:

```text
clear model + explicit seam + hidden complexity + replaceable realization
```

over:

```text
minimum initial code + implicit coupling + later compatibility debt
```

## Conventional principles as review lenses

The conventional KISS, DRY, YAGNI, SOLID, Separation of Concerns, premature-
optimization, and Law-of-Demeter principles are useful review vocabulary, but they are
not independent authorities or mechanical rules. Interpret them through the ownership,
invariant, contract, evolution, and cost model in this standard.

### KISS

Prefer the simplest coherent mental model that protects the required semantics and
intended evolution path. Simplicity means obvious ownership, contracts, lifecycle,
failure behavior, and dependency direction; it does not mean the fewest files, types,
modules, or lines of code.

Push unavoidable complexity behind narrow, explicit contracts instead of spreading it
among callers. Do not simplify by omitting invariants, collapsing distinct authorities,
or concentrating unrelated reasons to change.

### DRY

Keep each durable semantic rule, invariant, protocol fact, generated contract, and
authoritative decision in one canonical owner. Remove duplicated knowledge that would
otherwise have to change in lockstep.

Do not deduplicate merely similar code across independent authorities when doing so
would create false ownership or coupling. Repetition can be cheaper and more truthful
than a shared abstraction that owns no shared invariant.

### YAGNI

Do not implement speculative product capability, compatibility surfaces, plugin points,
registries, configuration, or generality whose requirements are not known well enough
to define a truthful contract.

YAGNI does not prohibit strategic design. It is valid to establish a clean seam,
reserve implementation freedom, or design a foundational reusable contract for
structurally predictable pressure without implementing the hypothetical future feature
itself.

### SOLID

Use SOLID as boundary heuristics rather than as a class-oriented architecture mandate:

- responsibilities follow coherent authority, invariants, lifecycle, and reasons to
  change;
- extension happens through owned contracts without exposing unrelated internals;
- substitutable implementations preserve the documented semantic contract;
- interfaces expose only the capability their consumers need;
- dependencies point toward stable semantics rather than incidental outer wiring.

Traits, interfaces, dependency inversion, and extension points still carry cost. Do
not introduce them solely to make the code look SOLID.

### Separation of Concerns

Separate concerns when they have materially different authority, invariants, lifecycle,
failure semantics, dependencies, scaling behavior, security policy, or reasons to
change. Keep related complexity together when splitting it would only create thin
pass-through layers.

Physical structure should make responsibility discoverable. File count and line count
are signals, not architecture rules.

### Avoid premature optimization

Correctness and truthful semantics come first, and targeted optimization claims should
be supported by measurement or bounded evidence. Profile and benchmark when choosing
among concrete performance tradeoffs or attributing a bottleneck.

This does not require intentionally weak foundations until a profiler complains.
Algorithmic complexity, memory traffic, data locality, batching opportunities,
parallelism boundaries, and scalable query topology are legitimate design concerns when
their pressure is known. Prefer designs that preserve room for optimization without
exposing one physical optimization strategy as semantic identity.

### Law of Demeter

Depend on the direct semantic owner or its explicit public contract. Do not reach
through collaborators into transitive implementation state or require callers to know
an internal object graph.

Do not satisfy this principle by adding chains of forwarding wrappers. A boundary
should hide a real decision or responsibility; indirection without information hiding
only relocates complexity.

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

Choose the simplest coherent implementation form that protects the actual boundary,
its known quality requirements, and its structurally predictable evolution pressure.
Functions, modules, components, domain authorities, ECS, actors, event sourcing, jobs,
services, and cells are tools, not universal architecture layers.

Prefer deep boundaries: a small, clear contract may hide substantial implementation
complexity when doing so reduces what consumers must understand. Avoid thin wrappers,
pass-through services, marker abstractions, or interface layers that add indirection
without hiding a decision, invariant, policy, or physical realization.

Introduce a boundary or abstraction when it buys a concrete property such as semantic
ownership, information hiding, isolation, security, independent scale, deployment
independence, testability, observability, reusable framework value, performance
freedom, or material reduction in drift and change amplification.

Generality is justified when the owner is genuinely foundational or reusable, or when a
more orthogonal contract removes special cases and reduces total complexity. Keep that
generality bounded by real invariant and consumer pressure; do not create a universal
meta-model merely because several callers look superficially similar.

Every boundary also costs code, tests, latency, versioning, debugging, observability,
coordination, and cognitive load. The goal is not the fewest boundaries or the most
boundaries: it is the architecture whose justified structure minimizes long-term
system complexity while preserving required quality attributes.

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
12. **Cost and quality** — which durable properties justify this structure, what cognitive or change cost does it remove, and are performance claims measured or structurally justified?

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
- minimizing files, types, or modules by concentrating unrelated responsibilities;
- thin abstractions or forwarding layers that add indirection without information hiding;
- speculative capability or generic extension machinery with no truthful contract pressure;
- deduplicating similar code across independent authorities into false shared ownership;
- targeted micro-optimization claims without evidence, or knowingly unscalable foundations excused as "measure later";
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
