import openrouteservice
import folium
client = openrouteservice.Client(key = '5b3ce3597851110001cf62482a9de61896d34496b207359e19a10fac')
coordinates = [[49.397645, 8.689543],[49.388036, 8.690433]]
route = client.directions(coordinates=coordinates,profile = 'driver-car',format='geojson')
map_directions = folium.Map(location=[33.77,-84.37],zoom_start=5)
folium.Geojson(route,name='route').add_to(map_directions)
folium.LayerControl().add_to(map_directions)
map_directions.save("map_directions.html")

print("abcd")