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

## Partitioned hosted execution

When measured hosted-validation latency justifies the additional orchestration, a
repository may expose bounded partitions of its canonical validation command for
parallel execution. Partitioning changes execution placement; it must not create a
second validation authority or weaken the complete canonical baseline.

The complete canonical invocation remains authoritative and must run every required
check without GitHub-specific state or partition orchestration. A partitioned interface
is an additional execution projection of that same repository-owned validation plan.

A repository that exposes partitions owns:

- the bounded partition inventory and stable partition identifiers;
- the assignment of every required validation obligation to those partitions;
- the fixed discovery and single-partition invocation contract;
- proof that the complete set of partitions is semantically equivalent to the complete
  canonical invocation.

When discovery or inventory is a checked-in projection of the authoritative validation
plan, the complete canonical invocation and every single-partition invocation must
validate that projection against the authoritative partition inventory before any
partition-specific work executes. This proof must not live only in one ordinary
partition, because stale or modified discovery data could omit that partition itself.
Inventory mismatch fails closed before partition-specific validation.

Partitioning must not silently change package selection, feature resolution, generated
state requirements, test semantics, policy coverage, or another validation invariant
merely to improve scheduling. Shared automation must not infer semantic lanes, decide
which repository checks may be omitted, or copy repository-specific commands into
workflow YAML.

A reusable workflow may discover a repository-owned partition inventory and execute the
fixed repository-owned partition entrypoint only when it:

- strictly validates the discovered data as bounded identifiers before using it for
  orchestration;
- accepts no repository-produced shell fragment, script, runner, toolchain, working
  directory, path, secret, or arbitrary command as execution policy;
- checks out and proves the same exact expected revision independently for every
  partition;
- does not require one partition's mutable workspace or build artifacts for another
  partition's correctness;
- collects independent partition failures without treating cancellation or omission as
  success;
- reports one stable aggregate validation result that succeeds only when discovery and
  every required partition succeed.

Partition job identities are supporting evidence, not separate semantic authorities.
The aggregate result remains the ordinary canonical hosted merge-readiness check unless
the owning repository explicitly requires additional independent evidence for another
reason.

No organization-wide partition count or semantic lane vocabulary is defined. A
repository may expose one partition, several partitions, or no partitioned interface.
Changing shared orchestration to support partitions is compatibility-significant:
existing immutable workflow revisions retain their historical behavior and each caller
adopts a newer accepted revision explicitly.

## Exact-head evidence

An accepted base is the accepted default-branch revision from which pull-request work was prepared and reviewed. A reviewed feature head is the exact branch commit that contains the proposed change.

Exact-head validation evidence is a successful validation of the revision selected for that evidence stage. For a `pull_request` event, reviewed feature-head evidence selects `github.event.pull_request.head.sha`; for `merge_group`, queue-integration evidence selects `github.sha`; for `push` and `workflow_dispatch`, it selects `github.sha`. The workflow explicitly selects the expected revision for checkout and proves that `git rev-parse HEAD` equals the expected revision before any invocation of the repository-owned canonical command runs.

A moved feature head invalidates earlier exact-head evidence. The opt-in documentation projection below may establish new exact-head evidence using an independently verified full run for identical executable inputs; it does not relabel the earlier run as validation of the new head. A workflow definition may be loaded from a pull-request merge ref while the reusable workflow explicitly checks out feature-head repository content. These are separate facts: the definition ref is not the validated repository revision.

Synthetic merge-result evidence validates GitHub's generated pull-request merge revision. It can be useful when intentionally requested, but it must be named merge-result evidence and must not be substituted for reviewed feature-head evidence. A merge-queue `merge_group` revision is a separate integration evidence stage, not this ordinary pull-request synthetic merge ref. Exact feature-head validation does not require duplicating the complete canonical suite against an ordinary synthetic pull-request merge result by default; queue-enabled repositories instead validate the required checks against the exact merge-group integration revision before the queue may merge it.

Feature-head, merge-group integration, and accepted-main validation are separate evidence stages. Do not assume SHA equality or inequality between the merge-group integration revision and the eventual accepted default-branch commit; a queue implementation may promote the already validated integration commit directly. An accepted squash merge is the immutable default-branch commit after acceptance and is not the reviewed feature head or an ordinary pull-request synthetic merge ref. Accepted-main push evidence independently proves the accepted default-branch state where `github.sha`, checkout ref, `git rev-parse HEAD`, and the accepted default-branch commit are equal.

Successful validation presents compact repository, event, revision, command, and conclusion evidence. Failed validation preserves command status, prints bounded diagnostics, retains a complete short-lived artifact, and removes temporary diagnostic state.

The authoring tool, local evidence, and model assessment do not replace independent CI. Local validation remains valuable preparation and should be reported honestly.

Agent-mediated publication and acceptance follow the [GitHub standard](github.md#agent-mediated-repository-changes). Executor-specific procedures may select exact-head CI when local execution is unavailable, but they do not redefine this validation contract.

## Change-aware documentation validation

The complete local command remains authoritative and runs every required check.
A Rust repository may opt in to a hosted documentation projection only after an
accepted caller change establishes an audited documentation boundary. The
repository owns the classification policy and fixed lightweight invocation
`cargo validate --docs`; the complete and lightweight invocations share the
same documentation and repository-policy checks. Full validation also validates
the policy structure and required documentation files.

Two opt-in policies are supported; select exactly one.

- **Explicit inventory:** the existing `validation-docs.txt` lists individual
  regular Markdown paths, not globs or executable content. Only content
  changes to existing listed regular files are eligible; additions, removals,
  renames and mode/type changes run full.
- **Documentation namespaces:** a regular root `validation-docs-policy.txt`
  containing exactly `markdown-namespaces-v1` and a final LF selects a fixed
  classification of regular, non-executable Markdown files directly at the
  repository root or under `docs/`. Use bounded, unambiguous ASCII path
  components; reject traversal, hidden components, ambiguous names, symlinks,
  executable files, submodules and non-Markdown content as eligible changes.
  The explicit inventory must be absent. Additions, removals and renames wholly
  within the eligible namespace may use the documentation projection; there
  is no per-document manifest to update. Renames are evaluated as removal
  and addition, and a move across the boundary changes non-documentation
  inputs. Mode/type changes never qualify.

Before adopting either policy, prove that accepted executable inputs do not
depend on the excluded documentation. For namespace mode, the proof must also
cover absence, presence, names and inventory of documents, including future
additions: build scripts, compilation inputs, tests, generated products,
packaging and runtime discovery must not consume or enumerate eligible
documents in a way that changes executable behavior. Repository-policy checks
may inspect documentation and its inventory when they run equivalently in
both validation modes. A filename extension, existing tree audit alone, or
successful full run is not proof of this namespace invariant. Review the
boundary whenever executable dependencies, file discovery or validation policy
change; revoke namespace eligibility through a full-validated policy change
if the invariant cannot be preserved. Repositories unable to establish the
stronger boundary retain the explicit inventory or full validation.

Selective hosted validation is permitted only when all of these hold:

- the exact expected feature or push revision is checked out and proved;
- the classification policy and caller workflow are byte-identical to the
  accepted default-branch policy (for a default-branch push, use the previous
  accepted revision), and the mutually exclusive policy selection is unchanged;
- the trusted classifier checks complete tracked inventories, including paths,
  modes and object identities, using the accepted policy, never candidate
  classification code. The comparison covers the union of paths in each pair
  of trees; every difference must satisfy the selected documentation policy.
  Non-eligible paths must match exactly. For namespace mode, every present side
  of a changed eligible leaf must be a regular non-executable Markdown blob;
  directory/file collisions or uncertain inventories select full validation;
- a successful full run is independently verified through GitHub Actions
  metadata, including repository, workflow path, pinned reusable revision,
  exact source revision, full-validation job and successful aggregate;
- all non-documentation inputs match both the accepted default-branch revision
  and that full-run revision, including classification policy and caller, and
  at least one eligible document differs from each;
- current exact-head documentation/policy validation succeeds, including
  required-document presence, link integrity and the selected policy checks.
  A documentation-only deletion cannot remove a required authority document
  or leave invalid links.

A docs-only run cannot establish reusable executable evidence. No workspace
artifacts or test binaries are carried between revisions. The evidence record
identifies the current revision and the verified full-run revision and run ID.
No classification decision may be made from a path filter, commit message,
user-supplied run ID, untrusted head classifier or unverified check label.

Uncertain, missing, truncated or inaccessible evidence selects full validation.
Manual dispatch, merge-group integration, policy/allowlist changes, unsupported
partition layouts and unsupported events receive the complete baseline. The
first adoption or migration between policies requires complete validation;
older workflow pins remain unchanged. Keep one stable required aggregate;
skipped or failed selected work must not report success. The reusable workflow
may implement this fixed, opt-in evidence projection, not repository-specific
semantic inference.

Before adopting namespace mode, qualify the actual hosted selector and
repository validator with ordinary additions, deletions and renames, rejected
required-document/link violations, executable or policy changes, mode/type
changes, unavailable evidence and unsuccessful selected work. Existing
inventory-mode behavior must remain compatible.

The projection remains restricted to a complete unpartitioned Rust baseline
and accepted executable inputs. A mixed code/documentation PR must run full
validation even after an earlier green code checkpoint: unmerged code may
introduce a new dependency on an excluded document. Reusing such evidence
requires a separate trusted dependency-boundary proof, not simply equal code
hashes between two feature revisions. Expand only with separate equivalence
proof.

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
