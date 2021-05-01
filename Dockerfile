FROM python:3.9

WORKDIR /app
RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
COPY mealplanner /app/mealplanner/
COPY migrations /app/migrations/
RUN poetry install --no-dev
CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:80", "--workers", "4", "mealplanner.wsgi:app"]
