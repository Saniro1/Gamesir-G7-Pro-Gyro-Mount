// G7 Pro V11: raised, late-turn curved flat supports following the user's annotated side profile.
// Built from V10, preserving EXACTLY the V10 hook, cover, Box 2 and outward lid.
// Keep V9 smooth top-to-back supports, box orientation, lid, and top support routing.
$fn=48;
part = "assembly_down";
rear_drop=22;
box_translate=[12.5,22.0,-34.0-rear_drop];
box_rotate=[-90,0,0];
curve_segments=28;

module original_top_fitting_clip() {
    intersection() {
        import("gamesir-dongle-holder.stl",convexity=12);
        translate([-10,-15,-8]) cube([45,16.2,30]);
    }
}

// Relax the slide-on channel to give more installation slack.
// Changes are INTERNAL only: enlarge the top pocket and throat,
// and add a lead-in funnel at the slide-entry end.
module relaxed_top_fitting_clip(){
    difference(){
        original_top_fitting_clip();
        union(){
            // 1) Top pocket enlargement: slightly more room where the controller top sits.
            translate([4.0,1.55,1.0]) cube([14.0,5.45,11.2]);
            // 2) Throat enlargement: allow the part to start sliding on easier.
            translate([4.1,-0.15,0.2]) cube([13.8,2.10,10.9]);
            // 3) Entry lead-in funnel to avoid snagging at the mouth.
            hull(){
                translate([3.2,-4.95,-0.25]) cube([15.6,3.10,3.30]);
                translate([4.2,-0.45,0.55]) cube([13.6,2.10,4.90]);
            }
            // 4) Small shoulder relief near upper sidewalls so the slide path is less grabby.
            translate([3.0,1.7,8.8]) cube([1.8,4.9,3.6]);
            translate([18.2,1.7,8.8]) cube([1.8,4.9,3.6]);
        }
    }
}

function bezier2(a,b,c,d,t) =
    pow(1-t,3)*a + 3*pow(1-t,2)*t*b + 3*(1-t)*t*t*c + pow(t,3)*d;
module yz_profile_strap(x,width) {
    // ENLARGED TOP-TO-BACK CLEARANCE: Supports remain near the BOX height
    // for much longer, then turn downward smoothly only near the top hook.
    // This changes the SUPPORT PATH, not cross-section (still flat 3.7 mm X).
    // Installed side-view sketch: box on left -> near-level deck -> smooth,
    // steep but tangent-continuous curved connection near the top hook.
    upper_outer = [[7.0,11.75],[14.2,11.75],[23.5,7.2],[23.5,-4.5]];
    lower_inner = [[20.0,-4.5],[20.0,3.2],[12.0,10.7],[6.0,11.0]];
    multmatrix([[0,0,1,x],[1,0,0,0],[0,1,0,0],[0,0,0,1]])
        linear_extrude(height=width)
        polygon(concat(
            [[7.0,12.85]],
            [for(i=[0:curve_segments]) bezier2(upper_outer[0],upper_outer[1],upper_outer[2],upper_outer[3],i/curve_segments)],
            // Full-height straight section remains unchanged at the box joint.
            [[23.5,-34.8], [20.0,-34.8], [20.0,-4.5]],
            [for(i=[1:curve_segments]) bezier2(lower_inner[0],lower_inner[1],lower_inner[2],lower_inner[3],i/curve_segments)],
            [[5.6,11.55],[5.2,11.55],[5.2,11.85],[3.7,11.85],[3.7,12.85]]
        ));
}
module long_rear_bracket() {
    union(){
        yz_profile_strap(2.1,3.7);
        yz_profile_strap(17.2,3.7);
        // Torsion tie BEFORE the removable box; no supports cross docking space.
        translate([5.3,20.2,-20.0]) cube([12.6,3.2,3.0]);
    }
}
module box_slide_rails(){
    translate([-14.35,-15.8,21.8]) cube([1.65,25.3,0.9]);
    translate([10.7,-15.8,21.8]) cube([1.65,25.3,0.9]);
    hull(){ translate([-14.64,8.10,22.02]) cube([0.34,0.4,0.4]); translate([-14.85,8.70,21.94]) cube([0.20,0.25,0.55]); }
    hull(){ translate([12.30,8.10,22.02]) cube([0.34,0.4,0.4]); translate([12.65,8.70,21.94]) cube([0.20,0.25,0.55]); }
}
module original_box_with_rails(){
    difference(){
        union(){ import("Box 2(1).stl",convexity=12); box_slide_rails(); }
        translate([-8.5,9.7,15.35]) cube([15.0,3.0,10.5]);
    }
}
module placed_box(){ translate(box_translate) rotate(box_rotate) original_box_with_rails(); }
module locking_slide_lid(){
    difference(){
        union(){
            translate([-15.55,-17.60,23.75]) cube([29.10,29.70,1.90]);
            translate([-15.55,-16.45,21.10]) cube([0.85,27.2,2.65]);
            translate([12.70,-16.45,21.10]) cube([0.85,27.2,2.65]);
            translate([-14.70,-16.45,21.10]) cube([0.72,27.2,0.50]);
            translate([11.98,-16.45,21.10]) cube([0.72,27.2,0.50]);
            translate([-4.75,-19.70,23.75]) cube([7.5,2.3,1.90]);
        }
        translate([-15.7,7.70,21.68]) cube([1.25,1.75,1.40]);
        translate([12.50,7.70,21.68]) cube([1.25,1.75,1.40]);
        translate([-8.7,8.65,23.20]) cube([15.4,5.10,3.20]);
    }
}
module placed_lid(){ translate(box_translate) rotate(box_rotate) locking_slide_lid(); }
module orient_to_installed_g7_frame(){ translate([0,0.2,8]) rotate([90,0,0]) translate([0,-0.2,-8]) children(); }
module correctly_downward_facing_hook(){
    translate([11.5,-1.775,0]) rotate([0,0,180]) translate([-11.5,1.775,0])
        relaxed_top_fitting_clip();
}
module upper_clip_attachment_pads(){
    translate([2.80,-4.70,10.70]) cube([3.65,1.10,4.45]);
    translate([16.55,-4.70,10.70]) cube([3.65,1.10,4.45]);
}
module exterior_hook_reinforcement() {
    hull() { for (x=[3.85,19.15]) for (z=[13.25,15.25]) translate([x,-4.68,z]) sphere(r=0.85,$fn=28); }
    for (x=[1.25,21.75]) { hull() { translate([x,-4.99,3.5]) sphere(r=1.08,$fn=28); translate([x,-4.99,11.0]) sphere(r=1.08,$fn=28); } }
}

// V21: EIGHT MILLIMETER LONGER HOOK REACH. V19: ONE BLENDED FULL-HEIGHT OUTER CHEEK -- no detached arch, no spacer ribs.
// Coordinate convention: left-to-right on the side view is installed Y decreasing.
// The newly formed outer envelope closely traces the ORIGINAL support bend,
// while the inside fills into the existing supports and upper hook.
// Below z=12.0, all new material stays REARWARD of installed Y=-4.56.
// Only the extended outer wall reaches toward z=-7.2 to join the hook shifted down 8 mm.
// V11 controller-facing hook module and support modules are unchanged.
function cr(p0,p1,p2,p3,t) =
    0.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t);
function smooth_path(p, steps=8) =
    concat([for(i=[0:len(p)-2],j=[0:steps-1])
        cr(p[max(0,i-1)],p[i],p[i+1],p[min(len(p)-1,i+2)],j/steps)],
        [p[len(p)-1]]);
module seamless_integral_end(){
    // Preserve the ORIGINAL V19 outer curve until the final vertical drop.
    // A straight continuation creates a visibly longer reach without changing
    // the G7 top hook shape or adding an awkward bulge.
    outer = smooth_path([
        [11.60,31.46], [8.70,31.47], [5.30,30.72],
        [2.20,28.65], [-0.50,25.55], [-2.65,22.20],
        [-4.30,18.65], [-5.55,15.10], [-6.18,12.25]
    ]);
    inner = smooth_path([
        [-4.56,11.9],[-4.36,13.2],[-2.40,15.1],
        [-0.40,18.5],[1.30,21.45],[3.80,25.10],
        [7.0,29.0],[11.60,30.1]
    ]);
    // Vertical outer wall is 8.0 mm longer, same continuous 1.62 mm
    // outer wall thickness in the final straight section.
    profile = concat(outer, [[-6.18,-7.2],[-4.56,-7.2]], inner);
    multmatrix([[0,0,1,1.12],[1,0,0,0],[0,1,0,0],[0,0,0,1]])
      linear_extrude(height=20.75,convexity=14)
        polygon(points=profile);
}

// V21 change: add 8 mm of actual DROP between the curved arm and clip.
// All three parts of the original V19 hook are rigidly relocated, not reshaped.
extra_drop = 8;
module original_hook_assembly_relocated(){
    translate([0,0,-extra_drop]) union(){
        correctly_downward_facing_hook();
        upper_clip_attachment_pads();
        exterior_hook_reinforcement();
    }
}

// UNIVERSAL MODULAR DOCK — dimensions in millimeters.
// Installed +Y is controller DOWN; +Z is outward/back from controller.
// Box rear surface is at Z=28.8; its open top faces +Z.
// Rotation of the whole removable module 180° about Z reverses USB-C.

// The male dovetail is CENTERED on Box2's back, making it reversible.
module reusable_box_dovetail(){
    hull(){
        // base rooted into original Box2 back surface (local Z=-1)
        translate([-6.4,-12.6,-1.20]) cube([10.8,19.6,0.42]);
        // broad undercut head = mechanical retention in mating receiver
        translate([-8.1,-12.6,-3.45]) cube([14.2,19.6,0.30]);
    }
}
module detachable_box(){
    union(){ original_box_with_rails(); reusable_box_dovetail(); }
}

// Installed-frame location of Box2 module on V21's support.
module module_location(){
    // Both historical transforms cancel rotations. Native Box2 local X/Y/Z
    // are aligned to installed X/Y/Z, translated by [12.5,64.2,29.8].
    translate([12.5,64.2,29.8]) children();
}
module removable_box_down(){ module_location() detachable_box(); }
module removable_box_up(){
    translate([11.5,61.4,0]) rotate([0,0,180])
        translate([-11.5,-61.4,0]) removable_box_down();
}
module removable_lid_down(){ module_location() locking_slide_lid(); }
module removable_lid_up(){
    translate([11.5,61.4,0]) rotate([0,0,180])
        translate([-11.5,-61.4,0]) removable_lid_down();
}

// Receiver slide: head has clearance at Z=26.35; mouth is at Z=28.55.
// Female channel is open at installed +Y for sliding in from controller bottom.
module receiver_channel_cut(){
    hull(){
        translate([3.92,50.0,25.94]) cube([15.16,25.8,0.16]);
        translate([5.85,50.0,28.60]) cube([11.30,25.8,0.16]);
    }
    translate([5.85,50.0,28.60]) cube([11.30,25.8,4.5]);
}
module universal_receiver_core(){
    difference(){
        translate([1.25,48.8,23.70]) cube([20.50,25.80,4.85]);
        receiver_channel_cut();
        // Through slot for a removable transverse safety key at the open end.
        translate([0.40,72.15,26.18]) cube([22.20,2.35,2.20]);
    }
}

// Curved support ends at Y=46, before Box2 begins at Y=46.7.
// Two under-box braces join into the rear base of the receiver rather than
// crossing the removable module's flat rear face or its dovetail.
module receiver_support_links(){
    for(x=[2.1,17.2]){
        hull(){
            translate([x,40.0,28.50]) cube([3.70,2.50,2.40]);
            translate([x,48.70,23.76]) cube([3.70,1.85,1.90]);
        }
    }
}
module installed_receiver(){
    union(){ universal_receiver_core(); receiver_support_links(); }
}
module modular_controller_mount(){
    union(){
        original_hook_assembly_relocated();
        orient_to_installed_g7_frame() long_rear_bracket();
        seamless_integral_end();
        installed_receiver();
    }
}

// Removable safety key. Insert after sliding the module fully into the dock;
// lift the outside finger tab to withdraw it before changing USB-C direction.
// Lock bar blocks movement in the exit direction, with a flared end grip.
module receiver_lock_key(){
    union(){
        translate([0.55,72.40,26.47]) cube([22.40,1.78,1.56]);
        // small latch nub catches outer wall after passing through cross slot
        // tapered spring barb protrudes only beyond the opposite outer wall
        hull(){
            translate([0.55,72.70,28.00]) cube([0.32,1.15,0.64]);
            translate([1.31,72.70,28.00]) cube([0.23,1.15,0.08]);
        }
        // thumb grip on outside of right edge, away from enclosure opening
        hull(){
            translate([22.80,72.05,26.04]) cube([1.0,2.6,2.35]);
            translate([26.00,71.45,25.70]) cube([0.9,3.7,3.0]);
        }
    }
}

// A *standalone standard interface* for future controller adapters.
// Male design and key are identical across all controllers using this socket.
// Local receiver origin is axis of dock: XY=0 at rail center, Z=0 at bottom.
module portable_receiver(){
    translate([-11.5,-61.4,-23.7]) universal_receiver_core();
}
module reusable_lock_key(){
    translate([-11.5,-61.4,-23.7]) receiver_lock_key();
}

if (part=="g7_mount") modular_controller_mount();
else if (part=="box") detachable_box();
else if (part=="lid") locking_slide_lid();
else if (part=="lock_key") reusable_lock_key();
else if (part=="universal_receiver") portable_receiver();
else if (part=="g7_receiver_only") installed_receiver();
else if (part=="assembled_down" || part=="assembly_down"){
    color("#4f6e83") modular_controller_mount();
    color("#d5ab64") removable_box_down();
    color("#e6cb89") removable_lid_down();
    color("#ee8555") receiver_lock_key();
}
else if(part=="assembly_up"){
    color("#4f6e83") modular_controller_mount();
    color("#d5ab64") removable_box_up();
    color("#e6cb89") removable_lid_up();
    color("#ee8555") receiver_lock_key();
}
else if(part=="assembly_exploded"){
    color("#4f6e83") modular_controller_mount();
    color("#d5ab64") translate([0,24,0]) removable_box_down();
    color("#e6cb89") translate([0,24,0]) removable_lid_down();
    color("#ee8555") translate([7,12,0]) receiver_lock_key();
}
// Optional small calibration coupon to test sliding friction before printing Box2.
module male_fit_test_coupon(){
    union(){
        translate([-11.0,-16.0,-1.00]) cube([20.0,26.0,1.00]);
        reusable_box_dovetail();
    }
}
if(part=="male_fit_coupon") male_fit_test_coupon();
