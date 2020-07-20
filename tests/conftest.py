"""App and api initialization"""
import os
from unittest.mock import patch, MagicMock

import pytest

from sqlalchemy.exc import IntegrityError, OperationalError

from src.api import create_app


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


class DuplicatedLatte:
    def __init__(self, title, ingredients, id=1):
        pass

    def insert(self):
        raise IntegrityError("err", "err", "err")


class OperationalErrLatte:
    def __init__(self, title, ingredients, id=1):
        pass

    def insert(self):
        raise OperationalError("err", "err", "err")


dummy_latte_instance = DummyLatte(
    "test", "[{'color': 'black', 'name': 'testing', 'parts': 1}]"
)
dummy_payload = {"title": "test", "ingredients": "test", "id": 1}
valid_payload = {
    "title": "testpayload",
    "ingredients": [{"color": "black", "name": "testingpayload", "parts": 2}],
}
wrong_payload = {"bad": "payload"}
invalid_payload = {"title": "not-so-good$"}

token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik5WWkxWaTNQVmhiaDllN2Zyenk4UCJ9.eyJpc3MiOiJodHRwczovL2NvZmZlLXNob3AtcHJvamVjdC5hdXRoMC5jb20vIiwic3ViIjoiMTk4bWFpWnNZSkV0b0taeXJaMmJZdzk5dXlVbUNrZmtAY2xpZW50cyIsImF1ZCI6ImRyaW5rcyIsImlhdCI6MTU5NTE5NjQzMywiZXhwIjoxNTk1MjgyODMzLCJhenAiOiIxOThtYWlac1lKRXRvS1p5cloyYll3OTl1eVVtQ2tmayIsInNjb3BlIjoiZ2V0OmxhdHRlIHBvc3Q6bGF0dGUgcGF0Y2g6bGF0dGUgZGVsZXRlOmxhdHRlIiwiZ3R5IjoiY2xpZW50LWNyZWRlbnRpYWxzIiwicGVybWlzc2lvbnMiOlsiZ2V0OmxhdHRlIiwicG9zdDpsYXR0ZSIsInBhdGNoOmxhdHRlIiwiZGVsZXRlOmxhdHRlIl19.vRioiEITUMr8vWMQ6TwF3Hw8jU7NV26InJvHOMjmukFYQVERFtbsSmQVGslgYOLkBd4KlZRDaTcmUr8FD017G9e-a5Utp-_0RBGCTuKHXTDzamWMelEXwTiD5LyxPXmB2Ej59q3vMpzWrj975o-OWGuhWN9x4FR6GmF0Emzkx7xqq4c371ninxMXM4Ie8gbnVHxWGdNYyt0dPCc85LHkuCiIbMdaqh8vT7wLbPvlWNStBKw1SkI9r-a1b6HGjQ0e_PRFvgnHpWWCAH0OUd5MWdiM-NmwnO_sFx1uWpAyICk5zCQRzbbo--i0kLA-uuT8berkVX7Pmvpv9_wpUUZmOg"


@pytest.fixture(scope="module")
@patch("src.api.db", MagicMock())
@patch("src.api.migrate", MagicMock())
def app():
    os.environ["DATABASE_URL"] = "sqlite:///test.db"
    return create_app("testing")
