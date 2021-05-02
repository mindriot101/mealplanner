FROM python:3.9 AS builder

WORKDIR /workspace
RUN apt-get update && apt-get install --no-install-recommends -y rustc cargo
RUN pip wheel --no-binary :all: 'cryptography==3.4.7'

FROM python:3.9

WORKDIR /app
COPY --from=builder /workspace/cryptography-3.4.7-cp39-cp39-linux_armv7l.whl .
RUN pip install ./cryptography-3.4.7-cp39-cp39-linux_armv7l.whl
RUN pip install poetry
COPY pyproject.toml poetry.lock /app/
COPY mealplanner /app/mealplanner/
COPY migrations /app/migrations/
RUN poetry install --no-dev
EXPOSE 80
CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:80", "mealplanner.wsgi:app"]
