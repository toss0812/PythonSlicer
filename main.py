from calculator import *
from reader import *
import itertools as it
import numpy as np          ## ignore the error message

## ========== CONDENSE
## Reduces a list of 3D Vectors to only have unique entries
def distill(to_condense: list):
    return np.unique(to_condense, axis=0) # find unique entries in list, axis=0 -> otherwise 2d array will be flattened and will return unique values of all entries
    ## Funny thing, numpy.unique() also sorts list on chosen axis, based on first entry basis



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

point_chain = []
point_leftover = []

temp_point = None
temp_dist = None
closest_point = None
closest_distance = None
ref_point = None

# while True:
#     try:
#         ref_point = intersections_distilled[-1]
#     except IndexError:
#         ref_point = plane_coord

#     while len(intersections_distilled) > 1:
#         pass # TODO: don't


print("aids")     

















## Generate all possible permutations of condensed points
# permutations = it.permutations(condensed, r=3)

# z = 0
# for x in permutations:
#     z = z + 1

# for x in permutations:
#     print(x[0])

# print(condensed)

# perimiter = []
# for i in permutations:
#     test = point_is_on_line(i[0], i[1], i[2])
#     if (test):
#         perimiter.append(i[2])

# for i in perimiter:
    # print(i)

# perimiter_condensed