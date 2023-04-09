#################
Python virtualenv
#################

About
=====

`virtualenv`_ is a tool to create isolated Python environments.
We recommend it for installing the software and its dependencies
independently of your Python distribution.

Install
=======

Create a Python `virtualenv`_::

    python3 -m venv .venv

Install::

    # Activate virtualenv
    source .venv/bin/activate

    # Install Python package
    pip install phenodata[sql]

.. _virtualenv: https://virtualenv.pypa.io/
