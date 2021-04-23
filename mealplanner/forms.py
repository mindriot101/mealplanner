from flask_wtf import FlaskForm
from wtforms import FloatField, StringField
from wtforms.validators import DataRequired


class NewIngredientForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    fat = FloatField("Fat")
    saturated_fat = FloatField("Saturated fat")
    carbohydrate = FloatField("Carbohydrate")
    protein = FloatField("Protein")
