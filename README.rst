.. image:: https://github.com/earthobservations/phenodata/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/earthobservations/phenodata/actions?workflow=Tests

.. image:: https://readthedocs.org/projects/phenodata/badge/
    :target: https://phenodata.readthedocs.io/

.. image:: https://codecov.io/gh/earthobservations/phenodata/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/earthobservations/phenodata

.. image:: https://static.pepy.tech/badge/phenodata/month
    :target: https://pepy.tech/project/phenodata

.. image:: https://img.shields.io/pypi/pyversions/phenodata.svg
    :target: https://pypi.org/project/phenodata/

.. image:: https://img.shields.io/pypi/v/phenodata.svg
    :target: https://pypi.org/project/phenodata/

.. image:: https://img.shields.io/pypi/l/phenodata.svg
    :target: https://pypi.org/project/phenodata/

|

#########
phenodata
#########

*Phenology data acquisition for humans.*


*****
About
*****

Phenodata is an acquisition and processing toolkit for open access phenology
data. It is based on `pandas`_, and can be used both as a standalone program,
and as a library.

Currently, it implements data wrappers for acquiring phenology observation
data published on the DWD Climate Data Center (CDC) FTP server operated by
»Deutscher Wetterdienst« (DWD). Adding adapters for other phenology databases
and APIs is possible and welcome.

Acknowledgements
================

Thanks to the many observers of »Deutscher Wetterdienst« (DWD), the »Global
Phenological Monitoring programme« (GPM), and all people working behind the
scenes for their commitment on recording observations and making the excellent
datasets available to the community. You know who you are.

Notes
=====

Please note that phenodata is beta-quality software, and a work in progress.
Contributions of all kinds are welcome, in order to make it more solid.

Breaking changes should be expected until a 1.0 release, so version pinning
is recommended, especially when you use phenodata as a library.



********
Synopsis
********

The easiest way to use phenodata, and to explore the dataset interactively,
is to use its command-line interface.

Those two examples will acquire observation data from DWD's network, only focus
on the "beginning of flowering" phase event, and present the results in tabular
format using values suitable for human consumption.

Acquire data from DWD's "immediate" dataset (Sofortmelder).

.. code-block:: bash

    phenodata observations \
        --source=dwd --dataset=immediate --partition=recent \
        --year=2023 --station=brandenburg \
        --species-preset=mellifera-de-primary \
        --phase="beginning of flowering" \
        --humanize --sort=Datum --format=rst

Acquire data from DWD's "annual" dataset (Jahresmelder).

.. code-block:: bash

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --year="2022,2023" --station=berlin \
        --species-preset=mellifera-de-primary \
        --phase="beginning of flowering" \
        --humanize --sort=Datum --format=rst

.. tip::

    The authors recommend to copy one of those snippets into a file and invoke it
    as a script program, in order to make subsequent invocations easier while
    editing and exploring different option values. If you discover a bug, or want
    to make your program available to others because you think it is useful, feel
    free to `share it back with us`_.

Output example
==============

Phenodata can produce output in different formats. This is a table in
`reStructuredText`_ format.

==========  ======================  ======================  =====================
Datum       Spezies                 Phase                   Station
==========  ======================  ======================  =====================
2018-02-17  common snowdrop         beginning of flowering  Berlin-Dahlem, Berlin
2018-02-19  common hazel            beginning of flowering  Berlin-Dahlem, Berlin
2018-03-30  goat willow             beginning of flowering  Berlin-Dahlem, Berlin
2018-04-07  dandelion               beginning of flowering  Berlin-Dahlem, Berlin
2018-04-15  cherry (late ripeness)  beginning of flowering  Berlin-Dahlem, Berlin
2018-04-21  winter oilseed rape     beginning of flowering  Berlin-Dahlem, Berlin
2018-04-23  apple (early ripeness)  beginning of flowering  Berlin-Dahlem, Berlin
2018-05-03  apple (late ripeness)   beginning of flowering  Berlin-Dahlem, Berlin
2018-05-24  black locust            beginning of flowering  Berlin-Dahlem, Berlin
2018-08-20  common heather          beginning of flowering  Berlin-Dahlem, Berlin
==========  ======================  ======================  =====================

.. note::

    Using the example snippet provided above, the program rendered a table in
    `reStructuredText`_ format using ``--format=rst``. In order to render
    tables in `Markdown`_ format, use ``--format=md``. For more tabular output
    formats, use ``--format=tabular:foo``, and consult the documentation of the
    `tabulate`_ package for choices of ``foo``.


*****
Usage
*****

Introduction
============

For most acquisition tasks, you will have to select one of two different
datasets of DWD, `annual-reporters`_ or `immediate-reporters`_. Further, the
data partition has to be selected, it is either ``recent``, or ``historical``.

Currently, as of 2023, the ``historical`` datasets extend from the past until
2021. All subsequent observations are stored within the ``recent`` dataset
partition.

The DWD publishes data in files separated by species, this means each plant's
data will be in a different file. By default, phenodata will acquire data for
all species (plants), in order to be able to respond to all kinds of queries
across the whole dataset.

If you are only interested in a limited set of species (plants), you can
improve data acquisition performance by using the ``filename`` option to only
select specific files for retrieval.

For example, when using ``--filename=Hasel,Schneegloeckchen``, only file names
containing ``Hasel`` or ``Schneegloeckchen`` will be retrieved, thus minimizing
the effort needed to acquire *all* files.

Install
=======

To install the software from PyPI, invoke::

    pip install 'phenodata[sql]' --upgrade

.. note::

    Please refer to the `virtualenv`_ page about best-practice recommendations to
    install the software separate from your system environment.

Library use
===========

This snippet demonstrates how to use phenodata as a library within individual
programs. For ready-to-run code examples, please have a look into the `examples
directory`_.

.. hidden

    .. code-block:: python

        >>> import os
        >>> import pytest
        >>> if "GITHUB_ACTION" in os.environ:
        ...     pytest.skip(msg="pytest-doctest-ellipsis-markers does not work on CI/GHA. Works on macOS though.", allow_module_level=True)

.. code-block:: python

    >>> import pandas as pd
    >>> from phenodata.ftp import FTPSession
    >>> from phenodata.dwd.cdc import DwdCdcClient
    >>> from phenodata.dwd.pheno import DwdPhenoData

    >>> cdc_client = DwdCdcClient(ftp=FTPSession())
    >>> client = DwdPhenoData(cdc=cdc_client, humanizer=None, dataset="immediate")
    >>> options = {
    ...     # Select data partition.
    ...     "partition": "recent",
    ...
    ...     # Filter by file names and years.
    ...     "filename": ["Hasel", "Raps", "Mais"],
    ...     "year": [2018, 2019, 2020],
    ...
    ...     # Filter by station identifier.
    ...     "station-id": [13346]
    ... }

    >>> observations: pd.DataFrame = client.get_observations(options, humanize=False)
    >>> observations.info()
    [...]
    >>> observations
    [...]


Command-line use
================

This section gives you an idea about how to use the ``phenodata`` program on
the command-line.

::

    $ phenodata --help

    Usage:
      phenodata info
      phenodata list-species --source=dwd [--format=csv]
      phenodata list-phases --source=dwd [--format=csv]
      phenodata list-stations --source=dwd --dataset=immediate [--all] [--filter=berlin] [--sort=Stationsname] [--format=csv]
      phenodata nearest-station --source=dwd --dataset=immediate --latitude=52.520007 --longitude=13.404954 [--format=csv]
      phenodata nearest-stations --source=dwd --dataset=immediate --latitude=52.520007 --longitude=13.404954 [--all] [--limit=10] [--format=csv]
      phenodata list-quality-levels --source=dwd [--format=csv]
      phenodata list-quality-bytes --source=dwd [--format=csv]
      phenodata list-filenames --source=dwd --dataset=immediate --partition=recent [--filename=Hasel,Schneegloeckchen] [--year=2017]
      phenodata list-urls --source=dwd --dataset=immediate --partition=recent [--filename=Hasel,Schneegloeckchen] [--year=2017]
      phenodata (observations|forecast) --source=dwd --dataset=immediate --partition=recent [--filename=Hasel,Schneegloeckchen] [--station-id=164,717] [--species-id=113,127] [--phase-id=5] [--quality-level=10] [--quality-byte=1,2,3] [--station=berlin,brandenburg] [--species=hazel,snowdrop] [--species-preset=mellifera-de-primary] [--phase=flowering] [--quality=ROUTKLI] [--year=2017] [--forecast-year=2021] [--humanize] [--show-ids] [--language=german] [--long-station] [--sort=Datum] [--sql=sql] [--format=csv] [--verbose]
      phenodata drop-cache --source=dwd
      phenodata --version
      phenodata (-h | --help)

    Data acquisition options:
      --source=<source>         Data source. Currently, only "dwd" is a valid identifier.
      --dataset=<dataset>       Data set. Use "immediate" or "annual" for "--source=dwd".
      --partition=<dataset>     Partition. Use "recent" or "historical" for "--source=dwd".
      --filename=<file>         Filter by file names (comma-separated list)

    Direct filtering options:
      --year=<year>             Filter by year (comma-separated list)
      --station-id=<station-id> Filter by station identifiers (comma-separated list)
      --species-id=<species-id> Filter by species identifiers (comma-separated list)
      --phase-id=<phase-id>     Filter by phase identifiers (comma-separated list)

    Humanized filtering options:
      --station=<station>       Filter by strings from "stations" data (comma-separated list)
      --species=<species>       Filter by strings from "species" data (comma-separated list)
      --phase=<phase>           Filter by strings from "phases" data (comma-separated list)
      --species-preset=<preset> Filter by strings from "species" data (comma-separated list)
                                The preset will get loaded from the "presets.json" file.

    Forecasting options:
      --forecast-year=<year>    Use as designated forecast year.

    Postprocess filtering options:
      --sql=<sql>               Apply given SQL query before output.

    Data output options:
      --format=<format>         Output data in designated format. Choose one of "tabular", "json",
                                "csv", or "string". Use "md" for Markdown output, or "rst" for
                                reStructuredText. With "tabular:foo", it is also possible to specify
                                other tabular output formats.  [default: tabular:psql]
      --sort=<sort>             Sort by given field names. (comma-separated list)
      --humanize                Resolve identifier-based fields to human-readable labels.
      --show-ids                Show identifiers alongside resolved labels, when using "--humanize".
      --language=<language>     Use labels in designated language, when using "--humanize"
                                [default: english].
      --long-station            Use long station name including "Naturraumgruppe" and "Naturraum".
      --limit=<limit>           Limit output of "nearest-stations" to designated number of entries.
                                [default: 10]
      --verbose                 Turn on verbose output.


********
Examples
********

The best way to explore phenodata is by running a few example invocations.

- The "Metadata" section will walk you through different commands which can be
  used to inquire information about monitoring stations/sites, and to list
  the actual files which will be acquired, in order to learn about data lineage.

- The "Observations" section will demonstrate command examples to acquire,
  process, and format actual observation data.


Metadata
========

Display list of species, with their German, English, and Latin names::

    phenodata list-species --source=dwd

Display list of phases, with their German and English names::

    phenodata list-phases --source=dwd

List of all reporting/monitoring stations::

    phenodata list-stations --source=dwd --dataset=immediate

List of stations, with filtering::

    phenodata list-stations --source=dwd --dataset=annual --filter="Fränkische Alb"

Display nearest station for given position::

    phenodata nearest-station --source=dwd --dataset=immediate \
        --latitude=52.520007 --longitude=13.404954

Display 20 nearest stations for given position::

    phenodata nearest-stations \
        --source=dwd --dataset=immediate \
        --latitude=52.520007 --longitude=13.404954 --limit=20

List of file names of recent observations by the annual reporters::

    phenodata list-filenames \
        --source=dwd --dataset=annual --partition=recent

Same as above, but with filtering by file name::

    phenodata list-filenames \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel,Kornelkirsche,Loewenzahn,Schneegloeckchen

List full URLs instead of only file names::

    phenodata list-urls \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel,Kornelkirsche,Loewenzahn,Schneegloeckchen


Observations
============

Basic
-----

Observations of hazel and snowdrop, using filename-based filtering at data acquisition time::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel,Schneegloeckchen

Observations of hazel and snowdrop (dito), but for specific station identifiers::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel,Schneegloeckchen --station-id=7521,7532

All observations for specific station identifiers and specific years::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --station-id=7521,7532 --year=2020,2021

All observations for specific station and species identifiers::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --station-id=7521,7532 --species-id=113,127

All observations marked as invalid::

    phenodata list-quality-bytes --source=dwd
    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --quality-byte=5,6,7,8


Humanized output
----------------

The option ``--humanize`` will improve textual output by resolving identifier
fields to appropriate human-readable text labels.

Observations for species "hazel", "snowdrop", "apple" and "pear" at station
"Berlin-Dahlem", output texts in the German language, if possible::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel,Schneegloeckchen,Apfel,Birne \
        --station-id=12132 \
        --humanize \
        --language=german


Humanized search
----------------

When using the ``--humanize`` option, you can use the non-identifier-based
filtering options ``--station``, ``--species``, and ``--phase``, to use
human-readable text labels for filtering instead of numeric identifiers.

Query observations by using real-world location names::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel,Schneegloeckchen \
        --station=berlin,brandenburg \
        --humanize --sort=Datum

Query observations near Munich with species names "hazel" and "snowdrop" in specific year::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --station=münchen \
        --species=hazel,snowdrop \
        --year=2022 \
        --humanize --sort=Datum

Now, let's query for any "flowering" observations. There will be ``beginning
of flowering``, ``general flowering``, and ``end of flowering``::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --station=münchen \
        --phase=flowering \
        --year=2022 \
        --humanize --sort=Datum

Same observations as before but with ``ROUTKLI`` quality marker::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --station=münchen \
        --phase=flowering \
        --quality="nicht beanstandet" \
        --year=2022 \
        --humanize --sort=Datum

Now, let's inquire those field values which have seen corrections instead
(``Feldwert korrigiert``)::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --station=münchen \
        --phase=flowering \
        --quality=korrigiert \
        --humanize --sort=Datum


Filtering with presets
----------------------

When using the ``--humanize`` option, you can also use pre-defined shortcuts
for lists of species by name. For example, the ``mellifera-de-primary`` preset
is defined within the `presets.json`_ file like::

    Hasel, Schneeglöckchen, Sal-Weide, Löwenzahn, Süßkirsche, Apfel, Winterraps, Robinie, Winter-Linde, Heidekraut

Then, you can use the option ``--species-preset=mellifera-de-primary`` instead
of the ``--species`` option for filtering only those specified species.

This example lists all "beginning of flowering" observations for the specified
years in Köln, only for the named list of species ``mellifera-de-primary``.
The result will be sorted by species and date, and human-readable labels will
be displayed in German, when possible::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --phase="beginning of flowering" \
        --year=2021,2022,2023 \
        --station=köln \
        --species-preset=mellifera-de-primary \
        --humanize --language=german --sort=Spezies,Datum

.. note::

    Contributions are welcome to introduce other groups of species which fit
    into different phenology domains or use-case categories.


Filtering with SQL
------------------

Phenodata uses the `DuckDB Python API`_ to let you directly query the `pandas`_
DataFrame produced by the data acquisition subsystem. This example uses an SQL
statement to filter the results by station name, and sort them by date::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --year=2019,2020,2021,2022,2023 \
        --species-preset=mellifera-de-primary --phase="beginning of flowering" \
        --humanize --language=german \
        --sql="SELECT * FROM data WHERE Station LIKE '%Berlin%' ORDER BY Datum" \
        --format=md


*******************
Project information
*******************

Resources
=========
- `Source code <https://github.com/earthobservations/phenodata>`_
- `Documentation <https://phenodata.readthedocs.io/>`_
- `Python Package Index (PyPI) <https://pypi.org/project/phenodata/>`_

Contributions
=============
If you would like to contribute, you are most welcome. Spend some time taking a
look around, locate a bug, design issue or spelling mistake and then send us a
pull request or create an issue. Thank you in advance for your efforts, the
authors really appreciate any kind of help and feedback.

Discussions
===========
Discussions around the development of phenodata and its applications are
taking place at the Hiveeyes forum. Enjoy reading them, and don't hesitate to
write in, if you think you may be able to contribute a thing or another, or
to share what you have been doing with the program in form of a "show and tell"
post.

- https://community.hiveeyes.org/t/phanologischer-kalender-fur-trachtpflanzen/664
- https://community.hiveeyes.org/t/phenodata-ein-datenbezug-und-manipulations-toolkit-fur-open-access-phanologiedaten/2892
- https://community.hiveeyes.org/t/phanologischer-kalender-2020/2893
- https://community.hiveeyes.org/t/klimadatenkalender-zur-anzeige-der-phanologischen-daten-des-deutschen-wetterdienstes/948
- https://community.hiveeyes.org/t/phanologie-und-imkerliche-eingriffe-bei-den-bienen/705
- https://community.hiveeyes.org/t/phenological-calendar-for-france/800

Development
===========
In order to setup a development environment on your workstation, please head
over to the `development sandbox`_ documentation. When you see the software
tests succeed, you should be ready to start hacking.

Code license
============
The project is licensed under the terms of the GNU AGPL license, see `LICENSE`_.

Data license
============
The DWD has information about their data re-use policy in German and English.
Please refer to the respective Disclaimer
(`de <https://www.dwd.de/DE/service/disclaimer/disclaimer_node.html>`__,
`en <https://www.dwd.de/EN/service/disclaimer/disclaimer.html>`__)
and Copyright
(`de <https://www.dwd.de/DE/service/copyright/copyright_node.html>`__,
`en <https://www.dwd.de/EN/service/copyright/copyright_artikel.html>`__)
information.

Disclaimer
==========
The project and its authors are not affiliated with DWD, GPM, USA-NPN, or any
other organization in any way. It is a sole project conceived by the community,
in order to make data more accessible, in the spirit of `open data`_ and `open
scientific data`_. The authors believe the world would be a better place if
public data could be loaded into `pandas`_ dataframes and `Xarray`_ datasets
easily.


.. _annual-reporters: https://www.dwd.de/DE/klimaumwelt/klimaueberwachung/phaenologie/daten_deutschland/jahresmelder/jahresmelder_node.html
.. _development sandbox: doc/development.rst
.. _DuckDB Python API: https://duckdb.org/docs/api/python/overview
.. _examples directory: https://github.com/earthobservations/phenodata/tree/main/examples
.. _immediate-reporters: https://www.dwd.de/DE/klimaumwelt/klimaueberwachung/phaenologie/daten_deutschland/sofortmelder/sofortmelder_node.html
.. _LICENSE: https://github.com/earthobservations/phenodata/blob/main/LICENSE
.. _Markdown: https://en.wikipedia.org/wiki/Markdown
.. _open data: https://en.wikipedia.org/wiki/Open_data
.. _open scientific data: https://en.wikipedia.org/wiki/Open_scientific_data
.. _pandas: https://pandas.pydata.org/
.. _presets.json: https://github.com/earthobservations/phenodata/blob/main/phenodata/dwd/presets.json
.. _reStructuredText: https://en.wikipedia.org/wiki/ReStructuredText
.. _share it back with us: https://github.com/earthobservations/phenodata/discussions/new?category=show-and-tell
.. _tabulate: https://github.com/astanin/python-tabulate
.. _virtualenv: https://github.com/earthobservations/phenodata/blob/main/doc/virtualenv.rst
.. _Xarray: https://xarray.dev/
