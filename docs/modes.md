# Modes

Currently three modes for using autohooks are supported:

* `pythonpath`
* `poetry`
* `pipenv`

These modes handle how autohooks, the plugins and their dependencies are loaded
during git hook execution.

If no mode is specified in the [`pyproject.toml` config file](./configuration)
and no mode is set during [activation](./installation.md), autohooks
will use the [pythonpath mode](#pythonpath-mode) by default.

```{note}
`poetry` or `pipenv` modes leverage the `/usr/bin/env` command using the
`--split-string` (`-S`) option. If `autohooks` detects that it is
running on an OS where `/usr/bin/env` is yet to support _split_strings_
(notably ubuntu < 19.x), `autohooks` will automatically change to an
internally chosen `poetry_multiline`/`pipenv_mutliline` mode. The
'multiline' modes *should not* be user-configured options; setting your
project to use `poetry` or `pipenv`allows team members the greatest
latitude to use an OS of their choice yet leverage the sane
`/usr/bin/env --split-string` if possible. Though `poetry_multiline`
would generally work for all, it is very confusing sorcery.
([Multiline shebang explained](https://rosettacode.org/wiki/Multiline_shebang#Python))
```

## Pythonpath Mode

In the `pythonpath` mode, the user has to install autohooks, the desired
[plugins](./plugins) and their dependencies into the [PYTHONPATH](https://docs.python.org/3/library/sys.html#sys.path)
manually.

This can be achieved by running something like `python3 -m pip install --user autohooks autohooks-plugin-xyz ...`
to put them into the installation directory of the [current user](https://docs.python.org/3/library/site.html#site.USER_SITE)
or with `sudo python3 -m pip install autohooks autohooks-plugin-xyz ...` for a system wide installation.

Alternatively, a [virtual environment](https://packaging.python.org/tutorials/installing-packages/#creating-and-using-virtual-environments)
could be used to separate the installation from the global and user wide
Python packages in conjunction with the `pythonpath` mode. A downside of using
this mode with a virtual environment is that [activating the environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#activating-a-virtual-environment)
has to be done manually.

To benefit from the advantages of a virtual environment a much better choice is
to use [poetry] or [pipenv] for managing the virtual environment automatically.

## Poetry Mode

With the `poetry` mode it is possible to run autohooks in a
dedicated environment controlled by [poetry]. By using the `poetry` mode the
virtual environment will be activated automatically in the background when
executing the autohooks based git commit hook. All dependencies are managed
by poetry using the `pyproject.toml` and `poetry.lock` files.

```{hint}
Using the `poetry` mode is highly recommended.
```

## Pipenv Mode

Alternatively to [poetry] [pipenv] can be used to manage dependencies.
In the `pipenv` mode [pipenv] is used to run autohooks in a dedicated virtual
environment. Pipenv uses a lock file to install exact versions. Therefore the
installation is deterministic and reliable between different developer setups.
In contrast to the `pythonpath` mode the activation of the virtual environment
provided by [pipenv] is done automatically in the background.

[pipenv]: https://pipenv.readthedocs.io/en/latest/
[poetry]: https://python-poetry.org/
