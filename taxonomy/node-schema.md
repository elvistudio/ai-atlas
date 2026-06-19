# Node Schema

This document defines the standard shape of an AI Atlas node for current and future taxonomy work.

It does not require an immediate migration of the existing canonical JSON. It defines the target structure for future reviewed work, validators, and eventual schema cleanup.

## Core principle

A node has both:

1. hierarchy information — where it sits in the primary tree,
2. concept information — what kind of concept it is.

Hierarchy level and concept type must remain separate.

## Stable node IDs

Each canonical node should eventually have a stable machine-readable `id`.

The `id` is not the same as the display `name`.

A display name may be improved for readability. A stable ID should not change for minor wording, capitalization, punctuation, or naming cleanup.

### ID format

Recommended format:

```text
ai.<scope>.<slug>
```

Rules:

- lowercase only,
- ASCII letters, numbers, dots, and underscores,
- no spaces,
- stable across minor display-name changes,
- not vendor-specific unless concrete products are explicitly in scope at a later level.

Suggested scopes:

- `field` — root field,
- `area` — Level 1 major or cross-cutting area,
- `subarea` — Level 2 main subarea,
- `method` — method,
- `architecture` — architecture,
- `model_family` — model family,
- `technique` — technique,
- `component` — system/model component,
- `system_pattern` — recurring system pattern,
- `safety` — safety/alignment concept,
- `evaluation` — evaluation concept,
- `governance` — governance concept,
- `future` — future-facing or speculative concept.

Examples:

```text
ai.field.artificial_intelligence
ai.area.machine_learning
ai.subarea.supervised_learning
ai.architecture.transformers
```

The future `Transformers` example is illustrative only. It is not a promoted Level 3 node.

### Renaming and deprecation

If a display name changes but the concept stays the same, keep the same `id`.

If a concept is split, merged, or replaced, preserve the old ID as deprecated rather than silently reusing it for a different meaning.

## Required fields

Recommended required fields for future canonical nodes:

```json
{
  "id": "ai.area.machine_learning",
  "name": "Machine Learning",
  "hierarchy_level": 1,
  "hierarchy_level_name": "Major Area",
  "concept_type": "Major Area",
  "primary_parent": "ai.field.artificial_intelligence",
  "children": [],
  "stability": "stable",
  "status": "stable",
  "description": "A short human-readable description."
}
```

Required field definitions:

- `id` — stable machine-readable identifier.
- `name` — canonical display name.
- `hierarchy_level` — numeric depth in the primary hierarchy.
- `hierarchy_level_name` — human-readable hierarchy level label.
- `concept_type` — type of concept, as defined in `concept-types.md`.
- `primary_parent` — stable ID of the main parent; root node may use `null`.
- `children` — list of child node IDs or names, depending on migration stage.
- `stability` — maturity of the concept name or category.
- `status` — lifecycle state in AI Atlas.
- `description` — short explanation for readers and reviewers.

## Optional fields

Recommended optional fields:

- `aliases` — alternative names, acronyms, or spelling variants.
- `relations` — typed non-tree relationships defined in `relations.md`.
- `review_notes` — reviewer-facing notes.
- `overlap_notes` — notes for cross-branch placement risk.
- `source_notes` — notes about evidence or rationale.
- `deprecated_by` — replacement node ID if deprecated.
- `replaces` — older node ID or name replaced by this node.
- `draft_only` — boolean marker for draft files.

## Relations field

A future node may represent relations like this:

```json
{
  "relations": [
    {
      "type": "alternative-parent",
      "target": "ai.area.foundation_models_and_general_purpose_ai",
      "note": "Plausible placement during draft review."
    }
  ]
}
```

Relation types must come from `relations.md`.

## Aliases field

Aliases should be stored as strings unless a future validator needs richer metadata.

```json
{
  "aliases": ["LLMs", "Language Foundation Models"]
}
```

Aliases do not create separate nodes.

## Level 1 example

```json
{
  "id": "ai.area.machine_learning",
  "name": "Machine Learning",
  "aliases": [],
  "hierarchy_level": 1,
  "hierarchy_level_name": "Major Area",
  "concept_type": "Major Area",
  "primary_parent": "ai.field.artificial_intelligence",
  "children": [
    "ai.subarea.supervised_learning",
    "ai.subarea.unsupervised_learning"
  ],
  "relations": [],
  "stability": "stable",
  "status": "stable",
  "description": "AI systems that learn patterns from data rather than relying only on hand-written rules."
}
```

## Level 2 example

```json
{
  "id": "ai.subarea.supervised_learning",
  "name": "Supervised Learning",
  "aliases": [],
  "hierarchy_level": 2,
  "hierarchy_level_name": "Main Subarea",
  "concept_type": "Paradigm",
  "primary_parent": "ai.area.machine_learning",
  "children": [],
  "relations": [],
  "stability": "stable",
  "status": "stable",
  "description": "A learning paradigm where models learn from labeled examples."
}
```

## Future Level 3 draft example

This example is illustrative only. It is not a promoted Level 3 taxonomy node.

```json
{
  "id": "ai.architecture.transformers",
  "name": "Transformers",
  "aliases": ["Transformer Architecture"],
  "hierarchy_level": 3,
  "hierarchy_level_name": "Method, Architecture, or Model Family",
  "concept_type": "Architecture",
  "primary_parent": "ai.subarea.deep_learning",
  "children": [],
  "relations": [
    {
      "type": "alternative-parent",
      "target": "ai.area.foundation_models_and_general_purpose_ai",
      "note": "Important for foundation models, but primary technical identity is architectural."
    }
  ],
  "stability": "stable",
  "status": "draft",
  "description": "A neural network architecture based on attention mechanisms.",
  "overlap_notes": "Cross-links may be needed to NLP, vision, multimodal, and foundation model branches."
}
```

## Validation expectations

Canonical validation and draft validation should remain separate.

Current canonical validation should continue to validate the Level 0–Level 2 taxonomy without requiring draft Level 3 files.

Future validators should be able to detect:

- missing IDs,
- duplicate IDs,
- invalid concept types,
- invalid relation types,
- alias duplication,
- invalid status values,
- missing primary parents outside the root node,
- references to missing target nodes,
- product/company/concrete-model/version nodes at disallowed levels.

No validator implementation is required by this document.
