"""
Figure: outcome semantic alignment / clustering across three intervention domains.

Illustrates the paragraph's central contrast:
  (1) differently-labeled outcomes that map onto the SAME construct, and
  (2) similarly-labeled outcomes that must NOT be mapped together, because
      they differ on follow-up window, measurement timing, or the specific
      construct being graded.

Each of the 3 columns is a real example drawn from a published/registered
trial (see REFERENCES at the bottom, and the numbered superscripts in the
figure). Edit COLUMNS below to change wording/examples; edit REFERENCES to
keep citation numbers in sync.

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

FIG_W, FIG_H = 10.2, 5.6

COLUMNS = [
    {
        "title": "Cardiovascular\nintervention trials",
        "construct": "Major adverse\ncardiovascular events",
        "merge_labels": [
            "“3-point MACE” [1]",
            "“Composite of CV death,\nMI, or stroke” [2]",
        ],
        "merge_heading": "Different wording → same construct",
        "sep_labels": [
            "“All-cause mortality,\n30 days” [3]",
            "“All-cause mortality,\n1 year” [4]",
        ],
        "sep_heading": "Similar wording → different constructs",
        "sep_note": "different follow-up windows",
    },
    {
        "title": "Glycemic control\ntrials",
        "construct": "HbA1c change\nfrom baseline",
        "merge_labels": [
            "“Reduction in HbA1c\nlevels” [5]",
            "“Change in glycosylated\nhemoglobin (HbA1c)” [6]",
        ],
        "merge_heading": "Different wording → same construct",
        "sep_labels": [
            "“Fasting blood\nglucose” [7]",
            "“Postprandial blood\nglucose (AUC)” [8]",
        ],
        "sep_heading": "Similar wording → different constructs",
        "sep_note": "different measurement timing",
    },
    {
        "title": "Treatment-related\nharm outcomes",
        "construct": "Grade ≥3 treatment-\nrelated adverse events",
        "merge_labels": [
            "“Grade 3 or higher\ntreatment-related AEs” [9]",
            "“AEs of grade 3–5,\nrelated to treatment” [10]",
        ],
        "merge_heading": "Different wording → same construct",
        "sep_labels": [
            "“Serious adverse\nevents (SAEs)” [11]",
            "“Grade ≥3 adverse\nevents, all-cause” [12]",
        ],
        "sep_heading": "Similar wording → different constructs",
        "sep_note": "seriousness ≠ severity grade",
    },
]

REFERENCES = [
    "1,2. Zinman B, et al. Empagliflozin, Cardiovascular Outcomes, and Mortality in Type 2 Diabetes "
    "(EMPA-REG OUTCOME). N Engl J Med 2015. pubmed.ncbi.nlm.nih.gov/26378978  |  "
    "Cardiovascular Inflammation Reduction Trial (CIRT). ClinicalTrials.gov NCT01594333.",
    "3,4. ACURATE neo2 IDE trial. ClinicalTrials.gov NCT03735667.  |  Frailty in Elderly Patients "
    "Receiving Cardiac Interventional Procedures. ClinicalTrials.gov NCT02386124.",
    "5,6. Impact of a digital application on HbA1c levels in people with diabetes: a randomized "
    "controlled trial. PMC12257309.  |  Comparison of NN1250 With Insulin Glargine in Type 1 "
    "Diabetes. ClinicalTrials.gov NCT01079234.",
    "7,8. Determining the optimal fasting glucose target for patients with type 2 diabetes "
    "(FPG GOAL trial). PubMed 30938035.  |  Improvements to postprandial glucose control in "
    "subjects with type 2 diabetes: a randomized placebo-controlled trial of a probiotic "
    "formulation. PubMed 32675291.",
    "9,10. Schmid P, et al. Pembrolizumab for Early Triple-Negative Breast Cancer (KEYNOTE-522). "
    "N Engl J Med 2020. doi:10.1056/NEJMoa1910549  |  Eggermont AMM, et al. Adjuvant Pembrolizumab "
    "versus Placebo in Resected Stage III Melanoma. N Engl J Med 2018. doi:10.1056/NEJMoa1802357",
    "11,12. Phase 1 Study of SGI-110 in Patients With Acute Myeloid Leukemia. ClinicalTrials.gov "
    "NCT02293993.  |  Gandhi L, et al. Pembrolizumab plus Chemotherapy in Metastatic Non-Small-Cell "
    "Lung Cancer (KEYNOTE-189). N Engl J Med 2018. doi:10.1056/NEJMoa1801005",
]


def rounded_box(ax, x, y, w, h, text, face, edge, fontsize=8.2, fontweight="normal",
                 textcolor=INK, zorder=3):
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.010,rounding_size=0.018",
        facecolor=face, edgecolor=edge, linewidth=1.1, zorder=zorder,
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
             fontweight=fontweight, color=textcolor, zorder=zorder + 1,
             linespacing=1.35)
    return box


def converge_arrow(ax, x0, y0, x1, y1, color):
    arrow = FancyArrowPatch(
        (x0, y0), (x1, y1),
        connectionstyle="arc3,rad=0.0",
        arrowstyle="-|>", mutation_scale=11,
        linewidth=1.4, color=color, zorder=2, shrinkA=2, shrinkB=4,
    )
    ax.add_patch(arrow)


def draw_column(ax, col):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Column title
    ax.text(0.5, 0.965, col["title"], ha="center", va="top",
             fontsize=10.5, fontweight="bold", color=INK, linespacing=1.3)

    # --- Merge block -------------------------------------------------
    ax.text(0.5, 0.775, col["merge_heading"], ha="center", va="center",
             fontsize=7.6, style="italic", color=GRAY)

    lx, rx = 0.24, 0.76
    top_y = 0.655
    rounded_box(ax, lx, top_y, 0.42, 0.155, col["merge_labels"][0],
                BOX_FACE, BOX_EDGE)
    rounded_box(ax, rx, top_y, 0.42, 0.155, col["merge_labels"][1],
                BOX_FACE, BOX_EDGE)

    construct_y = 0.435
    rounded_box(ax, 0.5, construct_y, 0.86, 0.145, col["construct"],
                "#DCEBF7", BLUE, fontsize=9.0, fontweight="bold",
                textcolor="#003A5C", zorder=3)

    converge_arrow(ax, lx, top_y - 0.078, 0.5 - 0.10, construct_y + 0.075, BLUE)
    converge_arrow(ax, rx, top_y - 0.078, 0.5 + 0.10, construct_y + 0.075, BLUE)

    # divider
    ax.plot([0.06, 0.94], [0.315, 0.315], color="#D9D9D9", linewidth=1.0, zorder=1)

    # --- Non-merge block ----------------------------------------------
    ax.text(0.5, 0.265, col["sep_heading"], ha="center", va="center",
             fontsize=7.6, style="italic", color=GRAY)

    sep_y = 0.145
    rounded_box(ax, lx, sep_y, 0.42, 0.155, col["sep_labels"][0],
                "#FCEFD8", "#B87E17")
    rounded_box(ax, rx, sep_y, 0.42, 0.155, col["sep_labels"][1],
                "#FCEFD8", "#B87E17")

    # blocked-merge glyph between the two boxes (drawn, not a text glyph,
    # so it survives PDF font subsetting for journal submission)
    ax.plot([0.5], [sep_y], marker="x", markersize=9, markeredgewidth=2.4,
             color=ORANGE, zorder=4, linestyle="none")

    ax.text(0.5, sep_y - 0.115, col["sep_note"], ha="center", va="center",
             fontsize=7.4, style="italic", color="#8A5A0D")


def main():
    fig, axes = plt.subplots(1, 3, figsize=(FIG_W, FIG_H))
    fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.16, wspace=0.06)

    for ax, col in zip(axes, COLUMNS):
        draw_column(ax, col)

    fig.text(0.5, 0.975,
              "From reported outcome labels to synthesis-ready outcome constructs",
              ha="center", va="top", fontsize=12.5, fontweight="bold", color=INK)

    # Legend for the two mechanisms
    legend_y = 0.055
    ax0 = axes[0]
    fig.text(0.30, legend_y, "→", color=BLUE, fontsize=13, fontweight="bold",
             ha="center", va="center")
    fig.text(0.315, legend_y, " mapped to a common construct", color=INK,
             fontsize=8.3, ha="left", va="center")
    fig.text(0.62, legend_y, "X", color=ORANGE, fontsize=11, fontweight="bold",
             ha="center", va="center", family="sans-serif")
    fig.text(0.635, legend_y, " kept as distinct constructs", color=INK,
             fontsize=8.3, ha="left", va="center")

    out_pdf = "outcome_mapping_figure.pdf"
    fig.savefig(out_pdf)
    fig.savefig("outcome_mapping_figure.png", dpi=300)
    print(f"Saved {out_pdf}")

    # Emit the reference list as a companion text file for the figure legend.
    with open("outcome_mapping_figure_references.txt", "w") as f:
        f.write("References for figure superscripts (for figure legend / methods text):\n\n")
        f.write("\n".join(REFERENCES))
    print("Saved outcome_mapping_figure_references.txt")


if __name__ == "__main__":
    main()
