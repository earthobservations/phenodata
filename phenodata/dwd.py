# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
import os
import re
import attr
import arrow
import logging
import dogpile.cache
import requests_ftp
import pandas as pd
from six import StringIO

logger = logging.getLogger(__name__)

# Cache metadata for 5 minutes
meta_cache = dogpile.cache.make_region().configure(
    "dogpile.cache.dbm",
    expiration_time=60 * 5,
    arguments={
        "filename": "/var/tmp/phenodata-meta-cache.dbm"
    }
)

# Use custom mechanism for caching content honoring modification time on server (mtime)
content_cache = dogpile.cache.make_region().configure(
    "dogpile.cache.dbm",
    arguments={
        "filename": "/var/tmp/phenodata-content-cache.dbm"
    }
)

@attr.s
class DwdDataAcquisition(object):

    baseurl = 'ftp://ftp-cdc.dwd.de/pub/CDC'

    dataset = attr.ib()
    directory = attr.ib(default=None)

    def __attrs_post_init__(self):
        self.dwdftp = requests_ftp.ftp.FTPSession()
        self.directory = '/observations_germany/phenology/{dataset}_reporters'.format(dataset=self.dataset)

    @meta_cache.cache_on_arguments()
    def ftp_list(self, directory):

        # Send FTP LIST command
        url = self.baseurl + directory
        response = self.dwdftp.list(url)
        #print 'FTP list response:\n{}'.format(response.content)
        if response.status_code != 226:
            message = 'FTP LIST command for {} failed'.format(url)
            logger.error(message)
            return []

        # Decode LIST response
        entries = []
        for line in response.content.split('\n'):

            # Skip empty lines
            line = line.strip()
            if not line: continue

            # Decode line format
            parts = re.split('\s+', line)
            size = int(parts[4])
            mtime = ' '.join(parts[5:8])
            filename = parts[8]

            # Parse modification date
            # https://arrow.readthedocs.io/en/latest/#arrow.factory.ArrowFactory.get
            # https://arrow.readthedocs.io/en/latest/#tokens
            # Examples: Mar 2 04:09, Jun 1 2017
            mtime = arrow.get(mtime, ['MMM D HH:mm', 'MMM D YYYY'])
            if mtime.year == 1:
                mtime = mtime.replace(year=2018)

            # Build directory entry
            entry = {
                'size': size,
                'mtime': mtime,
                'name': filename,
                'path': os.path.join(directory, filename)
            }
            entries.append(entry)

        return entries

    def ftp_get_mtime(self, urlpath):

        # Read container directory list
        directory = os.path.dirname(urlpath)
        entries = self.ftp_list(directory)

        # Build dictionary mapping file url to its modification time for easier lookup
        name_mtime_map = {}
        for entry in entries:
            name_mtime_map[entry['path']] = entry['mtime']

        # Resolve modification time of designated file url
        mtime = name_mtime_map.get(urlpath)

        return mtime

    def ftp_read_csv_cached(self, urlpath):

        shortpath = urlpath.replace(self.directory, '')

        mtime = self.ftp_get_mtime(urlpath)
        logger.info('Resource "{resource}": Last modified on "{mtime}"'.format(resource=shortpath, mtime=mtime))

        payload = None

        resource_key = urlpath
        mtime_key = 'mtime:{resource}'.format(resource=urlpath)
        mtime_cached = content_cache.get(mtime_key)
        if mtime_cached and mtime <= mtime_cached:
            logger.info('Resource "{resource}": Loading from cache'.format(resource=shortpath))
            payload = content_cache.get(resource_key)

        if payload is None:
            logger.info('Resource "{resource}": Retrieving from FTP'.format(resource=shortpath))
            payload = self.ftp_read_csv(urlpath)
            content_cache.set(resource_key, payload)
            content_cache.set(mtime_key, mtime)

        return payload

    def ftp_read_csv(self, urlpath):

        # Retrieve CSV file
        url = self.baseurl + urlpath
        response = self.dwdftp.retr(url)

        # TODO: Honor status code
        #print 'status:', resp.status_code

        # Acquire file content
        content = response.content.strip()

        # Fix CSV formatting
        content = content.replace('\r\n', '')
        content = re.sub(';eor;\s*', ';eor;\n', content)
        content = re.sub('; eor ;\s*', '; eor;\n', content)
        content = content.strip()

        # Specific fixups
        if 'Qualitaetsbyte' in urlpath:
            content = content.replace('Eintrittsdatum;', 'Eintrittsdatum,')

        # Debugging
        #print 'content:\n', response.content.decode('Windows-1252').encode('utf8')

        return content

    def dataframe_from_csv(self, payload, index=None, coerce_int=False):

        # Read CSV into Pandas DataFrame
        # https://pandas.pydata.org/pandas-docs/stable/io.html
        df = pd.read_csv(
            StringIO(payload), engine='c', encoding='Windows-1252',
            delimiter=';', skipinitialspace=True, skip_blank_lines=True,
        )

        if index is not None:
            df.set_index(df.columns[index], inplace=True)

        # Remove rows with empty values
        df.dropna(subset=['eor'], inplace=True)

        # Remove trailing nonsense columns
        last_column_index = len(df.columns) - 1
        last_column = df.columns[[last_column_index]]
        df.drop(last_column, axis=1, inplace=True)

        # Remove end-of-row tombstone
        df.drop('eor', axis=1, inplace=True)

        # Coerce types into correct format
        if coerce_int:
            df = df.astype(int)

        return df

    def fetch_csv(self, urlpath, index=None, coerce_int=False):
        return self.dataframe_from_csv(self.ftp_read_csv_cached(urlpath), index=index, coerce_int=coerce_int)

    def get_species(self):
        """Return Pandas DataFrame containing complete species information"""
        return self.fetch_csv('/help/PH_Beschreibung_Pflanze.txt', index=0)

    def get_phases(self):
        """Return Pandas DataFrame containing complete phases information"""
        return self.fetch_csv('/help/PH_Beschreibung_Phase.txt', index=0)

    def get_quality_levels(self):
        """Return Pandas DataFrame containing complete quality level information"""
        return self.fetch_csv('/help/PH_Beschreibung_Phaenologie_Qualitaetsniveau.txt', index=0)

    def get_quality_bytes(self):
        """Return Pandas DataFrame containing complete quality bytes information"""
        return self.fetch_csv('/help/PH_Beschreibung_Phaenologie_Qualitaetsbyte.txt', index=0)

    def get_stations(self):
        """Return Pandas DataFrame containing complete stations information"""
        if self.dataset == 'immediate':
            filename = 'PH_Beschreibung_Phaenologie_Stationen_Sofortmelder.txt'
        elif self.dataset == 'annual':
            filename = 'PH_Beschreibung_Phaenologie_Stationen_Jahresmelder.txt'
        else:
            raise KeyError('Unknown dataset "{}"'.format(self.dataset))

        return self.fetch_csv('/help/' + filename, index=0)


    def scan_files(self, partition, files=None, kind='path'):

        # Scan all names for designated dataset
        dataset_list = self.ftp_list(self.directory)
        #pprint(dataset_list)

        # crops, fruit, vine, wild
        categories = [entry['name'] for entry in dataset_list]

        # Compute list of items
        items = []
        for category in categories:
            data_directory = '/'.join([self.directory, category, partition])
            data_files = self.ftp_list(data_directory)
            #pprint(data_files)

            for entry in data_files:

                name = entry['name']
                path = entry['path']

                if 'PH_Beschreibung' in name or 'Spezifizierung' in name:
                    continue

                if not re.match('PH_(Sofort|Jahres)melder.+\.txt', name): continue

                use_me = False
                if files:
                    if self.filename_matches(name, files):
                        use_me = True
                else:
                    use_me = True

                if use_me:
                    if kind == 'name':
                        item = name
                    elif kind == 'path':
                        item = path
                    elif kind == 'url':
                        item = self.baseurl + path
                    else:
                        raise KeyError('kind="{}" not implemented'.format(kind))
                    items.append(item)

        return items

    def filename_matches(self, filename, fragments):
        for fragment in fragments:
            if fragment in filename:
                return True
        return False


    def query(self, partition=None, stations=None, regions=None, species=None, phases=None, files=None, years=None, forecast=False, **kwargs):
        paths = self.scan_files(partition, files=files)

        # The main DataFrame object
        results = pd.DataFrame()

        # Load multiple files into single DataFrame
        for path in paths:
            data = self.fetch_csv(path, coerce_int=True)

            # Skip invalid files
            if 'Kulturpflanze_Ruebe_akt' in path:
                logger.warning('Skipping file "{}" due to invalid header format (all caps)'.format(path))
                continue

            # Coerce "Eintrittsdatum" column into date format
            data['Eintrittsdatum'] = pd.to_datetime(data['Eintrittsdatum'], errors='coerce', format='%Y%m%d')

            # Append to DataFrame
            results = results.append(data)

        # Reset index column
        results.reset_index(drop=True, inplace=True)


        # Filter DataFrame
        # https://pythonspot.com/pandas-filter/
        # https://stackoverflow.com/questions/12065885/filter-dataframe-rows-if-value-in-column-is-in-a-set-list-of-values/12065904#12065904

        # Build expression from multiple criteria
        expression = True
        if stations:
            expression = expression & (results.Stations_id.isin(stations))
        if years:
            expression = expression & (results.Referenzjahr.isin(years))

        # Apply filter expression to DataFrame
        # https://pandas.pydata.org/pandas-docs/stable/indexing.html#boolean-indexing
        if type(expression) is not bool:
            results = results[expression]

        return results

    def get_observations(self, options):

        observations = self.query(
            partition=options['partition'],
            stations=options['stations'], regions=options['regions'],
            species=options['species'], phases=options['phases'], files=options['files'],
            years=options['years'], forecast=options['forecast'])

        return observations
