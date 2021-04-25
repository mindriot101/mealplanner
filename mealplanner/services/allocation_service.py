from ..models import Allocation
from ..forms import AllocateForm


class AllocationService:
    def generate_calendar(self):
        allocations = Allocation.query.all()
        return Calendar(allocations)


class Calendar:
    def __init__(self, allocations):
        self.allocations = allocations

    def days(self):
        return iter(self.allocations)

    def has(self, day, meal):
        selected = [a for a in self.allocations if a.day == day and a.meal == meal]
        if selected:
            return True

    def build_form(self, day, meal):
        return AllocateForm(day=day, meal=meal)

    def fetch(self, day, meal):
        selected = [a for a in self.allocations if a.day == day and a.meal == meal]
        if selected:
            return selected[0]


class Day:
    def __init__(self, day):
        self.day = day
