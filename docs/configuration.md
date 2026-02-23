# Configuration

For its configuration, autohooks uses the *pyproject.toml* file specified in
[PEP518](https://www.python.org/dev/peps/pep-0518/). This file is adjusted when
using the autohooks CLI but can also be changed manually.

Adding a `[tool.autohooks]` section allows to specify the desired [autohooks mode](./modes)
and to set python modules to be run as [autohooks plugins](./plugins).


## Mode Configuration

The mode can be set by adding a `mode =` line to the *pyproject.toml* file.
Current possible options are `"pythonpath"`, `"pipenv"`, `"poetry"` and `"uv"`(see
[autohooks mode](./modes)). If the mode setting is missing, the `pythonpath`
mode is used.

Example *pyproject.toml*:

`````{tabs}

````{group-tab} poetry
```toml
[tool.autohooks]
mode = "poetry"
```
````

````{group-tab} pipenv
```toml
[tool.autohooks]
mode = "pipenv"
```
````

````{group-tab} pip
```toml
[tool.autohooks]
mode = "pythonpath"
```
````

````{group-tab} uv
```toml
[tool.autohooks]
mode = "uv"
```
````

`````

Calling `autohooks activate` also allows for overriding the [mode](./modes)
defined in the *pyproject.toml* settings:


`````{tabs}

````{group-tab} poetry
```bash
poetry run autohooks activate --mode poetry --force
```
````

````{group-tab} pipenv
```bash
pipenv run autohooks activate --mode pipenv --force
```
````

````{group-tab} pip
```bash
autohooks activate --mode pythonpath --force
```
````

````{group-tab} uv
```bash
autohooks activate --mode uv --force
```
````

`````

Please keep in mind that autohooks will always issue a warning if the mode used
in the git hooks is different from the configured mode in the *pyproject.toml*
file.

The activation can always be verified by running `autohooks check`.

## Plugins Configuration

Afterwards, the pylint plugin can be configured to run as a pre-commit git hook
by adding the autohooks-plugins-pylint Python module name to the `pre-commit`
setting in the `[tool.autohooks]` section in the *pyproject.toml* file.

Example *pyproject.toml*:

```toml
[tool.autohooks]
mode = "poetry"
pre-commit = ["autohooks.plugins.pylint"]
```

Alternatively the `autohooks plugins` CLI can be used to manage the plugins.

`````{tabs}

````{group-tab} poetry
```bash
poetry run autohooks plugins add autohooks.plugins.pylint
```
````

````{group-tab} pipenv
```bash
pipenv run autohooks plugins add autohooks.plugins.pylint
```
````

````{group-tab} pip
```bash
autohooks plugins add autohooks.plugins.pylint
```
````

````{group-tab} uv
```bash
uv run autohooks plugins add autohooks.plugins.pylint
```
````

`````
