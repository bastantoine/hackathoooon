import os

from flask import Flask
from flask_cors import CORS

import db

def init_app():
    """Initialize the core application."""
    app = Flask(__name__)

    # Initialize Plugins
    CORS(app)

    with app.app_context():
        # Include our Routes
        from views.front import front
        from views.pass_api import pass_api

        # Register Blueprints
        app.register_blueprint(front)
        app.register_blueprint(pass_api)

        return app

if __name__ == "__main__":
    app = init_app()
    try:
        DEPLOY_SCALINGO = bool(int(os.environ.get('DEPLOY_SCALINGO', 0)))
    except ValueError:
        DEPLOY_SCALINGO = False
    if DEPLOY_SCALINGO:
        # We are deploying on Scalingo, let's create the routes for the static files
        try:
            port = int(os.environ.get("PORT", 5000))
        except ValueError:
            port = 5000
        db.init_db()
        app.run(host='0.0.0.0', port=port)
    else:
        app.run()
