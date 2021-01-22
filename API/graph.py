from dijkstra import Graph, DijkstraSPF

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

def get_itinerary(start, destination):
    # We check if the starting and ending point begins by B1 or B3
    if not start.startswith('B3') and not start.startswith('B1'):
        raise ValueError(f'Start name should start with either B1 or B3. Got {start}')
    if not destination.startswith('B3') and not destination.startswith('B1'):
        raise ValueError(f'Start name should start with either B1 or B3. Got {destination}')

    # We get all the rooms saved in the database
    rooms = query_db("SELECT name, linked_to FROM points")

    graph = Graph()
    for room in rooms:
        # We convert each room into a dictionary and we get the current room name
        room = dict(room)
        room_name = room.get("name", "")
        if room_name:
            # For each room connected to our current room
            for room_connected_and_distance in room.get("linked_to", "").split("|"):
                # On the connected room we get the name of the room and the distance
                room_connected, distance = room_connected_and_distance.split(";")
                # We add the connection in our graph
                graph.add_edge(room_name, room_connected, int(distance))

    # We generate our dijkstra and we search ou path
    dijkstra = DijkstraSPF(graph, start)
    itinerary_list = dijkstra.get_path(destination)
    return itinerary_list

def convert_rooms_itinerary_to_position_itinerary(itinerary_list):
    result_geometry = {}

    for room in itinerary_list:
        # We get the level of the current room
        level = room.split("-")[1][0]
        ## We get the geometry of the room and we convert it in float
        point = query_db(f"SELECT geometry FROM points WHERE name = '{room}'")
        x, y = dict(point[0]).get("geometry").split(';')
        x = float(x)
        y = float(y)

        # For the correct level list we add the point in our path
        current_itinerary_level = result_geometry.get(level, [])
        current_itinerary_level.append([x, y])
        result_geometry[level] = current_itinerary_level
    return result_geometry

def get_geometry_itinerary(start, destination):
    itinerary = get_itinerary(start, destination)
    return convert_rooms_itinerary_to_position_itinerary(itinerary)