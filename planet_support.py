import random, math
import numpy as np


def change_distance(node, distance):
    newnode = [0, 0, 0]
    distance_multiplier = distance/get_height(node)
    newnode[0] = node[0]*distance_multiplier
    newnode[1] = node[1]*distance_multiplier
    newnode[2] = node[2]*distance_multiplier
    return newnode

def get_height(node):
    return math.sqrt(node[0]**2 + node[1]**2 + node[2]**2)

def get_middle_point(point1, point2, point3):
    newx = (point1[0] + point2[0] + point3[0]) / 3
    newy = (point1[1] + point2[1] + point3[1]) / 3
    newz = (point1[2] + point2[2] + point3[2]) / 3
    return [newx, newy, newz]


##Perlin noise
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

def perlin(node, period, amplitude, random_hash, normalise=True):

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

    if normalise:
        standard_devs = value / 0.2
        sd = standard_devs

        cmdf = 0.5* math.tanh(179*sd/23 - 111/2*math.atan(37*sd/294)) + 0.5
        return amplitude*cmdf

    return 0.5*amplitude*(value + 1)
##end of perlin noise


def perspective(node, origin):
    pass

def crossproduct(node1, node2, node3):
    #returns unit vector of cross product
    x0, y0, z0 = node1
    x1, y1, z1 = node2
    x2, y2, z2 = node3
    vectorx0, vectory0, vectorz0 = x1-x0, y1-y0, z1-z0
    vectorx1, vectory1, vectorz1 = x2-x0, y2-y0, z2-z0
    
    newx = vectory0*vectorz1 - vectorz0*vectory1
    newy = vectorz0*vectorx1 - vectorx0*vectorz1
    newz = vectorx0*vectory1 - vectory0*vectorx1
    length = get_height([newx, newy, newz])
    newx = newx/length
    newy = newy/length
    newz = newz/length
    
    vector_magnitude = get_height([x0+newx, y0+newy, z0+newz])
    if magnitude(node1) > vector_magnitude:
        newx = -newx
        newy = -newy
        newz = -newz
    
    return (newx, newy, newz)

def dotproduct(vector1, vector2):
    return vector1[0]*vector2[0] + vector1[1]*vector2[1] + vector1[2]*vector2[2]

def magnitude(vector):
    return math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)

def lighting(node1, node2, node3, color, light):
    cross_product = crossproduct(node1, node2, node3)
    dot_product = dotproduct(light, cross_product)
    angle = math.degrees(math.acos(dot_product/(magnitude(cross_product)*magnitude(light))))
    r, g, b, a = color
    angleratio = 1-angle/180
    #higher if more light, lower if less light
    angleratio = 2*angleratio**2 - (4/3)*angleratio**3 + (1/3)*angleratio
    #smoothing function
    r, g, b = r*angleratio, g*angleratio, b*angleratio
    return (int(r), int(g), int(b), a)
        
        
        
        
    
