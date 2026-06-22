# Experimental D3 relation view

This viewer explores alternative ways to project AI Atlas concepts using
curated technical-lineage, implementation-dependency, overlap, application,
and governance relations.

It is experimental visualization work. The canonical taxonomy remains:

`taxonomy/ai-taxonomy-l1-l2.json`

Technical lineage is not taxonomy hierarchy placement. In particular,
`Generative AI` remains a Level 1 Major Area in the canonical hierarchy even
when the relation projection displays a common technical lineage such as:

`Artificial Intelligence → Machine Learning → Deep Learning → Generative AI`

The relations in `technical-lineage.json` are exploratory. They should
eventually be reviewed under a governed relation policy before any relation is
treated as canonical project data.

## Views

- **Canonical hierarchy** displays the existing Level 0–2 parent/child tree
  from the canonical JSON.
- **Technical lineage** displays only curated relations tagged for the
  `technical_lineage` view.
- **Cross-cutting overlaps** displays only curated relations tagged for the
  `cross_links` view.

Every non-hierarchy edge exposes its relation type and optional note on hover.
A persistent banner distinguishes these projections from canonical placement.

## Run locally

The page uses D3.js from a CDN and reads:

- `../../taxonomy/ai-taxonomy-l1-l2.json`
- `technical-lineage.json`

For the most reliable browser behavior, serve the repository root:

```sh
python3 -m http.server 8000
```

Then open:

`http://localhost:8000/experiments/d3-relation-view/`

When `index.html` is opened directly with a `file://` URL and browser security
blocks local JSON requests, the page provides file pickers for loading the same
canonical taxonomy and relation overlay manually.

This viewer exists to show useful alternative perspectives without changing
the canonical tree, concept types, IDs, meanings, or Level 3 promotion status.
