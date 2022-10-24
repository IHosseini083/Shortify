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
    - [In development mode](#in-development-mode)
    - [In production mode](#in-production-mode)
- [Documentation and Usage](#documentation-and-usage)
- [License](#license)

## Introduction

_Shortify_ is a fast, fully async and reliable URL shortener RESTful API built with Python and [FastAPI] framework.
It uses the open source [MongoDB] database for storing shortened URLs data and implements user registration via
OAuth2 JWT authentication.

## Features

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

- Python 3.8 or higher.
- [Poetry] for dependency management.
- Up and running [MongoDB] instance (locally or remotely).

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/IHosseini083/Shortify.git
```

### 2. Install dependencies

You need to configure [Poetry] to place the virtual environment in the project directory. To do so, run the following command:

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

#### FastAPI Application

| Name                   | Description                                |               Default               |        Type        |
|------------------------|:-------------------------------------------|:-----------------------------------:|:------------------:|
| `PROJECT_NAME`         | Project name.                              |             `Shortify`              |      `string`      |
| `PROJECT_VERSION`      | Project version.                           |   Current version of the project.   |      `string`      |
| `API_V1_STR`           | API version 1 prefix.                      |                `v1`                 |      `string`      |
| `DEBUG`                | Debug mode for development.                |               `True`                |     `boolean`      |
| `BACKEND_CORS_ORIGINS` | Allowed origins for CORS.                  | An empty list to allow all origins. | `list` of `string` |
| `USE_CORRELATION_ID`   | Use correlation ID middleware for logging. |               `True`                |     `boolean`      |

#### Logging

| Name            | Description                                |        Default        |   Type   |
|-----------------|:-------------------------------------------|:---------------------:|:--------:|
| `LOG_LEVEL`     | A logging level from the [logging] module. |        `INFO`         | `string` |
| `LOG_FILE_PATH` | Path to the log file.                      | `"logs/shortify.log"` | `string` |

#### MongoDB

| Name              | Description             |           Default            |   Type   |
|-------------------|:------------------------|:----------------------------:|:--------:|
| `MONGODB_URI`     | MongoDB connection URI. | `mongodb://localhost:27017/` | `string` |
| `MONGODB_DB_NAME` | MongoDB database name.  |          `shortify`          | `string` |

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

**Note:** To set any of these environment variables, you **MUST** prefix them with `SHORTIFY_` and then set them in your
shell or in a `.env` file placed at `shortify/.env`.
For example, to set `DEBUG` environment variable, you can do the following:

```bash
export SHORTIFY_DEBUG=True
```

Also note that **ALL** environment variables are **CASE SENSITIVE**.

### 4. Run the application

#### In development mode

If you want to run the application in development mode, you can simply run the following command in the project directory,
and it will start the application with [uvicorn] server on `localhost:8000`:

```bash
python -m shortify
```

If the `DEBUG` environment variable is set to `True`, the application will be run in debug mode and will be reloaded
automatically on code changes. If you're using [VSCode], you can use the debugger to debug the application by pressing
`F5` key.

#### In production mode

But if you're going to run the application in production (e.g. On a VPS), you can use a production-ready server like [gunicorn]
along-side [uvicorn]. You can do that by running the following command in the project directory:

```bash
gunicorn -k uvicorn.workers.UvicornWorker shortify.app.main:app --bind 0.0.0.0:8000
```

That will start the application on `SERVER_IP:8000`.

## Documentation and Usage

After running the application, you can access the OpenAPI (Swagger) documentation at `/v1/docs` endpoint.

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
