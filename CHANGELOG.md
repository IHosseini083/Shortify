# ♻️ Changelog

All notable changes to this project will be documented in this file.

The format used in this document is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [0.1.10] (2023-05-03)

### Added

- Dockerized project.
- Add new schema `CommonHTTPError` for common HTTP error response models in OpenAPI spec.
- Use `UTC` time in `structlog.processors.TimeStamper` processor.
- Add `UVICORN_HOST` and `UVICORN_PORT` as required environment variables to be explicitly
set by user.

### Removed

- Removed flake8 and autopep8 pre-commit hooks.
- Removed `charliermarsh.ruff` extension from VSCode's recommended extensions.
- Removed `scripts/test` script.
- Removed `LOG_FILE_PATH` environment variable and support for log files

### Changed

- Removed `@app.on_event("...")` functions and use `lifespan` feature instead:

```python
from contextlib import asynccontextmanager

from fastapi import FastAPI

@asynccontextmanager
async def lifespan(application: FastAPI):  # noqa
    # On startup
    yield
    # On shutdown


app = FastAPI(
  ...,
  lifespan=lifespan,
)
```

- Set pre-commit ci autoupdate schedule to `monthly`.
- Clean up README file and add instructions for using `Docker`.
- Use enum for validation of `LOG_LEVEL` environment variable instead of pydantic validator.
- Use `structlog.stdlib.BoundLogger` bound logger as `wrapper_class` for all structlog
loggers that we get from calling `structlog.get_logger()`.

## [0.1.7] (2022-11-14)

### Added

- Add poetry pre-commit hooks.

### Changed

- Bump beanie from 1.13.1 to 1.15.2, #19.
- Bump fastapi from 0.86.0 to 0.87.0
- Use [Ruff](https://github.com/charliermarsh/ruff) for linting.

### Fixed

- Fix `scripts/install` script to install dependencies when `poetry.lock` is found.
- Use `typing.Sequence` instead of `collections.abc.Sequence`.

## [0.1.6] (2022-11-10)

### Added

- Add support for MongoDB DNS Seed List connection schema (`mongodb+srv`).
- Add new section `Project Structure, Modifications and Best Practices` to README.

### Changed

- Reformat TODO file.
- pre-commit autoupdate, #16.
- Bump beanie from 1.13.0 to 1.13.1, #15.
- Bump fastapi from 0.85.2 to 0.86.0, #18.
- Correct path to docs in `Documentation and Usage` section.
- Update dependencies.
- Add `Stack` section to README.

## [0.1.5] (2022-10-24)

### Added

- Add correlation middleware.
- Add application logs to .gitignore.
- Add `add_correlation_id` logging processor.
- Add new field `MONGODB_DB_NAME` in app settings for database name.
- Add sample .env file.

### Changed

- Refactor logging functionality.
- Set default value for `MONGODB_URI` field in app settings.
- Complete all README file sections.

## [0.1.4] (2022-10-20)

### Added

- Add base structured logging system via `structlog`.
- Add custom `RequestValidationError` exception handler.

### Changed

- Increase `editor.rulers` in VSCode settings to 88.
- Bump fastapi from 0.85.0 to 0.85.1.

## [0.1.3] (2022-10-17)

### Added

- Include `poetry.lock` file in repository.
- Add EditorConfig configurations.
- Create pagination utility function.
- Add VSCode settings for linting, formatting and debugging Python code.

### Removed

- Remove default value of None for `api_key` field in `UserInDBBase` schema.

## [0.1.2] (2022-10-11)

### Added

- Add community code of conduct.

### Changed

- Bump black from 22.6.0 to 22.10.0.
- Bump beanie from 1.11.11 to 1.12.0.
- Use new poetry dependency grouping syntax for dev dependencies in pyproject.toml.

### Fixed

- Now a `HTTPException` with status code `403` is raised when the given `api_key` query parameter is invalid.

## [0.1.1] (2022-10-02)

### Added

- Add user authentication via API key.

## [0.1.0] (2022-09-29)

### Added

- Add utility to create class-based api views.
- Add `last_visit_at` field to `ShortUrl` schema.

### Changed

- Convert all api views except for the `/auth/` endpoints to class-based views.
- Update `get_by_username()` method of `User` model to comply with the constraints of the
  `username` field on user creation (handled by the `ConstrainedUsername` field type).

### Removed

- Remove redundant `get_by_origin()` method of `ShortUrl` model.

## [0.0.9] (2022-09-27)

### Added

- Add new field to `ShortUrl` model for last visit date and time.
- Add new class method to `ShortUrl` model for updating view count and last visit.
- Implement redirection to long URL when short URL is accessed via its identifier.

### Changed

- Bump `pyupgrade` pre-commit hook to v2.38.0, #10.
- Bump `beanie` from 1.11.9 to 1.11.11.

## [0.0.8] (2022-09-18)

### Added

- Implement sorting feature to endpoints that support pagination, #9 by @IHosseini083

### Changed

- Bump fastapi version from 0.82.0 to 0.85.0

## [0.0.7] (2022-09-18)

### Added

- Create a `ConstrainedStr` subclass named `ConstrainedUsername` to validate username
on user creation. The following rules are applied:

  - The username must be between 3 and 64 characters long.
  - All characters must be alphanumeric or one of the following: (`-`, `_`, `.`).
  - All characters are converted to lowercase.
  - Whitespaces are stripped from the beginning and end of the username.

- Add a `SHORTIFY_` prefix to environment variables used by the application settings to avoid
conflicts with other applications.

### Fixed

- Silent mypy error about `user.id` being `Optional[PydanticObjectId]` instead of `PydanticObjectId`.

## [0.0.6] (2022-09-18)

### Added

- Add new sections to `README.md` file about the project's features and license.

### Changed

- Changed type annotation for `MONGODB_URL` config variable in `Settings` class to
`pydantic.MongoDsn` instead of `str`. This change enables Pydantic to validate the
MongoDB connection string.
- Bump `black` pre-commit hook from 22.6.0 to 22.8.0
- Bump `fastapi` from 0.81.0 to 0.82.0

## [0.0.5] (2022-09-05)

### Added

- Add a new schema for common pagination query parameters.
- Add new endpoints to get short URLs for current user and another user by its username.

### Fixed

- Fix parsing of `BACKEND_CORS_ORIGINS` from environment variables.

## [0.0.4] (2022-09-02)

### Added

- Add pagination to the list of users and urls in the `/users` and `/urls` endpoints.
- Support `DELETE /urls/{ident}` requests to delete a short URL.

### Changed

- Return a unique short URL every time we attempt to shorten a URL.

## [0.0.3] (2022-09-01)

### Added

- Add OpenAPI metadata for tags and license information.

### Changed

- Allow only superusers to get a short URL by identifier.
- Return a `ORJSONResponse` directly instead of a dictionary when creating access tokens.

### Removed

- Remove `status` key from responses returned from `HTTPException` handler.

## [0.0.2] (2022-08-31)

### Added

- Add endpoint to get all shortened URLs with superuser privileges.
- Add endpoint to retrieve a short URL's stats by its unique identifier.

### Changed

- Creating short URLs does not require superuser privileges anymore.

[0.0.2]: https://github.com/IHosseini083/Shortify/releases/tag/v0.0.2
[0.0.3]: https://github.com/IHosseini083/Shortify/compare/v0.0.2...v0.0.3
[0.0.4]: https://github.com/IHosseini083/Shortify/compare/v0.0.3...v0.0.4
[0.0.5]: https://github.com/IHosseini083/Shortify/compare/v0.0.4...v0.0.5
[0.0.6]: https://github.com/IHosseini083/Shortify/compare/v0.0.5...v0.0.6
[0.0.7]: https://github.com/IHosseini083/Shortify/compare/v0.0.6...v0.0.7
[0.0.8]: https://github.com/IHosseini083/Shortify/compare/v0.0.7...v0.0.8
[0.0.9]: https://github.com/IHosseini083/Shortify/compare/v0.0.8...v0.0.9
[0.1.0]: https://github.com/IHosseini083/Shortify/compare/v0.0.9...v0.1.0
[0.1.1]: https://github.com/IHosseini083/Shortify/compare/v0.1.0...v0.1.1
[0.1.2]: https://github.com/IHosseini083/Shortify/compare/v0.1.1...v0.1.2
[0.1.3]: https://github.com/IHosseini083/Shortify/compare/v0.1.2...v0.1.3
[0.1.4]: https://github.com/IHosseini083/Shortify/compare/v0.1.3...v0.1.4
[0.1.5]: https://github.com/IHosseini083/Shortify/compare/v0.1.4...v0.1.5
[0.1.6]: https://github.com/IHosseini083/Shortify/compare/v0.1.5...v0.1.6
[0.1.7]: https://github.com/IHosseini083/Shortify/compare/v0.1.6...v0.1.7
[0.1.10]: https://github.com/IHosseini083/Shortify/compare/v0.1.7...v0.1.10
[unreleased]: https://github.com/IHosseini083/Shortify/compare/v0.1.10...HEAD
