# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
import sys
import logging
from docopt import docopt, DocoptExit
from tabulate import tabulate
from phenodata import __version__
from phenodata.ftp import FTPSession
from phenodata.dwd.cdc import DwdCdcClient
from phenodata.dwd.pheno import DwdPhenoData
from phenodata.util import boot_logging, normalize_options

"""
phenodata is a data acquisition and manipulation toolkit for open access phenology data.
"""

logger = logging.getLogger(__name__)

APP_NAME = 'phenodata'

def run():
    """
    Usage:
      phenodata info
      phenodata list-species --source=dwd [--format=csv]
      phenodata list-phases --source=dwd [--format=csv]
      phenodata list-stations --source=dwd --dataset=immediate [--format=csv]
      phenodata list-quality-levels --source=dwd [--format=csv]
      phenodata list-quality-bytes --source=dwd [--format=csv]
      phenodata list-filenames --source=dwd --dataset=immediate --partition=recent [--filename=Hasel,Schneegloeckchen] [--year=2017]
      phenodata list-urls --source=dwd --dataset=immediate --partition=recent [--filename=Hasel,Schneegloeckchen] [--year=2017]
      phenodata (observations|forecast) --source=dwd --dataset=immediate --partition=recent [--filename=Hasel,Schneegloeckchen] [--station-id=164,717] [--species-id=113,127] [--phase-id=5] [--quality-level=10] [--quality-byte=1,2,3] [--year=2017] [--format=csv]
      phenodata (observations|forecast) --source=dwd --dataset=immediate --partition=recent [--filename=Hasel,Schneegloeckchen] [--station=berlin,brandenburg] [--species=hazel,snowdrop] [--phase=flowering] [--year=2017] [--format=csv]
      phenodata --version
      phenodata (-h | --help)

    Data acquisition options:
      --source=<source>         Data source. Currently "dwd" only.
      --dataset=<dataset>       Data set. Use "immediate" or "annual" for --source=dwd.
      --partition=<dataset>     Partition. Use "recent" or "historical" for --source=dwd.
      --filename=<file>         Filter by file names (comma-separated list)

    Direct filtering options:
      --years=<years>           Filter by years (comma-separated list)
      --station-id=<station-id> Filter by station ids (comma-separated list)
      --species-id=<species-id> Filter by species ids (comma-separated list)
      --phase-id=<phase-id>     Filter by phase ids (comma-separated list)

    Humanized filtering options:
      --station=<station>       Filter by strings from "stations" data (comma-separated list)
      --species=<species>       Filter by strings from "species" data (comma-separated list)
      --phase=<phase>           Filter by strings from "phases" data (comma-separated list)

    Data formatting options:
      --format=<format>         Output data in designated format. Choose one of "tabular", "json", "csv" or "string".
                                With "tabular", it is also possible to specify the table format,
                                see https://bitbucket.org/astanin/python-tabulate. e.g. "tabular:presto".
                                [default: tabular:psql]
    """

    # Use generic commandline options schema and amend with current program name
    commandline_schema = run.__doc__

    # Read commandline options
    options = docopt(commandline_schema, version=APP_NAME + ' ' + __version__)

    # Initialize logging
    boot_logging(options)

    # Normalize commandline options
    options = normalize_options(options, list_items=[

        # Acquisition parameters
        'filename',

        # Filter parameters
        'year',

        # ID parameters
        'quality-level',
        'quality-byte',
        'station-id',
        'species-id',
        'phase-id',

        # Humanized parameters
        'quality',
        'location',
        'species',
        'phase',
    ])

    # Command line argument debugging
    #import pprint; print 'options:\n{}'.format(pprint.pformat(options))

    if options['info']:
        print('Name:         phenodata-{version}'.format(version=__version__))
        print('Description:  phenodata is a data acquisition and manipulation toolkit for open access phenology data')
        print('Data sources: DWD')
        # TODO: Add cache location and info
        return

    # Create data source adapter
    if options['source'] == 'dwd':
        cdc_client = DwdCdcClient(ftp=FTPSession())
        client = DwdPhenoData(cdc=cdc_client, dataset=options.get('dataset'))
    else:
        raise DocoptExit('Data source "{}" not implemented'.format(options['source']))

    # Dispatch command
    data = None
    if options['list-species']:
        data = client.get_species()
    elif options['list-phases']:
        data = client.get_phases()
    elif options['list-stations']:
        data = client.get_stations()
    elif options['list-quality-levels']:
        data = client.get_quality_levels()
    elif options['list-quality-bytes']:
        data = client.get_quality_bytes()

    elif options['list-filenames']:
        files = client.scan_files(options['partition'], include=options['filename'], field='name')
        print('\n'.join(files))
        return
    elif options['list-urls']:
        files = client.scan_files(options['partition'], include=options['filename'], field='url')
        print('\n'.join(files))
        return

    elif options['observations']:
        data = client.get_observations(options)

    elif options['forecast']:
        data = client.get_forecast(options)

    # Format and output results
    if data is not None:

        showindex = True
        if options['observations']:
            showindex = False

        output_format = options['format']

        output = None
        if output_format.startswith('tabular'):

            try:
                tablefmt = options['format'].split(':')[1]
            except:
                tablefmt = 'psql'

            # TODO: How to make "tabulate" print index column name?
            output = tabulate(data, headers=data.columns, showindex=showindex, tablefmt=tablefmt).encode('utf-8')

        elif output_format == 'csv':
            output = data.to_csv(encoding='utf-8', index=showindex)

        elif output_format == 'json':
            output = data.to_json(orient='table', date_format='iso')

        elif output_format == 'string':
            output = data.to_string()

        else:
            message = 'Unknown output format "{}"'.format(options['format'])
            logger.error(message)
            sys.exit(1)

        if output is not None:
            print(output)
        else:
            logger.warning('Empty output')
