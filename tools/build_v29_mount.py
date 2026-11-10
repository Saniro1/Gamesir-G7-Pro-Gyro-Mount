"""Robust manifold union: CGAL cannot reliably union the rotated imported receiver."""
from pathlib import Path
import tempfile, subprocess, os
import trimesh
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    parts=[]
    for part in ('hook','links','receiver'):
        path=Path(tmp)/(part+'.stl')
        subprocess.run(['openscad','--hardwarnings','--export-format','binstl','-o',str(path),'-D',f'part="build_{part}"',str(root/'cad/G7_Pro_Modular_v29.scad')],env=dict(os.environ,QT_QPA_PLATFORM='offscreen'),check=True)
        mesh=trimesh.load_mesh(path)
        assert mesh.is_watertight
        parts.append(mesh)
    mesh=trimesh.boolean.union(parts,engine='manifold')
    assert mesh.is_watertight and len(mesh.split())==1
    mesh.export(root/'printable/G7_Modular_v29_g7_mount.stl')
