FROM python:3.10-slim as base

ENV POETRY_VERSION=1.4.0
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

FROM base as poetry-base

RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

FROM base as release

COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

ENV PATH="${PATH}:${POETRY_VENV}/bin"

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry check

COPY . .

RUN poetry install --no-interaction --no-cache --without dev
