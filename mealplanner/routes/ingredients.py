from flask import request
from flask_restful import Resource
from marshmallow import fields, Schema, ValidationError
from sqlalchemy.exc import IntegrityError

from ..models import Ingredient
from ..db import db


class CreateIngredientSchema(Schema):
    name = fields.Str(required=True)


class IngredientsRoute(Resource):
    def get(self):
        return {"ingredients": [i.to_dict() for i in Ingredient.query.all()]}

    def post(self):
        try:
            payload = CreateIngredientSchema().load(request.get_json())
        except ValidationError as e:
            return {"message": "input validation error", "errors": e.messages}, 400

        ingredient = Ingredient(**payload)
        db.session.add(ingredient)
        try:
            db.session.commit()
        except IntegrityError:
            return {"message": "integrity error"}, 400

        return ingredient.to_dict(), 201
