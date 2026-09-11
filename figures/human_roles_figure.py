"""Human roles in AI-assisted systematic reviews.

Run: .venv/bin/python figures/human_roles_figure.py
Exports a 300-dpi PNG and editable PDF beside this source.
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

COLORS = dict(ink='#2B2B2B', gray='#6B6B6B', blue='#DCEBF7',
              amber='#FCEFD8', amber_edge='#B87E17', divider='#D9D9D9')
FIG_W, FIG_H = 11.8, 5.25
COLUMNS = [
    dict(title='Required input', group='Within the SR workflow',
         role='Enables the workflow\nto proceed',
         absent='Pipeline halts\nuntil input is provided',
         example='Reviewer sign-off before\nscreening decisions\nare finalized',
         report='Which stages require input;\nwho provides it and how'),
    dict(title='Permitted intervention', group='',
         role='Optionally changes\na system decision or output',
         absent='Pipeline continues\nwithout intervention',
         example='Optional correction of\na screening decision or\nan extracted value',
         report='Where edits are accepted;\nwhether they were used'),
    dict(title='Evaluation involvement', group='Assessment of the output',
         role='Provides a reference\nstandard or expert judgement',
         absent='Output can be produced;\nhuman assessment is absent',
         example='Original review decisions\nreused as a reference, or\nan expert panel’s judgements',
         report='Source of human judgements;\nwhich output was evaluated'),
]


def build_figure():
    plt.rcParams.update({'font.family': 'sans-serif',
        'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
        'pdf.fonttype': 42, 'ps.fonttype': 42})
    fig = plt.figure(figsize=(FIG_W, FIG_H), facecolor='white')
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, FIG_W), ylim=(0, FIG_H), aspect='equal')
    ax.axis('off')
    def text(x, y, value, size=14, weight='normal', color=None, ha='center'):
        return ax.text(x, y, value, fontsize=size, fontweight=weight,
                       color=color or COLORS['ink'], ha=ha, va='center', linespacing=1.2)
    start, width, gap = 2.04, 2.91, .30
    centers = [start + i*(width+gap) + width/2 for i in range(3)]
    text((centers[0]+centers[1])/2, 4.94, COLUMNS[0]['group'], 13, color=COLORS['gray'])
    text(centers[2], 4.94, COLUMNS[2]['group'], 13, color=COLORS['gray'])
    ax.plot([start, start+2*width+gap], [4.72,4.72], color=COLORS['divider'], lw=1)
    ax.plot([start+2*(width+gap),start+2*(width+gap)+width], [4.72,4.72], color=COLORS['divider'], lw=1)
    rows = [('Human role',3.65), ('Without this\ninvolvement',2.69),
            ('Example',1.65), ('Report explicitly',.59)]
    for title,y in rows:
        text(.30,y,title,14,'bold',ha='left')
    for i,col in enumerate(COLUMNS):
        x = start+i*(width+gap)
        center=centers[i]
        text(center,4.39,col['title'],15,'bold')
        for key,y,h,face,edge,bold in [
            ('role',3.65,.79,COLORS['blue'],'none',False),
            ('absent',2.69,.79,COLORS['amber'],COLORS['amber_edge'],True)]:
            ax.add_patch(FancyBboxPatch((x,y-h/2),width,h,
                boxstyle='round,pad=0,rounding_size=0.075',
                facecolor=face,edgecolor=edge,linewidth=1.2))
            text(center,y,col[key],14,'bold' if bold else 'normal')
        text(center,1.65,col['example'],14)
        ax.plot([x,x+width],[1.03,1.03],color=COLORS['divider'],lw=.8)
        text(center,.59,col['report'],13)
    # Separate evaluation from the two operational roles without a heavy grid.
    boundary=start+2*(width+gap)-gap/2
    ax.plot([boundary,boundary],[.22,4.64],color=COLORS['divider'],lw=1,ls=(0,(3,3)))
    return fig


def main():
    fig=build_figure()
    for ext in ('png','pdf'):
        output=Path(__file__).resolve().with_suffix('.'+ext)
        fig.savefig(output,dpi=300,facecolor='white')
        print(output)
    plt.close(fig)

if __name__=='__main__':
    main()
