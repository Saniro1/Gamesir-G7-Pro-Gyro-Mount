"""Installed docking transforms, in millimeters; +Y down, +Z outward."""
import numpy as np

def dock_tilt(version):
    m=np.eye(4)
    if version<29:return m
    inward=10. if version>=34 else 5.
    angle=-np.arcsin(inward/25.8)
    c,s=np.cos(angle),np.sin(angle)
    m[:3,:3]=[[1,0,0],[0,c,-s],[0,s,c]]
    pivot=np.array([0.,18.8,21.5215])
    m[:3,3]=pivot-m[:3,:3]@pivot
    return m

def transform_points(points,m):
    return np.asarray(points)@m[:3,:3].T+m[:3,3]
