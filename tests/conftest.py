"""App and api initialization"""
import os
import json
from collections import namedtuple
from urllib.request import urlopen
from unittest.mock import patch, MagicMock

import pytest

from src.api import create_app
from src.database.persistence import db
from src.auth.auth import requires_auth

AUTH0_DOMAIN = "coffe-shop-project.auth0.com"


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
exp_token = (
    "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5WWkxWaTNQVmhiaDllN2Zyenk4UCJ9."
    "eyJpc3MiOiJodHRwczovL2NvZmZlLXNob3AtcHJvamVjdC5hdXRoMC5jb20vIiwic3ViIjoiMTk4bWF"
    "pWnNZSkV0b0taeXJaMmJZdzk5dXlVbUNrZmtAY2xpZW50cyIsImF1ZCI6ImRyaW5rcyIsImlhdCI6MT"
    "U5NTM4MDg5NCwiZXhwIjoxNTk1NDY3Mjk0LCJhenAiOiIxOThtYWlac1lKRXRvS1p5cloyYll3OTl1e"
    "VVtQ2tmayIsInNjb3BlIjoiZ2V0OmxhdHRlIHBvc3Q6bGF0dGUgcGF0Y2g6bGF0dGUgZGVsZXRlOmxhd"
    "HRlIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZ2V0OmxhdHRlIiwic"
    "G9zdDpsYXR0ZSIsInBhdGNoOmxhdHRlIiwiZGVsZXRlOmxhdHRlIl19.VbUE01rVIsovJdCInEhttq_x"
    "ZofpHIQMZ2XzGky2xGj_SOZneIwbAqOIUyTm_R59cdzD1UhzVoPNBCY7gpzmVj4E3H_mBuUR0sj5JAA9"
    "2oil2l-XX-8f2BM-pCFgF_KOfivjx6zTydDCt56y8DmBef0bvL2I2AlXEnJLRYsKJZkPGR1h5k9MNL2f"
    "_7QLahjcU0R6B50bpz4oT8S2tXcaUaqQ88l6fCFDt817sj97oSC8Vm3Cg5p4M8z4BHqw6gfthm6H29U4"
    "AXiwAIvl8qWpNfsk0ugG9vBFs3i23coNjKWdIQYYRAxHRqNSBgX4DpkR4QVXVv2KyJESIBkzhqSmvg"
)

jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
jwks = {"loads.return_value": json.loads(jsonurl.read())}


def get_access(permission):
    @requires_auth(permission)
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
