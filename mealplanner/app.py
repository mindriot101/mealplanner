import os

from flask import Flask
from flask_migrate import Migrate  # type: ignore

from .db import db
from .routes import index, IngredientsView, NewIngredientsView


def create_app(testing=False):
    app = Flask(__name__)
    app.config["TESTING"] = testing
    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = os.getenv("MEALPLANNER_SECRET_KEY", "secret-key")
    db.init_app(app)
    Migrate(app, db)

    app.add_url_rule("/", "index", index)
    app.add_url_rule("/ingredients/", view_func=IngredientsView.as_view("ingredients"))
    app.add_url_rule(
        "/ingredients/new/", view_func=NewIngredientsView.as_view("new-ingredients")
    )

    return app
