import numpy as np
from stl import mesh
import math
'''
    ##### CALCULATOR FUNCTIONS #####
    #
    #   isect_line_plane(l0,l1,pc,pn):
    #       find intersection point of a line with a plane.
    #       - return 1 point if found
    #       - return both points if within plane
    #       - return none if no intersections
    #
    #
    #

    ##### CALCULATOR TODO's
    TODO: asdf
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
    ## Line lies within plane
    if (l0[2] == pc[2] and l1[2] == pc[2]):
        raise LineIsOnPlaneException()
    
    ## Line does not intersect plane
    if not(l0[2] < pc[2] < l1[2] or l1[2] < pc[2] < l1[2]):
        raise Exception()

    ld = l1-l0 ## calculate difference between start and end of line
    dot = np.dot(pn, ld) ## dot product of plane normal and difference
    
    ## from now on we basically work with vectors relative to l0
    if abs(dot)>epsilon:            ## if dot product > 0 -> line intersects plane
        w = l0 - pc                 ## line from line_start to plane_coordinate
        fac = -(np.dot(pn, w))/dot  ## factor to scale ld with
        new = ld * fac              ## scale ld with that factor
        out = new + l0              ## add line_start to return to a vector relative to Origin

        return out                  ## return new vector
    else:
        raise Exception()





'''
    ##################################################
'''
'''
    ===== CALCULATE DISTANCE BETWEEN POINTS =====
    = 
    = 
    = p0 :: p1 -> distance, direction vector
    = 
    = (square root of (absolute of(sum of (difference between corrosponding components) sqaured)))
    = 
'''
def distance_between_points(p0: np.array, p1: np.array): # TODO give more info for this fucky calculation
    return (
        math.sqrt(
            sum(
                [ math.pow(i-j,2)
                    for i,j in zip(p1, p0) ]
            )
        )
    )