FROM docker.arvancloud.ir/python:3.11.1-slim

ENV PYTHONDONTWRITEBYTECIDE=1
ENV PTRHONUNBUFFERED=1

WORKDIR /app
COPY ./core /app/

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN pip install poetry


RUN poetry install --no-dev


