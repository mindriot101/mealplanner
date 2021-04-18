from flask import request
from flask_restful import Resource
from marshmallow import fields, Schema, ValidationError
from sqlalchemy.exc import IntegrityError

from ..models import Recipe
from ..db import db


class CreateRecipeSchema(Schema):
    name = fields.Str(required=True)


class RecipesRoute(Resource):
    # def get(self):
    #     return {"ingredients": [i.to_dict() for i in Ingredient.query.all()]}

    def post(self):
        try:
            payload = CreateRecipeSchema().load(request.get_json())
        except ValidationError as e:
            return {"message": "input validation error", "errors": e.messages}, 400

        recipe = Recipe(**payload)
        db.session.add(recipe)
        try:
            db.session.commit()
        except IntegrityError:
            return {"message": "integrity error"}, 400

        return recipe.to_dict(), 201
