# Configuration

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
