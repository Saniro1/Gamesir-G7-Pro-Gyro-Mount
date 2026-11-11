"""Actual V33/V34 mount side projections and measured additional inward tilt."""
from pathlib import Path
import numpy as np,trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from design_frames import dock_tilt,transform_points
root=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(1,2,figsize=(12,7),sharex=True,sharey=True)
points=np.array([[1.25,18.8,21.5215],[1.25,44.6,21.5215]])
old=transform_points(points,dock_tilt(33));new=transform_points(points,dock_tilt(34))
for ax,v in zip(axes,[33,34]):
 for part,col in [('g7_mount','#455969'),('box','#d5ab64')]:
  m=trimesh.load_mesh(root/f'printable/G7_Modular_v{v}_{part}.stl')
  if part=='box':m.apply_translation([12.5,34.2,22.7715]);m.apply_transform(dock_tilt(v))
  ax.add_collection(PolyCollection(m.triangles[:,:,[2,1]],facecolor=col,edgecolor='none'))
 face=transform_points(points,dock_tilt(v));ax.plot(face[:,2],face[:,1],color='#087f8c',lw=3);ax.scatter(face[:,2],face[:,1],color='#087f8c',s=25,zorder=5)
 ax.set(title=f'V{v} — '+('previous inclination' if v==33 else 'lower edge another 5 mm inward'),xlabel='Outward from controller → Z (mm)',xlim=(-10,58),ylim=(66,-13),aspect='equal');ax.grid(alpha=.15)
axes[0].set_ylabel('Down the controller → Y (mm)')
ax=axes[1];ax.plot(old[:,2],old[:,1],'--',color='#087f8c',alpha=.6)
ax.annotate('',xy=(new[1,2],new[1,1]),xytext=(old[1,2],new[1,1]),arrowprops=dict(arrowstyle='<->',color='#b64522',lw=2))
ax.text(17.3,new[1,1]+1,'5 mm additional',color='#b64522',fontsize=10)
ax.annotate('Upper edge fixed',xy=(new[0,2],new[0,1]),xytext=(29,8),arrowprops=dict(arrowstyle='->'),fontsize=10)
fig.suptitle('V34 — bring the lower mount closer to the controller',fontsize=16)
fig.text(.5,.035,'Dark: mount • Tan: unchanged Box 2 • Teal: receiver face\nController shell is not modeled; the photo cannot establish exact clearance.',ha='center',fontsize=10)
fig.tight_layout(rect=(0,.10,1,.94));fig.savefig(root/'docs/V34_mount_tilt.png',dpi=160)
