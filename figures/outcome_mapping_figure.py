"""Outcome alignment across measures and follow-up times.

The figure contrasts differently worded outcomes that map to the same
construct with similarly worded outcomes that must remain distinct (panel A).
Panel B contrasts two review-specific approaches to grouping follow-up times,
using the examples and reference numbers in the supplied manuscript.
Selected follow-up durations come from the reviews' included-study tables:
https://pmc.ncbi.nlm.nih.gov/articles/PMC6464742/
https://pmc.ncbi.nlm.nih.gov/articles/PMC8571912/

Run: .venv/bin/python figures/outcome_mapping_figure.py
Exports a 300-dpi PNG and editable PDF beside this file.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


# Match the grouping palette and lighter geometry in Figure 3.
COLORS = {
    "ink": "#2B2B2B", "gray": "#6B6B6B",
    "indigo": "#5367A6", "indigo_fill": "#E8EBF6",
    "terracotta": "#B45F45", "terracotta_fill": "#F7E8E2",
    "neutral": "#F4F4F4", "neutral_edge": "#9A9A9A",
    "divider": "#D9D9D9",
}
PANEL_W = 6.7
FIG_W, FIG_H, DPI = 11.8, 4.9, 300
Y_MAX = 5.3
CONTENT_LEFT, CONTENT_RIGHT = 0.22, 6.45
CONTENT_WIDTH = CONTENT_RIGHT - CONTENT_LEFT
SOURCE_YS = (3.73, 1.59)
RESULT_YS = (2.92, 0.67)
SOURCE_H, RESULT_H = 0.55, 0.62

# Verified in CD008096.pdf, included-study tables and Analysis 1.6 (PDF p. 45).
# Douzinas 2006 (p. 31), Park 1992 (p. 36), Norton 1996 (p. 35),
# Bath 1997 (p. 28), Dennis 2005 (p. 30).
POOLED_FOLLOWUPS = ("20 days", "28 days", "6 weeks", "3 months", "6 months")
# Verified in CD001800.pdf against Analysis 1.1 (PDF pp. 221-222):
# Mutwalli 2012 (6 mo; p. 131), Campo 2020 (12 mo; p. 77),
# Pal 2013 (18 mo; p. 137), Toobert 2000 (24 mo; p. 166),
# Erdman 1986 (5 y; p. 90), Maroto 2005 (10 y; p. 126).
FOLLOWUP_WINDOWS = (
    ((6, 12), "Short term\n6-12 months"),
    ((18, 24), "Medium term\n>12-36 months"),
    ((60, 120), "Long term\n>36 months"),
)


def build_figure():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "pdf.fonttype": 42, "ps.fonttype": 42,
    })
    fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor="white")

    def text(ax, x, y, value, size=11.5, weight="normal", color="ink", ha="center"):
        return ax.text(x, y, value, ha=ha, va="center", fontsize=size,
                       fontweight=weight, color=COLORS.get(color, color),
                       linespacing=1.25)

    def box(ax, x, y, width, value, height=SOURCE_H, color=None, size=11.5):
        ax.add_patch(FancyBboxPatch(
            (x, y - height / 2), width, height,
            boxstyle="round,pad=0,rounding_size=0.065",
            facecolor=COLORS[color + "_fill" if color else "neutral"],
            edgecolor=COLORS[color or "neutral_edge"], linewidth=1.2,
            zorder=2,
        ))
        text(ax, x + width / 2, y, value, size=size)

    def arrow(ax, start_x, source_y, end_x, result_y, color):
        ax.add_patch(FancyArrowPatch(
            (start_x, source_y - SOURCE_H / 2 - 0.03),
            (end_x, result_y + RESULT_H / 2 + 0.04),
            arrowstyle="-|>", mutation_scale=12, linewidth=1.35,
            color=COLORS[color], shrinkA=1, shrinkB=1, zorder=1,
        ))

    def sources(ax, labels, y, gap=0.16):
        width = (CONTENT_WIDTH - (len(labels) - 1) * gap) / len(labels)
        xs = [CONTENT_LEFT + i * (width + gap) for i in range(len(labels))]
        for x, label in zip(xs, labels):
            box(ax, x, y, width, label)
        return xs, width

    axes = []
    for i, (letter, title) in enumerate((
            ("A", "Which measures represent\nthe same outcome?"),
            ("B", "Which follow-up times belong\nin the same synthesis?"))):
        ax = fig.add_axes([i / 2, 0, 0.5, 1])
        ax.set(xlim=(0, PANEL_W), ylim=(0, Y_MAX))
        ax.axis("off")
        text(ax, 0.22, 4.99, letter, size=16, weight="bold", ha="left")
        text(ax, 0.60, 4.99, title, size=14, ha="left")
        ax.plot([CONTENT_LEFT, CONTENT_RIGHT], [2.48, 2.48],
                color=COLORS["divider"], lw=1)
        axes.append(ax)

    left, right = axes
    left.plot([6.68, 6.68], [0.24, 5.20], color=COLORS["divider"], lw=1)

    # Both panels share two aligned examples: combine above, retain separate below.
    for ax, top, bottom in (
            (left, "Different wording, same outcome", "Similar wording, different outcomes"),
            (right, "Pool across follow-up", "Separate by follow-up window")):
        text(ax, CONTENT_LEFT, 4.37, top, size=12, weight="bold",
             color="indigo", ha="left")
        text(ax, CONTENT_LEFT, 2.23, bottom, size=12, weight="bold",
             color="terracotta", ha="left")

    # A, top: different measures map to the common pain construct.
    xs, width = sources(left, ("WOMAC pain\nsubscale", "KOOS pain\nsubscale", "VAS for pain"),
                        SOURCE_YS[0])
    center = (CONTENT_LEFT + CONTENT_RIGHT) / 2
    box(left, center - 0.80, RESULT_YS[0], 1.60, "Pain",
        height=RESULT_H, color="indigo", size=13)
    for i, x in enumerate(xs):
        arrow(left, x + width / 2, SOURCE_YS[0], center + (i - 1) * 0.30,
              RESULT_YS[0], "indigo")

    # A, bottom: shared instrument names do not make the constructs equivalent.
    xs, width = sources(left, ("WOMAC stiffness\nsubscale",
                                "WOMAC physical\nfunction subscale",
                                "WOMAC total\nscore"), SOURCE_YS[1])
    for x, label in zip(xs, ("Stiffness", "Physical function", "Composite score")):
        box(left, x, RESULT_YS[1], width, label, height=RESULT_H, color="terracotta")
        arrow(left, x + width / 2, SOURCE_YS[1], x + width / 2,
              RESULT_YS[1], "terracotta")

    # B, top: selected study durations enter a single mortality synthesis.
    text(right, CONTENT_LEFT, 4.10, "Mortality: selected study follow-ups",
         size=10, color="gray", ha="left")
    xs, width = sources(right, POOLED_FOLLOWUPS, SOURCE_YS[0], gap=0.12)
    box(right, center - 1.55, RESULT_YS[0], 3.10, "One pooled mortality estimate",
        height=RESULT_H, color="indigo")
    for i, x in enumerate(xs):
        arrow(right, x + width / 2, SOURCE_YS[0], center + (i - 2) * 0.30,
              RESULT_YS[0], "indigo")

    # B, bottom: two concrete durations are mapped into each follow-up window.
    text(right, CONTENT_LEFT, 1.96, "All-cause mortality: selected follow-ups (months)",
         size=10, color="gray", ha="left")
    values = [str(month) for months, _ in FOLLOWUP_WINDOWS for month in months]
    xs, width = sources(right, values, SOURCE_YS[1], gap=0.12)
    result_gap = 0.16
    result_width = (CONTENT_WIDTH - 2 * result_gap) / 3
    for i, (_, label) in enumerate(FOLLOWUP_WINDOWS):
        x = CONTENT_LEFT + i * (result_width + result_gap)
        box(right, x, RESULT_YS[1], result_width, label,
            height=RESULT_H, color="terracotta")
        for j in range(2):
            arrow(right, xs[2 * i + j] + width / 2, SOURCE_YS[1],
                  x + result_width / 2 + (j - 0.5) * 0.32,
                  RESULT_YS[1], "terracotta")

    return fig


def main():
    fig = build_figure()
    output_stem = Path(__file__).resolve().with_suffix("")
    for extension in ("png", "pdf"):
        output = output_stem.with_suffix("." + extension)
        fig.savefig(output, dpi=DPI, facecolor="white",
                    bbox_inches="tight", pad_inches=0.04)
        print(f"Saved {output}")
    plt.close(fig)


if __name__ == "__main__":
    main()
