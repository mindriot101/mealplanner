from flask import request
from flask_restful import Resource
from marshmallow import fields, Schema, ValidationError

from ..models import Ingredient
from ..db import db


class CreateIngredientSchema(Schema):
    name = fields.Str(required=True)


class IngredientsRoute(Resource):
    def post(self):
        payload = CreateIngredientSchema().load(request.get_json())

        ingredient = Ingredient(**payload)
        db.session.add(ingredient)
        db.session.commit()

        return ingredient.to_dict(), 201
