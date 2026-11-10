"""Draw measured receiver/base face references from the exported V25/V26 CAD."""
from pathlib import Path
import numpy as np,trimesh,matplotlib,argparse
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Patch
parser=argparse.ArgumentParser()
parser.add_argument('--latest',type=int,choices=[26,27,28],default=28)
args=parser.parse_args()
r=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(1,2,figsize=(14,7),facecolor='#f6f7f9')
for ax,v in zip(axes,[args.latest-1,args.latest]):
 shift=np.array([0,-30 if v>=27 else -40,3 if v==25 else -7.0285])
 hook=trimesh.load_mesh(r/'printable'/f'G7_Modular_v{v}_hook_fit_coupon.stl')
 face=float(hook.bounds[1,2]);dock_face=28.55+shift[2]
 ax.set_facecolor('#f6f7f9')
 for part,color in [('g7_mount','#436c85'),('box','#d6a64c'),('lid','#edd095'),('lock_key','#d96c42')]:
  m=trimesh.load_mesh(r/'printable'/f'G7_Modular_v{v}_{part}.stl')
  if part in ['box','lid']:m.apply_translation(np.array([12.5,64.2,29.8])+shift)
  if part=='lock_key':m.apply_translation(np.array([11.5,61.4,23.7])+shift)
  ax.add_collection(PolyCollection(m.triangles[:,:,[2,1]],facecolor=color,edgecolor='none'))
 ax.axvline(face,color='#394b5e',ls='--',lw=1.3)
 ax.axvline(dock_face,color=('#b34d31' if v==25 else '#287b50'),ls=':',lw=1.6)
 ax.annotate('',xy=(dock_face,-7),xytext=(face,-7),arrowprops=dict(arrowstyle='<->',color='#202b37',lw=1.5))
 ax.text((face+dock_face)/2,-8.5,f'{abs(face-dock_face):.2f} mm '+('outward' if v==25 else 'inward'),ha='center',fontsize=11)
 ax.set(xlim=(-10,68),ylim=(52,-12),xlabel='Outward depth (CAD Z, mm)',ylabel='Controller down (CAD Y, mm)')
 ax.set_aspect('equal');ax.grid(alpha=.15)
 ax.set_title(f'V{v}: '+('receiver outside base' if v==25 else ('receiver inset' if v==26 else ('lower box, gentler curve' if v==27 else 'rounded flowing curve'))),fontsize=15)
 if args.latest>=27:
  box_top=64.2+shift[1]-17.5;bridge_end=hook.bounds[1,1]
  ax.annotate('',xy=(57,box_top),xytext=(57,bridge_end),arrowprops=dict(arrowstyle='<->',color='#287b50'))
  ax.text(58,(bridge_end+box_top)/2,f'{box_top-bridge_end:.1f} mm\ngap',va='center',fontsize=10)
  ax.plot([dock_face,57],[bridge_end,bridge_end],color='#287b50',lw=.7,ls=':')
  ax.plot([48.42,57],[box_top,box_top],color='#287b50',lw=.7,ls=':')
fig.suptitle('Rounded transition, unchanged box position' if args.latest==28 else 'Receiver depth relative to the main base',fontsize=20,fontweight='bold')
fig.legend(handles=[Patch(color='#436c85',label='Bracket'),Patch(color='#d6a64c',label='Box 2'),Patch(color='#edd095',label='Lid')],loc='lower center',ncol=3,bbox_to_anchor=(.5,.09),frameon=False)
fig.text(.5,.035,'Dashed line: main-base outer reference. Dotted line: receiver box-facing surface.\nDimensions are from CAD; actual controller-shell clearance still needs a physical check.',ha='center',fontsize=11,color='#465467')
fig.tight_layout(rect=(0,.16,1,.92))
fig.savefig(r/'docs'/f'V{args.latest}_receiver_inset.png',dpi=160,bbox_inches='tight',facecolor=fig.get_facecolor())
