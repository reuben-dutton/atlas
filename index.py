import planet_main as pm
import facebook, requests

page_id = '140719353303841'
at = 'EAAaKi61MD2cBAHfcBme3L1ZAdqsZBYKoIR312Dqcx30zYRgL81eDyx15JqhgkZCoUVulzTw8ARklA2ViiRgkb1awTq7ajq26R9cyD6mki5j5kkdidMsIKI8aHRA8brb307GDJE1mu5Wy0uXWSzUxhnR9F2tH3NVtiFkydEv7QZDZD'

graph = facebook.GraphAPI(access_token=at)

pm.make_img(7)

graph.put_photo(image=open('movie.gif', 'rb'), message='')

