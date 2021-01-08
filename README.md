# hackathoooon

The project requires python3 and pip.

## How to install and run the project in dev mode

1. Clone the repo:
```
> git clone https://github.com/bastantoine/hackathoooon
> cd hackathoooon
```

2. Install and run the React app

```
> cd front-end
> npm install
> npm start
```

The React app should have been launched now, and can be accessed in your browser at localhost:3000.

3. Install and run the API

In an other terminal (make sure you are in the root directory of the repo):

```
> python3 -m venv venv
> source venv/bin/activate
> pip install --upgrade pip
> pip install -r requirements.txt
> export FLASK_ENV=development; python main.py
```

And now the API should be live too at localhost:5000

If you have trouble installing the Python virtualenv (`python3 -m venv venv`) on Windows, see the troubleshooting steps [here](https://github.com/bastantoine/hackathoooon/tree/master/API#windows).
