import numpy as np
from stl import mesh


'''
    l0: line start
    l1: line end
    pc: plane coordinate, coordinate on plane
    pn: plane normal, vector purpendicular to plane
'''
def isect_line_plane(l0:np.array, l1: np.array, pc: np.array, pn: np.array, epsilon = 1e-6):
    if (l0[2] == pc[2] and l1[2] == pc[2]): # line is on plane
        raise Exception()
    
    ld = l1-l0 # calculate difference between start and end of line
    dot = np.dot(pn, ld) # dot product of plane normal and difference

    if abs(dot)>epsilon: # if dot product != 0 -> line intersects plane
        w = l0 - pc
        fac = -(np.dot(pn, w))/dot
        new = ld * fac
        out = new + l0

        return out
    else:
        raise Exception()
    