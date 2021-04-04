FROM python:3.9-slim-buster as base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_NO_CACHE_DIR=off \
    POETRY_VERSION=1.1.4 \
    GUNICORN_VERSION=20.1.0

RUN pip install "poetry==$POETRY_VERSION" \
    && python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt | /venv/bin/pip install -r /dev/stdin \
    && /venv/bin/pip install "gunicorn==$GUNICORN_VERSION"

COPY . .

RUN poetry build && /venv/bin/pip install dist/*.whl

FROM base as final

COPY --from=builder /venv /venv
COPY extra/entrypoint.sh ./

CMD ["./entrypoint.sh"]
