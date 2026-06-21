# Canonical L1/L2 JSON Model

Status: draft policy / under review / not canonical

Source issue: [#22 — Formalize canonical taxonomy JSON](https://github.com/ai-atlas-project/ai-atlas/issues/22)

Related issues:

- [#15 — Define stable ID convention for taxonomy nodes](https://github.com/ai-atlas-project/ai-atlas/issues/15)
- [#16 — Define relation target typing for structured taxonomy nodes](https://github.com/ai-atlas-project/ai-atlas/issues/16)
- [#21 — Define public Level 3 review and promotion process](https://github.com/ai-atlas-project/ai-atlas/issues/21)

## Canonical source

`taxonomy/ai-taxonomy-l1-l2.json` is the canonical machine-readable source for public Level 0, Level 1, and Level 2 taxonomy content.

Markdown and generated views should be derived from or checked against this JSON. They must not be treated as independent canonical sources when they conflict with the JSON.

Level 3 content is out of scope for this canonical JSON until the Level 3 review and promotion process is approved and a separate explicit promotion change is reviewed.

This policy documents the current model and validation expectations. It does not modify canonical taxonomy content, generated views, relations, or Level 3 drafts.

## Current document structure

The canonical JSON currently contains:

- project metadata;
- version and status metadata;
- hierarchy-level definitions;
- one `level_0` root concept;
- a `level_1` array;
- a nested `level_2` array on each Level 1 concept.

The nested arrays are storage containers for the primary hierarchy. Concept identity and meaning remain in each concept object's fields.

## Required concept fields

Canonical Level 0, Level 1, and Level 2 concepts are expected to contain:

- `id`
- `name`
- `hierarchy_level`
- `hierarchy_level_name`
- `concept_type`
- `parent`
- `children`
- `stability`
- `description`

`parent` is required for every non-root concept. The Level 0 root has no parent and may omit `parent` or use `null` if the schema is normalized later.

`children` is required and may be an empty array.

The current JSON uses readable canonical names in `parent` and `children` references. A future reviewed migration may use IDs, but validators must follow the representation actually approved for the canonical file.

Level 1 objects also contain a `level_2` storage array. This container is structural metadata for the current document layout, not a separate concept property shared by every node.

## ID expectations

- IDs must be unique across all public Level 0, Level 1, and Level 2 concepts.
- IDs should be stable once accepted.
- IDs should use the `ai:<slug>` style already present in the current JSON.
- IDs must not encode mutable hierarchy placement, hierarchy depth, or concept type.
- IDs must not be silently renamed or reused for a different concept.
- Any future ID rename, split, merge, or deprecation requires an approved alias, deprecation, or successor policy.
- Public ID acceptance is a prerequisite for upgrading relation targets from `canonical_pending_id` to `canonical`.

## Parent-child consistency

- Every child reference must resolve to an existing concept.
- Every non-root concept must have a parent reference that resolves to an existing concept.
- Parent and child references must agree bidirectionally.
- A concept listed in a parent's `children` array must identify that parent in its `parent` field.
- A non-root concept's parent must list that concept in `children`.
- Hierarchy level numbers must be consistent with parent-child depth.
- Level 0 is the root, Level 1 concepts are children of Level 0, and Level 2 concepts are children of Level 1 concepts.
- Level means hierarchy depth, not concept type.

## Validation expectations

A future or existing validator should check:

- JSON parses;
- all required fields exist, with the root-parent exception documented above;
- all IDs are unique;
- all IDs are well-formed;
- all parent references resolve;
- all child references resolve;
- parent-child links are bidirectionally consistent;
- hierarchy levels are consistent with depth;
- Level 1 `level_2` storage arrays agree with the parent-child hierarchy;
- no Level 3 concepts are present in the canonical L1/L2 JSON;
- relation target validators can use the canonical JSON as a public ID lookup table.

Validator output should distinguish errors that invalidate the canonical model from warnings about optional metadata or future migration work.

## Canonical ID lookup

Validation tooling should be able to build a lookup keyed by `id` from every Level 0, Level 1, and Level 2 concept in the canonical JSON.

The lookup should support:

- ID uniqueness checks;
- ID-to-name resolution;
- relation target resolution;
- verification that a referenced ID belongs to public canonical L0-L2 data rather than a private or transitional draft;
- future alias, deprecation, or successor handling after those metadata rules are approved.

This lookup is validation behavior, not a second canonical data source.

## Relation target dependency

The relation target typing policy depends on accepted public IDs from this JSON.

`canonical_pending_id` should not be upgraded to `canonical` until:

- canonical IDs are accepted;
- validators can resolve those IDs;
- the relation target meaning remains unchanged.

This policy does not migrate relation targets itself.

## Scope boundaries

- Do not add Level 3 concepts to this JSON through schema formalization work.
- Do not change taxonomy names, hierarchy placement, concept types, stability, descriptions, or meaning as part of validator planning.
- Do not update generated views unless a later explicit synchronization step authorizes it.
- Keep relation migration separate from canonical JSON formalization.
