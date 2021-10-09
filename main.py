from calculator import *
from reader import *
import itertools as it

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



plane_coord = np.array([0,0,5], dtype=np.float32)   # coordinate on slice plane
plane_norm = np.array([0,0,1], dtype=np.float32)    # normal vector of slice plane, purpendicular to plane

intersections = []  # temp list to store any found intersections


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


## Calculate shortest route over points
point_chain = [None]        ## chain of points for permimiter
shortest_distance = 10e6    ## starting value -> 10^6mm = 100m

## Find first point of chain closest to (0,0,slice-plane-z)
for point in intersections_distilled: 
    temp_distance = distance_between_points(plane_coord, point) ## Calc distance between plane-coordinate and a point

    if temp_distance < shortest_distance:   ## if distance is less than any earlier found distance -> new closest point        
        point_chain[0] = point
        shortest_distance = temp_distance

print(len(intersections_distilled == 1))

# print(point_chain)

# print("\n\n")

## TODO: Remove remove closest point from list first

## GENERATE CHAIN
while True:
    # print(len(intersections_distilled == 1))
    if (len(intersections_distilled == 1)): ## REMINDER: WAAROM ZIET IE EEN LIJST MET LENGTE 8 ALS LENGTE 1 AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        point_chain.append(intersections_distilled[0])
        print("tering")
        break
    print("hoer")
    refrence_point = point_chain[-1]
    closest_distance = 10e6
    closest_point = 0

    for i in len(intersections_distilled):
        temp_point = intersections.pop(i)
        # print(temp_point)
        try:
            temp_distance = distance_between_points(refrence_point, temp_point)
        except Exception:
            pass
        if (0 < temp_distance < closest_distance):
            closest_distance = temp_distance
            closest_point = temp_distance

        else:
            intersections_distilled.insert(i, temp_point)

    point_chain.append(closest_point)


# print(point_chain)








# print (point_chain)










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