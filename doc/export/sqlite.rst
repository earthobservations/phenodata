.. _sqlite-export:

######################
SQLite database export
######################


*****
About
*****

You can use the ``phenodata export-observations`` subcommand to export observations
including metadata into an `SQLite`_ database.

The database will contain the data table ``dwd_observation``, and the metadata
tables ``dwd_station``, ``dwd_species``, ``dwd_phase``, ``dwd_quality_byte``,
and ``dwd_quality_level``. There is also a `database view`_ called ``dwd_phenology``,
which will join those tables together properly, and present a `denormalized`_ variant
of the data, ready for convenient querying.

If you want to create SQLite database archive files, containing **all datasets**,
or just download and use them, please follow up reading the :ref:`dwd-archive`
documentation section.


.. _sqlite-usage:

*****
Usage
*****

.. _sqlite-usage-produce:

Produce
=======

This example walks you through the steps needed to store a subset of the phenology
observation data available on DWD CDC into an SQLite database file on your machine.

Let's start by defining the database name.

.. code-block:: bash

    export DBPATH=phenodata-dwd-annual-recent-hasel.sqlite

Now, export a few selected data points to keep the database size small.

.. code-block:: bash

    phenodata export-observations \
        --source=dwd --dataset=annual --partition=recent \
        --station=münchen \
        --year=2021,2022,2023 \
        --filename=Hasel \
        --target=sqlite:///${DBPATH}

.. attention::

    Please note that each invocation will **overwrite (replace)** all tables
    within the given database without confirmation.


.. _sqlite-usage-consume:

Consume
=======

Inquire the database schema.

.. code-block:: bash

    # Show all tables and views.
    sqlite3 "${DBPATH}" '.tables'

    # Show schema of all tables and views.
    sqlite3 "${DBPATH}" '.fullschema --indent'

Run a query on the ``dwd_phenology`` view.

.. code-block:: bash

    sqlite3 -csv -header "${DBPATH}" 'SELECT * FROM dwd_phenology ORDER BY date;'

.. code-block:: bash

    sqlite3 -csv -header "${DBPATH}" <<SQL
    SELECT * FROM dwd_phenology ORDER BY date;
    SQL

.. seealso::

    For more example SQL statements, see also :ref:`SQLite DWD archive usage
    <dwd-archive-usage>`.


*******
Details
*******

You can always inspect the database schema using ``sqlite3 "${DBPATH}" '.fullschema
--indent'``. In order to learn about how the ``dwd_phenology`` `database view`_
looks like, this SQL example can be helpful.

.. code-block:: sql

    sqlite3 -csv -header "${DBPATH}" <<SQL
    SELECT
       dwd_observation.*,
       dwd_station.*,
       dwd_station.station_name AS station_name,
       dwd_species.species_name_en AS species_name,
       dwd_phase.phase_name_en AS phase_name
    FROM
       dwd_observation, dwd_station, dwd_species, dwd_phase
    WHERE true
       AND dwd_observation.station_id=dwd_station.id
       AND dwd_observation.species_id=dwd_species.id
       AND dwd_observation.phase_id=dwd_phase.id
    SQL

.. note::

    Please note this SQL example omits joining in the ``dwd_quality_byte``
    and ``dwd_quality_level`` tables for better readability. The view
    ``dwd_phenology`` *does* include them.


*******
Backlog
*******

.. todo::

    - [o] Add ``copyright`` table, including corresponding information from DWD
    - [o] Insert and query ``presets`` table
    - [o] How to publish using `datasette`_
    - [o] How to publish using `Grafana SQLite Datasource`_
    - [o] Explore compression options

      - https://stackoverflow.com/questions/10824347/does-sqlite3-compress-data
      - https://phiresky.github.io/blog/2022/sqlite-zstd/
      - https://hackaday.com/2022/08/01/never-too-rich-or-thin-compress-sqlite-80/
      - https://github.com/phiresky/sqlite-zstd


.. _database view: https://en.wikipedia.org/wiki/View_(SQL)
.. _datasette: https://datasette.io/
.. _denormalized: https://en.wikipedia.org/wiki/Denormalization
.. _Grafana SQLite Datasource: https://grafana.com/grafana/plugins/frser-sqlite-datasource/
.. _SQLite: https://sqlite.org/
