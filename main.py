from calculator import *
from reader import *
import itertools as it
import numpy as np          ## ignore the error message

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

line_permutations = [ ## Cython?
    [
        [0,3], [3,6]
    ],
    [
        [3,6], [6,9]
    ],
    [
        [0,3], [6,9]
    ]
]



plane_coord = np.array([0,0,5], dtype=np.float32)   # coordinate on slice plane
plane_norm = np.array([0,0,1], dtype=np.float32)    # normal vector of slice plane, purpendicular to plane

intersections = []  # temp list to store any found intersections


## Checking Lines with slicing plane
for line in range(len(my_mesh.points)): ## Check all polygons
    for start_stop in line_permutations:

        l0 = my_mesh.points[ line ][ start_stop[0][0] : start_stop[0][1] ]  ## 3D Matrix looping magic BS
        l1 = my_mesh.points[ line ][ start_stop[1][0] : start_stop[1][1] ]

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

print(intersections_distilled)

## TODO: do the thing of pathplanning yes
## TODO: do not use a leftovers bin, just reinsert not-shortest back into the first list, then do np.sort on the list after every itteration
# point_chain = []
# point_leftover = []

# temp_point = None
# temp_dist = None
# closest_point = None
# closest_distance = None
# ref_point = None

## True loop temporary disabled do to infinate loop
# while True:
#     try:
#         ref_point = intersections_distilled[-1]
#     except IndexError:
#         ref_point = plane_coord

#     while len(intersections_distilled) > 1:
#         pass ## TODO: don't

point_chain = []



while True:     ## IT FUCKING WORKS LETS GOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
    # print("len" + str(len(intersections_distilled)))
    if len(intersections_distilled) == 1:                                   ## if only one remaining -> must be closest point
        point_chain.extend([intersections_distilled[0], point_chain[0]])    ## add this point to chain and copy start position
        break

    closest_distance = 10e6
    closest_point = None
    bucket = []

    try:
        refrence = point_chain[-1]
    except IndexError:
        refrence = plane_coord

    # for temp_point in intersections_distilled:
    #     # print("p0: " + str(refrence))
    #     # print("p1: " + str(temp_point))
    #     temp_distance = distance_between_points(refrence, temp_point)
    #     # print("d:  " + str(temp_distance))
    #     if temp_distance < closest_distance:
    #         closest_point = temp_point

    # for temp_index in range(len(intersections_distilled)):
    #     print(temp_index)
    #     temp_point = intersections_distilled.pop(temp_index)
    #     temp_distance = distance_between_points(refrence, temp_point)

    #     if temp_distance < closest_distance:
    #         closest_point = temp_point
    #         closest_distance = temp_distance
    #     else:
    #         bucket.append(temp_point)

    while True:
        try:
            temp_point = intersections_distilled.pop(0)                 ## Take first point in line
        except IndexError:                                              ## if no point, stop trying
            break

        temp_distance = distance_between_points_2(refrence, temp_point)   ## Calculate distance
        # print("p0: {0},\np1: {1},\nd:  {2}".format(refrence, temp_point, str(temp_distance)))

        if temp_distance < closest_distance:    ## Check if this point is closer than last
            if closest_point:
                bucket.append(closest_point)    ## return other wrong closest to bucket
            closest_point = temp_point          ## Replace closest known point and distance
            closest_distance = temp_distance    ## |
            # print("yoink")
        else:
            bucket.append(temp_point)           ## Otherwise, discard point into bucket
            # print("yeet")
        
    point_chain.append(closest_point)           ## After all points have been tried, append closest point to chain
    # print("added: {0} to chain".format(closest_point))
    # print("temp point chain:\n{0}".format(point_chain))

    intersections_distilled = bucket                                    ## Reset bucket to origional list
    # print("leftovers" + str(bucket))

print(point_chain)