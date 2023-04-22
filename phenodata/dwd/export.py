import logging
import typing as t

from phenodata.dwd.model import DwdPhenoDataset, DwdPhenoDatabase, DwdPhenoPartition
from phenodata.dwd.pheno import DwdPhenoDataClient


logger = logging.getLogger(__name__)


def acquire_database(client: DwdPhenoDataClient, options: t.Optional[t.Dict[str, str]] = None) -> DwdPhenoDatabase:
    options = options or {}
    dataset = options.get("dataset", "unknown")
    partition = options.get("partition", "unknown")
    db = DwdPhenoDatabase(
        dataset=DwdPhenoDataset(dataset),
        partition=DwdPhenoPartition(partition),
        species=client.get_species(),
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
