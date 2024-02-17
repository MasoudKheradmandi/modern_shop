FROM docker.arvancloud.ir/python:3.11.1-slim

ENV PYTHONDONTWRITEBYTECIDE=1
ENV PTRHONUNBUFFERED=1

WORKDIR /app
COPY ./core /app/


RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root

COPY ./scripts/entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh