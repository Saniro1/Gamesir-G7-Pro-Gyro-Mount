// V28: rounded, tangent-continuous curve; docking position unchanged from V27.
// Receiver box-facing surface remains recessed 5 mm inside the main bridge.
// Retains V25 main-base depth, 9 mm clips and 30 mm raised box position (10 mm lower than V26).
// Installed +Y is controller down; +Z is outward from the controller.
$fn=48;
part="assembly_down";
bridge_outer_z=26.5215;
receiver_inset=5;
receiver_face_z=bridge_outer_z-receiver_inset;
receiver_base_z=receiver_face_z-4.85;
box_translate_z=receiver_face_z+1.25; // box rear at local Z=-1, 0.25 gap
module clip(){
    intersection(){
        import("../printable/G7_Modular_v24_hook_fit_coupon.stl",convexity=16);
        translate([-5,-10,-10])cube([35,30,20.01]);
    }
}
// Quintic Bezier: vertical at the clip root, horizontal at the crown.
// Collinear, equally spaced end controls give zero curvature at the crown.
function quintic(p,t)=pow(1-t,5)*p[0]+5*pow(1-t,4)*t*p[1]+10*pow(1-t,3)*pow(t,2)*p[2]+10*pow(1-t,2)*pow(t,3)*p[3]+5*(1-t)*pow(t,4)*p[4]+pow(t,5)*p[5];
function smootherstep(t)=t*t*t*(10-15*t+6*t*t);
function upper_center(t)=quintic([[-5.37,10],[-5.37,14],[-5.37,18],[-1.3,24.6215],[2.7,24.6215],[6.7,24.6215]],t);
function upper_radius(t)=.81+1.09*smootherstep(t);
module upper_band(){
    // Swept discs form a consistently rounded band with a round end cap.
    // Taper smoothly from the original 1.62 mm root to a 3.8 mm crown.
    for(i=[0:63])hull(){
        translate(upper_center(i/64))circle(r=upper_radius(i/64),$fn=64);
        translate(upper_center((i+1)/64))circle(r=upper_radius((i+1)/64),$fn=64);
    }
}
module curved_bridge(){
    intersection(){
        multmatrix([[0,0,1,1.12],[1,0,0,0],[0,1,0,0],[0,0,0,1]])linear_extrude(height=20.75,convexity=16)upper_band();
        translate([-5,-10,10])cube([35,30,40]);
    }
}
module hook(){union(){clip();curved_bridge();}}
function lower_center(t)=[6.7+15.3*t,24.6215-8.9215*smootherstep(t)];
module lower_band(){
    // Horizontal tangent and zero curvature at both ends. The crown shares
    // position/tangent with the upper band, removing the pointed V27 join.
    for(i=[0:63])hull(){
        translate(lower_center(i/64))circle(r=1.9,$fn=64);
        translate(lower_center((i+1)/64))circle(r=1.9,$fn=64);
    }
    hull(){translate([22,15.7])circle(r=1.9,$fn=64);translate([41.9,15.7])circle(r=1.9,$fn=64);}
}
module curved_links(){
    for(x=[2.1,17.2])multmatrix([[0,0,1,x],[1,0,0,0],[0,1,0,0],[0,0,0,1]])linear_extrude(height=3.7,convexity=16)lower_band();
}
module receiver(){import("../printable/G7_Modular_v23_universal_receiver.stl",convexity=14);}
module box(){import("../printable/G7_Modular_v23_box.stl",convexity=14);}
module lid(){import("../printable/G7_Modular_v23_lid.stl",convexity=12);}
module key(){import("../printable/G7_Modular_v23_lock_key.stl",convexity=12);}
module coupon(){import("../printable/G7_Modular_v23_male_fit_coupon.stl",convexity=12);}
module installed_receiver(){translate([11.5,31.4,receiver_base_z])receiver();}
module mount(){union(){hook();curved_links();installed_receiver();}}
module hook_coupon(){hook();}
module location(up=false){
    if(up)translate([11.5,31.4,0])rotate([0,0,180])translate([-11.5,-31.4,0])translate([12.5,34.2,box_translate_z])children();
    else translate([12.5,34.2,box_translate_z])children();
}
module installed_key(){translate([11.5,31.4,receiver_base_z])key();}
module assembly(up=false){color("#4f6e83")mount();color("#d5ab64")location(up)box();color("#e6cb89")location(up)lid();color("#ee8555")installed_key();}
assert(receiver_inset==5,"The V28 curved links are designed for a 5 mm face inset");
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
