# Release instructions

Before creating a new release please do a careful consideration about the
version number for the new release. We are following [Semantic Versioning](https://semver.org/)
and [PEP440](https://www.python.org/dev/peps/pep-0440/).

* Install development dependencies

  ```sh
  pipenv install --dev
  ```

* Fetch upstream changes and create release branch

  ```sh
  git fetch upstream
  git checkout -b create-new-release upstream/master
  ```

* Open autohooks/version.py
  and increment the version number.

* Create a source distribution only. Do **NOT** create a wheel by running
  bdist_wheel.

  ```sh
  rm -rf dist build autohooks.egg-info
  python3 setup.py sdist
  ```

* Create a git commit

  ```sh
  git add .
  git commit -m "Prepare release <version>"
  ```

* Create an account at [Test PyPI](https://packaging.python.org/guides/using-testpypi/)

* Upload the archives in dist to [Test PyPI](https://test.pypi.org/)

  ```sh
  twine upload --repository-url https://test.pypi.org/legacy/ dist/*
  ```

* Check if the package is available at https://test.pypi.org/project/autohooks

* Create a test directory

  ```sh
  mkdir autohooks-install-test
  cd autohooks-install-test
  pipenv run pip install --pre -I --extra-index-url https://test.pypi.org/simple/ autohooks
  ```

* Remove test environment

  ```sh
  pipenv --rm
  cd ..
  rm -rf autohooks-install-test
  ```

* Create an account at [PyPI](https://pypi.org/) if not exist already

* Upload to real [PyPI](https://pypi.org/)

  ```sh
  twine upload dist/*
  ```

* Check if new version is available at https://pypi.org/project/autohooks

* Create a git tag

  ```sh
  git tag v<version>
  ```

  or even signed with your gpg key

  ```sh
  git tag -s v<version>
  ```

* Update version in autohooks/version.py

  Use a alpha version like `(1, 1, 1, 'alpha')` or
  `(1, 1, 1, 'alpha', 0)`

* Create a commit

  ```sh
  git commit -m "Update version after <version> release"
  ```

* Push changes and tag to GitHub

  ```sh
  git push --tags upstream master
  ```
