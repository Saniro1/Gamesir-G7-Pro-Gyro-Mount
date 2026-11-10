# GameSir G7 Pro modular reversible gyro mount

**V27 is the current revision:** Box 2 sits **10 mm lower than V26**, with a longer, gentler curved transition and about **8 mm of upper-bridge clearance**. The **9 mm clips**, **5 mm receiver-face inset**, and **thin straight supports** are retained. The box is now 30 mm above its original V23 position.

The owner asked for more slack to fit the box. V27 lowers the complete module 10 mm, relaxes the tight return curve, and increases the upper-bridge-to-box clearance from about 1.2 mm to at least 8 mm. The revised fit has not yet been physically tested; print the short hook coupon first.

![Receiver face inset relative to the main base](docs/V27_receiver_inset.png)

## Download and print

- [Snapmaker U1 0.4 mm / Snapmaker PLA Black — supported V27 3MF](slicer/Snapmaker_U1_PLA_Black_0.4_V27/G7_Modular_v27_U1_0.4_Snapmaker_PLA_Black_Supported.3mf)
- [Editable, unsliced V27 project](slicer/Snapmaker_U1_PLA_Black_0.4_V27/G7_Modular_v27_U1_0.4_Snapmaker_PLA_Black.3mf)
- [Complete V27 ZIP](releases/G7_Pro_Modular_Reversible_Box2_V27_Complete.zip)
- [Revised attachment STL](printable/G7_Modular_v27_g7_mount.stl) and [9 mm hook test STL](printable/G7_Modular_v27_hook_fit_coupon.stl)

Open the 3MF **as a project** in Snapmaker Orca 2.4.1 or newer. The supported file includes cached toolpaths and supports; inspect them in Preview. Re-slice if you change anything.

Plate 1 contains the revised hook test, receiver, dovetail coupon and key. Plate 2 contains the complete four-part assembly. **The Box 2 enclosure, lid, key and dovetail profile are unchanged from V23**; reuse those prints if you already have them. To print only the revised attachment, select that object and re-slice rather than sending the cached full-plate job.

## Current geometry

- Trimmed 1 mm from the free ends of both top clips: 10 mm becomes 9 mm. No global scaling or thinning of their sides.
- Lowered the complete dock/box/key installation 10 mm from V26, leaving it 30 mm above V23.
- Kept the receiver face 5 mm inward of the main-base reference. The more gradual upper curve and longer curved links leave at least 8 mm between the upper bridge and the box leading wall in either USB orientation.
- Removed the old long arms and lower dock, and joined the raised receiver with short structural arms.
- Used sparse straight rectilinear print supports (normal/snug, 3 mm line spacing), 0.32 mm separation and a sparse interface. No tree supports.

The structural arms are permanent parts of the attachment. The thin print supports shown in the slicer preview are removable. See [revision measurements and validation](docs/V27_REVISION.md) and [U1 setup details](slicer/Snapmaker_U1_PLA_Black_0.4_V27/README.md).

The controller shell, rear buttons, triggers and cable routes still need a physical check at this new position. Check the short hook first and then the complete mount without loading the device. PLA flexure durability and the strength of the bracket/key have not been physically verified.

## Files and history

V27 CAD is in [cad/G7_Pro_Modular_v27.scad](cad/G7_Pro_Modular_v27.scad); its seven STLs are in `printable/`, and both assembly views are in `assemblies/`. The V27 CAD reuses the frozen V24 9 mm clip geometry and V23 interface meshes. Its upper curved cheek keeps the V25 outward depth but turns earlier in the downward direction. The controller-contact clip surfaces remain unchanged.

The complete original V22 ZIP and all 13 extracted files remain unchanged under `originals/`. V23, V24, V25 and V26 source, prints and projects are retained for history, including the [V23 instructions](docs/V23_README.md). **Use V27 filenames for this revision.** No license was supplied with the original files; this import does not assert ownership or grant a new license.

## Rebuild

Use the existing checkout; no Git worktree is needed. Requires OpenSCAD 2021.01 and Python 3.12:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r tools/requirements.txt
source .venv/bin/activate
./tools/build.sh 27
```

The build exports all seven V27 meshes and runs the geometry/assembly checks, writing `docs/validation_v27.json`. Explicitly use `./tools/build.sh 23` to reproduce the old version.

To regenerate the U1 projects and validate the saved file in the actual slicer:

```bash
.venv/bin/python tools/create_snapmaker_orca_project.py --design-version 27 \
  --resources /path/to/SnapmakerOrca/resources \
  --orca /path/to/snapmaker-orca --workdir /tmp/g7-u1-v27 --validate
python tools/package_release.py --design-version 27
```

The saved V27 project passed 84 project/slicing checks, and the V27 geometry passed 96 CAD checks. These establish model and slicer consistency, not physical fit or a load rating.
