# API

## How to install

### Configure the `.env` file

First you will need to configure the projet.

To do so, make a copy of `API/.env.sample` into `API/.env` (yes, only `.env`).

In this file, you should see one line: `API_URL = http://127.0.0.1:5000`. This is the root url to use to reach the API.

If you run everything locally, leave it like this. Otherwise I assume you know what to put there.

### Linux

```bash
> python3 -m venv venv
> source venv/bin/activate
> pip install --upgrade pip
> pip install -r requirements.txt
> export FLASK_ENV=development; python main.py
```

### Windows

In cmd, get into `.\hackathoooon\API`.

Then run `python3 -m venv venv`.

Then in `.\hackathoooon\API\venv\Scripts`, run `activate.bat`.

You now should have `(venv)` at the beginning of your command line prompt (for example `(venv) C:\why\not\Zoidberg`).

In `.\hackathoooon\API`, run `pip install -r requirements.txt`.

Then run `python3 main.py`.

Then go to http://localhost:5000/ on your favorite web browser, and voilà.

PS : if `python3` doesn't work, use your PATH name to Python (`python_path_name -m venv venv`)

PS2: if it still doesn't work, switch to Linux... who devs on Windows anyway 🙄
