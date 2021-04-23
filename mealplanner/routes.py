from flask import render_template, redirect, url_for
from flask.views import MethodView

from .models import Ingredient
from .forms import NewIngredientForm


def index():
    return render_template("index.html")


class IngredientsView(MethodView):
    def get(self):
        ingredients = Ingredient.query.all()
        return render_template("ingredients.html", ingredients=ingredients)

    def post(self):
        form = NewIngredientForm()
        if form.validate_on_submit():
            return redirect(url_for("ingredients"))
        return redirect(url_for("ingredients"))


class NewIngredientsView(MethodView):
    def get(self):
        form = NewIngredientForm()
        return render_template("new-ingredients.html", form=form)
