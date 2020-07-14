import os

from src.api import create_app

app = create_app(os.environ["FLASK_CONFIG"])
