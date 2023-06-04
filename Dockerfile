FROM python:3.11-slim

WORKDIR /app

RUN python -m pip install --upgrade pip

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY . /app

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

RUN poetry install

RUN ls

CMD ["python3", "-m", "/bot"]