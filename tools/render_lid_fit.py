"""V32: actual mesh sections showing closer lid fit and the filled receiver slot."""
from pathlib import Path
import trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
root=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(1,2,figsize=(12,5))
for part,v,color,label in [('box',32,'#c18b35','Box rail'),('lid',31,'#adb5bd','Previous lid'),('lid',32,'#087f8c','Tighter lid')]:
 m=trimesh.load_mesh(root/f'printable/G7_Modular_v{v}_{part}.stl');lines=trimesh.intersections.mesh_plane(m,[0,1,0],[0,-3,0])
 axes[0].add_collection(LineCollection(lines[:,:,[0,2]],colors=color,lw=2,label=label))
axes[0].set(xlim=(-15.8,-12.3),ylim=(20.9,26),xlabel='X (mm)',ylabel='Z (mm)',title='Left lid rail at a friction pad')
axes[0].annotate('Small local preload\n0.03 mm nominal',xy=(-14.335,22.2),xytext=(-13.9,24.9),arrowprops=dict(arrowstyle='->'),fontsize=9)
for v,color,label in [(31,'#adb5bd','Previous key slot'),(32,'#087f8c','Filled slot')]:
 m=trimesh.load_mesh(root/f'printable/G7_Modular_v{v}_universal_receiver.stl');lines=trimesh.intersections.mesh_plane(m,[1,0,0],[-9,0,0])
 axes[1].add_collection(LineCollection(lines[:,:,[1,2]],colors=color,lw=2,label=label))
axes[1].set(xlim=(9.5,13.6),ylim=(-.3,5.2),xlabel='Receiver Y (mm)',ylabel='Receiver Z (mm)',title='Receiver side wall: key slot removed')
for ax in axes:ax.set_aspect('equal');ax.grid(alpha=.15);ax.legend(loc='lower left',fontsize=9)
fig.suptitle('V32 — closer lid fit, keyless receiver, USB access preserved',fontsize=16)
fig.text(.5,.02,'Actual exported mesh sections • Physical friction and retention still require a test print.',ha='center',fontsize=10)
fig.tight_layout(rect=(0,.06,1,.93));fig.savefig(root/'docs/V32_lid_fit.png',dpi=160)
