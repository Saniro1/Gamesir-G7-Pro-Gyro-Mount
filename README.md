# GameSir G7 Pro modular reversible gyro mount

**V34 is current:** the receiver's lower edge is **another 5 mm closer to the controller than V33**, with its upper edge fixed. This is a cumulative 10 mm lower-edge inward shift from the upright V28 position. The curved lower links are rebuilt for the steeper angle. **Only the controller mount needs reprinting**; reuse the existing box and V33 cap.

![V33 and V34 inclination comparison](docs/V34_mount_tilt.png)

## Download and print

- [Supported V34 Snapmaker PLA Black 3MF](slicer/Snapmaker_U1_PLA_Black_0.4_V34/G7_Modular_v34_U1_0.4_Snapmaker_PLA_Black_Supported.3mf)
- [Editable unsliced PLA project](slicer/Snapmaker_U1_PLA_Black_0.4_V34/G7_Modular_v34_U1_0.4_Snapmaker_PLA_Black.3mf)
- [Revised controller mount STL](printable/G7_Modular_v34_g7_mount.stl)
- [Complete V34 ZIP](releases/G7_Pro_Modular_Reversible_Box2_V34_Complete_PLA.zip)
- [Printing instructions](slicer/Snapmaker_U1_PLA_Black_0.4_V34/README.md) and [revision measurements](docs/V34_REVISION.md)

Open the 3MF **as a project** in Snapmaker Orca 2.4.1 or newer. Setup remains **U1, 0.4 mm nozzle, Snapmaker PLA Basic Black 1.75 mm, textured PEI, top cover removed**, at **220°C nozzle / 65°C bed**. The thin peel sheets are included. Keep each object's shells together and retain Normal/manual mode; do not add automatic support blocks.

**To print only the revised mount:** remove the box and lid objects from plate 2, keep the complete mount object including its support sheets, and **re-slice**. The saved cached toolpaths describe the complete plate. The ordinary mount STL contains no disposable sheets; use the project for the prepared support setup.

## What changed and what is checked

The receiver face rotates rigidly from 11.17° to 22.81° inward relative to V28. The upper face edge stays fixed; the lower edge moves inward by 5 mm and shifts upward about 1.53 mm as a consequence of rotation. The supporting links flow from the unchanged rounded upper bridge into the newly tilted receiver floor. The mating profile is not scaled or distorted.

The controller clips retain their 9 mm insertion length and reduced cross-section. Box, longer-lipped cap, standalone keyless receiver and both fit coupons are byte-identical to V33. The key remains omitted, USB access remains open, and the controller dock retains its existing friction-based retention.

**91 CAD checks and 112 native project/slicing checks passed.** Both box orientations and insertion paths remain clear, the measured lower-edge change is another 5 mm, and both saved PLA plates reopened and sliced without plate-level warnings. Reports include matching mesh/project hashes.

The supplied photo shows the remaining gap and intended direction, but it does not provide a controller shell model or reliable scale. **Actual shell/button/cable clearance at the new angle is unverified.** Test the unloaded mount first; the nominal 5 mm movement is not a guarantee of flush contact or a holding-force measurement.

## History and rebuild

[V33 instructions](docs/V33_README.md), earlier revisions and previous material setups remain available. The original V22 files/ZIP are preserved. No license was supplied with those files; this import does not grant a new license.

Requires OpenSCAD 2021.01 and Python 3.12:

```bash
python -m venv .venv
.venv/bin/python -m pip install -r tools/requirements.txt
source .venv/bin/activate
./tools/build.sh 34
.venv/bin/python tools/create_snapmaker_orca_project.py --design-version 34 --material pla \
  --resources /path/to/SnapmakerOrca/resources \
  --orca /path/to/snapmaker-orca --workdir /tmp/g7-u1-v34-pla --validate
python tools/package_release.py --design-version 34 --material pla
```

The build copies five unchanged V33 parts, exports the frozen upper hook, new smooth lower links and tilted keyless receiver, then makes a checked manifold3d union. Source, six STLs, assemblies, supports, presets, reports and rebuild tools are included in the ZIP.
