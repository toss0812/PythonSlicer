from calculator import *
from reader import *

## ========== CONDENSE
## Reduces a list of 3D Vectors to only have unique entries
def condense(to_condense: list):
    return np.unique(to_condense, axis=0) # find unique entries in list, axis=0 -> otherwise 2d array will be flattened and will return unique values of all entries



## ========== MAIN THINGS
my_mesh = read("yes_box_bin.stl") # simple cube with sides of length = 10

print(my_mesh.points) 
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

''' ========================================================================================== '''
''' = yes, yes, this can be written smarter and more compact but fuck that, that's for later = '''
''' ========================================================================================== '''
# ## 0:3 -> 3:6
# for line in range(len(my_mesh.points)): # Itterte through all points
#     l0 = my_mesh.points[line][0:3] # first vector
#     l1 = my_mesh.points[line][3:6] # second vector

#     try:
#         i = isect_line_plane(l0, l1, plane_coord, plane_norm) # find intersection point
#         intersections.append(i) # add found intersection to temp list
#     except Exception: # if no intersection found "isect_line_plane()" raises Exception
#         pass

# ## 3:6 -> 6:9
# for line in range(len(my_mesh.points)):
#     l0 = my_mesh.points[line][3:6]
#     l1 = my_mesh.points[line][6:9]

#     try:
#         i = isect_line_plane(l0, l1, plane_coord, plane_norm)
#         intersections.append(i)
#     except Exception:
#         pass

# ## 0:3 -> 6:9
# for line in range(len(my_mesh.points)):
#     l0 = my_mesh.points[line][0:3]
#     l1 = my_mesh.points[line][6:9]

#     try:
#         i = isect_line_plane(l0, l1, plane_coord, plane_norm)
#         intersections.append(i)
#     except Exception:
#         pass

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



print(intersections)
condensed = condense(intersections)
print("\n\n\n")
print(condensed)