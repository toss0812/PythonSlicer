from calculator import *
import numpy as np
import itertools as it

a = np.array([0,0,5], dtype=np.float32)
b = np.array([0,10,5], dtype=np.float32)
c = np.array([0,5,5], dtype=np.float32)

d = point_is_on_line(a,b,c)

print(d)
# e = [a,b,c]

# f = it.permutations(e)



# for x in f:
#     print(x)