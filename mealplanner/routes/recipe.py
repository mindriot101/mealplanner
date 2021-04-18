from flask import request
from flask_restful import Resource
from marshmallow import fields, Schema, ValidationError, pre_load
from sqlalchemy.exc import IntegrityError

from ..models import Recipe
from ..db import db


class AddSchema(Schema):
    ingredient_id = fields.Str(required=True)
    count = fields.Float(required=True)


class RecipeRequestSchema(Schema):
    add = fields.Nested(AddSchema)

    @pre_load
    def validate(self, data, **kwargs):
        if len(data.keys()) == 0:
            raise ValidatationError("input data has no properties")
        return data


class RecipeRoute(Resource):
    def patch(self, id):
        recipe = Recipe.query.get(id)
        payload = RecipeRequestSchema().load(request.get_json())

        objects = []
        objects += self._handle_add(payload.get("add"))
        objects += self._handle_remove(payload.get("remove"))

        db.session.add_all(objects)
        db.session.commit()

        return {"recipe": recipe.to_dict()}

    def _handle_add(self, payload):
        return []

    def _handle_remove(self, payload):
        return []
