.. highlight:: sql

.. _ppodb:

##################################
Plant-Phenological Online Database
##################################


*****
About
*****
- http://www.phenology.de/
- https://rumo.biologie.hu-berlin.de/PPODB/

The plant phenological online database (PPODB):
an online database for long-term phenological data.


*******
Details
*******
- https://rumo.biologie.hu-berlin.de/PPODB/static/documentation/DescriptionPPODB.pdf
- https://www.researchgate.net/publication/236064456_The_plant_phenological_online_database_PPODB_An_online_database_for_long-term_phenological_data
- https://link.springer.com/article/10.1007/s00484-013-0650-2
- https://www.researchgate.net/publication/274832244_An_overview_of_the_phenological_observation_network_and_the_phenological_database_of_Germany's_national_meteorological_service_Deutscher_Wetterdienst
- https://www.researchgate.net/publication/226311858_Combining_Messy_Phenological_Time_Series
- https://cloud.r-project.org/web/packages/pheno/
- https://cloud.r-project.org/web/packages/pheno/pheno.pdf
- https://github.com/jzumer/pytwed/blob/master/pytwed/twed.c
- https://github.com/garrettwrong/cuTWED/blob/master/reference_implementation/twed.c


***
API
***
- https://rumo.biologie.hu-berlin.de/PPODB/database/sql_input


SQL example queries
===================

At first, you usually want to get an overview over the database and list all
available tables::

    SHOW TABLES;

Often, you want to check whether a certain table contains the information you
are interested in. Therefore, you want to have a quick overlook over the
columns in the table of interest::

    DESCRIBE agro_pheno_def;

Stations and observations are uniquely referenced to by identifiers. Therefore,
it is safer and more efficient to access phenological observations by their
identifiers rather than by names.

The identifiers of all stations with a name similar to "Geisenheim" can be
retrieved with the query::

    SELECT stat_id, stat_name
    FROM pheno_stations
    WHERE stat_name LIKE '%Geisenheim%';

In the DWD- and HIS-databases, a combination of plant and phase is referenced
by a single unique identifier, which is handy::

    SELECT *
    FROM dwd_pheno_def
    WHERE plant_name_en LIKE '%chestnut%' AND phase_name_en LIKE '%flowering%';

With a station-id and a phase-id, we can efficiently retrieve time series, e.g.
flowering of chestnut at Geisenheim (DWD)::

    SELECT obs_day, obs_year, source_db
    FROM all_pheno_obs
    WHERE stat_id=2430 AND phase_id=8;

We can also ask more complex questions, e.g. which of the following plants
flowered earliest after 1951 on average, hazelnut, chestnut or birch::

    SELECT AVG(obs_day) mean, b.plant_name_en plant, b.phase_name_en phase
    FROM dwd_pheno_obs a, dwd_pheno_def b
    WHERE a.phase_id=b.phase_id AND a.phase_id IN (1,8,220)
    GROUP BY a.phase_id
    ORDER BY mean;

or, e.g. how many single station time series are there that have a certain
length including all lengths and phases (see Figure 1 in the documentation)::

    SELECT c, COUNT(c)
    FROM (
        SELECT stat_id AS sid, phase_id AS pid, COUNT(distinct obs_year) AS c
        FROM all_pheno_obs
        WHERE phase_id != 0
        GROUP BY stat_id,phase_id
    )
    AS sq GROUP BY c;


****
More
****

- https://cran.r-project.org/web/packages/phenex/
- https://cran.r-project.org/web/packages/phenmod/
- https://cran.r-project.org/web/packages/phenmod/phenmod.pdf
- https://www.ufz.de/index.php?en=37615
