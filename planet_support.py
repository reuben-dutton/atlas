import random, math
import numpy as np


def change_distance(node, diameter, distance_multiplier=None):
    newnode = [0, 0, 0]
    if distance_multiplier == None:
        distance_multiplier = 0.5 * diameter/(math.sqrt(node[0]**2 + node[1]**2 + node[2]**2))
    newnode[0] = node[0]*distance_multiplier
    newnode[1] = node[1]*distance_multiplier
    newnode[2] = node[2]*distance_multiplier
    return newnode

def rotate_node(node, dimension, degrees, origin):
    cosTheta = math.cos(math.radians(degrees))
    sinTheta = math.sin(math.radians(degrees))
    node = [node[0]-origin[0], node[1]-origin[1], node[2]-origin[2]]
    if dimension in ['x', 'X']:
        y = node[1]
        z = node[2]
        node[1] = cosTheta * y - sinTheta * z
        node[2] = sinTheta * y + cosTheta * z
    elif dimension in ['y', 'Y']:
        x = node[0]
        z = node[2]
        node[0] = cosTheta * x - sinTheta * z
        node[2] = sinTheta * x + cosTheta * z
    elif dimension in ['z', 'Z']:
        x = node[0]
        y = node[1]
        node[0] = cosTheta * x - sinTheta * y
        node[1] = sinTheta * x + cosTheta * y

    return [node[0] + origin[0], node[1] + origin[1], node[2] + origin[2]]

def get_middle_point(point1, point2, point3=None):
    if point3==None:
        newx = (point1[0] + point2[0]) / 2
        newy = (point1[1] + point2[1]) / 2
        newz = (point1[2] + point2[2]) / 2
        newnode = [newx, newy, newz]
    else:
        newx = (point1[0] + point2[0] + point3[0]) / 3
        newy = (point1[1] + point2[1] + point3[1]) / 3
        newz = (point1[2] + point2[2] + point3[2]) / 3
        newnode = [newx, newy, newz]

    return newnode

def get_nodes(edge1, edge2, edge3):
    nodeset = set()
    for nodenum in edge1.union(edge2.union(edge3)):
        nodeset.add(nodenum)
    return list(nodeset)

def check_edges(edge1, edge2, edge3):
    if len(get_nodes(edge1, edge2, edge3)) == 3:
        if edge1 != edge2 and edge2 != edge3 and edge1 != edge3:
            return True
    return False

def lerp(a0, a1, w):
    return (1 - w)*a0 + w*a1
 
def dotGridGradient(ix, iy, iz, x, y, z, random_hash):
    coordinate_hash = hash((ix, iy, iz))
    combined_hash = hash((coordinate_hash, random_hash))
    random.seed(combined_hash)

    theta = 2*math.pi*random.random()
    randz = 2*random.random()-1
    randy = math.sqrt(1-randz**2)*math.sin(theta)
    randx = math.sqrt(1-randz**2)*math.cos(theta)
    

    dx = x - ix
    dy = y - iy
    dz = z - iz

    return (dz*randz + dx*randy + dy*randx)

def perlin(node, period, amplitude, random_hash):

    x = node[0]/period
    y = node[1]/period
    z = node[2]/period

    x0 = math.floor(x)
    x1 = x0 + 1
    y0 = math.floor(y)
    y1 = y0 + 1
    z0 = math.floor(z)
    z1 = z0 + 1

    sx = 3*(x-x0)**2 - 2*(x-x0)**3
    sy = 3*(y-y0)**2 - 2*(y-y0)**3
    sz = 3*(z-z0)**2 - 2*(z-z0)**3

    n0 = dotGridGradient(x0, y0, z0, x, y, z, random_hash)
    n1 = dotGridGradient(x1, y0, z0, x, y, z, random_hash)
    ix0 = lerp(n0, n1, sx)
    n0 = dotGridGradient(x0, y1, z0, x, y, z, random_hash)
    n1 = dotGridGradient(x1, y1, z0, x, y, z, random_hash)
    ix1 = lerp(n0, n1, sx)

    n0 = dotGridGradient(x0, y0, z1, x, y, z, random_hash)
    n1 = dotGridGradient(x1, y0, z1, x, y, z, random_hash)
    ix2 = lerp(n0, n1, sx)
    n0 = dotGridGradient(x0, y1, z1, x, y, z, random_hash)
    n1 = dotGridGradient(x1, y1, z1, x, y, z, random_hash)
    ix3 = lerp(n0, n1, sx)
    
    ix4 = lerp(ix0, ix1, sy)
    ix5 = lerp(ix2, ix3, sy)

    value = lerp(ix4, ix5, sz)

    return 0.5*amplitude*(value + 1)


def perspective(node, origin):
    pass
    
