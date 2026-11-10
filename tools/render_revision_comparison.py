"""Render V23/V24 installed assemblies in a common frame; no controller mesh is implied."""
from pathlib import Path
import numpy as np,trimesh,argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
parser=argparse.ArgumentParser()
parser.add_argument('--latest',type=int,choices=[24,25],default=25)
args=parser.parse_args()
r=Path(__file__).resolve().parents[1]
versions=[23,24] if args.latest==24 else [24,25]
fig=plt.figure(figsize=(12,9),facecolor='#f6f7f9')
for i,v in enumerate(versions,1):
 ax=fig.add_subplot(1,2,i,projection='3d',facecolor='#f6f7f9')
 shift=np.array([0,-40,3 if v==25 else 8]) if v>=24 else np.zeros(3)
 for part,color in [('g7_mount','#436c85'),('box','#d6a64c'),('lid','#edd095'),('lock_key','#d96c42')]:
  m=trimesh.load_mesh(r/'printable'/f'G7_Modular_v{v}_{part}.stl')
  if part in ['box','lid']:m.apply_translation(np.array([12.5,64.2,29.8])+shift)
  if part=='lock_key':m.apply_translation(np.array([11.5,61.4,23.7])+shift)
  q=m.vertices.copy();m.vertices=np.column_stack([q[:,0],q[:,2],-q[:,1]])
  ax.add_collection3d(Poly3DCollection(m.triangles,facecolors=color,edgecolors='none'))
 ax.set(xlim=(-5,30),ylim=(-10,68),zlim=(-82,12));ax.set_box_aspect((35,78,94));ax.view_init(elev=12,azim=-42);ax.set_axis_off()
 ax.set_title(f'V{v}'+(' — previous' if i==1 else (' — 40 mm higher dock' if args.latest==24 else ' — 5 mm closer, curved bridge')),fontsize=14)
fig.suptitle('G7 Pro attachment revision',fontsize=22,fontweight='bold')
fig.text(.5,.10,('V24: 9 mm clips, dock raised 40 mm, 8 mm outward clearance.' if args.latest==24 else 'V25: curved transitions restored; bridge and dock 5 mm closer to the shell.\nThe 9 mm clips, 40 mm raised height and existing Box 2 interface are retained.'),ha='center',fontsize=12,color='#394b5e')
fig.text(.5,.04,'CAD comparison only. Physical controller fit and strength still need testing.',ha='center',fontsize=11,color='#536476')
fig.subplots_adjust(top=.9,bottom=.18,wspace=.02)
fig.savefig(r/'docs'/f'V{args.latest}_comparison.png',dpi=160,bbox_inches='tight',facecolor=fig.get_facecolor())
