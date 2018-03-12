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
from pprint import pformat

logger = logging.getLogger(__name__)

# Cache metadata for 5 minutes
meta_cache = dogpile.cache.make_region().configure(
    "dogpile.cache.dbm",
    expiration_time=60 * 5,
    arguments={
        "filename": "/var/tmp/phenodata-meta-cache.dbm"
    }
)

# Use custom mechanism for caching content honoring modification time (mtime)
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

    def __attrs_post_init__(self):
        self.dwdftp = requests_ftp.ftp.FTPSession()

    @meta_cache.cache_on_arguments()
    def ftp_list(self, directory):
        url = self.baseurl + directory
        response = self.dwdftp.list(url)

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
                'url': os.path.join(directory, filename)
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
            name_mtime_map[entry['url']] = entry['mtime']

        # Resolve modification time of designated file url
        mtime = name_mtime_map.get(urlpath)

        return mtime

    def ftp_read_csv_cached(self, urlpath):

        mtime = self.ftp_get_mtime(urlpath)
        logger.info('Resource "{resource}" was modified on "{mtime}"'.format(resource=urlpath, mtime=mtime))

        payload = None

        resource_key = urlpath
        mtime_key = 'mtime:{resource}'.format(resource=urlpath)
        mtime_cached = content_cache.get(mtime_key)
        if mtime_cached and mtime <= mtime_cached:
            logger.info('Loading resource "{resource}" from cache'.format(resource=urlpath))
            payload = content_cache.get(resource_key)

        if payload is None:
            logger.info('Loading resource "{resource}" from FTP'.format(resource=urlpath))
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
        content = response.content

        # Fix CSV formatting
        content = content.replace('\r\n', '')
        content = re.sub(';eor;\s*', ';eor;\n', content)

        # Debugging
        #print 'content:\n', response.content.decode('Windows-1252').encode('utf8'); return

        return content

    def dataframe_from_csv(self, payload):

        # Read CSV into Pandas DataFrame
        # https://pandas.pydata.org/pandas-docs/stable/io.html
        df = pd.read_csv(
            StringIO(payload), engine='c', encoding='Windows-1252',
            delimiter=';', skipinitialspace=True, skip_blank_lines=True,
            index_col=0)

        # Remove empty rows
        df.dropna(subset=['eor'], inplace=True)

        # Remove trailing nonsense columns
        last_column = len(df.columns) - 1
        df.drop(df.columns[[last_column]], axis=1, inplace=True)
        df.drop('eor', axis=1, inplace=True)

        return df

    def fetch_csv(self, urlpath):
        return self.dataframe_from_csv(self.ftp_read_csv_cached(urlpath))

    def get_species(self):
        """Return Pandas DataFrame containing complete species information"""
        return self.fetch_csv('/help/PH_Beschreibung_Pflanze.txt')

    def get_phases(self):
        """Return Pandas DataFrame containing complete phases information"""
        return self.fetch_csv('/help/PH_Beschreibung_Phase.txt')

    def get_quality_levels(self):
        """Return Pandas DataFrame containing complete quality level information"""
        return self.fetch_csv('/help/PH_Beschreibung_Phaenologie_Qualitaetsniveau.txt')

    def get_stations(self, dataset):
        """Return Pandas DataFrame containing complete stations information"""
        if dataset == 'immediate':
            filename = 'PH_Beschreibung_Phaenologie_Stationen_Sofortmelder.txt'
        elif dataset == 'annual':
            filename = 'PH_Beschreibung_Phaenologie_Stationen_Jahresmelder.txt'
        else:
            raise KeyError('Unknown dataset "{}"'.format(dataset))

        return self.fetch_csv('/help/' + filename)
