DROP TABLE IF EXISTS room;

CREATE TABLE room (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TINYTEXT NOT NULL,
	geometry TEXT NOT NULL,
	room_type ENUM("Salle", "Couloir", "Escalier"),
	door_pos TEXT NOT NULL
);