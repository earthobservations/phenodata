import logging
import typing as t

import pandas as pd

from phenodata.dwd.model import DwdPhenoDataset, DwdPhenoDatabase, DwdPhenoPartition
from phenodata.dwd.pheno import DwdPhenoDataClient


logger = logging.getLogger(__name__)


def acquire_database(client: DwdPhenoDataClient, options: t.Optional[t.Dict[str, str]] = None) -> DwdPhenoDatabase:
    options = options or {}
    dataset = options.get("dataset", "unknown")
    partition = options.get("partition", "unknown")

    species = client.get_species()
    species_group = get_species_presets_df(species)

    db = DwdPhenoDatabase(
        dataset=DwdPhenoDataset(dataset),
        partition=DwdPhenoPartition(partition),
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
    logger.info(f"Exporting data to {target}")
    # TODO: Warn that specific options will not be honored.
    db = acquire_database(client=client, options=options).with_canonical_column_names()
    db.info()
    db.to_sql(target)
    # Optionally print samples.
    # print(db.observations)
    logger.info(f"Exported data to {target}")


def get_species_presets_df(species: pd.DataFrame):
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
