"""Actual V28/V29 mesh side views with measured receiver-face datums."""
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
for ax,v in zip(axes,[28,29]):
 for part,col in [('g7_mount','#455969'),('box','#d5ab64')]:
  m=trimesh.load_mesh(root/'printable'/f'G7_Modular_v{v}_{part}.stl')
  if part=='box':
   m.apply_translation([12.5,34.2,22.7715]);m.apply_transform(dock_tilt(v))
  # horizontal is outward Z, vertical is controller-down Y.
  ax.add_collection(PolyCollection(m.triangles[:,:,[2,1]],facecolor=col,edgecolor='none',alpha=1))
 face=transform_points(points,dock_tilt(v))
 ax.plot(face[:,2],face[:,1],color='#087f8c',lw=3)
 ax.scatter(face[:,2],face[:,1],color='#087f8c',s=25,zorder=5)
 ax.set(title=f'V{v} — '+('previous position' if v==28 else 'bottom 5 mm inward'),xlabel='Outward from controller → Z (mm)',xlim=(-10,58),ylim=(65,-13),aspect='equal')
 ax.grid(alpha=.15)
axes[0].set_ylabel('Down the controller → Y (mm)')
ax=axes[1]
ax.plot([21.5215,21.5215],[18.8,44.6],'--',color='#087f8c',alpha=.5)
end=transform_points(points,dock_tilt(29))[1]
ax.annotate('',xy=(end[2],end[1]),xytext=(21.5215,end[1]),arrowprops=dict(arrowstyle='<->',color='#b64522',lw=2))
ax.text(22.3,end[1]+2,'5 mm',color='#b64522')
ax.annotate('Fixed upper edge\n11.17° inward tilt',xy=(21.5215,18.8),xytext=(28,8),arrowprops=dict(arrowstyle='->'),fontsize=10)
fig.suptitle('G7 Pro slider: fixed top, lower edge closer to the controller',fontsize=15)
fig.text(.5,.035,'Side projections of exported meshes • Dark: bracket • Tan: Box 2 • Teal: receiver face\nController shell is not modeled; verify physical clearance before loading.',ha='center',fontsize=10)
fig.tight_layout(rect=(0,.10,1,.94))
fig.savefig(root/'docs/V29_slider_tilt.png',dpi=160)
