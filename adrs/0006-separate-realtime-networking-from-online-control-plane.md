# ADR 0006: Separate realtime networking from online control-plane authority

- Status: accepted
- Date: 2026-08-24
- Owner: Dornglut organization
- Scope: Runen multiplayer and online-service repository boundaries

## Context

Dornglut now has `dornglut/runen-net` as the standalone authority for realtime multiplayer networking semantics and has created `dornglut/runen-online` for the online-game control plane around multiplayer products.

RunenNet already establishes an engine-independent networking boundary. Its normative identity and session contracts deliberately keep authentication principals, persistent account identity, matchmaking identity, server discovery, connect-ticket issuance, lobby membership, roster policy, and game settings outside RunenNet semantics. Without a corresponding cross-repository decision, those exclusions could be reintroduced inconsistently in RunenOnline, Runenwerk, or game-server integrations.

The two repositories also need a dependency rule that preserves independent semantics while allowing one game/server application to compose both.

## Decision

Dornglut separates realtime multiplayer networking from online-game control-plane authority.

### RunenNet

`dornglut/runen-net` owns host- and transport-independent realtime multiplayer networking semantics and the implementations that realize its accepted repository-local contracts.

RunenNet does not acquire ownership of persistent account systems, social/product services, matchmaking policy, server-fleet policy, or durable application state merely because those concerns participate in multiplayer admission or operation.

### RunenOnline

`dornglut/runen-online` is a standalone Rust framework for provider-neutral online-game control-plane semantics outside the active realtime networking core.

Its repository-local authority may subsequently define independently justified contracts for concerns such as persistent player/account association, parties and lobbies, matchmaking, match assignment, server allocation, and game-server admission grants. This ADR establishes the repository boundary only; it does not predefine that internal taxonomy or authorize implementation before the owning RunenOnline work accepts it.

RunenOnline does not own RunenNet participant/session/replication/delivery semantics, game simulation, ECS/runtime behavior, or provider-specific infrastructure semantics.

### Composition boundary

RunenNet and RunenOnline are sibling standalone frameworks. Neither framework depends on the other merely to define its semantic core.

A game server, application, or explicit integration package may consume both and establish mappings between their distinct identity domains. In particular, external authentication or persistent player identity does not become a RunenNet `ParticipantId`, a RunenOnline match identity does not automatically become a RunenNet `SessionId`, and server-allocation identity does not become transport-connection identity.

`dornglut/runenwerk` may integrate or orchestrate RunenNet and RunenOnline as a downstream integration platform, but it does not redefine either framework's semantics.

Authoritative game rules and simulation policy remain game/application concerns unless a separate accepted framework explicitly owns them.

### Provider boundary

Provider and infrastructure choices realize control-plane contracts but do not define them merely through adoption. PostgreSQL, Redis, OIDC providers, Nakama, Agones, GameLift, HTTP, gRPC, or equivalent technologies therefore remain adapters/infrastructure unless a narrower accepted contract says otherwise.

## Consequences

- RunenNet can evolve realtime networking without becoming a general backend platform.
- RunenOnline can evolve online-service semantics without becoming a second networking stack.
- game servers can compose both frameworks without collapsing persistent identity, match assignment, session identity, participant identity, or transport identity into one domain;
- Runenwerk remains a downstream integration consumer rather than hidden semantic authority;
- backend/provider selection remains replaceable and evidence-driven;
- RunenOnline must establish its own specification, architecture, roadmap, validation, and implementation authority before substantive product code is accepted.

## Alternatives considered

### Put online services inside RunenNet

Rejected. Authentication, matchmaking, allocation, durable player state, and social/product services have different lifecycles and correctness obligations from realtime session networking and are already explicitly excluded by current RunenNet authority.

### Make RunenOnline depend directly on RunenNet from inception

Rejected. Some RunenOnline capabilities can exist without an active realtime session, and a mandatory dependency would let an immature RunenNet public surface become hidden RunenOnline architecture authority. Integration belongs at an explicit consumer boundary unless later evidence justifies a narrower adapter dependency.

### Make Runenwerk the shared owner

Rejected. Runenwerk is an integration platform and downstream consumer. Moving shared semantics there would reverse the standalone-framework dependency direction.

### Adopt one backend provider as the architecture

Rejected. Provider products solve realization and operational problems but should not own portable RunenOnline semantics by default.

## Affected repositories

- `dornglut/engineering`
- `dornglut/runen-net`
- `dornglut/runen-online`
- `dornglut/runenwerk` as a potential downstream integrator

No product-repository semantic change is made by this ADR alone.

## Adoption or migration

1. Accept this ADR and the corresponding `architecture/runen-family.md` reconciliation in Engineering.
2. Bootstrap RunenOnline's repository-local authority and validation from the accepted organization boundary before substantive implementation.
3. Keep current RunenNet semantics and implementation unchanged; future RunenOnline/RunenNet or Runenwerk integration is authorized only by separately accepted work in the repository that owns that integration.

No source transfer, compatibility layer, provider migration, or coordinated product cutover is required by this decision.

## Supersedes

None.

## Superseded by

None.
