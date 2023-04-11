###########
Development
###########


*******
Sandbox
*******

Acquire sources, create Python virtualenv, install package and dependencies,
and run software tests::

    git clone https://github.com/earthobservations/phenodata
    cd phenodata
    make check


*****
Tests
*****

In order to run tests individually, enter the virtualenv, and invoke ``pytest``
directly, like::

    source .venv/bin/activate
    pytest -k sql
    pytest -k readme
    pytest -k example

