# Plugins

Plugins are implementing the real functionality of autohooks. They can be
roughly divided into formatting and linting plugins. Currently the following
plugins using the `pre-commit` hook exist:

## Formatting

* Python code formatting via [black](https://github.com/greenbone/autohooks-plugin-black)

* Python import sorting via [isort](https://github.com/greenbone/autohooks-plugin-isort)

* Python code formatting via [autopep8](https://github.com/LeoIV/autohooks-plugin-autopep8)

## Linting

* Python code linting via [pylint](https://github.com/greenbone/autohooks-plugin-pylint)

* Python code linting via [flake8](https://github.com/greenbone/autohooks-plugin-flake8)

## Other

* Running tests via [pytest](https://github.com/greenbone/autohooks-plugin-pytest/)
