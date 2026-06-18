# Print Poster Generation

Generate the draft Level 1-Level 2 modular-grid poster from the canonical JSON taxonomy:

```bash
python3 scripts/generate_print_poster.py
```

The default output is:

```text
build/print/ai-atlas-l1-l2-modular-grid.svg
```

The default page size is A1 landscape. Use `--size` to select another supported
size, or run the script with `--help` for all options.

To create a PDF, open the SVG in a browser or a vector editor such as Inkscape,
Illustrator, Affinity Designer, or Figma, then export or print it as PDF. Keep
the document dimensions unchanged to preserve the selected print size.

The generated poster is a draft prototype for review, not a final public AI
Atlas poster. Generated files under `build/` are intentionally not committed.

## Radial atlas prototype

Generate the experimental radial Level 1-Level 2 poster with:

```bash
python3 scripts/generate_radial_poster.py
```

The default A1 landscape output is:

```text
build/print/ai-atlas-l1-l2-radial-atlas.svg
```

Detailed mode is the default and includes all Level 1 and Level 2 concepts.
Overview mode shows the center and all Level 1 areas without Level 2 lists:

```bash
python3 scripts/generate_radial_poster.py --mode overview \
  --output build/print/ai-atlas-radial-overview.svg
```

The radial generator also supports A0 landscape and a large square format; run
it with `--help` for input, output, mode, and size options. These outputs are
draft visual-direction prototypes, not final public posters, and remain
uncommitted under `build/`.
