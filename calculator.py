import numpy as np
from stl import mesh
'''
    ##### CALCULATOR FUNCTIONS #####
    #
    #
    #
    #
    #

    ##### CALCULATOR TODO's
    TODO: in isect_line_plane() -> if all "z"-values are equal line is on plane -> should return both points instead of raising Exception, or return customException
    TODO: ignore points already on a line to ensure to double extrusion over line segment
    TODO:
'''
'''
    ##################################################
'''
''' 
    ===== FIND INTERSECTION =====
    = This function is to find the intersection between a line-segment and a plane
    = 
    = l0 :: l1 :: pc :: pn :: epsilon(default = 1e-6) -> intersect_point
    = 
    = l0: line start
    = l1: line end
    = pc: plane coordinate, coordinate on plane
    = pn: plane normal, vector purpendicular to plane
    = epsilon: correction for 0, due to loss of accuracy in converting between float32 and internally used float64 -> 1e-6 = 1*10^-6, is a close enough approximation
    ============================= 
'''
def isect_line_plane(l0:np.array, l1: np.array, pc: np.array, pn: np.array, epsilon = 1e-6):
    if (l0[2] == pc[2] and l1[2] == pc[2]): # line is on plane ##TODO: return both points as intersecting points
        raise Exception()
    
    ld = l1-l0 # calculate difference between start and end of line
    dot = np.dot(pn, ld) # dot product of plane normal and difference
    # from now on we basically work with vectors relative to l0

    if abs(dot)>epsilon:            # if dot product > 0 -> line intersects plane
        w = l0 - pc                 # line from line_start to plane_coordinate
        fac = -(np.dot(pn, w))/dot  # factor to scale ld with
        new = ld * fac              # scale ld with that factor
        out = new + l0              # add line_start to return to a vector relative to Origin

        return out  # return new vector
    else: # 
        raise Exception()




'''
    ##################################################
'''
'''
    ===== CHECK IF POINT IS ON LINE =====
    = This function is to check if a point is already on a line segment;
    = if so, it can be ignored to reduce amount of perimiter points
    = 
    = l0 :: l1 :: p -> Boolean
    = 
    = l0: start of line
    = l1: end of line
    = p: any point
    =====================================
'''
def point_is_on_line(l0: np.array, l1: np.array, p: np.array, epsilon = 1e-6):
    # ignore z-component as all points are already in a plane
    l0 = l0[:2] 
    l1 = l1[:2]
    p = p[:2]

    # vectors relative to l0
    d_p_l0 = p - l0
    d_l1_l0 = l1 - l0

    cross = np.cross(d_p_l0, d_l1_l0)
    if (cross == 0): # check if normal vector of 2 relative vectors is 0
        k_ac = np.dot(d_l1_l0, d_p_l0)
        k_ab = np.dot(d_l1_l0, d_l1_l0)

        if (0 < k_ac < k_ab):
            return True
        else:
            return False ##

    