import json

from flask import (
    Blueprint,
    render_template,
)

rooms = Blueprint('rooms', __name__, template_folder='templates/rooms')

@rooms.route('/rooms/import')
def template_test():
    return render_template('import.html')
