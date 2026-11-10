"""Robust manifold union: CGAL cannot reliably union the rotated imported receiver."""
from pathlib import Path
import tempfile, subprocess, os
import trimesh, argparse
p=argparse.ArgumentParser();p.add_argument("--design-version",type=int,choices=[29,30],default=29);version=p.parse_args().design_version
root=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    parts=[]
    for part in ('hook','links','receiver'):
        path=Path(tmp)/(part+'.stl')
        subprocess.run(['openscad','--hardwarnings','--export-format','binstl','-o',str(path),'-D',f'part="build_{part}"',str(root/f'cad/G7_Pro_Modular_v{version}.scad')],env=dict(os.environ,QT_QPA_PLATFORM='offscreen'),check=True)
        mesh=trimesh.load_mesh(path)
        assert mesh.is_watertight
        parts.append(mesh)
    mesh=trimesh.boolean.union(parts,engine='manifold')
    assert mesh.is_watertight and len(mesh.split())==1
    mesh.export(root/f'printable/G7_Modular_v{version}_g7_mount.stl')
