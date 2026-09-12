# Initiatives

An initiative is an optional durable charter for one large cross-repository outcome.

Use an initiative only when:

- at least two repositories are affected;
- multiple local issues or delivery phases are required;
- sequencing or migration order matters;
- rollback or closure evidence matters;
- one engineering issue cannot represent the outcome clearly.

An initiative links repository-local issues. It does not replace ADRs, the Engineering Portfolio, repository roadmaps, or pull requests.

Allowed statuses are `proposed`, `active`, `completed`, and `cancelled`.

## Active

- [RunenECS schedule semantics and Runenwerk lifecycle cutover](runenecs-schedule-semantics-and-runenwerk-lifecycle-cutover.md) — coordinate ordering-presence and publication-frontier migrations across RunenECS and Runenwerk

## Proposed

None.

## Closed

- [RunenECS standalone authority cutover](runenecs-standalone-authority-cutover.md) — completed standalone RunenECS authority handoff and Runenwerk exact-revision predecessor retirement
- [RunenGPU GX standalone authority cutover](runengpu-gx-standalone-authority-cutover.md) — completed standalone RunenGPU authority handoff and Runenwerk exact-revision cutover
- [Verified-head validation adoption](verified-head-validation.md) — completed immutable, exact-head repository validation adoption
- [Provider-neutral repository automation](provider-neutral-repository-automation.md) — cancelled by ADR 0003
