import folium
import requests
import json
import time
#!pip install goslate
#!pip install countryinfo
from geopy import distance
from countryinfo import CountryInfo
coordinates ={}
cordenadas=[]
# Function to get the coordinates of a location using OpenStreetMap Nominatim API
#segundo def
def get_location_coordinates(location):
  url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
  headers = {
    'User-Agent': 'Tryout',
    'From': 'ingrese correo'  # This is another valid field
  }
  response = requests.get(url,headers=headers).json()
  if len(response) == 0:
    lat = float(response[0]['lat'])
    lon = float(response[0]['lon'])
    print(lat, lon)
    return (lat, lon)
  else:
      lat = float(response[0]['lat'])
      lon = float(response[0]['lon'])
      return (lat, lon)

# Function to get the distance between two coordinates using OpenRouteService API
def get_distance(origin, destination):
  url = f"https://api.openrouteservice.org/v2/directions/driving-car?api_key=api key&start={origin[1]},{origin[0]}&end={destination[1]},{destination[0]}"
  headers = {'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8'}
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    data = response.json()
    distance_2 = data['features'][0]['properties']['segments'][0]['distance']
    return distance_2
  else:
    distance_2 = distance.distance(origin, destination)
    return distance_2*1000

# Main function to sort a list of places based on their proximity to a starting location
#primer def
def sort_places_by_proximity(starting_location, places_list):
  starting_coordinates = get_location_coordinates(starting_location)
  if starting_coordinates is None:
    print(f"Could not find starting location coordinates for {starting_location}")
    return None
  distances = []
  for place in places_list:
    location = get_location_coordinates(place)
    if location is None:
      print(f"Could not find location for {place}")
      continue
    distance = get_distance(starting_coordinates, location)
    if distance is None:
      print(f"Could not calculate distance for {place}")
      continue
    coordinates[place]= location
    distances.append((distance, place))
  sorted_places = [place for _, place in sorted(distances)]
  return sorted_places

def lugares (sorted_places):
  for i in sorted_places:
    x = coordinates.get(i)
    cordenadas.append(x)
  return cordenadas

#Start of the program
starting_location = input("starting place ")
places_input = input("Enter a comma-separated list of places: ")
#Separate the places
places_list = places_input.split(",")

sorted_places = sort_places_by_proximity(starting_location, places_list)
print("Sorted places:")
for place in sorted_places:
    print(place)
new_places = input("Enter a new place to add to the list: ")
places = [place.strip() for place in new_places.split(",")]
places_list.extend(places)
sorted_places = sort_places_by_proximity(starting_location, places_list)
print("Sorted places:")
for place in sorted_places:
  print(place)
#prueba
lugares(sorted_places)
cordenadas.insert(0, get_location_coordinates(starting_location))
map_center=cordenadas[0]
m=folium.Map(location=map_center, zoom_start=13)
coordinates[starting_location]= get_location_coordinates(starting_location)
for i in cordenadas:
  y = [k for k, v in coordinates.items() if v == i] [0]
  folium.Marker(i, popup=y).add_to(m)
folium.PolyLine(cordenadas,tooltip="Coast").add_to(m)
m
