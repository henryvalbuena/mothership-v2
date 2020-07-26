"""App and api initialization"""
import os
import json
from collections import namedtuple
from urllib.request import urlopen
from unittest.mock import patch, MagicMock

import pytest

from src.api import create_app
from src.database.persistence import db
from src.auth.auth import requires_auth, AUTH0_DOMAIN


class DummyLatte:
    def __init__(self, title, ingredients, id=1, ex=None):
        self.id = id
        self.title = title
        self.ingredients = ingredients
        self.ex = ex

    @property
    def query(self):
        return self

    def filter(self, expression):
        if self.ex is not None:
            raise self.ex
        return self

    def one(self):
        if self.ex is not None:
            raise self.ex
        return self

    def all(self):
        if self.ex is not None:
            raise self.ex
        return [self]

    def long(self):
        return {"id": self.id, "title": self.title, "ingredients": self.ingredients}

    def insert(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass


class DummyProject:
    def __init__(self, title, meta, description, image, git_repo, demo_link, id=1):
        self.id = id
        self.title = title
        self.meta = meta
        self.description = description
        self.image = image
        self.git_repo = git_repo
        self.demo_link = demo_link

    @property
    def query(self):
        return self

    def filter(self, expression):
        return self

    def one(self):
        return self

    def all(self):
        return [self]

    @property
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "meta": self.meta,
            "description": self.description,
            "image": self.image,
            "git_repo": self.git_repo,
            "demo_link": self.demo_link,
        }

    def insert(self):
        pass

    def update(self, title, meta, description, image, git_repo, demo_link):
        self.title = title
        self.meta = meta
        self.description = description
        self.image = image
        self.git_repo = git_repo
        self.demo_link = demo_link

    def delete(self):
        pass


mocked_request = namedtuple("request", "headers")
dummy_latte_instance = DummyLatte(
    "test", "[{'color': 'black', 'name': 'testing', 'parts': 1}]"
)
dummy_project_instance = DummyProject(
    "test",
    '["meta", "testing"]',
    "some testing",
    "image.png",
    "github.com",
    "heroku.com",
)
project_payload_good = {
    "title": "test",
    "meta": ["meta", "testing"],
    "description": "some testing",
    "image": "image.png",
    "git_repo": "github.com",
    "demo_link": "heroku.com",
}
dummy_payload = {"title": "test", "ingredients": "test", "id": 1}
valid_payload = {
    "title": "testpayload",
    "ingredients": [{"color": "black", "name": "testingpayload", "parts": 2}],
}
wrong_payload = {"bad": "payload"}
invalid_payload = {"title": "not-so-good$", "ingredients": "not-so-good$-neither"}
exp_latte_token = (
    "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktCaGRneWZrZVhwd1RjbnpfRUxRNSJ9."
    "eyJpc3MiOiJodHRwczovL21vdGhlcnNoaXAtdjIudXMuYXV0aDAuY29tLyIsInN1YiI6IkxUYTV6V"
    "EwwTEljNGlsQlZtc1lNdHhyVnVvWm85NlNRQGNsaWVudHMiLCJhdWQiOiJsYXR0ZSIsImlhdCI6MT"
    "U5NTczMzQxNywiZXhwIjoxNTk1ODE5ODE3LCJhenAiOiJMVGE1elRMMExJYzRpbEJWbXNZTXR4clZ"
    "1b1pvOTZTUSIsInNjb3BlIjoiZ2V0OmxhdHRlIHBvc3Q6bGF0dGUgcGF0Y2g6bGF0dGUgZGVsZXRl"
    "OmxhdHRlIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIn0.pynwhfRghIZf_xkdmF76nu0BVFJkA"
    "988XTXlxJ7bOAjAOR7jjPQ7WJ9ZmcqG_Fz0SRbcZ0u9PG8ZFRD6o7nVcoOdos8K_9_T-qDlhrvPizM"
    "8Dw-8-hhvg3Pe9ksxw-qwnRbj1gf7wveohuLBKVjdA_KqAbIg89uGRcYu7hrueCJO7W8dJ5NWjfE1b"
    "VeEPLYNZY7MgE6Xc5uZX-U0OOuza0Ee9JUjHbSkax-ZG3tv_rLL5YyWePswS_8MTwiq3aL6vy5Noow"
    "aLOY40F7lPGl58T33Xp2XW5nFbG6tkXgQuN7E1-QlCg-xich6mS5jR95MLyfIPToxMQ6y1qcfvS-K5w"
)
exp_project_token = (
    "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktCaGRneWZrZVhwd1RjbnpfRUxRNSJ9."
    "eyJpc3MiOiJodHRwczovL21vdGhlcnNoaXAtdjIudXMuYXV0aDAuY29tLyIsInN1YiI6IjZiMG9kN"
    "1p2V2w3bUkxWHFrMXRpOVBvVmlWeTY1RlpUQGNsaWVudHMiLCJhdWQiOiJwcm9qZWN0IiwiaWF0Ij"
    "oxNTk1NzM1NjA3LCJleHAiOjE1OTU4MjIwMDcsImF6cCI6IjZiMG9kN1p2V2w3bUkxWHFrMXRpOVB"
    "vVmlWeTY1RlpUIiwic2NvcGUiOiJnZXQ6cHJvamVjdCBwb3N0OnByb2plY3QgcGF0Y2g6cHJvamVj"
    "dCBkZWxldGU6cHJvamVjdCIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zI"
    "jpbImdldDpwcm9qZWN0IiwicG9zdDpwcm9qZWN0IiwicGF0Y2g6cHJvamVjdCIsImRlbGV0ZTpwcm"
    "9qZWN0Il19.Lzf2d61NyuBxz2eoeI1xHLK5-T8u1h6Ep5RQdQCfRgSfuR5Weyy8OSdZrSYYva7l_t"
    "A9eifKylzQZkQDXqnKiT_1pGqfX3zRKyMzzKaTxPh-I73GO7AQTT0JIMPAbQXuZW4adDuHzWrZJz-"
    "uuvA-CmRkRVfLIJNV7YIvEelUPAFlCAvqqtjfHfr71YCdRosalR2gtg6TxMK0RtoJA7ahO14lAP3K"
    "8ax00U75E4Js40DLtU93Iy8BuWjBOcCdYajRixGiLTJZDdEG4FBlAuEUwQvYeO89HA9WHLSbAtxzi"
    "mG0NvbkVch9f26sWqQejLQHx5xh22V8j5DH0bQDbvsMnw"
)

jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
jwks = {"loads.return_value": json.loads(jsonurl.read())}


def get_access(permission, audiente):
    @requires_auth(permission, audiente)
    def deco(jwt):
        return jwt

    return deco


@pytest.fixture(scope="module")
@patch("src.api.db", MagicMock())
@patch("src.api.migrate", MagicMock())
def app():
    os.environ["DATABASE_URL"] = "sqlite:///test.db"
    return create_app("testing")


@pytest.fixture(scope="module")
def db_testing():
    os.environ["DATABASE_URL"] = "sqlite:///test.db"
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
