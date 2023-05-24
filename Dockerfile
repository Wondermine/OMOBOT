FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml /app/pyproject.toml

RUN python -m pip install --upgrade pip

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN  poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN ls .

RUN cat requirements.txt

RUN poetry install

COPY . /app

CMD ["python3", "/app/main.py"]