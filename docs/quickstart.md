# Quickstart

Autohooks is distributed on [PyPI]. Because it is a tool and library mostly used
for development it can be best used with [uv].

Quick installation of [pylint] and [black] plugins using [uv]:

```shell
uv add --dev autohooks autohooks-plugin-black autohooks-plugin-pylint

uv run autohooks activate --mode uv
uv run autohooks plugins add autohooks.plugins.black autohooks.plugins.pylint
```

[PyPI]: https://pypi.org
[black]: https://black.readthedocs.io/en/stable/
[pylint]: https://pylint.readthedocs.io/en/latest/
[uv]: https://docs.astral.sh/uv/
