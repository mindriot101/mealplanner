from flask.views import MethodView

from .models import Ingredient


class ApiIngredientsView(MethodView):
    def get(self):
        ingredients = Ingredient.query.all()
        return {"ingredients": [i.to_dict() for i in ingredients]}
