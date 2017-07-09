# Atlas

This is a python script designed to generate random planets, along with an animation of the planet in .gif format. The script currently uses the Python Imaging Library (PIL) and imageio libraries to create the gif, and math/random/numpy to generate the models. The end goal of this project is to create a script capable of generating a planet every day and posting it to a facebook page made specifically to display these planets.

## Short Explanation
Each planet is a [subdivided icosahedron](https://en.wikipedia.org/wiki/Geodesic_grid) which has been normalised (pushed outwards) to the inside of a sphere. Terrain is generated and coloured randomly depending on planet type, but is done using 3D [Perlin noise](https://en.wikipedia.org/wiki/Perlin_noise) in order to create a 'natural' looking change between environments/biomes. The planet lighting is based on the direction each face is facing. Facing away reduces exposure to light, facing towards increases exposure.

## Credit
I must give credit to the following sources for their explanation and implementation of perlin noise generation and biome generation, which I drew inspiration from when adding terrain and biome generation to this project:
[Making maps with noise functions](http://www.redblobgames.com/maps/terrain-from-noise/) and
[Polygonal Map Generation for Games](http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/)
both by/at [Red Blob Games](http://www.redblobgames.com/)
and
[Procedural Planet Generation](http://experilous.com/1/blog/post/procedural-planet-generation) by Andy Gainey
at [Experilous.com](http://experilous.com/)

I'd also like give credit for the biome colourings on my earth-like planets to [Red Blob Games](http://www.redblobgames.com/) again for their adaptation of the [Whittaker diagram](http://w3.marietta.edu/~biol/biomes/biome_main.htm).


## Currently Implemented
 - **Planet Types**
     - Earth Analog (Terrestrial planets with plant life and liquid water oceans)
     - Iron Planets (Terrestrial planet with a high concentration of iron or iron oxide on its surface)

 - **General Features**
     - Terrain generation (mountains, valleys, islands, etc.)
     - Biome assignment (colourings of different sections of each planet by moisture level and elevation)
     - Clouds
     - Random axis of rotation
     
 - **Animation Generation**
     - One full rotation around the axis of rotation for the planet
     - Stars (randomly generated and coloured stars are placed in the background)
     - Lighting (generated using a 3d vector indicating the direction of exposure)
     
## To Be Implemented
 - **Planet Types**
     - Gas Planets
         - Gas Dwarfs (essentially a smaller version of a gas giant)
         - Gas Giants (e.g. Saturn, Jupiter)
         - Ice Giants (e.g. Neptune, Uranus)
         - Chthonian Planets (a gas planet with the gas largely removed due to close proximity to its star)
         - Helium Planets (a gas planet with an atmosphere composed primarily of helium)
     - Terrestrial Planets
         - Ice Planet (A planet composed entirely of ice C02, O2, etc.)
         - Silicate Planet (A terrestrial planet with a crust/mantle primarily composed of silicate-based compounds)
         - Carbon Planet (A planet with a crust/mantle primarily composed of carbon-based compounds)
         - Desert Planet (Like Tattooine, Arrakis, a planet with a surface with extremely low amounts of liquid water)
     - Other
         - Lava Planet (A planet which has a surface entirely covered in lava/magma.
         - Ocean Planet (A planet entirely covered in liquid water)

 - **General Features**
     - Orbiting bodies such as moons, binary planets, etc.
     - Optimising the generation of biomes and terrain
     
 - **Animation Generation**
     - Add support for orbiting bodies as mentioned above
     - Optimising the rotation of planets and their orbiting bodies
     - Optimising gif generation
