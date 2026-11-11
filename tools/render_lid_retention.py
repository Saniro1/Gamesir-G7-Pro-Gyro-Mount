"""Actual V32/V33 cap sections at the rail hooks."""
from pathlib import Path
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
root=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(1,2,figsize=(11,5))
for ax,limits in zip(axes,[(-15.7,-12.7),(10.7,13.7)]):
 for part,version,color,label in [('box',33,'#b98a35','Existing box rail'),('lid',32,'#aeb6bf','V32 lip'),('lid',33,'#087f8c','V33 longer lip')]:
  m=trimesh.load_mesh(root/f'printable/G7_Modular_v{version}_{part}.stl');lines=trimesh.intersections.mesh_plane(m,[0,1,0],[0,-3,0])
  ax.add_collection(LineCollection(lines[:,:,[0,2]],colors=color,lw=2,label=label))
 ax.set(xlim=limits,ylim=(20.9,23.1),xlabel='X (mm)',ylabel='Z (mm)',aspect='equal');ax.grid(alpha=.15);ax.legend(loc='upper center',fontsize=9)
axes[0].annotate('',xy=(-13.23,21.3),xytext=(-13.83,21.3),arrowprops=dict(arrowstyle='<->',color='#b54c22',lw=2))
axes[0].text(-13.85,21.02,'+0.60 mm',fontsize=10,color='#b54c22')
axes[0].set_title('Left rail hook');axes[1].set_title('Right rail hook')
fig.suptitle('V33 — retaining lips reach farther under both Box 2 rails',fontsize=16)
fig.text(.5,.045,'Nominal rail overlap: 0.52 → 1.12 mm per side • 0.23 mm clearance to box sidewall\nExported mesh sections; physical retention still requires testing.',ha='center',fontsize=10)
fig.tight_layout(rect=(0,.12,1,.92));fig.savefig(root/'docs/V33_lid_retention.png',dpi=160)
