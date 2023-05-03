<div align="center">
<h1><a href="https://github.com/IHosseini/Shortify"><b>Shortify</b></a></h1>
<a href="https://www.python.org">
    <img src="https://img.shields.io/badge/Python-3.8+-3776AB.svg?style=flat&logo=python&logoColor=white" alt="Python">
</a>
<a href="https://github.com/psf/black">
    <img src="https://img.shields.io/static/v1?label=code%20style&message=black&color=black&style=flat" alt="Code Style: black">
</a>
<a href="https://github.com/pre-commit/pre-commit">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat" alt="pre-commit">
</a>
</div>

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
    - [1. Clone the repository](#1-clone-the-repository)
    - [2. Install dependencies](#2-install-dependencies)
    - [3. Configure environment variables](#3-configure-environment-variables)
        - [FastAPI Application](#fastapi-application)
        - [Logging](#logging)
        - [MongoDB](#mongodb)
        - [Superuser](#superuser)
        - [Authentication](#authentication)
        - [Short URLs](#short-urls)
    - [4. Run the application](#4-run-the-application)
        - [Using Docker (Recommended)](#using-docker-recommended)
        - [Manually](#manually)
- [Documentation and Usage](#documentation-and-usage)
- [Project Structure, Modifications and Best Practices](#project-structure-modifications-and-best-practices)
    - [Creating new API routes](#creating-new-api-routes)
    - [FastAPI Best Practices](#fastapi-best-practices)
- [Stack](#stack)
- [License](#license)

## Introduction

_Shortify_ is a fast, fully async and reliable URL shortener RESTful API built with Python and [FastAPI] framework.
It uses the open source [MongoDB] database for storing shortened URLs data and implements user registration via
OAuth2 JWT authentication.

## Features

- Dockerized and ready to be deployed.
- Fully async and non-blocking.
- Uses [FastAPI] framework for API development:
- Uses [MongoDB] as data store for users and shortened URLs.
- Extensible architecture for adding new API endpoints and services.
- Descriptive and well-documented code.
- OAuth2 (with hashed passwords and JWT tokens) based user authentication.
- Uses [Poetry] for dependency management.
- Automated code formatting and linting with [pre-commit] and [black].
- [CORS (Cross Origin Resource Sharing)](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) support.
- Pagination support for listing shortened URLs and users.
- Structured logging with [structlog].
- Correlation ID middleware for logging and tracing requests across services.
- Class-based API endpoints for better code organization and reducing duplication.
- Fully type annotated code for better IDE support and code quality.

## Requirements

Manual installation:

- Python 3.8 or higher.
- [Poetry] for dependency management.
- Up and running [MongoDB] instance (locally or remotely).

Using Docker:

- [Docker]
- [Docker-Compose]

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/IHosseini083/Shortify.git
```

### 2. Install dependencies

⚠️ **Skip this step if you want to use docker for running the application.**

You need to configure [Poetry] to place the virtual environment in the project directory. To do so, run the following
command:

```bash
poetry config --local virtualenvs.in-project true
```

Then, install dependencies:

```bash
poetry install
```

If you're on Linux, you can just skip all the above steps and run the `scripts/install` script:

```bash
chmod +x scripts/install  # make the script executable
./scripts/install
```

### 3. Configure environment variables

You can see the table of all environment variables below. Those marked with `*` are required and **MUST** be set before
running the application. Rest of them are optional and have default values.

**Note:** To set any of these environment variables below, you **MUST** prefix them with `SHORTIFY_` and then set them
in your shell or in a `.env` file placed at the root directory (e.g. you can copy `.env.example` to `.env`).
For example, to set `DEBUG` environment variable, you can do the following:

```bash
export SHORTIFY_DEBUG=True
```

Also note that **ALL** environment variables are **CASE SENSITIVE**.

#### FastAPI Application

| Name                 | Description                                |               Default               |        Type        |
|----------------------|:-------------------------------------------|:-----------------------------------:|:------------------:|
| `PROJECT_NAME`       | Project name.                              |             `Shortify`              |      `string`      |
| `PROJECT_VERSION`    | Project version.                           |   Current version of the project.   |      `string`      |
| `API_V1_STR`         | API version 1 prefix.                      |                `v1`                 |      `string`      |
| `DEBUG`              | Debug mode for development.                |               `True`                |     `boolean`      |
| `CORS_ORIGINS`       | Allowed origins for CORS.                  | An empty list to allow all origins. | `list` of `string` |
| `USE_CORRELATION_ID` | Use correlation ID middleware for logging. |               `True`                |     `boolean`      |
| `UVICORN_HOST`*      | Host address for uvicorn server.           |                 `-`                 |      `string`      |
| `UVICORN_PORT`*      | Port number for uvicorn server.            |                 `-`                 |     `integer`      |

#### Logging

| Name            | Description                                |        Default        |   Type   |
|-----------------|:-------------------------------------------|:---------------------:|:--------:|
| `LOG_LEVEL`     | A logging level from the [logging] module. |        `INFO`         | `string` |

#### MongoDB

| Name              | Description             |        Default        |   Type   |
|-------------------|:------------------------|:---------------------:|:--------:|
| `MONGODB_URI`     | MongoDB connection URI. | `mongodb://db:27017/` | `string` |
| `MONGODB_DB_NAME` | MongoDB database name.  |      `shortify`       | `string` |

#### Superuser

| Name                        | Description                      | Default |   Type   |
|-----------------------------|:---------------------------------|:-------:|:--------:|
| `FIRST_SUPERUSER`*          | Username of the first superuser. |   `-`   | `string` |
| `FIRST_SUPERUSER_EMAIL`*    | Email of the first superuser.    |   `-`   | `string` |
| `FIRST_SUPERUSER_PASSWORD`* | Password of the first superuser. |   `-`   | `string` |

#### Authentication

| Name                          | Description                              |                       Default                       |   Type    |
|-------------------------------|:-----------------------------------------|:---------------------------------------------------:|:---------:|
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token expiration time in minutes. |                  `1440` (24 hours)                  | `integer` |
| `SECRET_KEY`                  | Secret key for signing JWT tokens.       | 43 random characters generated by [secrets] module. | `string`  |

#### Short URLs

| Name               | Description                     | Default |   Type    |
|--------------------|:--------------------------------|:-------:|:---------:|
| `URL_IDENT_LENGTH` | Length of the shortened URL ID. |   `7`   | `integer` |

### 4. Run the application

After setting all the required and optional environment variables in `.env.example` file, copy it to `.env` file so that
it's usable both by Docker and _Shortify_ app.

Run the following commands to start up the services:

#### Using Docker (Recommended)

This will start two containers, one for _Shortify_ and another one for [MongoDB].

```bash
docker compose up -d
```

#### Manually

An up & running [MongoDB] instance is required and `SHORTIFY_MONGODB_URI` environment variable must
be handled accordingly because its default value is only compatible with Docker installation of the app.

```bash
python -m shortify
```

If the `SHORTIFY_DEBUG` environment variable is set to `True`, the application will be run in debug mode and will be
reloaded automatically on code changes.

Now your application is available at `http://{SHORTIFY_UVICORN_HOST}:{SHORTIFY_UVICORN_HOST}/`.

## Documentation and Usage

After running the application, you can access the OpenAPI (Swagger) documentation at `/api/v1/docs` endpoint.

## Project Structure, Modifications and Best Practices

Structure of `shortify` folder containing main files and folders of the application is consistent and straightforward
and just by looking at module names it gives you an idea of what's inside it!

```
./shortify
│    __init__.py
│    __main__.py        # Runs the development server
├─── app                # Primary app folder
│   │    main.py        # Contains FastAPI application and its settings
│   │    __init__.py    # Contains project version variable
│   ├─── api            # All API views/routes are here
│   ├─── core           # Core configs and utils for the application
│   ├─── db             # Database initialization and session (if needded)
│   ├─── middlewares    # ASGI middlewares for FastAPI application
│   ├─── models         # Database models
│   ├─── schemas        # Pydantic schemas
│   ├─── static         # Static files served at /static endpoint
│   ├─── utils          # Utilites used by the API
```

### Creating new API routes

To create new API routes and add them to your main application, you need to create new `fastapi.APIRouter` instances or
use the existing ones depending on the endpoint you need to implement. All API routers for API version one (v1) are
located at `shortify/app/api/v1/endpoints` folder and then grouped together in `shortify/app/api/v1/__init__.py` file by
including
them in a separate `fastapi.APIRouter` instance that will be added to main app:

```python
# shortify/app/api/v1/__init__.py
from fastapi import APIRouter

from shortify.app.api.v1.endpoints import auth, urls, users
from shortify.app.core.config import settings

router = APIRouter(prefix=f"/{settings.API_V1_STR}")
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(urls.router, prefix="/urls", tags=["URLs"])
```

Now let's say you want to add a new router for statistics about short URLs and then add it to your main app, this is how
you're going to do it:

1. Create new module named `stats.py` in `shortify/app/api/v1/endpoints` package.
2. Create an `fastapi.APIRouter` instance in `stats.py` module.

```python
# shortify/app/api/v1/endpoints/stats.py
from fastapi import APIRouter

router = APIRouter()
```

3. E.g. Create an API route to get most visited short URLs in descending order

```python
# shortify/app/api/v1/endpoints/stats.py
from fastapi import APIRouter
from typing import List
from shortify.app.models import ShortUrl

router = APIRouter()


@router.get("/most-visited")
async def get_most_visited_urls(skip: int = 0, limit: int = 10) -> List[ShortUrl]:
    # Sort URLs in descending order based on their views
    return await ShortUrl.find(skip=skip, limit=limit).sort(-ShortUrl.views).to_list()
```

You could also implement the route using class-based views decorator but since we don't have any dependencies or code
duplications, this approach was simply enough for our use-case.

4. Finally, add the newly created router to the main router for version one

```python
# shortify/app/api/v1/__init__.py
from fastapi import APIRouter

from shortify.app.api.v1.endpoints import stats
from shortify.app.core.config import settings

router = APIRouter(prefix=f"/{settings.API_V1_STR}")
# Other routers omitted for brevity
router.include_router(stats.router, prefix="/stats", tags=["Statistics"])
```

5. That's it! now you can see the created endpoint in your API docs.

### FastAPI Best Practices

You want to extend the application with the best practices available? check out the below repositories:

- [fastapi-best-practices]
- [full-stack-fastapi-postgresql] (by FastAPI creator, Sebastián Ramírez)

## Stack

Frameworks and technologies used in _Shortify_

- [FastAPI] (Web framework)
- [structlog] (Logging)
- [MongoDB] (Database)
- [beanie] (ODM)
- [poetry] (Dependency Management)
- [pre-commit] (Git hook)
- [ruff] (Linter)
- [black] & [isort] (Formatter)
- [mypy] (Type checker)

## License

This project is licensed under the terms of the [GPL-3.0] license.

<p align="center">&mdash; ⚡ &mdash;</p>

[FastAPI]: https://github.com/tiangolo/fastapi "Modern, high-performance, web framework for building APIs with Python."
[MongoDB]: https://www.mongodb.com/ "General purpose, document-based, distributed database."
[Poetry]: https://python-poetry.org/ "Python dependency management and packaging made easy."
[pre-commit]: https://pre-commit.com/ "A framework for managing and maintaining multi-language pre-commit hooks."
[black]: https://github.com/psf/black "The uncompromising Python code formatter."
[GPL-3.0]: https://www.gnu.org/licenses/gpl-3.0.en.html "GNU General Public License v3.0"
[structlog]: https://www.structlog.org/en/stable/ "Structured logging for Python."
[logging]: https://docs.python.org/3/library/logging.html "Logging facility for Python."
[secrets]: https://docs.python.org/3/library/secrets.html "Generate secure random numbers for managing secrets."
[uvicorn]: https://www.uvicorn.org/ "The lightning-fast ASGI server."
[gunicorn]: https://gunicorn.org/ "A Python WSGI HTTP Server for UNIX."
[VSCode]: https://code.visualstudio.com/ "Redefined and optimized code editor for building and debugging modern web and cloud applications."
[fastapi-best-practices]: https://github.com/zhanymkanov/fastapi-best-practices "Opinionated list of best practices and conventions."
[full-stack-fastapi-postgresql]: https://github.com/tiangolo/full-stack-fastapi-postgresql "Full stack, modern web application generator. Using FastAPI, PostgreSQL as database, Docker, automatic HTTPS and more."
[pydantic]: https://github.com/pydantic/pydantic "Data parsing and validation using Python type hints."
[beanie]: <https://github.com/roman-right/beanie> "Python ODM for MongoDB."
[isort]: <https://github.com/PyCQA/isort> "A Python utility / library to sort imports."
[mypy]: https://github.com/python/mypy "Optional static typing for Python."
[ruff]: https://github.com/charliermarsh/ruff "An extremely fast Python linter, written in Rust."
[Docker]: https://github.com/docker/
[Docker-Compose]: https://github.com/docker/compose "Define and run multi-container applications with Docker."
