"""V32: tighter lid, no transverse receiver key slot; preserve USB access."""
from pathlib import Path
import os,subprocess,tempfile,shutil
import trimesh,numpy as np
from design_frames import dock_tilt
root=Path(__file__).resolve().parents[1]
for part in ['box','male_fit_coupon','hook_fit_coupon']:
 shutil.copy2(root/f'printable/G7_Modular_v31_{part}.stl',root/f'printable/G7_Modular_v32_{part}.stl')
with tempfile.TemporaryDirectory() as tmp:
 for part in ['lid','slot_fill']:
  out=Path(tmp)/f'{part}.stl'
  subprocess.run(['openscad','--hardwarnings','--export-format','binstl','-o',str(out),'-D',f'part="{part}"',str(root/'cad/G7_Pro_Modular_v32.scad')],env=dict(os.environ,QT_QPA_PLATFORM='offscreen'),check=True)
  if part!='slot_fill':shutil.copy2(out,root/f'printable/G7_Modular_v32_{part}.stl')
  else:
   patch=trimesh.load_mesh(out);patch.vertices=np.round(patch.vertices,5)
   receiver=trimesh.load_mesh(root/'printable/G7_Modular_v31_universal_receiver.stl');receiver.vertices=np.round(receiver.vertices,5)
   receiver=trimesh.boolean.union([receiver,patch],engine='manifold')
   receiver.export(root/'printable/G7_Modular_v32_universal_receiver.stl')
   patch.apply_translation([11.5,31.4,16.6715])
   mount=trimesh.load_mesh(root/'printable/G7_Modular_v31_g7_mount.stl')
   mount.apply_transform(np.linalg.inv(dock_tilt(32)))
   # Canonicalize the rotated receiver's float32 coplanar surfaces before union.
   vertices=mount.vertices.copy();mask=vertices[:,1]>18
   vertices[mask]=np.round(vertices[mask],5);mount.vertices=vertices
   mount=trimesh.boolean.union([mount,patch],engine='manifold')
   mount.apply_transform(dock_tilt(32))
   assert mount.is_watertight and len(mount.split())==1
   target=root/'printable/G7_Modular_v32_g7_mount.stl'
   mount.export(target)
   final=trimesh.load_mesh(target)
   assert final.is_watertight and final.is_winding_consistent and len(final.split())==1
