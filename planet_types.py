import planet_support as ps
import random, math

class BodySetting(object):
    ''' Abstract class containing all the values that a planet requires.
        This includes random hashes which are used to generate:
            - Moisture
                ~ (mh)
            - Terrain elevation
                ~ (tlh, tmh, tsh)
            - Clouds (optional)
                ~ (ch)
                
        Also, it includes other random values such as:
            - Seed (The seed generating the planet)
                ~ (seed)
            - Diameter
                ~ (diameter)
            - Values dictating how terrain is generated
                ~ (large_noise_weight, medium_noise_weight, small_noise_weight)
                ~ (large_noise_width, medium_noise_width, small_noise_width)
                ~ (amplitude)
                ~ (max_height, min_height)
            - Values dictating how moisture is generated
                ~ (moisture_noise_width)
            - Values dictating how biomes are decided
                ~ (total_moisture_levels, total_elevation_levels)
                ~ (biome_dictionary)

        Further, planet-specific values are detailed in the comments under
        their respective class.
    '''
    def __init__(self, diameter, seed):
        ''' Initializes the BodySetting class

            Parameters:
                diameter (int) : The diameter (size) of the planet
                seed (str) : The string used to seed the planet's generation

        '''
        self._diameter = diameter
        self._seed = seed

    def get_attributes(self):
        return self._attr

    def set_hashes(self):
        ''' Sets the hashes that are used for random generation of terrain,
            moisture and clouds if applicable.
        '''
        random.seed(self._seed)
        self._mh = hash(random.random())
        #moisture hash
        self._tlh = hash(random.random())
        #terrain large hash
        self._tmh = hash(random.random())
        #terrain medium hash
        self._tsh = hash(random.random())
        #terrain small hash

        if self._clouds_boolean:
            self._ch = hash(random.random())

    def get_diameter(self):
        return self._diameter
    
    def get_biome_color(self, elevation, moisture):
        return self._biome_dict[self._biome_assignments.get((elevation, moisture), self._biome_other)]

    def get_terrain_noise(self, node, island_array):
        large_noise = ps.perlin(node, self._large_noise_width, self._amplitude, self._tlh)
        med_noise = ps.perlin(node, self._medium_noise_width, self._amplitude, self._tmh)
        small_noise = ps.perlin(node, self._small_noise_width, self._amplitude, self._tsh)
        
        lnd, mnd, snd = self._large_noise_weight, self._medium_noise_weight, self._small_noise_weight
        noise = (lnd*large_noise + mnd*med_noise + snd*small_noise)

        if self._islands_boolean:
            min_dist_ratio = 0
            for island in island_array:
                    island_size = island[1]
                    dist_from_mountain = math.sqrt((node[0]-island[0][0])**2 + (node[1]-island[0][1])**2 + (node[2]-island[0][2])**2)
                    dist_ratio = 1 - dist_from_mountain/island_size
                    if dist_ratio > min_dist_ratio:
                        min_dist_ratio = dist_ratio
            noise = noise - self._amplitude*(lnd + mnd + snd)*(1-min_dist_ratio)
            if noise < 0:
                return 0
            else:
                return noise
        return noise

    def get_moisture_noise(self, node):
        noise = ps.perlin(node, self._moisture_noise_width, self._total_moisture_levels, self._mh)
        try:
            altitude = abs(math.asin(2*node[1]/self._diameter))
        except:
            altitude = 1

        noise = (self._total_moisture_levels - 1)*noise*altitude**2/self._total_moisture_levels + altitude
            
            
        if noise > self._total_moisture_levels:
            noise = self._total_moisture_levels
        return noise

    def get_biome(self, node):
        height = ps.get_height(node)
        moisture_level = math.ceil(self.get_moisture_noise(node))
        elevation_level = math.ceil(self._total_elevation_levels*(height-self._min_height)/self._height_range)
        
        return self.get_biome_color(elevation_level, moisture_level)

    def get_islands(self, nodes):
        island_array = []
        if self._islands_boolean:
            island_total = random.randrange(self._min_island_number, self._max_island_number + 1)
            for i in range(island_total):
                island_size = random.random()*(self._max_island_size - self._min_island_size) + self._min_island_size
                island_array.append([nodes[random.randrange(len(nodes))], island_size])
        return island_array

    def is_cloud(self, node):
        if self._clouds_boolean:
            cloud_noise = self.get_cloud_noise(node)
            return (cloud_noise > self._cloud_noise_cutoff)
        return False

    def get_cloud_noise(self, node):
        if self._clouds_boolean:
            noise = ps.perlin(node, self._cloud_noise_width, 1, self._ch)
            return noise

    def get_cloud_color(self):
        if self._clouds_boolean:
            return self._cloud_color

    def get_cloud_height(self):
        if self._clouds_boolean:
            return self._cloud_height
        

class PlanetSetting(BodySetting):

    def __init__(self, diameter, seed):
        super().__init__(diameter, seed)
        

class TerrestrialPlanet(PlanetSetting):

    def __init__(self, diameter, seed):
        super().__init__(diameter, seed)
        

class GasPlanet(PlanetSetting):

    def __init__(self, diameter, seed):
        super().__init__(diameter, seed)


class MoonSetting(BodySetting):

    def __init__(self, diameter, seed, orbiting_body):
        super().__init__(diameter, seed)
        self._orbiting_body = orbiting_body

    def get_orbiting_body(self):
        return self._orbiting_body

        

''' The following classes are different planet types. EarthAnalog is given as an example
    to show exactly what is needed for a terrestrial planet, and GasGiant is given as
    an example of a gas planet. ClassicMoon is also commented as an example of a moon.
'''

##
## TERRESTRIAL PLANETS
##

class IronPlanet(TerrestrialPlanet):

    def __init__(self, diameter, seed):

        super().__init__(diameter, seed)
        
        self._planet_type = 'IRON TERRESTRIAL'
        self._attr = {'atmosphere': 0}

        #Terrain_noise_generation
        self._large_noise_weight = 1
        self._medium_noise_weight = 0.3
        self._small_noise_weight = 0.1
        self._large_noise_width = (1/4) * self._diameter
        self._medium_noise_width = (1/8) * self._diameter
        self._small_noise_width = (1/14) * self._diameter
        self._max_height = 0.55*self._diameter
        self._min_height = 0.5*self._diameter
        self._height_range = self._max_height - self._min_height
        self._amplitude = self._height_range/(0.5*self._diameter*(self._large_noise_weight + self._medium_noise_weight + self._small_noise_weight))

        #Moisture_noise_generation
        self._moisture_noise_width = (1/4)*self._diameter

        #Biomes
        self._total_moisture_levels = 4
        self._total_elevation_levels = 3
        
        #Biome colors
        self._biome_dict = {}
        self._biome_dict['SOOT'] = (130, 107, 70, 255)
        self._biome_dict['HIGH IRON'] = (138, 94, 69, 255)
        self._biome_dict['MEDIUM IRON'] = (197, 127, 91, 255)
        self._biome_dict['LOW IRON'] = (203, 145, 124, 255)
        self._biome_dict['ICE'] = (224, 255, 255, 255)
        self._biome_dict['SNOW'] = (255, 255, 255, 255)
        self._biome_dict['BASE TERRAIN'] = (168, 121, 103, 255)
        # Elevation level, moisture_level --> Biome
        self._biome_assignments = {}
        self._biome_assignments[(3, 4)] = 'ICE'
        self._biome_assignments[(3, 3)] = 'SNOW'
        self._biome_assignments[(3, 2)] = 'HIGH IRON'
        self._biome_assignments[(3, 1)] = 'MEDIUM IRON'
        self._biome_assignments[(2, 4)] = 'ICE'
        self._biome_assignments[(2, 3)] = 'SNOW'
        self._biome_assignments[(2, 2)] = 'MEDIUM IRON'
        self._biome_assignments[(2, 1)] = 'LOW IRON'
        self._biome_assignments[(1, 4)] = 'SNOW'
        self._biome_assignments[(1, 3)] = 'MEDIUM IRON'
        self._biome_assignments[(1, 2)] = 'LOW IRON'
        self._biome_assignments[(1, 1)] = 'SOOT'
        self._biome_other = 'BASE TERRAIN'

        #Clouds
        self._clouds_boolean = False
        self._cloud_color = None
        self._cloud_height = None
        self._cloud_noise_width = None
        self._cloud_noise_cutoff = None

        #Islands
        self._islands_boolean = False
        self._max_island_number = None
        self._min_island_number = None
        self._max_island_size = None
        self._min_island_size = None

        self.set_hashes()

class IcePlanet(TerrestrialPlanet):

    def __init__(self, diameter, seed):

        super().__init__(diameter, seed)
        
        self._planet_type = 'ICE TERRESTRIAL'
        self._attr = {'atmosphere': 0}

        #Terrain_noise_generation
        self._large_noise_weight = 1
        self._medium_noise_weight = 0.3
        self._small_noise_weight = 0.1
        self._large_noise_width = (1/4) * self._diameter
        self._medium_noise_width = (1/8) * self._diameter
        self._small_noise_width = (1/14) * self._diameter
        self._max_height = 0.55*self._diameter
        self._min_height = 0.5*self._diameter
        self._height_range = self._max_height - self._min_height
        self._amplitude = self._height_range/(0.5*self._diameter*(self._large_noise_weight + self._medium_noise_weight + self._small_noise_weight))

        #Moisture_noise_generation
        self._moisture_noise_width = (1/2)*self._diameter

        #Biomes
        self._total_moisture_levels = 3
        self._total_elevation_levels = 3
        
        #Biome colors
        self._biome_dict = {}
        self._biome_dict['HEAVY SNOW'] = (248, 248, 248, 255)
        self._biome_dict['HEAVY ICE'] = (229, 246, 255, 255)
        self._biome_dict['LIGHT BLUE ICE'] = (212, 240, 255, 255)
        self._biome_dict['MEDIUM BLUE ICE'] = (203, 237, 255, 255)
        self._biome_dict['LIGHT GREEN ICE'] = (203, 255, 246, 255)
        self._biome_dict['MEDIUM GREEN ICE'] = (177, 255, 241, 255)
        self._biome_dict['DARK GREEN ICE'] = (153, 255, 236, 255)
        self._biome_dict['DARK BLUE ICE'] = (143, 206, 239, 255)
        self._biome_dict['MEDIUM BLUEISH ICE'] = (153, 220, 255, 255)
        self._biome_dict['BASE TERRAIN'] = (120, 196, 236, 255)
        # Elevation level, moisture_level --> Biome
        self._biome_assignments = {}
        self._biome_assignments[(3, 3)] = 'HEAVY SNOW'
        self._biome_assignments[(3, 2)] = 'HEAVY ICE'
        self._biome_assignments[(3, 1)] = 'LIGHT BLUE ICE'
        self._biome_assignments[(2, 3)] = 'MEDIUM BLUE ICE'
        self._biome_assignments[(2, 2)] = 'LIGHT GREEN ICE'
        self._biome_assignments[(2, 1)] = 'MEDIUM GREEN ICE'
        self._biome_assignments[(1, 3)] = 'DARK GREEN ICE'
        self._biome_assignments[(1, 2)] = 'DARK BLUE ICE'
        self._biome_assignments[(1, 1)] = 'MEDIUM BLUEISH ICE'
        self._biome_other = 'BASE TERRAIN'

        #Clouds
        self._clouds_boolean = False
        self._cloud_color = None
        self._cloud_height = None
        self._cloud_noise_width = None
        self._cloud_noise_cutoff = None

        #Islands
        self._islands_boolean = False
        self._max_island_number = None
        self._min_island_number = None
        self._max_island_size = None
        self._min_island_size = None

        self.set_hashes()


class EarthAnalog(TerrestrialPlanet):

    def __init__(self, diameter, seed):

        super().__init__(diameter, seed)
        
        self._planet_type = 'TERRESTRIAL OCEANS'
        self._attr = {'atmosphere': 0.3}

        #Terrain_noise_generation
        self._large_noise_weight = 1
        self._medium_noise_weight = 0.3
        self._small_noise_weight = 0.1
        self._large_noise_width = (1/4) * self._diameter
        self._medium_noise_width = (1/8) * self._diameter
        self._small_noise_width = (1/14) * self._diameter
        self._max_height = 0.55*self._diameter
        self._min_height = 0.5*self._diameter
        self._height_range = self._max_height - self._min_height
        self._amplitude = self._height_range/(0.5*self._diameter*(self._large_noise_weight + self._medium_noise_weight + self._small_noise_weight))

        #Moisture_noise_generation
        self._moisture_noise_width = (1/5)*self._diameter

        #Biomes
        self._total_moisture_levels = 6
        self._total_elevation_levels = 4
        
        #Biome colors
        self._biome_dict = {}
        self._biome_dict['SNOW'] = (248, 248, 248, 255)
        self._biome_dict['TUNDRA'] = (221, 221, 187, 255)
        self._biome_dict['BARE'] = (187, 187, 187, 255)
        self._biome_dict['SCORCHED'] = (153, 153, 153, 255)
        self._biome_dict['TAIGA'] = (204, 212, 187, 255)
        self._biome_dict['SHRUBLAND'] = (196, 204, 187, 255)
        self._biome_dict['TEMPERATE DESERT'] = (228, 232, 202, 255)
        self._biome_dict['TEMPERATE RAIN FOREST'] = (164, 196, 168, 255)
        self._biome_dict['TEMPERATE DECIDUOUS FOREST'] = (180, 196, 169, 255)
        self._biome_dict['GRASSLAND'] = (196, 212, 170, 255)
        self._biome_dict['TROPICAL RAIN FOREST'] = (156, 187, 169, 255)
        self._biome_dict['TROPICAL SEASONAL FOREST'] = (169, 204, 164, 255)
        self._biome_dict['SUBTROPICAL DESERT'] = (233, 221, 199, 255)
        self._biome_dict['OCEAN'] = (63, 156, 255, 255)
        # Elevation level, moisture_level --> Biome
        self._biome_assignments = {}
        self._biome_assignments[(4, 6)] = 'SNOW'
        self._biome_assignments[(4, 5)] = 'SNOW'
        self._biome_assignments[(4, 4)] = 'SNOW'
        self._biome_assignments[(4, 3)] = 'TUNDRA'
        self._biome_assignments[(4, 2)] = 'BARE'
        self._biome_assignments[(4, 1)] = 'SCORCHED'
        self._biome_assignments[(3, 6)] = 'SNOW'
        self._biome_assignments[(3, 5)] = 'TAIGA'
        self._biome_assignments[(3, 4)] = 'SHRUBLAND'
        self._biome_assignments[(3, 3)] = 'SHRUBLAND'
        self._biome_assignments[(3, 2)] = 'TEMPERATE DESERT'
        self._biome_assignments[(3, 1)] = 'TEMPERATE DESERT'
        self._biome_assignments[(2, 6)] = 'SNOW'
        self._biome_assignments[(2, 5)] = 'TEMPERATE DECIDUOUS FOREST'
        self._biome_assignments[(2, 4)] = 'TEMPERATE DECIDUOUS FOREST'
        self._biome_assignments[(2, 3)] = 'GRASSLAND'
        self._biome_assignments[(2, 2)] = 'GRASSLAND'
        self._biome_assignments[(2, 1)] = 'TEMPERATE DESERT'
        self._biome_assignments[(1, 6)] = 'TROPICAL RAIN FOREST'
        self._biome_assignments[(1, 5)] = 'TROPICAL RAIN FOREST'
        self._biome_assignments[(1, 4)] = 'TROPICAL SEASONAL FOREST'
        self._biome_assignments[(1, 3)] = 'TROPICAL SEASONAL FOREST'
        self._biome_assignments[(1, 2)] = 'GRASSLAND'
        self._biome_assignments[(1, 1)] = 'SUBTROPICAL DESERT'
        self._biome_other = 'OCEAN'

        #Clouds
        self._clouds_boolean = True
        self._cloud_color = (255, 255, 255, 255)
        self._cloud_height = self._max_height
        self._cloud_noise_width = (1/5) * self._diameter
        self._cloud_noise_cutoff = 0.75

        #Islands
        self._islands_boolean = True
        self._max_island_number = 14
        self._min_island_number = 7
        self._max_island_size = (2/3) * self._diameter
        self._min_island_size = (1/5) * self._diameter

        self.set_hashes()



##
## GAS PLANETS
##





##
## MOONS
##
        
class ClassicMoon(MoonSetting):

    def __init__(self, diameter, orbiting_body):

        super().__init__(diameter, orbiting_body)
        
        self._planet_type = 'CLASSIC MOON'
        self._attr = {'atmosphere': 0}

        #Terrain_generation
        self._max_island_number = 35
        self._min_island_number = 30
        self._max_island_size = (3/5) * self._diameter
        self._min_island_size = (1/10) * self._diameter

        #Terrain_noise_generation
        self._large_noise_weight = 1
        self._medium_noise_weight = 0.4
        self._small_noise_weight = 0.3
        self._large_noise_width = (1/5) * self._diameter
        self._medium_noise_width = (1/10) * self._diameter
        self._small_noise_width = (1/20) * self._diameter
        self._max_height = 0.51*self._diameter
        self._min_height = 0.5*self._diameter
        self._height_range = self._max_height - self._min_height
        self._amplitude = self._height_range/(0.5*self._diameter*(self._large_noise_weight + self._medium_noise_weight + self._small_noise_weight))

        #Moisture_noise_generation
        self._moisture_noise_width = (1/3)*self._diameter

        #Biomes
        self._total_moisture_levels = 2
        self._total_elevation_levels = 2
        
        #Biome colors
        self._biome_dict = {}
        self._biome_dict['GREY1'] = (200, 200, 200, 255)
        self._biome_dict['GREY2'] = (180, 180, 180, 255)
        self._biome_dict['GREY3'] = (187, 180, 160, 255)
        self._biome_dict['GREY4'] = (153, 153, 153, 255)
        self._biome_dict['GREY5'] = (204, 212, 187, 255)
        # Elevation level, moisture_level --> Biome
        self._biome_assignments = {}
        self._biome_assignments[(2, 2)] = 'GREY1'
        self._biome_assignments[(1, 2)] = 'GREY2'
        self._biome_assignments[(2, 1)] = 'GREY3'
        self._biome_assignments[(1, 1)] = 'GREY4'
        self._biome_other = 'GREY5'

        self.set_hashes(seed)




