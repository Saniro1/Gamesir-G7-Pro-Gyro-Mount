# GameSir G7 Pro modular reversible gyro mount

**V24 is the current revision:** both top clips are shortened from **10 mm to 9 mm**, their width/thickness stay unchanged, and the Box 2 dock sits **40 mm higher**. The U1 project uses **thin straight supports, with no branches**.

The owner reported that the previous clips were too long and tight, and the previous dock sat too low. V24 incorporates that feedback. The revised fit has not yet been physically tested; print the short hook coupon first.

![V23 and V24 assembly comparison](docs/V24_comparison.png)

## Download and print

- [Snapmaker U1 0.4 mm / Snapmaker PLA Black — supported V24 3MF](slicer/Snapmaker_U1_PLA_Black_0.4_V24/G7_Modular_v24_U1_0.4_Snapmaker_PLA_Black_Supported.3mf)
- [Editable, unsliced V24 project](slicer/Snapmaker_U1_PLA_Black_0.4_V24/G7_Modular_v24_U1_0.4_Snapmaker_PLA_Black.3mf)
- [Complete V24 ZIP](releases/G7_Pro_Modular_Reversible_Box2_V24_Complete.zip)
- [Revised attachment STL](printable/G7_Modular_v24_g7_mount.stl) and [9 mm hook test STL](printable/G7_Modular_v24_hook_fit_coupon.stl)

Open the 3MF **as a project** in Snapmaker Orca 2.4.1 or newer. The supported file includes cached toolpaths and supports; inspect them in Preview. Re-slice if you change anything.

Plate 1 contains the revised hook test, receiver, dovetail coupon and key. Plate 2 contains the complete four-part assembly. **The Box 2 enclosure, lid, key and dovetail profile are unchanged from V23**; reuse those prints if you already have them. To print only the revised attachment, select that object and re-slice rather than sending the cached full-plate job.

## Changes in V24

- Trimmed 1 mm from the free ends of both top clips: 10 mm becomes 9 mm. No global scaling or thinning of their sides.
- Moved the complete dock/box/key installation 40 mm toward the controller top.
- Added 8 mm outward stand-off at the new dock position so the existing upper bend does not obstruct the box or female channel. This is an additional offset, not a change to the requested 40 mm height adjustment.
- Removed the old long arms and lower dock, and joined the raised receiver with short structural arms.
- Used sparse straight rectilinear print supports (normal/snug, 3 mm line spacing), 0.32 mm separation and a sparse interface. No tree supports.

The structural arms are permanent parts of the attachment. The thin print supports shown in the slicer preview are removable. See [revision measurements and validation](docs/V24_REVISION.md) and [U1 setup details](slicer/Snapmaker_U1_PLA_Black_0.4_V24/README.md).

The controller shell, rear buttons, triggers and cable routes still need a physical check at this new position. Check the short hook first and then the complete mount without loading the device. PLA flexure durability and the strength of the bracket/key have not been physically verified.

## Files and history

V24 CAD is in [cad/G7_Pro_Modular_v24.scad](cad/G7_Pro_Modular_v24.scad); its seven STLs are in `printable/`, and both assembly views are in `assemblies/`. The V24 CAD uses the included, frozen V23 meshes as its baseline, keeping the controller clip surfaces above the end trim and the existing interface geometry intact.

The complete original V22 ZIP and all 13 extracted files remain unchanged under `originals/`. V23 source, prints and projects are retained for history, including the [V23 instructions](docs/V23_README.md). **Use V24 filenames for this revision.** No license was supplied with the original files; this import does not assert ownership or grant a new license.

## Rebuild

Use the existing checkout; no Git worktree is needed. Requires OpenSCAD 2021.01 and Python 3.12:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r tools/requirements.txt
source .venv/bin/activate
./tools/build.sh 24
```

The build exports all seven V24 meshes and runs the geometry/assembly checks, writing `docs/validation_v24.json`. Explicitly use `./tools/build.sh 23` to reproduce the old version.

To regenerate the U1 projects and validate the saved file in the actual slicer:

```bash
.venv/bin/python tools/create_snapmaker_orca_project.py --design-version 24 \
  --resources /path/to/SnapmakerOrca/resources \
  --orca /path/to/snapmaker-orca --workdir /tmp/g7-u1-v24 --validate
python tools/package_release.py --design-version 24
```

The saved V24 project passed 84 project/slicing checks, and the V24 geometry passed 92 CAD checks. These establish model and slicer consistency, not physical fit or a load rating.
