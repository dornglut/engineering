# Licensing standard

This standard implements the repository licensing classes established by ADR 0007. It governs current repository representation and migration mechanics; it does not replace the license texts or any separately executed commercial agreement.

## License classes

### Network and service products

Public open-source license: `AGPL-3.0-only`.

A separate commercial license may be offered by copyright holder(s) with sufficient rights to grant it.

Current repositories:

- `dornglut/runen-online`;
- `dornglut/werkstatt`.

### Product libraries, SDKs, engines, and toolchains

Public open-source license: `GPL-3.0-only`.

A separate commercial license may be offered by copyright holder(s) with sufficient rights to grant it.

Current repositories:

- `dornglut/runen`;
- `dornglut/runenwerk`;
- `dornglut/runen-ui`;
- `dornglut/runen-sdf`;
- `dornglut/runen-spatial`;
- `dornglut/runen-net`.

Planned `runen-gpu`, `runen-render`, and `runen-ecs` use this class unless a later accepted organization decision changes the classification.

`dornglut/runen-lab` uses `GPL-3.0-only` without a promised commercial alternative.

### Organization governance and shared infrastructure

License: `Apache-2.0`.

Current repositories:

- `dornglut/.github`;
- `dornglut/engineering`;
- `dornglut/github-workflows`.

## Required repository representation

A maintained repository must make its current license unambiguous.

### Dual-licensed product repository

Required:

- `LICENSE` containing the complete applicable GPLv3 or AGPLv3 text;
- `LICENSING.md` describing the public open-source path and the availability of a separate commercial agreement;
- README license section linking to both files;
- package metadata using only the public SPDX identifier, such as `GPL-3.0-only` or `AGPL-3.0-only`;
- validation that rejects stale active MIT/Apache product-license claims after migration.

A separate commercial agreement is not an SPDX license. Do not use values such as `GPL-3.0-only OR Commercial`, `AGPL-3.0-only OR Commercial`, `Commercial`, or another invented identifier in Cargo/package SPDX metadata.

`LICENSING.md` must not invent customer pricing, warranties, indemnities, SLAs, patent grants beyond the selected public license, or other commercial contract terms. It may state that separate commercial terms are available from copyright holder(s) authorized to grant them.

### GPL-only showcase repository

Required:

- `LICENSE` containing GPLv3;
- README license section;
- package metadata `GPL-3.0-only` where applicable.

A commercial alternative is not advertised unless separately authorized.

### Apache infrastructure repository

Required:

- `LICENSE` containing Apache License 2.0;
- README license section;
- package metadata `Apache-2.0` where applicable.

Add `NOTICE` only when required by incorporated material or an accepted repository need; do not create an empty notice file for symmetry.

## Historical licenses

License changes are prospective.

A migration repository must state in `LICENSING.md` or another canonical license note that revisions published before the licensing-policy migration remain available under the licenses granted on those revisions. Current files must not claim that previously granted MIT, Apache-2.0, or dual-permissive rights were revoked.

Old license files may be removed from the current branch when they no longer license the current revision. Git history preserves the prior grant and its exact text. A repository may retain an explicitly historical license record only when it cannot be mistaken for a current alternative license.

Third-party dependencies and incorporated third-party source retain their own licenses. A Dornglut repository license change must not relabel third-party material.

## Commercial licensing authority

A repository may advertise a separate commercial license only when copyright holder(s) with sufficient rights can grant the required proprietary terms for the covered code.

Repository membership, GitHub organization ownership, or maintainer status does not by itself establish legal ownership of every copyright interest. Commercial agreements must be executed by the party or parties actually authorized to grant them.

Commercial license text, pricing, customer-specific rights, warranties, indemnities, support obligations, and similar terms are outside this engineering standard and require separate legal/business review.

## Contributions

Commercial dual licensing requires relicensing authority over accepted code.

Until a reviewed inbound contribution mechanism is established, repositories in the AGPL-plus-commercial and GPL-plus-commercial classes:

- must use `owner-only` or `discussion` contribution classification for code;
- must not merge external code pull requests;
- may accept issue reports, design discussion, reviews, reproducible cases, and other non-code participation according to local policy;
- must not rely on an implicit assumption that a GitHub pull request automatically grants commercial relicensing rights.

A future CLA, copyright assignment, or other inbound license must be separately reviewed and accepted before it becomes required workflow.

## Migration procedure

Each repository migration is separately issue-owned and begins from accepted `main`.

The bounded migration should, as applicable:

1. inventory the current license files, package metadata, README claims, contribution policy, and provenance constraints;
2. confirm that the migration does not relabel third-party material;
3. replace the current public license file with the assigned class license;
4. add `LICENSING.md` for commercial dual-licensed products;
5. remove stale current-branch license alternatives that no longer apply;
6. update README and package metadata;
7. update repository validation to enforce the intended current license representation when the repository already validates licensing;
8. reconcile contribution classification and local contribution guidance;
9. run the repository's canonical validation on the exact feature head;
10. record the accepted migration revision when closing the owning issue.

Do not combine unrelated product behavior, API, dependency, or architecture changes into a licensing migration.

## New repositories

Repository creation must select the license class from ADR 0007 before accepting substantive implementation.

If a proposed repository does not fit an existing class, resolve the classification through Engineering before publication rather than choosing a local exception silently.
