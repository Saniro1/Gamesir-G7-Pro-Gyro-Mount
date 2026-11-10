"""V31 actual disposable sheets and example single-bead sliced layer."""
from pathlib import Path
import json,re
import numpy as np,trimesh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.collections import LineCollection
import argparse
p=argparse.ArgumentParser();p.add_argument('--workdir',type=Path,required=True);p.add_argument('--design-version',type=int,choices=[31,32],default=32);args=p.parse_args()
root=Path(__file__).resolve().parents[1];folder=root/f'slicer/Snapmaker_U1_IEMAI_Matte_PETG_Black_0.4_V{args.design_version}'
fig=plt.figure(figsize=(13,7),facecolor='#f7f8fa')
for i,part in enumerate(['g7_mount','box']):
 ax=fig.add_subplot(1,3,i+1,projection='3d')
 shells=sorted(trimesh.load_mesh(args.workdir/'models'/f'{part}.stl').split(),key=lambda s:s.volume,reverse=True)
 ax.add_collection3d(Poly3DCollection(shells[0].triangles,facecolor='#647282',edgecolor='none',alpha=.22))
 for m in shells[1:]:ax.add_collection3d(Poly3DCollection(m.triangles,facecolor='#df8a20',edgecolor='none',alpha=1))
 b=trimesh.util.concatenate(shells).bounds
 ax.set(xlim=(b[0,0]-2,b[1,0]+2),ylim=(b[0,1]-2,b[1,1]+2),zlim=(0,b[1,2]+1));ax.set_box_aspect(b[1]-b[0]+[4,4,1]);ax.set_axis_off();ax.view_init(elev=24,azim=-58)
 ax.set_title(('Bracket' if i==0 else 'Box 2')+f'\n{len(shells)-1} separate peel sections',fontsize=12)
ax=fig.add_subplot(1,3,3)
# Extrusions at a real 10.12 mm layer near the bracket, not an invented diagram.
pos=np.zeros(3);segments=[];colors=[]
records=json.loads((folder/'peel_sheets_manifest.json').read_text())['parts']['g7_mount']['sheets']
for line in (args.workdir/'validation/plate_2.gcode').read_text().splitlines():
 code=line.split(';')[0]
 if not re.match(r'^G[01]\s',code):continue
 values={k:float(v) for k,v in re.findall(r'([XYZE])(-?[0-9.]+)',code)};new=pos.copy()
 for j,k in enumerate('XYZ'):
  if k in values:new[j]=values[k]
 if values.get('E',0)>0 and abs(new[2]-10.12)<.01 and np.linalg.norm(new[:2]-pos[:2])>.02 and new[0]<72:
  segments.append([pos[:2],new[:2]])
  mid=(new+pos)/2
  is_sheet=any(abs(mid[0]-45-r['x_mm'])<.12 and 100+r['bounds_mm'][0][1]<mid[1]<100+r['bounds_mm'][1][1] for r in records)
  colors.append('#ce7c18' if is_sheet else '#647282')
 pos=new
ax.add_collection(LineCollection(segments,colors=colors,linewidths=1.5));ax.autoscale();ax.set_aspect('equal');ax.set_title('Actual bracket extrusion paths\nat Z = 10.12 mm',fontsize=12);ax.set_xlabel('X (mm)');ax.set_ylabel('Y (mm)');ax.grid(alpha=.15)
fig.suptitle(f'V{args.design_version} — thin, separate sheets to peel away individually',fontsize=18)
fig.text(.5,.05,'Amber: disposable sheets • Transparent gray: accessory\n0.45 mm sheets • 0.32 mm top air gap • no shared raft or dense support roof\nMesh and G-code checks only; physical removal force has not been tested.',ha='center',fontsize=11)
fig.tight_layout(rect=(0,.17,1,.93));fig.savefig(folder/'peel_sheet_preview.png',dpi=160,facecolor=fig.get_facecolor())
