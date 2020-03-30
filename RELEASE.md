# Release instructions

Before creating a new release please do a careful consideration about the
version number for the new release. We are following [Semantic Versioning](https://semver.org/)
and [PEP440](https://www.python.org/dev/peps/pep-0440/).

* Install development dependencies

  ```sh
  poetry install
  ```

* Fetch upstream changes and create release branch

  ```sh
  git fetch upstream
  git checkout -b create-new-release upstream/master
  ```

* Open [autohooks/version.py](autohooks/version.py)
  and increment the version number.

* Update [CHANGELOG](CHANGELOG.md)

* Create a source distribution only. Do **NOT** create a wheel by running
  poetry build without arguments.

  ```sh
  rm -rf dist build autohooks.egg-info pip-wheel-metadata
  poetry build --format=sdist
  ```

* Create a git commit

  ```sh
  git add .
  git commit -m "Prepare release <version>"
  ```

* Create a pypirc file

  ```sh
  vim ~/.pypirc
  ```

  with the following content (Note: `<username>` must be replaced)

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = <username>

[testpypi]
repository = https://test.pypi.org/legacy/
username = <username>
```

* Create an account at [Test PyPI](https://packaging.python.org/guides/using-testpypi/)

* Upload the archives in dist to [Test PyPI](https://test.pypi.org/)

  ```sh
  twine upload -r testpypi dist/*
  ```

* Check if the package is available at https://test.pypi.org/project/autohooks

* Create a test directory

  ```sh
  mkdir autohooks-install-test
  cd autohooks-install-test
  git init
  python3 -m venv test-env
  source ./test-env/bin/activate
  pip install --pre -I --extra-index-url https://test.pypi.org/simple/ autohooks
  autohooks check
  python -c "from autohooks.version import get_version; print(get_version())"
  ```

* Remove test environment

  ```sh
  cd ..
  rm -rf autohooks-install-test
  ```

* Create a release PR

  ```sh
  git push origin
  ```
  Open GitHub and create a PR against https://github.com/greenbone/autohooks

* Update after PR is merged

  ```sh
  git fetch upstream
  git rebase upstream/master master
  ```
* Create a git tag

  ```sh
  git tag v<version>
  ```

  or even signed with your gpg key

  ```sh
  git tag -s v<version>
  ```

* Push tag to GitHub

  ```sh
  git push --tags upstream
  ```

* Uploading to PyPI is done automatically by pushing a git tag via CircleCI

* Check if new version is available at https://pypi.org/project/autohooks

* Update version in `pyproject.toml`

  Use a development version like `1.1.1.dev1`

* Create a commit

  ```sh
  git commit -m "Update version after <version> release"
  ```

* Push changes to GitHub

  ```sh
  git push upstream
  ```

* Create a Github release:

   See https://help.github.com/articles/creating-releases/
