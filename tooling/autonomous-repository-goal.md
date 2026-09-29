# Autonomous repository goal template

This is a maintained, executor-neutral invocation template for autonomous Dornglut repository work.

It does **not** authorize work or replace repository authority. Use it together with the current repository's `AGENTS.md`, accepted issues/decisions, roadmap where relevant, and Dornglut Engineering governance. More specific accepted authority wins.

## Reusable goal

```text
Work autonomously through <repository> from its current accepted authority and live repository state.

Start by reading the repository's AGENTS.md and required authority entrypoints, then applicable Dornglut Engineering governance. Re-resolve the default branch, active issues/PRs, dependencies, writers, reviews, validation state, and relevant roadmap before choosing or continuing work. Never treat stale session context, a previous “next step,” a handoff, or a roadmap item alone as implementation authority.

Continue actual work while justified:
- resume valid accepted in-flight work first;
- otherwise select the correct accepted and actionable work from current authority, dependencies, roadmap sequencing, and Portfolio priority where relevant;
- when a material question is not decision-complete, route it to bounded investigation rather than inventing implementation;
- when no further accepted actionable work is justified, stop and report that state.

For each bounded delivery, preserve repository-local ownership and architecture, follow its accepted issue/branch/PR discipline, and avoid compatibility layers, duplicate authorities, speculative abstractions, unrelated scope, or unapproved dependency/public-contract expansion.

After every meaningful state transition, critically review before continuing. Re-resolve current state and verify that the work remains necessary, correctly owned, architecturally sound, minimal, complete, within accepted scope, and still the correct next action. Do not continue mechanically from an earlier plan.

Before acceptance:
- cold-review the complete accepted-base → candidate-head diff;
- verify authority and dependency closure;
- verify exact-head required validation/evidence;
- re-check default-branch drift, competing writers, reviews, unresolved threads, and mergeability;
- treat every candidate-head movement as invalidating earlier exact-head validation and review;
- report only evidence actually observed.

Use the repository's accepted merge method. Never infer new implementation, merge, or acceptance authority from general autonomy, a previous acceptance, a stale plan, or an unaccepted issue/roadmap item. A current accepted issue may authorize implementation within its bounded scope. When repository authority requires explicit human/owner acceptance, leave the candidate clean, frozen, evidence-complete, and acceptance-ready.

After an accepted merge, reconcile only the durable authorities actually affected, re-resolve the repository, critically reassess work selection, and continue with the next justified accepted item.

Do not stop merely because one investigation, issue, PR, or merge completed. Stop only when current authority establishes a genuine blocker, unavailable required evidence/tooling, an authority conflict, a required human acceptance boundary, or no further justified accepted work.

Do not create generated handoff prompts, work-state ledgers, truth certificates, temporary process authority, or other parallel sources of truth unless accepted repository authority explicitly requires them.
```

Executor-specific procedures may add environment mechanics but must not weaken normative Engineering standards or repository-local authority. This template itself is not a source of authorization. For GPT Web + GitHub connector work, also use [the GPT Web GitHub procedure](gpt-web-github.md).
