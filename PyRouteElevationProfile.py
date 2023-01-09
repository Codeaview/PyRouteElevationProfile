import openrouteservice
from pprint import pprint
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import argparse


argParser = argparse.ArgumentParser()
argParser.add_argument("-slat", "--startlatitude", help="Startpoint latitude of point")
argParser.add_argument("-slng", "--startlongitude", help="Startpoint longitute of point")
argParser.add_argument("-elat", "--endlatitude", help="Endpoint latitude of point")
argParser.add_argument("-elng", "--endlongitude", help="Endpoint longitute of point")
argParser.add_argument("-k", "--secretkey", help="Secret API key from Openrouteservice")
argParser.add_argument("-p", "--plot", help="Should the result be plotted (0 - no, 1 - yes")

args = argParser.parse_args()
shouldPlot = args.plot
secretKey = args.secretkey

# routeLubienMyslenice = ((19.980357561386278, 49.72037999582303),(19.93733261706287, 49.820465778926604))
startendpoints = ((args.startlongitude, args.startlatitude,),(args.endlongitude, args.endlatitude))

client = openrouteservice.Client(key=secretKey) # Specify your personal API key
route_request = {'coordinates': startendpoints,
                     'format_out': 'geojson',
                     'profile': 'driving-car',
                     'preference': 'shortest',
                     'instructions': False,
                     "elevation": True
                     }
route = client.directions(**route_request)

# pprint(route)
coordinates = route["features"][0]["geometry"]["coordinates"]
# pprint(coordinates)
print("Number of received coordinates: " + str(len(coordinates)))
totalLength = route["features"][0]["properties"]["summary"]["distance"]
print("Length of the route: " + str(totalLength) + " m")
metersPerCoordinate = totalLength / len(coordinates)
print("Coordinates are placed every " + str(metersPerCoordinate) + " m")

# print("Calculating distances:")
distance = 0
elevations = []
# Add first elevation
elevations.append({'x': 0, 'elevation': coordinates[0][2]} )
for index in range(1,len(coordinates)):
    previousPoint = coordinates[index - 1]
    previousPointLatLng = (previousPoint[1], previousPoint[0])
    currentPoint = coordinates[index]
    currentPointLatLng = (currentPoint[1], currentPoint[0])
    deltaDistance = geodesic(previousPointLatLng, currentPointLatLng).meters
    distance += deltaDistance
    elevations.append({'x': distance, 'elevation': coordinates[index][2]})
# pprint(elevations)
print("X values")
for i in range(0,len(elevations)):
   print(round(elevations[i]["x"], 0), end=" ")
print()
print("Corresponding elevation values")
for i in range(0,len(elevations)):
   print(round(elevations[i]["elevation"]), end=" ")
print()

# Return x value
def getX(o):
    return o['x']

# Return elevation value
def getElevation(o):
    return o['elevation']

# show the plot
if shouldPlot == '1':
   x = list(map(getX, elevations))
   y = list(map(getElevation, elevations))

   plt.plot(x,y) 

   plt.xlabel('x [m]') 
   plt.ylabel('elevation [m]') 
   plt.title('Road profile') 
      
   plt.show() 