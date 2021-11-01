from calculator import *
import numpy as np          ## ignore the errormessage
import itertools as it

a = np.array([0,10,5], dtype=np.float32)
b = np.array([0,5,5], dtype=np.float32)
c = np.array([0,5,5], dtype=np.float32)


d1 = distance_between_points(b,a)
d2 = distance_between_points_2(b,a)
print("d1: {0}\nd2: {1}".format(d1, d2))


# d = distance_between_points(a,b)

# d = [a,b,c]
# e = b

# d.remove(e)


# np.delete(d, b, axis=1)

# print(a)
# e = [a,b,c]

# f = it.permutations(e)



# for x in f:
#     print(x)


