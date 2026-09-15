"""Human roles in AI-assisted systematic reviews.

Run: .venv/bin/python figures/human_roles_figure.py
Exports a 300-dpi PNG and editable PDF beside this source.
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

COLORS = dict(ink='#20262B',
              role_fill='#E7EDF1', role_edge='#526D7A',
              absent_fill='#F1F2F3', absent_edge='#747C82',
              divider='#C9CED2')
FIG_W, FIG_H = 11.8, 4.4
COLUMNS = [
    dict(title='Required input', group='Within the SR workflow',
         role='Enables the workflow\nto proceed',
         absent='Pipeline halts\nuntil input is provided',
         example='Reviewer sign-off before\nscreening decisions\nare finalized'),
    dict(title='Optional input', group='',
         role='Optionally changes\na system decision or output',
         absent='Pipeline continues\nwithout modification',
         example='Optional correction of\na screening decision or\nan extracted value'),
    dict(title='Output evaluation', group='Outside of the SR workflow',
         role='Provides a reference\nstandard from experts',
         absent='Output can be produced;\nhuman assessment is absent',
         example='Original review decisions\nreused as a reference, or\nan expert panel’s judgements'),
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
    text((centers[0]+centers[1])/2, 4.09, COLUMNS[0]['group'], 14.5)
    text(centers[2], 4.09, COLUMNS[2]['group'], 14.5)
    ax.plot([start, start+2*width+gap], [3.87,3.87], color=COLORS['divider'], lw=1.2)
    ax.plot([start+2*(width+gap),start+2*(width+gap)+width], [3.87,3.87], color=COLORS['divider'], lw=1.2)
    rows = [('Human role',2.80), ('Without this\ninvolvement',1.84),
            ('Example',.70)]
    for title,y in rows:
        text(.30,y,title,15.5,'bold',ha='left')
    for i,col in enumerate(COLUMNS):
        x = start+i*(width+gap)
        center=centers[i]
        text(center,3.54,col['title'],17,'bold')
        for key,y,h,face,edge,bold in [
            ('role',2.80,.79,COLORS['role_fill'],COLORS['role_edge'],False),
            ('absent',1.84,.79,COLORS['absent_fill'],COLORS['absent_edge'],False)]:
            ax.add_patch(FancyBboxPatch((x,y-h/2),width,h,
                boxstyle='round,pad=0,rounding_size=0.075',
                facecolor=face,edgecolor=edge,linewidth=1.2))
            text(center,y,col[key],15.5,'bold' if bold else 'normal')
        text(center,.70,col['example'],15)
    # Separate evaluation from the two operational roles without a heavy grid.
    boundary=start+2*(width+gap)-gap/2
    ax.plot([boundary,boundary],[.15,3.79],color=COLORS['divider'],lw=1.2,ls=(0,(3,3)))
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
