# ADR 0007: Establish organization-wide product licensing classes

- Status: accepted
- Date: 2026-08-24
- Owner: Dornglut organization
- Scope: Repository licensing and commercial licensing policy

## Context

Dornglut repositories currently use inconsistent licensing. Some product repositories are MIT-licensed, some use `MIT OR Apache-2.0`, and newer repositories do not yet expose an explicit product license. That inconsistency was acceptable during early extraction and bootstrap work but is not a sound long-term basis for a commercial open-source product family.

Dornglut intends to keep source-visible, genuinely open-source paths while preserving a separate paid licensing path for proprietary product use where the copyright holder has sufficient rights to grant one. Network/service products also need a license that addresses modified software offered primarily over a network.

The organization must distinguish the public open-source license from any separately negotiated commercial agreement. A commercial agreement is not an SPDX license and must not be encoded as though it were one in Cargo or other standardized package metadata.

Existing permissions already granted under MIT, Apache-2.0, or another license on historical revisions are not revoked by adopting a different license prospectively.

Commercial relicensing also requires sufficient rights over contributed code. Accepting external code under terms that do not preserve the necessary relicensing rights could prevent a complete dual-licensed product from being offered commercially.

## Decision

Dornglut establishes three repository license classes.

### Network and service products

Products whose normal deployment includes hosted, remotely interactive, or service-side execution use:

> `AGPL-3.0-only` as the public open-source license, with a separate commercial license available from copyright holder(s) that have sufficient rights to grant it.

Initial repositories:

- `dornglut/runen-online`;
- `dornglut/werkstatt`.

The AGPL path remains a commercial-use-capable open-source path. The separate commercial agreement exists for customers that require rights different from the AGPL terms.

### Product libraries, SDKs, engines, and toolchains

Reusable product code whose ordinary commercial use is primarily through incorporation, linking, distribution, or delivery with another product uses:

> `GPL-3.0-only` as the public open-source license, with a separate commercial license available from copyright holder(s) that have sufficient rights to grant it.

Initial repositories:

- `dornglut/runen`;
- `dornglut/runenwerk`;
- `dornglut/runen-ui`;
- `dornglut/runen-sdf`;
- `dornglut/runen-spatial`;
- `dornglut/runen-net`.

Planned `dornglut/runen-gpu`, `dornglut/runen-render`, and `dornglut/runen-ecs` inherit this class when created unless a later accepted organization decision assigns a different class.

`dornglut/runen-lab` uses `GPL-3.0-only` without promising a separate commercial license. It is a downstream showcase and experimental application collection rather than a commercial framework authority.

### Organization governance and shared infrastructure

Repositories whose purpose is organization policy, community defaults, or reusable CI orchestration use `Apache-2.0`:

- `dornglut/.github`;
- `dornglut/engineering`;
- `dornglut/github-workflows`.

These repositories are intended to be reusable organization infrastructure rather than commercial product capture points.

### Repository representation

The canonical mechanics are defined by `standards/licensing.md`.

For a dual-licensed product repository:

- the standard SPDX/package metadata declares only the public open-source license (`GPL-3.0-only` or `AGPL-3.0-only`);
- `LICENSE` contains the corresponding public license text;
- `LICENSING.md` explains that a separate commercial license may be obtained from copyright holder(s) with sufficient rights;
- a private commercial agreement is not represented as an SPDX expression and is not invented in repository source;
- README and package metadata must not imply that historical permissive grants were revoked.

### Historical grants

This decision is prospective. A repository migration changes the license for the code as published from that migration revision onward, subject to copyright ownership and any third-party code obligations.

Historical revisions remain available under the licenses granted on those revisions. Removing an old license file from the current branch does not revoke rights previously granted.

### Contributions and relicensing authority

A dual-licensed repository must not merge external code contributions under inbound terms that prevent the copyright holder(s) from granting the complete product under the commercial licensing path.

Until a reviewed inbound licensing mechanism is adopted, dual-licensed product repositories must use `owner-only` or `discussion` contribution policy for code and decline external code pull requests. Issue reports, design discussion, review, and other non-code participation may remain open according to repository policy.

This ADR does not draft a CLA, copyright assignment, commercial EULA, pricing schedule, or customer contract. Those instruments require separate review before use.

## Consequences

- Dornglut gains a coherent public-open-source plus commercial-license strategy for products that are intended to support paid proprietary use.
- RunenOnline and Werkstatt receive a network-aware copyleft default suitable for service-side deployment.
- Runen libraries, SDKs, Runenwerk, and the Runen compiler/toolchain receive one consistent strong-copyleft public default with a separately negotiable proprietary path.
- Governance and shared CI remain low-friction reusable infrastructure.
- Historical MIT and Apache-2.0 versions remain usable under their original grants.
- A fork may continue from a previously permissive historical revision; future Dornglut development is not required to remain permissively licensed because of that history.
- Package metadata remains valid SPDX rather than inventing a pseudo-license identifier for a private contract.
- Contributor policy becomes a prerequisite to accepting external code in commercial dual-licensed products.
- Repository-specific migrations remain separately reviewable and must pass each repository's canonical validation.

## Alternatives considered

### Keep MIT or Apache-2.0 for product repositories

Rejected for the commercial product classes. Permissive licenses allow proprietary incorporation and redistribution without creating a requirement to obtain separate proprietary rights, which does not match the intended commercial licensing model.

### Make all Dornglut repositories AGPL-3.0-only

Rejected. Network-interaction copyleft is appropriate for service products but unnecessarily broad as the organization-wide default for SDKs, engines, compiler/toolchains, governance, and CI infrastructure.

### Make all product repositories commercial-only or source-available

Rejected. Dornglut intends to retain a genuine open-source path and the adoption, inspectability, self-hosting, and community benefits that follow from it.

### Use `GPL-3.0-or-later` or `AGPL-3.0-or-later`

Rejected. Dornglut deliberately selects the version-3-only forms so later GNU license versions do not automatically become alternative terms for current Dornglut code.

### Put `GPL-3.0-only OR Commercial` in Cargo metadata

Rejected. `Commercial` is not an SPDX license identifier. The public license belongs in standardized metadata; the separate commercial path belongs in `LICENSING.md` and the separately executed agreement.

### Draft a Dornglut-specific commercial license and CLA in this ADR

Rejected. Those are legal instruments with consequences beyond repository architecture and require separate professional review before use.

## Affected repositories

- `dornglut/.github`
- `dornglut/engineering`
- `dornglut/github-workflows`
- `dornglut/runen`
- `dornglut/runenwerk`
- `dornglut/runen-lab`
- `dornglut/runen-ui`
- `dornglut/runen-sdf`
- `dornglut/runen-spatial`
- `dornglut/runen-net`
- `dornglut/runen-online`
- `dornglut/werkstatt`
- planned `dornglut/runen-gpu`
- planned `dornglut/runen-render`
- planned `dornglut/runen-ecs`

## Adoption or migration

1. Accept this ADR and `standards/licensing.md` in Engineering.
2. Migrate `runen-online`, `runen-net`, and `runen` before further release/public-surface progression because their current licensing is either commercially inconsistent or absent.
3. Migrate the remaining existing product repositories through repository-owned issues and pull requests, preserving exact historical-license statements and canonical validation.
4. Migrate `.github`, `engineering`, and `github-workflows` to Apache-2.0 without changing their non-product authority.
5. Reconcile README license sections, license files, Cargo/package metadata, validation, and repository contribution classification for every affected repository.
6. Do not accept external code into dual-licensed products until reviewed inbound contribution terms preserve the intended commercial relicensing path.
7. Establish a reviewed commercial licensing agreement and inbound contribution mechanism before selling proprietary rights or accepting external code that would require those instruments.

No product semantic, API, package-topology, or runtime behavior change is authorized by this ADR.

## Supersedes

None.

## Superseded by

None.
