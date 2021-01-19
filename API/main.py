import os

from flask import (
    Flask,
    send_from_directory, request,
)
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def main():
    return 'Hello there!'

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


############################
# ROUTES FOR SCALINGO ONLY #
############################

# Before the deployement, a GitHub Action job will build the React app, and copy the files in
# API/static. Then the routes below will be used to serve the files without needing any nginx
# running.

def view_maker(directory, filename):
    # Helper used to create the views used to serve the static files
    # From: https://stackoverflow.com/a/13734321/10104112
    return lambda: send_from_directory(directory=directory, filename=filename)

def setup_routes_for_scalingo():
    create_route_for_files_of_folder('./build')

def create_route_for_files_of_folder(path):
    for entry in os.listdir(path):
        filename = os.path.join(path, entry)
        if os.path.isfile(filename):
            # We have a file, let's create a route to serve it under it's own path, so a file stored
            # at build/static/css/my_file.css wwould be served under /static/css/my_file.css
            app.add_url_rule(
                '/' + filename.replace('./build/', ''),
                endpoint=filename.replace('./build/', ''),
                view_func=view_maker(path, entry)
            )
        elif os.path.isdir(filename):
            # We have a folder, let's create the routes for all it's files
            create_route_for_files_of_folder(filename)

############################

if __name__ == "__main__":
    try:
        DEPLOY_SCALINGO = bool(int(os.environ.get('DEPLOY_SCALINGO', 0)))
    except ValueError:
        DEPLOY_SCALINGO = False
    if DEPLOY_SCALINGO:
        # We are deploying on Scalingo, let's create the routes for the static files
        setup_routes_for_scalingo()
        try:
            port = int(os.environ.get("PORT", 5000))
        except ValueError:
            port = 5000
        app.run(host='0.0.0.0', port=port)
    else:
        app.run()
