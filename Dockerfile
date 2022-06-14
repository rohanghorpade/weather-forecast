# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster AS builder

WORKDIR /app

COPY . .

COPY requirements.txt .

RUN pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt

ENV FLASK_APP=run.py

ENV FLASK_RUN_PORT=8000

RUN chmod u+x ./run.sh

CMD ./run.sh