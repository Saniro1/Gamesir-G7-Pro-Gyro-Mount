// V24: 9 mm top clips and dock raised 40 mm relative to V23.
// Installed +Y is controller DOWN; +Z is outward from the controller.
// Width/thickness of both clips and the Box 2 interface are preserved.
$fn=48;
part="assembly_down";
clip_shortening=1; // V23 clips are 10 mm long; V24 default is 9 mm.
dock_raise=40;
dock_outward=8; // Clears the existing upper bend at the raised position.
old_clip_tip=-7.9;
module previous_mount(){import("../printable/G7_Modular_v23_g7_mount.stl",convexity=20);}
module shortened_hook(){
    intersection(){
        previous_mount();
        // Preserve both cheeks and the upper curve. Remove the old long arms
        // and receiver, and trim 1 mm from the clip free ends, not their sides.
        translate([-5,-10,old_clip_tip+clip_shortening])cube([35,24.2,60]);
    }
}
module receiver(){import("../printable/G7_Modular_v23_universal_receiver.stl",convexity=14);}
module box(){import("../printable/G7_Modular_v23_box.stl",convexity=14);}
module lid(){import("../printable/G7_Modular_v23_lid.stl",convexity=12);}
module key(){import("../printable/G7_Modular_v23_lock_key.stl",convexity=12);}
module coupon(){import("../printable/G7_Modular_v23_male_fit_coupon.stl",convexity=12);}
module installed_receiver(){translate([11.5,61.4-dock_raise,23.7+dock_outward])receiver();}
module support_links(){
    // Permanent structural arms, NOT print supports. Their upper faces stay
    // below the receiver floor so they cannot enter the dovetail channel.
    for(x=[2.1,17.2])
        translate([x,8.0,28.2])cube([3.7,25.8,4.4]);
}
module mount(){union(){shortened_hook();support_links();installed_receiver();}}
module hook_coupon(){
    intersection(){shortened_hook();translate([-5,-10,-10])cube([35,22,45]);}
}
module location(up=false){
    if(up)
        translate([11.5,61.4-dock_raise,0])rotate([0,0,180])
        translate([-11.5,-(61.4-dock_raise),0])
        translate([12.5,64.2-dock_raise,29.8+dock_outward])children();
    else translate([12.5,64.2-dock_raise,29.8+dock_outward])children();
}
module installed_key(){translate([11.5,61.4-dock_raise,23.7+dock_outward])key();}
module assembly(up=false){
    color("#4f6e83")mount();
    color("#d5ab64")location(up)box();
    color("#e6cb89")location(up)lid();
    color("#ee8555")installed_key();
}
assert(clip_shortening>=0 && clip_shortening<=2,"Clip shortening must be 0..2 mm");
// Structural links are designed and validated for this exact dock position.
assert(dock_raise==40 && dock_outward==8,"V24 structural links require a 40 mm raise and 8 mm outward offset");
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
