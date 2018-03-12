bumpversion:
	bumpversion $(bump)

push:
	git push && git push --tags

sdist:
	python setup.py sdist

upload:
	twine upload --skip-existing dist/phenodata-*.tar.gz

# make release bump=minor  (major,minor,patch)
release: bumpversion push sdist upload


docs-virtualenv:
	$(eval venvpath := ".venv_sphinx")
	@test -e $(venvpath)/bin/python || `command -v virtualenv` --python=`command -v python` --no-site-packages $(venvpath)
	@$(venvpath)/bin/pip install --quiet --requirement requirements-docs.txt

docs-html: docs-virtualenv
	$(eval venvpath := ".venv_sphinx")
	touch doc/index.rst
	export SPHINXBUILD="`pwd`/$(venvpath)/bin/sphinx-build"; cd doc; make html
