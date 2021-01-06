# API

## How to install

# Linux

```bash
> python3 -m venv venv
> source venv/bin/activate
> pip install --update pip
> pip install -r requirements.txt
> export FLASK_ENV=development; python main.py
```

# Windows
In cmd, get into .\hackathoooon\API.
Then run ```python3 -m venv venv```.
Then in .\hackathoooon\API\venv\Scripts, run ```activate.bat```.
You now should have "(venv)" at the beginning of your command line (for example (venv) C:\why\not\Zoidberg).
In .\hackathoooon\API, run ```pip install -r requirements.txt```.
Then run ```python3 main.py```.
Then go to http://localhost:5000/ on your favorite web browser, and voilà.

PS : if ```python3``` doesn't work, use your PATH name to Python (```python_path_name -m venv venv```)