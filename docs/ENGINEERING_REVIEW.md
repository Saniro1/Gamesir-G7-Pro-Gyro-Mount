# V22 inspection and V23 corrections

## Evidence and scope

Input: `G7_Pro_Modular_Reversible_Box2_V22_Complete.zip` provided by the owner. All 13 archived files are preserved verbatim under `originals/v22/`, along with the ZIP itself. The archive's prior instructions are historical claims, not independent fit evidence. No separate ChatGPT conversation was available. The owner confirmed that the hook has not been printed/tested.

No controller scan, measured contact profile, source hook STL, source Box 2 STL, gyro-device model, mass, cable model or printer calibration was supplied. Overall controller dimensions alone would not establish hook fit. This review therefore preserves controller contact surfaces and device cavity rather than inventing a new fit. **Successful CAD checks cannot certify physical G7 Pro compatibility.**

## Measurements from the exported V22 solids

All six supplied STL parts are watertight, consistently wound, positive-volume, single connected solids. Assembled mount, box, lid and key do not overlap in either USB orientation at the supplied reference pose. The box and attached lid can slide out of the mount without rigid collisions with the key removed.

The V22 male dovetail is 19.6 mm long, centered at local X=-1, Y=-2.8. Its head is 14.2 mm wide and root is 10.8 mm wide. In installed coordinates its Y span is 51.6–71.2 mm. Native Box 2 rear surface Z=-1 becomes installed Z=28.8. The male's bottom is installed Z=26.35; receiver floor is approximately Z=26.10 (0.25 mm gap). The mount-to-box rear-face gap is 0.25 mm. These are ideal mesh dimensions, not achievable printer accuracy claims. The roughly 0.23–0.28 mm per-side profile clearances need calibration.

### Stop defect

V22's nominal channel starts at installed Y=50.0; its intended dovetail stop would allow about 1.6 mm inward travel from the reference pose. But the enclosure begins touching the support links after approximately 0.97 mm inward travel. At -1.0 mm the measured collision volume is about 0.00164 mm³; at -1.5 mm it is about 0.6666 mm³. This means the support can take contact before the designed rail stop. V23 adds solid material across the channel back to Y=51.4, leaving 0.2 mm inward travel. Tests verify that first stop contact is low in the receiver, not on the enclosure/support arm.

The existing key allows about 1.2 mm outward play before contacting the trailing dovetail end. V23 retains this position; the combined ideal axial free play is about 1.4 mm. It is not an anti-rattle fit. Reducing play further should follow printer calibration and a physical test.

### Key flexure

V22's snap bump intersects the receiver during transverse insertion, but was mounted on a solid bar without a dedicated flexure slot. V23 adds a tongue approximately 12.95 mm long, 1.15 mm wide and 0.80 mm thick, with a 0.40 mm gap beneath it. The bump needs approximately 0.27 mm downward deflection to pass the slot roof. The model provides space for that motion; no material/strain, fatigue, insertion-force or pull-out-force test has been performed. The solid bar/grip remain clear during insertion; sampled rigid interference occurs only above the slot roof at the flex bump.

V22 has a 0.17 mm roof above the key opening, less than a typical 0.20 mm layer. V23 fills the upper part of that slot and cuts a matching 2.20 mm-high slot 0.40 mm lower. This leaves a 0.57 mm roof and approximately 2.08 mm of receiver floor beneath the slot. The matching key moves down 0.40 mm. These dimensions still need sliced-layer inspection and physical testing; they are not a load rating. The V23 key and receiver should be used together.

### Lid

The assembled lid clears the box. Sliding across its existing detents produces small intentional overlaps (maximum approximately 0.07 mm³ in the opening direction). These detents are not reported as collision-free motion. Their elastic fit and wear require a test print. The lid and box cavity were left unchanged.

### Source repair and reference geometry

The supplied SCAD references two absent source meshes. Its full controller hook and enclosure cannot rebuild reliably from that source alone. The original SCAD is retained for provenance. V23 instead imports the exact provided final mount, box and lid meshes, modifies the mount/receiver stop with solid operations, and defines the replacement key and test coupons procedurally. This makes the package self-contained without claiming to recover missing editable controller/cavity surfaces. OpenSCAD `--hardwarnings` is used for every exported part.

## Validation

`tools/package_and_validate.py` tests the actual exported STLs and the 3MF geometry written to disk. See `validation.json` for current measured values and SHA-256 hashes identifying the tested meshes. Key/lid snap interference is explicitly distinguished from the rigid collision checks. Insertion paths are sampled at 0.25 mm intervals over 40 mm; this is not a proof of collision freedom for every possible installation angle or elastic deformation.

The tests cover both reversed orientations, stop contact, key blocking, consistent standalone receiver geometry, geometry preservation, connected/watertight solids, separated bed layout and 3MF round trips. They do not cover physical controller fit, controller installation, cable plugs, device contents, surface finish, slicer behavior, strength or fatigue. Assembly 3MFs are for viewing; separated layouts still need slicing review and may exceed some printer beds.

## Physical acceptance checklist

- Hook coupon slides onto the actual G7 Pro and seats fully without tools, damage, excessive force or looseness. Photograph the seated position from top and side and measure any gaps/interference.
- Full mount clears the shell throughout installation, all trigger positions, rear-button travel and cable routing. Check any charging dock separately.
- Dovetail coupon slides by hand in the V23 receiver, reaches the new stop, and can be removed with the key withdrawn.
- Key tongue is free (gap not fused), can be pressed to release, returns fully after insertion, and blocks withdrawal without cracking. Inspect the receiver roof and slot in the sliced preview and print.
- Box holds the actual gyro device without pinching it or pressing its controls. USB opening and lid notch fit the actual plug and cable bend in both orientations.
- Lid can open/close repeatedly without cracking or excessive force.
- Only after those pass, test retention progressively over a protected surface with the intended device mass. No load rating is established here.

If the hook is too tight/loose, take measurements at the actual contact locations before revising it. The short coupon is only a screening test, not evidence that the arms clear the controller.
