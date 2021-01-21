import sqlite3

DATABASE = "./database.sqlite"

# From https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def insert(table, params):
    columns, values = [], []
    for key, value in params.items():
        columns.append(key)
        values.append(f"'{value}'")
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(values)})"
    db = get_db()
    db.cursor().execute(query)
    db.commit()
    db.close()

def init_db():
    db = get_db()
    with open('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()
