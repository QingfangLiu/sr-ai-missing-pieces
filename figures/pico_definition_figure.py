"""Review-level PICO-S boundary decisions. Export editable PDF and 300-dpi PNG."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

INK, GRAY = '#2B2B2B', '#6B6B6B'
BLUE, BLUE_FILL = '#0072B2', '#DCEBF7'
AMBER, AMBER_FILL = '#B87E17', '#FCEFD8'

def build_figure():
    plt.rcParams.update({'font.family':'sans-serif',
        'font.sans-serif':['Arial','Helvetica','DejaVu Sans'],
        'pdf.fonttype':42, 'ps.fonttype':42})
    # Sized close to a journal text width so labels remain legible when inserted.
    fig = plt.figure(figsize=(9.2, 3.64), facecolor='white')
    ax = fig.add_axes([0,0,1,1])
    ax.set(xlim=(0,12), ylim=(.85,5.6), aspect='equal')
    ax.axis('off')
    def text(x,y,s,size=12,weight='normal',color=INK,ha='center',va='center'):
        ax.text(x,y,s,ha=ha,va=va,fontsize=size,fontweight=weight,
                color=color,linespacing=1.25)
    def box(x,y,w,h,s,face='#F4F4F4',edge='#9A9A9A',size=12,weight='normal'):
        ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,
            boxstyle='round,pad=0,rounding_size=0.065',facecolor=face,
            edgecolor=edge,lw=1.2,zorder=2))
        text(x,y,s,size,weight)
    def arrow(x,y,xx,yy,color=GRAY):
        ax.add_patch(FancyArrowPatch((x,y),(xx,yy),arrowstyle='-|>',
            mutation_scale=13,lw=1.4,color=color,shrinkA=3,shrinkB=3,zorder=1))

    # Three aligned panels.
    text(.3,5.5,'A',16,'bold',ha='left',va='top')
    text(.62,5.5,'From review question to\neligibility criteria',14,'bold',ha='left',va='top')
    text(4.2,5.5,'B',16,'bold',ha='left',va='top')
    text(4.52,5.5,'Group interventions or\nanalyze them separately?',14,'bold',ha='left',va='top')
    text(8.2,5.5,'C',16,'bold',ha='left',va='top')
    text(8.52,5.5,'How should co-interventions\naffect eligibility?',14,'bold',ha='left',va='top')

    # Panel A: the vertical review-definition flow.
    box(2,4.25,2.4,.68,'Review question',size=14,weight='bold')
    arrow(2,3.89,2,3.55)
    box(2,3.18,2.4,.68,'Review-level\nPICO-S',size=14,weight='bold')
    arrow(2,2.82,2,2.48)
    box(2,2.11,2.4,.68,'Eligibility criteria',size=14,weight='bold')
    text(2,1.36,'Review-level definitions are often\nsupplied by humans in current\nLLM-based review workflows',11.5,color=GRAY)

    # Panel B: lumper-splitter choices for intervention classes.
    text(6,4.72,'Newer-generation antidepressants',11.5,color=GRAY)
    for x,s in [(4.65,'Fluoxetine'),(6,'Paroxetine'),(7.35,'Sertraline')]:
        box(x,4.3,1.15,.48,s,size=10.5)
        arrow(x,4.04,6+(x-6)*.25,3.55,BLUE)
    text(4.35,3.64,'Lumper',12,'bold',BLUE,ha='left')
    box(6,3.2,3.35,.62,'One intervention class\nPooled class estimate',BLUE_FILL,BLUE,12.5,'bold')
    text(4.35,2.56,'Splitter',12,'bold',AMBER,ha='left')
    for x,s in [(4.65,'Fluoxetine'),(6,'Paroxetine'),(7.35,'Sertraline')]:
        box(x,2.08,1.15,.48,s,AMBER_FILL,AMBER,10.5)
    text(6,1.56,'Separate compound-level estimates',11.5,color=GRAY)

    # Panel C: context-dependent co-intervention rules.
    text(10,4.72,'Typically delivered together',12.5,'bold')
    box(10,4.14,3.35,.7,'Behavioral support\n+ pharmacotherapy',BLUE_FILL,BLUE,12.5)
    arrow(10,3.78,10,3.51,BLUE)
    text(10,3.25,'Requiring support alone may\nexclude most relevant trials',11.5)
    text(10,2.55,'Optional addition',12.5,'bold')
    box(10,1.96,3.35,.7,'Antidepressant medication\nwith or without psychotherapy',AMBER_FILL,AMBER,11.5)
    text(10,1.15,'The added therapy may\nmodify the effect',11.5,color=GRAY)
    return fig

if __name__ == '__main__':
    fig=build_figure()
    for ext in ('pdf','png'):
        out=Path(__file__).resolve().with_suffix('.'+ext)
        fig.savefig(out,dpi=300,facecolor='white')
        print(out)
    plt.close(fig)
