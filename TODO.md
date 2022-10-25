# TODOs and notes for the project

## Completed ✅

## Work in progress ⚒️

## Planned 📝

- [ ] Dockerize the project.

## Ideas 💡

- ### Caching

    We can use a caching system backed for example by Redis to cache the results of the
    API calls when the user is not logged in or we don't want to record any activity.
    This will reduce the number of API calls and will improve the performance of the application.
    For this, we can use something like [fastapi-cache].

- ### Rate limiting

<!-- Links -->
[fastapi-cache]: https://github.com/long2ice/fastapi-cache
