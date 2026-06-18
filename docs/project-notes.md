# Project Notes

## Current direction

AI Atlas starts as a clean hierarchy of modern AI.

The first goal is not to create the deepest possible map.

The first goal is to create a stable Level 1 and Level 2 model that can be reviewed by colleagues.

## Important design decisions

- Transformers are not Level 1.
- Deep Learning is under Machine Learning.
- Reinforcement Learning is under Machine Learning.
- Continual Learning is under Machine Learning.
- Large Language Models are under Foundation Models and General-Purpose AI.
- Autonomous Agents are under Agentic and Multi-Agent Systems, not only under future AI.
- Generative AI remains Level 1 because it is a major cross-cutting modern AI category.
- AI Safety, Alignment and Governance remains Level 1 because it cuts across the whole field.

## Expert cleanup before Level 3

Before expanding to Level 3, the Level 1–Level 2 taxonomy was reviewed and cleaned up.

Applied cleanup decisions:

- `Multi-Agent Systems` was renamed to `Agentic and Multi-Agent Systems`.
- `Foundation and General-Purpose Models` was renamed to `Foundation Models and General-Purpose AI`.
- `Autonomous Agents` was moved from `AGI and Future AI` to `Agentic and Multi-Agent Systems`.
- `Continual Learning` was moved from `AGI and Future AI` to `Machine Learning`.
- `Knowledge Representation` remains canonical under `Knowledge and Reasoning`.
- `Symbolic Knowledge Representation` is used under `Symbolic AI` to avoid an exact duplicate.
- `Text Generation` remains under `Generative AI`.
- `Natural Language Generation` is used under `Natural Language and Speech` to avoid an exact duplicate.
- `Representation Learning` and `Data-Centric AI` were added under `Machine Learning`.
- `AI UX and Trust` was renamed to `AI User Experience and Trust`.
- Level 2 hierarchy terminology was clarified from `Subfield` to `Main Subarea`.
- Several names were clarified before Level 3 expansion.

## Typed knowledge map

We decided to separate hierarchy depth from concept type.

This means:

- depth describes where a concept sits in the tree,
- type describes what kind of concept it is.

This prepares the project for future Level 3, Level 4, and visual formats such as posters, Markmap, Mermaid, Obsidian, and a possible website.

## Roadmap

### v0.1 — Clean Level 1–Level 2 taxonomy

Create the initial clean hierarchy:

- Level 0 — Field
- Level 1 — Major Areas
- Level 2 — Main Subareas

### v0.2 — Typed concept model and visual grammar

Add metadata and visual structure:

- hierarchy level names,
- concept types,
- stability metadata,
- visual grammar,
- mixed licensing model.

### v0.3 — Level 3 encyclopedia draft

Add Level 3 concepts for understanding and exploration.

This should be treated as an encyclopedia draft, not the final canonical taxonomy.

### v0.4 — Validation and generated views

Add validation and synchronization tools:

- JSON schema,
- taxonomy validation script,
- generated Markmap,
- generated Mermaid,
- generated Obsidian vault updates.

### v0.5 — Website or public preview

Create a public-facing version of AI Atlas.

Possible outputs:

- static website,
- interactive graph,
- public documentation,
- early visual preview.

### v1.0 — Stable public AI Atlas

Publish a stable public version suitable for broader review and use.

This version should have:

- reviewed taxonomy,
- clear licensing,
- contribution process,
- validation workflow,
- public presentation format.
