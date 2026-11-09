# Snapmaker U1 · 0.4 mm · Snapmaker PLA Black

Open **G7_Modular_v23_U1_0.4_Snapmaker_PLA_Black.3mf** in **Snapmaker Orca 2.4.1 or newer**, choosing **Open as project / Load configuration**. It contains the printer/material/process settings, object orientations, support overrides, and two plates. It is an unsliced project; review the preview and slice the selected plate on your computer before sending it to the printer.

This uses the official **Snapmaker PLA Basic @U1** preset for regular PLA, with color set to black. If the spool label says Eco, Matte or SnapSpeed, select that matching material instead. All parts use filament 1, mapped to the first U1 tool; load black PLA there or remap to the tool holding it. No other filament or support material is required.

## Included plates

| Plate | Parts | Orca estimate |
| --- | --- | --- |
| 01 – Fit tests first | Short controller hook, standalone receiver, male dovetail coupon, locking key | 55m 34s; 9.22 g |
| 02 – Complete mount | Full mount, box, lid, locking key | 2h 44m 45s; 29.38 g |

Print plate 1 first. Check the actual hook on your controller, the dovetail fit and the key's release action before printing plate 2. These estimates include the slicer's modeled support/brim use; actual printer time/material can differ. The design has not been physically printed or fitted to a controller.

## Saved settings

| Setting | Value |
| --- | --- |
| Printer | Snapmaker U1, 0.4 mm nozzles |
| Material | Snapmaker PLA Basic, black |
| Bed | Textured PEI |
| Nozzle / bed temperature | 220°C / 65°C, including first layer |
| Maximum volumetric flow | 8 mm³/s (reduced from stock 15) |
| Layer height / first layer | 0.16 / 0.20 mm |
| Walls | 4, Arachne |
| Top / bottom layers | 6 / 5 |
| Infill | 25% gyroid; key 100% |
| Outer / inner wall speeds | 40 / 60 mm/s; key 25 / 30 |
| Infill / top surface speed | 80 / 35 mm/s |
| Support | Normal auto, snug, build plate only |
| Support contact gap | 0.20 mm Z, 0.35 mm XY |
| Brim | 5 mm outer brim, 0.15 mm gap; disabled on lid and standalone receiver |
| Scale / XY size correction | 100% / zero; elephant foot compensation 0.15 mm |
| Sequence / prime tower | By layer / disabled (single material) |

The mount and hook coupon stand in their original CAD frame with supports, preserving the hook/dock orientation between test and final print. Box and male coupon sit on their dovetail heads with support under the surrounding enclosure/coupon plate. The lid's broad outer face lies on the bed. The standalone receiver is upright and support-free to keep its channel clean.

**The locking key is on its long side with removable supports.** This places its flex gap vertically and avoids a 13 mm unsupported cantilever in the original flat orientation. Remove its support and brim carefully and inspect that the gap and tongue are free. The model itself is unchanged. PLA is more brittle than the PETG originally suggested for this flexure, so test insertion/release gently and inspect for cracking. This setup is not a strength or fatigue certification.

Check that the actual bed is textured PEI, the loaded tool is mapped correctly and supports release cleanly from contact surfaces. Keep the model scale at 100%; whole-part scaling changes the controller hook and box cavity as well as the dovetail. Physical controller/device fit remains unverified.

## Validation and reproducibility

Created and reopened with the official Snapmaker Orca **2.4.1** Linux release from:

- https://github.com/Snapmaker/OrcaSlicer/releases/tag/v2.4.1
- Printer/material base settings: that release's bundled `resources/profiles/Snapmaker`.

Both plates were sliced from the saved project with return code 0, no plate-level slicing warnings, and nonempty G-code. `validation.json` records project SHA-256, 60 checks, saved/reloaded settings, geometry preservation and plate membership/clearance. No physical print or graphical UI inspection was performed. The delivered 3MF excludes the validation G-code so you can inspect and slice it yourself.

The CLI in 2.4.1 has inherited Bambu baseline/version handling: reopening its own project requires `--allow-newer-file`, and it reports missing optional BBL baseline paths and an empty bed-exclusion polygon. Validation confirms the full saved U1 configuration is retained and both plates slice successfully. The generator omits a redundant partial process-preset `wipe_tower_filament=0` field to avoid another 2.4.1 CLI null-pointer bug; prime tower stays disabled and the merged project retains the default. These are CLI workarounds, not printer G-code modifications. Manufacturer start/end/tool-change routines remain unchanged.

Using the repository's existing virtual environment and an installed Snapmaker Orca 2.4.1 runtime:

```bash
.venv/bin/python tools/create_snapmaker_orca_project.py \
  --resources /path/to/SnapmakerOrca/resources \
  --orca /path/to/snapmaker-orca \
  --workdir /tmp/g7-u1-project --validate
```

The executable can be a wrapper that provides your system's required libraries and `--datadir`; it must pass through the supplied arguments. The generator writes the unsliced project and its resolved preset JSONs, then reopens/slices it and runs the validator. It leaves oriented intermediate STLs, logs and validation G-code in the scratch working directory. No Git worktree is needed. The printer profile JSON is primarily a resolved build input; use the 3MF to open the configured project.
