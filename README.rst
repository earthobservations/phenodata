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

Introduction
============
For most acquisition tasks, you must choose from one of two different datasets: `annual-reporters`_ and `immediate-reporters`_.

To improve data acquisition performance, also consider applying
the ``--filename=`` parameter for file name filtering.

Example: When using ``--filename=Hasel,Schneegloeckchen``, only file names containing
``Hasel`` or ``Schneegloeckchen`` will be retrieved, thus minimizing the required effort
to acquire all files.

.. _annual-reporters: https://www.dwd.de/DE/klimaumwelt/klimaueberwachung/phaenologie/daten_deutschland/jahresmelder/jahresmelder_node.html
.. _immediate-reporters: https://www.dwd.de/DE/klimaumwelt/klimaueberwachung/phaenologie/daten_deutschland/sofortmelder/sofortmelder_node.html


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
      phenodata list-stations --source=dwd --dataset=immediate [--all] [--format=csv]
      phenodata nearest-station --source=dwd --dataset=immediate --latitude=52.520007 --longitude=13.404954 [--format=csv]
      phenodata nearest-stations --source=dwd --dataset=immediate [--all] --latitude=52.520007 --longitude=13.404954 [--limit=10] [--format=csv]
      phenodata list-quality-levels --source=dwd [--format=csv]
      phenodata list-quality-bytes --source=dwd [--format=csv]
      phenodata list-filenames --source=dwd --dataset=immediate --partition=recent [--filename=Hasel,Schneegloeckchen] [--year=2017]
      phenodata list-urls --source=dwd --dataset=immediate --partition=recent [--filename=Hasel,Schneegloeckchen] [--year=2017]
      phenodata (observations|forecast) --source=dwd --dataset=immediate --partition=recent [--filename=Hasel,Schneegloeckchen] [--station-id=164,717] [--species-id=113,127] [--phase-id=5] [--quality-level=10] [--quality-byte=1,2,3] [--station=berlin,brandenburg] [--species=hazel,snowdrop] [--species-preset=mellifera-primary] [--phase=flowering] [--quality=ROUTKLI] [--year=2017] [--humanize] [--show-ids] [--language=german] [--long-station] [--sort=Datum] [--format=csv]
      phenodata drop-cache --source=dwd
      phenodata --version
      phenodata (-h | --help)

    Data acquisition options:
      --source=<source>         Data source. Currently "dwd" only.
      --dataset=<dataset>       Data set. Use "immediate" or "annual" for --source=dwd.
      --partition=<dataset>     Partition. Use "recent" or "historical" for --source=dwd.
      --filename=<file>         Filter by file names (comma-separated list)

    Direct filtering options:
      --years=<years>           Filter by years (comma-separated list)
      --station-id=<station-id> Filter by station ids (comma-separated list)
      --species-id=<species-id> Filter by species ids (comma-separated list)
      --phase-id=<phase-id>     Filter by phase ids (comma-separated list)

    Humanized filtering options:
      --station=<station>       Filter by strings from "stations" data (comma-separated list)
      --species=<species>       Filter by strings from "species" data (comma-separated list)
      --phase=<phase>           Filter by strings from "phases" data (comma-separated list)
      --species-preset=<preset> Filter by strings from "species" data (comma-separated list) loaded from ``presets.json`` file

    Data output options:
      --format=<format>         Output data in designated format. Choose one of "tabular", "json", "csv" or "string".
                                With "tabular", it is also possible to specify the table format,
                                see https://bitbucket.org/astanin/python-tabulate. e.g. "tabular:presto".
                                [default: tabular:psql]
      --sort=<sort>             Sort by given column names (comma-separated list)
      --humanize                Resolve ID-based columns to real names with "observations" and "forecast" output.
      --show-ids                Show IDs alongside resolved text representation when using ``--humanize``.
      --language=<language>     Use labels in designated language when using ``--humanize`` [default: english].
      --long-station            Use long station name including "Naturraumgruppe" and "Naturraum".
      --limit=<limit>           Limit output of "nearest-stations" to designated number of entries.
                                [default: 10]

----

**************
Output example
**************

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

----


*******************
Invocation examples
*******************


Metadata
========

List of species::

    phenodata list-species --source=dwd

List of phases::

    phenodata list-phases --source=dwd

List of stations::

    phenodata list-stations --source=dwd --dataset=immediate

List of file names of recent observations by the annual reporters::

    phenodata list-filenames --source=dwd --dataset=annual --partition=recent

List of full URLs to observations using filename-based filtering::

    phenodata list-urls --source=dwd --dataset=annual --partition=recent --filename=Hasel,Schneegloeckchen

Display nearest station for given position::

    phenodata nearest-station --source=dwd --dataset=immediate --latitude=52.520007 --longitude=13.404954

Display 20 nearest stations for given position::

    phenodata nearest-stations \
        --source=dwd --dataset=immediate \
        --latitude=52.520007 --longitude=13.404954 --limit=20


Observations
============

Observations of hazel and snowdrop, using filename-based filtering at data acquisition time::

    phenodata observations --source=dwd --dataset=annual --partition=recent --filename=Hasel,Schneegloeckchen

Observations of hazel and snowdrop (dito), but for station ids 164 and 717 only::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel,Schneegloeckchen --station-id=164,717

All observations for station ids 164 and 717 in years 2016 and 2017::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --station-id=164,717 --year=2016,2017

All observations for station ids 164 and 717 and species ids 113 and 127::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --station-id=164,717 --species-id=113,127

All invalid observations::

    phenodata list-quality-bytes --source=dwd
    phenodata observations --source=dwd --dataset=annual --partition=recent --quality-byte=5,6,7,8


Forecasting
===========
Acquire data from observations in Berlin-Dahlem and München-Pasing and forecast to current year
using grouping and by computing the "mean" value of the "Jultag" column::

    phenodata forecast \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel,Schneegloeckchen,Apfel,Birne \
        --station-id=12132,10961 --format=string



*************************
Humanized output examples
*************************
The option ``--humanize`` will improve textual output by resolving ID columns
in the observation data to their appropriate text representions from metadata files.

Observations
============
Observations for species "hazel", "snowdrop", "apple" and "pear" at station "Berlin-Dahlem",
output texts in the German language if possible::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel,Schneegloeckchen,Apfel,Birne \
        --station-id=12132 \
        --humanize --language=german


Forecasting
===========

Specific events
---------------
Forecast of "beginning of flowering" events at station "Berlin-Dahlem".
Use all species of the "primary group": "hazel", "snowdrop", "goat willow",
"dandelion", "cherry", "apple", "winter oilseed rape", "black locust" and "common heather".
Sort by date, ascending.
::

    phenodata forecast \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel,Schneegloeckchen,Sal-Weide,Loewenzahn,Suesskirsche,Apfel,Winterraps,Robinie,Winter-Linde,Heidekraut \
        --station-id=12132 --phase-id=5 \
        --humanize \
        --sort=Datum \
        --format=tabular:rst

Event sequence for each species
-------------------------------
Forecast of all events at station "Berlin-Dahlem".
Use all species of the "primary group" (dito).
Sort by species and date, ascending.
::

    phenodata forecast \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel,Schneegloeckchen,Sal-Weide,Loewenzahn,Suesskirsche,Apfel,Winterraps,Robinie,Winter-Linde,Heidekraut \
        --station-id=12132 \
        --humanize --language=german \
        --sort=Spezies,Datum


*************************
Humanized search examples
*************************

Observations
============
Query observations by using textual representation of "station" information::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel,Schneegloeckchen \
        --station=berlin,brandenburg \
        --humanize --sort=Datum

Observations near Munich for species "hazel" or "snowdrop" in 2018::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --station=münchen \
        --species=hazel,snowdrop \
        --year=2018 \
        --humanize --sort=Datum

Observations for any "flowering" events in 2017 and 2018 around Munich::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --station=münchen \
        --phase=flowering \
        --year=2017,2018 \
        --humanize --sort=Datum

Same observations but with "ROUTKLI" quality::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --station=münchen \
        --phase=flowering \
        --quality=ROUTKLI \
        --year=2017 \
        --humanize --sort=Datum

Investigate some "flowering" observations near Munich which have seen corrections last year::

    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --station=münchen \
        --phase=flowering \
        --quality=korrigiert \
        --year=2017 \
        --humanize --sort=Datum


Forecasting
===========
Forecast based on "beginning of flowering" events of 2015-2017 in Thüringen and Bayern for the given list of species.
Sort by species and date.
::

    phenodata forecast \
        --source=dwd --dataset=annual --partition=recent \
        --station=thüringen,bayern \
        --species=Hasel,Schneeglöckchen,Sal-Weide,Löwenzahn,Süßkirsche,Apfel,Winterraps,Robinie,Winter-Linde,Heidekraut \
        --phase-id=5 \
        --year=2015,2016,2017 \
        --humanize --language=german \
        --sort=Spezies,Datum

Forecast based on "beginning of flowering" events of 2015-2017 in Berlin for the named list of species "mellifera-de-primary".
Sort by date.
::

    phenodata forecast \
        --source=dwd --dataset=annual --partition=recent \
        --station=köln \
        --phase="beginning of flowering" \
        --year=2015,2016,2017 \
        --humanize --language=german \
        --sort=Datum \
        --species-preset=mellifera-de-primary

.. note::

    The species presets like ``mellifera-de-primary`` and others are currently stored in
    `presets.json <https://github.com/hiveeyes/phenodata/blob/master/phenodata/dwd/presets.json>`__.


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
