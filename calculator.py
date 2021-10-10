import numpy as np
from stl import mesh
import math
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
    ####################################################################################################
'''
'''
    Custom Errors
'''
## Line is completely within slicing plane
class LineIsOnPlaneException(Exception):
    def __init__(self):
        super().__init__("Line is on plane")

## When an array is compared to "None"
class NoneComparisionException(Exception):
    def __init__(self):
        super().__init__("An array was compared to \"None\"")

## Distance between points is 0
class ZeroDistanceException(Exception):
    def __init__(self):
        super().__init__("Distance between points is 0")





'''
    ####################################################################################################
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
        raise LineIsOnPlaneException()
    
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
    ####################################################################################################
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

    print("\n")

    ## vectors relative to l0
    d_p_l0 = p - l0     ## from l0 to p
    d_l1_l0 = l1 - l0   ## from l0 to l1

    # print("l0" + str(l0))
    # print("l1"+ str(l1))
    # print("p" + str(p))
    # print("dpl0"+ str(d_p_l0))
    # print("dl0l1" + str(d_l1_l0))

    cross = np.cross(d_p_l0, d_l1_l0) ## calculate cross product
    if (cross == 0): ## check if normal vector of 2 relative vectors is 0
        k_ac = np.dot(d_l1_l0, d_p_l0)  ## dot product of l0-l1 and l0-p
        k_ab = np.dot(d_l1_l0, d_l1_l0) ## dot product of l0-l1 and l0-l1

        # print("teef")
        if (0 < k_ac and k_ac < k_ab): ## if k_ac is less than k_ab and greater than 0 -> point is on line
            print("hoer")
            return True
        else:
            # print("bitch")
            return False
    else:
        return False





'''
    ##################################################
'''
'''
    ===== CALCULATE DISTANCE BETWEEN POINTS =====
    = 
    = 
    = p0 :: p1 -> distance, direction vector
    = 
    = (square root of (sum of (difference between corrosponding components) sqaured))
    = 
'''
def distance_between_points(p0: np.array, p1: np.array):
    return (
        math.sqrt(
            sum(
                [ math.pow(i,2) - pow(j,2)
                    for i,j in zip(p1, p0) ]
            )
        )
    )
    