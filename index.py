import planet_main as pm
import facebook, requests
import json

env = json.loads(open('env.json').read())
page_id = '140719353303841'
at = env['page_token']

graph = facebook.GraphAPI(access_token=at)

pm.make_img(5)

graph.put_photo(image=open('movie.gif', 'rb'), message='')

