import random, math
import numpy as np


def change_distance(node, distance):
    ''' Changes the height of a node.

        Parameters:
            node (array<float, float, float>) : The node being changed.
            distance (float) : The height to which the node is being extended.

        Returns:
            newnode (array<float, float, float>) : The adjusted node.

    '''
    newnode = [0, 0, 0]
    distance_multiplier = distance/get_height(node)
    newnode[0] = node[0]*distance_multiplier
    newnode[1] = node[1]*distance_multiplier
    newnode[2] = node[2]*distance_multiplier
    return newnode

def get_height(node):
    ''' Calculates the height of a node, relative to the coordinates (0, 0, 0).

        Parameters:
            node (array<float, float, float>) : The node being evaluated.

        Returns:
            height (int) : The height of the given node.

    '''
    return math.sqrt(node[0]**2 + node[1]**2 + node[2]**2)

def get_middle_point(point1, point2, point3):
    ''' Calculates the point equidistant from three other points.

        Parameters:
            point1 (array<float, float, float>) : The first point.
            point2 (array<float, float, float>) : The second point.
            point3 (array<float, float, float>) : The third point.

        Returns:
            middlenode (array<float, float, float>) : The equidistant point.

    '''
    newx = (point1[0] + point2[0] + point3[0]) / 3
    newy = (point1[1] + point2[1] + point3[1]) / 3
    newz = (point1[2] + point2[2] + point3[2]) / 3
    return [newx, newy, newz]


##Perlin noise
def lerp(a0, a1, w):
    ''' To be honest I don't know what this does, if you see this
        comment remind me to find out and update the comment
    '''
    return (1 - w)*a0 + w*a1
 
def dotGridGradient(ix, iy, iz, x, y, z, random_hash):
    ''' Calculates a random directional vector for a point, and then
        returns the dot product between that vector and the vector between
        that point and a rounded point.

        Parameters:
            ix (float) : The rounded point's x value.
            iy (float) : The rounded point's y value.
            iz (float) : The rounded point's z value.
            x (float) : The initial point's x value.
            y (float) : The initial point's y value.
            z (float) : The initial point's z value.
            random_hash (str) : A random hash used to seed the random
                                generator.

        Returns:
            dot_product (float) : The end product of the two vectors.

    '''
    combined_hash = hash(((ix, iy, iz), random_hash))
    random.seed(combined_hash)

    theta = 2*math.pi*random.random()
    randz = 2*random.random()-1
    randy = math.sqrt(1-randz**2)*math.sin(theta)
    randx = math.sqrt(1-randz**2)*math.cos(theta)

    dx = x - ix
    dy = y - iy
    dz = z - iz

    return (dz*randz + dx*randy + dy*randx)

def perlin(node, period, amplitude, random_hash, uniform=True):
    ''' Generates perlin noise for a given node.

        Parameters:
            node (array<float, float, float>) : An arbitrary node.
            period (float) : How spread out randomness is i.e. how smoothed out?
            amplitude (float) : How extreme values can be i.e. how high?
            random_hash (str) : A hash used to seed the random generator.
            normalise (boolean) : Determines whether the returned values are normally
                                    or uniformly distributed.

        Returns:
            noise (float) : A random value between 0 and [amplitude].

    '''
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

    if uniform:
        ## A standard deviation for these values is around 0.2
        standard_devs = value / 0.2
        sd = standard_devs

        # A function that approximates the cumulative frequency function
        # More here: https://www.hindawi.com/journals/mpe/2012/124029/
        cmdf = 0.5* math.tanh(179*sd/23 - 111/2*math.atan(37*sd/294)) + 0.5
        return amplitude*cmdf

    return 0.5*amplitude*(value + 1)
##end of perlin noise


def perspective(node, origin):
    ## Meant to be implemented whenever I get around to orbiting bodies
    pass

def crossproduct(node1, node2, node3):
    ''' Returns the unit vector cross product of three nodes.
        i.e. takes two vectors from node1 to node2 and node1 to node3
        and calculates the cross product.

        Parameters:
            node1 (array<float, float, float>) : The first node.
            node2 (array<float, float, float>) : The second node.
            node3 (array<float, float, float>) : The third node.

        Returns:
            crossproduct (tuple<float, float, float>) : The cross product.

    '''
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
    if get_height(node1) > vector_magnitude:
        newx = -newx
        newy = -newy
        newz = -newz
    
    return [newx, newy, newz]

def dotproduct(vector1, vector2):
    '''Returns the dotproduct between two vectors.

        Parameters:
            vector1 (array<float, float, float>) : The first vector.
            vector2 (array<float, float, float>) : The second vector.

        Returns:
            dotproduct (float) : The dot product.
            
    '''
    return vector1[0]*vector2[0] + vector1[1]*vector2[1] + vector1[2]*vector2[2]


def lighting(node1, node2, node3, color, light, attr):
    '''Calculates how much light is being cast onto a face.

        Parameters:
            node1 (array<float, float, float>) : The first node of the face.
            node2 (array<float, float, float>) : The second node of the face.
            node3 (array<float, float, float>) : The third node of the face.
            color (array<float, float, float, float>) : The face's color.
            light (array<float, float, float>) : The direction light is coming from.

        Returns:
            color (array<int, int, int>) : The new color of the face
    '''

    normal = crossproduct(node1, node2, node3)
    light = light
    view = [0, 0, 1]
    reflection = 2*(dotproduct(normal, light))*np.array(normal) - np.array(light)
    reflection = reflection.tolist()
    avg_z = (node1[2] + node2[2] + node3[2])/3

    fog_mod = attr['atmosphere']

    ambient = np.array(color)
    diffuse = 0.85*max(0, dotproduct(normal, light))*np.array(color)
    new_color = 0.4*ambient + 0.6*diffuse
    
    fog_p = math.exp(-((260-avg_z)/260)*fog_mod)
    new_color = fog_p*new_color+(1-fog_p)*np.array([255, 255, 255, 255])

    r, g, b, a = new_color.tolist()
    new_color = (int(r), int(g), int(b), 255)
    
    return new_color
        
        
        
        
    
