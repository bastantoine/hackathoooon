#retourne 3 fichier, un pour construire les salles du rdc, un pour le 1er étage, un pour les contours du bâtiment
import json

from flask import (Blueprint)

geometry = Blueprint('geometry', __name__)

@geometry.route('/geometry/floor')
def geojson_floors():
    from db import query_db
    query = "SELECT name, geometry, room_type FROM rooms"
    magic_list = query_db(query)
    print("BENDER BENDER BENDER")
    print(magic_list)

if __name__ == "__main__":
    geojson_floors()