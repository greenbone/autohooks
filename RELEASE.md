# Release instructions

Before creating a new release please do a careful consideration about the
version number for the new release. We are following [Semantic Versioning](https://semver.org/)
and [PEP440](https://www.python.org/dev/peps/pep-0440/).

## Preparing the Required Python Packages

* Install development dependencies

  ```sh
  poetry install
  ```

* Install twine for pypi package uploads

  ```sh
  python3 -m pip install --user --upgrade twine
  ```

## Configuring the Access to the Python Package Index (PyPI)

*Note:* This is only necessary for users performing the release process for the
first time.

* Create an account at [Test PyPI](https://packaging.python.org/guides/using-testpypi/).

* Create an account at [PyPI](https://pypi.org/).

* Create a pypi configuration file `~/.pypirc` with the following content (Note:
  `<username>` must be replaced):

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

## Prepare testing the Release

* Fetch upstream changes and create release branch

  ```sh
  git fetch upstream
  git checkout -b create-new-release upstream/master
  ```

* Get the current version number

  ```sh
  poetry run python -m autohooks.version show
  ```

* Update the version number to some alpha version e.g.

  ```sh
  poetry run python -m autohooks.version update 2.2.3a1
  ```

## Uploading to the PyPI Test Instance

* Create a source and wheel distribution:

  ```sh
  rm -rf dist build autohooks.egg-info pip-wheel-metadata
  poetry build
  ```

* Upload the archives in `dist` to [Test PyPI](https://test.pypi.org/):

  ```sh
  twine upload -r testpypi dist/*
  ```

* Check if the package is available at <https://test.pypi.org/project/autohooks>

* Create a test directory

  ```sh
  mkdir autohooks-install-test
  cd autohooks-install-test
  git init
  python3 -m venv test-env
  source ./test-env/bin/activate
  pip install -U pip  # ensure the environment uses a recent version of pip
  pip install --pre -I --extra-index-url https://test.pypi.org/simple/ autohooks
  python -c "from autohooks.version import get_version; print(get_version())"
  autohooks check
  ```

* Remove test environment

  ```sh
  deactivate
  cd ..
  rm -rf autohooks-install-test
  ```

## Prepare the Release

* Determine new release version number

  If the output is something like  `2.2.3.dev1` or `2.2.3a1`, the new version
  should be `2.2.3`.

* Update to new version number (`<new-version>` must be replaced by the version
  from the last step)

  ```sh
  cd path/to/git/clone/of/autohooks
  poetry run python -m autohooks.version update <new-version>
  ```

* Update the `CHANGELOG.md` file:
  * Change `[unreleased]` to new release version.
  * Add a release date.
  * Update reference to Github diff.
  * Remove empty sub sections like *Deprecated*.

* Create a git commit:

  ```sh
  git add .
  git commit -m "Prepare release <version>"
  ```

## Performing the Release on GitHub

* Create a pull request (PR) for the earlier commit:

  ```sh
  git push origin
  ```
  Open GitHub and create a PR against <https://github.com/greenbone/autohooks>

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

## Uploading to the 'real' PyPI

* Uploading to PyPI is done automatically by pushing a git tag via CircleCI

* Check if new version is available at <https://pypi.org/project/autohooks>

## Bumping `master` Branch to the Next Version

* Update to a Development Version

  The next version should contain an incremented minor version and a dev suffix
  e.g. 2.3.0.dev1

  ```sh
  poetry run python -m autohooks.version update <next-dev-version>
  ```

* Create a commit

  ```sh
  git commit -m "Update version after <version> release"
  ```

* Push changes to GitHub

  ```sh
  git push upstream
  ```

## Announcing the Release

* Create a Github release:

   See https://help.github.com/articles/creating-releases/
