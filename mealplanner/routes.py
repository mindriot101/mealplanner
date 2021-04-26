import logging
from collections import defaultdict

from flask import render_template, redirect, url_for, flash, request
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from .models import Ingredient, Recipe, Allocation
from .forms import NewIngredientForm, NewAllocationForm
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
        days = [
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
        ]
        meals = ["breakfast", "lunch", "dinner"]
        return render_template(
            "planner.html", calendar=calendar, days=days, meals=meals
        )


class NewAllocationView(MethodView):
    def __init__(self, allocation_service):
        self.allocation_service = allocation_service

    def get(self, day, meal):
        form = NewAllocationForm()
        form.recipe.choices = [(str(r.id), r.name) for r in Recipe.query.all()]
        return render_template("new-allocation.html", form=form, day=day, meal=meal)

    def post(self, day, meal):
        form = NewAllocationForm()
        form.recipe.choices = [(str(r.id), r.name) for r in Recipe.query.all()]
        if form.validate_on_submit():
            self.allocation_service.allocate(day, meal, form)
            return redirect(url_for("planner"))
        return render_template("new-allocation.html", form=form, day=day, meal=meal)


class DeleteAllocationView(MethodView):
    def __init__(self, allocation_service):
        self.allocation_service = allocation_service

    def post(self, id):
        self.allocation_service.delete(id)
        return redirect(url_for("planner"))


class ShoppingListView(MethodView):
    def get(self):
        allocations = Allocation.query.all()
        # TODO: stop the n+1
        accum = defaultdict(int)
        for a in allocations:
            r = a.recipe
            if not r:
                continue
            for m in r.memberships:
                i = m.ingredient
                accum[i.name] += m.count

        return render_template("shopping-list.html", ingredients=accum)
