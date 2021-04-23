import logging

from flask import render_template, redirect, url_for, flash
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from .models import Ingredient
from .forms import NewIngredientForm
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
