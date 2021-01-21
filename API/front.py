import os
from flask import render_template, Blueprint
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

load_dotenv()

front = Blueprint('front', __name__, template_folder='templates')
@front.route('/')
def template_test():
    # We get the user information from our mocked API
    user = requests.get(os.path.join(os.environ.get('API_URL', ''), 'mock/pass/calendar?user=1'))
    user_calendar = json.loads(user.text)['calendar']

    # We search the next_course
    today = datetime.today()
    today_course = {}
    while today_course == "":
        try:
            # We try to find a course for today, if we don't find => fail
            today_course = user_calendar[today.strftime('%A')]
            break
        except:
            # We pass to the next day
            today += datetime.timedelta(days=1)
            break


    return render_template('template.html', today=today_course)