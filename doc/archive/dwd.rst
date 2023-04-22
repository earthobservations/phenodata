.. _dwd-archive:

###########################
DWD SQLite database archive
###########################


*****
About
*****

This section explains how to export all available datasets into corresponding `SQLite`_
database files, using the ``phenodata export-observations-all`` subcommand.

If you want to create database files by selecting individual subsets of the data,
please refer to the :ref:`sqlite-export` documentation.


*******
Archive
*******

The SQLite database files produced by phenodata can be downloaded at
https://phenodata.hiveeyes.org/. Please recognize the DWD data copyright
notices referenced below.


*****
Usage
*****

.. code-block:: python

    phenodata export-observations-all

The command will create four SQLite database files, they can be :ref:`consumed
<sqlite-usage-consume>` using the ``sqlite3`` command, or other tools.

- ``phenodata-dwd-annual-historical.sqlite`` (1.7 GB)
- ``phenodata-dwd-annual-recent.sqlite`` (24 MB)
- ``phenodata-dwd-immediate-historical.sqlite`` (90 MB)
- ``phenodata-dwd-immediate-recent.sqlite`` (5.5 MB)

.. note::

    The cache directory, for example located at ``/Users/<username>/Library/Caches/phenodata``
    on macOS machines, will hold all the data downloaded from DWD servers. It is about
    160 MB in size for both of the "recent" datasets, while ``immediate-historical``
    weighs in with about 500 MB, and ``annual-historical`` with about 3 GB.


************
Attributions
************

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


.. _copyright-de: https://www.dwd.de/DE/service/copyright/copyright_node.html
.. _copyright-en: https://www.dwd.de/EN/service/copyright/copyright_node.html
.. _datasette: https://datasette.io/
.. _GeoNutzV (de): https://www.gesetze-im-internet.de/geonutzv/GeoNutzV.pdf
.. _GeoNutzV (en): https://www.bmuv.de/fileadmin/Daten_BMU/Download_PDF/Strategien_Bilanzen_Gesetze/130309_geonutzv_bgbi_englisch_bf.pdf
.. _Grafana SQLite Datasource: https://grafana.com/grafana/plugins/frser-sqlite-datasource/
.. _SQLite: https://sqlite.org/
