// V32 lid: slightly closer sliding fit, with local friction pads.
// USB access and snap-detent reliefs are preserved; neither is a locking-key hole.
part="lid";
side_inset=.15;
roof_drop=.10;
pad_projection=.23; // nominal rail-side clearance .20 => .03 mm local preload
module friction_pad(left=true,y=0){
    inner=left ? -14.7+side_inset : 12.7-side_inset;
    hull(){
        translate([left?inner-.04:inner-.01,y-1.5,21.95])cube([.05,3,.55]);
        translate([left?inner-.01:inner-pad_projection,y-.6,21.95])cube([pad_projection+.01,1.2,.55]);
    }
}
module lid(){
    difference(){
        union(){
            translate([-15.55,-17.60,23.75-roof_drop])cube([29.10,29.70,1.90]);
            translate([-15.55+side_inset,-16.45,21.10])cube([.85,27.2,2.65-roof_drop]);
            translate([12.70-side_inset,-16.45,21.10])cube([.85,27.2,2.65-roof_drop]);
            translate([-14.70+side_inset,-16.45,21.10])cube([.72,27.2,.50]);
            translate([11.98-side_inset,-16.45,21.10])cube([.72,27.2,.50]);
            translate([-4.75,-19.70,23.75-roof_drop])cube([7.5,2.3,1.90]);
            for(y=[-10,-3,4]){friction_pad(true,y);friction_pad(false,y);}
        }
        // Existing snap-detent reliefs, not locking-key holes.
        translate([-15.7,7.70,21.68])cube([1.40,1.75,1.40]);
        translate([12.35,7.70,21.68])cube([1.40,1.75,1.40]);
        translate([-8.7,8.65,23.20])cube([15.4,5.10,3.20]);
    }
}

module channel(){
 hull(){translate([-7.58,-20,2.24])cube([15.16,40,.16]);translate([-5.65,-20,4.9])cube([11.3,40,.16]);}
 translate([-5.65,-20,4.9])cube([11.3,40,5]);
}
module slot_fill(){difference(){translate([-10.25,10.75,2.08])cube([20.5,2.35,2.2]);channel();}}
module receiver(){union(){import("../printable/G7_Modular_v31_universal_receiver.stl",convexity=12);slot_fill();}}
if(part=="lid")lid();
else if(part=="universal_receiver")receiver();
else if(part=="slot_fill")slot_fill();
else if(part=="g7_mount")assert(false,"Build the mounted patch with tools/build_v32.py");
else import(str("../printable/G7_Modular_v31_",part,".stl"),convexity=20);
