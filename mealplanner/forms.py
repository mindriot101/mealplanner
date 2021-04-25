from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, IntegerField, HiddenField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets.html5 import NumberInput


class NewIngredientForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    fat = FloatField("Fat", validators=[Optional()], widget=NumberInput(step=0.1))
    saturated_fat = FloatField(
        "Saturated fat", validators=[Optional()], widget=NumberInput(step=0.1)
    )
    carbohydrate = FloatField(
        "Carbohydrate", validators=[Optional()], widget=NumberInput(step=0.1)
    )
    protein = FloatField(
        "Protein", validators=[Optional()], widget=NumberInput(step=0.1)
    )


class MembershipForm(FlaskForm):
    ingredient_name = StringField("Ingredient name", validators=[DataRequired()])
    count = IntegerField("Count", validators=[DataRequired()], widget=NumberInput())


class AllocateForm(FlaskForm):
    day = HiddenField("day")
    meal = HiddenField("meal")
