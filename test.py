from calculator import *
import numpy as np

a = np.array([1,1], dtype=np.float32)
b = np.array([5,5], dtype=np.float32)
c = np.array([3,3], dtype=np.float32)

d = point_is_on_line(a,b,c)

print(d)