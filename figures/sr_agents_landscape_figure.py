"""LLM agent landscape for systematic review and meta-analysis.

Run: .venv/bin/python figures/sr_agents_landscape_figure.py
Exports a 300-dpi PNG and editable PDF beside this source.
Edit ROWS to update the table. Columns: system, search, screening, extraction,
risk of bias, statistical pooling, evaluation scope. Codes: Y/H/--.
The figure is self-contained.
"""
from pathlib import Path
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.offsetbox import AnnotationBbox, VPacker, TextArea

# First-listed author in the reviewed paper (including papers with co-first authors).
FIRST_AUTHORS = {
    'TrialMind': 'Wang',
    'otto-SR': 'Cao',
    'A4SLR': 'Lee',
    'AgentSLR': 'Padarha',
    'LUMEN': 'Huang',
    'AutoSynthesis': 'Taherinezhad',
    'MetaMind': 'Livieratos',
    'LatteReview': 'Rouzrokh',
    'AutoMetaCoder': 'Min',
    'InsightAgent': 'Qiu',
    'Manalyzer': 'Xu',
    'meta-pipe': 'Lin',
}

# Journal/proceedings year where established; otherwise the reviewed preprint.
PUBLICATION = {
    'TrialMind': '2025',
    'otto-SR': 'preprint',
    'A4SLR': '2025',
    'AgentSLR': '2026',
    'LUMEN': 'preprint',
    'AutoSynthesis': 'preprint',
    'MetaMind': '2026',
    'LatteReview': 'preprint',
    'AutoMetaCoder': 'preprint',
    'InsightAgent': '2025',
    'Manalyzer': 'preprint',
    'meta-pipe': 'preprint',
}

ROWS = [['TrialMind',
  'Y',
  'Y',
  'Y',
  '--',
  'H',
  '100 clinical SRs / 2,220 studies; numerical standardization feeds human-run R pooling'],
 ['otto-SR',
  'H',
  'Y',
  'Y',
  'Y',
  'H',
  'Task benchmarks and reproduction/update of 12 Cochrane reviews; search and analysis were '
  'investigator-performed using inherited specifications'],
 ['A4SLR',
  'Y',
  'Y',
  'Y',
  'Y',
  '--',
  'Two clinical use cases: lung cancer and perinatal mood/anxiety disorders'],
 ['AgentSLR',
  'Y',
  'Y',
  'Y',
  '--',
  '--',
  'Nine priority pathogens; structured epidemiological extraction and descriptive/narrative '
  'reports'],
 ['LUMEN',
  'Y',
  'Y',
  'Y',
  'Y',
  'Y',
  'Five clinical review applications plus two screening benchmarks; expert analytical decisions '
  'remain'],
 ['AutoSynthesis',
  'Y',
  'Y',
  'Y',
  'Y',
  'Y',
  'Demonstration on LLM persuasion, compared with published meta-analysis; limited breadth of '
  'validation'],
 ['MetaMind',
  'Y',
  'H',
  'Y',
  '--',
  'Y',
  "Ulcerative colitis / Crohn's disease NMA; manual feasibility, eligibility, and model-fit "
  'assessment'],
 ['LatteReview',
  '--',
  'Y',
  'Y',
  '--',
  '--',
  'Modular screening / extraction framework; framework examples and task evaluations, not full SR '
  'validation'],
 ['AutoMetaCoder',
  '--',
  'Y',
  'Y',
  '--',
  '--',
  'Screening implemented but not formally evaluated; extraction evaluated on 55 studies from a '
  'psychology meta-analysis'],
 ['InsightAgent',
  '--',
  'Y',
  '--',
  '--',
  '--',
  'Interactive abstract-level screening and narrative synthesis; no structured data extraction; '
  'nine-professional user study'],
 ['Manalyzer',
  'Y',
  'Y',
  'Y',
  '--',
  '--',
  '729 papers across atmosphere, agriculture, environment; generates general analyses rather than '
  'conventional effect-size pooling'],
 ['meta-pipe',
  'Y',
  'Y',
  'Y',
  'Y',
  'Y',
  'Implemented architecture; no empirical validation data; five mandatory human decision points']]


def build_figure():
    plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'], 'pdf.fonttype': 42, 'ps.fonttype': 42})
    fig, ax = plt.subplots(figsize=(10.8, 10.0))
    fig.subplots_adjust(left=.008, right=.992, top=.992, bottom=.008)
    ax.set_xlim(0, 10.8); ax.set_ylim(0, 16); ax.axis('off')
    xs = [0, 2.15, 2.99, 3.89, 4.82, 5.57, 6.50, 10.8]
    headers = ['System', 'Search /\nretrieval', 'Screening', 'Extraction', 'Risk of\nbias', 'Statistical\npooling', 'Evaluation scope and boundary']
    top=14.55; hh=.79; rh=.86
    ax.add_patch(Rectangle((0,top-hh),xs[-1],hh,color='#183b49'))
    for j,h in enumerate(headers):
        header_x = xs[j] + .10 if j in [0, 6] else (xs[j] + xs[j+1]) / 2
        header_x += {2: -.05, 3: .05}.get(j, 0)
        ax.text(header_x, top-hh/2, h, va='center',
                ha='left' if j in [0, 6] else 'center', fontsize=12,
                color='white', weight='bold')
    colors={'Y':('#e4f1ef','#1e675f'),
            'H':('#f8ebd5','#855b13'),
            '--':('#f3f4f5','#859099')}
    for i,row in enumerate(ROWS):
        y=top-hh-(i+1)*rh
        ax.add_patch(Rectangle((0,y),xs[-1],rh,color='#f5f8fa' if i%2==0 else 'white'))
        ax.plot([0,xs[-1]],[y,y],color='#dbe3e7',lw=.6)
        name = TextArea(row[0].replace(' [added]', ' *'),
                        textprops=dict(fontsize=11.5, weight='bold', color='#183b49'))
        citation = TextArea(f"({FIRST_AUTHORS[row[0]]}, {PUBLICATION[row[0]]})",
                            textprops=dict(fontsize=11.5, weight='normal', color='#183b49'))
        label = VPacker(children=[name, citation], align='left', pad=0, sep=3)
        ax.add_artist(AnnotationBbox(label, (.10, y+rh/2), xycoords='data',
                                    box_alignment=(0, .5), frameon=False, pad=0))
        for j in range(1,6):
            bg,fg=colors[row[j]]; cx=(xs[j]+xs[j+1])/2
            ax.add_patch(Rectangle((cx-.29,y+.19),.58,rh-.38,facecolor=bg,edgecolor='none'))
            ax.text(cx,y+rh/2,row[j],ha='center',va='center',fontsize=13,weight='bold',color=fg)
        ax.text(xs[6]+.10,y+rh/2,textwrap.fill(row[6],53),fontsize=11.5,va='center',linespacing=1.3,color='#30434e')
    bottom=top-hh-len(ROWS)*rh
    # Keep the capability legend visible; longer explanations stay in the caption.
    legend = [
        ('Y', 'Implemented by the system', .10, bottom - .34),
        ('H', 'Human-performed or inherited from the source review', 3.28, bottom - .34),
        ('--', 'Not implemented', 8.05, bottom - .34),
    ]
    for code, meaning, x, y in legend:
        bg, fg = colors[code]
        ax.add_patch(Rectangle((x, y - .14), .34, .28,
                               facecolor=bg, edgecolor='none'))
        ax.text(x + .17, y, code, fontsize=10.5, weight='bold',
                ha='center', va='center', color=fg)
        ax.text(x + .44, y, meaning, fontsize=10.5,
                ha='left', va='center', color='#30434e')
    ax.set_ylim(bottom - .62, top + .05)
    return fig


def main():
    fig = build_figure()
    for ext in ('png', 'pdf'):
        output = Path(__file__).resolve().with_suffix('.' + ext)
        fig.savefig(output, dpi=300, facecolor='white')
        print(output)
    plt.close(fig)


if __name__ == '__main__':
    main()
