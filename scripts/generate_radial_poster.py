#!/usr/bin/env python3
"""Generate a draft radial AI Atlas poster as SVG.

The generator uses only the Python standard library and reads the canonical
Level 1-Level 2 taxonomy JSON. The layout is an experimental radial atlas:
Level 0 sits at the center, Level 1 areas form the inner ring, and detailed
mode groups Level 2 concepts into horizontal mini-lists inside their sectors.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import textwrap
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "taxonomy" / "ai-taxonomy-l1-l2.json"
DEFAULT_OUTPUT = ROOT / "build" / "print" / "ai-atlas-l1-l2-radial-atlas.svg"

SIZES_MM = {
    "A1_LANDSCAPE": (841, 594),
    "A0_LANDSCAPE": (1189, 841),
    "SQUARE_LARGE": (841, 841),
}

SECTOR_COLORS = [
    "#E8F2FF",
    "#EAF7EA",
    "#FFF3DF",
    "#F4ECFF",
    "#E9F7F7",
    "#FFF0F0",
    "#EEF0FF",
    "#F8F8E8",
    "#EAF1F6",
    "#F1F5EA",
    "#F7EEF5",
    "#EFF6F0",
    "#F3F3F3",
]

SECTOR_STROKES = [
    "#3978B8",
    "#3E8750",
    "#B87820",
    "#7952A8",
    "#33858A",
    "#B85B5B",
    "#596CB8",
    "#8A8734",
    "#4D7892",
    "#71854C",
    "#985C87",
    "#4B805A",
    "#666666",
]


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def load_taxonomy(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as source:
        data = json.load(source)

    if not isinstance(data, dict):
        raise ValueError("Taxonomy JSON must be an object.")
    if not isinstance(data.get("level_0"), dict):
        raise ValueError("Taxonomy JSON must contain a level_0 object.")
    if not isinstance(data.get("level_1"), list):
        raise ValueError("Taxonomy JSON must contain a level_1 list.")
    return data


def point(cx: float, cy: float, rx: float, ry: float, angle: float) -> tuple[float, float]:
    radians = math.radians(angle)
    return cx + rx * math.cos(radians), cy + ry * math.sin(radians)


def wrap_label(label: str, width: int, max_lines: int) -> list[str]:
    lines = textwrap.wrap(
        label,
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    ) or [label]
    if len(lines) <= max_lines:
        return lines
    kept = lines[:max_lines]
    kept[-1] = kept[-1].rstrip(".,;:") + "…"
    return kept


def text_element(
    x: float,
    y: float,
    lines: list[str],
    *,
    size: float,
    weight: int = 400,
    fill: str = "#151515",
    anchor: str = "middle",
    rotation: float | None = None,
    line_gap: float = 1.18,
) -> str:
    transform = ""
    if rotation is not None:
        transform = f' transform="rotate({rotation:.2f} {x:.2f} {y:.2f})"'
    tspans = []
    first_y = y - (len(lines) - 1) * size * line_gap / 2
    for index, line in enumerate(lines):
        dy = 0 if index == 0 else size * line_gap
        tspans.append(
            f'<tspan x="{x:.2f}" dy="{dy:.2f}">{esc(line)}</tspan>'
        )
    return (
        f'<text x="{x:.2f}" y="{first_y:.2f}" font-size="{size:.2f}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{transform}>'
        + "".join(tspans)
        + "</text>"
    )


def sector_path(
    cx: float,
    cy: float,
    inner_rx: float,
    inner_ry: float,
    outer_rx: float,
    outer_ry: float,
    start_angle: float,
    end_angle: float,
) -> str:
    outer_start = point(cx, cy, outer_rx, outer_ry, start_angle)
    outer_end = point(cx, cy, outer_rx, outer_ry, end_angle)
    inner_end = point(cx, cy, inner_rx, inner_ry, end_angle)
    inner_start = point(cx, cy, inner_rx, inner_ry, start_angle)
    large_arc = 1 if end_angle - start_angle > 180 else 0
    return (
        f"M {outer_start[0]:.2f},{outer_start[1]:.2f} "
        f"A {outer_rx:.2f},{outer_ry:.2f} 0 {large_arc} 1 {outer_end[0]:.2f},{outer_end[1]:.2f} "
        f"L {inner_end[0]:.2f},{inner_end[1]:.2f} "
        f"A {inner_rx:.2f},{inner_ry:.2f} 0 {large_arc} 0 {inner_start[0]:.2f},{inner_start[1]:.2f} Z"
    )


def draw_sector_card(
    branch: dict[str, Any],
    *,
    cx: float,
    cy: float,
    angle: float,
    radius_x: float,
    radius_y: float,
    fill: str,
    accent: str,
    scale: float,
    mode: str,
) -> str:
    name = str(branch.get("name", "Untitled"))
    nodes = branch.get("level_2", [])
    if not isinstance(nodes, list):
        nodes = []

    x, y = point(cx, cy, radius_x, radius_y, angle)
    if mode == "overview":
        card_width = 78 * scale
        title_lines = wrap_label(name, width=26, max_lines=3)
        card_height = max(24, 10 + len(title_lines) * 4.3) * scale
        return (
            f'<g data-level="1" data-name="{esc(name)}">'
            f'<rect x="{x - card_width / 2:.2f}" y="{y - card_height / 2:.2f}" '
            f'width="{card_width:.2f}" height="{card_height:.2f}" rx="{5 * scale:.2f}" '
            f'fill="{fill}" stroke="{accent}" stroke-width="{1.15 * scale:.2f}" />'
            + text_element(
                x,
                y,
                title_lines,
                size=3.7 * scale,
                weight=750,
            )
            + "</g>"
        )

    card_width = 110 * scale
    card_height = 62 * scale
    card_x = x - card_width / 2
    card_y = y - card_height / 2
    padding = 4.2 * scale
    title_lines = wrap_label(name, width=31, max_lines=2)
    title_size = 3.25 * scale
    title_line_height = title_size * 1.16
    title_block_height = max(8.5 * scale, len(title_lines) * title_line_height)
    divider_y = card_y + padding + title_block_height + 1.5 * scale
    list_top = divider_y + 4.0 * scale
    column_gap = 3.0 * scale
    column_width = (card_width - 2 * padding - column_gap) / 2
    rows = math.ceil(len(nodes) / 2)
    row_height = 5.15 * scale

    parts = [
        f'<g data-level="1" data-name="{esc(name)}">',
        f'<rect x="{card_x:.2f}" y="{card_y:.2f}" width="{card_width:.2f}" '
        f'height="{card_height:.2f}" rx="{4.5 * scale:.2f}" fill="#FFFFFF" '
        f'fill-opacity="0.94" stroke="{accent}" stroke-width="{0.9 * scale:.2f}" />',
        f'<rect x="{card_x:.2f}" y="{card_y:.2f}" width="{card_width:.2f}" '
        f'height="{(divider_y - card_y):.2f}" rx="{4.5 * scale:.2f}" fill="{fill}" />',
        text_element(
            x,
            card_y + padding + title_block_height / 2,
            title_lines,
            size=title_size,
            weight=750,
        ),
        f'<line x1="{card_x + padding:.2f}" y1="{divider_y:.2f}" '
        f'x2="{card_x + card_width - padding:.2f}" y2="{divider_y:.2f}" '
        f'stroke="{accent}" stroke-width="{0.45 * scale:.2f}" />',
    ]

    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            continue
        column = index // rows
        row = index % rows
        item_name = str(node.get("name", "Untitled"))
        item_x = card_x + padding + column * (column_width + column_gap)
        item_y = list_top + row * row_height
        item_size = (2.12 if len(item_name) > 31 else 2.35) * scale
        parts.append(
            f'<g data-level="2" data-name="{esc(item_name)}">'
            f'<circle cx="{item_x + 0.8 * scale:.2f}" cy="{item_y - 0.7 * scale:.2f}" '
            f'r="{0.62 * scale:.2f}" fill="{accent}" />'
            + text_element(
                item_x + 2.6 * scale,
                item_y,
                [item_name],
                size=item_size,
                weight=500,
                anchor="start",
            )
            + "</g>"
        )

    parts.append("</g>")
    return "\n".join(parts)


def generate_svg(data: dict[str, Any], *, size_name: str, mode: str) -> str:
    width, height = SIZES_MM[size_name]
    level_0 = data["level_0"]
    branches = data["level_1"]
    if not branches:
        raise ValueError("Taxonomy has no Level 1 areas.")

    scale = min(width / 841, height / 594)
    margin = 18 * scale
    cx = width / 2
    cy = height / 2 + 10 * scale
    outer_rx = width * 0.445
    outer_ry = height * 0.405
    # The first prototype used 31% of the atlas radius for the center. Reducing
    # that to 21.5% frees roughly 31% of the former center footprint for labels.
    sector_inner_rx = outer_rx * 0.215
    sector_inner_ry = outer_ry * 0.215
    card_radius_factor = 0.70 if mode == "detailed" else 0.59
    card_radius_x = outer_rx * card_radius_factor
    card_radius_y = outer_ry * card_radius_factor

    project = str(data.get("project", "AI Atlas"))
    root_name = str(level_0.get("name", "Artificial Intelligence"))
    version = str(data.get("version", ""))
    count = len(branches)
    sector_span = 360 / count
    start_offset = -90 - sector_span / 2

    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}mm" height="{height}mm" viewBox="0 0 {width} {height}">',
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#FFFFFF" />',
        '<style>text { font-family: Inter, Arial, Helvetica, sans-serif; }</style>',
        f'<text x="{margin:.2f}" y="{17 * scale:.2f}" font-size="{8.8 * scale:.2f}" font-weight="800" fill="#111111">{esc(project)} · Radial Atlas</text>',
        f'<text x="{margin:.2f}" y="{26 * scale:.2f}" font-size="{3.4 * scale:.2f}" fill="#444444">Draft radial atlas prototype · {esc(mode)} mode · not final public poster</text>',
    ]

    for index, branch in enumerate(branches):
        angle_start = start_offset + index * sector_span + 0.8
        angle_end = start_offset + (index + 1) * sector_span - 0.8
        fill = SECTOR_COLORS[index % len(SECTOR_COLORS)]
        stroke = SECTOR_STROKES[index % len(SECTOR_STROKES)]
        parts.append(
            f'<path d="{sector_path(cx, cy, sector_inner_rx, sector_inner_ry, outer_rx, outer_ry, angle_start, angle_end)}" '
            f'fill="{fill}" fill-opacity="0.62" stroke="{stroke}" stroke-width="{0.45 * scale:.2f}" />'
        )

    parts.extend(
        [
            f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{sector_inner_rx:.2f}" ry="{sector_inner_ry:.2f}" fill="#111827" />',
            f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{outer_rx:.2f}" ry="{outer_ry:.2f}" fill="none" stroke="#BBC1C9" stroke-width="{0.45 * scale:.2f}" />',
            f'<g data-level="0" data-name="{esc(root_name)}">',
            text_element(cx, cy - 5 * scale, [project], size=7.4 * scale, weight=800, fill="#FFFFFF"),
            text_element(cx, cy + 7 * scale, wrap_label(root_name, 26, 2), size=4.2 * scale, weight=600, fill="#E5E7EB"),
            f'<text x="{cx:.2f}" y="{cy + 19 * scale:.2f}" font-size="{2.6 * scale:.2f}" fill="#B9C1CC" text-anchor="middle">Level 0 · Field</text>',
            "</g>",
        ]
    )

    for index, branch in enumerate(branches):
        angle = start_offset + (index + 0.5) * sector_span
        fill = SECTOR_COLORS[index % len(SECTOR_COLORS)]
        stroke = SECTOR_STROKES[index % len(SECTOR_STROKES)]
        parts.append(
            draw_sector_card(
                branch,
                cx=cx,
                cy=cy,
                angle=angle,
                radius_x=card_radius_x,
                radius_y=card_radius_y,
                fill=fill,
                accent=stroke,
                scale=scale,
                mode=mode,
            )
        )

    legend_y = height - 13 * scale
    legend = (
        "Legend: center = Level 0 field · sector cards = Level 1 areas"
        + (" with Level 2 mini-lists" if mode == "detailed" else "")
        + " · draft radial atlas prototype, not final public poster"
    )
    parts.append(
        f'<text x="{margin:.2f}" y="{legend_y:.2f}" font-size="{2.8 * scale:.2f}" fill="#444444">{esc(legend)}</text>'
    )
    parts.append(
        f'<text x="{width - margin:.2f}" y="{legend_y:.2f}" font-size="{2.8 * scale:.2f}" fill="#666666" text-anchor="end">AI Atlas v{esc(version)}</text>'
    )
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a draft AI Atlas radial SVG poster."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help=f"Taxonomy JSON input. Default: {DEFAULT_INPUT.relative_to(ROOT)}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"SVG output. Default: {DEFAULT_OUTPUT.relative_to(ROOT)}",
    )
    parser.add_argument(
        "--size",
        choices=sorted(SIZES_MM),
        default="A1_LANDSCAPE",
        help="Printable target size. Default: A1_LANDSCAPE.",
    )
    parser.add_argument(
        "--mode",
        choices=("overview", "detailed"),
        default="detailed",
        help="Content density. Default: detailed.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = args.input if args.input.is_absolute() else ROOT / args.input
    output_path = args.output if args.output.is_absolute() else ROOT / args.output
    data = load_taxonomy(input_path)
    svg = generate_svg(data, size_name=args.size, mode=args.mode)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg, encoding="utf-8")
    try:
        display_path = output_path.relative_to(ROOT)
    except ValueError:
        display_path = output_path
    print(f"Generated {display_path}")
    print("Draft radial atlas prototype; export the SVG from a browser or vector editor to create a PDF.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
