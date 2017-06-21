from PIL import ImageDraw, Image, ImageFont
import numpy as np
import imageio
import math, random
import time, datetime
random.seed()

t = time.time()

class Shape:
    

    def __init__(self, diameter):
        self._diameter = diameter
        self.define_base_nodes()
        self.define_base_edges()
        self.define_base_faces()

    def define_base_nodes(self):
        raise NotImplementedError()

    def define_base_edges(self):
        raise NotImplementedError()

    def define_base_faces(self):
        raise NotImplementedError()

    def rotate(self, dimension, degrees):
        cosTheta = math.cos(math.radians(degrees))
        sinTheta = math.sin(math.radians(degrees))
        if dimension in ['x', 'X']:
            for node in self._nodes:
                y = node[1]
                z = node[2]
                node[1] = cosTheta * y - sinTheta * z
                node[2] = sinTheta * y + cosTheta * z
        elif dimension in ['y', 'Y']:
            for node in self._nodes:
                x = node[0]
                z = node[2]
                node[0] = cosTheta * x - sinTheta * z
                node[2] = sinTheta * x + cosTheta * z
        elif dimension in ['z', 'Z']:
            for node in self._nodes:
                x = node[0]
                y = node[1]
                node[0] = cosTheta * x - sinTheta * y
                node[1] = sinTheta * x + cosTheta * y
    

    def draw_shape(self, canvasSize):
        xcentre, ycentre = canvasSize
        xc = xcentre/2
        yc = ycentre/2
        image = Image.new("RGBA", canvasSize, color=(255, 255, 255, 255))
        draw = ImageDraw.Draw(image)
        nodesize = 1
        draw_level_width = 20
##        for z in range(-int(0.6self._diameter), int(0.6*self._diameter), draw_level_width):
##            for face in self._faces:
##                n1num, n2num, n3num = get_nodes(self._edges[face[0]], self._edges[face[1]], self._edges[face[2]])
##                n1 = self._nodes[n1num]
##                n2 = self._nodes[n2num]
##                n3 = self._nodes[n3num]
##                mid = get_middle_point(n1, n2, n3)
##                if z <= mid[2] < z+draw_level_width:
##                    draw.polygon([(n1[0]+xc, n1[1]+yc),(n2[0]+xc, n2[1]+yc),(n3[0]+xc, n3[1]+yc)], fill=(95, 95, 95))
        for edge in self._edges:
            n1num, n2num = edge
            n1 = self._nodes[n1num]
            n2 = self._nodes[n2num]
            mid = get_middle_point(n1, n2)
            #if z <= mid[2] < z+draw_level_width:
            if mid[2] > 0:
                draw.line((n1[0] + xc, n1[1] + yc, n2[0] + xc, n2[1] + yc), width=nodesize, fill=(65, 65, 65, 255))
            

        return image

    def gen_gif(self, canvasSize, angles, filename = 'movie.gif'):
        images = []
        for i in range(400):
            self.rotate('x', 0.25)
            self.rotate('y', 0.75)
            self.rotate('z', 0.5)
            image = self.draw_shape(canvasSize)
            if i % 50 == 49:
                print('Finished for image no#', i+1)
            image = np.asarray(image)
            images.append(image)
        return images
            
        

class Tetrahedron(Shape):

    def __init__(self, diameter):
        super().__init__(diameter)

    def define_base_nodes(self):
        d = self._diameter
        ychange = 3*d/4
        y_up = 2*ychange/3
        y_down = y_up/2
        z_up = ychange / (math.sqrt(3))
        z_down = z_up/2
        xchange = 2*ychange / (math.sqrt(3))
        x_up = xchange/2
        x_down = x_up
        self._nodes = []
        self._nodes.append([0, y_up, 0])
        self._nodes.append([0, -y_down, z_up])
        self._nodes.append([x_up, -y_down, -z_down])
        self._nodes.append([-x_down, -y_down, -z_down])

    def define_base_edges(self):
        self._edges = []
        self._edges.append((0, 1))
        self._edges.append((0, 2))
        self._edges.append((0, 3))
        self._edges.append((1, 2))
        self._edges.append((1, 3))
        self._edges.append((2, 3))

    def define_base_faces(self):
        self._faces = []
        self._faces.append((0, 1, 3))
        self._faces.append((0, 2, 4))
        self._faces.append((1, 2, 5))
        self._faces.append((3, 4, 5))

    

class Cube(Shape):

    def __init__(self, diameter):
        super().__init__(diameter)

    def define_base_nodes(self):
        d = self._diameter
        edge_length = d / (2*math.sqrt(3))
        self._nodes = []
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    a = (-1)**(i+1)
                    b = (-1)**(j+1)
                    c = (-1)**(k+1)
                    self._nodes.append([a*edge_length, b*edge_length, c*edge_length])

    def define_base_edges(self):
        self._edges = []
        self._edges.append((0, 1))
        self._edges.append((0, 2))
        self._edges.append((0, 4))
        self._edges.append((1, 3))
        self._edges.append((1, 5))
        self._edges.append((2, 3))
        self._edges.append((2, 6))
        self._edges.append((4, 5))
        self._edges.append((4, 6))
        self._edges.append((5, 7))
        self._edges.append((6, 7))
        self._edges.append((3, 7))

    def define_base_faces(self):
        pass
        

class Icosahedron(Shape):

    def __init__(self, diameter):
        super().__init__(diameter)

    def define_base_nodes(self):
        d = self._diameter
        a = math.sqrt(d**2 / (1 + ((1 + math.sqrt(5))/2)**2))/2
        phi = a * (1 + math.sqrt(5))/2
        self._nodes = []
        self._nodes.append([0, -a, -phi])
        self._nodes.append([0, -a, phi])
        self._nodes.append([0, a, -phi])
        self._nodes.append([0, a, phi])
        self._nodes.append([-a, -phi, 0])
        self._nodes.append([-a, phi, 0])
        self._nodes.append([a, -phi, 0])
        self._nodes.append([a, phi, 0])
        self._nodes.append([-phi, 0, -a])
        self._nodes.append([phi, 0, -a])
        self._nodes.append([-phi, 0, a])
        self._nodes.append([phi, 0, a])

    def define_base_edges(self):
        self._edges = []
        self._edges.append({0, 2}) #0
        self._edges.append({1, 3}) #1
        self._edges.append({4, 6}) #2
        self._edges.append({5, 7}) #3
        self._edges.append({8, 10}) #4
        self._edges.append({9, 11}) #5
        self._edges.append({0, 4}) #6
        self._edges.append({0, 6}) #7
        self._edges.append({1, 4}) #8
        self._edges.append({1, 6}) #9
        self._edges.append({2, 5}) #10
        self._edges.append({2, 7}) #11
        self._edges.append({3, 5}) #12
        self._edges.append({3, 7}) #13
        self._edges.append({0, 8}) #14
        self._edges.append({0, 9}) #15
        self._edges.append({1, 10}) #16
        self._edges.append({1, 11}) #17
        self._edges.append({2, 8}) #18
        self._edges.append({2, 9}) #19
        self._edges.append({3, 10}) #20
        self._edges.append({3, 11}) #21
        self._edges.append({6, 9}) #22
        self._edges.append({6, 11}) #23
        self._edges.append({7, 9}) #24
        self._edges.append({7, 11}) #25
        self._edges.append({4, 8}) #26
        self._edges.append({4, 10}) #27
        self._edges.append({5, 8}) #28
        self._edges.append({5, 10}) #29

    def define_base_faces(self):
        self._faces = []
        for i in range(len(self._edges)):
            for j in range(i+1, len(self._edges)):
                for k in range(j+1, len(self._edges)):
                    edge1 = self._edges[i]
                    edge2 = self._edges[j]
                    edge3 = self._edges[k]
                    if check_edges(edge1, edge2, edge3):
                        self._faces.append((i, j, k))

    def complexify(self, comp=1):
        for x in range(comp):
            new_faces = []
            new_edges = []
            new_nodes = self._nodes

            nodelength = len(self._nodes)
            edgelength = len(self._edges)
            facelength = len(self._faces)
            

            for i in range(edgelength):
                node1num, node2num = self._edges[i]
                node1, node2 = self._nodes[node1num], self._nodes[node2num]
                midnode = get_middle_point(node1, node2)
                new_nodes.append(midnode)
                new_edges.extend([{node1num, nodelength + i}, {node2num, nodelength + i}])
            
            
            for i in range(facelength):
                
                face = self._faces[i]
                edgenum = [face[0], face[1], face[2]]
                edge1, edge2, edge3 = self._edges[edgenum[0]], self._edges[edgenum[1]], self._edges[edgenum[2]]
                node1num, node2num, node3num = get_nodes(edge1, edge2, edge3)
                node1, node2, node3 = self._nodes[node1num], self._nodes[node2num], self._nodes[node3num]
                
                node12 = new_nodes[nodelength + edgenum[0]]
                node13 = new_nodes[nodelength + edgenum[1]]
                node23 = new_nodes[nodelength + edgenum[2]]

                new_edges.append({nodelength + edgenum[0], nodelength + edgenum[1]})
                new_edges.append({nodelength + edgenum[0], nodelength + edgenum[2]})
                new_edges.append({nodelength + edgenum[1], nodelength + edgenum[2]})

                edgecheck = [new_edges[edgenum[0]*2], new_edges[edgenum[0]*2+1]]
                edgecheck.extend([new_edges[edgenum[1]*2], new_edges[edgenum[1]*2+1]])
                edgecheck.extend([new_edges[edgenum[2]*2], new_edges[edgenum[2]*2+1]])
                edgecheck.append(new_edges[2*edgelength+i*3])
                edgecheck.append(new_edges[2*edgelength+i*3+1])
                edgecheck.append(new_edges[2*edgelength+i*3+2])
                
                for a in range(len(edgecheck)):
                    for b in range(a+1, len(edgecheck)):
                        for c in range(b+1, len(edgecheck)):
                            edge1 = edgecheck[a]
                            edge2 = edgecheck[b]
                            edge3 = edgecheck[c]
                            if check_edges(edge1, edge2, edge3):
                                if a < 6:
                                    f = edgenum[(a//2)]*2+(a%2)
                                else:
                                    f = 2*edgelength + i*3 + (a - 6)
                                if b < 6:
                                    g = edgenum[(b//2)]*2+(b%2)
                                else:
                                    g = 2*edgelength + i*3 + (b - 6)
                                if c < 6:
                                    h = edgenum[(c//2)]*2+(c%2)
                                else:
                                    h = 2*edgelength + i*3 + (c - 6)
                                
                                new_faces.append((f, g, h))

            print('Complexity Level', x+1, 'completed.')
                
            self._nodes = new_nodes
            self._edges = new_edges
            self._faces = new_faces

            self.normalize()
            

    def normalize(self):
        for node in self._nodes:
            distancemodifier = 0.5 * self._diameter/(math.sqrt(node[0]**2 + node[1]**2 + node[2]**2))
            node[0] = node[0]*distancemodifier
            node[1] = node[1]*distancemodifier
            node[2] = node[2]*distancemodifier


    def add_mountains(self, mountain_count):

        max_height = 1.15
        min_height = 0.95
        height_range = max_height - min_height
        spread_depth = 10
        
        for i in range(mountain_count):
            height_factor = int((random.random() * height_range + min_height) * 10000 ) / 10000
            somenodenum = random.randrange(0, len(self._nodes))
            nodes = [[somenodenum]]
            all_nna = [somenodenum]
            self.change_distance(somenodenum, height_factor)
            for i in range(1, spread_depth):
                height_factor = 0.62*height_factor + 0.38
                nodes.append([])
                for edge in self._edges:
                    for node in nodes[i-1]:
                        if node == edge[0]:
                            if not (edge[1] in all_nna):
                                nodes[i].append(edge[1])
                                all_nna.append(edge[1])
                                self.change_distance(edge[1], height_factor)
                        elif node == edge[1]:
                            if not (edge[0] in all_nna):
                                nodes[i].append(edge[0])
                                all_nna.append(edge[0])
                                self.change_distance(edge[0], height_factor)
                

    def change_distance(self, node_num, distance_multiplier):
        self._nodes[node_num][0] = self._nodes[node_num][0]*distance_multiplier
        self._nodes[node_num][1] = self._nodes[node_num][1]*distance_multiplier
        self._nodes[node_num][2] = self._nodes[node_num][2]*distance_multiplier
                

        

class Prism(Shape):

    def __init__(self, diameter):
        super().__init__(diameter)

    def define_base_nodes(self):
        pass

    def define_base_edges(self):
        pass

        

class Antiprism(Shape):

    def __init__(self, diameter):
        super().__init__(diameter)

    def define_base_nodes(self):
        pass

    def define_base_edges(self):
        pass


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


         
def main():
    
    new_t = time.time() - t
    print('Process started at ', new_t, 'seconds.')
    shape = Icosahedron(275)
    new_t = time.time() - t
    print('Shape finished after ', new_t, 'seconds.')
    shape.complexify(comp=5)
    new_t = time.time() - t
    print('Complexity finished after ', new_t, 'seconds.')
    #shape.add_mountains(100)
    new_t = time.time() - t
    print('Mountains finished after ', new_t, 'seconds.')
    images = shape.gen_gif((400, 400), ['x'])
    new_t = time.time() - t
    print('Movie.gif created after ', new_t, 'seconds.')
    imageio.mimsave('movie.gif', images, fps=60)
    new_t = time.time() - t
    print('Gif saved after ', new_t, 'seconds.')

if __name__ == "__main__":
    main()
