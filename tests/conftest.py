import pytest

from mealplanner.app import create_app
from mealplanner.db import db


@pytest.fixture
def app():
    return create_app(testing=True)


@pytest.fixture
def app_context(app):
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app_context, app):
    with app.test_client() as client:
        yield client
