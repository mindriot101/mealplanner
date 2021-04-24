from mealplanner.models import Allocation, Recipe, Ingredient, Membership
from mealplanner.services.allocation_service import AllocationService
from mealplanner.db import db


def test_generate_blank_calendar(app_context):
    service = AllocationService()

    calendar = service.generate_calendar()

    days = calendar.days()
    assert len(list(days)) == 0


def test_generate_single_day(app_context):
    i = Ingredient(name="cheese")
    r = Recipe(name="cheese on toast")
    Membership(ingredient=i, recipes=r, count=2)
    allocation = Allocation(meal="lunch", day="tuesday", recipe=r)
    db.session.add(allocation)
    db.session.commit()

    service = AllocationService()

    calendar = service.generate_calendar()

    days = list(calendar.days())
    assert len(days) == 1
    assert days[0] == allocation
