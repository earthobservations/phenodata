# -*- coding: utf-8 -*-
# (c) 2023, The Earth Observations Developers
import datetime
import logging
import sys
import typing as t
from collections import OrderedDict

import pandas as pd

from phenodata import __appname__, __version__
from phenodata.dwd.model import DwdPhenoDataset, DwdPhenoDatabase, DwdPhenoPartition
from phenodata.dwd.pheno import DwdPhenoDataClient


logger = logging.getLogger(__name__)


def acquire_database(client: DwdPhenoDataClient, options: t.Optional[t.Dict[str, str]] = None) -> DwdPhenoDatabase:
    options = options or {}
    dataset = options.get("dataset", "unknown")
    partition = options.get("partition", "unknown")

    species = client.get_species()
    species_group = get_species_groups(species)

    db = DwdPhenoDatabase(
        dataset=DwdPhenoDataset(dataset),
        partition=DwdPhenoPartition(partition),
        about=get_about(dataset=dataset, partition=partition),
        species=species,
        species_group=species_group,
        phase=client.get_phases(),
        quality_level=client.get_quality_levels(),
        quality_byte=client.get_quality_bytes(),
        station=client.get_stations(filter=options['filter'], all=options['all']),
        observation=client.get_observations(options=options),
    )
    db.observation["source"] = "dwd"
    db.observation["dataset"] = db.dataset.name.lower()
    db.observation["partition"] = db.partition.name.lower()
    return db


def export_database(client, target, options):
    if sys.version_info <= (3, 7):
        raise DeprecationWarning("The SQLite export feature does not work on Python 3.7")
    logger.info(f"Exporting data to {target}")
    # TODO: Warn that specific options will not be honored.
    db = acquire_database(client=client, options=options).with_canonical_column_names()
    db.info()
    db.to_sql(target)
    # Optionally print samples.
    # print(db.observations)
    logger.info(f"Exported data to {target}")


def get_species_groups(species: pd.DataFrame):
    """
    Convert species groups from `presets.json` into DataFrame.
    """
    data = DwdPhenoDataClient.load_preset_species()
    outdata = []
    for group_name, items_raw in data.items():
        items = list(map(str.strip, items_raw.split(",")))
        for item in items:
            result = species.query("Objekt == @item")
            try:
                species_id = result.index.values[0]
            except:
                logger.warning(f"Species name not found in data: {item}")
                continue
            outitem = {"species_id": species_id, "group_name": group_name, "species_name_de": item}
            outdata.append(outitem)
    outdf = pd.DataFrame.from_records(outdata, index="species_id")
    outdf.attrs["name"] = "species_group"
    return outdf


def get_about(dataset: str, partition: str) -> pd.DataFrame:
    """
    Provide database metadata.
    """
    today = datetime.datetime.today().strftime("%Y-%m-%d")
    about = pd.DataFrame.from_records([
        {"name": "type", "value": "Dataset"},
        {"name": "title", "value": "DWD SQLite database archive"},
        {"name": "subject", "value": "Providing unrestricted and free access to plant phenological observation data, "
                                     "in the spirit of PPODB"},
        {"name": "description", "value": "Full dumps of DWD plant phenological observation data in SQLite database format"},
        {"name": "source", "value": "DWD Climate Data Center (CDC); https://www.dwd.de/EN/ourservices/opendata/opendata.html; https://opendata.dwd.de/climate_environment/CDC/observations_germany/phenology/; https://opendata.dwd.de/climate_environment/CDC/help/"},
        {"name": "creator", "value": f"DWD Climate Data Center (CDC): Phenological observations of plants from sowing to harvest ({dataset} reporters, {partition}), Version v007, {today}"},
        {"name": "spatial", "value": "Mostly Germany"},
        {"name": "publisher", "value": f"{__appname__} {__version__} - an acquisition and processing toolkit for open access phenology data"},
        {"name": "copyright", "value": "DWD CDC; https://phenodata.readthedocs.io/en/latest/archive/dwd.html#data-copyright"},
        {"name": "created", "value": today},
        {"name": "modified", "value": today},
        {"name": "references", "value": "https://phenodata.readthedocs.io/en/latest/archive/dwd.html"},
    ])
    about.attrs["name"] = "about"
    about = about.set_index("name")
    return about
