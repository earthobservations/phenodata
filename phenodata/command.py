# -*- coding: utf-8 -*-
# (c) 2018-2023, The Earth Observations Developers
"""
phenodata is an acquisition and processing toolkit for open access phenology data.
"""
import sys
import logging
from docopt import docopt, DocoptExit
from tabulate import tabulate
from phenodata import __appname__, __version__
from phenodata.dwd.export import export_database
from phenodata.ftp import FTPSession
from phenodata.dwd.cdc import DwdCdcClient
from phenodata.dwd.pheno import DwdPhenoDataClient, DwdPhenoDataHumanizer
from phenodata.util import boot_logging, normalize_options, options_convert_lists

logger = logging.getLogger(__name__)


def run():
    """
    Usage:
      phenodata info
      phenodata list-species --source=dwd [--format=csv]
      phenodata list-phases --source=dwd [--format=csv]
      phenodata list-stations --source=dwd --dataset=immediate [--all] [--filter=berlin] [--sort=Stationsname] [--format=csv]
      phenodata nearest-station --source=dwd --dataset=immediate --latitude=52.520007 --longitude=13.404954 [--format=csv]
      phenodata nearest-stations --source=dwd --dataset=immediate --latitude=52.520007 --longitude=13.404954 [--all] [--limit=10] [--format=csv]
      phenodata list-quality-levels --source=dwd [--format=csv]
      phenodata list-quality-bytes --source=dwd [--format=csv]
      phenodata list-filenames --source=dwd --dataset=immediate --partition=recent [--filename=Hasel,Schneegloeckchen] [--year=2017]
      phenodata list-urls --source=dwd --dataset=immediate --partition=recent [--filename=Hasel,Schneegloeckchen] [--year=2017]
      phenodata (observations|forecast) --source=dwd --dataset=immediate --partition=recent [--filename=Hasel,Schneegloeckchen] [--station-id=164,717] [--species-id=113,127] [--phase-id=5] [--quality-level=10] [--quality-byte=1,2,3] [--station=berlin,brandenburg] [--species=hazel,snowdrop] [--species-preset=mellifera-de-primary] [--phase=flowering] [--quality=ROUTKLI] [--year=2017] [--forecast-year=2021] [--humanize] [--show-ids] [--language=german] [--long-station] [--sort=Datum] [--sql=sql] [--format=csv] [--verbose]
      phenodata export-observations --source=dwd --dataset=immediate --partition=recent --target=sqlite:///phenodata-dwd-sample.sqlite [--filename=Hasel,Schneegloeckchen] [--station-id=164,717] [--species-id=113,127] [--phase-id=5] [--station=berlin,brandenburg] [--species=hazel,snowdrop] [--species-preset=mellifera-de-primary] [--year=2017] [--format=sqlite] [--verbose]
      phenodata export-observations-all --source=dwd [--verbose]
      phenodata drop-cache --source=dwd
      phenodata --version
      phenodata (-h | --help)

    Data acquisition options:
      --source=<source>         Data source. Currently, only "dwd" is a valid identifier.
      --dataset=<dataset>       Data set. Use "immediate" or "annual" for "--source=dwd".
      --partition=<dataset>     Partition. Use "recent" or "historical" for "--source=dwd".
      --filename=<file>         Filter by file names (comma-separated list)

    Direct filtering options:
      --year=<year>             Filter by year (comma-separated list)
      --station-id=<station-id> Filter by station identifiers (comma-separated list)
      --species-id=<species-id> Filter by species identifiers (comma-separated list)
      --phase-id=<phase-id>     Filter by phase identifiers (comma-separated list)

    Humanized filtering options:
      --station=<station>       Filter by strings from "stations" data (comma-separated list)
      --species=<species>       Filter by strings from "species" data (comma-separated list)
      --phase=<phase>           Filter by strings from "phases" data (comma-separated list)
      --species-preset=<preset> Filter by strings from "species" data (comma-separated list)
                                The preset will get loaded from the "presets.json" file.

    Forecasting options:
      --forecast-year=<year>    Use as designated forecast year.

    Postprocess filtering options:
      --sql=<sql>               Apply given SQL query before output.

    Data output options:
      --format=<format>         Output data in designated format. Choose one of "tabular", "json",
                                "csv", or "string". With "tabular", it is also possible to specify
                                the table format. Use "tabular:pipe" for Markdown output, or
                                "tabular:rst" for reStructuredText. [default: tabular:psql]
      --sort=<sort>             Sort by given field names. (comma-separated list)
      --humanize                Resolve identifier-based fields to human-readable labels.
      --show-ids                Show identifiers alongside resolved labels, when using "--humanize".
      --language=<language>     Use labels in designated language, when using "--humanize"
                                [default: english].
      --long-station            Use long station name including "Naturraumgruppe" and "Naturraum".
      --limit=<limit>           Limit output of "nearest-stations" to designated number of entries.
                                [default: 10]
      --verbose                 Turn on verbose output.
    """

    # Use generic commandline options schema and amend with current program name
    commandline_schema = run.__doc__

    # Read commandline options
    options = docopt(commandline_schema, version=f'{__appname__} {__version__}')

    # Initialize logging
    boot_logging(options)

    # Normalize commandline options
    options = normalize_options(options, encoding='utf-8')

    # Expand options
    preset_name = options['species-preset']
    if preset_name:
        options['species'] = DwdPhenoDataClient.load_preset('options', 'species', preset_name)

    # Coerce comma-separated list fields
    options_convert_lists(options, list_items=[

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
        'station',
        'species',
        'phase',

        # Sorting parameters
        'sort',
    ])

    # Command line argument debugging
    #import pprint; print 'options:\n{}'.format(pprint.pformat(options))

    if options['info']:
        print('Name:         phenodata-{version}'.format(version=__version__))
        print('Description:  phenodata is an acquisition and processing toolkit for open access phenology data')
        print('Data sources: DWD')
        # TODO: Add cache location and info
        return

    # Create data source adapter
    if options['source'] == 'dwd':
        cdc_client = DwdCdcClient(ftp=FTPSession())
        humanizer = DwdPhenoDataHumanizer(language=options['language'], long_station=options['long-station'], show_ids=options['show-ids'])
        client = DwdPhenoDataClient(cdc=cdc_client, humanizer=humanizer, dataset=options.get('dataset'))
    else:
        message = 'Data source "{}" not implemented'.format(options['source'])
        logger.error(message)
        raise DocoptExit(message)

    # Dispatch command
    data = None
    if options['list-species']:
        data = client.get_species()
    elif options['list-phases']:
        data = client.get_phases()
    elif options['list-stations']:
        data = client.get_stations(filter=options['filter'], all=options['all'])
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
        data = client.get_observations(options, humanize=options['humanize'])

    elif options['forecast']:
        data = client.get_forecast(options, forecast_year=options['forecast-year'], humanize=options['humanize'])

    elif options['nearest-station']:
        data = client.nearest_station(float(options['latitude']), float(options['longitude']), all=options['all'])

    elif options['nearest-stations']:
        data = client.nearest_stations(float(options['latitude']), float(options['longitude']), all=options['all'], limit=int(options['limit']))

    elif options['drop-cache']:
        client.cdc.ftp.ensure_cache_manager()
        if client.cdc.ftp.cache.drop():
            logger.info('Dropping the cache succeeded')
        else:
            logger.warning('Dropping the cache failed')
        return

    elif options['export-observations']:
        target = options['target']
        export_database(client, target, options)

    elif options['export-observations-all']:
        source = options["source"]
        for partition in ["recent", "historical"]:
            for dataset in ["immediate", "annual"]:
                dbname = f"phenodata-{source}-{dataset}-{partition}.sqlite"
                target = f"sqlite:///{dbname}"
                options["dataset"] = dataset
                options["partition"] = partition
                logger.debug(f"Running database export with options: {options}")
                client = DwdPhenoDataClient(cdc=cdc_client, humanizer=humanizer, dataset=options.get('dataset'))
                export_database(client, target, options)

    # Query results
    if data is not None and options["sql"]:
        import duckdb
        data = duckdb.query(query=options["sql"], alias="data").df()

    # Format and output results
    if data is not None:

        output_format = options['format'].lower()

        # Whether to show the index column or not
        showindex = True
        if options['observations'] or options['forecast']:

            # Don't display index column.
            showindex = False

            # Apply minor cosmetic amendments.
            date_field_candidates = ['Eintrittsdatum', 'Datum']
            for date_field in date_field_candidates:
                if date_field in data:
                    data[date_field] = data[date_field].astype(str)

        # Sort columns
        if options['sort']:
            data.sort_values(options['sort'], inplace=True)

        # Handle aliases for reStructuredText and Markdown
        if output_format in ["restructuredtext", "rst"]:
            output_format = "tabular:rst"
        elif output_format in ["markdown", "md"]:
            output_format = "tabular:pipe"

        output = None
        if output_format.startswith('tabular'):

            try:
                tablefmt = output_format.split(':')[1]
            except:
                tablefmt = 'psql'

            # TODO: How to make "tabulate" print index column name?
            output = tabulate(data, headers=data.columns, showindex=showindex, tablefmt=tablefmt)

        elif output_format == 'csv':
            output = data.to_csv(encoding='utf-8', index=showindex)

        elif output_format == 'json':
            if showindex:
                data = data.reset_index()
            output = data.to_json(orient='records', date_format='iso')

        elif output_format == 'string':
            output = data.to_string()

        else:
            message = 'Unknown output format "{}"'.format(options['format'])
            logger.error(message)
            sys.exit(1)

        if output is not None:
            if sys.version_info.major == 2:
                print(output.encode('utf-8'))
            else:
                print(output)
        else:
            logger.warning('Empty output')
