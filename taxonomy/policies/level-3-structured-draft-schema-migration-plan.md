# Level 3 Structured Draft Schema Migration Plan

Status: draft migration plan / under review / not canonical

Source issue: [#18 — Normalize structured draft schema for Level 3 nodes](https://github.com/ai-atlas-project/ai-atlas/issues/18)

Related issues:

- [#15 — Define stable ID convention for taxonomy nodes](https://github.com/ai-atlas-project/ai-atlas/issues/15)
- [#16 — Define relation target typing for structured taxonomy nodes](https://github.com/ai-atlas-project/ai-atlas/issues/16)
- [#17 — Define cross-branch file placement policy for Level 3 drafts](https://github.com/ai-atlas-project/ai-atlas/issues/17)
- [#21 — Define public Level 3 review and promotion process](https://github.com/ai-atlas-project/ai-atlas/issues/21)
- [#22 — Formalize canonical taxonomy JSON](https://github.com/ai-atlas-project/ai-atlas/issues/22)

## Purpose

Define a safe migration sequence for private Level 3 structured draft files after schema, stable-ID, relation-target, and package/standalone policies have been clarified.

## Scope

This is policy and migration planning only.

- No public canonical taxonomy changes.
- No generated view changes.
- No private structured JSON migration in this PR.
- No Level 3 promotion.

## Current state

Private Level 3 work includes:

- standalone single-node draft files;
- branch package/context files;
- a private index and navigation layer;
- public non-canonical draft proposals.

These artifacts serve different review purposes. A migration must preserve those roles and must not treat parallel private representations as independent canonical sources.

## Migration order

1. Inventory private Level 3 structured files.
2. Classify each file as a standalone node, branch package/context artifact, review note, or index.
3. Validate required schema fields against [`level-3-structured-draft-schema.md`](level-3-structured-draft-schema.md).
4. Validate IDs as provisional/private or canonical public references.
5. Validate relation targets against [`relation-target-typing.md`](relation-target-typing.md).
6. Preserve package files as context unless a separate package migration review approves synchronization, archival, or removal.
7. Run small pilot migrations before broad changes.
8. Use Codex or local validation for multi-file JSON edits.
9. Update public issues with migration results.
10. Keep Level 3 non-canonical until the [Level 3 review and promotion process](level-3-review-and-promotion-process.md) in #21 is approved.

## Validation checklist

- JSON parses.
- Required file-level fields are present.
- Required node-level fields are present.
- `draft_only: true`.
- `canonical_promotion_status: not promoted`.
- `promotion_blockers` is present.
- `id` is present and clearly provisional or accepted.
- `primary_parent` and `primary_parent_name` are present.
- Relation targets use the approved typed pattern or are explicitly provisional.
- No generated views changed.
- No canonical taxonomy meaning changed.

## Stop conditions

Stop and require a separate focused review before:

- broad multi-file migration;
- deleting or restructuring package files;
- changing concept type;
- changing hierarchy placement;
- changing relation meaning;
- public Level 3 promotion;
- generating or updating public Level 3 views.
