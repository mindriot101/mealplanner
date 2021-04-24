import os
import logging

from flask import Flask
from flask_migrate import Migrate  # type: ignore

from .db import db
from .routes import (
    index,
    IngredientsView,
    NewIngredientsView,
    IngredientView,
    RecipesView,
    RecipeView,
    NewRecipesView,
)
from .api import ApiIngredientsView
from .services.ingredient_service import IngredientService
from .services.recipe_service import RecipeService

try:
    from flask_debugtoolbar import DebugToolbarExtension
except ImportError:
    DEBUG_TOOLBAR = False
else:
    DEBUG_TOOLBAR = True


def create_app(testing=False):
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger(__name__)
    app = Flask(__name__)
    if app.debug:
        logger.setLevel(logging.DEBUG)
    logger.info("starting app")
    app.config["TESTING"] = testing
    if testing:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
    app.secret_key = os.getenv("MEALPLANNER_SECRET_KEY", "secret-key")
    db.init_app(app)
    if DEBUG_TOOLBAR:
        DebugToolbarExtension(app)
    Migrate(app, db)

    # Service objects
    ingredient_service = IngredientService()
    recipe_service = RecipeService()

    # HTML routes
    app.add_url_rule("/", "index", index)
    app.add_url_rule(
        "/recipes/",
        view_func=RecipesView.as_view("recipes", recipe_service=recipe_service),
    )
    app.add_url_rule(
        "/recipes/<uuid:id>",
        view_func=RecipeView.as_view(
            "recipe",
            recipe_service=recipe_service,
        ),
    )
    app.add_url_rule(
        "/recipes/new/",
        view_func=NewRecipesView.as_view("new-recipe"),
    )
    app.add_url_rule(
        "/ingredients/<uuid:id>",
        view_func=IngredientView.as_view(
            "ingredient",
            ingredient_service=ingredient_service,
        ),
    )
    app.add_url_rule(
        "/ingredients/",
        view_func=IngredientsView.as_view(
            "ingredients", ingredient_service=ingredient_service
        ),
    )
    app.add_url_rule(
        "/ingredients/new/",
        view_func=NewIngredientsView.as_view("new-ingredients"),
    )

    # API routes
    app.add_url_rule(
        "/api/ingredients", view_func=ApiIngredientsView.as_view("api:ingredients")
    )

    return app
