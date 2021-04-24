import logging

from flask import render_template, redirect, url_for, flash, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from .models import Ingredient, Recipe
from .forms import NewIngredientForm
from .services.recipe_service import InvalidForm
from .db import db


logger = logging.getLogger(__name__)


def index():
    return render_template("index.html")


class IngredientView(MethodView):
    def __init__(self, ingredient_service):
        self.ingredient_service = ingredient_service

    def get(self, id):
        ingredient = self.ingredient_service.get(id)
        return render_template("ingredient.html", ingredient=ingredient)

    def post(self, id):
        self.ingredient_service.delete(id)
        return redirect(url_for("ingredients"))


class IngredientsView(MethodView):
    def __init__(self, ingredient_service):
        self.ingredient_service = ingredient_service

    def get(self):
        ingredients = Ingredient.query.all()
        return render_template("ingredients.html", ingredients=ingredients)

    def post(self):
        form = NewIngredientForm()
        if form.validate_on_submit():
            logger.debug("form valid")
            ingredient = self.ingredient_service.new_from_form(form)
            db.session.add(ingredient)
            try:
                db.session.commit()
            except IntegrityError:
                flash("ingredient already exists")
            return redirect(url_for("ingredients"))
        else:
            return render_template("new-ingredients.html", form=form)


class NewIngredientsView(MethodView):
    def get(self):
        form = NewIngredientForm()
        return render_template("new-ingredients.html", form=form)


class RecipesView(MethodView):
    def __init__(self, recipe_service):
        self.recipe_service = recipe_service

    def get(self):
        recipes = Recipe.query.all()
        return render_template("recipes.html", recipes=recipes)

    def post(self):
        try:
            self.recipe_service.create_recipe_and_memberships(request.form)
        except InvalidForm as e:
            flash(str(e))
            return redirect(url_for("new-recipe"))
        except IntegrityError:
            flash("recipe already exists")
            return redirect(url_for("new-recipe"))
        return redirect(url_for("recipes"))


class RecipeView(MethodView):
    def __init__(self, recipe_service):
        self.recipe_service = recipe_service

    def get(self, id):
        recipe = self.recipe_service.get(id)
        return render_template("recipe.html", recipe=recipe)

    def post(self, id):
        self.recipe_service.delete(id)
        return redirect(url_for("recipes"))


class NewRecipesView(MethodView):
    def get(self):
        return render_template("new-recipe.html")


class PlannerView(MethodView):
    def __init__(self, allocation_service):
        self.allocation_service = allocation_service

    def get(self):
        calendar = self.allocation_service.generate_calendar()
        return render_template("planner.html", calendar=calendar)
