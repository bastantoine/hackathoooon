from db import query_db


def get_linked_points_of_point(point):
    if not point.startswith('B3') and not point.startswith('B1'):
        raise ValueError(f'Point name should start with either B1 or B3. Got {point}')
    return [list(row)[0] for row in query_db(f"SELECT name FROM points WHERE linked_to LIKE '%{point}%'")]

def get_geometry_of_room(room):
    if not room.startswith('B3') and not room.startswith('B1'):
        raise ValueError(f'Room name should start with either B1 or B3. Got {room}')
    return [list(row)[0] for row in query_db(f"SELECT geometry FROM rooms WHERE room_type != 'corridor' AND name = '{room}'")]

def get_geometry_of_point(point):
    if not point.startswith('B3') and not point.startswith('B1'):
        raise ValueError(f'Point name should start with either B1 or B3. Got {point}')
    return [list(row)[0] for row in query_db(f"SELECT geometry FROM points WHERE name = '{point}'")]
