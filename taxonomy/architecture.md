# Taxonomy Architecture

AI Atlas is a public taxonomy and typed knowledge map of modern Artificial Intelligence.

It uses two complementary structures:

1. A primary navigational hierarchy.
2. A typed concept graph.

The hierarchy helps readers browse the field. The concept graph helps represent cross-cutting concepts, aliases, relationships, status, and future validation without forcing every concept into a single clean subtree.

## Current canonical scope

The current public canonical taxonomy remains:

- Level 0 — Field
- Level 1 — Major Area
- Level 2 — Main Subarea

Level 3 is draft/review work until explicitly promoted.

## Hierarchy level vs concept type

Hierarchy level and concept type are separate properties.

A hierarchy level says where a node appears in the tree.

A concept type says what kind of concept the node is.

For example:

- `Machine Learning` is a Level 1 node and a `Major Area`.
- `Deep Learning` is a Level 2 node and a `Subfield`.
- A future draft `Transformers` node might be a Level 3 node and an `Architecture`.

The same hierarchy level may contain different concept types when that makes the taxonomy more accurate and readable.

## Primary hierarchy

The primary hierarchy should answer the reader's first navigation question:

> Where should I look first for this concept?

A canonical node should normally have one primary parent. This keeps the public taxonomy readable and avoids duplicate branches.

## Concept graph

The concept graph records additional structure that a strict tree cannot represent well.

Supporting documents:

- `relations.md` defines graph relations and cross-links.
- `node-schema.md` defines node fields, stable IDs, and validation-facing structure.
- `naming-and-aliases.md` defines canonical names, aliases, synonyms, acronyms, and naming exclusions.
- `status-and-lifecycle.md` defines concept status, stability, promotion, rejection, and deprecation.
- `concept-types.md` defines concept types and governance rules.

## Draft vs canonical

Draft material can be useful for exploration, review, and branch planning.

Canonical public taxonomy should contain only reviewed and intentionally promoted content.

Draft Level 3 work must not destabilize Level 1 or Level 2. If Level 3 work reveals a Level 1 or Level 2 issue, record it as a review finding rather than silently changing the canonical taxonomy.

## What should not be forced into the hierarchy

Some concepts are cross-cutting. Some are better represented as relations. Some are too immature, product-specific, or vendor-specific to be canonical taxonomy nodes.

Do not force a concept into the hierarchy only because it is popular or useful. If placement is unclear, keep it in draft review until the concept has a defensible primary parent, concept type, and status.
