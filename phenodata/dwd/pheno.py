# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
import attr
import logging
import pandas as pd

logger = logging.getLogger(__name__)

@attr.s
class DwdPhenoData(object):
    """
    Conveniently access phenology information from the Climate Data Center (CDC)
    FTP server operated by »Deutscher Wetterdienst« (DWD).

    See also `cdc-readme`_:
    Phenological data is collected at about 1200 active stations. The state of development of
    selected plants (e.g., apple, birch, snow drops, goose berry, wheat, vine, etc.) is reported
    by annual reporters and immediate reporters.

    The lists of phenological stations can be found in the list of phenology `annual reporters`_
    and the list of phenology `immediate reporters`_.

    .. _cdc-readme: ftp://ftp-cdc.dwd.de/pub/CDC/Readme_intro_CDC_ftp.txt
    .. _annual reporters: ftp://ftp-cdc.dwd.de/pub/CDC/help/PH_Beschreibung_Phaenologie_Stationen_Jahresmelder.txt
    .. _immediate reporters: ftp://ftp-cdc.dwd.de/pub/CDC/help/PH_Beschreibung_Phaenologie_Stationen_Sofortmelder.txt

    """

    # Instance of the lowlevel DWD CDC FTP server client wrapper object ``phenodata.dwd.cdc.DwdCdcClient``
    cdc = attr.ib()

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
        """
        return self.cdc.get_dataframe(path='/help/PH_Beschreibung_Phaenologie_Qualitaetsbyte.txt', index_column=0)

    def get_stations(self):
        """
        Return DataFrame with stations information.
        """

        if self.dataset == 'immediate':
            filename = '/help/PH_Beschreibung_Phaenologie_Stationen_Sofortmelder.txt'
        elif self.dataset == 'annual':
            filename = '/help/PH_Beschreibung_Phaenologie_Stationen_Jahresmelder.txt'
        else:
            raise KeyError('Unknown dataset "{}"'.format(self.dataset))

        return self.cdc.get_dataframe(path=filename, index_column=0)

    def get_observations(self, options):
        """
        Obtain query options.
        Compute DataFrame with combined observation data.
        Apply a bunch of filters to the result data.
        """

        observations = self.query(partition=options['partition'], files=options['files'])

        observations = self.flux(
            observations,
            stations=options['stations'], regions=options['regions'],
            species=options['species'], phases=options['phases'],
            years=options['years'], forecast=options['forecast'])

        return observations

    def query(self, partition=None, files=None):
        """
        The FTP/Pandas workhorse, converges data from multiple observation data
        CSV files on upstream CDC FTP server into a single Pandas DataFrame object.

        - Obtains ``partition`` parameter which can be either ``annual`` or ``immediate``.
        - Obtains optional ``files`` parameter which will be applied
          as an "include" filter to the list of scanned file names.
        """

        logger.info('Starting data acquisition')

        # Search FTP server
        paths = self.scan_files(partition, files=files, field='url')

        # The main DataFrame object
        results = pd.DataFrame()

        # Load multiple files into single DataFrame
        for path in paths:

            # Acquire DataFrame from CSV data
            data = self.cdc.get_dataframe(path, coerce_int=True)

            # Sanity checks
            if data is None:
                continue

            # Skip invalid files
            if 'Kulturpflanze_Ruebe_akt' in path:
                logger.warning('Skipping file "{}" due to invalid header format (all caps)'.format(path))
                continue

            # Coerce "Eintrittsdatum" column into date format
            data['Eintrittsdatum'] = pd.to_datetime(data['Eintrittsdatum'], errors='coerce', format='%Y%m%d')

            # Append to DataFrame
            results = results.append(data)

        # Sanity checks
        if results.empty:
            logger.info('Querying DWD CDC returned empty results')
            return

        # Reset index column
        results.reset_index(drop=True, inplace=True)

        return results

    def flux(self, results, stations=None, regions=None, species=None, phases=None, years=None, forecast=False):
        """
        The flux compensator. All filtering on the DataFrame takes places here.
        """

        logger.info('Flux compensator: Filter and transform data')

        # Filter DataFrame
        # https://pythonspot.com/pandas-filter/
        # https://stackoverflow.com/questions/12065885/filter-dataframe-rows-if-value-in-column-is-in-a-set-list-of-values/12065904#12065904

        # Build "boolean indexing" filter expression from multiple criteria
        # https://pandas.pydata.org/pandas-docs/stable/indexing.html#boolean-indexing
        expression = True
        if stations:
            expression &= results.Stations_id.isin(stations)
        if years:
            expression &= results.Referenzjahr.isin(years)

        # Apply filter expression to DataFrame
        if type(expression) is not bool:
            results = results[expression]

        return results

    def scan_files(self, partition, files=None, field=None):
        """
        Scan upstream files in three-level directory hierarchy.
        """

        # The full URL to the FTP data directory
        url = self.cdc.baseurl + self.data_directory

        # Query FTP server for files
        entries = self.cdc.ftp.scan_files(
            url, subdir=partition,
            include=files,
            include_base=['PH_(Sofort|Jahres)melder.+\.txt'],
            exclude_base=['PH_Beschreibung', 'Spezifizierung'],
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
