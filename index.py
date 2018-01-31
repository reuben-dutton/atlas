import planet_main as pm
import facebook, requests
import json
import sys

env = json.loads(open(sys.path[0] + '/env.json').read())
page_id = env['page_id']
at = env['page_token']

graph = facebook.GraphAPI(access_token=at)

pm.make_img(7)

graph.put_photo(image=open('movie.gif', 'rb'), message='')

