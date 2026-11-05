"""Optional documentation render: pip install matplotlib==3.10.8."""
from pathlib import Path
import numpy as np
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

root = Path(__file__).resolve().parents[1]
parts = {p: trimesh.load_mesh(root/'printable'/f'G7_Modular_v23_{p}.stl')
         for p in ('g7_mount', 'box', 'lid', 'lock_key')}
colors = {'g7_mount':'#416b86', 'box':'#d9a94e', 'lid':'#f0d697', 'lock_key':'#df6c45'}
fig = plt.figure(figsize=(15, 7), facecolor='#f7f8fa')
for i, up in enumerate((False, True)):
    ax = fig.add_subplot(1,3,i+1,projection='3d', facecolor='#f7f8fa')
    for p, original in parts.items():
        m=original.copy()
        if p in ('box','lid'):
            m.apply_translation([12.5,64.2,29.8])
            if up: m.vertices[:,:2]=2*np.array([11.5,61.4])-m.vertices[:,:2]
        if p=='lock_key':m.apply_translation([11.5,61.4,23.7])
        ax.add_collection3d(Poly3DCollection(m.triangles, facecolors=colors[p], edgecolors='#263848', linewidths=.07, alpha=1))
    ax.set(xlim=(-5,30),ylim=(-10,85),zlim=(-10,60))
    ax.set_box_aspect((35,95,70));ax.view_init(elev=25,azim=-45);ax.set_axis_off()
    ax.set_title('USB opening '+('up' if up else 'down'), fontsize=14)
ax = fig.add_subplot(1,3,3,projection='3d', facecolor='#f7f8fa')
m=parts['lock_key']
ax.add_collection3d(Poly3DCollection(m.triangles,facecolors=colors['lock_key'],edgecolors='#733b27',linewidths=.25))
lo,hi=m.bounds
ax.set(xlim=(lo[0]-1,hi[0]+1),ylim=(lo[1]-1,hi[1]+1),zlim=(lo[2]-.5,hi[2]+.5))
ax.set_box_aspect(hi-lo+[2,2,1]);ax.view_init(elev=20,azim=-65);ax.set_axis_off()
ax.set_title('V23 key: flexible tongue',fontsize=14)
fig.suptitle('G7 Pro modular mount | V23 prototype',fontsize=22,fontweight='bold',y=.94)
fig.text(.5,.08,'CAD geometry only • Controller fit, printing tolerances and latch strength require physical testing',ha='center',fontsize=12,color='#455569')
fig.savefig(root/'docs'/'V23_preview.png',dpi=150,bbox_inches='tight',facecolor=fig.get_facecolor())
