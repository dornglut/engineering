# Autonomous repository goal template

This is a maintained, executor-neutral invocation template for autonomous Dornglut repository work.

It does **not** authorize work or replace repository authority. Use it together with the current repository's `AGENTS.md`, accepted issues/decisions, roadmap where relevant, and Dornglut Engineering governance. More specific accepted authority wins.

## Reusable goal

```text
Work autonomously through <repository> from its current accepted authority and live repository state.

Start by reading the repository's AGENTS.md and required authority entrypoints, then applicable Dornglut Engineering governance. Re-resolve the default branch, active issues/PRs, dependencies, writers, reviews, validation state, relevant roadmap, and Portfolio priority where available before choosing or continuing work. Never treat stale session context, a previous “next step,” a handoff, an unmerged branch, or a roadmap item alone as implementation authority.

Derive the current work graph before executing:
- resume valid accepted in-flight work first;
- identify ready, blocked, deferred/revisit-gated, and successor-gated tracks;
- identify dependency order plus writer, validation, workflow, manifest/lockfile, public-contract, and other shared-authority conflicts;
- when no existing accepted issue is ready, determine from current accepted authority whether one bounded investigation or delivery is justified;
- treat the absence of a pre-existing issue as neither permission to invent work nor a reason to stop;
- when a material question is not decision-complete, route it to bounded investigation rather than inventing implementation;
- do not mass-create speculative future issues merely to mirror roadmap rows or backend feature lists.

When independent accepted tracks exist, do not serialize them merely because one track was selected first. If the executor supports subagents, workers, worktrees, or equivalent isolated execution, use parallel execution when it is safe and materially useful. A writing worker must have exactly one accepted owning issue, an explicit accepted base, one isolated branch/workspace/writer authority, a bounded write set, and independent validation/review/acceptance. Read-only investigation workers may share the same accepted revision.

Never give parallel workers overlapping mutable authority without an accepted serialization or staged-integration plan. Shared root manifests and lockfiles, protected workflows or validation authority, organization policy, dependency transitions, public-contract transitions, and overlapping source files remain serialized when Engineering or repository-local authority requires it. A worker result is evidence, not accepted repository state. Re-resolve the repository before consuming another worker's result, and never treat an unmerged worker branch as dependency authority.

For each bounded investigation or delivery, preserve repository-local ownership and architecture, follow its accepted issue/branch/PR discipline, and avoid compatibility layers, duplicate authorities, speculative abstractions, unrelated scope, or unapproved dependency/public-contract expansion.

After every meaningful state transition or worker completion, critically review and rederive the work graph. Re-resolve current state and verify that each remaining track is still necessary, correctly owned, architecturally sound, minimal, complete within its scope, and still correctly ordered. If previously independent tracks now overlap, serialize them from current accepted state rather than mechanically combining candidate branches.

When current accepted authority explicitly permits an investigation to establish one bounded successor, or otherwise already establishes a decision-complete bounded successor, create exactly the justified investigation/delivery issue and continue under the same standing authorization. Do not infer a new architecture/public-contract/ownership decision from an investigation that was not authorized to make that decision, and do not create a speculative successor inventory.

Before acceptance of any candidate:
- cold-review the complete accepted-base → candidate-head diff;
- verify authority and dependency closure;
- verify exact-head required validation/evidence;
- re-check default-branch drift, competing writers, reviews, unresolved threads, and mergeability;
- treat every candidate-head movement as invalidating earlier exact-head validation and review;
- report only evidence actually observed.

Use the repository's accepted merge method. Never infer new implementation, merge, or acceptance authority from stale context, a previous unrelated acceptance, a stale plan, or an unaccepted issue/roadmap item. A current accepted issue may authorize implementation within its bounded scope.

By invoking this goal as the repository owner or another authority permitted to grant merge/acceptance permission, I explicitly grant standing authorization for routine implementation, acceptance, merge, issue closure, required authority reconciliation, justified issue creation within current accepted authority, and continued work across the bounded autonomous sequence, provided every repository governance and exact-head gate still passes. Do not pause for repeated routine approval after each PR, issue, or roadmap slice.

Standing authorization does not cover a new architecture/public-contract/ownership decision not already accepted or explicitly delegated to an accepted investigation, material scope expansion beyond current authority, unresolved authority conflict, failed or unavailable required evidence, an unsafe/destructive action outside the accepted scope, or any boundary that current authority explicitly reserves for a separate human decision. At such a boundary, leave the affected candidate clean and evidence-complete and stop only that transition; continue other independent authorized tracks when safe.

After an accepted merge, reconcile only the durable authorities actually affected, re-resolve the repository, rederive the work graph, and continue with the next justified accepted or authority-permitted bounded item.

Do not stop merely because one investigation, issue, PR, worker, or merge completed, or because one track is blocked while another independent track is ready. Before declaring the repository idle, reconcile relevant remaining roadmap PLAN work, completed investigations with explicit successor gates, blockers and accepted unblock paths, DEFER/revisit gates and whether their conditions changed, qualification obligations, and material accepted dependency/standards changes.

Stop the overall autonomous sequence only when every remaining relevant track is either complete or currently unable to proceed because of a genuine blocker, unavailable required evidence/tooling, unresolved authority conflict, specifically non-delegated human decision, explicit defer/revisit gate, or lack of any justified bounded successor under current authority. A blocker on one track stops only that transition while independent authorized tracks remain ready.

Do not create generated handoff prompts, work-state ledgers, truth certificates, temporary process authority, or other parallel sources of truth unless accepted repository authority explicitly requires them.
```

Executor-specific procedures may add environment mechanics but must not weaken normative Engineering standards or repository-local authority. Parallel execution is optional when the executor lacks safe isolation and mandatory only to the extent current authority and executor capabilities make it both safe and materially useful. The standing grant is effective only when the person invoking the goal actually has the repository authority it claims; otherwise it grants nothing. For GPT Web + GitHub connector work, also use [the GPT Web GitHub procedure](gpt-web-github.md).
