import os
from flask import render_template, Blueprint
from dotenv import load_dotenv
import requests
import json
from datetime import datetime, timedelta

load_dotenv()

front = Blueprint('front', __name__, template_folder='templates/front')
@front.route('/')
def template_test():
    # We get the user information from our mocked API
    user_data = requests.get(os.path.join(os.environ.get('API_URL', ''), 'mock/pass/calendar?user=1'))

    course = get_current_or_next_course(user_data)

    return render_template('template.html', course=course)

def get_current_or_next_course(user_data):
    user_calendar = json.loads(user_data.text)['calendar']

    # We search for the next course
    now = datetime.now()
    today = now.strftime('%A')

    # First try to get the courses of today
    today_courses = user_calendar.get(today, [])

    if today_courses:
        # We have one or more classes this day
        next_or_current_courses = list(filter(
            lambda course: now < datetime.strptime(course['end'], '%H:%M'),
            today_courses
        ))
        if next_or_current_courses:
            # Return the next or current course left in the day
            return next_or_current_courses[0]

    next_day = now
    while next_day < next_day + timedelta(days=7):
        next_day += timedelta(days=1)
        this_day_courses = user_calendar.get(next_day.strftime('%A'), [])
        if this_day_courses:
            return this_day_courses[0]

    return {}