from flask import (
    Blueprint,
    request,
    jsonify
)

from graph import get_geometry_itinerary

itinerary = Blueprint('itinerary', __name__)

@itinerary.route('/api/itinerary')
def get_itinerary():
    # We get the starting and destination room
    start = request.args.get('start')
    destination = request.args.get('destination')

    print(start, destination)

    if start is None:
        return jsonify({"error": "The starting room is undefined"})
    if destination is None:
        return jsonify({"error": "The destination room is undefined"})

    itinerary = get_geometry_itinerary(start, destination)

    geo_json = {
        "type": "FeatureCollection",
        "features": []
    }
    for key in itinerary:
        feature = {
                "type": "Feature",
                "properties": {
                "start": start,
                "end": destination,
                "floor": key
            },
            "geometry": {
                "type": "LineString",
                "coordinates": itinerary[key]
            }
        }
        geo_json["features"].append(feature)

    return jsonify(geo_json)
