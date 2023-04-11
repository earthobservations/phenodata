# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
from __future__ import print_function
import attr
import json
import logging
import pandas as pd
import pkg_resources
from datetime import datetime
from phenodata.util import haversine_distance, iterate_with_progressbar

logger = logging.getLogger(__name__)


@attr.s
class DwdPhenoData:
    """
    Conveniently access phenology information from the Climate Data Center (CDC)
    FTP server operated by »Deutscher Wetterdienst« (DWD).

    See also `cdc-readme`_:
    Phenological data is collected at about 1200 active stations. The state of development of
    selected plants (e.g., apple, birch, snow drops, goose berry, wheat, vine, etc.) is reported
    by annual reporters and immediate reporters.

    The lists of phenological stations can be found in the list of phenology `annual reporters`_
    and the list of phenology `immediate reporters`_.

    .. _cdc-readme: ftp://opendata.dwd.de/climate_environment/CDC/Readme_intro_CDC_ftp.txt
    .. _annual reporters: ftp://opendata.dwd.de/climate_environment/CDC/help/PH_Beschreibung_Phaenologie_Stationen_Jahresmelder.txt
    .. _immediate reporters: ftp://opendata.dwd.de/climate_environment/CDC/help/PH_Beschreibung_Phaenologie_Stationen_Sofortmelder.txt

    """

    # Instance of the lowlevel DWD CDC FTP server client wrapper object ``phenodata.dwd.cdc.DwdCdcClient``
    cdc = attr.ib()

    # Instance of ``phenodata.dwd.pheno.DwdPhenoDataHumanizer``
    humanizer = attr.ib()

    # The dataset to access, either "annual" or "immediate"
    dataset = attr.ib()

    @property
    def data_directory(self):
        """
        Location of observations on the FTP server
        """
        return '/observations_germany/phenology/{dataset}_reporters'.format(dataset=self.dataset)

    def get_species(self):
        """
        Return DataFrame with species information
        """
        return self.cdc.get_dataframe(path='/help/PH_Beschreibung_Pflanze.txt', index_column=0)

    def get_phases(self):
        """
        Return DataFrame with phases information
        """
        return self.cdc.get_dataframe(path='/help/PH_Beschreibung_Phase.txt', index_column=0)

    def get_quality_levels(self):
        """
        Return DataFrame with quality level information
        """
        return self.cdc.get_dataframe(path='/help/PH_Beschreibung_Phaenologie_Qualitaetsniveau.txt', index_column=0)

    def get_quality_bytes(self):
        """
        Return DataFrame with quality bytes information
        ftp://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/standard_format/qualitaetsbytes.pdf
        """
        return self.cdc.get_dataframe(path='/help/PH_Beschreibung_Phaenologie_Qualitaetsbyte.txt', index_column=0)

    def get_stations(self, filter=None, all=False):
        """
        Return DataFrame with stations information.
        """

        if self.dataset == 'immediate':
            filename = '/help/PH_Beschreibung_Phaenologie_Stationen_Sofortmelder.txt'
        elif self.dataset == 'annual':
            filename = '/help/PH_Beschreibung_Phaenologie_Stationen_Jahresmelder.txt'
        else:
            raise KeyError('Unknown dataset "{}"'.format(self.dataset))

        # Read stations CSV file
        data = self.cdc.get_dataframe(path=filename, index_column=0)

        # Unless "all==True", use only rows with "Datum Stationsaufloesung" == nan
        if not all:
            data = data[data['Datum Stationsaufloesung'].isna()]

        # Appropriately coerce geolocation values to float
        #dataframe_coerce_columns(data, ['geograph.Breite', 'geograph.Laenge'], float)

        # A. Basic filtering

        if filter:
            # Build "boolean indexing" filter expression from multiple ID-based criteria
            # https://pandas.pydata.org/pandas-docs/stable/indexing.html#boolean-indexing
            reference_fields = [
                'Stationsname',
                'Naturraumgruppe',
                'Naturraum',
                'Bundesland',
            ]

            expression = False
            for reference_field in reference_fields:
                #print(reference_field, filter)
                expression |= data[reference_field].str.contains(filter, case=False)

            # Apply filter expression to DataFrame
            if type(expression) is not bool:
                data = data[expression]

        return data

    def nearest_station(self, latitude, longitude, all=False):
        """
        Select closest station.
        """
        return self.nearest_stations(latitude, longitude, all=all).head(1)

    def nearest_stations(self, latitude, longitude, all=False, limit=10):
        """
        Select closest stations.

        Stolen from https://github.com/marians/dwd-weather
        """

        # Retrieve stations
        stations = self.get_stations(all=all)

        # Build list of distances to corresponding station
        distances = []
        for index, station in stations.iterrows():
            distance = haversine_distance(
                (longitude, latitude),
                (station['geograph.Laenge'], station['geograph.Breite'])
            )
            distances.append(distance)

        # Insert list of distances as new column
        stations.insert(1, 'Distanz', distances)

        # Sort ascending by distance value and limit row count
        stations = stations.sort_values('Distanz').head(n=limit)

        # Convert Series to DataFrame again
        frame = pd.DataFrame(stations)

        return frame

    def get_observations(self, options, humanize=False):
        """
        Retrieve observations.

        - Obtain query options
        - Compute DataFrame with combined observation data
        - Apply a bunch of filters to the result data
        """

        # Acquire data
        observations = self.query(partition=options['partition'], files=options.get('filename'))

        # Sanity checks
        if observations is None:
            return

        # Filter data
        observations = self.flux(observations, criteria=options)

        # Sanity checks
        if observations is None:
            logger.warning('No results found')
            return

        # Optionally humanize DataFrame
        if humanize:
            megaframe = self.create_megaframe(observations)
            observations = self.humanizer.get_observations(megaframe)

        # or pass-through with minor cosmetic amendments
        else:
            observations['Eintrittsdatum'] = observations['Eintrittsdatum'].astype(str)

        return observations

    def get_forecast(self, options, forecast_year=None, humanize=False):
        """
        Forecast observations.

        - Obtain query options
        - Get real observations, all filtering options can be used
        - Group results by (Stations_id, Objekt_id, Phase_id)
        - Aggregate mean "day of the year" value of the "Jultag" values for each group
        """

        # Compute target year.
        target_year = datetime.today().year
        if forecast_year is not None:
            target_year = datetime.strptime(str(forecast_year), "%Y").year

        # Get current observations
        observations = self.get_observations(options)

        # Sanity checks
        if observations is None:
            return

        # Group by station, species and phase
        # https://pandas.pydata.org/pandas-docs/stable/groupby.html
        grouped = observations.groupby(['Stations_id', 'Objekt_id', 'Phase_id'])

        # Aggregate mean "day of the year" value of the "Jultag" values for each group
        series = grouped['Jultag'].mean().round().astype(int)

        # Convert Series to DataFrame
        forecast = series.to_frame()


        # Compute ISO date from "day of the year" values and insert as new column
        real_dates = pd.to_datetime(target_year * 1000 + forecast['Jultag'], errors='coerce', format='%Y%j')
        forecast.insert(0, 'Datum', real_dates)

        # Resolve index column to real columns
        station_ids = []
        species_ids = []
        phase_ids = []
        for index, row in forecast.iterrows():
            # Decode index column and collect its components
            station_id, species_id, phase_id = index
            station_ids.append(station_id)
            species_ids.append(species_id)
            phase_ids.append(phase_id)

        forecast['Stations_id'], forecast['Objekt_id'], forecast['Phase_id'] = station_ids, species_ids, phase_ids


        # Optionally humanize DataFrame
        if humanize:
            megaframe = self.create_megaframe(forecast, drop_index_columns=True)
            forecast = self.humanizer.get_forecast(megaframe, target_year=target_year)

        # or pass-through with minor cosmetic amendments
        else:
            forecast['Datum'] = forecast['Datum'].astype(str)

        return forecast

    def query(self, partition=None, files=None):
        """
        The FTP/pandas workhorse, converges data from multiple observation data
        CSV files on upstream CDC FTP server into a single pandas DataFrame object.

        - Obtains ``partition`` parameter which can be either ``annual`` or ``immediate``.
        - Obtains optional ``files`` parameter which will be applied
          as an "include" filter to the list of scanned file names.
        """

        logger.info('Scanning for files')

        # Search FTP server
        paths = self.scan_files(partition, include=files, field='url')

        logger.info('Starting data acquisition with {} files'.format(len(paths)))

        # The main DataFrame object
        results = pd.DataFrame()

        # Load multiple files into single DataFrame
        for path in iterate_with_progressbar(paths):

            logger.debug('Processing file "{}"'.format(path))

            # Acquire DataFrame from CSV data
            data = self.cdc.get_dataframe(path, coerce_int=True)

            # Sanity checks
            if data is None:
                logger.warning('File "{}" is empty')
                continue

            # Coerce "Eintrittsdatum" column into date format
            data['Eintrittsdatum'] = pd.to_datetime(data['Eintrittsdatum'], errors='coerce', format='%Y%m%d')

            results = pd.concat([results, data], sort=False)

        # Sanity checks
        if results.empty:
            logger.info('Querying DWD CDC returned empty results')
            return

        # Reset index column
        results.reset_index(drop=True, inplace=True)

        return results

    def create_megaframe(self, frame, drop_index_columns=False):

        # https://pandas.pydata.org/pandas-docs/stable/merging.html#database-style-dataframe-joining-merging

        # Prevent errors like::
        #   ValueError: 'Stations_id' is both an index level and a column label, which is ambiguous.
        if drop_index_columns:
            frame.drop(columns=['Stations_id'], axis='columns', inplace=True)

        # Stations
        frame = pd.merge(frame, self.get_stations(), left_on='Stations_id', right_on='Stations_id')

        # Species
        frame = pd.merge(frame, self.get_species(), left_on='Objekt_id', right_on='Objekt_ID')

        # Phases
        frame = pd.merge(frame, self.get_phases(), left_on='Phase_id', right_on='Phase_ID')

        # Quality level
        if 'Qualitaetsniveau' in frame:
            frame = pd.merge(frame, self.get_quality_levels(), left_on='Qualitaetsniveau', right_index=True)

        # Quality byte
        # ftp://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/standard_format/qualitaetsbytes.pdf
        if 'Eintrittsdatum_QB' in frame:
            frame = pd.merge(frame, self.get_quality_bytes(), left_on='Eintrittsdatum_QB', right_index=True)

        # Debugging
        #print frame.to_csv(encoding='utf-8')

        return frame

    def flux(self, results, criteria=None):
        """
        The flux compensator. All filtering on the DataFrame takes places here.
        """

        logger.info('Entering flux compensator: Filter and transform data')

        criteria = criteria or {}

        # Sanity checks
        if results is None:
            return

        # Filter DataFrame
        # https://pythonspot.com/pandas-filter/
        # https://stackoverflow.com/questions/12065885/filter-dataframe-rows-if-value-in-column-is-in-a-set-list-of-values/12065904#12065904


        # A. Basic filtering

        # Build "boolean indexing" filter expression from multiple ID-based criteria
        # https://pandas.pydata.org/pandas-docs/stable/indexing.html#boolean-indexing
        isin_map = {
            'year': 'Referenzjahr',
            'quality-level': 'Qualitaetsniveau',
            'quality-byte': 'Eintrittsdatum_QB',
            'station-id': 'Stations_id',
            'species-id': 'Objekt_id',
            'phase-id': 'Phase_id',
        }

        # Low-level filtering based on IDs
        # For each designated field, add ``.isin`` criteria to "boolean index" expression
        expression = True
        for key, field in list(isin_map.items()):
            if field not in results:
                continue
            reference = results[field]
            if key in criteria and criteria[key]:
                values = map(int, criteria[key])
                expression &= reference.isin(values)

        # Apply filter expression to DataFrame
        if type(expression) is not bool:
            results = results[expression]


        # B. Humanized filtering based on merged/joined DataFrames

        # Build "boolean indexing" filter expression from multiple text-based criteria
        # https://pandas.pydata.org/pandas-docs/stable/indexing.html#boolean-indexing
        # https://stackoverflow.com/questions/12065885/filter-dataframe-rows-if-value-in-column-is-in-a-set-list-of-values/26724725#26724725
        patterns_map = {
            'station': ['Stationsname', 'Naturraumgruppe', 'Naturraum', 'Bundesland'],
            'species': ['Objekt', 'Objekt_englisch', 'Objekt_latein'],
            'phase':   ['Phase', 'Phase_englisch'],
            'quality': ['Beschreibung_x', 'Beschreibung_y'],
        }

        # Remember columns of current DataFrame
        columns = results.columns

        expression = True
        is_megaframe = False
        for field, reference_fields in list(patterns_map.items()):

            if field in criteria and criteria[field]:

                # Create megaframe as this will contain all information required for advanced searching
                if not is_megaframe:
                    is_megaframe = True
                    results = self.create_megaframe(results)

                # The list of patterns to search for. Any match counts.
                pattern = '|'.join(criteria[field])

                subexpression = False
                for reference_field in reference_fields:
                    subexpression |= results[reference_field].str.contains(pattern, case=False)

                expression &= subexpression

        # Shrink megaframe back using projection on former columns
        results = results[columns]

        # Apply filter expression to DataFrame
        if type(expression) is not bool:
            results = results[expression]

        return results

    def scan_files(self, partition, include=None, field=None):
        """
        Scan upstream files in three-level directory hierarchy.
        """

        # The full URL to the FTP data directory
        url = self.cdc.baseurl + self.data_directory

        # Query FTP server for files
        entries = self.cdc.ftp.scan_files(
            url, subdir=partition,
            include=include,
            include_base=['PH_(Sofort|Jahres)melder.+\.txt'],
            exclude_base=['PH_Beschreibung', 'Spezifizierung', 'PH_.+_Notiz'],
        )

        # Return entries if projection to field not requested
        if not field:
            return entries

        # Project entries to results
        results = []
        for entry in entries:

            try:
                item = entry[field]
                results.append(item)

            except KeyError:
                raise KeyError('Projection "field={}" not available'.format(field))

        return results

    @classmethod
    def load_preset(cls, section, option, name):
        resource = pkg_resources.resource_stream(__name__, 'presets.json')
        presets = json.load(resource)
        try:
            value = presets[section][option][name]
            return value
        except KeyError:
            message = 'Preset "{}" not found in file "{}"'.format(name, resource.name)
            logger.error(message)
            raise KeyError(message)

@attr.s
class DwdPhenoDataHumanizer:
    """
    Bring result DataFrame in a more pleasant shape.
    """

    # Output language. "english", "german" or "latin"
    language = attr.ib()

    # Whether to output long station name including "Naturraumgruppe" and "Naturraum"
    long_station = attr.ib()

    # Whether to show IDs alongside resolved text representation
    show_ids = attr.ib()

    def get_observations(self, frame):

        canvas = pd.DataFrame()

        stations, species, phases, quality_levels, quality_bytes = self.get_fields(frame)

        # Build fresh DataFrame with designated order of columns
        canvas['Jahr'] = frame['Referenzjahr']
        canvas['Datum'] = frame['Eintrittsdatum'].astype(str)
        canvas['Tag'] = frame['Jultag']
        canvas['Spezies'] = species
        canvas['Phase'] = phases
        canvas['Station'] = stations
        canvas['QS-Level'] = quality_levels
        canvas['QS-Byte'] = quality_bytes

        return canvas

    def get_forecast(self, frame, target_year):

        canvas = pd.DataFrame()

        stations, species, phases, quality_levels, quality_bytes = self.get_fields(frame)

        # Build fresh DataFrame with designated order of columns
        canvas['Datum'] = frame['Datum'].astype(str)
        canvas['Tag'] = frame['Jultag']
        canvas['Spezies'] = species
        canvas['Phase'] = phases
        canvas['Station'] = stations

        canvas.insert(0, 'Jahr', target_year)

        return canvas

    def get_fields(self, frame):

        # Which fields to use from "station" entity
        if self.long_station:
            station_fields = ['Stationsname', 'Naturraumgruppe', 'Naturraum', 'Bundesland']
        else:
            station_fields = ['Stationsname', 'Bundesland']

        # Improved map for quality level texts
        quality_level_text = {
            1: u'Load time checks',
            7: u'ROUTKLI validated',
            10: u'ROUTKLI validated and corrected',
            }

        # Which field to choose from the "species" entity. One of "Objekt", "Objekt_englisch", "Objekt_latein".
        # Which field to choose from the "phase" entity. One of "Phase", "Phase_englisch".
        species_field = 'Objekt_englisch'
        phase_field = 'Phase_englisch'
        if self.language:
            language = self.language.lower()
            if language == 'german':
                species_field = 'Objekt'
                phase_field = 'Phase'
                quality_level_text = {
                    1: u'Vorabprüfung beim Laden',
                    7: u'ROUTKLI geprüft',
                    10: u'ROUTKLI geprüft und korrigiert',
                    }
            elif language == 'latin':
                species_field = 'Objekt_latein'

        stations = []
        species = []
        phases = []
        quality_levels = []
        quality_bytes = []
        for index, row in frame.iterrows():

            # Station
            station_parts = [row[field] for field in station_fields if field in row]
            station_label = ', '.join(station_parts)
            if self.show_ids:
                station_label += ' [{}]'.format(row['Stations_id'])
            stations.append(station_label)

            # Species
            species_label = row.get(species_field, '')
            if self.show_ids:
                species_label += ' [{}]'.format(row['Objekt_id'])
            species.append(species_label)

            # Phase
            phase_label = row.get(phase_field, '')
            if self.show_ids:
                phase_label += ' [{}]'.format(row['Phase_id'])
            phases.append(phase_label)

            # Qualitaetsniveau
            if 'Qualitaetsniveau' in row:
                ql_label = quality_level_text.get(row['Qualitaetsniveau'], row.get('Beschreibung_x', ''))
                if self.show_ids:
                    ql_label += ' [{}]'.format(row['Qualitaetsniveau'])
                quality_levels.append(ql_label)

            # Qualitaetsbyte
            # ftp://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/standard_format/qualitaetsbytes.pdf
            if 'Eintrittsdatum_QB' in row:
                qb_label = row.get('Beschreibung_y', '')
                if self.show_ids:
                    qb_label += ' [{}]'.format(row['Eintrittsdatum_QB'])
                quality_bytes.append(qb_label)

        return stations, species, phases, quality_levels, quality_bytes
