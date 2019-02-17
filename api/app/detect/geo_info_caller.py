import googlemaps
from datetime import datetime
from collections import namedtuple
import sys

GeoObj = namedtuple('geo_object', ['destinations', 'distance_texts', 'distance_values',
                                   'duration_texts', 'duration_values'])

def get_geo_info(user_coords, dest_coords, mode='walking'):
  user_coords = tuple(user_coords)
  dest_coords = list(map(tuple, dest_coords))
  gmaps = googlemaps.Client(key='AIzaSyDjm1LEi97iX2-DBTu0d2xnAQrO9ElYDE8')
  distance_result = gmaps.distance_matrix(origins=user_coords, destinations=dest_coords, mode=mode)

  dests = distance_result['destination_addresses']
  dists = [elem['distance']['text'] for elem in distance_result['rows'][0]['elements']]
  durs = [elem['duration']['text'] for elem in distance_result['rows'][0]['elements']]
  
  v_dists = [elem['distance']['value'] for elem in distance_result['rows'][0]['elements']]
  v_durs = [elem['duration']['value'] for elem in distance_result['rows'][0]['elements']]
  
  geo_info = GeoObj(dests, dists, v_dists, durs, v_durs)
  return geo_info


if __name__ == '__main__':
  user_coords = sys.argv[1]
  user_coords = tuple(map(float, user_coords.split(',')))
  dest_coords = sys.argv[2:]
#  dest_coords = dest_coords.split(' ')
  dest_coords = [tuple(map(float, dest_coord.split(','))) for dest_coord in dest_coords]
  geo_info = get_geo_info(user_coords, dest_coords, mode='walking')

