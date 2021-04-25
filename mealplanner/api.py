from flask.views import MethodView

from .models import Ingredient, Recipe, Membership


class ApiIngredientsView(MethodView):
    def get(self):
        ingredients = Ingredient.query.all()
        return {"ingredients": [i.to_dict() for i in ingredients]}


class ApiRecipesView(MethodView):
    def get(self):
        recipes = Membership.query.all()
        return {"recipes": [r.to_dict() for r in recipes]}
