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
      phenodata list-species --source=dwd
      phenodata list-phases --source=dwd
      phenodata list-stations --source=dwd --dataset=immediate
      phenodata list-quality-levels --source=dwd

      phenodata info
      phenodata --version
      phenodata (-h | --help)

    Document acquisition options:
      --source=<source>         Data source. Currently "dwd" only.
      --dataset=<dataset>       Data set. Use "immediate" or "annual" for --source=dwd.
    """

    # Use generic commandline options schema and amend with current program name
    commandline_schema = run.__doc__

    # Read commandline options
    options = docopt(commandline_schema, version=APP_NAME + ' ' + __version__)

    # Initialize logging
    boot_logging(options)

    # Normalize commandline options
    options = normalize_options(options)

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
        data = client.get_stations(dataset=options['dataset'])
    elif options['list-quality-levels']:
        data = client.get_quality_levels()

    # TODO: Do either this or that
    #print data.to_string()
    #print data.to_json(orient='index')

    # TODO: How to make "tabulate" print index column name
    payload = tabulate(data, headers=data.columns, showindex=True, tablefmt='psql').encode('utf-8')
    print(payload)
