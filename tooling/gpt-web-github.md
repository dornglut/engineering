# GPT Web GitHub procedure

Use this procedure with the [agent-mediated repository workflow](../standards/github.md#agent-mediated-repository-changes) and [validation contract](../standards/validation.md).

## Defaults

For the current GPT Web + GitHub connector environment:

- use exact commit, tree, and file reads for repository state;
- do not attempt local `git clone`, worktrees, or `cargo validate` unless a checked-out execution environment is explicitly available;
- use draft-PR exact-head CI for bounded changes safe to publish before execution;
- prefer a normal checked-out executor when correctness requires execution before publication; when none is available, use the exact source-snapshot fallback below only if its fidelity requirements can be satisfied.

Do not repeatedly probe unavailable capabilities merely to rediscover these defaults.

## Inspection

Default to exact base → authority → repository inventory → exact relevant files → dependency closure.

Code search is optional discovery only. Skip it when known unavailable or unindexed. If it fails with an indexing or infrastructure error, fall back to deterministic reads rather than repeatedly retrying. Empty search results never prove absence.

If broad semantic closure cannot be established confidently with connector reads, use a checked-out/search-capable executor.

Read every modified existing file completely from the exact publication parent; never reconstruct from search output, partial ranges, truncated responses, stale revisions, or memory.

## Exact source-snapshot execution fallback

Use this fallback only when a normal checked-out executor is unavailable and the active environment can faithfully materialize the exact accepted repository source tree from immutable Git objects. When every requirement below is satisfied, that materialized workspace satisfies this procedure's checked-out-execution requirement for pre-publication work; it is still not a normal Git checkout and does not become Git publication, history, or ref authority.

The fallback must fail closed unless all applicable requirements below are satisfied:

1. Record the exact accepted commit and root tree SHA before materialization.
2. Enumerate the complete repository tree from immutable Git tree objects. If a recursive tree response is truncated, unavailable, or otherwise insufficient to prove completeness, traverse child trees deterministically. Stop if complete inventory cannot be established.
3. Retrieve file content by immutable blob SHA rather than by a moving branch or default-ref file read. Preserve supported Git object type and file-mode semantics needed by the repository.
4. Materialize and verify the complete accepted repository tree. Verify local bytes, paths, and relevant modes against the immutable object inventory before treating the workspace as exact.
5. Stop rather than approximate when required fidelity cannot be established, including unsupported symlinks, submodules, LFS-expanded content, binary content, executable/file modes, or another repository object type the active environment cannot reproduce faithfully.
6. Do not invent upstream Git history. Local synthetic Git metadata may be created only when a required command needs ordinary worktree or diff mechanics; its baseline tree must be the already verified accepted snapshot, and its local commits or refs must never be reported as GitHub history or publication evidence.
7. Prove required toolchains and dependencies are available to the materialized workspace before relying on it for compile-, generation-, format-, or test-driven correctness. A dependency or toolchain that cannot be resolved is a stop condition, not permission to publish unexecuted work.
8. Run the repository-required pre-publication commands in the materialized workspace and report only execution actually observed there. Snapshot execution does not replace repository-owned exact-head CI.
9. Construct the publication candidate separately under the existing complete off-ref candidate rules, using the accepted GitHub commit/tree as publication parent. Review the accepted-base→candidate diff before moving any branch. Never publish the reconstructed workspace or synthetic Git metadata wholesale.
10. Re-resolve default and feature refs immediately before publication and retain the existing guarded, non-force, no-partial-publication rules.

Do not use this fallback merely because it is possible. Prefer a normal checkout whenever it is available or when repository fidelity, Git metadata, dependency resolution, or required execution cannot be established more simply and confidently with the snapshot path.

## Publication

Construct one complete off-ref candidate before moving a branch. Initial work parents the accepted base; corrections parent the exact previous feature head.

Before publication, verify publication-parent→candidate and accepted-base→candidate diffs against authorized scope.

Re-resolve refs immediately before publication. Create a new branch directly at the completed candidate. For corrections, require the feature branch to still equal the expected previous head, then use a non-force fast-forward. A mismatch or rejected update is a stop condition.

Do not claim compare-and-swap semantics unless the connector explicitly provides an expected-old-head guard. Never publish coherent multi-file work as sequential branch-visible file writes.

## Validation and handoff

Normal bounded path: complete candidate → draft PR → exact-head CI → assurance → guarded merge. Do not simulate local canonical validation when no local executor exists. Any feature-head change requires fresh CI and assurance.

Use a normal checked-out executor for compile-driven implementation, generated or formatter-owned state, large mechanical refactors, binary/LFS/submodule/file-mode-sensitive work, broad semantic repository analysis, required files that cannot be read completely, or repositories without suitable exact-head CI whenever the exact source-snapshot fallback cannot faithfully satisfy the same required inspection and pre-publication execution.
