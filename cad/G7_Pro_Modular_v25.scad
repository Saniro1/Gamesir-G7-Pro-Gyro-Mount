// V25: V23-style curved bridge, moved 5 mm inward relative to V24.
// The 9 mm clips and 40 mm raised docking position are retained.
// Installed +Y is controller DOWN; +Z is outward from the shell.
$fn=48;
part="assembly_down";
dock_raise=40;
dock_outward=3; // V24 was +8: this is 5 mm closer to the controller.
curve_steps=8;
function cr(p0,p1,p2,p3,t)=.5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t*t+(-p0+3*p1-3*p2+p3)*t*t*t);
function smooth_path(p)=concat([for(i=[0:len(p)-2],j=[0:curve_steps-1])cr(p[max(0,i-1)],p[i],p[i+1],p[min(len(p)-1,i+2)],j/curve_steps)],[p[len(p)-1]]);
function smoothstep(t)=t*t*(3-2*t);
// Preserve the clip/root below Z=10. Ease into a full 5 mm inward shift
// by Z=28, with continuous tangents at both ends of the transition.
function recessed(p)= [p[0],p[1]-5*smoothstep(min(1,max(0,(p[1]-10)/18)))];
module clip(){
    intersection(){
        import("../printable/G7_Modular_v24_hook_fit_coupon.stl",convexity=16);
        translate([-5,-10,-10])cube([35,30,20.01]);
    }
}
module curved_bridge(){
    // Original V23 wide curved-cheek paths, reconstructed as a proper polygon
    // and re-extruded after the inward easing, rather than warping triangles.
    outer=smooth_path([[11.60,31.46],[8.70,31.47],[5.30,30.72],[2.20,28.65],[-.50,25.55],[-2.65,22.20],[-4.30,18.65],[-5.55,15.10],[-6.18,12.25]]);
    inner=smooth_path([[-4.56,11.9],[-4.36,13.2],[-2.40,15.1],[-.40,18.5],[1.30,21.45],[3.80,25.10],[7,29],[11.60,30.1]]);
    profile=[for(p=concat(outer,[[-6.18,-7.2],[-4.56,-7.2]],inner))recessed(p)];
    intersection(){
        multmatrix([[0,0,1,1.12],[1,0,0,0],[0,1,0,0],[0,0,0,1]])linear_extrude(height=20.75,convexity=16)polygon(profile);
        translate([-5,-10,10])cube([35,30,40]);
    }
}
module hook(){union(){clip();curved_bridge();}}
function bezier(a,b,c,d,t)=pow(1-t,3)*a+3*pow(1-t,2)*t*b+3*(1-t)*t*t*c+pow(t,3)*d;
module curved_links(){
    // Permanent curved structural links: 3.7 mm wide and 3.8 mm deep.
    // Their upper surfaces stay below the channel floor at installed Z=29.1.
    top=[for(i=[0:24])bezier([5,26],[8.5,26],[10.5,27.6],[16,27.6],i/24)];
    bottom=[for(i=[0:24])bezier([16,23.8],[10.5,23.8],[8.5,22.2],[5,22.2],i/24)];
    profile=concat(top,[[33.8,27.6],[33.8,23.8],[16,23.8]],bottom);
    for(x=[2.1,17.2])multmatrix([[0,0,1,x],[1,0,0,0],[0,1,0,0],[0,0,0,1]])linear_extrude(height=3.7,convexity=16)polygon(profile);
}
module receiver(){import("../printable/G7_Modular_v23_universal_receiver.stl",convexity=14);}
module box(){import("../printable/G7_Modular_v23_box.stl",convexity=14);}
module lid(){import("../printable/G7_Modular_v23_lid.stl",convexity=12);}
module key(){import("../printable/G7_Modular_v23_lock_key.stl",convexity=12);}
module coupon(){import("../printable/G7_Modular_v23_male_fit_coupon.stl",convexity=12);}
module installed_receiver(){translate([11.5,21.4,26.7])receiver();}
module mount(){union(){hook();curved_links();installed_receiver();}}
module hook_coupon(){hook();}
module location(up=false){
    if(up)translate([11.5,21.4,0])rotate([0,0,180])translate([-11.5,-21.4,0])translate([12.5,24.2,32.8])children();
    else translate([12.5,24.2,32.8])children();
}
module installed_key(){translate([11.5,21.4,26.7])key();}
module assembly(up=false){
    color("#4f6e83")mount();color("#d5ab64")location(up)box();color("#e6cb89")location(up)lid();color("#ee8555")installed_key();
}
assert(dock_raise==40 && dock_outward==3,"V25 links require a 40 mm raise and 3 mm outward offset from V23");
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
