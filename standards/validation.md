# Validation standard

Every Dornglut repository owns the meaning of its canonical validation command.

Shared automation may invoke that command. It must not recreate or redefine the repository's validation semantics.

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

Merge evidence identifies the exact reviewed head and the successful workflow run or status attached to it.

A passing run on an earlier commit is not merge evidence for a moved head.

The authoring tool, local evidence, and model assessment do not replace independent CI. Local validation remains valuable preparation and should be reported honestly.

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

## Failure behavior

Validation fails closed when:

- required authority is absent;
- exact-head checks fail;
- a generated product is stale;
- a public contract or repository policy is inconsistent;
- a supersession or closure record is incomplete;
- active documentation points to retired or historical authority.

Failures are corrected in the owning repository through an ordinary pull request.
