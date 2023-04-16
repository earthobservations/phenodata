#########
Forecasts
#########


*****
About
*****

For computing "forecasts", phenodata implements a naive approach, which should
be taken with a grain of salt. The computation is based on the ``Jultag`` field
from observation data of the previous years.

Details
=======

The implementation can be found in ``phenodata.dwd.pheno.DwdPhenoDataClient.get_forecast``,
and looks roughly like this:

.. code-block:: python

    # Get current observations.
    observations = self.get_observations()

    # Group by station, species and phase.
    # https://pandas.pydata.org/pandas-docs/stable/groupby.html
    grouped = observations.groupby(["Stations_id", "Objekt_id", "Phase_id"])

    # Aggregate mean "day of the year" value of the "Jultag" values for each group.
    forecast = grouped["Jultag"].mean().round().astype(int).to_frame()



*****
Usage
*****

Let's outline a few invocations by example.

Basic
=====
Acquire observation data from annual reporters in "Berlin-Dahlem" and
"München-Pasing" for certain species, and forecast them to the current
year using grouping and by computing the "mean" value of the ``Jultag``
field. Sort result by ``Station``, ``Datum``, and ``Spezies``::

    phenodata forecast \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel,Schneegloeckchen,Apfel,Birne \
        --humanize --station=dahlem,pasing --sort=Station,Datum,Spezies


Humanized output
================

Specific events
---------------

Forecast of "beginning of flowering" observations at station "Berlin-Dahlem".
Use all species of the "primary group": "hazel", "snowdrop", "goat willow",
"dandelion", "cherry", "apple", "winter oilseed rape", "black locust", and
"common heather". Sort by date, ascending. Rendered in reStructuredText
table format::

    phenodata forecast \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel,Schneegloeckchen,Sal-Weide,Loewenzahn,Suesskirsche,Apfel,Winterraps,Robinie,Winter-Linde,Heidekraut \
        --station=dahlem --phase="beginning of flowering" \
        --humanize \
        --sort=Datum \
        --format=tabular:rst

Event sequence for each species
-------------------------------

Forecast of all observation types at station "Berlin-Dahlem", using all species
of the "primary group" (dito). Sort by species and date, ascending. Display
labels in German language::

    phenodata forecast \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel,Schneegloeckchen,Sal-Weide,Loewenzahn,Suesskirsche,Apfel,Winterraps,Robinie,Winter-Linde,Heidekraut \
        --station=dahlem \
        --humanize --language=german \
        --sort=Spezies,Datum


Humanized search
================

Forecast based on "beginning of flowering" observations of 2021-2023 in
Thüringen and Bayern for the given list of species. Sort by species and date::

    phenodata forecast \
        --source=dwd --dataset=annual --partition=recent \
        --phase="beginning of flowering" \
        --year=2021,2022,2023 \
        --station=thüringen,bayern \
        --species=Hasel,Schneeglöckchen,Sal-Weide,Löwenzahn,Süßkirsche,Apfel,Winterraps,Robinie,Winter-Linde,Heidekraut \
        --sort=Spezies,Datum \
        --humanize --language=german

Forecast based on "beginning of flowering" observations of 2021-2023 in Köln
for the named list of species ``mellifera-de-primary``. Sort by date::

    phenodata forecast \
        --source=dwd --dataset=annual --partition=recent \
        --station=köln \
        --phase="beginning of flowering" \
        --year=2021,2022,2023 \
        --humanize --language=german \
        --sort=Datum \
        --species-preset=mellifera-de-primary

