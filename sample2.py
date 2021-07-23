import openrouteservice
from openrouteservice import convert

coords = ((49.397645, 8.689543),(49.388036, 8.690433))

client = openrouteservice.Client(key='5b3ce3597851110001cf62482a9de61896d34496b207359e19a10fac') # Specify your personal API key

# decode_polyline needs the geometry only
geometry = client.directions(coords)['routes'][0]['geometry']

decoded = convert.decode_polyline(geometry)

print(decoded)
