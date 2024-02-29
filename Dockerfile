FROM python:3.11.8-bullseye

ENV POETRY_VERSION=1.7.1
ENV WORKDIR=/srv
ENV APPDIR=${WORKDIR}/resume_filter

WORKDIR ${WORKDIR}

COPY . .

RUN pip install --no-cache-dir poetry==${POETRY_VERSION}
RUN poetry install --only main

EXPOSE 8080
ENTRYPOINT poetry run uvicorn --app-dir ${APPDIR} --host 0.0.0.0 --port 8080 app:app
