import json
import os

from flask import Flask
from flask_cors import CORS

import db
from views.rooms import insert_features_in_db

def init_db():
    # Make sure we have the tables up-to-date in the DB
    db.init_db()

    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    main_dir = os.path.join(SITE_ROOT, "views", "resources", "GEOJSON")
    # Some GeoJSON files are not meant to be used in the graph, and thus should not be imported in
    # the DB. Don't even try, this will raise an error
    excluded_filenames = [
        'CONTOUR.geojson'
    ]
    filenames = [
        filename for filename in os.listdir(main_dir)
        if filename.endswith('.geojson')
           and filename not in excluded_filenames
    ]
    for filename in filenames:
        with open(os.path.join(main_dir, filename)) as file:
            insert_features_in_db(filename, json.loads(file.read()))
            print(f"Inserted features of {filename}")

def init_app():
    """Initialize the core application."""
    app = Flask(__name__)

    # Initialize Plugins
    CORS(app)

    init_db()

    with app.app_context():
        # Include our Routes
        from views.front import front
        from views.pass_api import pass_api
        from views.rooms import rooms
        from views.geometry import geometry
        from views.itinerary import itinerary

        # Register Blueprints
        app.register_blueprint(front)
        app.register_blueprint(pass_api)
        app.register_blueprint(rooms)
        app.register_blueprint(geometry)
        app.register_blueprint(itinerary)

        return app


if __name__ == "__main__":
    app = init_app()
    try:
        DEPLOY_SCALINGO = bool(int(os.environ.get('DEPLOY_SCALINGO', 0)))
    except ValueError:
        DEPLOY_SCALINGO = False
    if DEPLOY_SCALINGO:
        try:
            port = int(os.environ.get("PORT", 5000))
        except ValueError:
            port = 5000
        app.run(host='0.0.0.0', port=port)
    else:
        app.run()
