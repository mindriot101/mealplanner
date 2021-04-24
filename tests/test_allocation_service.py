from mealplanner.services.allocation_service import AllocationService


def test_generate_blank_calendar(app_context):
    service = AllocationService()

    calendar = service.generate_calendar()

    days = calendar.days()
    assert next(days).day == "Monday"
