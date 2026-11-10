// V29: rigidly tilt slider so its bottom edge is 5 mm closer to the shell.
// Upper slider edge is the fixed pivot; the mating profile is not warped.
// Receiver upper edge is recessed 5 mm; lower edge is an additional 5 mm inward.
// Use tools/build.sh 29 for robust manifold union of rotated imported meshes.
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
tilt_angle=-asin(5/25.8);
hinge_y=18.8;
hinge_z=receiver_face_z;
function tilt_yz(p)=[hinge_y+cos(tilt_angle)*(p[0]-hinge_y)-sin(tilt_angle)*(p[1]-hinge_z),hinge_z+sin(tilt_angle)*(p[0]-hinge_y)+cos(tilt_angle)*(p[1]-hinge_z)];
module dock_tilt(){translate([0,hinge_y,hinge_z])rotate([tilt_angle,0,0])translate([0,-hinge_y,-hinge_z])children();}
function lower_center(t)=let(c=[6.7,24.6215],e=tilt_yz([22,15.7]),d=[cos(tilt_angle),sin(tilt_angle)])quintic([c,c+[4,0],c+[8,0],e-6*d,e-3*d,e],t);
module lower_band(){
    // Horizontal crown tangent and tilted receiver tangent, zero endpoint curvature.
    // The crown shares
    // position/tangent with the upper band, removing the pointed V27 join.
    for(i=[0:63])hull(){
        translate(lower_center(i/64))circle(r=1.9,$fn=64);
        translate(lower_center((i+1)/64))circle(r=1.9,$fn=64);
    }
    hull(){translate(tilt_yz([22,15.7]))circle(r=1.9,$fn=64);translate(tilt_yz([41.9,15.7]))circle(r=1.9,$fn=64);}
}
module curved_links(){
    for(x=[2.1,17.2])multmatrix([[0,0,1,x],[1,0,0,0],[0,1,0,0],[0,0,0,1]])linear_extrude(height=3.7,convexity=16)lower_band();
}
module receiver(){import("../printable/G7_Modular_v23_universal_receiver.stl",convexity=14);}
module box(){import("../printable/G7_Modular_v23_box.stl",convexity=14);}
module lid(){import("../printable/G7_Modular_v23_lid.stl",convexity=12);}
module key(){import("../printable/G7_Modular_v23_lock_key.stl",convexity=12);}
module coupon(){import("../printable/G7_Modular_v23_male_fit_coupon.stl",convexity=12);}
module installed_receiver(){dock_tilt()render()translate([11.5,31.4,receiver_base_z])receiver();}
module mount(){union(){hook();curved_links();installed_receiver();}}
module hook_coupon(){hook();}
module location(up=false){
    dock_tilt(){
    if(up)translate([11.5,31.4,0])rotate([0,0,180])translate([-11.5,-31.4,0])translate([12.5,34.2,box_translate_z])children();
    else translate([12.5,34.2,box_translate_z])children();
    }
}
module installed_key(){dock_tilt()translate([11.5,31.4,receiver_base_z])key();}
module assembly(up=false){color("#4f6e83")mount();color("#d5ab64")location(up)box();color("#e6cb89")location(up)lid();color("#ee8555")installed_key();}
assert(receiver_inset==5,"The V29 curved links are designed for a 5 mm face inset");
if(part=="g7_mount")mount();
else if(part=="build_hook")hook();
else if(part=="build_links")curved_links();
else if(part=="build_receiver")installed_receiver();
else if(part=="box")box();
else if(part=="lid")lid();
else if(part=="lock_key")key();
else if(part=="universal_receiver")receiver();
else if(part=="male_fit_coupon")coupon();
else if(part=="hook_fit_coupon")hook_coupon();
else if(part=="assembly_down")assembly(false);
else if(part=="assembly_up")assembly(true);
else assert(false,"Unknown part selector");
