from PIL import ImageDraw, Image, ImageFont
import numpy as np
import imageio
import math, random
import time, datetime
import planet_support as ps
import planet_types as pt

class PlanetaryObject(object):

    def __init__(self, planet_type, seed, complexity):
        self._planet = planet_type
        self._diameter = self._planet.get_diameter()
        self.define_base_nodes()
        self.define_base_faces()
        self.complexify(complexity)
        random.seed(seed)
        self.define_rotation()


    def define_rotation(self):
        spin_options = [-1, 1]
        self._axis_spin = random.choice(spin_options)
        self._axis_elevation_angle = random.randrange(-90, 90)
        self._axis_azimuth_angle = random.randrange(-180, 180)
        self.set_axis()

    def spin(self, speed):
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


            
        

    def set_axis(self):
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
        d = self._diameter
        a = d / math.sqrt(11 + 2*math.sqrt(5))
        phi = a * (1 + math.sqrt(5))/2
        self._nodes = []
        self._nodes.append(ps.change_distance([0, -a, -phi], self._diameter))
        self._nodes.append(ps.change_distance([0, -a, phi], self._diameter))
        self._nodes.append(ps.change_distance([0, a, -phi], self._diameter))
        self._nodes.append(ps.change_distance([0, a, phi], self._diameter))
        self._nodes.append(ps.change_distance([-a, -phi, 0], self._diameter))
        self._nodes.append(ps.change_distance([-a, phi, 0], self._diameter))
        self._nodes.append(ps.change_distance([a, -phi, 0], self._diameter))
        self._nodes.append(ps.change_distance([a, phi, 0], self._diameter))
        self._nodes.append(ps.change_distance([-phi, 0, -a], self._diameter))
        self._nodes.append(ps.change_distance([phi, 0, -a], self._diameter))
        self._nodes.append(ps.change_distance([-phi, 0, a], self._diameter))
        self._nodes.append(ps.change_distance([phi, 0, a], self._diameter))

    def define_base_faces(self):
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
            
        for x in range(complexity):

            new_faces = []
            nodelength = len(self._nodes)
            
            for i in range(len(self._faces)):
                
                face = self._faces[i]

                for j in range(3):
                    for k in range(j+1, 3):
                        node1, node2 = self._nodes[face[j]], self._nodes[face[k]]
                        midnode = ps.get_middle_point(node1, node2)
                        self._nodes.append(ps.change_distance(midnode, self._diameter))

                node1num, node2num, node3num = face
                node1, node2, node3 = self._nodes[node1num], self._nodes[node2num], self._nodes[node3num]
                
                newnodenum1 = nodelength + i * 3
                newnodenum2 = nodelength + i * 3 + 1
                newnodenum3 = nodelength + i * 3 + 2

                new_faces.append([node1num, newnodenum1, newnodenum2])
                new_faces.append([node2num, newnodenum1, newnodenum3])
                new_faces.append([node3num, newnodenum2, newnodenum3])
                new_faces.append([newnodenum1, newnodenum2, newnodenum3])

            self._faces = new_faces



class EarthAnalog(PlanetaryObject):

    def __init__(self, planet_type, seed, complexity):
        super().__init__(planet_type, seed, complexity)
        self.gen_terrain()
        self.assign_biomes()
        self.gen_clouds()

    def assign_biomes(self):
        
        moisture_noise_hash = hash(random.random())
        
        for face in self._faces:
            node1, node2, node3 = self._nodes[face[0]], self._nodes[face[1]], self._nodes[face[2]]
            mid = ps.get_middle_point(node1, node2, node3)

            height = ps.get_height(mid)

            tml = self._planet.get_moisture_levels()
            tel = self._planet.get_elevation_levels()
            mw = self._planet.get_moisture_width()

            min_height = self._planet.get_min_height()
            height_range = self._planet.get_height_range()
            
            moisture_level = ps.perlin(mid, mw, tml, moisture_noise_hash)
            
            if moisture_level > 0.55*tml:
                moisture_level = moisture_level*(2 - moisture_level/tml)
            elif moisture_level < 0.45*tml:
                moisture_level = tml - (tml-moisture_level)*(1 + moisture_level/tml)
                
            moisture_level = math.ceil(moisture_level)
            elevation_level = math.ceil(tel*(height-min_height)/height_range)
            
            biome_color = self._planet.get_biome_color(elevation_level, moisture_level)
            
            face.append(biome_color)
        

    def gen_terrain(self):

        terrain_large_noise_hash = hash(random.random())
        terrain_med_noise_hash = hash(random.random())
        terrain_small_noise_hash = hash(random.random())

        nodes_length = len(self._nodes)
        
        largenoisewidth, mednoisewidth, smallnoisewidth = self._planet.get_terrain_width()
        lnd, mnd, snd = self._planet.get_terrain_noise()

        amplitude = self._planet.get_terrain_amplitude()
        
        max_height = self._planet.get_max_height()
        min_height = self._planet.get_min_height()
        height_range = self._planet.get_height_range()

        max_island_number, min_island_number = self._planet.get_island_number_range()
        max_island_size, min_island_size = self._planet.get_island_size_range()
        
        island_total = random.randrange(min_island_number, max_island_number + 1)
        rmarray = []
        for i in range(island_total):
            island_size = random.random()*(max_island_size - min_island_size) + min_island_size
            rmarray.append([self._nodes[random.randrange(nodes_length)], island_size])
        
        new_nodes = []
        for node in self._nodes:

            min_dist_ratio = 0

            for rm in rmarray:
                island_size = rm[1]
                dist_from_mountain = math.sqrt((node[0]-rm[0][0])**2 + (node[1]-rm[0][1])**2 + (node[2]-rm[0][2])**2)
                dist_ratio = 1 - dist_from_mountain/island_size
                if dist_ratio > min_dist_ratio:
                    min_dist_ratio = dist_ratio

            

            large_noise = ps.perlin(node, largenoisewidth, amplitude, terrain_large_noise_hash)
            med_noise = ps.perlin(node, mednoisewidth, amplitude, terrain_med_noise_hash)
            small_noise = ps.perlin(node, smallnoisewidth, amplitude, terrain_small_noise_hash)

            noise = (lnd*large_noise + mnd*med_noise + snd*small_noise)
            actual_noise = noise - amplitude*(lnd + mnd + snd)*(1-min_dist_ratio)
            if actual_noise < 0:
                actual_noise = 0
            multiplier = 1 + actual_noise

            new_nodes.append(ps.change_distance(node, self._diameter, multiplier))
                
        self._nodes = new_nodes

    def gen_clouds(self):
        cloud_color = self._planet.get_cloud_color()
        self._cloud_faces = []
        if cloud_color == None:
            pass
        cloud_hash = hash(random.random())
        cloud_cutoff = self._planet.get_cloud_cutoff()
        cloud_noise_width = self._planet.get_cloud_width()
        cloud_height = self._planet.get_cloud_height()
        for face in self._faces:
            n1, n2, n3 = self._nodes[face[0]], self._nodes[face[1]], self._nodes[face[2]]
            middle_node = ps.get_middle_point(n1, n2, n3)
            cloud_noise = ps.perlin(middle_node, cloud_noise_width, 1, cloud_hash)
            if cloud_noise > cloud_cutoff:
                new_cloud = face[:-1] + [cloud_color]
                self._cloud_faces.append(new_cloud)
            
        


class GifCanvas:

    def __init__(self, canvas_size, background_color):
        self._canvas_width, self._canvas_height = canvas_size
        self._canvas_size = canvas_size
        self._background_color = background_color
        self._gif_images = []
        self._bodies = {}
        self.gen_base_canvas(100, 1, 1)
        self.set_lighting([0, 0, 1])

    def set_lighting(self, light_vector):
        self._light_vector = light_vector

    def gen_base_canvas(self, star_number, star_min_size, star_max_size):
        self._base_canvas = Image.new("RGB", self._canvas_size, color=self._background_color)
        base_canvas_draw = ImageDraw.Draw(self._base_canvas, 'RGBA')

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

        for i in range(int(self._canvas_width*self._canvas_height/1000)):
            star_color = colors[random.randrange(8)]
            xcentre = random.randrange(self._canvas_width)
            ycentre = random.randrange(self._canvas_height)
            star_size = random.randrange(star_min_size, star_max_size+1)
            coordinates = [xcentre-math.ceil(star_size/2), ycentre-math.ceil(star_size/2), xcentre+math.ceil(star_size/2), ycentre+math.ceil(star_size/2)]
            base_canvas_draw.ellipse(coordinates, fill=star_color)
        
        

    def draw_image(self):
        self._canvas = self._base_canvas.copy()
        canvas_draw = ImageDraw.Draw(self._canvas, 'RGBA')

        draw_faces = []
        
        for body, position in self._bodies.items():
            for face in body._faces:
                n1, n2, n3 = body._nodes[face[0]], body._nodes[face[1]], body._nodes[face[2]]
                mid = ps.get_middle_point(n1, n2, n3)
                zcoord = mid[2]
                color = ps.lighting(n1, n2, n3, face[3], self._light_vector)
                draw_faces.append((zcoord, n1, n2, n3, color, position))

            for face in body._cloud_faces:
                n1, n2, n3, color = body._nodes[face[0]], body._nodes[face[1]], body._nodes[face[2]], face[3]
                cloud_height = body._planet.get_cloud_height()
                n1 = ps.change_distance(n1, 2*cloud_height)
                n2 = ps.change_distance(n2, 2*cloud_height)
                n3 = ps.change_distance(n3, 2*cloud_height)
                mid = ps.get_middle_point(n1, n2, n3)
                zcoord = mid[2]
                color = ps.lighting(n1, n2, n3, color, self._light_vector)
                draw_faces.append((zcoord, n1, n2, n3, color, position))


            draw_faces = sorted(draw_faces)
            
            for face in draw_faces:
                xc, yc = face[5]
                fillcolor = face[4]
                canvas_draw.polygon([(face[1][0]+xc, face[1][1]+yc),(face[2][0]+xc, face[2][1]+yc),(face[3][0]+xc, face[3][1]+yc)], fill=fillcolor)

        return self._canvas

    def add_body(self, body, position='centre'):
        if position == 'centre':
            self._bodies[body] = (self._canvas_width/2, self._canvas_height/2)
        elif self._bodies.get(position[0], None) != None:
            self._bodies[body] = [position[0], [self._bodies[position[0]][0]-position[1], self._bodies[position[0]][1], 0]]
        else:
            self._bodies[body] = position

    def remove_body(self, body):
        del self._bodies[body]
        
    def make_gif(self, fps=60, filepath='movie.gif'):
        self._gif_images = []
        for i in range(180):
            for body, position in self._bodies.items():
                body.spin(2)
                image = self.draw_image()
                image = np.asarray(image)
                self._gif_images.append(image)
            print('Image', i+1, 'completed.')
                
        self.save_gif(fps, filepath)


    def save_gif(self, fps=60, filepath='movie.mp4'):
        if self._gif_images != []:
            imageio.mimsave(filepath, self._gif_images, fps=fps)
            print('Gif saved!')


def main():

    background_color = (0, 0, 0, 255)
    canvas_size = (750, 750)

    planet_type = pt.TerrestrialOceans(450)

    seed = str(input('Please enter a seed: '))
    complexity = int(input('Please enter a complexity: '))
    planet = EarthAnalog(planet_type, seed, complexity)
    
    gifcanvas = GifCanvas(canvas_size, background_color)
    gifcanvas.add_body(planet, 'centre')
    light_vector = [0, 0, 1]
    gifcanvas.set_lighting(light_vector)
    gifcanvas.make_gif()
    
if __name__ == "__main__":
    main()
