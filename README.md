# hackathoooon

The project requires python3 and pip.

## How to install and run the project in dev mode

1. Clone the repo:
```
> git clone https://github.com/bastantoine/hackathoooon
> cd hackathoooon
```

2. Install and run the project

First you will need to configure the projet.

To do so, make a copy of `API/.env.sample` into `API/.env` (yes, only `.env`).

In this file, you should see one line: `API_URL = http://127.0.0.1:5000`. This is the root url to use to reach the API.

If you run everything locally, leave it like this. Otherwise I assume you know what to put there.

In a terminal (make sure you are in the root directory of the repo):

```
> python3 -m venv venv
> source venv/bin/activate
> pip install --upgrade pip
> pip install -r requirements.txt
> export FLASK_ENV=development; python main.py
```

And now the project should be live at localhost:5000

If you have trouble installing the Python virtualenv (`python3 -m venv venv`) on Windows, see the troubleshooting steps [here](https://github.com/bastantoine/hackathoooon/tree/master/API#windows).

3. Initialize the database

On your browser, go on localhost:5000/rooms/import

Select in your files the geojson files containing the geographical data of the campus.

Press the "Send" button.

## Database explanation

The rooms are defined by a list of points which make a polygon, in the geojson files and in the database.
Each room has a type, which defines if they are an usual room, a corridor (so not an ending destination) or a staircase.
Doors position are also stored, and the serve as end nodes for the graph that represents the different roads between rooms.
