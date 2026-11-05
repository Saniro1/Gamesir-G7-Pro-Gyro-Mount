// Units: mm. Mesh-backed repair of supplied V22; controller fit NOT verified.
// Original controller-contact surfaces and box cavity are preserved.
// All imports are shipped in reference/; no missing external assets.
$fn=48;
part="assembly_down";
// Positive values enlarge the dock channel in X only. Reprint the receiver
// and fit coupon when changing this. Leave zero until a physical fit test.
dock_extra_x=0;
stop_y=51.4; // male starts at 51.6: 0.2 axial clearance at nominal pose

module channel(){
    hull(){
        translate([3.92-dock_extra_x,50,25.94]) cube([15.16+2*dock_extra_x,25.8,.16]);
        translate([5.85-dock_extra_x,50,28.60]) cube([11.30+2*dock_extra_x,25.8,.16]);
    }
    translate([5.85-dock_extra_x,50,28.60]) cube([11.30+2*dock_extra_x,25.8,4.5]);
}
module stop_extension(){
    // Full-width solid stop joins floor and side walls. Stop is reached before
    // the enclosure touches the support links (~0.97 mm inward in V22).
    translate([1.25,49.9,23.7]) cube([20.5,stop_y-49.9,4.85]);
}
module dock_modifications(){
    difference(){
        union(){
            children();stop_extension();
            // Restore material above the old key slot before cutting a slot
            // 0.4 mm lower: roof becomes 0.57 mm instead of 0.17 mm.
            translate([1.25,72.15,27.98])cube([20.5,2.35,.57]);
        }
        // Channel widening is limited to the sliding portion, preserving stop.
        intersection(){channel();translate([-10,stop_y,20])cube([45,35,15]);}
        translate([.4,72.15,25.78])cube([22.2,2.35,2.2]);
    }
}
module mount(){dock_modifications() import("reference/mount_v22.stl",convexity=20);}
module receiver(){
    translate([-11.5,-61.4,-23.7]) dock_modifications()
        intersection(){
            import("reference/mount_v22.stl",convexity=20);
            translate([1.25,48.8,23.7]) cube([20.5,25.8,4.85]);
        }
}
module box(){import("reference/box_v22.stl",convexity=12);}
module lid(){import("reference/lid_v22.stl",convexity=12);}
module male_dovetail(){
    hull(){
        translate([-6.4,-12.6,-1.2])cube([10.8,19.6,.42]);
        translate([-8.1,-12.6,-3.45])cube([14.2,19.6,.30]);
    }
}
module coupon(){
    union(){translate([-11,-16,-1])cube([20,26,1]);male_dovetail();}
}
module installed_key(){
    translate([0,0,-.4])
    // Spring tongue runs along X, free at the left; anchor at X=13.5.
    // 12.95 mm free length, 0.8 mm thickness, 0.40 mm bending gap.
    // Slot roof Z=27.98; bump peak Z=28.25 requires ~0.27 mm deflection.
    union(){
        translate([.55,72.40,26.43])cube([22.40,1.78,.55]);
        translate([13.5,72.40,26.43])cube([9.45,1.78,1.65]);
        translate([.55,72.70,27.38])cube([13.2,1.15,.80]);
        // Gentle insertion ramp; exposed free end can be pressed to release.
        hull(){
            translate([.55,72.70,28.13])cube([.32,1.15,.52]);
            translate([1.05,72.70,28.13])cube([.22,1.15,.05]);
        }
        hull(){
            translate([22.80,72.05,26.43])cube([1,2.6,1.96]);
            translate([26,71.45,26.43])cube([.9,3.7,2.27]);
        }
    }
}
module key(){translate([-11.5,-61.4,-23.7])installed_key();}
module hook_coupon(){
    // Complete width and contact geometry of the hook and its outer bridge.
    // Only the long rear arms/dock are cropped away. Never use to carry a load.
    intersection(){mount();translate([-5,-10,-10])cube([35,22,45]);}
}
module location(up=false){
    if(up) translate([11.5,61.4,0])rotate([0,0,180])translate([-11.5,-61.4,0])translate([12.5,64.2,29.8])children();
    else translate([12.5,64.2,29.8])children();
}
module assembly(up=false){
    color("#4f6e83")mount();
    color("#d5ab64")location(up)box();
    color("#e6cb89")location(up)lid();
    color("#ee8555")installed_key();
}
assert(dock_extra_x>=0 && dock_extra_x<=.5,"dock_extra_x must be 0..0.5 mm");
assert(stop_y>=51.1 && stop_y<=51.5,"stop_y must be 51.1..51.5 mm");
if(part=="g7_mount")mount();
else if(part=="box")box();
else if(part=="lid")lid();
else if(part=="lock_key")key();
else if(part=="universal_receiver")receiver();
else if(part=="male_fit_coupon")coupon();
else if(part=="hook_fit_coupon")hook_coupon();
else if(part=="assembly_down")assembly(false);
else if(part=="assembly_up")assembly(true);
else assert(false,"Unknown part selector");
