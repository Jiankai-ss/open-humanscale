"""Render figures from the supplied evaluation snapshots; no inferred scores."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = json.loads((ROOT / 'article-03-evidence.json').read_text())
OUT = ROOT / 'dist' / 'assets'
COLORS = ['#b78052', '#42658c']
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12,
                     'axes.labelcolor': '#41505a', 'text.color': '#253541',
                     'xtick.color': '#41505a', 'ytick.color': '#6d777b',
                     'svg.fonttype': 'none'})

def style(ax, ymax, ylabel):
    ax.set_ylim(0, ymax)
    ax.set_ylabel(ylabel, labelpad=10)
    ax.spines[['top', 'right', 'left']].set_visible(False)
    ax.spines['bottom'].set_color('#dfe3e7')
    ax.tick_params(axis='both', length=0, pad=9)
    ax.yaxis.grid(True, color='#e8edf0', linewidth=0.8)
    ax.set_axisbelow(True)

def bars(ax, values, labels, ymax, ylabel, title, fmt, colors=COLORS):
    style(ax, ymax, ylabel)
    positions = list(range(len(values)))
    ax.bar(positions, values, width=.54, color=colors, zorder=3)
    ax.set_xticks(positions, labels)
    ax.set_xlim(-.65, len(values)-.35)
    ax.set_title(title, fontsize=16, loc='left', pad=26, fontweight='bold')
    for x, val in enumerate(values):
        ax.text(x, val+ymax*.025, fmt.format(val), ha='center', fontsize=18 if len(values)>2 else 21,
                color=colors[x], fontweight='bold')

fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
labels = ['By data amount', 'Balanced 1:1']
bars(axes[0], [DATA[k]['average_success_percent'] for k in ['uniform','balanced']],
     labels, 20, 'Mean success (%)', 'Overall success', '{:.2f}%')
bars(axes[1], [len(DATA[k]['covered_tasks']) for k in ['uniform','balanced']],
     labels, 50, 'Covered tasks / 50', 'Task coverage (mean success ≥ 2%)', '{:.0f}')
fig.subplots_adjust(left=.075, right=.98, top=.78, bottom=.19, wspace=.32)
fig.savefig(OUT/'a3-success-coverage.svg', facecolor='white')
fig.savefig(OUT/'a3-success-coverage.png', dpi=180, facecolor='white')
plt.close(fig)

fig, ax = plt.subplots(figsize=(6.3, 4.8))
labels = ['Balanced', 'Two-stage']
v3 = DATA['posttraining']['qpos_v3']
bars(ax, [max(x['average'] for x in v3 if x['recipe']==k)
              for k in ['balanced','two_stage']], labels,
     100, 'Mean success (%)', 'qpos post-training', '{:.2f}%', ['#42658c','#8c688f'])
fig.subplots_adjust(left=.16, right=.96, top=.78, bottom=.19)
fig.savefig(OUT/'a3-qpos-posttraining.svg', facecolor='white')
fig.savefig(OUT/'a3-qpos-posttraining.png', dpi=180, facecolor='white')
plt.close(fig)

# Compare the same two recipes before and after target-task adaptation.
# The two-stage zero-shot evaluation is an explicitly labelled partial snapshot.
fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
comparison_colors = ['#42658c', '#8c688f']
bars(axes[0], [DATA['balanced']['average_success_percent'],
               DATA['two_stage_zeroshot']['average_success_percent']],
     ['Balanced', 'Two-stage*'], 20, 'Mean success (%)',
     'RoboTwin zero-shot', '{:.2f}%', comparison_colors)
bars(axes[1], [max(x['average'] for x in v3 if x['recipe']==k)
              for k in ['balanced', 'two_stage']],
     ['Balanced', 'Two-stage'], 100, 'Mean success (%)',
     'qpos post-training', '{:.2f}%', comparison_colors)
fig.subplots_adjust(left=.075, right=.98, top=.78, bottom=.24, wspace=.32)
fig.text(.075, .045, '* Two-stage zero-shot: 4,989 / 5,000 scored; evaluation in progress.',
         fontsize=10, color='#6d777b')
fig.savefig(OUT/'a3-zero-posttraining.svg', facecolor='white')
fig.savefig(OUT/'a3-zero-posttraining.png', dpi=180, facecolor='white')
plt.close(fig)
print('Rendered article 3 figures from article-03-evidence.json')
