FROM python:3.9-slim

WORKDIR .

COPY . .

RUN pip3 install poetry

RUN poetry config virtualenvs.create false

RUN poetry install
 
CMD ["python3", "main.py"]
