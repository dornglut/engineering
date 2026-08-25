# Validation standard

Every Dornglut repository owns the meaning of its canonical validation command.

Shared automation may invoke that command. It must not recreate or redefine the repository's validation semantics.

Engineering exposes its repository-owned validation through `cargo validate`, backed
by a local `xtask`. This removes Python-launcher choice from the Engineering interface;
the shared workflow remains a read-only caller and does not own these checks.
For Engineering, that one command runs a formatting check, Clippy with warnings denied,
locked workspace tests, and the pure repository-authority checker in that order.

## Canonical command

A maintained repository exposes one documented command that represents merge readiness.

The command must be:

- checked into the repository;
- deterministic enough for exact-head verification;
- runnable without repository write credentials;
- explicit about required toolchains and generated state;
- updated in the same repository when its meaning changes.

Focused tests may exist, but they do not replace the canonical baseline.

## Reusable orchestration

`dornglut/github-workflows` owns thin reusable workflow implementation.

A consumer workflow should:

- pin the reusable workflow to an immutable accepted commit;
- request read-only contents permission;
- pass no arbitrary shell command;
- expose stable check names;
- call the repository-owned command;
- avoid product-specific logic.

Reusable workflows must not:

- author or format source;
- push branches;
- commit generated fixes;
- merge their own output;
- require product secrets for ordinary validation;
- turn issue or model text into commands.

Third-party Actions are pinned to full commit SHAs with readable version comments and maintained through reviewed dependency updates.

## Exact-head evidence

An accepted base is the accepted default-branch revision from which pull-request work was prepared and reviewed. A reviewed feature head is the exact branch commit that contains the proposed change.

Exact-head validation evidence is a successful validation of that reviewed feature head. For a `pull_request` event, the expected revision is `github.event.pull_request.head.sha`; for `push` and `workflow_dispatch`, it is `github.sha`. The workflow explicitly selects the expected revision for checkout and proves that `git rev-parse HEAD` equals the expected revision before the repository-owned canonical command runs.

A moved feature head invalidates earlier exact-head evidence. A workflow definition may be loaded from a pull-request merge ref while the reusable workflow explicitly checks out feature-head repository content. These are separate facts: the definition ref is not the validated repository revision.

Synthetic merge-result evidence validates GitHub's generated pull-request merge revision. It can be useful when intentionally requested, but it must be named merge-result evidence and must not be substituted for reviewed feature-head evidence. Exact feature-head validation does not require duplicating the complete canonical suite against the synthetic merge result by default; final review still checks the accepted base and current mergeability.

An accepted squash merge is the immutable default-branch commit created after a pull request is accepted. It is neither the reviewed feature head nor a synthetic merge ref. Accepted-main push evidence is a successful default-branch push validation where `github.sha`, checkout ref, `git rev-parse HEAD`, and the accepted default-branch commit are equal.

Successful validation presents compact repository, event, revision, command, and conclusion evidence. Failed validation preserves command status, prints bounded diagnostics, retains a complete short-lived artifact, and removes temporary diagnostic state.

The authoring tool, local evidence, and model assessment do not replace independent CI. Local validation remains valuable preparation and should be reported honestly.

## GPT Web repository publication

When GPT Web authors a bounded repository change, it follows the same repository authority and exact-head acceptance rules as a checked-out executor, with these publication requirements:

1. Establish current repository authority and record the exact accepted base commit and tree.
2. Read every modified existing file completely from the exact publication parent. Never reconstruct a file from truncated, partial, stale, or remembered output.
3. Audit dependency closure before editing, including existing tests and assertions that encode the affected or former behavior.
4. Do not edit an unauthorized path. Demonstrate the dependency and amend the owning authority before expanding scope.
5. Construct all additions, modifications, deletions, and renames off-ref. Create the complete single-parent publication commit, or deliberate linear commit chain, before moving a branch reference.
6. Use the accepted base as the first publication parent. Later corrections use the exact previous feature head as their parent.
7. Re-resolve default-branch and feature-branch state before publication. Unexpected feature-branch movement is a stop condition. If default-branch movement materially changes authority, scope, dependencies, semantics, validation, merge behavior, or required tree identity, establish that default head as a new accepted base and reconstruct the feature on a new branch and pull-request lineage rather than rewriting the old one.
8. Publish new work by creating the isolated branch directly at the completed head. Advance an existing feature branch only by non-force fast-forward from the verified previous head. Never write directly to the default branch or expose connector-induced partial-file states.
9. Verify publication-parent-to-new-head for the current publication and accepted-base-to-feature-head for total scope. Reconcile every changed, added, deleted, or renamed path and every material semantic delta with authority.
10. Use a draft pull request for independent execution validation. Repository-owned canonical validation remains authoritative; GitHub Actions may execute it for GPT Web when local execution is unavailable.
11. Treat CI as falsification, not scope authority. Mechanical corrections remain inside existing authority. Semantic, baseline, dependency, or out-of-scope failures are investigated before behavior or scope changes.
12. Any feature-head movement invalidates validation, review, and assurance tied to the previous head.
13. Before acceptance, reconcile the exact final head with owning authority, dependency closure, the complete accepted-base-to-head diff, canonical exact-head validation, material pull-request discussion and reviews, unresolved review threads, and current default-branch state.
14. Immediately before merge, re-resolve feature and default-branch heads, require the feature branch to equal the exact reviewed SHA, reconfirm current-base compatibility, and guard the merge by that exact SHA.
15. Where tree identity is an acceptance requirement, verify that the accepted merge tree equals the reviewed feature tree and that the resulting default branch is the intended accepted state.

Prefer one atomic publication commit for bounded GPT Web work. Multiple deliberate semantic commits are acceptable only when they are linear, single-parent, constructed off-ref, and published as one coherent head.

Use a checked-out executor such as Codex when correctness materially depends on pre-publication compilation, generated-state updates, large or formatting-sensitive transformations, binary assets, or tooling unavailable to GPT Web.

## Documentation repositories

Documentation-oriented repositories validate at least:

- required authority files;
- UTF-8 text and final newlines;
- whitespace;
- repository-relative links;
- active namespace rules;
- ADR numbering, metadata, indexing, and supersession;
- initiative status, indexing, and closure;
- absence of retired duplicate authority paths;
- absence of volatile PR, branch, or workflow-run state in durable authority documents.

## Security boundary

Validation workflows are read-only.

A source-writing workflow is not validation and requires a separately accepted authority, credential, threat model, and review path.

Temporary source-export or self-authoring workflows must not be introduced to compensate for an authoring-tool limitation. Select a suitable checked-out executor instead.

## Adoption

ADR 0004 adopts this document as the target standard. Existing repositories may remain temporarily nonconformant only during an explicit owning-repository migration. New changes must not increase divergence, and each exception closes through the corresponding normalization work.

## Failure behavior

Validation fails closed when:

- required authority is absent;
- exact-head checks fail;
- a generated product is stale;
- a public contract or repository policy is inconsistent;
- a supersession or closure record is incomplete;
- active documentation points to retired or historical authority.

Failures are corrected in the owning repository through an ordinary pull request.
