# ♻️ Changelog

All notable changes to this project will be documented in this file.

The format used in this document is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

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
[unreleased]: https://github.com/IHosseini083/Shortify/compare/v0.0.4...HEAD
