from PIL import ImageDraw, Image, ImageFont
import numpy as np
import imageio
import math, random
import time, datetime
import planet_support as ps
import planet_types as pt

class PlanetObject(object):
    '''Planet is an object representing a planet with basic methods for:
        - Defining the rotational axis
        - Spinning the planet based on the given speed and using the rotational axis
        - Defining the base nodes for the planet
        - Defining the base faces for the planet
        - Increasing the complexity of the planet (subdividing the faces)
        - Generating biomes
        - Generating terrain
        - Generating clouds (if applicable for that planet type)

    '''

    def __init__(self, planet, complexity):
        ''' Initializes the planet

            Parameters:
                planet_type (PlanetType) : The information class holding the planet's characteristic info
                complexity (int) : An int representing how smooth/complex the planet should be.
                
        '''
        self._planet = planet
        self._radius = self._planet.get_diameter() * 0.5
        self.define_base_nodes()
        self.define_base_faces()
        self.complexify(complexity)
        self.define_rotation() 
        self.gen_terrain()
        self.assign_biomes()
        self.gen_clouds()


    def define_rotation(self):
        ''' Initializes the axis of rotation for the planet. The axis is mapped using the
            spherical coordinates system. The spin is either clockwise from above (-1) or
            anti-clockwise from above (1).
                
        '''
        spin_options = [-1, 1]
        self._axis_spin = random.choice(spin_options)
        self._axis_elevation_angle = random.randrange(-90, 90)
        self._axis_azimuth_angle = random.randrange(-180, 180)
        self.set_axis()

    def spin(self, speed):
        ''' Spins the planet at a certain speed around its axis. Speed is directly proportional
            to amount of degrees the planet spins. (i.e. speed=1 will turn the planet 1
            degree in the direction of spin)

            Parameters:
                speed (float) : The speed at which the planet is rotated
                
        '''
        cosTheta1 = math.cos(math.radians(self._axis_azimuth_angle))
        sinTheta1 = -math.sin(math.radians(self._axis_azimuth_angle))
        cosTheta2 = math.cos(math.radians(self._axis_elevation_angle))
        sinTheta2 = -math.sin(math.radians(self._axis_elevation_angle))
        cosTheta3 = math.cos(math.radians(speed*self._axis_spin))
        sinTheta3 = math.sin(math.radians(speed*self._axis_spin))
        for node in self._nodes:
            x = node[0]
            z = node[2]
            node[0] = cosTheta1 * x - sinTheta1 * z
            node[2] = sinTheta1 * x + cosTheta1 * z
            x = node[0]
            y = node[1]
            node[0] = cosTheta2 * x - sinTheta2 * y
            node[1] = sinTheta2 * x + cosTheta2 * y
            x = node[0]
            z = node[2]
            node[0] = cosTheta3 * x - sinTheta3 * z
            node[2] = sinTheta3 * x + cosTheta3 * z
            x = node[0]
            y = node[1]
            node[0] = cosTheta2 * x + sinTheta2 * y
            node[1] = -sinTheta2 * x + cosTheta2 * y
            x = node[0]
            z = node[2]
            node[0] = cosTheta1 * x + sinTheta1 * z
            node[2] = -sinTheta1 * x + cosTheta1 * z

    def temp_rotate(self, speed):
        ''' Spins the planet around the Y axis at a certain speed. Speed is directly proportional
            to amount of degrees the planet spins. (i.e. speed=1 will turn the planet 1
            degree in the direction of spin)

            Parameters:
                speed (float) : The speed at which the planet is rotated.
                
        '''
        cosTheta3 = math.cos(math.radians(speed*self._axis_spin))
        sinTheta3 = math.sin(math.radians(speed*self._axis_spin))
        for node in self._nodes:
            x = node[0]
            z = node[2]
            node[0] = cosTheta3 * x - sinTheta3 * z
            node[2] = sinTheta3 * x + cosTheta3 * z

    def set_axis(self):
        ''' Rotates the planet such that it is in line with its rotational axis.
                
        '''
        cosTheta = math.cos(math.radians(self._axis_elevation_angle))
        sinTheta = math.sin(math.radians(self._axis_elevation_angle))
        cosTheta2 = math.cos(math.radians(self._axis_azimuth_angle))
        sinTheta2 = math.sin(math.radians(self._axis_azimuth_angle))
        for node in self._nodes:
            x = node[0]
            y = node[1]
            node[0] = cosTheta * x - sinTheta * y
            node[1] = sinTheta * x + cosTheta * y
            x = node[0]
            z = node[2]
            node[0] = cosTheta2 * x - sinTheta2 * z
            node[2] = sinTheta2 * x + cosTheta2 * z

    def define_base_nodes(self):
        ''' Defines the first 12 nodes that make up the subdivided icosahedron.
                
        '''
        a = 1 / math.sqrt(11 + 2*math.sqrt(5))
        phi = a * (1 + math.sqrt(5))/2
        self._nodes = []
        self._nodes.append(ps.change_distance([0, -a, -phi], self._radius))
        self._nodes.append(ps.change_distance([0, -a, phi], self._radius))
        self._nodes.append(ps.change_distance([0, a, -phi], self._radius))
        self._nodes.append(ps.change_distance([0, a, phi], self._radius))
        self._nodes.append(ps.change_distance([-a, -phi, 0], self._radius))
        self._nodes.append(ps.change_distance([-a, phi, 0], self._radius))
        self._nodes.append(ps.change_distance([a, -phi, 0], self._radius))
        self._nodes.append(ps.change_distance([a, phi, 0], self._radius))
        self._nodes.append(ps.change_distance([-phi, 0, -a], self._radius))
        self._nodes.append(ps.change_distance([phi, 0, -a], self._radius))
        self._nodes.append(ps.change_distance([-phi, 0, a], self._radius))
        self._nodes.append(ps.change_distance([phi, 0, a], self._radius))

    def define_base_faces(self):
        ''' Defines the first 20 faces that make up the subdivided icosahedron.

        '''
        self._faces = []
        self._faces.append([0, 2, 8])
        self._faces.append([0, 2, 9])
        self._faces.append([1, 3, 10])
        self._faces.append([1, 3, 11])
        self._faces.append([0, 4, 6])
        self._faces.append([1, 4, 6])
        self._faces.append([2, 5, 7])
        self._faces.append([3, 5, 7])
        self._faces.append([4, 8, 10])
        self._faces.append([5, 8, 10])
        self._faces.append([6, 9, 11])
        self._faces.append([7, 9, 11])
        self._faces.append([0, 4, 8])
        self._faces.append([0, 6, 9])
        self._faces.append([1, 4, 10])
        self._faces.append([1, 6, 11])
        self._faces.append([2, 5, 8])
        self._faces.append([2, 7, 9])
        self._faces.append([3, 5, 10])
        self._faces.append([3, 7, 11])

    def complexify(self, complexity):
        ''' Subdivides the icosahedron (the planet) [complexity] times. (i.e. if
            the complexity is 6, this will subdivided the planet 6 times.

            Parameters:
                complexity (int) : How far the planet will be subdivided.
                
        '''   
        for x in range(complexity):

            new_faces = []
            nodelength = len(self._nodes)

            #When subdividing the grid, each face is split into 4 other faces.
            #This means that an extra 3 nodes are needed; each node is inbetween
            #two other nodes.
            for i in range(len(self._faces)):

                #Take a face from the original faces.
                face = self._faces[i]

                #For each combination of nodes in that face:
                for j in range(3):
                    for k in range(j+1, 3):
                        #Create a node that is directly inbetween those two nodes,
                        node1, node2 = self._nodes[face[j]], self._nodes[face[k]]
                        midnode = (node1[0]/2+node2[0]/2, node1[1]/2+node2[1]/2, node1[2]/2+node2[2]/2)
                        #And add it to the existing nodes
                        self._nodes.append(ps.change_distance(midnode, self._radius))

                #Additionally, take the three nodes that make up the face
                node1num, node2num, node3num = face
                node1, node2, node3 = self._nodes[node1num], self._nodes[node2num], self._nodes[node3num]

                #And take the indexes of the new nodes that were just added to the face.
                newnodenum1 = nodelength + i * 3
                newnodenum2 = nodelength + i * 3 + 1
                newnodenum3 = nodelength + i * 3 + 2

                #And add 4 new faces such that each face is the combination
                #of two new nodes and the node that was used to make both
                #of them.
                new_faces.append([node1num, newnodenum1, newnodenum2])
                new_faces.append([node2num, newnodenum1, newnodenum3])
                new_faces.append([node3num, newnodenum2, newnodenum3])
                new_faces.append([newnodenum1, newnodenum2, newnodenum3])

            #Then set the current faces to be the new faces
            self._faces = new_faces

        #And repeat this process [complexity] times.
            

    def assign_biomes(self):
        ''' Assigns a biome to every face on the planet according to its moisture
            level and elevation.
                
        '''
        #For each face on the grid,
        for face in self._faces:
            node1, node2, node3 = self._nodes[face[0]], self._nodes[face[1]], self._nodes[face[2]]

            #Get the node directly in the centre of the face
            mid = ps.get_middle_point(node1, node2, node3)

            #And check the planet_type to see what biome that node should be
            biome_color = self._planet.get_biome(mid)

            #Then add that biome color to the node for later reference.
            face.append(biome_color)
        

    def gen_terrain(self):
        ''' Assigns a pseudo-random height to every node on the planet.
                
        '''
        #Generate an array of node numbers which islands should be located
        #(if applicable for that planet type)
        island_array = self._planet.get_islands(self._nodes)
        new_nodes = []
        #For each nodoe in the grid
        for node in self._nodes:
            #Ask the planet_type how high that node should be (taking into account
            #possible islands)
            noise = self._planet.get_terrain_noise(node, island_array)
            multiplier = 1 + noise

            #And then change that node to be that height
            new_nodes.append(ps.change_distance(node, self._radius*multiplier))
            
        self._nodes = new_nodes
        

    def gen_clouds(self):
        ''' If the planet has clouds, this will generate random clouds.
            Clouds are generated from the existing faces on the planet;
            when a cloud is added it is composed of a face and cloud color
            instead of a brand new face. It is then changed to the appropriate
            height when printed on a GifCanvas.

        '''
        self._cloud_faces = []

        #For each face in the grid.
        for face in self._faces:
            #Get the node in the centre of the face.
            n1, n2, n3 = self._nodes[face[0]], self._nodes[face[1]], self._nodes[face[2]]
            mid = ps.get_middle_point(n1, n2, n3)
            #Retrieve the cloud color
            cloud_color = self._planet.get_cloud_color()
            #If the face is a cloud,
            if self._planet.is_cloud(mid):
                #Add it to the cloud faces.
                new_cloud = face[:-1] + [cloud_color]
                self._cloud_faces.append(new_cloud)
    

class GifCanvas:
    '''GifCanvas is an abstract class that is used to "print" a Planet object
       onto a .gif file.
        
    '''
    def __init__(self, canvas_size, background_color):
        ''' Initializes the GifCanvas object.

            Parameters:
                canvas_size (tuple<int, int>) : The dimensions of the resulting .gif.
                background_color (tuple<int, int, int, int>) : The color of the background.
                
        '''
        self._canvas_width, self._canvas_height = canvas_size
        self._canvas_size = canvas_size
        self._background_color = background_color
        self._gif_images = []
        self._bodies = {}
        self.gen_base_canvas(1, 1)
        self.set_lighting([0, 0, 1])

    def set_lighting(self, light_vector):
        ''' Sets the lighting to come from a specific angle.

            Parameters:
                light_vector (array<float, float, float>) : The direction from which light originates.
                
        '''
        self._light_vector = light_vector

    def gen_base_canvas(self, star_min_size, star_max_size):
        ''' Creates the canvas on which the planet is printed, including stars.

            Parameters:
                star_number (int) : Number of stars in the background
                star_min_size (int) : The minimum star size in pixels wide.
                star_max_size (int) : The maximum star size in pixels wide.
                
        '''
        #Create the base canvas
        self._base_canvas = Image.new("RGB", self._canvas_size, color=self._background_color)
        base_canvas_draw = ImageDraw.Draw(self._base_canvas, 'RGBA')

        #Different star colours
        greenwhite_star = (204, 255, 204, 255)
        blue_star = (153, 204, 255, 255)
        white_star = (255, 255, 255, 255)
        yellowwhite_star = (255, 255, 153, 255)
        yellow_star = (255, 232, 131, 255)
        orange_star = (254, 204, 177, 255)
        orangered_star = (255, 153, 102, 255)
        red_star = (255, 204, 203, 255)
        colors = []
        colors.append(greenwhite_star)
        colors.append(blue_star)
        colors.append(white_star)
        colors.append(yellowwhite_star)
        colors.append(yellow_star)
        colors.append(orange_star)
        colors.append(orangered_star)
        colors.append(red_star)

        #Create a number of stars with a random star colour
        #and random position.
        for i in range(int(self._canvas_width*self._canvas_height/1000)):
            star_color = colors[random.randrange(8)]
            xcentre = random.randrange(self._canvas_width)
            ycentre = random.randrange(self._canvas_height)
            star_size = random.randrange(star_min_size, star_max_size+1)
            coordinates = [xcentre-math.ceil(star_size/2), ycentre-math.ceil(star_size/2), xcentre+math.ceil(star_size/2), ycentre+math.ceil(star_size/2)]
            base_canvas_draw.ellipse(coordinates, fill=star_color)
        
        

    def draw_image(self):
        ''' Draws a single image using a planet object.
                
        '''
        self._canvas = self._base_canvas.copy()
        canvas_draw = ImageDraw.Draw(self._canvas, 'RGBA')

        draw_faces = []
        
        for body, position in self._bodies.items():
            #Add normal faces to the draw list as separate arrays
            #with the zcoord at the front of the array
            for face in body._faces:
                n1, n2, n3 = body._nodes[face[0]], body._nodes[face[1]], body._nodes[face[2]]
                mid = ps.get_middle_point(n1, n2, n3)
                zcoord = mid[2]
                color = ps.lighting(n1, n2, n3, face[3], self._light_vector)
                #color = (120, 120, 0, 255)
                #for testing lighting
                draw_faces.append((zcoord, n1, n2, n3, color, position))

            draw_faces = sorted(draw_faces)[math.ceil(len(draw_faces)/2):len(draw_faces)]
                
            #level 5 takes 0.7 seconds
            #so about 65% of rendering time
            #lighting takes up ~70% of this time

            #Add cloud faces to the draw list
            #This follows the same logic as normal faces.
            for face in body._cloud_faces:
                n1, n2, n3, color = body._nodes[face[0]], body._nodes[face[1]], body._nodes[face[2]], face[3]
                cloud_height = body._planet.get_cloud_height()
                n1 = ps.change_distance(n1, cloud_height)
                n2 = ps.change_distance(n2, cloud_height)
                n3 = ps.change_distance(n3, cloud_height)
                mid = ps.get_middle_point(n1, n2, n3)
                zcoord = mid[2]
                color = ps.lighting(n1, n2, n3, color, self._light_vector)
                draw_faces.append((zcoord, n1, n2, n3, color, position))
                
            #level 5 takes 0.03 seconds
            #so about 3% of rendering time

            #Sort the faces by z coordinate
            draw_faces = sorted(draw_faces)
            
            #level 5 takes 0.05 seconds
            #so about 5% of rendering time

            #Draw the faces in the draw list
            for face in draw_faces:
                xc, yc = face[5]
                fillcolor = face[4]
                canvas_draw.polygon([(face[1][0]+xc, face[1][1]+yc),(face[2][0]+xc, face[2][1]+yc),(face[3][0]+xc, face[3][1]+yc)], fill=fillcolor)
                
            #level 5 takes 0.3 seconds
            #so about 28% of rendering time

        return self._canvas

    def add_body(self, body, position='centre'):
        ''' Adds a planet to the GifCanvas object. All added objects will be drawn.

            Parameters:
                body (PlanetObject) : The body being added to the GifCanvas
                position (tuple<int, int>) : Where the centre of the planet will be drawn
                                             (in x-y coordinates).
                
        '''
        if position == 'centre':
            self._bodies[body] = (self._canvas_width/2, self._canvas_height/2)
        elif self._bodies.get(position[0], None) != None:
            self._bodies[body] = [position[0], [self._bodies[position[0]][0]-position[1], self._bodies[position[0]][1], 0]]
        else:
            self._bodies[body] = position

    def remove_body(self, body):
        ''' Removes a body from the GifCanvas

            Parameters:
                body (PlanetObject) : The body being removed.
                
        '''
        del self._bodies[body]
        
    def make_img(self, filepath='movie.jpeg'):
        ''' Generates a still image of the planet

            Parameters:
                filepath (str) : Where the image will be saved.
                
        '''
        image = self.draw_image()
        image.save(filepath, "JPEG")
	

    def make_gif(self, fps=60, filepath='movie.gif'):
        ''' Generates a gif of the planets currently loaded in the GifCanvas.

            Parameters:
                fps (int) : The desired frames per second of the final gif.
                filepath (str) : Where the gif will be saved.
                
        '''
        self._gif_images = []
        for i in range(360):
            for body, position in self._bodies.items():
                #body.spin(2) Removed until I find a more optimised version because it takes fucking forever to spin this shit
                #beyblades let em rip
                body.temp_rotate(1)
                image = self.draw_image()
                image = np.asarray(image)
                self._gif_images.append(image)
            print('Image', i+1, 'completed.')
                
        self.save_gif(fps, filepath)


    def save_gif(self, fps=60, filepath='movie.mp4'):
        ''' Saves a gif of the planets currently loaded in the GifCanvas.

            Parameters:
                fps (int) : The desired frames per second of the final gif.
                filepath (str) : Where the gif will be saved.
                
        '''
        if self._gif_images != []:
            imageio.mimsave(filepath, self._gif_images, fps=fps)
            print('Gif saved!')


def main():

    background_color = (0, 0, 0, 255)
    canvas_size = (750, 750)

    #create the planet type and planet object
    seed = str(input('Please enter a seed: '))
    complexity = int(input('Please enter a complexity: '))
    planettype = pt.IcePlanet(450, seed)
    planet = PlanetObject(planettype, complexity)

    #draw the planet
    gifcanvas = GifCanvas(canvas_size, background_color)
    gifcanvas.add_body(planet, 'centre')
    light_vector = [-1, 0, 1]
    gifcanvas.set_lighting(light_vector)
    gifcanvas.make_gif()

def make_gif(complexity):
    background_color = (0, 0, 0, 255)
    canvas_size = (750, 750)

    #create the planet type and planet object
    seed = random.random()
    planettype = pt.EarthAnalog(450, seed)
    planet = PlanetObject(planettype, complexity)

    #draw the planet
    gifcanvas = GifCanvas(canvas_size, background_color)
    gifcanvas.add_body(planet, 'centre')
    light_vector = [-1, 0, 1]
    gifcanvas.set_lighting(light_vector)
    gifcanvas.make_gif()

def make_img(complexity):
    background_color = (0, 0, 0, 255)
    canvas_size = (1280, 720)

    seed = random.random()
    planet_types = [pt.EarthAnalog(500, seed),
                    pt.IronPlanet(500, seed),
                    pt.IcePlanet(500, seed)]
    planet_type = random.choice(planet_types)
    planet = PlanetObject(planet_type, complexity)

    gifcanvas = GifCanvas(canvas_size, background_color)
    gifcanvas.add_body(planet, 'centre')
    light_vector = [-1, 0, 1]
    gifcanvas.set_lighting(light_vector)
    gifcanvas.make_img()
    
if __name__ == "__main__":
    main()
