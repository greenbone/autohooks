# Installation

Three steps are necessary for installing autohooks:

  1. Installing autohooks into the current environment
  2. Activating the [git hook](https://git-scm.com/docs/githooks)
  3. Installing and configuring the plugins to be run

For fulfilling these steps different tooling can be used. Most prominent tools are:

* [poetry]
* [pipenv]
* [pip]

```{note}
Using [poetry] is recommended for installing and maintaining autohooks.
```

## 1. Installing autohooks into the Current Environment

Fist of all autohooks needs to be installed to provide the
[CLI](https://en.wikipedia.org/wiki/Command-line_interface).

````{hint}
When using [pip] it might be necessary to adjust your `PATH` to allow executing
the autohooks CLI without having to reference the full installation path later
on.

```bash
export PATH=$PATH:~/.local/bin
```
````

``````{tabs}

`````{group-tab} poetry
To install autohooks as a development dependency run

```{code-block}
poetry add --dev autohooks
```
`````

`````{group-tab} pipenv
To install autohooks as a development dependency run
```{code-block}
pipenv install --dev autohooks
```
`````

`````{group-tab} pip

To install autohooks globally for the current user run

```{code-block}
python3 -m pip install --user autohooks
```
`````
``````

## 2. Activating the Git Hook

To actually do something when a git commit is created, it is required to
activate the git hook in every git clone. This can be done by running

`````{tabs}

````{group-tab} poetry
```bash
poetry run autohooks activate --mode poetry
```
````

````{group-tab} pipenv
```bash
pipenv run autohooks activate --mode pipenv
```
````

````{group-tab} pip
```bash
autohooks activate --mode pythonpath
```
````
`````

## 3. Installing and Configuring the Plugins to Be Run

To finally run an action on git commits, [autohooks plugins](./plugins) have to
be installed and configured. For example to install the Python linting via
pylint plugin run

`````{tabs}
````{group-tab} poetry
```bash
poetry add --dev autohooks-plugin-pylint
poetry run autohooks plugins add autohooks.plugins.pylint
```
````

````{group-tab} pipenv
```bash
pipenv install --dev autohooks-plugin-pylint
pipenv run autohooks plugins add autohooks.plugins.pylint
```
````

````{group-tab} pip
```bash
python3 -m pip install --user autohooks-plugin-pylint
autohooks plugins add autohooks.plugins.pylint
```
````
`````
[pipenv]: https://pipenv.readthedocs.io/en/latest/
[poetry]: https://python-poetry.org/
[pip]: https://pip.pypa.io/en/stable/
