FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml app/pyproject.toml

RUN python -m pip install --upgrade pip

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY . /app

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN cat requirements.txt

RUN ls .

RUN poetry install

CMD ["python3", "app/main.py"]