"""Outcome semantic alignment in knee osteoarthritis trials.

The figure contrasts differently worded outcomes that map to the same
construct with similarly worded outcomes that must remain distinct.

Run: .venv/bin/python figures/outcome_mapping_figure.py
Exports a 300-dpi PNG and editable PDF beside this file.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


# Match the green/red palette used in panel B of error_propagation_figure.py.
COLORS = {
    "ink": "#2B2B2B",
    "gray": "#6B6B6B",
    "green": "#368A45",
    "green_fill": "#E6F3E7",
    "red": "#CC3D35",
    "red_fill": "#FBE8E6",
    "neutral": "#F4F4F4",
    "neutral_edge": "#9A9A9A",
    "divider": "#D9D9D9",
}

FIG_W, FIG_H, DPI = 6.7, 3.15, 300


def build_figure():
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

    fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, 6.7), ylim=(0.82, 3.97))
    ax.axis("off")

    def text(x, y, value, size=11, weight="normal", color="ink",
             ha="center", style="normal"):
        return ax.text(
            x, y, value, ha=ha, va="center", fontsize=size,
            fontweight=weight, fontstyle=style,
            color=COLORS.get(color, color), linespacing=1.25,
        )

    def box(x, y, w, h, value, face="neutral", edge="neutral_edge",
            size=11, weight="normal", text_color="ink"):
        ax.add_patch(FancyBboxPatch(
            (x, y - h / 2), w, h,
            boxstyle="round,pad=0.01,rounding_size=0.10",
            facecolor=COLORS.get(face, face),
            edgecolor=COLORS.get(edge, edge), linewidth=1.7,
        ))
        text(x + w / 2, y, value, size=size, weight=weight,
             color=text_color)

    def arrow(start, end, color="green"):
        ax.add_patch(FancyArrowPatch(
            start, end, arrowstyle="-|>", mutation_scale=15,
            linewidth=2.0, color=COLORS[color], shrinkA=2, shrinkB=0,
        ))

    # Relationship labels form a left-hand column so the examples can use
    # the available horizontal space.
    content_left, content_right = 1.75, 6.45
    text(0.22, 3.28, "Different wording\n→ same outcome",
         size=11.5, weight="bold", color="ink", ha="left")

    merge_labels = [
        "“WOMAC pain\nsubscale”",
        "“KOOS pain\nsubscale”",
        "“VAS for\npain”",
    ]
    gap = 0.16
    source_w = (content_right - content_left - 2 * gap) / 3
    source_y, source_h = 3.40, 0.72
    source_xs = [content_left + i * (source_w + gap) for i in range(3)]
    for x, label in zip(source_xs, merge_labels):
        box(x, source_y, source_w, source_h, label, size=11.0)

    construct_y, construct_h = 2.43, 0.62
    center_x = (content_left + content_right) / 2
    construct_w = 1.05
    box(center_x - construct_w / 2, construct_y, construct_w, construct_h,
        "Pain", face="green_fill", edge="green", size=15, weight="bold",
        text_color="green")
    target_xs = [center_x - 0.34, center_x, center_x + 0.34]
    arrow_end_y = construct_y + construct_h / 2 + 0.04
    for x, target_x in zip(source_xs, target_xs):
        arrow((x + source_w / 2, source_y - source_h / 2),
              (target_x, arrow_end_y))

    ax.plot([0.22, 6.45], [1.95, 1.95], color=COLORS["divider"], lw=1.2)

    text(0.22, 1.28, "Similar wording\n→ different\noutcomes",
         size=11.5, weight="bold", color="ink", ha="left")

    separate_labels = [
        "“WOMAC stiffness\nsubscale”",
        "“WOMAC physical\nfunction subscale”",
        "“WOMAC total\nscore”",
    ]
    separate_y, separate_h = 1.40, 0.82
    for x, label in zip(source_xs, separate_labels):
        box(x, separate_y, source_w, separate_h, label,
            face="red_fill", edge="red", size=10.6)

    for left_x, right_x in zip(source_xs[:-1], source_xs[1:]):
        marker_x = (left_x + source_w + right_x) / 2
        ax.plot([marker_x], [separate_y], marker="x", markersize=13,
                markeredgewidth=3.2, color=COLORS["red"], linestyle="none")

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
