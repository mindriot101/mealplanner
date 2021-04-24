class AllocationService:
    def generate_calendar(self):
        return Calendar()


class Calendar:
    def days(self):
        return iter([Day("Monday")])


class Day:
    def __init__(self, day):
        self.day = day
