# Repository lifecycle

## Create

A new repository requires:

- a named purpose and owning domain;
- explicit relationship to existing repositories;
- public or private visibility decision;
- default branch `main`;
- one read-only validation command;
- local README and `AGENTS.md`;
- ownership of issues, decisions, releases, and compatibility;
- no duplicate source authority.

Skeleton repositories may reserve a namespace, but they must not imply a completed extraction or public contract.

## Develop

Nontrivial work is issue-owned and based on the current accepted default branch. Pull requests remain bounded, validate exact heads, and document scope, non-scope, migration, and next action.

Repositories consume shared defaults and workflows without surrendering local validation semantics. A shared workflow may invoke a repository command; it must not recreate the repository's validation logic.

## Extract or transfer

Before moving a subsystem into a standalone repository:

1. correct the source boundary in the current owner;
2. transfer one accepted implementation authority;
3. prove standalone validation and downstream conformance;
4. migrate real consumers;
5. delete the old source and workspace authority;
6. prove no forwarding package, alias, include, branch dependency, submodule, or duplicate implementation remains;
7. close provenance and release policy.

## Archive

Archive only when active consumers, issues, releases, security obligations, and replacement authority are documented. Archived repositories are historical evidence, not active dependencies.
