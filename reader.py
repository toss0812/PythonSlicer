import numpy as np
from stl import mesh

def read(file):
    return mesh.Mesh.from_file(file)