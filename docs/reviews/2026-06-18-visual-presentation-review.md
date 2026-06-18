# Visual Presentation Review — Static Print Formats

Date: 2026-06-18

Scope: review the current static visual presentation brief and recommend the first printable prototype format.

This review does not modify taxonomy content, concept types, generated views, validation scripts, or Level 3 concepts.

## Sources reviewed

- `docs/visual-presentation-brief.md`
- `docs/review-agents/visual-map-print-designer.md`
- `docs/review-agents/documentation-community-editor.md`
- `docs/review-agents/john-senior-ai-reviewer.md`
- `taxonomy/visual-grammar.md`
- current Level 1-Level 2 taxonomy files

## Iris — Visual Map and Print Design Review

### Executive summary

- Overall static presentation readiness: proceed.
- Best first layout: modular grid.
- Best second layout: radial atlas.
- Biggest readability risk: trying to show too much in the first public poster.

### Format review

#### Essentials Poster

Good for public explanation, but it should not be the first internal design prototype. It requires editorial reduction and therefore risks hiding taxonomy issues too early.

#### Full L1-L2 Poster

Best first prototype. It uses the current canonical scope and can reveal real density, label length, grouping, and readability problems.

#### Review Wall Map

Useful after the Full L1-L2 prototype exists. It should include numbering and enough margin for critique.

### Layout review

#### Modular grid

Recommended first. It is the safest layout for print because each Level 1 area can become a panel with readable Level 2 entries. It supports review and avoids the geometry problems of radial layouts.

#### Radial atlas

Recommended second. It is stronger as a visual identity and public-facing map, but it needs careful label discipline and should be tested after the modular grid establishes content density.

#### Layered tree

Useful as a structural reference, but likely too outline-like for a public AI Atlas poster.

#### Subway-map style

Promising as a future experimental visual, but too risky for the first taxonomy poster because it may imply sequence, routes, or dependencies that are not part of the taxonomy.

### Iris recommendation

Proceed with a low-fidelity Full L1-L2 modular grid prototype first, then create a radial atlas prototype for comparison.

## Documentation and Community Editor Review

### Executive summary

The brief is clear and contributor-friendly. It explains audience, scope, candidate formats, and review questions well enough for the next prototype step.

### Communication risks

- The phrase “poster” may imply a polished public artifact too early.
- The distinction between “prototype”, “public preview”, and “review wall map” should remain explicit.
- The first prototype should be marked as internal / draft until reviewed.

### Recommendation

Proceed, but name the first output as a prototype, not a final poster.

## John Review

### Executive summary

The direction is correct. The first visual artifact should help expose taxonomy structure and readability issues, not hide them behind design polish.

### Main concern

The project should not move directly to a highly stylized public map before testing whether all Level 2 labels fit and whether the Level 1 grouping still reads cleanly.

### Recommendation

Use the modular grid as the first evidence-gathering prototype. Use the radial atlas later for identity and public presentation.

## Final recommendation

Proceed with this order:

1. Create a Full L1-L2 modular grid prototype.
2. Review it with Iris, Documentation and Community Editor, and John.
3. Create a radial atlas prototype from the same data.
4. Compare readability and density.
5. Choose the first public printable preview format.

## Suggested next implementation step

Create a generated prototype from the canonical taxonomy data:

- source: `taxonomy/ai-taxonomy-l1-l2.json`
- output: static SVG and PDF prototype
- layout: modular grid
- target size: A1 landscape first, then A0 if needed
- status label: Draft prototype / not final taxonomy poster
