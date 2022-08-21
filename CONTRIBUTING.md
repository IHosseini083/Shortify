# Contributing

Thank you for being interested in contributing to Shortify.
There are many ways you can contribute to the project:

- Try Shortify and [report bugs/issues you find](https://github.com/IHosseini/Shortify/issues/new)
- Implement new features
- [Review Pull Requests of others](https://github.com/IHosseini/Shortify/pulls)
- Write documentation

## Reporting Bugs or Other Issues

Try to be more descriptive as you can and in case of a bug report,
provide as much information as possible, for example:

- OS platform
- Python version
- Installed dependencies and versions (`python -m pip freeze`)
- Code snippet
- Error traceback

You should always try to reduce any examples to the *simplest possible case*
that demonstrates the issue.

## Development

Prerequisites:

- [Python](https://python.org/) version 3.8 or later.
- [Poetry](https://python-poetry.org/ 'Python packaging and dependency management system') for dependency management. You should know basic stuff about handling dependencies using poetry command line interface.

To start developing Shortify, create a **fork** of the
[Shortify repository](https://github.com/IHosseini/Shortify) on GitHub.

Then clone your fork with the following command replacing `YOUR-USERNAME` with
your GitHub username:

```shell
git clone https://github.com/YOUR-USERNAME/Shortify
```

You can now install the project and its dependencies using:

```shell
cd shortify
sudo chmod +x scripts/*
scripts/install
```

## Testing and Linting

We use custom shell scripts to automate testing, linting,
and documentation building workflow.

To run the tests, use:

```shell
scripts/test
```

Any additional arguments will be passed to `pytest`. See the [pytest documentation](https://docs.pytest.org/en/latest/how-to/usage.html) for more information.

For example, to run a single test script:

```shell
scripts/test tests/test_application.py
```

To run the code auto-formatting:

```shell
scripts/lint
```

Lastly, to run code checks separately (they are also run as part of `scripts/test`), run:

```shell
scripts/check
```

<p align="center">
    <em>
    Taken from <a href="https://github.com/encode/starlette">Starlette</a>'s contribution guidelines.
    </em>
</p>
