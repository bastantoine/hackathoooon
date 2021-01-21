import json

from flask import (
    Blueprint,
    render_template,
    request,
)

rooms = Blueprint('rooms', __name__, template_folder='templates/rooms')

class BadGeoJSONException(Exception):
    pass

@rooms.route('/rooms/import', methods=['GET', 'POST'])
def import_geojson_files():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('import.html', error_message = 'File missing')

        file = request.files['file']

        if file.filename == '':
            return render_template('import.html', error_message = 'File missing')

        outputs = {}
        for file in request.files.getlist('file'):
            if file and file.filename.endswith('.geojson'):
                data = json.loads(file.read())
                try:
                    output = insert_features_in_db(file.filename, data)
                    outputs[file.filename] = output
                except BadGeoJSONException as exp:
                    return render_template('import.html', error_message = f"Error in the GeoJSON : {exp.message}")
        output_str = '\n'.join(f"<code>{key}</code><br/>{value}" for key, value in outputs.items())
        return render_template('import.html', success_message = f'<b>Import made successfuly!</b>\n\n{output_str}'.replace('\n', '<br/>'))

    return render_template('import.html')

def insert_features_in_db(filename, geo_json):

    from db import insert

    def get_key_or_raise(input, key):
        try:
            return input[key]
        except KeyError:
            raise BadGeoJSONException(f'Missing {key} attribute')

    features = get_key_or_raise(geo_json, 'features')

    room_types = {
        'salle': 'room',
        'couloir': 'corridor',
        'escalier': 'stair',
    }

    message = []

    building_name = filename.split('-')[0]

    for feature in features:
        properties = get_key_or_raise(feature, 'properties')
        geometry = get_key_or_raise(feature, 'geometry')
        geometry_type = get_key_or_raise(geometry, 'type')
        coordinates = get_key_or_raise(geometry, 'coordinates')
        if geometry_type == 'MultiPolygon':
            coordinates = coordinates[0][0]
            room_name = get_key_or_raise(properties, 'salle')
            if not room_name.startswith(building_name):
                room_name = f"{building_name}-{room_name}"
            room_type = room_types[get_key_or_raise(properties, 'type')]

            insert('rooms', {
                'name': room_name,
                'room_type': room_type,
                'geometry': '|'.join([f"{x};{y}" for x, y in coordinates]),
                'door_pos': ''
            })
            message.append(f"Inserting {room_type} {room_name}")

        elif geometry_type == 'Point':
            coordinates = [coordinates]
            room_name = get_key_or_raise(properties, 'room')
            if not room_name.startswith(building_name):
                room_name = f"{building_name}-{room_name}"
            _point_type = get_key_or_raise(properties, 'type')
            point_type = room_types.get(_point_type, _point_type)
            linked_to = get_key_or_raise(properties, 'linked_to').replace(' ,', '|').replace(' ', '')
            insert('points', {
                'name': room_name,
                'point_type': point_type,
                'geometry': '|'.join([f"{x};{y}" for x, y in coordinates]),
                'linked_to': linked_to,
            })
            message.append(f"Inserting point for {point_type} {room_name}")

    return "\n".join(message)
