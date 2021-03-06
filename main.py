from calculator import *
from reader import *
import itertools as it
import numpy as np

''' 
==================================================
= Program written by Tom Dingenouts @toss0812
================================================== 
'''

## ========== DISTILL
## Reduces a list of 3D Vectors to only have unique entries
def distill(to_condense: list):
    temp = np.unique(to_condense, axis=0) ## Find unique entries in list, axis=0 -> otherwise 2d array will be flattened and will return unique values of all entries
    ## Funny thing, "numpy.unique()" also sorts list on chosen axis, based on first entry basis
    return temp.tolist()



## ========== MAIN THINGS

#F1 Ask the user for the name of the input and output files
input_file = input("please enter input file name (*.stl): ")
try:
    my_mesh = read(input_file) ## Simple cube with sides of length = 10
except Exception:
    print("no known file")
    exit()

output_file = input("please enter output file name: ")

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

line_permutations = [   ## Used in magic 3D matrix BS
    [ [0,3], [3,6] ],
    [ [3,6], [6,9] ],
    [ [0,3], [6,9] ]
]

offset_x = 10.0
offset_y = 10.0
offset_z = 0.1
total_extruded_distance = 0.0
extrusion_conversion_factor = 0.033





f = open('{0}.gcode'.format(output_file), 'w')    ## Open file for writing

maker_message = "; Welcome to Noodle v1.6.8 \n; Generated with Genuine Passion and a dash of Anger" ## maker message gets added to the .gcode file as a signature
f.write(maker_message)                                                                          ## append maker message
f.write('\n; PRINT SETTINGS\n; offsets: X:{0} Y:{1} Z{2}'.format(offset_x, offset_y, offset_z)) ## append print settings
f.write('\nG28 ; HOME ALL AXIS')                                                                ## start with auto-homing sequence




# max_layer_height = np.amax(my_mesh.points, axis=0)
# print(max_layer_height)

## Generate z-height for slicing and toolpath generation
step_height = 1                         ## TODO: USE MAX HEIGHT OF OBJECT FOR USE IN LAYER ITERATION
layers = np.arange(0, 30, step_height)  ## Stepheight of >1 will result in strange z values, due to 32bit-/ 64bit_float conversion


''' ################################################## ITTERATE TO SLICE & PLAN THROUGH ALL LAYERS '''
for layer_height in layers:
    ''' ============================== FIND LINE-PLANE INTERSECTIONS '''
    plane_coord = np.array([0, 0 ,layer_height], dtype=np.float32)  ## Coordinate on slice plane
    plane_norm  = np.array([0, 0, 1], dtype=np.float32)             ## Normal vector of slice plane, purpendicular to plane

    intersections = []  ## Temp list to store any found intersections

    #F1
    ## Checking Lines with slicing plane
    for polygon in range(len(my_mesh.points)): ## Check all polygons
        for start_stop in line_permutations:
            l0 = my_mesh.points[ polygon ][ start_stop[0][0] : start_stop[0][1] ]  ## "2D / 3D" Matrix looping magic BS
            l1 = my_mesh.points[ polygon ][ start_stop[1][0] : start_stop[1][1] ]  ## |

            ## Point calculation may cause errors
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
    
    
    
    
    ''' ============================== GENERATE NOZZLE PATH '''
    point_chain = []

    while True:     ## IT FUCKING WORKS LETS GOOOOOOOOO, *dabs*
        if len(intersections_distilled) == 1:                                   ## If only one remaining -> must be closest point
            point_chain.extend([intersections_distilled[0], point_chain[0]])    ## Add this point to chain and copy start position
            break

        if len(intersections_distilled) == 0:
            break

        ## "Gentlemen, synchronise your deathwatches."
        closest_distance = 10e6 ## Temp closest distance, ridicilously large
        closest_point = None    ## Temp closest point
        bucket = []             ## (1)"Gentlemen, this is a bucket."   (2)"Dear God."   (1)"Wait, there is more."   (2)"No..."

        try:
            refrence = point_chain[-1]  ## If pointchain is empty
        except IndexError:              ## |
            refrence = plane_coord      ## \-> use plane coordinate as refrence

        while True:
            try:
                temp_point = intersections_distilled.pop(0) ## Take first point in line
            except IndexError:                              ## If no point, stop trying
                break

            temp_distance = distance_between_points(refrence, temp_point)   ## Calculate distance

            if temp_distance < closest_distance:    ## Check if this point is closer than last
                if closest_point:
                    bucket.append(closest_point)    ## Return other wrong closest to bucket
                closest_point = temp_point          ## Replace closest known point and distance
                closest_distance = temp_distance    ## |
            else:
                bucket.append(temp_point)           ## Otherwise, discard point into bucket
            
        point_chain.append(closest_point)           ## After all points have been tried, append closest point to chain

        intersections_distilled = bucket            ## Reset bucket to origional list
    

    ''' ============================== GENERATE GCODE '''
    f.write("\n; LAYER HEIGHT: {0}".format(layer_height))

    for index in range(len(point_chain)):
        any_point = point_chain[index]
        prev_point = point_chain[index-1]
        print(any_point)
        if(index == 0):
            prev_point = any_point

        d = distance_between_points(any_point, prev_point) * extrusion_conversion_factor
        total_extruded_distance = total_extruded_distance + d
        any_point = any_point + [offset_x, offset_y, offset_z]

        f.write("\nG1 F1800 X{0} Y{1} Z{2} E{3}".format(any_point[0],any_point[1],any_point[2],total_extruded_distance))

f.write('\n; THANK GOD I\'M DONE')  ## Final message
f.close()                           ## Close file