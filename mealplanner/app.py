import os

from flask import Flask
from flask_migrate import Migrate  # type: ignore
from flask_restful import Api

from .db import db
from .routes.ingredients import IngredientsRoute
from .routes.recipes import RecipesRoute
from .routes.recipe import RecipeRoute


def create_app(testing=False):
    app = Flask(__name__)
    app.config["TESTING"] = testing
    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    api = Api(app)
    db.init_app(app)
    Migrate(app, db)

    api.add_resource(IngredientsRoute, "/ingredients")
    api.add_resource(RecipesRoute, "/recipes")
    api.add_resource(RecipeRoute, "/recipes/<uuid:id>")

    return app
