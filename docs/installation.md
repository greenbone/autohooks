# Installation

Four steps are necessary for installing autohooks:

1. Choosing an autohooks mode
2. Installing the autohooks python package into the current environment
3. Configuring plugins to be run
4. Activating the [git hooks](https://git-scm.com/docs/githooks)

## 1. Choosing an autohooks Mode

For its configuration, autohooks uses the *pyproject.toml* file specified in
[PEP518](https://www.python.org/dev/peps/pep-0518/).
Adding a *[tool.autohooks]* section allows to specify the desired [autohooks mode](./modes)
and to set python modules to be run as [autohooks plugins](./plugins).

The mode can be set by adding a `mode =` line to the *pyproject.toml* file.
Current possible options are `"pythonpath"`, `"pipenv"` and `"poetry"` (see
[autohooks mode](./modes)). If the mode setting is missing, the `pythonpath`
mode is used.

Example *pyproject.toml*:

```toml
[tool.autohooks]
mode = "poetry"
```

## 2. Installing the autohooks Python Package into the Current Environment

Using [poetry] is highly recommended for installing the autohooks python package.

To install autohooks as a development dependency run

```sh
poetry add --dev autohooks
```

Alternatively, autohooks can be installed directly from GitHub by running

```sh
poetry add --dev git+https://github.com/greenbone/autohooks
```

## 3. Configuring Plugins to Be Run

To actually run an action on git hooks, [autohooks plugins](./plugins) have to be
installed and configured, e.g., to install python linting via pylint run

```bash
poetry add --dev autohooks-plugin-pylint
```

Afterwards, the pylint plugin can be configured to run as a pre-commit git hook
by adding the autohooks-plugins-pylint python module name to the `pre-commit`
setting in the `[tool.autohooks]` section in the *pyproject.toml* file.

Example *pyproject.toml*:

```toml
[tool.autohooks]
mode = "poetry"
pre-commit = ["autohooks.plugins.pylint"]
```

### 4. Activating the Git Hooks

Because installing and activating git hooks automatically isn't reliable (with
using source distributions and different versions of pip) and even impossible
(with using [wheels](https://www.python.org/dev/peps/pep-0427/)) the hooks need
to be activated manually once in each installation.

To activate the git hooks run

```bash
poetry run autohooks activate
```

Calling `activate` also allows for overriding the [mode](./modes) defined in the
*pyproject.toml* settings for testing purposes.

Example:


```bash
autohooks activate --mode pipenv
```

Please keep in mind that autohooks will always issue a warning if the mode used
in the git hooks is different from the configured mode in the *pyproject.toml*
file.

The activation can always be verified by running `autohooks check`.

[pipenv]: https://pipenv.readthedocs.io/en/latest/
[poetry]: https://python-poetry.org/
