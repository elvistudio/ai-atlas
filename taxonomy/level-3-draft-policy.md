# Level 3 Draft Policy

This policy defines how AI Atlas should treat early Level 3 taxonomy work.

Level 3 is not yet part of the public canonical taxonomy. Until explicitly reviewed and promoted, Level 3 material is draft/review work.

## Related architecture policies

Level 3 draft work should follow these public architecture documents:

- `taxonomy/architecture.md` — overall taxonomy architecture.
- `taxonomy/relations.md` — relation model and primary-parent / cross-link policy.
- `taxonomy/node-schema.md` — node fields, stable IDs, and validation-facing expectations.
- `taxonomy/naming-and-aliases.md` — canonical names, aliases, and naming exclusions.
- `taxonomy/status-and-lifecycle.md` — status lifecycle, stability, promotion, rejection, and deprecation.
- `taxonomy/concept-types.md` — concept type definitions and governance.

## Current status

Current public canonical taxonomy scope:

- Level 0 — Field
- Level 1 — Major Area
- Level 2 — Main Subarea

Current canonical source files:

- `taxonomy/ai-taxonomy-l1-l2.json`
- `taxonomy/ai-taxonomy-l1-l2.md`

Level 3 work must not destabilize Level 1 or Level 2.

## Purpose of Level 3

Level 3 should add deeper technical concepts under existing Level 2 nodes.

Good Level 3 candidates are usually stable, reusable concepts such as:

- methods,
- architectures,
- model families,
- system patterns,
- broad techniques when they are important enough to sit directly below a Level 2 area.

Level 3 should help readers understand how AI research areas, methods, architectures, and system patterns fit together.

It should not turn AI Atlas into a list of products, companies, temporary labels, or concrete model versions.

## Allowed Level 3 concept types

Allowed by default:

- Method
- Architecture
- Model Family
- System Pattern
- Technique, when broad and stable enough
- Component, when it is a major reusable system component
- Evaluation Concept, when placed under an evaluation-related parent
- Safety Concept, when placed under a safety/alignment parent

Allowed with caution:

- Application Area, only if it is genuinely a technical subarea below an existing Level 2 parent
- Future Concept, only inside future-facing branches and clearly marked

Not allowed at Level 3 by default:

- Product
- Company
- Concrete Model
- Concrete Model Version
- Temporary Marketing Label
- Vendor-Specific Feature

## Product and model-version rule

Do not add specific products, company names, commercial systems, or concrete model versions to Level 3.

They may be considered later at deeper levels only if AI Atlas explicitly decides to include concrete systems, products, or examples.

## Promotion criteria

A Level 3 candidate may be promoted only if:

- its name is stable and academically or technically recognizable,
- it is not a product, company, or concrete model version,
- it has a clear primary parent,
- its concept type is explicit,
- its short description is understandable,
- it does not duplicate an existing concept,
- known overlaps are documented,
- cross-links are proposed where needed,
- it can be represented without confusing the Level 1 and Level 2 structure.

## Rejection or deferral criteria

A candidate should be rejected or deferred if:

- it is mostly a product, company, vendor label, or product feature,
- it is a concrete model version,
- it is a temporary hype term,
- it belongs better at Level 4 or Level 5,
- it duplicates an existing concept,
- it has no stable parent,
- it would force a misleading hierarchy,
- it needs cross-link support before a primary parent can be chosen.

## Cross-link policy

Some Level 3 concepts naturally touch multiple branches.

For draft Level 3 work:

1. Choose one primary parent when possible.
2. Record alternative possible parents.
3. Record related concepts.
4. Do not duplicate the same concept under multiple parents unless explicitly justified.
5. If placement is unclear, keep the concept in draft review instead of forcing it into the tree.

Use `taxonomy/relations.md` for the full relation model.

## Generated views policy

Canonical public generated views should remain aligned with the current canonical taxonomy scope.

Until Level 3 is promoted:

- public Markmap and Obsidian views should remain Level 1–Level 2 only,
- draft Level 3 views, if generated, should live separately from canonical public views,
- draft Level 3 views must be clearly marked as draft,
- Obsidian draft Level 3 notes should not be mixed into the canonical Obsidian vault unless promotion is approved,
- README and project notes should make clear which views are canonical and which are draft.

After Level 3 promotion, generated views may include Level 3 only if they can represent the deeper hierarchy without confusing the stable Level 1–Level 2 structure.

## Validation expectations

Validators should distinguish canonical taxonomy files from draft taxonomy files.

Until Level 3 is promoted:

- canonical validation should continue to validate the current Level 0–Level 2 taxonomy,
- draft Level 3 files should not break canonical validation unless the validator is explicitly configured to validate drafts,
- draft Level 3 validation may run separately from canonical validation,
- draft validation errors should not imply that the public canonical taxonomy is invalid.

Use `taxonomy/node-schema.md` for general node schema and validation-facing expectations.

A future Level 3 validator should check at least:

- parent-child consistency,
- duplicate concept names within the same validation scope,
- required fields for each node,
- valid hierarchy level values,
- valid hierarchy level names,
- valid concept types,
- stable parent references,
- no product/company/concrete-model/version nodes at Level 3,
- documented overlap or cross-link notes for high-risk concepts.

Recommended required fields for a Level 3 draft node:

- `name`
- `hierarchy_level`
- `hierarchy_level_name`
- `concept_type`
- `parent`
- `children`
- `stability`
- `description`
- `overlap_notes` or equivalent review notes when cross-branch risk exists

Canonical Level 3 promotion should wait until validation can check Level 3 structure without weakening or confusing existing Level 1–Level 2 validation.

## Stability rule

Level 3 should prefer stable technical names.

Use `emerging` only when the concept is important but still settling.
Use `speculative` only inside future-facing branches or when the concept is explicitly not mature.

## Level 1 and Level 2 stability rule

Level 3 work must not casually rewrite Level 1 or Level 2.

If Level 3 work reveals a Level 1 or Level 2 issue, record it as a finding. Do not fix it inside a Level 3 draft unless the task explicitly includes Level 1/Level 2 cleanup and passes the appropriate review process.
