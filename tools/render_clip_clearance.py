"""Compare actual insertion-section mesh outlines; dimensions are in mm."""
from pathlib import Path
import trimesh,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
root=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(1,2,figsize=(12,5))
for v,col in [(29,'#aab3ba'),(30,'#087f8c')]:
 m=trimesh.load_mesh(root/'printable'/f'G7_Modular_v{v}_hook_fit_coupon.stl')
 for ax,normal,origin,dims in [(axes[0],[0,0,1],[0,0,-3],[0,1]),(axes[1],[0,1,0],[0,0,0],[0,2])]:
  lines=trimesh.intersections.mesh_plane(m,normal,origin)
  ax.add_collection(LineCollection(lines[:,:,dims],colors=col,lw=2,label=f'V{v}'))
axes[0].set(xlim=(-.5,5),ylim=(-3,2),xlabel='X width (mm)',ylabel='Y thickness (mm)',title='Insertion section: 0.5 mm off each face')
axes[1].set(xlim=(-.5,5),ylim=(-8,3),xlabel='X width (mm)',ylabel='Z insertion length (mm)',title='Length remains 9 mm')
for ax in axes:ax.set_aspect('equal');ax.grid(alpha=.2);ax.legend()
fig.suptitle('Left controller clip — actual mesh sections; right clip receives the same reduction')
fig.tight_layout();fig.savefig(root/'docs/V30_clip_clearance.png',dpi=160)
