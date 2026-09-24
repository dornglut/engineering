# ADR 0011: Establish RunenInput as standalone device-input framework authority

- Status: accepted
- Date: 2026-09-24
- Owner: Dornglut organization
- Scope: Runen-family backend-neutral device-input observation and confirmed-state boundary

## Context

Runenwerk completed the input-boundary sequence required by its accepted device-input
architecture. The I0 investigation first selected internal boundary repair rather than
premature extraction. I1 then separated backend-neutral device observations and
confirmed state from backend APIs, Runenwerk product actions, UI interaction semantics,
and native-tablet acquisition. I2 subsequently proved the shared boundary with two
structurally different consumers: drawing/tablet input and the Render Lab real-time
camera.

The fresh I3 decision in
[dornglut/runenwerk#771](https://github.com/dornglut/runenwerk/issues/771)
selected `EXTRACTION_DESIGN_JUSTIFIED`. That decision found a coherent reusable
observation/reducer authority while also confirming that Runenwerk's current
`InputState` is not the extraction unit: it still owns integration, compatibility,
frame projection, ECS hosting, and backend-facing conveniences around the reusable
semantic core.

Dornglut therefore needs an organization-level repository boundary before any
successor repository is created or source authority moves.

## Decision

Dornglut establishes `dornglut/runen-input` as a **planned standalone Runen-family
Rust framework** for backend-neutral device-level input observations and deterministic
confirmed-state semantics.

RunenInput owns reusable semantics for:

- session-scoped source, device, tool, control, and contact identity whose invariants
  belong to neutral input;
- physical and logical keyboard evidence, key location, repeat, and reconciliation
  provenance as distinct facts;
- pointer buttons, absolute pointer position, and relative motion without reconstructing
  one from another;
- two-dimensional scroll, measurement domain, phase, and source provenance;
- touch/contact lifetime and cancellation;
- tablet/stylus physical observations demonstrated by real consumers, including
  tool/contact identity, pressure and orientation measurements, history, prediction,
  and evidence status;
- coordinate and measurement domains, source time, delivery/history role, evidence
  certainty, and observation origin;
- deterministic observation admission/order and confirmed-state reduction;
- framework-local conformance for those semantics.

RunenInput does **not** own:

- Runenwerk App, Host, native-window, event-loop, or frame lifecycle;
- winit, native OS APIs, acquisition, backend health, calibration acquisition, or
  recovery policy;
- Runenwerk product actions, bindings, defaults, rebinding, or camera behavior;
- RunenUI focus, capture, routing, widget targeting, text editing, accessibility, or
  other UI interaction semantics;
- committed text or IME composition;
- Draw stroke/tool behavior or Render Lab orbit/pan/zoom/sensitivity policy;
- RunenECS scheduling, resource, component, or system semantics;
- persisted replay/device-profile formats, cross-process/network input protocols, or
  stable hardware identity without separate future authority;
- a generic event bus, universal action framework, `RunenCore`, or speculative input
  families introduced only for symmetry.

The intended dependency direction is one-way. Backend and product integration may
consume RunenInput contracts; RunenInput does not depend upward on Runenwerk, RunenUI,
or RunenECS merely because those repositories consume input.

This ADR establishes repository-family membership, high-level ownership, and transfer
direction only. It does not stabilize a Rust API or package topology and does not make
the existing Runenwerk `InputState` a public framework contract.

Current reusable input source authority remains in Runenwerk until a successor default
branch is accepted under [ADR 0008](0008-adopt-bounded-source-authority-handoffs.md).
Before that authority switch, Runenwerk must complete the bounded source-boundary
correction required by I3 so the transferable semantic/reducer owner is explicit and
Runenwerk-only legacy projections remain outside it.

After successor acceptance, the accepted `runen-input` revision becomes sole semantic
source authority and the Runenwerk predecessor copy freezes. Runenwerk then migrates to
an immutable accepted successor revision and deletes the predecessor reusable
implementation in the same downstream cutover boundary. No forwarding package/module,
source include, compatibility alias, moving dependency, or duplicate writable
authority may survive the handoff.

## Alternatives considered

### Keep reusable device-input semantics permanently internal to Runenwerk

Rejected as the current direction. That was the correct outcome before boundary repair,
but I1/I2/I3 now demonstrate an independently useful semantic owner with two materially
different consumers and no required dependency on Runenwerk product/runtime semantics.

### Extract the current Runenwerk InputState

Rejected. `InputState` remains a Runenwerk integration/projection shell containing
backend compatibility, ECS hosting, text/frame conveniences, and product-facing
projections around the reusable neutral authority.

### Merge input semantics into RunenUI or a generic action framework

Rejected. Device observations, application actions, committed text, and UI
focus/routing/editing have different invariant owners. Sharing a consumer does not
justify merging those authorities.

### Make RunenInput own platform or Host realization

Rejected. Native event acquisition and application/window lifecycle remain adapter and
Runenwerk responsibilities. The reusable framework describes admitted device-level
evidence and confirmed state, not the event loop that delivered it.

## Consequences

- A standalone RunenInput successor may be bootstrapped after the Runenwerk
  pre-transfer source-boundary correction is accepted.
- Runenwerk remains the current semantic source authority until ADR 0008's successor
  acceptance switch.
- Backend adapters and Runenwerk integration become downstream consumers of the
  standalone framework after cutover.
- RunenUI, Draw, Render Lab, and product action systems retain their existing semantic
  ownership and receive explicit adapted input contracts where needed.
- New device families or persistence/network contracts remain consumer-pressure-driven
  future decisions rather than extraction prerequisites.
- The transfer requires a qualifying Engineering initiative because successor
  acceptance and predecessor deletion span repositories and are order-sensitive.

## Affected repositories

- `dornglut/engineering` owns this cross-repository decision and the transfer
  initiative.
- `dornglut/runenwerk` remains predecessor semantic source authority until successor
  acceptance, and owns pre-transfer boundary correction plus downstream cutover and
  predecessor deletion.
- future `dornglut/runen-input` will own the transferred reusable implementation,
  public contract, conformance, validation, and framework evolution after acceptance.
- `dornglut/runen-ui` is an explicit downstream semantic neighbor; this decision
  changes no RunenUI source or ownership.

## Adoption or migration

1. Accept this ADR, add RunenInput to planned Runen-family architecture, and activate
   the RunenInput standalone-authority-cutover initiative.
2. Complete a bounded Runenwerk pre-transfer source-boundary correction and exact
   transfer census without creating compatibility forwarding.
3. Bootstrap the successor repository under the current `rust-framework` repository
   standard and create repository-local transfer authority.
4. Prepare and validate the successor candidate while Runenwerk remains sole semantic
   source authority.
5. Accept the successor through its normal repository workflow; its accepted default
   branch becomes sole semantic source authority under ADR 0008.
6. Freeze the Runenwerk predecessor copy, pin Runenwerk to an immutable accepted
   successor revision, migrate consumers/adapters, and delete predecessor reusable
   source in the same downstream cutover.
7. Prove no forwarding, mirror, source include, moving dependency, private reach-through,
   or duplicate implementation authority remains; then reconcile RunenInput from
   planned to current family membership and close the transfer initiative.

## Supersedes

None.

## Superseded by

None.
