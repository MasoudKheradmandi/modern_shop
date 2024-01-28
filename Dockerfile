FROM docker.arvancloud.ir/python:3.11.1-slim

ENV PYTHONDONTWRITEBYTECIDE=1
ENV PTRHONUNBUFFERED=1


RUN pip install poetry==1.4.2


WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-dev


COPY ./core /app/