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

Exact-head validation evidence is a successful validation of the revision selected for that evidence stage. For a `pull_request` event, reviewed feature-head evidence selects `github.event.pull_request.head.sha`; for `merge_group`, queue-integration evidence selects `github.sha`; for `push` and `workflow_dispatch`, it selects `github.sha`. The workflow explicitly selects the expected revision for checkout and proves that `git rev-parse HEAD` equals the expected revision before any repository-owned canonical validation invocation runs.

A moved feature head invalidates earlier exact-head evidence. A workflow definition may be loaded from a pull-request merge ref while the reusable workflow explicitly checks out feature-head repository content. These are separate facts: the definition ref is not the validated repository revision.

Synthetic merge-result evidence validates GitHub's generated pull-request merge revision. It can be useful when intentionally requested, but it must be named merge-result evidence and must not be substituted for reviewed feature-head evidence. A merge-queue `merge_group` revision is a separate integration evidence stage, not this ordinary pull-request synthetic merge ref. Exact feature-head validation does not require duplicating the complete canonical suite against an ordinary synthetic pull-request merge result by default; queue-enabled repositories instead validate the required checks against the exact merge-group integration revision before the queue may merge it.

Feature-head, merge-group integration, and accepted-main validation are separate evidence stages. Do not assume SHA equality or inequality between the merge-group integration revision and the eventual accepted default-branch commit; a queue implementation may promote the already validated integration commit directly. An accepted squash merge is the immutable default-branch commit after acceptance and is not the reviewed feature head or an ordinary pull-request synthetic merge ref. Accepted-main push evidence independently proves the accepted default-branch state where `github.sha`, checkout ref, `git rev-parse HEAD`, and the accepted default-branch commit are equal.

Successful validation presents compact repository, event, revision, command, and conclusion evidence. Failed validation preserves command status, prints bounded diagnostics, retains a complete short-lived artifact, and removes temporary diagnostic state.

The authoring tool, local evidence, and model assessment do not replace independent CI. Local validation remains valuable preparation and should be reported honestly.

Agent-mediated publication and acceptance follow the [GitHub standard](github.md#agent-mediated-repository-changes). Executor-specific procedures may select exact-head CI when local execution is unavailable, but they do not redefine this validation contract.

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
