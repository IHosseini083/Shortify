# ♻️ Changelog

All notable changes to this project will be documented in this file.

The format used in this document is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

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
[0.0.8]: https://github.com/IHosseini083/Shortify/compare/v0.0.8...v0.0.8
[unreleased]: https://github.com/IHosseini083/Shortify/compare/v0.0.8...HEAD
