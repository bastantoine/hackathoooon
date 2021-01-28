import os

from flask import (Blueprint, jsonify)

geometry = Blueprint('geometry', __name__)

@geometry.route('/geometry/floor0')
def geojson_floor0():
    from db import query_db

    query = "SELECT name, geometry, room_type FROM rooms"
    room_list = [dict(elements) for elements in query_db(query)]
    dict_rooms = {"type": "FeatureCollection", "features": []}
    for room in room_list :
        if not is_first_floor(room['name']):
            parsed_points = room_parse(room['geometry'])
            dict_room = {
                "type": "Feature",
                "properties": {
                    "type": room['room_type'],
                    "salle": room['name']
                },
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [[parsed_points]]
                }
            }
            dict_rooms['features'].append(dict_room)
    return(jsonify(dict_rooms))

@geometry.route('/geometry/floor1')
def geojson_floor1():
    from db import query_db

    query = "SELECT name, geometry, room_type FROM rooms"
    room_list = [dict(elements) for elements in query_db(query)]
    dict_rooms = {"type": "FeatureCollection", "features": []}
    for room in room_list :
        if is_first_floor(room['name']):
            parsed_points = room_parse(room['geometry'])
            dict_room = {
                "type": "Feature",
                "properties": {
                    "type": room['room_type'],
                    "salle": room['name']
                },
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [[parsed_points]]
                }
            }
            dict_rooms['features'].append(dict_room)
    return(jsonify(dict_rooms))

@geometry.route('/geometry/contour')
def geojson_contour():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "resources", "GEOJSON/CONTOUR.geojson")
    with open(json_url) as json_file:
        data = json_file.read()
    return(data)

def room_parse(room_geometry):
    points = room_geometry.split('|')
    parsed_points = []
    for point in points :
        parsed_points.append([float(point.split(';')[0]),float(point.split(';')[1])])
    return parsed_points

def is_first_floor(room_name):
    return(room_name.split('-')[1].startswith('1'))
