FROM python:3.11 as requirements-stage
WORKDIR /tmp

ENV PIP_CACHE_DIR=/var/cache/pip
ENV POETRY_CACHE_DIR=/var/cache/poetry
ENV POETRY_VIRTUALENVS_CREATE=0
ENV VIRTUAL_ENV=/usr/src/env

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev gcc

RUN --mount=type=cache,id=pip,target=$PIP_CACHE_DIR,sharing=locked \
    pip install poetry==1.8.4

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN --mount=type=cache,id=poetry,target=$POETRY_CACHE_DIR,sharing=locked \
    poetry install --no-root


FROM python:3.11

ARG WORKDIR=/application
ARG USER=app-user
ENV VIRTUAL_ENV=/usr/src/env

RUN useradd -N -u 1001 $USER
COPY --from=requirements-stage $VIRTUAL_ENV $VIRTUAL_ENV

ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONHASHSEED=random
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR $WORKDIR
COPY . $WORKDIR

# RUN python main.py download-files

USER $USER

ENTRYPOINT ["python", "main.py"]
CMD ["dev"]
