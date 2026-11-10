"""Render oriented meshes and actual support toolpaths. Optional: matplotlib 3.10.8."""
from pathlib import Path
import argparse,json,re
import numpy as np,trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection

parser=argparse.ArgumentParser()
parser.add_argument('--workdir',type=Path,required=True)
parser.add_argument('--design-version',type=int,choices=[23,24,25,26],default=26)
args=parser.parse_args()
repo=Path(__file__).resolve().parents[1]
plates=json.loads((args.workdir/'assemble.json').read_text())['plates']
fig=plt.figure(figsize=(14,10),facecolor='#f6f7f9')
for index,plate in enumerate(plates,1):
 ax=fig.add_subplot(2,1,index,projection='3d',facecolor='#f6f7f9')
 # Plot the actual support/brim extrusion centerlines, not imagined scaffolds.
 g=(args.workdir/'validation'/f'plate_{index}.gcode').read_text()
 position=np.zeros(3);feature='';segments=[]
 for line in g.splitlines():
  if line.startswith(';TYPE:'):feature=line[6:].strip()
  code=line.split(';')[0].strip()
  if not re.match(r'^G[01]\s',code):continue
  values={k:float(v) for k,v in re.findall(r'([XYZE])(-?[0-9.]+)',code)}
  new=position.copy()
  for i,k in enumerate('XYZ'):
   if k in values:new[i]=values[k]
  if (feature.startswith('Support') or feature=='Brim') and values.get('E',0)>0 and not np.array_equal(position,new):
   segments.append([position.copy(),new.copy()])
  position=new
 ax.add_collection3d(Line3DCollection(segments,colors='#dc8d26',linewidths=.45,alpha=.7))
 for obj in plate['objects']:
  m=trimesh.load_mesh(obj['path']);m.apply_translation([obj['pos_x'][0],obj['pos_y'][0],0])
  ax.add_collection3d(Poly3DCollection(m.triangles,facecolors='#343e4c',edgecolors='none',alpha=.92))
 ax.set(xlim=(30,232),ylim=(85,148),zlim=(0,85))
 ax.set_box_aspect((202,63,85));ax.view_init(elev=19,azim=-70);ax.set_axis_off()
 ax.set_title(plate['plate_name'],fontsize=14,pad=0)
fig.suptitle('G7 Pro · U1 PLA Black · revised print orientations',fontsize=20,fontweight='bold',y=.97)
fig.text(.5,.055,'Dark: model geometry   •   Amber: actual sliced supports and brims\nCAD/toolpath preview only — physical fit and print performance still require testing',ha='center',fontsize=11,color='#465467')
fig.subplots_adjust(top=.91,bottom=.12,hspace=.12)
fig.savefig(repo/'slicer'/('Snapmaker_U1_PLA_Black_0.4' if args.design_version==23 else f'Snapmaker_U1_PLA_Black_0.4_V{args.design_version}')/'support_preview.png',dpi=160,facecolor=fig.get_facecolor(),bbox_inches='tight')
