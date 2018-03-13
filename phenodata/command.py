# -*- coding: utf-8 -*-
# (c) 2018 Andreas Motl <andreas@hiveeyes.org>
import logging
from docopt import docopt, DocoptExit
from tabulate import tabulate
from phenodata import __version__
from phenodata.dwd import DwdDataAcquisition
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
      phenodata list-species --source=dwd
      phenodata list-phases --source=dwd
      phenodata list-stations --source=dwd --dataset=immediate
      phenodata list-quality-levels --source=dwd
      phenodata list-filenames --source=dwd --dataset=immediate --partition=recent [--files=Hasel,Schneegloeckchen] [--years=2017 | --forecast]
      phenodata list-urls --source=dwd --dataset=immediate --partition=recent [--files=Hasel,Schneegloeckchen] [--years=2017 | --forecast]
      phenodata observations --source=dwd --dataset=immediate --partition=recent [--files=Hasel,Schneegloeckchen] [--stations=164,717 | --regions=berlin,brandenburg] [--species=hazel,snowdrop] [--phases=flowering] [--years=2017 | --forecast]
      phenodata --version
      phenodata (-h | --help)

    Data acquisition options:
      --source=<source>         Data source. Currently "dwd" only.
      --dataset=<dataset>       Data set. Use "immediate" or "annual" for --source=dwd.
      --partition=<dataset>     Partition. Use "recent" or "historical" for --source=dwd.

    Data filtering options:
      --files=<files>           Filter by files (comma-separated list)
      --years=<years>           Filter by years (comma-separated list)
      --stations=<stations>     Filter by station ids (comma-separated list)
      --regions=<regions>       Filter by region names (comma-separated list)
      --species=<species>       Filter by species names (comma-separated list)
      --phases=<phases>         Filter by phase names (comma-separated list)
    """

    # Use generic commandline options schema and amend with current program name
    commandline_schema = run.__doc__

    # Read commandline options
    options = docopt(commandline_schema, version=APP_NAME + ' ' + __version__)

    # Initialize logging
    boot_logging(options)

    # Normalize commandline options
    options = normalize_options(options, list_items=['stations', 'regions', 'species', 'phases', 'files', 'years'])

    # Command line argument debugging
    #print 'options:\n{}'.format(pformat(options))

    if options['info']:
        print('Name:         phenodata-{version}'.format(version=__version__))
        print('Description:  phenodata is a data acquisition and manipulation toolkit for open access phenology data')
        print('Data sources: DWD')
        return

    # Create data source adapter instance
    if options['source'] == 'dwd':
        client = DwdDataAcquisition(dataset=options.get('dataset'))
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
    elif options['list-filenames']:
        files = client.scan_files(options['partition'], files=options['files'], kind='name')
        print('\n'.join(files))
        return
    elif options['list-urls']:
        files = client.scan_files(options['partition'], files=options['files'], kind='url')
        print('\n'.join(files))
        return

    elif options['observations']:
        data = client.get_observations(options)

    # TODO: Do either this or that
    #print data.to_string(); return
    #print data.to_json(orient='index')

    if data is not None:

        showindex = True
        if options['observations']:
            showindex = False

        # TODO: How to make "tabulate" print index column name
        payload = tabulate(data, headers=data.columns, showindex=showindex, tablefmt='psql').encode('utf-8')
        print(payload)

