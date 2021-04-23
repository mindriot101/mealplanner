from ..models import Ingredient


class IngredientService:
    def new_from_form(self, form):
        return Ingredient(
            name=form.name.data,
            fat=form.fat.data,
            saturated_fat=form.saturated_fat.data,
            carbohydrate=form.carbohydrate.data,
            protein=form.protein.data,
        )
