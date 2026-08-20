"""
Figure: outcome semantic alignment / clustering across three intervention domains.

Illustrates the paragraph's central contrast:
  (1) differently-labeled outcomes that map onto the SAME construct, and
  (2) similarly-labeled outcomes that must NOT be mapped together, because
      they differ on follow-up window, measurement timing, or the specific
      construct being graded.

Each of the 3 columns is a real example drawn from a published/registered
trial. The figure itself carries no citation numbers by design — citations
belong in the figure caption/legend text, tracked separately. Edit COLUMNS
below to change wording/examples.

Output: outcome_mapping_figure.pdf (vector, edit-safe) in this folder.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.path import Path

# ---------------------------------------------------------------------------
# Style: Nature Medicine-ish — sans-serif, restrained color, no chart junk.
# ---------------------------------------------------------------------------
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "pdf.fonttype": 42,   # embed as editable text, not outlines/curves
    "ps.fonttype": 42,
    "axes.linewidth": 0,
})

BLUE = "#0072B2"     # merge / converges-to-one-construct
ORANGE = "#E69F00"   # kept separate / must NOT be merged
INK = "#2B2B2B"
GRAY = "#6B6B6B"
BOX_FACE = "#F4F4F4"
BOX_EDGE = "#9A9A9A"

FIG_W, FIG_H = 10.2, 5.48

COLUMNS = [
    {
        "title": "Knee osteoarthritis\ntrials",
        "construct": "Pain",
        "merge_labels": [
            "“WOMAC pain\nsubscale”",
            "“KOOS pain\nsubscale”",
            "“VAS for\npain”",
        ],
        "merge_heading": "Different wording → same construct",
        "sep_labels": [
            "“WOMAC\nstiffness\nsubscale”",
            "“WOMAC\nphysical\nfunction\nsubscale”",
            "“WOMAC\ntotal\nscore”",
        ],
        "sep_heading": "Similar wording → different constructs",
        "sep_note": "same instrument, different construct",
    },
    {
        "title": "Depression trials",
        "construct": "Depressive symptoms",
        "merge_labels": [
            "“HAM-D · PHQ-9 · GDS · HSCL-20 ·\nMADRS · BDI-FS · CES-D”",
        ],
        "merge_heading": "Different wording → same construct",
        "sep_labels": [
            "“Depressive symptom\nseverity (SMD)”",
            "“Disease remission\n(RR)”",
        ],
        "sep_heading": "Similar wording → different constructs",
        "sep_note": "continuous severity ≠ binary remission",
    },
    {
        "title": "Treatment-related\nharm outcomes",
        "construct": "Grade ≥3 treatment-\nrelated adverse events",
        "merge_labels": [
            "“Grade 3 or higher\ntreatment-related AEs”",
            "“AEs of grade 3–5,\nrelated to treatment”",
        ],
        "merge_heading": "Different wording → same construct",
        "sep_labels": [
            "“Serious adverse\nevents (SAEs)”",
            "“Grade ≥3 adverse\nevents, all-cause”",
        ],
        "sep_heading": "Similar wording → different constructs",
        "sep_note": "seriousness ≠ severity grade",
    },
]

def rounded_box(ax, x, y, w, h, text, face, edge, fontsize=10.5, fontweight="bold",
                 textcolor=INK, zorder=3):
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.010,rounding_size=0.018",
        facecolor=face, edgecolor=edge, linewidth=1.7, zorder=zorder,
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
             fontweight=fontweight, color=textcolor, zorder=zorder + 1,
             linespacing=1.3)
    return box


def converge_arrow(ax, x0, y0, x1, y1, color):
    arrow = FancyArrowPatch(
        (x0, y0), (x1, y1),
        connectionstyle="arc3,rad=0.0",
        arrowstyle="-|>", mutation_scale=15,
        linewidth=2.0, color=color, zorder=2, shrinkA=2, shrinkB=4,
    )
    ax.add_patch(arrow)


def draw_column(ax, col):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Column title
    ax.text(0.5, 0.975, col["title"], ha="center", va="top",
             fontsize=14.5, fontweight="bold", color=INK, linespacing=1.25)

    # --- Merge block (supports 2 or 3 converging labels) --------------
    ax.text(0.5, 0.79, col["merge_heading"], ha="center", va="center",
             fontsize=11, style="italic", fontweight="bold", color=GRAY)

    n = len(col["merge_labels"])
    span_l, span_r = 0.02, 0.98
    xs = [span_l + (span_r - span_l) * (i + 0.5) / n for i in range(n)]
    box_w = (span_r - span_l) / n - 0.015
    box_fs = 9.8 if n <= 2 else 9.4
    top_y = 0.66
    for x, label in zip(xs, col["merge_labels"]):
        rounded_box(ax, x, top_y, box_w, 0.185, label, BOX_FACE, BOX_EDGE,
                    fontsize=box_fs)

    construct_y = 0.42
    rounded_box(ax, 0.5, construct_y, 0.9, 0.165, col["construct"],
                "#DCEBF7", BLUE, fontsize=14.5, fontweight="bold",
                textcolor="#003A5C", zorder=3)

    for i, x in enumerate(xs):
        target_x = 0.5 + (i - (n - 1) / 2) * 0.12
        converge_arrow(ax, x, top_y - 0.095, target_x, construct_y + 0.085, BLUE)

    # divider
    ax.plot([0.04, 0.96], [0.29, 0.29], color="#D9D9D9", linewidth=1.4, zorder=1)

    # --- Non-merge block ----------------------------------------------
    ax.text(0.5, 0.245, col["sep_heading"], ha="center", va="center",
             fontsize=11, style="italic", fontweight="bold", color=GRAY)

    sep_labels = col["sep_labels"]
    n_sep = len(sep_labels)
    sep_span_l, sep_span_r = 0.02, 0.98
    sep_gap = 0.025 if n_sep <= 2 else 0.055
    sep_box_w = ((sep_span_r - sep_span_l) - sep_gap * (n_sep - 1)) / n_sep
    sep_xs = [sep_span_l + sep_box_w / 2 + i * (sep_box_w + sep_gap)
              for i in range(n_sep)]
    sep_box_fs = 9.8 if n_sep <= 2 else 8.3
    sep_box_h = 0.185 if n_sep <= 2 else 0.22
    sep_y = 0.115 if n_sep <= 2 else 0.10
    for x, label in zip(sep_xs, sep_labels):
        rounded_box(ax, x, sep_y, sep_box_w, sep_box_h, label,
                    "#FCEFD8", "#B87E17", fontsize=sep_box_fs)

    # blocked-merge glyph between each adjacent pair (drawn, not a text
    # glyph, so it survives PDF font subsetting for journal submission)
    for x0, x1 in zip(sep_xs[:-1], sep_xs[1:]):
        ax.plot([(x0 + x1) / 2], [sep_y], marker="x", markersize=13,
                 markeredgewidth=3.2, color=ORANGE, zorder=4, linestyle="none")

    ax.text(0.5, sep_y - 0.135, col["sep_note"], ha="center", va="center",
             fontsize=10.5, style="italic", fontweight="bold", color="#8A5A0D")


def main():
    fig, axes = plt.subplots(1, 3, figsize=(FIG_W, FIG_H))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.99, bottom=0.15, wspace=0.05)

    for ax, col in zip(axes, COLUMNS):
        draw_column(ax, col)

    # Legend for the two mechanisms
    legend_y = 0.045
    fig.text(0.28, legend_y, "→", color=BLUE, fontsize=17, fontweight="bold",
             ha="center", va="center")
    fig.text(0.30, legend_y, " mapped to a common construct", color=INK,
             fontsize=12, fontweight="bold", ha="left", va="center")
    fig.text(0.63, legend_y, "X", color=ORANGE, fontsize=14, fontweight="bold",
             ha="center", va="center", family="sans-serif")
    fig.text(0.65, legend_y, " kept as distinct constructs", color=INK,
             fontsize=12, fontweight="bold", ha="left", va="center")

    out_pdf = "outcome_mapping_figure.pdf"
    fig.savefig(out_pdf)
    fig.savefig("outcome_mapping_figure.png", dpi=300)
    print(f"Saved {out_pdf}")


if __name__ == "__main__":
    main()
