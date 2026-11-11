"""Explicit, separate 0.45 mm peel sheets derived from vertical mesh intersections.

Supports are disposable model shells, not auto-generated support blocks. Air gaps
are physical mesh gaps; automatic generation must remain off (normal/manual, without enforcers).
"""
import numpy as np
import trimesh

THICKNESS=.45
TOP_GAP=.32
BOTTOM_GAP=.32
PITCH=3.0
CELL=.4
PANEL=8.0
TEAR_GAP=.8


def vertical_hits(mesh, x, ys):
    """Sorted unique vertical triangle crossings, without optional ray libraries."""
    out=[[] for _ in ys]
    for tri,normal in zip(mesh.triangles,mesh.face_normals):
        a,b,c=tri
        den=(b[1]-c[1])*(a[0]-c[0])+(c[0]-b[0])*(a[1]-c[1])
        if abs(den)<1e-10 or x<tri[:,0].min()-1e-8 or x>tri[:,0].max()+1e-8:continue
        idx=np.flatnonzero((ys>=tri[:,1].min()-1e-8)&(ys<=tri[:,1].max()+1e-8))
        y=ys[idx]
        u=((b[1]-c[1])*(x-c[0])+(c[0]-b[0])*(y-c[1]))/den
        v=((c[1]-a[1])*(x-c[0])+(a[0]-c[0])*(y-c[1]))/den
        w=1-u-v
        for i,z in zip(idx[(u>=-1e-8)&(v>=-1e-8)&(w>=-1e-8)],(u*a[2]+v*b[2]+w*c[2])[(u>=-1e-8)&(v>=-1e-8)&(w>=-1e-8)]):out[i].append((float(z),float(normal[2])))
    for i,row in enumerate(out):
        clean=[]
        for z,n in sorted(row):
            if not clean or z-clean[-1][0]>1e-5:clean.append((z,n))
        out[i]=clean
    return out


def air_interval(row,mid):
    floor=0.
    for i,(z,n) in enumerate(row):
        if z>mid:
            if i%2: return None # midpoint is inside solid
            return floor,z,n
        floor=z
    return floor,float('inf'),0.


def make_sheets(mesh, sheet_xs=None):
    width,depth,height=mesh.extents
    xs=list(np.arange(.85,width-.5,PITCH))
    # Fine hook tongues must each have a sheet under them, not miss a coarse grid.
    if width<24:
        for x in [1.75,width-1.75]:
            xs=[a for a in xs if abs(a-x)>1.6]+[x]
    xs=sorted(xs if sheet_xs is None else sheet_xs)
    ys=np.arange(.25,depth-.1,CELL)
    pieces=[];records=[]
    for x in xs:
        rows=vertical_hits(mesh,x,ys)
        # Conservative corner samples keep sheets clear of neighboring solids.
        neighbors=[vertical_hits(mesh,x+dx,ys+dy) for dx in [-THICKNESS/2-.25,THICKNESS/2+.25] for dy in [-CELL/2-.25,CELL/2+.25]]
        groups={}
        for j,(y,row) in enumerate(zip(ys,rows)):
            floor=0.
            for i,(ceiling,n) in enumerate(row):
                if i%2:
                    floor=ceiling;continue
                if n>-.70 or ceiling-floor<TOP_GAP+BOTTOM_GAP+.4:continue
                mid=(floor+ceiling)/2
                intervals=[air_interval(rr[j],mid) for rr in neighbors]
                if any(a is None for a in intervals):continue
                lo=max([floor]+[a[0] for a in intervals]);hi=min([ceiling]+[a[1] for a in intervals])
                bottom=0 if lo<1e-5 else lo+BOTTOM_GAP
                top=hi-TOP_GAP
                if top-bottom<.4:continue
                # Independent 8 mm long sheets separated by 0.8 mm tear channels.
                panel=int(y/(PANEL+TEAR_GAP))
                if y-panel*(PANEL+TEAR_GAP)>PANEL-CELL/2:continue
                box=trimesh.creation.box(extents=[THICKNESS,CELL,top-bottom]);box.apply_translation([x,y,(top+bottom)/2])
                groups.setdefault((panel,i),[]).append(box)
        for (panel,band),boxes in groups.items():
            m=trimesh.boolean.union(boxes,engine='manifold')
            for sheet in m.split():
                if sheet.extents[1]<.79:continue
                # Individual feet, never a shared raft joining sheets.
                if sheet.bounds[0,2]<1e-5:
                    foot=trimesh.creation.box(extents=[1.4,sheet.extents[1],.2]);foot.apply_translation([x,sheet.bounds[:,1].mean(),.1])
                    hit=trimesh.boolean.intersection([foot,mesh],engine='manifold')
                    if len(hit.faces)==0 or abs(hit.volume)<1e-6:
                        sheet=trimesh.boolean.union([sheet,foot],engine='manifold')
                assert sheet.is_watertight
                pieces.append(sheet)
                records.append(dict(x_mm=float(x),bounds_mm=sheet.bounds.tolist(),volume_mm3=float(sheet.volume)))
    if not pieces:return None,[]
    support=trimesh.util.concatenate(pieces)
    hit=trimesh.boolean.intersection([support,mesh],engine='manifold')
    assert len(hit.faces)==0 or abs(hit.volume)<1e-5
    return support,records
