.. image:: https://img.shields.io/badge/Python-2.7-green.svg
    :target: https://pypi.org/project/phenodata/

.. image:: https://img.shields.io/pypi/v/phenodata.svg
    :target: https://pypi.org/project/phenodata/

.. image:: https://img.shields.io/github/tag/hiveeyes/phenodata.svg
    :target: https://github.com/hiveeyes/phenodata

|

#################################################
phenodata - phenology data acquisition for humans
#################################################


*****
About
*****
phenodata is a data acquisition and manipulation toolkit for open access phenology data.
It is written in Python.

Currently, it implements data wrappers for acquiring phenology observation data published
on the DWD Climate Data Center (CDC) FTP server operated by »Deutscher Wetterdienst« (DWD).

Under the hood, it uses the fine Pandas_ data analysis library for data mangling, amongst others.

.. _Pandas: https://pandas.pydata.org/


****************
Acknowledgements
****************
Thanks to the many observers, »Deutscher Wetterdienst«,
the »Global Phenological Monitoring programme« and all people working behind
the scenes for their commitment in recording the observations and for making
the excellent datasets available to the community. You know who you are.


***************
Getting started
***************

Install
=======
If you know your way around Python, installing this software is really easy::

    pip install phenodata --upgrade

Please refer to the `virtualenv`_ page about further recommendations how to install and use this software.

.. _virtualenv: https://github.com/hiveeyes/phenodata/blob/master/doc/virtualenv.rst


Usage
=====
::

    $ phenodata --help
    Usage:
      phenodata info
      phenodata list-species --source=dwd [--format=csv]
      phenodata list-phases --source=dwd [--format=csv]
      phenodata list-stations --source=dwd --dataset=immediate [--format=csv]
      phenodata list-quality-levels --source=dwd [--format=csv]
      phenodata list-quality-bytes --source=dwd [--format=csv]
      phenodata list-filenames --source=dwd --dataset=immediate --partition=recent [--files=Hasel,Schneegloeckchen] [--years=2017 | --forecast]
      phenodata list-urls --source=dwd --dataset=immediate --partition=recent [--files=Hasel,Schneegloeckchen] [--years=2017 | --forecast]
      phenodata observations --source=dwd --dataset=immediate --partition=recent [--files=Hasel,Schneegloeckchen] [--stations=164,717 | --regions=berlin,brandenburg] [--species=hazel,snowdrop] [--phases=flowering] [--years=2017 | --forecast] [--format=csv]
      phenodata --version
      phenodata (-h | --help)

    Data acquisition options:
      --source=<source>         Data source. Currently "dwd" only.
      --dataset=<dataset>       Data set. Use "annual" or "immediate" for --source=dwd.
      --partition=<dataset>     Partition. Use "recent" or "historical" for --source=dwd.

    Data filtering options:
      --files=<files>           Filter by files (comma-separated list)
      --years=<years>           Filter by years (comma-separated list)
      --stations=<stations>     Filter by station ids (comma-separated list)
      --regions=<regions>       Filter by region names (comma-separated list)
      --species=<species>       Filter by species names (comma-separated list)
      --phases=<phases>         Filter by phase names (comma-separated list)

    Data formatting options:
      --format=<format>         Output data in designated format. Choose one of "tabular", "json" or "csv".
                                With "tabular", it is also possible to specify the table format,
                                see https://bitbucket.org/astanin/python-tabulate. e.g. "tabular:presto".
                                [default: tabular:psql]

.. note::

    For most acquisition tasks, you must choose from one of two different datasets: `annual-reporters`_ and `immediate-reporters`_.

.. _annual-reporters: https://www.dwd.de/DE/klimaumwelt/klimaueberwachung/phaenologie/daten_deutschland/jahresmelder/jahresmelder_node.html
.. _immediate-reporters: https://www.dwd.de/DE/klimaumwelt/klimaueberwachung/phaenologie/daten_deutschland/sofortmelder/sofortmelder_node.html


Examples
========


Metadata
--------

Display list of species::

    phenodata list-species --source=dwd

Display list of phases::

    phenodata list-phases --source=dwd

Display list of stations::

    phenodata list-stations --source=dwd --dataset=immediate

Display list of file names of recent observations by the annual reporters::

    phenodata list-filenames --source=dwd --dataset=annual --partition=recent

Display list of full URLs to recent observations by the annual reporters
and apply filter criteria to the filename::

    phenodata list-urls --source=dwd --dataset=annual --partition=recent --files=Hasel,Schneegloeckchen


Observations
------------

Display observations of hazel and snowdrop::

    phenodata observations --source=dwd --dataset=annual --partition=recent --files=Hasel,Schneegloeckchen

Display observations of hazel and snowdrop for stations 164 and 717::

    phenodata observations --source=dwd --dataset=annual --partition=recent --files=Hasel,Schneegloeckchen --stations=164,717

Display all observations for stations 164 and 717 in 2016 and 2017::

    phenodata observations --source=dwd --dataset=annual --partition=recent --stations=164,717 --years=2016,2017


Todo
----
.. warning:: These commands are not implemented yet.

Display regular flowering events for hazel and snowdrop around Berlin and Brandenburg (Germany) in 2017::

    phenodata calendar --source=dwd --dataset=immediate --partition=recent --regions=berlin,brandenburg --species=hazel,snowdrop --phases=flowering --years=2017

    phenodata calendar --source=dwd --dataset=immediate --partition=historical --regions=berlin,brandenburg --species=hazel,snowdrop --phases=flowering --years=1958

Display forecast for "beginning of flowering" events for canola and sweet cherry
around Thüringen and Bayern (Germany), deduced from annual/recent data::

    phenodata calendar --source=dwd --dataset=annual --partition=recent --regions=thüringen,bayern --species=raps,süßkirsche --phases-bbch=60 --forecast

To improve data acquisition performance, also consider applying
the ``--files=`` parameter for file name filtering.

Example: When using ``--files=Hasel,Schneegloeckchen``, only file names
containing ``Hasel`` or ``Schneegloeckchen`` will be retrieved.


*******************
Project information
*******************

About
=====
The "phenodata" program is released under the AGPL license.
The code lives on `GitHub <https://github.com/hiveeyes/phenodata>`_ and
the Python package is published to `PyPI <https://pypi.org/project/phenodata/>`_.
You might also want to have a look at the `documentation <https://hiveeyes.org/docs/phenodata/>`_.

The software has been tested on Python 2.7.

If you'd like to contribute you're most welcome!
Spend some time taking a look around, locate a bug, design issue or
spelling mistake and then send us a pull request or create an issue.

Thanks in advance for your efforts, we really appreciate any help or feedback.

Code license
============
Licensed under the AGPL license. See LICENSE_ file for details.

.. _LICENSE: https://github.com/hiveeyes/phenodata/blob/master/LICENSE

Data license
============
The DWD has information about their re-use policy in German and English.
Please refer to the respective Disclaimer
(`de <https://www.dwd.de/DE/service/disclaimer/disclaimer_node.html>`__,
`en <https://www.dwd.de/EN/service/disclaimer/disclaimer.html>`__)
and Copyright
(`de <https://www.dwd.de/DE/service/copyright/copyright_node.html>`__,
`en <https://www.dwd.de/EN/service/copyright/copyright_artikel.html>`__)
information.

Disclaimer
==========
The project and its authors are not affiliated with DWD, USA-NPN or any
other data provider in any way. It is a sole project from the community
for making data more accessible in the spirit of open data.
