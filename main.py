from calculator import *
from reader import *
import itertools as it
import numpy as np          ## ignore the error message

'''
    ##### MAIN FUNCTIONS #####
    #
    #
    #
    #
    #

    ##### CALCULATOR TODO's
    TODO: make program loop through all layers
'''

## ========== CONDENSE
## Reduces a list of 3D Vectors to only have unique entries
def distill(to_condense: list):
    temp = np.unique(to_condense, axis=0) # find unique entries in list, axis=0 -> otherwise 2d array will be flattened and will return unique values of all entries
    ## Funny thing, numpy.unique() also sorts list on chosen axis, based on first entry basis
    return temp.tolist()



## ========== MAIN THINGS
my_mesh = read("untitled v0.stl") # simple cube with sides of length = 10

# print(my_mesh.points) 
'''
this is a representation of an .stl polygon in a numpy.ndarray
dtype = float32
[
    [x0, y0, z0, x1, y1, z1, x2, y2, z2],
    ...
    ..
    .
]
'''

line_permutations = [
    [ [0,3], [3,6] ],
    [ [3,6], [6,9] ],
    [ [0,3], [6,9] ]
]

offsetX = 10.0
offsetY = 10.0
offsetZ = 0.1

maker_message = "; HOLY FUCK I HATE MY LIFE\n; FLAVOR:Marlin\n; Generated with Retardation 0.6.8\n"

f = open('x.gcode', 'a')    ## Open file for writing
f.write(maker_message)
f.write('G28 ; HOME ALL AXIS\n')

for layer_height in range(0,11,1):
    plane_coord = np.array([0, 0 ,layer_height], dtype=np.float32)   ## coordinate on slice plane
    plane_norm  = np.array([0, 0, 1], dtype=np.float32)    ## normal vector of slice plane, purpendicular to plane

    intersections = []  # temp list to store any found intersections

    ## Checking Lines with slicing plane
    for line in range(len(my_mesh.points)): ## Check all polygons
        for start_stop in line_permutations:

            l0 = my_mesh.points[ line ][ start_stop[0][0] : start_stop[0][1] ]  ## 3D Matrix looping magic BS
            l1 = my_mesh.points[ line ][ start_stop[1][0] : start_stop[1][1] ]  ## |

            try: 
                i = isect_line_plane(l0, l1, plane_coord, plane_norm)   ## Calculate intersection point
                intersections.append(i)                                 ## If no errors -> add point to intersections

            ## Catchers
            except LineIsOnPlaneException:  ## Line is on plane -> add both points as intersections
                intersections.extend([l0, l1])
            
            except Exception:   ## Any other exception line isec not found
                pass

    ## Remove repeat points
    intersections_distilled = distill(intersections)

    # print(intersections_distilled)
    point_chain = []

    while True:     ## IT FUCKING WORKS LETS GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
        # print("len" + str(len(intersections_distilled)))
        if len(intersections_distilled) == 1:                                   ## if only one remaining -> must be closest point
            point_chain.extend([intersections_distilled[0], point_chain[0]])    ## add this point to chain and copy start position
            break

        closest_distance = 10e6 ## temp closest distance
        closest_point = None    ## temp closest point
        bucket = []             ## this is a bucket

        try:
            refrence = point_chain[-1]  ## if pointchain is empty
        except IndexError:              ## |
            refrence = plane_coord      ## \-> ues plane coordinate as refrence

        while True:
            try:
                temp_point = intersections_distilled.pop(0) ## Take first point in line
            except IndexError:                              ## if no point, stop trying
                break

            temp_distance = distance_between_points_2(refrence, temp_point)   ## Calculate distance

            if temp_distance < closest_distance:    ## Check if this point is closer than last
                if closest_point:
                    bucket.append(closest_point)    ## return other wrong closest to bucket
                closest_point = temp_point          ## Replace closest known point and distance
                closest_distance = temp_distance    ## |
            else:
                bucket.append(temp_point)           ## Otherwise, discard point into bucket
            
        point_chain.append(closest_point)           ## After all points have been tried, append closest point to chain

        intersections_distilled = bucket            ## Reset bucket to origional list

    ## Print chain as layer
    print(point_chain)
    
    f.write("; LAYER HEIGHT\n")
    for any_point in point_chain:
        x = any_point[0] + offsetX
        y = any_point[1] + offsetY
        z = any_point[2] + offsetZ
        f.write("G1 X{0} Y{1} Z{2}\n".format(x,y,z))