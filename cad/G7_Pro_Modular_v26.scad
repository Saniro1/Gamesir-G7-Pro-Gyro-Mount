// V26: receiver box-facing surface recessed 5 mm inside the main bridge.
// Retains V25 main-base depth, 9 mm clips and 40 mm raised box position.
// Installed +Y is controller down; +Z is outward from the controller.
$fn=48;
part="assembly_down";
bridge_outer_z=26.5215;
receiver_inset=5;
receiver_face_z=bridge_outer_z-receiver_inset;
receiver_base_z=receiver_face_z-4.85;
box_translate_z=receiver_face_z+1.25; // box rear at local Z=-1, 0.25 gap
curve_steps=8;
function cr(p0,p1,p2,p3,t)=.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t);
function smooth_path(p)=concat([for(i=[0:len(p)-2],j=[0:curve_steps-1])cr(p[max(0,i-1)],p[i],p[i+1],p[min(len(p)-1,i+2)],j/curve_steps)],[p[len(p)-1]]);
function smoothstep(t)=t*t*(3-2*t);
// Depth of main base is unchanged from V25. Turn earlier in Y so that the
// raised box's front wall can pass without striking the upper bridge.
function compact(p)=[p[0]-6.2*smoothstep(min(1,max(0,p[0]/11.6))),p[1]-5*smoothstep(min(1,max(0,(p[1]-10)/18)))];
module clip(){
    intersection(){
        import("../printable/G7_Modular_v24_hook_fit_coupon.stl",convexity=16);
        translate([-5,-10,-10])cube([35,30,20.01]);
    }
}
module curved_bridge(){
    outer=smooth_path([[11.60,31.46],[8.70,31.47],[5.30,30.72],[2.20,28.65],[-.50,25.55],[-2.65,22.20],[-4.30,18.65],[-5.55,15.10],[-6.18,12.25]]);
    inner=smooth_path([[-4.56,11.9],[-4.36,13.2],[-2.40,15.1],[-.40,18.5],[1.30,21.45],[3.80,25.10],[7,29],[11.60,30.1]]);
    profile=[for(p=concat(outer,[[-6.18,-7.2],[-4.56,-7.2]],inner))compact(p)];
    intersection(){
        multmatrix([[0,0,1,1.12],[1,0,0,0],[0,1,0,0],[0,0,0,1]])linear_extrude(height=20.75,convexity=16)polygon(profile);
        translate([-5,-10,10])cube([35,30,40]);
    }
}
module hook(){union(){clip();curved_bridge();}}
function bezier(a,b,c,d,t)=pow(1-t,3)*a+3*pow(1-t,2)*t*b+3*(1-t)*t*t*c+pow(t,3)*d;
module curved_links(){
    // Curved downward step. Keep the links below the box's rear surface by
    // the time Y reaches its leading wall (~6.6..6.7 in either USB direction).
    top=[for(i=[0:32])bezier([2.2,25.8],[6,25.8],[6,17.6],[10.5,17.6],i/32)];
    bottom=[for(i=[0:32])bezier([10.5,13.8],[2.2,13.8],[2.2,22],[2.2,22],i/32)];
    profile=concat(top,[[33.8,17.6],[33.8,13.8],[10.5,13.8]],bottom);
    for(x=[2.1,17.2])multmatrix([[0,0,1,x],[1,0,0,0],[0,1,0,0],[0,0,0,1]])linear_extrude(height=3.7,convexity=16)polygon(profile);
}
module receiver(){import("../printable/G7_Modular_v23_universal_receiver.stl",convexity=14);}
module box(){import("../printable/G7_Modular_v23_box.stl",convexity=14);}
module lid(){import("../printable/G7_Modular_v23_lid.stl",convexity=12);}
module key(){import("../printable/G7_Modular_v23_lock_key.stl",convexity=12);}
module coupon(){import("../printable/G7_Modular_v23_male_fit_coupon.stl",convexity=12);}
module installed_receiver(){translate([11.5,21.4,receiver_base_z])receiver();}
module mount(){union(){hook();curved_links();installed_receiver();}}
module hook_coupon(){hook();}
module location(up=false){
    if(up)translate([11.5,21.4,0])rotate([0,0,180])translate([-11.5,-21.4,0])translate([12.5,24.2,box_translate_z])children();
    else translate([12.5,24.2,box_translate_z])children();
}
module installed_key(){translate([11.5,21.4,receiver_base_z])key();}
module assembly(up=false){color("#4f6e83")mount();color("#d5ab64")location(up)box();color("#e6cb89")location(up)lid();color("#ee8555")installed_key();}
assert(receiver_inset==5,"The V26 curved links are designed for a 5 mm face inset");
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
