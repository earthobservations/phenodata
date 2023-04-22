import dataclasses
import io
import logging
from contextlib import redirect_stdout
from enum import Enum
import typing as t

import pandas as pd
from sqlalchemy import create_engine, Engine
import sqlalchemy as sa

logger = logging.getLogger(__name__)


class DwdPhenoDataset(Enum):
    ANNUAL = "annual"
    IMMEDIATE = "immediate"


class DwdPhenoPartition(Enum):
    RECENT = "recent"
    HISTORICAL = "historical"


@dataclasses.dataclass
class CanonicalCollection:
    index_names: t.List[str]
    column_map: t.Dict[str, str]


class CanonicalColumnMap:
    species = CanonicalCollection(
        index_names=["id"],
        column_map={
            "Objekt": "species_name_de",
            "Objekt_englisch": "species_name_en",
            "Objekt_latein": "species_name_la",
        },
    )
    phase = CanonicalCollection(
        index_names=["id"],
        column_map={
            "Phase": "phase_name_de",
            "Phase_englisch": "phase_name_en",
        },
    )
    station = CanonicalCollection(
        index_names=["id"],
        column_map={
            "Stationsname": "station_name",
            "geograph.Breite": "latitude",
            "geograph.Laenge": "longitude",
            "Stationshoehe": "altitude",
            "Naturraumgruppe_Code": "area_group_code",
            "Naturraumgruppe": "area_group",
            "Naturraum_Code": "area_code",
            "Naturraum": "area",
            "Datum Stationsaufloesung": "station_date_abandoned",
            "Bundesland": "state",
        },
    )
    quality_level = CanonicalCollection(
        index_names=["id"],
        column_map={
            "Beschreibung": "description",
        },
    )
    quality_byte = CanonicalCollection(
        index_names=["id"],
        column_map={
            "Beschreibung": "description",
        },
    )
    observation = CanonicalCollection(
        index_names=["id"],
        column_map={
            "Stations_id": "station_id",
            "Referenzjahr": "reference_year",
            "Qualitaetsniveau": "quality_level_id",
            "Objekt_id": "species_id",
            "Phase_id": "phase_id",
            "Eintrittsdatum": "date",
            "Eintrittsdatum_QB": "quality_byte_id",
            "Jultag": "day_of_year",
        },
    )


@dataclasses.dataclass
class DwdPhenoDatabase:
    dataset: DwdPhenoDataset
    partition: DwdPhenoPartition
    species: pd.DataFrame
    phase: pd.DataFrame
    quality_level: pd.DataFrame
    quality_byte: pd.DataFrame
    station: pd.DataFrame
    observation: pd.DataFrame

    @property
    def slots(self):
        return [self.species, self.phase, self.quality_level, self.quality_byte, self.station, self.observation]

    def info(self):
        for slot in self.slots:
            print(f"### {slot.attrs['name']}")
            slot.info()
            print()

    def __repr__(self):
        buffer = io.StringIO()
        with redirect_stdout(buffer) as out:
            for slot in self.slots:
                print(f"### {slot.attrs['name']}")
                print(slot)
                print()
        buffer.seek(0)
        return buffer.read()

    def with_canonical_column_names(self) -> "DwdPhenoDatabase":
        """
        Translate DWD column names to canonical english column names.
        """
        for slot in self.slots:
            thing = slot
            name = thing.attrs["name"]
            transformer = getattr(CanonicalColumnMap, name, None)
            if transformer:
                thing = thing.rename(columns=transformer.column_map)
                thing.index.names = transformer.index_names
                setattr(self, name, thing)
        return self

    def to_sql(self, dsn: str):
        """
        Export data to RDBMS/SQL database.
        """
        engine = create_engine(dsn)
        with engine.connect() as connection:
            connection.execute(sa.text("DROP VIEW IF EXISTS dwd_phenology;"))
            connection.commit()

        for slot in self.slots:
            name = slot.attrs["name"]
            table_name = f"dwd_{name}"
            slot.to_sql(name=table_name, con=engine, if_exists="replace")

        self.to_sql_create_view(engine)

    def to_sql_create_view(self, engine: Engine):

        """
        createview = CreateView('viewname', t.select().where(t.c.id > 5))
        engine.execute(createview)
        return
        """

        with engine.connect() as connection:
            connection.execute(sa.text("DROP VIEW IF EXISTS dwd_phenology;"))
            connection.execute(sa.text("""
CREATE VIEW dwd_phenology AS
   SELECT
      dwd_observation.source,
      dwd_observation.dataset,
      dwd_observation.partition,
      dwd_station.station_name,
      dwd_station.station_name || ', ' ||
          dwd_station.area_group || ', ' ||
          dwd_station.area || ', ' ||
          dwd_station.state
          AS station_full,
      dwd_observation.date,
      dwd_observation.day_of_year,
      dwd_species.species_name_en,
      dwd_species.species_name_de,
      dwd_phase.phase_name_en,
      dwd_phase.phase_name_de,
      dwd_quality_level.description AS quality_level,
      dwd_quality_byte.description AS quality_byte,
      dwd_observation.reference_year,
      dwd_station.latitude,
      dwd_station.longitude,
      dwd_station.altitude,
      dwd_station.area_group_code,
      dwd_station.area_group,
      dwd_station.area_code,
      dwd_station.area,
      dwd_station.state,
      dwd_station.station_date_abandoned
   FROM
      dwd_observation, dwd_station, dwd_species, dwd_phase, dwd_quality_level, dwd_quality_byte
   WHERE true
      AND dwd_observation.station_id=dwd_station.id
      AND dwd_observation.species_id=dwd_species.id
      AND dwd_observation.phase_id=dwd_phase.id
      AND dwd_observation.quality_level_id=dwd_quality_level.id
      AND dwd_observation.quality_byte_id=dwd_quality_byte.id
            """))
            connection.commit()
