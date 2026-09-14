"""Review-level PICO-S boundary decisions. Export editable PDF and 300-dpi PNG."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

INK, GRAY = '#2B2B2B', '#6B6B6B'
INDIGO, INDIGO_FILL = '#5367A6', '#E8EBF6'
TERRACOTTA, TERRACOTTA_FILL = '#B45F45', '#F7E8E2'
TEAL = '#3F6B73'
TEAL_STANDARD_FILL, TEAL_OPTIONAL_FILL = '#DCEAEC', '#EEF4F5'

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
    text(.3,5.56,'A',16,'bold',ha='left',va='top')
    text(.62,5.5,'From review question to\neligibility criteria',14,ha='left',va='top')
    text(3.755,5.56,'B',16,'bold',ha='left',va='top')
    text(4.075,5.5,'Group interventions or\nanalyze them separately?',14,ha='left',va='top')
    text(8.2,5.56,'C',16,'bold',ha='left',va='top')
    text(8.52,5.5,'How should co-interventions\naffect study eligibility?',14,ha='left',va='top')

    # Panel A: the vertical review-definition flow.
    box(2,4.25,2.4,.68,'Review question',size=14)
    arrow(2,3.89,2,3.55)
    box(2,3.18,2.4,.68,'Review-level\nPICO-S',size=14)
    arrow(2,2.82,2,2.48)
    box(2,2.11,2.4,.68,'Eligibility criteria',size=14)

    # Panel B: lumper-splitter choices for intervention classes.
    for x,s in [(4.65,'Fluoxetine'),(6,'Paroxetine'),(7.35,'Sertraline')]:
        box(x,4.3,1.15,.48,s,size=10.5)
        arrow(x,4.04,6+(x-6)*.25,3.55,INDIGO)
    text(4.075,3.75,'Lumper',12,'bold',INDIGO,ha='left')
    box(6,3.2,3.85,.62,'Newer-generation antidepressants',INDIGO_FILL,INDIGO,10.5)
    text(6,2.71,'One intervention class; pooled class estimate',10.5)
    text(4.075,2.30,'Splitter',12,'bold',TERRACOTTA,ha='left')
    for x,s in [(4.65,'Fluoxetine'),(6,'Paroxetine'),(7.35,'Sertraline')]:
        box(x,1.82,1.15,.48,s,TERRACOTTA_FILL,TERRACOTTA,10.5)
    text(4.075,1.40,'Separate compound-level estimates',10.5,ha='left')

    # Panel C: context-dependent co-intervention rules.
    text(8.52,4.72,'Co-intervention is standard',12.5,'bold',TEAL,ha='left')
    box(10.195,4.14,3.35,.7,'Smoking-cessation behavioral support\n+ pharmacotherapy',TEAL_STANDARD_FILL,TEAL,10.5)
    arrow(10.195,3.78,10.195,3.43,TEAL)
    text(8.52,3.23,'Excluding combination studies would\nomit most relevant evidence',10.5,ha='left')
    text(8.52,2.72,'Co-intervention is optional',12.5,'bold',TEAL,ha='left')
    box(10.195,2.17,3.35,.7,'Antidepressant medication\n± psychotherapy',TEAL_OPTIONAL_FILL,TEAL,11.5)
    arrow(10.195,1.81,10.195,1.46,TEAL)
    text(8.52,1.21,'Restricting eligibility to studies of\nthe intervention alone may yield\na cleaner effect estimate',10.5,ha='left')
    return fig

if __name__ == '__main__':
    fig=build_figure()
    for ext in ('pdf','png'):
        out=Path(__file__).resolve().with_suffix('.'+ext)
        fig.savefig(out,dpi=300,facecolor='white')
        print(out)
    plt.close(fig)
