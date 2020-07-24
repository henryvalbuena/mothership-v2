"""Tests for Latte persistance model"""
from sqlalchemy.orm.exc import NoResultFound

from src.database.models import Latte

import pytest


def test_latte_creation(db_testing):
    """Test creating latte"""
    with db_testing.app_context():
        latte = Latte(title="test", ingredients='{"some": "thing"}')
        latte.insert()
    size = Latte.query.all()
    latte = Latte.query.filter(Latte.id == 1).one().long()
    title = latte["title"]
    ingredients = latte["ingredients"]

    assert len(size) > 0
    assert title == "test"
    assert "some" in ingredients


def test_latte_update(db_testing):
    """Test updating latte"""
    with db_testing.app_context():
        latte = Latte(title="old", ingredients='{"some": "thing"}')
        latte.insert()
        latte = Latte.query.filter(Latte.title == "old").one()
        latte.title = "new"
        latte.update()

    latte = Latte.query.filter(Latte.title == "new").one().long()
    title = latte["title"]
    ingredients = latte["ingredients"]

    assert title == "new"
    assert "some" in ingredients


def test_latte_delete(db_testing):
    """Test deleting latte"""
    with db_testing.app_context():
        latte = Latte(title="delete", ingredients='{"some": "thing"}')
        latte.insert()
        latte = Latte.query.filter(Latte.title == "delete").one()

        assert latte.title == "delete"

        latte.delete()

    with pytest.raises(NoResultFound) as err:
        Latte.query.filter(Latte.title == "delete").one()

    assert str(err.value) == "No row was found for one()"
