// V30: controller insertion tongues 0.5 mm smaller on each cross-section face.
// Insertion length stays 9 mm. V29 receiver position/tilt is unchanged.
// Use tools/build.sh 30 for robust finished mesh union.
part="assembly_down";
module old_hook(){import("../printable/G7_Modular_v29_hook_fit_coupon.stl",convexity=20);}
module small_tab(x){
    // Original tongue: X=x..x+3.5, Y=-1.3..1.2, Z=-6.9..2.1.
    // Resize about its section center only; never scale insertion length Z.
    translate([x+1.75,-.05,0])scale([2.5/3.5,1.5/2.5,1])translate([-x-1.75,.05,0])
        intersection(){old_hook();translate([x-.01,-1.3,-6.91])cube([3.52,2.51,9.02]);}
}
module clip_neck(x){
    // Retain the attachment leg and its full root. Blend to the narrower tongue.
    hull(){
        intersection(){old_hook();translate([x+.5,-2,-6.9])cube([2.5,.1,9]);}
        intersection(){small_tab(x);translate([x+.49,-.8,-6.91])cube([2.52,.1,9.02]);}
    }
}
module hook(){
    union(){
        difference(){old_hook();
            for(x=[.25,19.25])translate([x-.01,-2,-6.91])cube([3.52,3.21,9.02]);
        }
        for(x=[.25,19.25]){small_tab(x);clip_neck(x);}
    }
}
module receiver(){import("../printable/G7_Modular_v23_universal_receiver.stl",convexity=14);}
module box(){import("../printable/G7_Modular_v23_box.stl",convexity=14);}
module lid(){import("../printable/G7_Modular_v23_lid.stl",convexity=12);}
module key(){import("../printable/G7_Modular_v23_lock_key.stl",convexity=12);}
module coupon(){import("../printable/G7_Modular_v23_male_fit_coupon.stl",convexity=12);}
receiver_face_z=21.5215;
function quintic(p,t)=pow(1-t,5)*p[0]+5*pow(1-t,4)*t*p[1]+10*pow(1-t,3)*pow(t,2)*p[2]+10*pow(1-t,2)*pow(t,3)*p[3]+5*(1-t)*pow(t,4)*p[4]+pow(t,5)*p[5];
function smootherstep(t)=t*t*t*(10-15*t+6*t*t);
function upper_center(t)=quintic([[-5.37,10],[-5.37,14],[-5.37,18],[-1.3,24.6215],[2.7,24.6215],[6.7,24.6215]],t);
function upper_radius(t)=.81+1.09*smootherstep(t);

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

module old_components(p){if(p=="build_links")curved_links();else dock_tilt()translate([11.5,31.4,16.6715])receiver();}
module mount(){union(){hook();old_components("build_links");old_components("build_receiver");}}
module dock(){translate([0,18.8,21.5215])rotate([-asin(5/25.8),0,0])translate([0,-18.8,-21.5215])children();}
module placed(up=false){dock(){if(up)translate([11.5,31.4,0])rotate([0,0,180])translate([-11.5,-31.4,0])translate([12.5,34.2,22.7715])children();else translate([12.5,34.2,22.7715])children();}}
if(part=="g7_mount")mount();
else if(part=="build_hook"||part=="hook_fit_coupon")hook();
else if(part=="build_links"||part=="build_receiver")old_components(part);
else if(part=="box")box();
else if(part=="lid")lid();
else if(part=="lock_key")key();
else if(part=="universal_receiver")receiver();
else if(part=="male_fit_coupon")coupon();
else {mount();placed(part=="assembly_up")box();placed(part=="assembly_up")lid();dock()translate([11.5,31.4,16.6715])key();}
