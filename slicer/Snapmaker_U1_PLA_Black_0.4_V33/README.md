# V33 — Snapmaker PLA Basic Black, U1 0.4 mm

Open `G7_Modular_v33_U1_0.4_Snapmaker_PLA_Black_Supported.3mf` **as a project** in Snapmaker Orca 2.4.1 or newer. It includes the U1 machine preset, PLA material preset, part placements, thin peel sheets and actual cached toolpaths. The file without `_Supported` is editable and unsliced.

V33 extends both cap retaining lips by 0.60 mm, from 0.72 to 1.32 mm reach. Nominal overlap under each box rail increases from 0.52 to 1.12 mm. Only the cap needs reprinting. All other accessory parts match V32. There is no locking key on either plate; USB access and the 9 mm controller clips remain.

| Setting | Saved PLA value |
|---|---|
| Printer / nozzle | Snapmaker U1 / 0.4 mm |
| Material / color | Snapmaker PLA Basic, 1.75 mm / black |
| Surface / cover | Textured PEI / top cover removed |
| Nozzle | 220°C, first and subsequent layers |
| Bed | 65°C, first and subsequent layers |
| Active chamber heating | Disabled |
| Layers | 0.16 mm; first layer 0.20 mm |
| Walls / infill | 4 / 25% gyroid |
| Outer / inner walls | 40 / 60 mm/s |
| Infill / top | 80 / 35 mm/s, also flow-limited |
| First layer / infill | 20 / 25 mm/s |
| Maximum volumetric speed | 8 mm³/s |
| Cooling | Official PLA cooling; fan off for first layer, normal min/max 100% |
| Brim | Disabled; sheets have individual small feet |

The material derives from the official `Snapmaker PLA Basic @U1` preset bundled with Snapmaker Orca 2.4.1. Black color and the conservative 8 mm³/s flow cap are set explicitly. Stock U1 start/end G-code and purge/cleaning behavior remain. Temperatures and fan changes during cleaning are distinct from part-printing settings. These settings have not been physically calibrated on this spool.

## Longer rail hooks

The new tips retain 0.23 mm nominal clearance from the box side walls and the previous vertical rail clearance. V32 friction pads, roof and wall spacing remain. Eight additional peel-sheet sections support the longer cap lips. Print only the whole lid object from plate 2 and re-slice if testing it against your existing box. Physical holding force has not been measured.

## Thin peel sheets and printing

Explicit 0.45 mm disposable sheets are already included as separate shells inside each print object. They retain V31/V33's 0.32 mm top gap, nominal 3 mm pitch and short independent sections. Keep each whole object intact and in its saved orientation. **Do not split shells or switch Normal/manual to automatic supports.** No additional support blocks are generated; the ordinary support-gap/density fields do not control the explicit mesh sheets.

Plate 1: hook test, keyless receiver and male docking fit test. Plate 2: keyless bracket, Box 2 and tighter lid. The first plate has 13 disposable sections, the second 48. To print only the tighter lid against your existing box, remove the other whole objects from plate 2 and re-slice. Do not print stale full-plate cached toolpaths after changing the plate contents.

Print the short fit tests before the full assembly: PLA fit and flexibility can differ from PETG. Let the parts cool, hold the body close to each support section, and peel one sheet at a time. Cut a stubborn strand instead of levering against a clip. Do not force a binding clip or lid. Thin sheets favor removal but can leave rough or sagged undersides. Physical removal ease is unverified.

The keyless docking connection retains the previous sliding clearances and relies on friction; the tighter cap does not secure the entire box to the controller. Test the unloaded dock before installing the device. No physical retention force, strength or fatigue life is established.

## Validation

Both plates reopened and sliced in actual Snapmaker Orca 2.4.1 without plate-level warnings. The project passed **112 checks**, including saved PLA settings and cooling, actual heating commands, saved accessory surfaces, separate sheets with no accessory overlap, actual sheet extrusions and exact embedded G-code. See `validation.json` for the project hashes and details.

Estimated totals including disposable sheets: plate 1 **37m 28s / 6.59 g**; plate 2 **2h 6m 48s / 19.17 g**. These are slicer estimates, not measured print results.

![PLA project sheet geometry and actual sliced layer](peel_sheet_preview.png)

Rebuild using `tools/create_snapmaker_orca_project.py --design-version 32 --material pla` with the usual resources, Orca and workdir arguments. V33 defaults to PLA; specifying `--material pla` makes that choice explicit.
