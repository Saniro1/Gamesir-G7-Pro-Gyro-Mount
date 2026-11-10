"""Render successive installed assemblies in a common frame; no controller mesh is implied."""
from pathlib import Path
import numpy as np,trimesh,argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
parser=argparse.ArgumentParser()
parser.add_argument('--latest',type=int,choices=[24,25,26,27,28],default=28)
args=parser.parse_args()
r=Path(__file__).resolve().parents[1]
versions=[args.latest-1,args.latest]
fig=plt.figure(figsize=(12,9),facecolor='#f6f7f9')
for i,v in enumerate(versions,1):
 ax=fig.add_subplot(1,2,i,projection='3d',facecolor='#f6f7f9')
 shift=np.array([0,-30 if v>=27 else -40,{24:8,25:3,26:-7.0285,27:-7.0285,28:-7.0285}[v]]) if v>=24 else np.zeros(3)
 for part,color in [('g7_mount','#436c85'),('box','#d6a64c'),('lid','#edd095'),('lock_key','#d96c42')]:
  m=trimesh.load_mesh(r/'printable'/f'G7_Modular_v{v}_{part}.stl')
  if part in ['box','lid']:m.apply_translation(np.array([12.5,64.2,29.8])+shift)
  if part=='lock_key':m.apply_translation(np.array([11.5,61.4,23.7])+shift)
  q=m.vertices.copy();m.vertices=np.column_stack([q[:,0],q[:,2],-q[:,1]])
  ax.add_collection3d(Poly3DCollection(m.triangles,facecolors=color,edgecolors='none'))
 ax.set(xlim=(-5,30),ylim=(-10,68),zlim=(-82,12));ax.set_box_aspect((35,78,94));ax.view_init(elev=12,azim=-42);ax.set_axis_off()
 ax.set_title(f'V{v}'+(' — previous' if i==1 else (' — 40 mm higher dock' if args.latest==24 else (' — 5 mm closer, curved bridge' if args.latest==25 else (' — receiver inset 5 mm' if args.latest==26 else (' — box lowered 10 mm' if args.latest==27 else ' — rounded flowing curve'))))),fontsize=14)
fig.suptitle('G7 Pro attachment revision',fontsize=22,fontweight='bold')
fig.text(.5,.10,('V24: 9 mm clips, dock raised 40 mm, 8 mm outward clearance.' if args.latest==24 else ('V25: curved transitions restored; bridge and dock 5 mm closer to the shell.\nThe 9 mm clips, 40 mm raised height and existing Box 2 interface are retained.' if args.latest==25 else ('V26: receiver face sits 5 mm inward of the main-base outer reference.\nBase depth, 9 mm clips and 40 mm raised mounting height are retained.' if args.latest==26 else ('V27: box lowered 10 mm with a longer, gentler curve and more insertion room.\nThe 9 mm clips, 5 mm receiver inset and thin straight print supports are retained.' if args.latest==27 else 'V28: rounded crown, smooth shared tangent and consistent thickness through the return.\nBox position, 9 mm clips, 5 mm inset and insertion clearance remain unchanged.')))),ha='center',fontsize=12,color='#394b5e')
fig.text(.5,.04,'CAD comparison only. Physical controller fit and strength still need testing.',ha='center',fontsize=11,color='#536476')
fig.subplots_adjust(top=.9,bottom=.18,wspace=.02)
fig.savefig(r/'docs'/f'V{args.latest}_comparison.png',dpi=160,bbox_inches='tight',facecolor=fig.get_facecolor())
