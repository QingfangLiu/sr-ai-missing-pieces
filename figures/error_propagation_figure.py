"""Conceptual error propagation in systematic reviews (SRs).

Run: .venv/bin/python figures/error_propagation_figure.py
Requires matplotlib. Exports a 300-dpi PNG and editable PDF/SVG beside this file.
Edit PATHWAYS and COLORS to customize the examples and styling.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

COLORS = dict(ink="#2B2B2B", gray="#6B6B6B", blue="#0072B2",
              green="#368A45", red="#CC3D35",
              blue_fill="#DCEBF7", green_fill="#E6F3E7", red_fill="#FBE8E6", black="#000000",
              divider="#D9D9D9", neutral="#F4F4F4")
FIG_W, FIG_H, DPI = 10.2, 7.75, 300
Y_MIN = -0.15
ERROR_ARROW_LENGTH = 0.20
FONT_INCREASE = 5.5
PATHWAYS = [
    dict(y=2.20, title="Low-impact error example", edge="green",
         boxes=["Commentary\narticle\nmistakenly\nincluded",
                "No extractable\noutcome data",
                "Little impact\non downstream\nsynthesis"]),
    dict(y=.60, title="High-impact error example", edge="red",
         boxes=["Study of an\nineligible\nintervention\nincluded",
                "Outcome data\nextracted and\nretained in\nsynthesis",
                "May bias pooled\nestimate /\nconclusions"]),
]


def build_figure():
    plt.rcParams.update({"font.family": "sans-serif",
                         "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
                         "pdf.fonttype": 42, "ps.fonttype": 42,
                         "svg.fonttype": "none"})
    fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor="white")
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, 9.1), ylim=(Y_MIN, Y_MIN + FIG_H), aspect="auto")
    ax.axis("off")

    def text(x, y, value, size=12, weight="normal", color="ink", ha="center"):
        return ax.text(x, y, value, fontsize=size+FONT_INCREASE, fontweight=weight,
                       color=COLORS.get(color, color), ha=ha, va="center",
                       linespacing=1.35)

    def box(x, y, w, h, value="", face="neutral", edge="none", size=12,
            weight="normal"):
        ax.add_patch(FancyBboxPatch((x, y-h/2), w, h,
                     boxstyle="round,pad=0,rounding_size=0.075",
                     facecolor=COLORS.get(face, face),
                     edgecolor=COLORS.get(edge, edge), linewidth=1.2))
        if value:
            text(x+w/2, y, value, size, weight)

    def arrow(start, end, color="gray", rad=0):
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="->",
                     connectionstyle=f"arc3,rad={rad}", mutation_scale=12,
                     linewidth=1.3, color=COLORS[color], shrinkA=0, shrinkB=0))

    def divider(x0, x1, y):
        ax.plot([x0, x1], [y, y], color=COLORS["divider"], lw=1)

    # A: stagewise processing and human cross-stage checking.
    text(.3, 7.25, "A  Error propagation through the systematic review pipeline", 15, "bold", ha="left")
    text(.3, 3.12, "B  Downstream impact of different error types", 15, "bold", ha="left")
    # Error columns share the screening, extraction, and synthesis centers
    # with both workflows above (4.38, 6.18, and 7.98).
    error_columns = [(3.57, 1.62), (5.37, 1.62), (7.17, 1.62)]
    for path in PATHWAYS:
        y = path["y"]
        box(3.54, y, 5.36, 1.20, face=path["edge"]+"_fill")
        text(.3, y, path["title"], 12 if path["edge"] == "green" else 10.5,
             "bold", path["edge"], ha="left")
        for i, (x, width) in enumerate(error_columns):
            text(x+width/2, y, path["boxes"][i], size=10.5,
                 weight="bold" if i == 2 else "normal", color="black")
            if i < 2:
                center = (x+width/2 + error_columns[i+1][0]+error_columns[i+1][1]/2)/2
                arrow((center-ERROR_ARROW_LENGTH/2, y),
                      (center+ERROR_ARROW_LENGTH/2, y), "black")
    divider(.3, 8.75, 3.48)

    # Feedback highlights the eligibility check described in the paragraph.
    def workflow(y, human):
        text(.3, y, "Human\nreviewer" if human else "Stagewise AI\nworkflow",
             12, "bold", "blue" if human else "ink", ha="left")
        xs = [2.0, 3.80, 5.60, 7.40]
        labels = ["Search", "Screening", "Data\nextraction", "Evidence\nsynthesis"]
        for i, (x, value) in enumerate(zip(xs, labels)):
            box(x-.10, y, 1.36, .68, value, size=10.5)
            if i < len(xs)-1:
                arrow((x+1.29, y), (xs[i+1]-.13, y))
        if human:
            arrow((6.18, y+.39), (4.38, y+.39), "blue", rad=.14)

    workflow(6.58, False)
    text(1.90, 6.02, "Downstream stages generally accept upstream outputs.",
         11, color="gray", ha="left")
    workflow(4.47, True)
    box(3.78, 5.43, 3.0, .62, face="blue_fill")
    note = text(5.28, 5.43, "Eligibility can be confirmed\nduring extraction", 11, color="black")
    note.set_fontstyle("italic")
    text(1.90, 3.90, "Reviewers may revisit earlier decisions.",
         11, color="gray", ha="left")

    return fig


def main():
    fig = build_figure()
    for extension in ("png", "pdf", "svg"):
        output = Path(__file__).resolve().with_suffix("."+extension)
        fig.savefig(output, dpi=DPI, facecolor="white")
        print(f"Saved {output}")
    plt.close(fig)


if __name__ == "__main__":
    main()
