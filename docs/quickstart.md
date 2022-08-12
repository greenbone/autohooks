# Quickstart

Autohooks is distributed on [PyPI]. Because it is a tool and library mostly used
for development it can be best used with [poetry].

Quick installation of [pylint] and [black] plugins using [poetry]:

```shell
poetry add --dev autohooks autohooks-plugin-black autohooks-plugin-pylint

poetry run autohooks activate --mode poetry
poetry run autohooks plugins add autohooks.plugins.black autohooks.plugins.pylint
```

[PyPI]: https://pypi.org
[poetry]: https://python-poetry.org/
[black]: https://black.readthedocs.io/en/stable/
[pylint]: https://pylint.readthedocs.io/en/latest/
