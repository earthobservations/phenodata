# =============
# Configuration
# =============

$(eval venv         := .venv)
$(eval pip          := $(venv)/bin/pip)
$(eval python       := $(venv)/bin/python)
$(eval pytest       := $(venv)/bin/pytest)
$(eval bumpversion  := $(venv)/bin/bumpversion)
$(eval twine        := $(venv)/bin/twine)
$(eval proselint    := $(venv)/bin/proselint)


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

docs-lint: install-tests
	$(proselint) *.rst doc/*.rst doc/**/*.rst

check: docs-lint test


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
	@$(twine) upload --skip-existing --verbose dist/{*.tar.gz,*.whl}


# =================
# Installer targets
# =================

install-package:
	@test -e $(python) || python3 -m venv $(venv)
	$(pip) install --prefer-binary --editable=.[test,develop,release,sql]

install-doctools:
	@test -e $(python) || python3 -m venv $(venv)
	$(pip) install --requirement doc/requirements.txt --upgrade

install-releasetools:
	@test -e $(python) || python3 -m venv $(venv)
	$(pip) install --requirement requirements-release.txt --upgrade

install-tests:
	@test -e $(python) || python3 -m venv $(venv)
	$(pip) install --requirement requirements-tests.txt --upgrade
