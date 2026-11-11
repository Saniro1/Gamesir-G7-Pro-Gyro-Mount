// V33: extend both under-rail return lips by 0.60 mm; V32 fit otherwise retained.
// USB access and snap-detent reliefs are preserved; neither is a locking-key hole.
part="lid";
side_inset=.15;
roof_drop=.10;
lip_reach=1.32; // V32 was .72 mm
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
            translate([-14.70+side_inset,-16.45,21.10])cube([lip_reach,27.2,.50]);
            translate([12.70-side_inset-lip_reach,-16.45,21.10])cube([lip_reach,27.2,.50]);
            translate([-4.75,-19.70,23.75-roof_drop])cube([7.5,2.3,1.90]);
            for(y=[-10,-3,4]){friction_pad(true,y);friction_pad(false,y);}
        }
        // Existing snap-detent reliefs, not locking-key holes.
        translate([-15.7,7.70,21.68])cube([1.40,1.75,1.40]);
        translate([12.35,7.70,21.68])cube([1.40,1.75,1.40]);
        translate([-8.7,8.65,23.20])cube([15.4,5.10,3.20]);
    }
}

if(part=="lid")lid();
else import(str("../printable/G7_Modular_v32_",part,".stl"),convexity=20);
