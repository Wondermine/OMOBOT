FROM python:3.9-slim

WORKDIR /

COPY pyproject.toml app/pyproject.toml

RUN python -m pip install --upgrade pip

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

COPY . /app

CMD ["python3", "/app/main.py"]