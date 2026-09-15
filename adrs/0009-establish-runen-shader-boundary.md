# ADR 0009: Establish RunenShader as standalone shader-toolchain authority

- Status: accepted
- Date: 2026-09-15
- Owner: Dornglut organization
- Scope: Runen-family shader-source, shader-toolchain, GPU, and rendering repository boundaries

## Context

`dornglut/runen-gpu` is the standalone authority for backend-neutral GPU resource, program-admission, pipeline, work, submission, transfer, surface, and device semantics. Its accepted boundary deliberately keeps shader source discovery and authoring-toolchain policy outside RunenGPU, while canonical WGSL remains the program source admitted before private backend realization.

Dornglut has no standalone authority for reusable shader-source composition, frontend compilation, canonical shader-artifact formation, source-facing diagnostics, or source provenance. Leaving those concerns to individual renderers, applications, or GPU consumers would duplicate source semantics and couple reusable authoring/toolchain behavior to unrelated rendering or execution policy.

The Runen language repository also establishes a useful architectural discipline: semantic ownership is separate from compiler representation, verification evidence, and physical realization; logical identity is not inferred from filesystem or physical representation; and independently owned semantic domains compose through explicit bridges rather than implementation coincidence. RunenShader should apply those engineering principles without acquiring Runen language semantics or a production dependency on `dornglut/runen`.

## Decision

Dornglut establishes `dornglut/runen-shader` as a standalone Rust framework/toolchain authority for reusable shader-source and shader-compilation semantics.

### RunenShader

RunenShader owns repository-local contracts for explicit shader-compilation inputs, logical shader package/module/source-unit identity, frontend selection, source and module resolution, dependency revision identity, compilation outcomes, canonical shader-artifact formation, source provenance, source mapping, diagnostics, and reproducibility.

The repository-local specification owns the exact normalized semantic model. Frontend compiler structures, intermediate representations, filesystem paths, caches, process state, and vendor reflection do not become semantic authority merely because an implementation uses them.

RunenShader does not own Runen language semantics; GPU adapter/device/resource/work/submission semantics; GPU program-interface, binding, or pipeline admission; renderer material, lighting, visibility, frame-composition, or image-formation semantics; application recovery or last-known-good policy; filesystem watching or hot-reload policy; or package-registry and network-fetch policy.

### Canonical program-product boundary

The initial RunenShader canonical program product is WGSL plus the RunenShader-owned artifact evidence required by its repository-local contract.

Canonical WGSL is an explicit composition boundary, not shared semantic ownership. RunenShader establishes that one exact canonical artifact was formed from one admitted shader-compilation input. RunenGPU independently establishes whether canonical WGSL is admissible for its GPU program, interface, binding, pipeline, and execution contracts.

RunenShader reflection or frontend metadata must not become a second authority for RunenGPU program-interface facts. RunenGPU remains source-producer-neutral and may admit canonical WGSL supplied by RunenShader or another valid producer.

### Dependency direction

RunenShader and RunenGPU are sibling standalone frameworks. Neither requires a production dependency on the other merely to define its semantic core.

A consumer that needs both concerns, including future `dornglut/runen-render`, may depend on both repositories and own an explicit integration that submits RunenShader canonical WGSL into RunenGPU program admission. That integration does not transfer shader-source authority into RunenGPU or GPU-execution authority into RunenShader.

RunenShader does not depend on `dornglut/runen` merely because its specification and architecture use compatible design principles. The Runen language repository remains the sole authority for Runen programming-language semantics.

### Frontend and realization neutrality

This organization decision does not standardize WESL, Slang, plain WGSL, a universal shader IR, or a generic frontend-plugin mechanism. Concrete frontends and compiler dependencies are repository-local realization and product-surface decisions that require accepted RunenShader work.

A frontend becomes supported only through RunenShader's repository-local contracts, validation, and conformance evidence. Adoption of a frontend compiler does not make that compiler's private IR, reflection model, filesystem resolver, or extension semantics a Dornglut-wide authority.

### Repository classification

When created, `dornglut/runen-shader` uses the `rust-framework` repository profile. It is public, uses default branch `main`, begins owner-maintained under contribution classification `owner-only`, and uses the product library/SDK/engine/toolchain licensing class: `GPL-3.0-only` publicly with the separately governed commercial licensing path.

The repository owns one canonical read-only validation command, expected to be `cargo validate`, and a thin immutable shared-workflow caller in accordance with organization standards.

## Consequences

- reusable shader authoring and compilation gain one semantic owner rather than being duplicated in RunenGPU, RunenRender, Runenwerk, or applications;
- RunenGPU remains backend-neutral GPU execution authority and does not become a shader build system;
- future RunenRender can consume both shader artifacts and GPU execution without becoming the hidden owner of either framework;
- logical shader identities and dependencies can remain independent from filesystem and build-system conventions;
- frontend implementations may evolve or be replaced without changing the RunenGPU public contract when they preserve the RunenShader canonical product contract;
- repository-local RunenShader semantics, implementation, roadmap, and issues must be established before substantive shader-toolchain code is accepted.

## Alternatives considered

### Put shader authoring and compilation inside RunenGPU

Rejected. RunenGPU owns generic GPU execution and canonical WGSL admission. Filesystem/module/frontend/toolchain concerns have distinct invariants and would couple GPU consumers to authoring policy they may not need.

### Put shader authoring and compilation inside RunenRender

Rejected. Compute and other non-render GPU consumers may require the same source/toolchain capability, while renderer materials and image-formation policy are a separate semantic domain.

### Make RunenShader depend directly on RunenGPU

Rejected as a mandatory core relationship. Forming a canonical shader artifact does not require a GPU context, device, resource, pipeline, or submission authority. Consumers that need execution can compose the sibling frameworks explicitly.

### Treat one frontend compiler as the semantic model

Rejected. WESL, Slang, WGSL tooling, and future frontends are realizations of the source-to-artifact boundary. Their private module model, reflection, IR, resolver, or diagnostics must not silently define portable RunenShader semantics.

### Extend the Runen programming language repository to own shader tooling

Rejected. `dornglut/runen` owns Runen language semantics and its compiler/proving work. Shader authoring frontends and canonical WGSL artifact formation are an independent toolchain concern unless a future accepted cross-repository decision establishes a concrete Runen-language shader bridge.

## Affected repositories

- `dornglut/engineering`
- planned `dornglut/runen-shader`
- `dornglut/runen-gpu` as the canonical-WGSL execution-side sibling
- planned `dornglut/runen-render` as a future consumer of both
- `dornglut/runen` only as independent design precedent; no Runen semantic change is made

No product-repository semantic change is made by this ADR alone.

## Adoption or migration

1. Accept this ADR and reconcile `architecture/runen-family.md`.
2. Create `dornglut/runen-shader` with the repository classification and validation boundary established above.
3. Bootstrap RunenShader's repository-local normative specification, architecture, testing contract, roadmap/status, licensing representation, and issue-owned delivery plan before substantive implementation.
4. Accept concrete frontend support and implementation only through RunenShader-owned issues and exact-head validation.
5. Adopt RunenShader from RunenRender, Runenwerk, or other consumers only through separately accepted consumer work.

No source transfer, compatibility layer, Runen language change, RunenGPU semantic change, or RunenRender implementation is authorized by this decision. Any future source-authority transfer follows ADR 0008 separately.

## Supersedes

None.

## Superseded by

None.
