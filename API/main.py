from flask import Flask
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def main():
    return 'Hello there!'

@app.route('/covid')
def covid_controller():
    uri = "https://coronavirusapi-france.now.sh/LiveDataByDepartement?Departement=Loire-Atlantique"
    try:
        uResponse = requests.get(uri)
    except requests.ConnectionError:
        return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)

    return data["LiveDataByDepartement"][0]


if __name__ == "__main__":
    app.run()
