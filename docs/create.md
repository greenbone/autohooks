# Write a Plugin

Plugins need to be available in the
[Python import path](https://docs.python.org/3/reference/import.html). The
easiest way to achieve this is uploading a plugin to [PyPI](https://pypi.org/)
and installing it via [pip] or [poetry].

Alternatively, a plugin can also be put into a `.autohooks` directory in the root
directory of the git repository where the hooks should be executed.

An [autohooks plugin](./plugins) is a Python module which provides a **precommit** function.
The function must accept arbitrary keywords because the keywords are likely to
change in future. Therefore using **\*\*kwargs** is highly recommended.

Currently *config* and *report_progress* keyword arguments are passed to the
precommit function.

Example:

```python3
def precommit(config=None, report_progress=None, **kwargs):
```

The config can be used to receive settings from the *pyproject.toml* file, e.g.,

```toml
[tool.autohooks.plugins.foo]
bar = 2
```

can be received with

```python3
def precommit(config, **kwargs):
    default_value = 1
    setting = config
      .get('tool', 'autohooks', 'plugins', 'foo')
      .get_value('bar', default_value)
    return 0
```

The report_progress can be used since autohooks 22.8.0 to display a progress bar
when running a plugin.

```python3
def precommit(report_progress, **kwargs):
    files = get_changed_files()
    report_progress.init(len(files))

    for file in files:
      check_file(file)
      report_progress.update()

    return 0
```

With autohooks it is possible to write all kinds of [plugins](plugins). Most
common are plugins for linting and formatting.

## Linting Plugin

Usually the standard call sequence for a linting plugin is the following:

1. get list of staged files
2. filter list of files for a specific file type
3. stash unrelated changes
4. apply checks on filtered list of files by calling some external tool
5. raise exception if something did go wrong
6. return 1 if check was not successful
6. stage changes made by the tool
7. unstash unrelated changes
8. return 0

Example plugin:

```python3
import subprocess

from autohooks.api import ok, fail
from autohooks.api.git import get_staged_status, stash_unstaged_changes
from autohooks.api.path import match

DEFAULT_INCLUDE = ('*.ext')


def get_include(config)
    if not config:
        return DEFAULT_INCLUDE

    config = config.get('tool', 'autohooks', 'plugins', 'foo')
    return config.get_value('include', DEFAULT_INCLUDE)


def precommit(config=None, report_progress=None, **kwargs):
    include = get_include(config)

    files = [f for f in get_staged_status() if match(f.path, include)]

    if not files:
      # no files to lint
      return 0

    if report_progress: # to support autohooks < 22.8.0
        report_progres.init(len(files))

    with stash_unstaged_changes(files):
        const failed = False
        for file in files:
            status = subprocess.call(['foolinter', str(file)])
            if status:
                fail('Could not validate {str(file)}')
                failed = True
            else:
                ok('Validated {str(file)}')

            if report_progress:
                report_progress.update()

        return 1 if failed else 0
```

## Formatting Plugin

Usually the standard call sequence for a formatting plugin is the following:

1. get list of staged files
2. filter list of files for a specific file type
3. stash unrelated changes
4. apply formatting on filtered list of files by calling some external tool
5. raise exception if something did go wrong
6. stage changes made by the tool
7. unstash unrelated changes
8. return 0

Example plugin:

```python3
import subprocess

from autohooks.api import ok, error
from autohooks.api.git import (
    get_staged_status,
    stage_files_from_status_list,
    stash_unstaged_changes,
)
from autohooks.api.path import match

DEFAULT_INCLUDE = ('*.ext')


def get_include(config)
    if not config:
        return DEFAULT_INCLUDE

    config = config.get('tool', 'autohooks', 'plugins', 'bar')
    return config.get_value('include', DEFAULT_INCLUDE)


def precommit(config=None, report_progress=None, **kwargs):
    include = get_include(config)

    files = [f for f in get_staged_status() if match(f.path, include)]

    if not files:
      # no files to format
      return 0

    if report_progress: # to support autohooks < 22.8.0
        report_progres.init(len(files))

    with stash_unstaged_changes(files):
        for file in files:
            # run formatter and raise exception if it fails
            subprocess.run(['barformatter', str(file)], check=True)
            ok('Formatted {str(file)}')

            if report_progress:
                report_progress.update()

        return 0
```

[poetry]: https://python-poetry.org/
[pip]: https://pip.pypa.io/en/stable/
