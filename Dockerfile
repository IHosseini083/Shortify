FROM python:3.11.3-slim as builder

# Environment variables necessary for Poetry installation
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VERSION="1.4.2"
ENV POETRY_VIRTUALENVS_IN_PROJECT=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN set -x \
    && curl -sSL https://install.python-poetry.org | python3 -

# This will enable us to invoke Poetry as `poetry` command
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /code

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-ansi --no-interaction --without dev

FROM python:3.11.3-slim

WORKDIR /code

# Copy the .venv folder from builder image
COPY --from=builder /code/.venv ./.venv

ENV PYTHONBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

COPY ./shortify ./shortify

CMD [".venv/bin/python", "-m", "shortify"]
