import numpy as np
import pandas as pd
import folium
import openrouteservice as ors
import csv

ORSkey = '5b3ce3597851110001cf624884124dee95314ba39780a7e4ee4cbc6f'

locations = pd.read_csv("WoolworthsLocations.csv")

coords = locations[['Long','Lat']]
coords = coords.to_numpy().tolist()


m = folium.Map(location = list(reversed(coords[2])), zoom_start=10.25)


for i in range (0,len(coords)):
    if locations.Type[i] == 'Countdown':
        iconCol = 'green'

    elif locations.Type[i] == 'FreshChoice':
        iconCol = 'blue'

    elif locations.Type[i] == 'SuperValue':
        iconCol = 'red'

    elif locations.Type[i] == 'Countdown Metro':
        iconCol = 'orange'

    elif locations.Type[i] == 'Distribution Centre':
        iconCol = 'black'

    folium.Marker(list(reversed(coords[i])), popup= locations.Store[i], icon = folium.Icon(color=iconCol)).add_to(m)

#m.save("routes.html")
client = ors.Client(key = ORSkey)


route = client.directions(coordinates = [coords[55], coords[65], coords[4], coords[18], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[26], coords[31], coords[45], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[41], coords[37], coords[64], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[1], coords[53], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[58], coords[54], coords[51], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[41], coords[37], coords[64], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[22], coords[0], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[49], coords[48], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[8], coords[35], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[5], coords[62], coords[38], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[42], coords[36], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[19], coords[16], coords[56], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[34], coords[52], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[59], coords[3], coords[11], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[15], coords[13], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[39], coords[10], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[32], coords[29], coords[43], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[24], coords[25], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[17], coords[60], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[47], coords[14], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[20], coords[28], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[6], coords[44], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[61], coords[40], coords[30], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[33], coords[7], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[12], coords[63], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[57], coords[2], coords[27], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)

route = client.directions(coordinates = [coords[55], coords[46], coords[21], coords[55]], profile = 'driving-hgv', format = 'geojson', validate = False)
folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][0]['geometry']['coordinates']]).add_to(m)


#m = folium.Map(locations = [-36.95770671222872, 174.81407132219618], zoom_start=15)

#folium.PolyLine(locations = [list(reversed(coord)) for coord in route ['features'][1]['geometry']['coordinates']]).add_to(m)

m.save("RoutesForWeekdays.html")


