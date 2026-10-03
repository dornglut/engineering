# Software design standard

This standard is Dornglut's organization-wide default for project-neutral software
design. It applies when an owning repository has no more specific accepted authority
for the question. Repository code and tests still own current behavior, repository
ADRs own local durable architecture, and organization ADRs own accepted
cross-repository architecture. More-specific accepted authority MAY specialize this
standard.

This document is not a product architecture, roadmap, implementation plan, or catalog
of mandatory patterns. It defines project-neutral design defaults and review criteria.

## Normative force

Only the all-caps key words `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and
`MAY` carry special normative meaning in this document:

- `MUST` and `MUST NOT` state requirements while this standard governs the question;
- `SHOULD` and `SHOULD NOT` state strong defaults that can be departed from only
  for a concrete, reviewable reason;
- `MAY` states permission, not recommendation.

Lowercase forms retain their ordinary English meaning. Bare imperatives do not create
additional hidden requirement levels. Examples, explanatory mappings, and named
patterns are informative and MUST NOT independently authorize work or architecture.

## Core model

Design decisions SHOULD start from relevant boundary pressure rather than pattern
preference:

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

Only the dimensions material to the design need explicit treatment.

## Strategic design posture

Dornglut optimizes for long-term code health and conceptual simplicity, not minimum
initial code volume. Additional modules, types, boundaries, validation, diagnostics,
or tooling MAY be justified when they materially buy durable properties such as:

- correctness and invariant protection;
- explicit ownership, information hiding, and lower coupling;
- type safety and clear contracts;
- observability, diagnosability, and testability;
- efficient or scalable algorithms, data representation, and execution;
- evolvability, replaceability, and deletion;
- reusable framework quality when reuse is an accepted repository purpose.

More structure is not automatically more complexity. A larger decomposition can reduce
system complexity when it reduces hidden dependencies, the number of places that need
coordinated change, or the amount of unrelated implementation knowledge required to
make a safe change. Conversely, a small file or short implementation can still be
architecturally complex when it concentrates unrelated responsibilities or leaks
decisions across boundaries.

Deliberate design investment MAY precede an immediate feature when current accepted
authority or demonstrated domain pressure already establishes material volatility,
boundary pressure, or a workload/scale dimension targeted by the design.
Implementations MUST NOT add speculative product behavior or extension machinery solely
for hypothetical consumers or requirements whose actual shape is still unknown.
Preserving implementation freedom around known pressure remains valid design work.

## 1. Authority and invariants

An authority is the owner that decides what is valid for one semantic invariant set.
Usage, storage, presentation, transport, or execution does not by itself create
authority.

Each semantic invariant set SHOULD have one clear authority. An invariant that matters
MUST be enforced by its owning authority or an explicit validation boundary, not only
by UI, callers, documentation, or convention.

Different representations MAY coexist when they own different invariants. Their
correspondence SHOULD be explicit rather than inferred from one universal identity or
one global object model.

Helpers and reusable implementation MUST NOT be promoted to semantic authority merely
because they are shared.

## 2. Boundary contracts and flows

Boundaries SHOULD expose owner-defined contracts rather than foreign internals.
Contracts can include function or interface signatures, commands, queries, events,
DTOs, immutable snapshots, schemas, persisted formats, protocol messages, products,
projections, status, and diagnostics.

When this standard uses the following flow terms, they mean:

```text
Command     request to change state
Query       request to read state
Event       accepted fact that happened
Product     owner-defined formed or derived output
Projection  derived read or view model
Status      observed current condition
Diagnostic  explanation of a failure, warning, or rejection
```

A proposed change capable of violating owned invariants MUST be accepted or validated
by the owning authority before it becomes authoritative. Unrelated semantic owners
MUST NOT be collapsed into one universal command model merely to unify transport or
invocation.

Reads across an authority boundary MUST use an owner-defined contract rather than
foreign private mutable state. The owner contract MAY be a query result, immutable
snapshot, product, projection, prepared input, stream, or another owner-defined value.

## 3. Dependency direction and representation

Stable semantic rules SHOULD remain independent from incidental outer wiring. Concrete
repository structure MAY differ.

Stable semantic contracts MUST NOT depend on UI, transport, persistence, vendor, host,
or deployment details unless those details are themselves part of the semantics or a
more-specific accepted decision establishes the dependency.

Dependency inversion MUST NOT be used to justify universal registries, global service
locators, vague extension points, or a shared meta-model that erases distinct owners.

When an editable or persistent description and an optimized executable realization
have materially different responsibilities, they SHOULD remain distinct.

## 4. Authoritative and derived state

Caches, projections, indexes, view models, and similar read-oriented structures are
derived unless an accepted design explicitly promotes them to authority.

Derived state SHOULD be rebuildable or reproducible from owned source contracts when
practical. If it cannot be, the owning authority and recovery semantics MUST be
explicit.

Provenance or production mechanism does not by itself establish authority. The owning
authority MUST define whether and how externally produced, generated, imported,
migrated, or projected state is admitted. Consuming another authority's accepted
output MUST NOT silently transfer that authority's invariants or mutation rights to the
consumer.

## 5. Policy, capability, and validity

The following questions MUST remain distinct when they materially apply:

```text
support/capability  what can this implementation or host do?
requirement         what does this consumer need?
policy              what is this actor or environment allowed to request?
validity            is the proposed state semantically valid?
authority           who is authorized to decide or mutate the governed truth?
```

Capability MUST NOT be treated as permission. Permission MUST NOT be treated as
semantic validity.

Policy that gates unsafe or privileged operations SHOULD fail closed when uncertainty
would otherwise make the operation appear allowed.

## 6. Time and consistency

When ordering, timing, concurrency, or history affects semantics, the temporal model
MUST be explicit.

When different actors or observations can see different state in a way that affects
correctness, the required consistency guarantees MUST be explicit.

When correctness depends on compatibility between facts from multiple authorities, the
combining boundary MUST define its admission criteria. It MUST NOT silently assume one
global transaction, identity, revision, or "latest" state unless such a contract
actually exists.

Admission MAY consider owner-local revision, time, scope, completeness, freshness,
availability, provenance, correspondence, or an explicitly legal fallback. Admission
SHOULD depend only on facts required by the consumer's semantics.

## 7. Storage and execution

Storage persists state; execution realizes work; neither automatically owns semantic
truth.

Storage and execution placement MUST NOT silently acquire semantic authority. Storage
and authority MAY be colocated, and execution MAY move across deployment boundaries
when the owner contract permits it.

A semantic contract MUST NOT change solely because execution or deployment placement
changes unless the move changes the contract's actual semantics.

## 8. Failure, diagnostics, and observation

A boundary whose failures affect caller or system behavior MUST define how materially
different outcomes are represented or handled. Outcomes that callers need to handle
differently MUST remain distinguishable.

Failure modes that affect correctness, durability, security, or supported operation
MUST be observable to the relevant callers, operators, tests, or automation.
Diagnostics SHOULD identify the affected subject and provide enough stable context to
distinguish and act on meaningful failures.

## 9. Durable contracts and evolution

Durable shared contracts SHOULD define an evolution or versioning strategy before broad
use when compatibility or persistence can outlive one implementation revision.

Design SHOULD support migration, replacement, simplification, and deletion as well as
growth.

A compatibility surface MUST be retained while a current published contract or
consumer obligation requires it. A temporary compatibility surface MUST have an
explicit removal condition and SHOULD NOT remain solely to avoid consumer edits after
the obligation ends.

## 10. Abstraction, information hiding, and boundary cost

Concrete implementation and deployment patterns are tools, not mandatory architecture
layers.

Boundaries SHOULD expose narrow contracts that hide substantial implementation
complexity and volatile decisions from consumers. A useful boundary reduces what its
callers need to know about storage layout, caching, algorithms, scheduling, backend
choice, physical encoding, or another replaceable realization detail.

A new boundary or abstraction SHOULD buy a concrete property such as semantic
ownership, information hiding, isolation, security, independent scale, deployment
independence, testability, observability, reuse under an accepted reusable role,
freedom to change physical realization, or material reduction in drift and coupled
change.

Generality MAY be justified when the owning repository has an accepted foundational or
reusable role, or when a more orthogonal contract removes real special cases and
reduces total complexity. A universal meta-model MUST NOT be introduced solely because
several callers look superficially similar.

Concrete optimization claims and trade-offs between viable implementations SHOULD be
supported by measurement or other bounded evidence. A known complexity or resource
bound that conflicts with an accepted workload, scale target, or unavoidable growth
dimension MUST NOT be ignored solely under a "measure later" rationale.

Algorithmic complexity, indexing strategy, memory traffic, data locality, batching, and
parallelism MAY be reasoned about architecturally before a concrete bottleneck is
measured when those properties are already material to the accepted design pressure.
Physical optimization strategy SHOULD remain private unless it is itself part of the
required semantic contract.

Every boundary carries code, testing, debugging, versioning, coordination, and
maintainer cost. Additional structure SHOULD remain only while the durable property it
buys justifies that cost.

## 11. Decomposition and source structure

Four related forms of decomposition MUST NOT be conflated:

```text
semantic decomposition        what concepts and authorities exist?
dependency decomposition      which dependency directions are allowed?
implementation decomposition  which decisions and responsibilities are hidden together?
physical decomposition        which source units contain the implementation?
```

Semantic ownership and implementation boundaries SHOULD be determined before physical
placement is treated as architectural evidence. Physical separation into files,
modules, packages, or other source units MUST NOT by itself be treated as proof of
semantic authority or coherent implementation decomposition.

Decomposition SHOULD be introduced when separation creates a coherent boundary that
materially reduces coupled knowledge, dependency surface, state or lifecycle coupling,
or unrelated reasons to change. Differences in lifecycle, dependencies, failure
behavior, state ownership, policy, security, or performance are signals to inspect;
they are not by themselves sufficient reason to split.

A structural refactor MUST NOT be considered complete solely because code moves into
more files. It SHOULD reduce at least one meaningful concentration of unrelated
knowledge, mutable state, dependency surface, volatile decisions, lifecycle
responsibilities, or reasons to change. A large orchestration function or type MAY
remain a responsibility concentration even when its helpers live in separate sibling
modules.

One cohesive algorithm SHOULD NOT be fragmented solely to satisfy file, function, or
line-count aesthetics. Size is evidence to inspect, not an architectural limit.
Reviewers SHOULD evaluate whether a unit is understandable in isolation, whether its
dependencies are necessary, whether replaceable decisions remain hidden, and whether
changes for unrelated reasons can be made independently.

Physical source structure SHOULD make the resulting responsibilities discoverable.
Names SHOULD reflect responsibility, and local helpers SHOULD remain local until a real
shared responsibility or shared knowledge emerges. Sharing implementation MUST NOT by
itself create semantic authority. Repository-specific language, framework conventions,
and file-layout rules remain owned by the repository that needs them.

## 12. Tests, fitness functions, and public surfaces

Tests SHOULD protect semantic invariants and boundary behavior rather than only examples
of current implementation.

When an important architectural rule can be checked mechanically at reasonable cost,
the owning repository SHOULD prefer a fitness function such as a test, lint, metadata
check, schema validator, dependency-direction check, or CI gate over prose alone.
Validation policy and exact-head acceptance remain owned by the
[validation standard](validation.md).

A public API is also a usability surface. Normal consumers SHOULD be able to discover
and compose the supported path from public exports, documentation, examples, and
diagnostics without depending on private internals.

## 13. Automation is a caller, not an authority

Agents, scripts, generators, and workflow automation MUST use the same public
contracts, policy gates, validation, diagnostics, and acceptance boundaries as other
callers unless more-specific accepted authority explicitly defines another path.

Automation MAY inspect, propose, generate candidates, and run validation. It MUST NOT
turn generated output into accepted truth by bypassing the authority that owns the
invariants.

## Design checklist

For a significant boundary, the following questions provide review coverage. Only the
questions that materially apply need answers:

1. **Authority** — who owns the truth?
2. **Invariants** — what conditions cannot be violated?
3. **Contract** — what crosses the boundary?
4. **Flow** — is it a command, query, event, product, projection, status, or diagnostic?
5. **Policy and validity** — who can request it, and who decides whether it is valid?
6. **Time** — what ordering or temporal model affects meaning?
7. **Consistency** — what consistency is required, including cross-owner admission?
8. **Storage** — what persists state, and is it distinct from authority?
9. **Execution** — where and how does work run?
10. **Failure and observation** — how does it fail, recover, and become observable?
11. **Evolution** — how is it versioned, migrated, replaced, simplified, or deleted?
12. **Decomposition** — are semantic ownership, dependency direction, hidden
    implementation decisions, and physical source placement aligned without being
    conflated?
13. **Cost and quality** — which durable properties justify this structure, what coupled
    change or unrelated knowledge does it remove, and which concrete performance claims
    need evidence?

## Conventional terminology mapping

Common programming principles remain useful search and review vocabulary, but they are
explanatory mappings onto this standard rather than separate design authorities:

| Conventional term | Interpretation in this standard |
| --- | --- |
| KISS | Conceptual simplicity and explicit ownership rather than minimum files, types, or lines. |
| DRY | One owner for genuinely shared knowledge or responsibility; similar syntax alone does not justify a shared abstraction. |
| YAGNI | No speculative capability; preserving implementation freedom around known volatility remains valid design work. |
| SOLID | Responsibility, substitution, interface, and dependency-direction ideas used as boundary heuristics rather than a class or trait mandate. |
| Separation of Concerns | Separation of materially different ownership, lifecycle, dependency, failure, policy, or change concerns without empty layers. |
| Avoid Premature Optimization | Evidence for concrete optimization claims and trade-offs while known complexity and resource bounds remain legitimate architectural concerns. |
| Law of Demeter | Direct owner contracts instead of transitive implementation knowledge; forwarding chains are not information hiding. |

## Common anti-patterns

Common anti-patterns include:

- UI, transport, storage, execution, or caches silently becoming semantic authority;
- direct mutation of foreign authoritative state or dependency on foreign private
  mutable internals;
- mutable derived state becoming source truth without an explicit authority change;
- capability facts being treated as permission or semantic validity;
- silent composition of independently evolving authority outputs without required
  compatibility criteria;
- durable shared contracts used across revisions without an evolution or compatibility
  strategy;
- universal registries, command models, extension models, or meta-models that erase
  real ownership;
- thin abstractions or forwarding layers that add indirection without hiding a real
  decision or responsibility;
- physical file/module splitting presented as architectural decomposition while
  responsibility concentration remains;
- speculative capability or generic extension machinery with no current requirement,
  established variation, or accepted reusable role;
- deduplicating similar code into false shared ownership;
- ignoring a known complexity or resource bound that conflicts with an accepted
  workload or scale requirement;
- generated or automated output bypassing normal validation or acceptance;
- compatibility surfaces retained without a current obligation or justified consumer
  need, or temporary compatibility surfaces with no removal condition.

## Related organization authority

This standard owns project-neutral software-design defaults only. Other Engineering
authorities own their respective questions:

- [Authority and work](../governance/authority-and-work.md) owns work state, durable
  versus operational authority, evidence, and document/work lifecycle;
- [Repository standard](repositories.md) owns repository profiles, extraction, root
  contracts, and repository lifecycle;
- [Validation standard](validation.md) owns canonical validation and exact-head
  acceptance;
- [GitHub standard](github.md) owns repository settings and contribution workflow;
- [Runen family architecture](../architecture/runen-family.md) owns current
  organization repository roles and cross-repository dependency direction;
- [Organization ADRs](../adrs/README.md) own accepted durable cross-repository
  decisions.

Repository-specific architecture, public contracts, runtime behavior, product policy,
and roadmap sequence remain owned by the repository responsible for them.
