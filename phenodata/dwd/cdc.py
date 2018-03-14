# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
import re
import attr
import pandas as pd
from six import StringIO
from phenodata.util import dataframe_strip_strings, dataframe_coerce_columns

@attr.s
class DwdCdcClient(object):
    """
    Base functionality for conveniently accessing the Climate Data Center (CDC)
    FTP server operated by »Deutscher Wetterdienst« (DWD).
    """

    # The base URL to data on the CDC FTP server
    baseurl = 'ftp://ftp-cdc.dwd.de/pub/CDC'

    # Instance of ``phenodata.ftp.FTPSession`` object for lowlevel access to CDC FTP
    ftp = attr.ib()

    def get_dataframe(self, url=None, path=None, index_column=None, coerce_int=False):
        """
        Read single CSV file from FTP url and convert to Pandas DataFrame object.

        Obtains either a full ``url`` parameter or a ``path`` parameter
        for addressing the remote resource. If the ``path`` parameter is given,
        ``self.baseurl`` will be prefixed to ``path`` before accessing the resource.

        Optionally obtains ``index_column`` parameter.
        Use this to set the index of designated index column.

        Optionally obtains ``coerce_int`` parameter.
        Use this to convert all values to integer format.
        """
        if path:
            url = self.baseurl + path
        return self.csv_to_dataframe(self.read_csv(url), index_column=index_column, coerce_int=coerce_int)

    def read_csv(self, url):
        """
        Read CSV file from FTP url and apply response caching based on file modification time (mtime).
        Fixup different anomalies to make it compatible with ``pandas.read_csv``.
        """

        # Retrieve CSV file
        content = self.ftp.retr_cached(url, strip_base=self.baseurl)

        # Sanity checks
        if not content:
            return

        # Fix CSV formatting
        content = content.strip()
        content = content.replace('\r\n', '')
        content = re.sub(';eor;\s*', ';eor;\n', content)
        content = re.sub('; eor ;\s*', '; eor;\n', content)
        content = content.strip()

        # Specific fixups
        if 'Qualitaetsbyte' in url:
            content = content.replace('Eintrittsdatum;', 'Eintrittsdatum,')

        # Debugging
        #print 'content:\n', response.content.decode('Windows-1252').encode('utf8')

        return StringIO(content)

    def csv_to_dataframe(self, stream, index_column=None, coerce_int=False):
        """
        Read CSV data from stream into Pandas DataFrame object.

        Optionally obtains ``index_column`` parameter.
        Use this to set the index of designated index column.

        Optionally obtains ``coerce_int`` parameter.
        Use this to convert all values to integer format.
        """

        # Sanity checks
        if not stream or stream.len == 0:
            return

        # Read CSV into Pandas DataFrame
        # https://pandas.pydata.org/pandas-docs/stable/io.html
        df = pd.read_csv(
            stream, engine='c', encoding='Windows-1252',
            delimiter=';', skipinitialspace=True, skip_blank_lines=True,
        )


        # A. Apply cleanups

        # Strip whitespace from all column headers
        # https://stackoverflow.com/questions/21606987/how-can-i-strip-the-whitespace-from-pandas-dataframe-headers/21607530#21607530
        df.rename(columns=lambda x: x.strip(), inplace=True)

        # Strip whitespace from all values
        df = df.apply(dataframe_strip_strings, axis=0)

        # Remove rows with empty values
        df.dropna(subset=['eor'], inplace=True)

        # Remove trailing nonsense column
        # FIXME: Only remove if there actually *are* nonsense columns
        last_column_index = len(df.columns) - 1
        last_column = df.columns[[last_column_index]]
        df.drop(last_column, axis=1, inplace=True)

        # Remove end-of-row tombstone
        df.drop('eor', axis=1, inplace=True)


        # B. Apply coercions

        # Coerce types into correct format
        if coerce_int:
            df = df.astype(int)

        # Initialize index column on DataFrame
        if index_column is not None:

            # Get name of index column
            index_column_name = df.columns[index_column]

            # Coerce values in index column to integer
            dataframe_coerce_columns(df, [index_column_name], int)

            # Establish index on index column
            df.set_index(index_column_name, inplace=True)

        return df
