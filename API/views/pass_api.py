import json
import os

from flask import (
    Blueprint,
    request,
)

pass_api = Blueprint('pass_api', __name__)

@pass_api.route('/mock/pass/calendar')
def pass_controller():
    # We get the user Id from the url
    user = request.args.get('user', default = '1', type = str)

    # We open the json resources which contains all our calendars.
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "resources", "pass.json")
    print(SITE_ROOT, json_url)
    with open(json_url) as json_file:
        data = json.load(json_file)

    # We fetch the calendar corresponding to the specified user
    calendar = data.get(user, {})
    return calendar
