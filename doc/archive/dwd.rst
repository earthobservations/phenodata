.. _dwd-archive:

###########################
DWD SQLite database archive
###########################


*****
About
*****

This page contains information about `SQLite`_ database files produced by the
`phenodata`_ program and its ``export-observations-all`` subcommand.

Prior art
=========

`Jonas Dierenbach`_, `Franz-W. Badeck`_, and `Jörg Schaber`_ presented `PPODB`_,
the Plant-Phenological Online Database, that provides unrestricted and free access
to over 16 million plant phenological observations, mostly in Germany.

Its `PPODB SQL interface`_ offers online SQL access to the database, running on
premises of the `Institute for Theoretical Biophysics at the Humboldt University`_.

In the same spirit, we are producing and publishing `SQLite`_ database files about
the same matter, for everyone to run database queries on their own hardware.

.. seealso::

    In order to learn the important details about `PPODB`_, we recommend reading the
    `PPODB summary`_. More details can be discovered within the scientific paper
    `The plant phenological online database (PPODB) » an online database for long-term
    phenological data`_, and the `Plant-Phenological Online Database (PPODB) handbook`_.

Data source
===========
Data and metadata is acquired from the `DWD CDC Open Data Server`_, specifically
the ``observations_germany/phenology`` and ``help`` directories.

- https://opendata.dwd.de/climate_environment/CDC/observations_germany/phenology/
- https://opendata.dwd.de/climate_environment/CDC/help/

SQLite database files
=====================
The `data folder`_ contains four SQLite database files. Before downloading and
using them, please recognize the DWD data copyright notices referenced below at
:ref:`data-copyright`.

- ``phenodata-dwd-annual-historical.sqlite`` (1.7 GB)
- ``phenodata-dwd-annual-recent.sqlite`` (24 MB)
- ``phenodata-dwd-immediate-historical.sqlite`` (90 MB)
- ``phenodata-dwd-immediate-recent.sqlite`` (5.5 MB)


.. _dwd-archive-usage:

*****
Usage
*****

Getting started
===============

Let's start by defining the database name, and downloading the file.

.. code-block:: bash

    export DBPATH=phenodata-dwd-immediate-historical.sqlite
    wget --no-clobber "https://phenodata.hiveeyes.org/data/dwd/${DBPATH}"

Inquire the database schema.

.. code-block:: bash

    # Display all tables and views.
    sqlite3 "${DBPATH}" '.tables'

    # Display schema of all tables and views.
    sqlite3 "${DBPATH}" '.fullschema --indent'

    # Display database metadata information.
    sqlite3 "${DBPATH}" --header --csv 'SELECT * FROM dwd_about'

The database about historical observations from immediate reporters contains
~250,000 records as of 2023.

.. code-block:: bash

    sqlite3 "${DBPATH}" 'SELECT COUNT(*) FROM dwd_phenology;'
    252378

It spans the time range of observations between 1979 and 2021.

.. code-block:: bash

    sqlite3 "${DBPATH}" 'SELECT MIN(reference_year), MAX(reference_year) FROM dwd_phenology;'
    1979|2021

Run a query on the ``dwd_phenology`` view, with output in CSV format.

.. code-block:: bash

    sqlite3 -csv -header "${DBPATH}" 'SELECT * FROM dwd_phenology ORDER BY date;'

The same query, but more suitable when aiming to write your query using multiple
lines, for example within a program or script file.

.. code-block:: bash

    sqlite3 -csv -header "${DBPATH}" <<SQL
    SELECT * FROM dwd_phenology ORDER BY date;
    SQL


PPODB examples
==============

Those examples have been taken from the `PPODB SQL interface`_ page, and
slightly adjusted to use the DWD/Phenology/SQLite database schema.

.. highlight:: sql

To invoke those queries, start an interactive shell using ``sqlite3``::

    sqlite3 "${DBPATH}" --header --csv

At first, you usually want to get an overview over the database and list all
available tables::

    .tables

Often, you want to check whether a certain table contains the information you
are interested in. Therefore, you want to have a quick overlook over the columns
in the table of interest::

    .schema dwd_phase --indent

Stations and observations are uniquely referenced by identifiers. Therefore, it is
safer and more efficient to access phenological observations by their identifiers
rather than by names. The identifiers of all stations with a name similar to
"Geisenheim" can be retrieved with the query::

    SELECT station_id, station_full
    FROM dwd_phenology
    WHERE station_full LIKE '%Geisenheim%';

Within the database, a combination of plant and phase is referenced by a single
unique identifier, which is handy::

    SELECT *
    FROM dwd_phenology
    WHERE
        species_name_en LIKE '%hazel%' AND
        phase_name_en LIKE '%flowering%';

With a station-id and a phase-id, you can efficiently retrieve time series, e.g. flowering
of hazel at Geisenheim (DWD)::

    SELECT day_of_year, reference_year, source, species_name_en
    FROM dwd_phenology
    WHERE
        station_id=19476 AND
        species_id=113 AND
        phase_id=5
    ORDER BY reference_year, day_of_year;

Contrary to PPODB's recommendation, we think it is acceptable to use human-readable
labels for querying. If you will discover this to be a bottleneck for your application,
please consider adding additional indexes::

    SELECT day_of_year, reference_year, source, species_name_en
    FROM dwd_phenology
    WHERE
        station_full LIKE '%Geisenheim%' AND
        species_name_en LIKE '%hazel%' AND
        phase_name_en LIKE '%flowering%'
    ORDER BY reference_year, day_of_year;

You can also ask more complex questions, e.g. which of the following plants flowered
earliest after 1951 on average, hazelnut, chestnut or birch?::

    SELECT AVG(day_of_year) mean, reference_year, species_name_en plant, phase_name_en phase
    FROM dwd_phenology
    WHERE phase_name_en LIKE '%flowering%'
    GROUP BY phase_id ORDER BY mean;

or, e.g. how many single station time series are there that have a certain length including
all lengths and phases (see Figure 1 in the documentation)?::

    SELECT c, COUNT(c) FROM
        (
        SELECT station_id AS sid, phase_id AS pid, COUNT(DISTINCT reference_year) AS c
        FROM dwd_phenology
        WHERE phase_id != 0 GROUP BY station_id, phase_id
        )
    AS sq GROUP BY c;

Specialist's toolbox
====================

At `phenological calendar for foraging plants`_, we are discussing the development
of a convenient phenological calendar for beekeepers. Here, we are presenting
corresponding database queries suitable for that purpose.

In order to query the database for multiple plants conveniently, there is the
``dwd_species_group`` table, derived from phenodata's `presets.json`_ file.
The statement below uses the group ``mellifera-de-primary-openhive``, to list
all observations of "flowering" events for primary foraging plants of honeybees
(apis mellifera), filtering by location on behalf of the synthesized
``station_full`` field::

    SELECT
        reference_year,
        day_of_year,
        source,
        species_name_de,
        phase_name_de,
        station_name
    FROM dwd_phenology_group
    WHERE true
        AND group_name = 'mellifera-de-primary-openhive'
        AND phase_name_en LIKE '%flowering%'
        AND station_full LIKE '%brandenburg%';

In order to list the available plant group names, query the ``dwd_species_group``
table::

    SELECT
        dwd_species.*
    FROM dwd_species_group, dwd_species
    WHERE true
        AND dwd_species_group.species_id=dwd_species.id
        AND group_name='mellifera-de-primary-openhive';

::

    205,Winterraps,"winter oilseed rape","Brassica napus var. napus"
    209,Sonnenblume,sunflower,"Helianthus annuus"
    215,Mais,maize,"Zea mays"
    310,Apfel,apple,"Malus domestica"
    320,Birne,pear,"Pyrus communis"
    330,"Süßkirsche",cherry,"Prunus avium"
    340,Sauerkirsche,morello,"Prunus cerasus"
    382,Himbeere,raspberry,"Rubus idaeus"
    383,Brombeere,blackberry,"Rubus fructicosus"
    113,Hasel,"common hazel","Corylus avellana"
    114,Heidekraut,"common heather","Calluna vulgaris"
    120,"Löwenzahn",dandelion,"Taraxacum officinale"
    121,Robinie,"black locust","Robinia pseudoacacia"
    122,Rosskastanie,"horse chestnut","Aesculus hippocastanum"
    124,Sal-Weide,"goat willow","Salix caprea"
    131,Spitz-Ahorn,"Norway maple","Acer platanoides"
    137,Winter-Linde,"small leafed lime","Tilia cordata"

.. note::

    If you have a different use case, or think the existing species groups should be
    expanded, do not hesitate to drop us a line by `creating an issue`_, in order to
    propose changes to the ``dwd_species_group`` table.


************
Attributions
************

.. _data-copyright:

Data copyright
==============

    All information on the web pages of the DWD is protected by copyright.
    As laid down in the Ordinance Setting the Terms of Use for the Provision of
    Federal Spatial Data (GeoNutzV), all spatial data and spatial data services
    available "for free" access may be used without any restrictions provided that
    the source is acknowledged. When speaking of spatial data, this also includes
    any location-related weather and climate information presented on the DWD open
    web pages.

    Any other content presented on DWD web pages, in whole or extracts thereof, may
    be reproduced, altered, distributed, used or publicly presented only if expressly
    permitted by the DWD.

.. image:: https://www.dwd.de/SharedDocs/bilder/DE/logos/dwd/dwd_logo_258x69.png?__blob=normal&v=1

| Source: Deutscher Wetterdienst (DWD)
| Copyright information: `en <copyright-en_>`_, `de <copyright-de_>`_
| GeoNutzV: `en <GeoNutzV (en)_>`_, `de <GeoNutzV (de)_>`_

Acknowledgements
================

Thanks to the many observers of »Deutscher Wetterdienst« (DWD), the »Global
Phenological Monitoring programme« (GPM), and all people working behind the
scenes for their commitment on recording observations and making the excellent
datasets available to the community. You know who you are.


*********
Reproduce
*********

This section explains how to export all available datasets into corresponding
`SQLite`_ database files, on your own machine, using the ``export-observations-all``
subcommand.

The process will take about five to ten minutes, based on the capacity of your
computing device. Processing the immediate/historical+recent and annual/recent
data is pretty fast. The annual/historical data however, as the largest one
with a size of ~1.7 GB, takes the major share of computing time on the export
operation.

.. code-block:: python

    phenodata export-observations-all --source=dwd

The command will create four SQLite database files, they can be :ref:`consumed
<sqlite-usage-consume>` using the ``sqlite3`` command, or other tools.

.. tip::

    If you want to create database files by selecting individual subsets of the
    data, please refer to the :ref:`sqlite-export` documentation.

.. note::

    The cache directory, for example located at ``/Users/<username>/Library/Caches/phenodata``
    on macOS machines, will hold all the data downloaded from DWD servers. It is about
    160 MB in size for both of the "recent" datasets, while ``immediate-historical``
    weighs in with about 500 MB, and ``annual-historical`` with about another 3 GB.

Upload
======
::

    rsync -azuv phenodata-dwd-*.sqlite root@elbanco.hiveeyes.org:/var/lib/phenodata/dwd


*******
Backlog
*******

.. todo::

    - [o] Publish using `datasette`_
    - [o] Publish using `Grafana SQLite Datasource`_
    - [o] Outline other end-user tools to consume the databases
    - [o] Implement ``phenodata.open_database("dwd", "immediate", "recent")``
      to consume the databases
    - [o] Acknowledge PPODB
    - [o] Add a few SQL query examples


----

Enjoy your research.


.. _copyright-de: https://www.dwd.de/DE/service/copyright/copyright_node.html
.. _copyright-en: https://www.dwd.de/EN/service/copyright/copyright_node.html
.. _creating an issue: https://github.com/earthobservations/phenodata/issues
.. _data folder: https://phenodata.hiveeyes.org/data/
.. _datasette: https://datasette.io/
.. _DWD CDC Open Data Server: https://www.dwd.de/EN/ourservices/opendata/opendata.html
.. _Franz-W. Badeck: https://badeck.eu/
.. _GeoNutzV (de): https://www.gesetze-im-internet.de/geonutzv/GeoNutzV.pdf
.. _GeoNutzV (en): https://www.bmuv.de/fileadmin/Daten_BMU/Download_PDF/Strategien_Bilanzen_Gesetze/130309_geonutzv_bgbi_englisch_bf.pdf
.. _Grafana SQLite Datasource: https://grafana.com/grafana/plugins/frser-sqlite-datasource/
.. _Institute for Theoretical Biophysics at the Humboldt University: https://rumo.biologie.hu-berlin.de/
.. _Jonas Dierenbach: https://www.researchgate.net/scientific-contributions/Jonas-Dierenbach-2007294130
.. _Jörg Schaber: https://fairdomhub.org/people/445
.. _phenodata: https://phenodata.readthedocs.io/
.. _phenological calendar for foraging plants: https://community.hiveeyes.org/t/phanologischer-kalender-fur-trachtpflanzen/664
.. _Plant-Phenological Online Database (PPODB) handbook: https://rumo.biologie.hu-berlin.de/PPODB/static/documentation/DescriptionPPODB.pdf
.. _PPODB: https://rumo.biologie.hu-berlin.de/PPODB/
.. _PPODB SQL interface: https://rumo.biologie.hu-berlin.de/PPODB/database/sql_input
.. _PPODB summary: https://community.hiveeyes.org/t/plant-phenological-online-database-ppodb/4888
.. _presets.json: https://github.com/earthobservations/phenodata/blob/main/phenodata/dwd/presets.json
.. _SQLite: https://sqlite.org/
.. _The plant phenological online database (PPODB) » an online database for long-term phenological data: https://link.springer.com/article/10.1007/s00484-013-0650-2
