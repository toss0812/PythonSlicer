from calculator import *
from reader import *
import itertools as it

## ========== CONDENSE
## Reduces a list of 3D Vectors to only have unique entries
def condense(to_condense: list):
    return np.unique(to_condense, axis=0) # find unique entries in list, axis=0 -> otherwise 2d array will be flattened and will return unique values of all entries



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



plane_coord = np.array([0,0,5], dtype=np.float32) # coordinate on slice plane
plane_norm = np.array([0,0,1], dtype=np.float32) # normal vector of slice plane, purpendicular to plane

intersections = [] # temp list to store any found intersections

## for 
for line in range(len(my_mesh.points)): ## Check all polygons
    for start_stop in line_permutations:

        l0 = my_mesh.points[ line ][ start_stop[0][0] : start_stop[0][1] ]
        l1 = my_mesh.points[ line ][ start_stop[1][0] : start_stop[1][1] ]

        try: 
            i = isect_line_plane(l0, l1, plane_coord, plane_norm)
            intersections.append(i)
        except Exception:
            pass



## Remove repeat points
condensed = condense(intersections)

## Generate all possible permutations of condensed points
permutations = it.permutations(condensed, r=3)

z = 0
# for x in permutations:
#     z = z + 1

# for x in permutations:
#     print(x[0])

# print(condensed)

perimiter = []
for i in permutations:
    test = point_is_on_line(i[0], i[1], i[2])
    if (test):
        perimiter.append(i[2])

for i in perimiter:
    print(i)

# perimiter_condensed