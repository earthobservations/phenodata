# =============
# Configuration
# =============

$(eval venv         := .venv)
$(eval pip          := $(venv)/bin/pip)
$(eval python       := $(venv)/bin/python)
$(eval pytest       := $(venv)/bin/pytest)
$(eval bumpversion  := $(venv)/bin/bumpversion)
$(eval twine        := $(venv)/bin/twine)


# ============
# Main targets
# ============

# Run software tests.
.PHONY: test
test: install-package install-tests
	$(pytest)

# Release this piece of software
# Synopsis:
#   make release bump=minor  (major,minor,patch)
release: bumpversion push build pypi-upload

# Build the documentation
docs-html: install-doctools
	touch doc/index.rst
	export SPHINXBUILD="`pwd`/$(venv)/bin/sphinx-build"; cd doc; make html


# ===============
# Utility targets
# ===============
bumpversion: install-releasetools
	@$(bumpversion) $(bump)

push:
	git push && git push --tags

build:
	@$(python) -m build

pypi-upload: install-releasetools
	@$(twine) upload --skip-existing dist/*.tar.gz


# =================
# Installer targets
# =================

install-package:
	@test -e $(python) || python3 -m venv $(venv)
	@$(pip) install --quiet --use-pep517 --prefer-binary --editable=.[test,develop,release,sql]

install-doctools:
	@test -e $(python) || python3 -m venv $(venv)
	@$(pip) install --quiet --requirement requirements-docs.txt --upgrade

install-releasetools:
	@test -e $(python) || python3 -m venv $(venv)
	@$(pip) install --quiet --requirement requirements-release.txt --upgrade

install-tests:
	@test -e $(python) || python3 -m venv $(venv)
	@$(pip) install --quiet --requirement requirements-tests.txt --upgrade
