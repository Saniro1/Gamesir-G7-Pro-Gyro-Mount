"""Rebuild smooth lower links into a more inclined keyless receiver."""
from pathlib import Path
import tempfile,subprocess,os,shutil
import trimesh
root=Path(__file__).resolve().parents[1]
for part in ['box','lid','universal_receiver','male_fit_coupon','hook_fit_coupon']:
 shutil.copy2(root/f'printable/G7_Modular_v33_{part}.stl',root/f'printable/G7_Modular_v34_{part}.stl')
with tempfile.TemporaryDirectory() as tmp:
 components=[]
 for part in ['hook','links','receiver']:
  path=Path(tmp)/(part+'.stl')
  subprocess.run(['openscad','--hardwarnings','--export-format','binstl','-o',str(path),'-D',f'part="build_{part}"',str(root/'cad/G7_Pro_Modular_v34.scad')],env=dict(os.environ,QT_QPA_PLATFORM='offscreen'),check=True)
  mesh=trimesh.load_mesh(path);assert mesh.is_watertight;components.append(mesh)
 mount=trimesh.boolean.union(components,engine='manifold')
 assert mount.is_watertight and len(mount.split())==1
 target=root/'printable/G7_Modular_v34_g7_mount.stl';mount.export(target)
 mount=trimesh.load_mesh(target)
 assert mount.is_watertight and mount.is_winding_consistent and len(mount.split())==1
