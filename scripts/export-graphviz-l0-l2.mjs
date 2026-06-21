#!/usr/bin/env node

import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const repositoryRoot = path.resolve(scriptDirectory, "..");
const taxonomyPath = path.join(
  repositoryRoot,
  "taxonomy",
  "ai-taxonomy-l1-l2.json",
);
const outputPath = path.join(
  repositoryRoot,
  "exports",
  "graphviz",
  "ai-atlas-v0.1-l0-l2.dot",
);

const nodeStyleByLevel = {
  0: {
    fillcolor: "#0F766E",
    color: "#115E59",
    fontcolor: "#FFFFFF",
    fontsize: "20",
    penwidth: "2.5",
    margin: "0.20,0.14",
  },
  1: {
    fillcolor: "#CCFBF1",
    color: "#0F766E",
    fontcolor: "#134E4A",
    fontsize: "14",
    penwidth: "1.8",
    margin: "0.16,0.10",
  },
  2: {
    fillcolor: "#F0FDFA",
    color: "#5EEAD4",
    fontcolor: "#134E4A",
    fontsize: "10",
    penwidth: "1.0",
    margin: "0.12,0.08",
  },
};

function escapeDotString(value) {
  return String(value)
    .replaceAll("\\", "\\\\")
    .replaceAll('"', '\\"')
    .replaceAll("\r", "\\r")
    .replaceAll("\n", "\\n");
}

function quoteDotString(value) {
  return `"${escapeDotString(value)}"`;
}

function formatAttributes(attributes) {
  return Object.entries(attributes)
    .map(([key, value]) => `${key}=${quoteDotString(value)}`)
    .join(", ");
}

function validateCanonicalSource(root, level1) {
  if (!root || root.hierarchy_level !== 0 || !Array.isArray(level1)) {
    throw new Error(
      "Canonical taxonomy must contain a Level 0 root and a level_1 array.",
    );
  }

  const level2 = [];
  const expectedRootChildren = [];

  for (const parent of level1) {
    if (
      parent.hierarchy_level !== 1 ||
      parent.parent !== root.name ||
      !Array.isArray(parent.level_2)
    ) {
      throw new Error(
        `Invalid Level 1 hierarchy for "${parent.name ?? "unnamed concept"}".`,
      );
    }

    expectedRootChildren.push(parent.name);
    const expectedLevel2Children = [];

    for (const child of parent.level_2) {
      if (child.hierarchy_level !== 2 || child.parent !== parent.name) {
        throw new Error(
          `Invalid Level 2 hierarchy for "${child.name ?? "unnamed concept"}".`,
        );
      }

      expectedLevel2Children.push(child.name);
      level2.push(child);
    }

    if (
      JSON.stringify(parent.children) !==
      JSON.stringify(expectedLevel2Children)
    ) {
      throw new Error(
        `Level 1 children do not match level_2 entries for "${parent.name}".`,
      );
    }
  }

  if (JSON.stringify(root.children) !== JSON.stringify(expectedRootChildren)) {
    throw new Error("Level 0 children do not match level_1 entries.");
  }

  const concepts = [root, ...level1, ...level2];
  const ids = concepts.map((concept) => concept.id);

  if (
    ids.some((id) => typeof id !== "string" || id.length === 0) ||
    new Set(ids).size !== ids.length
  ) {
    throw new Error("Canonical concepts must have unique, non-empty IDs.");
  }

  if (concepts.some((concept) => concept.hierarchy_level > 2)) {
    throw new Error("Graphviz export must not contain concepts above Level 2.");
  }

  return concepts;
}

function toNodeStatement(concept) {
  const levelStyle = nodeStyleByLevel[concept.hierarchy_level];

  if (!levelStyle) {
    throw new Error(
      `Unsupported hierarchy level ${concept.hierarchy_level} for "${concept.name}".`,
    );
  }

  const attributes = {
    label: concept.name,
    ...levelStyle,
  };

  return `  ${quoteDotString(concept.id)} [${formatAttributes(attributes)}];`;
}

function toEdgeStatement(parent, child) {
  return `  ${quoteDotString(parent.id)} -> ${quoteDotString(child.id)};`;
}

async function main() {
  const taxonomy = JSON.parse(await readFile(taxonomyPath, "utf8"));
  const root = taxonomy.level_0;
  const level1 = taxonomy.level_1;
  const concepts = validateCanonicalSource(root, level1);
  const edges = [
    ...level1.map((concept) => [root, concept]),
    ...level1.flatMap((parent) =>
      parent.level_2.map((child) => [parent, child]),
    ),
  ];

  const lines = [
    "digraph AIAtlas {",
    '  graph [rankdir="LR", splines="true", overlap="false", nodesep="0.35", ranksep="1.10", pad="0.20", bgcolor="#FFFFFF"];',
    '  node [shape="box", style="rounded,filled", fontname="Helvetica"];',
    '  edge [color="#94A3B8", penwidth="1.0", arrowsize="0.7"];',
    "",
    "  // Canonical Level 0-2 nodes",
    ...concepts.map(toNodeStatement),
    "",
    "  // Directed parent-child edges",
    ...edges.map(([parent, child]) => toEdgeStatement(parent, child)),
    "}",
    "",
  ];

  await mkdir(path.dirname(outputPath), { recursive: true });
  await writeFile(outputPath, lines.join("\n"));

  console.log(
    `Generated Graphviz export: ${concepts.length} nodes, ${edges.length} edges.`,
  );
}

main().catch((error) => {
  console.error(`Graphviz export failed: ${error.message}`);
  process.exitCode = 1;
});
