"""Editable three-task diagram of LLM-assisted systematic reviews.

Run: python3 figures/task_centered_paradigm_figure.py
Requires: matplotlib (python3 -m pip install matplotlib).
PNG and PDF are saved alongside this script, regardless of working directory.
Edit TEXT, STAGES, COLORS, and the layout constants below to customize the figure.
PDF embeds editable fonts.
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


TEXT = {
    "input": "Input",
    "action": "LLM’s role",
    "output": "Output",
    "evaluation": "Typical\nevaluation",
}

STAGES = [
    {
        "title": "Literature searching",
        "input": "Review question",
        "action": "LLM generates\nBoolean queries",
        "output": "Retrieved study records",
        "evaluation": "Recall, precision, etc.",
    },
    {
        "title": "Study screening",
        "input": "Study records +\neligibility criteria",
        "action": "LLM classifies\ninclude / exclude",
        "output": "Inclusion/exclusion\ndecisions",
        "evaluation": "Recall, specificity,\nagreement, etc.",
    },
    {
        "title": "Data extraction",
        "input": "Full texts +\nextraction forms",
        "action": "LLM extracts\nstructured fields",
        "output": "Study-level data",
        "evaluation": "Field-level or study-level\naccuracy or agreement, etc.",
    },
]

# Palette and typography match outcome_mapping_figure.py.
COLORS = {
    "ink": "#2B2B2B", "gray": "#6B6B6B", "blue": "#0072B2",
    "data_fill": "#DCEBF7", "action_fill": "#FCEFD8",
    "action_edge": "#B87E17", "divider": "#D9D9D9",
}
FIG_W, FIG_H = 11.8, 4.10
# Reserve a shared row-label gutter, including the evaluation row.
Y_MIN = 0.50
DPI = 300
FONT_SIZE = 16
MARGIN, COLUMN_GAP = 0.40, 0.55
LABEL_GUTTER = 1.60
OUTPUT_STEM = "task_centered_paradigm_figure"


def label(ax, x, y, text, size=FONT_SIZE, weight="normal", color=None, ha="center"):
    return ax.text(x, y, text, ha=ha, va="center", fontsize=size,
                   fontweight=weight, color=color or COLORS["ink"], linespacing=1.15)


def rounded_box(ax, x, y, width, height, text, face, edge="none", weight="normal"):
    ax.add_patch(FancyBboxPatch(
        (x, y), width, height,
        boxstyle="round,pad=0,rounding_size=0.075",
        facecolor=face, edgecolor=edge, linewidth=1.2,
    ))
    label(ax, x + width / 2, y + height / 2, text, weight=weight)


def arrow(ax, start, end, width=1.1, scale=11):
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="->",
                                mutation_scale=scale, linewidth=width,
                                color=COLORS["gray"], shrinkA=0, shrinkB=0))


def build_figure():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "pdf.fonttype": 42, "ps.fonttype": 42,
    })
    fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, FIG_W), ylim=(Y_MIN, Y_MIN + FIG_H), aspect="equal")
    ax.axis("off")

    for key, y in (("input", 3.77), ("action", 2.75), ("output", 1.69),
                   ("evaluation", 0.92)):
        label(ax, MARGIN, y, TEXT[key], weight="bold", ha="left")

    column_width = (FIG_W - 2 * MARGIN - LABEL_GUTTER - COLUMN_GAP * (len(STAGES) - 1)) / len(STAGES)
    for i, stage in enumerate(STAGES):
        x = MARGIN + LABEL_GUTTER + i * (column_width + COLUMN_GAP)
        center = x + column_width / 2
        label(ax, center, 4.30, stage["title"], size=15, weight="bold")

        rounded_box(ax, x, 3.46, column_width, 0.62, stage["input"], COLORS["data_fill"])
        arrow(ax, (center, 3.42), (center, 3.24))
        rounded_box(ax, x, 2.36, column_width, 0.78, stage["action"],
                    COLORS["action_fill"], COLORS["action_edge"], weight="bold")
        arrow(ax, (center, 2.27), (center, 2.09))
        rounded_box(ax, x, 1.38, column_width, 0.62, stage["output"], COLORS["data_fill"])

        ax.plot([x, x + column_width], [1.27, 1.27], color=COLORS["divider"], linewidth=0.8)
        label(ax, center, 0.92, stage["evaluation"], size=16, color=COLORS["ink"])

    return fig


def main():
    fig = build_figure()
    output_dir = Path(__file__).resolve().parent
    for extension in ("png", "pdf"):
        output = output_dir / f"{OUTPUT_STEM}.{extension}"
        fig.savefig(output, dpi=DPI, facecolor="white")
        print(f"Saved {output}")
    plt.close(fig)


if __name__ == "__main__":
    main()
