import random, math
import numpy as np
import json

units = json.loads(open('json/units.json').read())
classes = json.loads(open('json/units.json').read())

stats = dict()
stats['sun_mass'] = -math.log(random.random()) + 0.45
stats['sun_age'] = random.uniform(0.01*(stats['sun_mass'])**(-2.5), 10*(stats['sun_mass'])**(-2.5))
stats['sun_radii'] = 0.6*math.exp(0.3*stats['sun_mass'])
stats['sun_temp'] = 3700*stats['sun_mass'] + 2100
stats['sun_lum'] = 0.05*math.exp(3*stats['sun_mass'])

stats['planet_age'] = random.uniform(0.8*stats['sun_age'], 0.9*stats['sun_age'])
stats['planet_albedo'] = random.uniform(0, 1)
stats['planet_dist'] = random.uniform(0.25, 85)
if stats['planet_dist'] > 75:
    stats['planet_dist'] = -1
    stats['planet_eqtemp'] = random.uniform(0, 10)
else:
    stats['planet_eqtemp'] = (stats['sun_temp'])*((1-stats['planet_albedo'])**0.25)*(7*10**6*stats['sun_radii']/(3*10**8*stats['planet_dist']))**0.5

for key, item in stats.items():
    print(key, item, units.get(key, ''))







