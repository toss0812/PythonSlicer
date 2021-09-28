import numpy as np
from stl import mesh

def isect_line_plane(l0:np.array, l1: np.array, pc: np.array, pn: np.array, epsilon = 1e-6):
    if (l0[2] == pc[2] and l1[2] == pc[2]): # line is on plane
        raise Exception()
    
    ld = l1-l0
    dot = np.dot(pn, ld)

    if abs(dot)>epsilon:
        w = l0 - pc
        fac = -(np.dot(pn, w))/dot
        new = ld * fac
        out = new + l0

        return out
    else:
        raise Exception()
    