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

## Requirements

## Setup

## Documentation and Usage

## License

This project is licensed under the terms of the [GPL-3.0] license.

<p align="center">&mdash; ⚡ &mdash;</p>

[FastAPI]: https://github.com/tiangolo/fastapi "Modern, high-performance, web framework for building APIs with Python."
[MongoDB]: https://www.mongodb.com/ "General purpose, document-based, distributed database."
[Poetry]: https://python-poetry.org/ "Python dependency management and packaging made easy."
[pre-commit]: https://pre-commit.com/ "A framework for managing and maintaining multi-language pre-commit hooks."
[black]: https://github.com/psf/black "The uncompromising Python code formatter."
[GPL-3.0]: https://www.gnu.org/licenses/gpl-3.0.en.html "GNU General Public License v3.0"
