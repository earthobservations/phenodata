# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
import re
import attr
import logging
import requests
import requests_ftp
import pandas as pd
from six import StringIO

logger = logging.getLogger(__name__)

# Monkeypatch Requests Sessions to provide all the helper methods needed for use with FTP
requests_ftp.monkeypatch_session()

@attr.s
class DwdDataAcquisition(object):

    baseurl = 'ftp://ftp-cdc.dwd.de/pub/CDC'

    dataset = attr.ib()

    def __attrs_post_init__(self):
        self.dwdftp = requests.Session()

    def read_ftp_csv(self, url):

        # Retrieve CSV file
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

        # Read CSV into Pandas DataFrame
        # https://pandas.pydata.org/pandas-docs/stable/io.html
        df = pd.read_csv(
            StringIO(content), engine='c', encoding='Windows-1252',
            delimiter=';', skipinitialspace=True, skip_blank_lines=True,
            index_col=0)

        # Remove empty rows
        df.dropna(subset=['eor'], inplace=True)

        # Remove trailing nonsense columns
        last_column = len(df.columns) - 1
        df.drop(df.columns[[last_column]], axis=1, inplace=True)
        df.drop('eor', axis=1, inplace=True)

        return df

    def get_species(self):
        """Return Pandas DataFrame containing complete species information"""
        return self.read_ftp_csv(self.baseurl + '/help/PH_Beschreibung_Pflanze.txt')

    def get_phases(self):
        """Return Pandas DataFrame containing complete phases information"""
        return self.read_ftp_csv(self.baseurl + '/help/PH_Beschreibung_Phase.txt')

    def get_stations(self, dataset):
        """Return Pandas DataFrame containing complete stations information"""
        if dataset == 'immediate':
            filename = 'PH_Beschreibung_Phaenologie_Stationen_Sofortmelder.txt'
        elif dataset == 'annual':
            filename = 'PH_Beschreibung_Phaenologie_Stationen_Jahresmelder.txt'
        else:
            raise KeyError('Unknown dataset "{}"'.format(dataset))

        return self.read_ftp_csv(self.baseurl + '/help/' + filename)
