#!/usr/bin/env python3
"""Validate AI Atlas Level 1-Level 2 taxonomy consistency.

This script intentionally uses only the Python standard library so it can run
in GitHub Actions without installing project dependencies.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAXONOMY_MD = ROOT / "taxonomy" / "ai-taxonomy-l1-l2.md"
TAXONOMY_JSON = ROOT / "taxonomy" / "ai-taxonomy-l1-l2.json"
MARKMAP = ROOT / "markmap" / "ai-atlas-markmap.md"
MERMAID_MD = ROOT / "mermaid" / "ai-atlas-mindmap.md"
MERMAID_MMD = ROOT / "mermaid" / "ai-atlas-mindmap.mmd"
OBSIDIAN_ROOT = ROOT / "obsidian" / "AI Atlas Vault"
OBSIDIAN_L1 = OBSIDIAN_ROOT / "Level 1"
OBSIDIAN_L2 = OBSIDIAN_ROOT / "Level 2"


def read(path: Path) -> str:
    if not path.exists():
        raise AssertionError(f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def parse_markdown_taxonomy(text: str) -> list[dict[str, object]]:
    if "## Level 1 and Level 2" not in text:
        raise AssertionError("Markdown taxonomy is missing '## Level 1 and Level 2'.")

    section = text.split("## Level 1 and Level 2", 1)[1]
    branches: list[dict[str, object]] = []
    current: dict[str, object] | None = None

    for line in section.splitlines():
        heading = re.match(r"^###\s+\d+\.\s+(.+?)\s*$", line)
        if heading:
            current = {"name": heading.group(1), "children": []}
            branches.append(current)
            continue

        bullet = re.match(r"^-\s+(.+?)\s*$", line)
        if bullet and current is not None:
            children = current["children"]
            assert isinstance(children, list)
            children.append(bullet.group(1))

    if not branches:
        raise AssertionError("No Level 1 branches found in Markdown taxonomy.")

    return branches


def concept_names_from_json(data: dict[str, object]) -> tuple[list[str], dict[str, list[str]]]:
    level_1 = data.get("level_1")
    if not isinstance(level_1, list):
        raise AssertionError("JSON taxonomy must contain a level_1 list.")

    names: list[str] = []
    children_by_parent: dict[str, list[str]] = {}

    for node in level_1:
        if not isinstance(node, dict):
            raise AssertionError("Each level_1 item must be an object.")
        name = node.get("name")
        children = node.get("children")
        level_2 = node.get("level_2")
        if not isinstance(name, str):
            raise AssertionError("Each level_1 item must have a string name.")
        if not isinstance(children, list) or not all(isinstance(x, str) for x in children):
            raise AssertionError(f"Level 1 node {name!r} must have string children.")
        if not isinstance(level_2, list):
            raise AssertionError(f"Level 1 node {name!r} must have a level_2 list.")

        level_2_names = []
        for child in level_2:
            if not isinstance(child, dict):
                raise AssertionError(f"Level 2 item under {name!r} must be an object.")
            child_name = child.get("name")
            parent = child.get("parent")
            if not isinstance(child_name, str):
                raise AssertionError(f"Level 2 item under {name!r} must have a string name.")
            if parent != name:
                raise AssertionError(
                    f"Level 2 item {child_name!r} has parent {parent!r}, expected {name!r}."
                )
            level_2_names.append(child_name)

        if children != level_2_names:
            raise AssertionError(
                f"Level 1 node {name!r} has children that do not match its level_2 names.\n"
                f"children={children}\nlevel_2={level_2_names}"
            )

        names.append(name)
        children_by_parent[name] = list(children)

    return names, children_by_parent


def validate_markdown_matches_json(md_branches: list[dict[str, object]], data: dict[str, object]) -> None:
    json_l1_names, json_children = concept_names_from_json(data)
    md_l1_names = [str(branch["name"]) for branch in md_branches]

    if md_l1_names != json_l1_names:
        raise AssertionError(
            "Level 1 order/names differ between Markdown and JSON.\n"
            f"Markdown: {md_l1_names}\nJSON: {json_l1_names}"
        )

    root = data.get("level_0")
    if not isinstance(root, dict):
        raise AssertionError("JSON taxonomy must contain a level_0 object.")
    root_children = root.get("children")
    if root_children != json_l1_names:
        raise AssertionError(
            "JSON level_0 children must match level_1 names.\n"
            f"level_0.children={root_children}\nlevel_1={json_l1_names}"
        )

    for branch in md_branches:
        name = str(branch["name"])
        children = branch["children"]
        assert isinstance(children, list)
        if children != json_children[name]:
            raise AssertionError(
                f"Level 2 children differ for {name!r}.\n"
                f"Markdown: {children}\nJSON: {json_children[name]}"
            )


def all_concepts(children_by_parent: dict[str, list[str]]) -> list[str]:
    concepts: list[str] = []
    for parent, children in children_by_parent.items():
        concepts.append(parent)
        concepts.extend(children)
    return concepts


def validate_no_duplicate_level2(children_by_parent: dict[str, list[str]]) -> None:
    seen: dict[str, str] = {}
    duplicates: list[str] = []
    for parent, children in children_by_parent.items():
        for child in children:
            if child in seen:
                duplicates.append(f"{child!r} under both {seen[child]!r} and {parent!r}")
            else:
                seen[child] = parent
    if duplicates:
        raise AssertionError("Duplicate Level 2 names found: " + "; ".join(duplicates))


def validate_generated_views(concepts: list[str]) -> None:
    generated_files = [MARKMAP, MERMAID_MD, MERMAID_MMD]
    for path in generated_files:
        text = read(path)
        for concept in concepts:
            if concept not in text:
                raise AssertionError(f"{path.relative_to(ROOT)} is missing concept {concept!r}.")


def validate_obsidian(children_by_parent: dict[str, list[str]]) -> None:
    root_text = read(OBSIDIAN_ROOT / "00 Artificial Intelligence.md")

    expected_l1 = set(children_by_parent)
    actual_l1 = {p.stem for p in OBSIDIAN_L1.glob("*.md")}
    if actual_l1 != expected_l1:
        raise AssertionError(
            "Obsidian Level 1 pages do not match taxonomy.\n"
            f"Missing: {sorted(expected_l1 - actual_l1)}\n"
            f"Extra: {sorted(actual_l1 - expected_l1)}"
        )

    expected_l2 = {child for children in children_by_parent.values() for child in children}
    actual_l2 = {p.stem for p in OBSIDIAN_L2.glob("*.md")}
    if actual_l2 != expected_l2:
        raise AssertionError(
            "Obsidian Level 2 pages do not match taxonomy.\n"
            f"Missing: {sorted(expected_l2 - actual_l2)}\n"
            f"Extra: {sorted(actual_l2 - expected_l2)}"
        )

    for parent, children in children_by_parent.items():
        if f"Level 1/{parent}" not in root_text:
            raise AssertionError(f"Obsidian root page is missing Level 1 link for {parent!r}.")

        parent_text = read(OBSIDIAN_L1 / f"{parent}.md")
        for child in children:
            if f"Level 2/{child}" not in parent_text:
                raise AssertionError(
                    f"Obsidian Level 1 page {parent!r} is missing child link {child!r}."
                )

            child_text = read(OBSIDIAN_L2 / f"{child}.md")
            if f"Level 1/{parent}" not in child_text:
                raise AssertionError(
                    f"Obsidian Level 2 page {child!r} is missing parent link {parent!r}."
                )


def validate_no_obsolete_pages() -> None:
    obsolete_exact_page_stems = {
        "Foundation and General-Purpose Models",
        "Multi-Agent Systems",
        "Classical Control",
        "Code Models",
        "Generative Model Families",
        "Human Feedback",
        "Evaluation and Benchmarking",
    }
    actual_stems = {p.stem for p in OBSIDIAN_L1.glob("*.md")} | {p.stem for p in OBSIDIAN_L2.glob("*.md")}
    leftover = obsolete_exact_page_stems & actual_stems
    if leftover:
        raise AssertionError(f"Obsolete Obsidian pages still exist: {sorted(leftover)}")


def main() -> int:
    errors: list[str] = []
    try:
        data = json.loads(read(TAXONOMY_JSON))
        md_branches = parse_markdown_taxonomy(read(TAXONOMY_MD))
        validate_markdown_matches_json(md_branches, data)
        _, children_by_parent = concept_names_from_json(data)
        validate_no_duplicate_level2(children_by_parent)
        concepts = all_concepts(children_by_parent)
        validate_generated_views(concepts)
        validate_obsidian(children_by_parent)
        validate_no_obsolete_pages()
    except Exception as exc:  # noqa: BLE001 - display all validation failures clearly in CI.
        errors.append(str(exc))

    if errors:
        print("AI Atlas taxonomy validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print("AI Atlas taxonomy validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
