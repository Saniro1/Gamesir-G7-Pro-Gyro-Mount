// V34: additional 5 mm inward displacement at the receiver lower face.
// Upper receiver edge stays fixed; cumulative lower-edge shift is 10 mm from V28.
part="g7_mount";
module hook(){import("../printable/G7_Modular_v33_hook_fit_coupon.stl",convexity=20);}
module receiver(){import("../printable/G7_Modular_v33_universal_receiver.stl",convexity=20);}
receiver_face_z=21.5215;
function quintic(p,t)=pow(1-t,5)*p[0]+5*pow(1-t,4)*t*p[1]+10*pow(1-t,3)*pow(t,2)*p[2]+10*pow(1-t,2)*pow(t,3)*p[3]+5*(1-t)*pow(t,4)*p[4]+pow(t,5)*p[5];
function smootherstep(t)=t*t*t*(10-15*t+6*t*t);
function upper_center(t)=quintic([[-5.37,10],[-5.37,14],[-5.37,18],[-1.3,24.6215],[2.7,24.6215],[6.7,24.6215]],t);
function upper_radius(t)=.81+1.09*smootherstep(t);

tilt_angle=-asin(10/25.8);
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


module installed_receiver(){dock_tilt()translate([11.5,31.4,16.6715])receiver();}
if(part=="build_links")curved_links();
else if(part=="build_hook"||part=="hook_fit_coupon")hook();
else if(part=="build_receiver")installed_receiver();
else if(part=="g7_mount")union(){hook();curved_links();installed_receiver();}
else import(str("../printable/G7_Modular_v33_",part,".stl"),convexity=20);
