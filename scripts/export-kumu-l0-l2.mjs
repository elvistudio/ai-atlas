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
  "kumu",
  "ai-atlas-v0.1-l0-l2-kumu.json",
);

const kumuPresentationByLevel = {
  0: {
    display_level: "Level 0",
    node_role: "Root",
    kumu_size: 48,
    kumu_color_group: "Root",
  },
  1: {
    display_level: "Level 1",
    node_role: "Major Area",
    kumu_size: 34,
    kumu_color_group: "Major Area",
  },
  2: {
    display_level: "Level 2",
    node_role: "Main Subarea",
    kumu_size: 18,
    kumu_color_group: "Main Subarea",
  },
};

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
    throw new Error("Kumu export must not contain concepts above Level 2.");
  }

  return concepts;
}

function toElement(concept) {
  const presentation = kumuPresentationByLevel[concept.hierarchy_level];

  if (!presentation) {
    throw new Error(
      `Unsupported hierarchy level ${concept.hierarchy_level} for "${concept.name}".`,
    );
  }

  return {
    id: concept.id,
    label: concept.name,
    name: concept.name,
    ...presentation,
    hierarchy_level: concept.hierarchy_level,
    hierarchy_level_name: concept.hierarchy_level_name,
    concept_type: concept.concept_type,
    stability: concept.stability,
    parent: concept.parent ?? null,
    description: concept.description,
  };
}

function toConnection(parent, child) {
  return {
    from: parent.id,
    to: child.id,
    label: "contains",
    type: "parent-child",
    direction: "directed",
  };
}

async function main() {
  const taxonomy = JSON.parse(await readFile(taxonomyPath, "utf8"));
  const root = taxonomy.level_0;
  const level1 = taxonomy.level_1;

  const concepts = validateCanonicalSource(root, level1);

  const elements = concepts.map(toElement);
  const connections = [
    ...level1.map((concept) => toConnection(root, concept)),
    ...level1.flatMap((parent) =>
      parent.level_2.map((child) => toConnection(parent, child)),
    ),
  ];

  const exportData = { elements, connections };

  await mkdir(path.dirname(outputPath), { recursive: true });
  await writeFile(outputPath, `${JSON.stringify(exportData, null, 2)}\n`);

  console.log(
    `Generated Kumu export: ${elements.length} elements, ${connections.length} connections.`,
  );
}

main().catch((error) => {
  console.error(`Kumu export failed: ${error.message}`);
  process.exitCode = 1;
});
