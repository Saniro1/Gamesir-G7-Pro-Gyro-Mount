"""Build portable multi-object 3MFs and check actual exported V23/V24/V25 meshes.

Run after tools/build.sh's OpenSCAD exports. No controller/device model exists;
these tests assess printed-part geometry only, not hardware fit or strength.
"""
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import zipfile
import xml.etree.ElementTree as ET
import numpy as np
import trimesh

parser=argparse.ArgumentParser()
parser.add_argument('--design-version',type=int,choices=[23,24,25],default=25)
args=parser.parse_args()
VERSION=args.design_version
SHIFT=np.array([0.,-40.,3. if VERSION==25 else 8.]) if VERSION>=24 else np.zeros(3)
ROOT = Path(__file__).resolve().parents[1]
REPORT=ROOT/'docs'/('validation.json' if VERSION==23 else f'validation_v{VERSION}.json')
REPORT.unlink(missing_ok=True)
PARTS = ('g7_mount', 'box', 'lid', 'lock_key', 'universal_receiver',
         'male_fit_coupon', 'hook_fit_coupon')
M = {p: trimesh.load_mesh(ROOT / 'printable' / f'G7_Modular_v{VERSION}_{p}.stl') for p in PARTS}
TOL = 1e-4  # mm^3; manifold float32 intersection noise
checks = []


def check(name, condition, **evidence):
    checks.append(dict(name=name, passed=bool(condition), **evidence))
    if not condition:
        raise AssertionError(f'{name}: {evidence}')


def translated(mesh, offset):
    mesh = mesh.copy()
    mesh.apply_translation(offset)
    return mesh


def common(a, b):
    return trimesh.boolean.intersection([a, b], engine='manifold')


def overlap(a, b):
    c = common(a, b)
    return float(c.volume) if len(c.faces) else 0.0


def assembly(up=False):
    result = {p: M[p].copy() for p in PARTS[:4]}
    for p in ('box', 'lid'):
        result[p].apply_translation(np.array([12.5, 64.2, 29.8])+SHIFT)
        if up:
            result[p].vertices[:, :2] = 2 * (np.array([11.5, 61.4])+SHIFT[:2]) - result[p].vertices[:, :2]
    result['lock_key'].apply_translation(np.array([11.5, 61.4, 23.7])+SHIFT)
    return result


for p, mesh in M.items():
    check(f'{p}: closed connected positive solid', mesh.is_watertight and mesh.is_winding_consistent
          and len(mesh.split()) == 1 and mesh.volume > 0,
          volume_mm3=float(mesh.volume), bounds_mm=mesh.bounds.tolist(), triangles=len(mesh.faces))

for up in (False, True):
    pose = assembly(up)
    orientation = 'USB_up' if up else 'USB_down'
    for a, b in itertools.combinations(pose, 2):
        v = overlap(pose[a], pose[b])
        check(f'{orientation}: {a}/{b} assembled clearance', v < TOL, overlap_mm3=v)
    # 0.25 mm samples across the entire 40 mm insertion/removal path, key removed.
    for p in ('box', 'lid'):
        values = [overlap(pose['g7_mount'], translated(pose[p], [0, d, 0]))
                  for d in np.arange(0, 40.01, .25)]
        check(f'{orientation}: {p} insertion path', max(values) < TOL,
              samples=len(values), max_overlap_mm3=max(values))
    # With key installed, outward motion must be blocked before rail disengages.
    v = overlap(pose['lock_key'], translated(pose['box'], [0, 1.3, 0]))
    check(f'{orientation}: key blocks withdrawal', v > .1, overlap_mm3=v)
    # No support-arm contact before the new receiver stop. At -0.3 mm, contact
    # must be with the low stop, never the higher support links or enclosure.
    v = overlap(pose['g7_mount'], translated(pose['box'], [0, -.19, 0]))
    check(f'{orientation}: approach to closed stop', v < TOL, overlap_mm3=v)
    hit = common(pose['g7_mount'], translated(pose['box'], [0, -.3, 0]))
    check(f'{orientation}: stop takes contact', len(hit.faces) > 0 and hit.volume > 1
          and hit.bounds[0, 1] >= 51.29+SHIFT[1] and hit.bounds[1, 2] <= 28.56+SHIFT[2],
          overlap_mm3=float(hit.volume), bounds_mm=hit.bounds.tolist())

# Verify the exported portable receiver and mount have the same channel/stop.
receiver = translated(M['universal_receiver'], np.array([11.5, 61.4, 23.7])+SHIFT)
region = trimesh.creation.box(extents=[20.5, 25.8, 4.85])
region.apply_translation(np.array([11.5, 61.7, 26.125])+SHIFT)
cut = common(M['g7_mount'], region)
delta = float(trimesh.boolean.difference([cut,receiver],engine='manifold').volume + trimesh.boolean.difference([receiver,cut],engine='manifold').volume)
check('portable receiver matches integrated receiver', delta < .002, symmetric_difference_mm3=float(delta))


# Inspect material over/under the revised slot in a side wall, outside the
# dovetail channel. This catches a source/export drift back to the thin roof.
probe = trimesh.creation.box(extents=[1, 1, 1])
probe.apply_translation(np.array([2.5, 73.3, 28.25])+SHIFT)
roof_volume = common(M['g7_mount'], probe).volume
check('key slot roof is 0.57 mm thick', abs(roof_volume - .57) < 1e-4,
      measured_thickness_mm=float(roof_volume))
probe = trimesh.creation.box(extents=[1, 1, 2.4])
probe.apply_translation(np.array([2.5, 73.3, 24.9])+SHIFT)
floor_volume = common(M['g7_mount'], probe).volume
check('key slot retains 2.08 mm floor', abs(floor_volume - 2.08) < 1e-4,
      measured_thickness_mm=float(floor_volume))

# Key insertion intentionally requires elastic latch deflection. Test that all
# interference is confined to the flexible tongue, not the rigid bar or grip.
key = assembly()['lock_key']
volumes, hit_bounds = [], []
for d in np.arange(0, 28.01, .25):
    hit = common(M['g7_mount'], translated(key, [d, 0, 0]))
    if len(hit.faces) and hit.volume > TOL:
        volumes.append(float(hit.volume))
        hit_bounds.append(hit.bounds.tolist())
check('key insertion interference confined to flex bump', bool(volumes)
      and all(b[0][2] >= 27.979+SHIFT[2] and b[1][2] <= 28.251+SHIFT[2] for b in hit_bounds),
      max_overlap_mm3=max(volumes, default=0),
      required_tip_deflection_mm=.27, designed_under_tongue_gap_mm=.40)

# Box/lid detents are intentionally NOT zero-interference in motion. Record
# them separately; this is not evidence that a printed snap will flex safely.
lid_motion = [overlap(M['box'], translated(M['lid'], [0, -d, 0]))
              for d in np.arange(0, 35.01, .25)]
check('lid can clear box after sliding toward negative local Y',
      lid_motion[-1] < TOL and max(lid_motion) < .1,
      max_intentional_detent_overlap_mm3=max(lid_motion), samples=len(lid_motion))

# The preserved box cavity, lid and controller contact geometry must not drift.
for p in ('box', 'lid'):
    old = trimesh.load_mesh(ROOT / 'cad' / 'reference' / f'{p}_v22.stl')
    delta = abs(old.volume + M[p].volume - 2 * common(old, M[p]).volume)
    check(f'{p}: supplied geometry preserved', delta < .01, symmetric_difference_mm3=float(delta))
if VERSION==23:
    old = trimesh.load_mesh(ROOT / 'cad' / 'reference' / 'mount_v22.stl')
    hook_region = trimesh.creation.box(extents=[35, 22, 45])
    hook_region.apply_translation([12.5, 1, 12.5])
    old_hook = common(old, hook_region)
    new_hook = common(M['g7_mount'], hook_region)
    delta = abs(old_hook.volume + new_hook.volume - 2 * common(old_hook, new_hook).volume)
    check('controller hook geometry preserved', delta < .01, symmetric_difference_mm3=float(delta))
else:
    old = trimesh.load_mesh(ROOT/'printable'/'G7_Modular_v23_g7_mount.stl')
    # Above the free-end cut, the actual controller clip region is unchanged.
    region=trimesh.creation.box(extents=[30,14,16.9])
    region.apply_translation([11.5,-3.,1.55]) # Z=-6.9..10, Y=-10..4
    old_hook=common(old,region);new_hook=common(M['g7_mount'],region)
    delta=abs(old_hook.volume+new_hook.volume-2*common(old_hook,new_hook).volume)
    check('clip sides and thickness preserved above shortened tips',delta<.01,symmetric_difference_mm3=float(delta))
    for x in [2.5,20.5]:
        probe=trimesh.creation.box(extents=[.1,6,11.1])
        probe.apply_translation([x,-1.8,-3.45]) # Z=-9..2.1, includes the clip only
        before=common(old,probe);after=common(M['g7_mount'],probe)
        check(f'clip at X={x}: 10 mm to 9 mm',abs(before.extents[2]-10)<.001 and abs(after.extents[2]-9)<.001,
              old_length_mm=float(before.extents[2]),new_length_mm=float(after.extents[2]))
    check('receiver exactly 40 mm higher',abs(M['g7_mount'].bounds[1,1]-(old.bounds[1,1]-40))<1e-4,
          previous_open_end_y_mm=float(old.bounds[1,1]),new_open_end_y_mm=float(M['g7_mount'].bounds[1,1]))
    check('raised module male head clears retained upper bend',assembly()['box'].bounds[0,2]-M['hook_fit_coupon'].bounds[1,2]>2,
          clearance_mm=float(assembly()['box'].bounds[0,2]-M['hook_fit_coupon'].bounds[1,2]))
    if VERSION==25:
        previous=trimesh.load_mesh(ROOT/'printable'/'G7_Modular_v24_g7_mount.stl')
        old_coupon=trimesh.load_mesh(ROOT/'printable'/'G7_Modular_v24_hook_fit_coupon.stl')
        check('dock 5 mm closer to controller than V24',abs(previous.bounds[1,2]-M['g7_mount'].bounds[1,2]-5)<.001,offset_mm=float(previous.bounds[1,2]-M['g7_mount'].bounds[1,2]))
        check('curved bridge 5 mm closer than V24',abs(old_coupon.bounds[1,2]-M['hook_fit_coupon'].bounds[1,2]-5)<.001,offset_mm=float(old_coupon.bounds[1,2]-M['hook_fit_coupon'].bounds[1,2]))
    for name in ['box','lid','lock_key','male_fit_coupon','universal_receiver']:
        old_part=trimesh.load_mesh(ROOT/'printable'/f'G7_Modular_v23_{name}.stl')
        delta=abs(old_part.volume+M[name].volume-2*common(old_part,M[name]).volume)
        check(f'{name}: V23 interface geometry retained',delta<.01,symmetric_difference_mm3=float(delta))

NS = 'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'
ET.register_namespace('', NS)


def save_3mf(path, meshes, label):
    root = ET.Element(f'{{{NS}}}model', unit='millimeter', attrib={'{http://www.w3.org/XML/1998/namespace}lang': 'en-US'})
    ET.SubElement(root, f'{{{NS}}}metadata', name='Title').text = label
    ET.SubElement(root, f'{{{NS}}}metadata', name='Description').text = f'V{VERSION} prototype; controller physical fit unverified. No slicer process settings.'
    resources = ET.SubElement(root, f'{{{NS}}}resources')
    build = ET.SubElement(root, f'{{{NS}}}build')
    for i, (name, mesh) in enumerate(meshes.items(), 1):
        obj = ET.SubElement(resources, f'{{{NS}}}object', id=str(i), name=name, type='model')
        geo = ET.SubElement(obj, f'{{{NS}}}mesh')
        vertices = ET.SubElement(geo, f'{{{NS}}}vertices')
        triangles = ET.SubElement(geo, f'{{{NS}}}triangles')
        for v in mesh.vertices:
            ET.SubElement(vertices, f'{{{NS}}}vertex', **{k: format(float(x), '.9g') for k, x in zip('xyz', v)})
        for f in mesh.faces:
            ET.SubElement(triangles, f'{{{NS}}}triangle', **{k: str(int(x)) for k, x in zip(('v1', 'v2', 'v3'), f)})
        ET.SubElement(build, f'{{{NS}}}item', objectid=str(i))
    with zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('3D/3dmodel.model', ET.tostring(root, encoding='utf-8', xml_declaration=True))
        z.writestr('[Content_Types].xml', '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels', '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel0" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    # Read back actual vertex/face values and object references, checking bounds.
    with zipfile.ZipFile(path) as z:
        reread = ET.fromstring(z.read('3D/3dmodel.model'))
        objects = reread.findall(f'./{{{NS}}}resources/{{{NS}}}object')
        check(f'{path.name}: object count', len(objects) == len(meshes))
        for obj, (name, expected) in zip(objects, meshes.items()):
            vv = [[float(v.attrib[a]) for a in 'xyz'] for v in obj.findall(f'.//{{{NS}}}vertex')]
            ff = [[int(f.attrib[a]) for a in ('v1', 'v2', 'v3')] for f in obj.findall(f'.//{{{NS}}}triangle')]
            actual = trimesh.Trimesh(vv, ff)
            check(f'{path.name}: {name} mesh round trip', actual.is_watertight and
                  np.allclose(actual.bounds, expected.bounds, atol=1e-6) and len(actual.faces) == len(expected.faces))


out = ROOT / 'assemblies'
out.mkdir(exist_ok=True)
for up in (False, True):
    save_3mf(out / f'G7_Modular_v{VERSION}_Assembly_USB_{"Up" if up else "Down"}.3mf', assembly(up), f'V{VERSION} assembly view only; do not slice assembled')

# Separate all seven objects with a 12 mm gap and put every object on Z=0.
# This is a layout, NOT a promise of support-free printing or printer bed fit.
layout = {}
x = 0.
for p, mesh in M.items():
    mesh = mesh.copy()
    # Put the lid's outer face on the bed, avoiding an elevated flat lid panel.
    if p == 'lid':
        mesh.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    mesh.apply_translation([x - mesh.bounds[0, 0], -mesh.bounds[0, 1], -mesh.bounds[0, 2]])
    x = mesh.bounds[1, 0] + 12
    layout[p] = mesh
for a, b in itertools.combinations(layout, 2):
    # Axis-separated layout is stronger evidence here than sampling triangles.
    check(f'print layout: {a}/{b} separated',
          layout[a].bounds[1, 0] + 11.99 <= layout[b].bounds[0, 0])
for p, mesh in layout.items():
    check(f'print layout: {p} on bed', abs(mesh.bounds[0, 2]) < 1e-6)
save_3mf(out / f'G7_Modular_v{VERSION}_Separated_7_Parts.3mf', layout, f'V{VERSION} separated geometry; review orientation and supports in slicer')

report = dict(status='CAD checks passed; physical hardware fit unverified',
              software=dict(trimesh=trimesh.__version__, numpy=np.__version__),
              mesh_sha256={p: hashlib.sha256((ROOT/'printable'/f'G7_Modular_v{VERSION}_{p}.stl').read_bytes()).hexdigest() for p in PARTS},
              check_count=len(checks), checks=checks,
              unverified=['G7 Pro shape and hook grip', 'Controller installation path',
                          'Rear button, trigger, USB and charging dock clearance',
                          'Contents of Box 2 and cable plug clearance',
                          'Printer tolerances, latch flexibility, fatigue and load strength'],
              print_layout_bounds_mm=[np.min([v.bounds[0] for v in layout.values()], axis=0).tolist(),
                                      np.max([v.bounds[1] for v in layout.values()], axis=0).tolist()])
REPORT.write_text(json.dumps(report, indent=2)+'\n')
print(f'{len(checks)} CAD checks passed. Physical controller/device fit remains UNVERIFIED.')
