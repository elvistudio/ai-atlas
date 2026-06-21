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

function toElement(concept) {
  return {
    id: concept.id,
    label: concept.name,
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

  if (!root || !Array.isArray(level1)) {
    throw new Error("Canonical taxonomy must contain level_0 and level_1.");
  }

  const level2 = level1.flatMap((concept) => {
    if (!Array.isArray(concept.level_2)) {
      throw new Error(`Level 1 concept "${concept.name}" has no level_2 array.`);
    }

    return concept.level_2;
  });
  const concepts = [root, ...level1, ...level2];

  if (concepts.some((concept) => concept.hierarchy_level > 2)) {
    throw new Error("Kumu export must not contain concepts above Level 2.");
  }

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
