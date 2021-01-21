import os

from flask import (
    Flask,
    request,
)
from flask_cors import CORS
import json

from front import front

app = Flask(__name__)
CORS(app)

app.register_blueprint(front)

@app.route('/mock/pass/calendar')
def pass_controller():
    # We get the user Id from the url
    user = request.args.get('user', default = '1', type = str)

    # We open the json resources which contains all our calendars.
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "resources", "pass.json")
    with open(json_url) as json_file:
        data = json.load(json_file)

    # We fetch the calendar corresponding to the specified user
    calendar = data.get(user, {})
    return calendar

if __name__ == "__main__":
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
        app.run(host='0.0.0.0', port=port)
    else:
        app.run()
