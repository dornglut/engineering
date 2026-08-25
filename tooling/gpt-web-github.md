# GPT Web GitHub procedure

Use this procedure with the [agent-mediated repository workflow](../standards/github.md#agent-mediated-repository-changes) and [validation contract](../standards/validation.md).

## Defaults

For the current GPT Web + GitHub connector environment:

- use exact commit, tree, and file reads for repository state;
- do not attempt local `git clone`, worktrees, or `cargo validate` unless a checked-out execution environment is explicitly available;
- use draft-PR exact-head CI for bounded changes safe to publish before execution;
- use a checked-out executor when correctness requires execution before publication.

Do not repeatedly probe unavailable capabilities merely to rediscover these defaults.

## Inspection

Default to exact base → authority → repository inventory → exact relevant files → dependency closure.

Code search is optional discovery only. Skip it when known unavailable or unindexed. If it fails with an indexing or infrastructure error, fall back to deterministic reads rather than repeatedly retrying. Empty search results never prove absence.

If broad semantic closure cannot be established confidently with connector reads, use a checked-out/search-capable executor.

Read every modified existing file completely from the exact publication parent; never reconstruct from search output, partial ranges, truncated responses, stale revisions, or memory.

## Publication

Construct one complete off-ref candidate before moving a branch. Initial work parents the accepted base; corrections parent the exact previous feature head.

Before publication, verify publication-parent→candidate and accepted-base→candidate diffs against authorized scope.

Re-resolve refs immediately before publication. Create a new branch directly at the completed candidate. For corrections, require the feature branch to still equal the expected previous head, then use a non-force fast-forward. A mismatch or rejected update is a stop condition.

Do not claim compare-and-swap semantics unless the connector explicitly provides an expected-old-head guard. Never publish coherent multi-file work as sequential branch-visible file writes.

## Validation and handoff

Normal bounded path: complete candidate → draft PR → exact-head CI → assurance → guarded merge. Do not simulate local canonical validation when no local executor exists. Any feature-head change requires fresh CI and assurance.

Use a checked-out executor for compile-driven implementation, generated or formatter-owned state, large mechanical refactors, binary/LFS/submodule/file-mode-sensitive work, broad semantic repository analysis, required files that cannot be read completely, or repositories without suitable exact-head CI.
