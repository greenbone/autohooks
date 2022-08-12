# Installation

Three steps are necessary for installing autohooks:

1. Installing the autohooks python package into the current environment
2. Activating the [git hooks](https://git-scm.com/docs/githooks)
3. Configuring plugins to be run

## 1. Installing the autohooks Python Package into the Current Environment

```{note}

Using [poetry] is highly recommended for installing the autohooks python package.

```

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
````{hint}
It may be necessary to adjust your `PATH` to allow executing the autohooks
command without having to reference the full installation path.

```bash
export PATH=$PATH:~/.local/bin
```
````

To install autohooks globally for the current user run

```{code-block}
python3 -m pip install --user autohooks
```
`````
``````

### 2. Activating the Git Hook

To activate the git hook run

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

## 3. Configuring Plugins to Be Run

To actually run an action on git hooks, [autohooks plugins](./plugins) have to be
installed and configured, e.g., to install python linting via pylint run

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
