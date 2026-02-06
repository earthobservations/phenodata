import sqlite3
import sys

import pytest
from datadiff.tools import assert_equal

from tests.util import run_command

if sys.version_info < (3, 8):
    raise pytest.skip(msg="The SQLite export feature does not work on Python 3.7", allow_module_level=True)


def test_export_sqlite_single_species(tmp_path):

    # Export annual/recent to SQLite database.
    dbpath = tmp_path / "test.sqlite"
    command = f"""
    phenodata export-observations \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel \
        --target=sqlite:///{dbpath}
        """
    run_command(command)

    # Run query to validate data.
    sql = """
    SELECT day_of_year, reference_year, source, species_name_en
    FROM dwd_phenology
    WHERE
        station_full LIKE '%Geisenheim%' AND
        species_name_en LIKE '%hazel%' AND
        phase_name_en LIKE '%flowering%'
    ORDER BY reference_year, day_of_year;    
    """
    sqlite = sqlite3.connect(dbpath)
    cursor = sqlite.execute(sql)
    results = cursor.fetchall()

    # In 2023, annual reporters did not report their observations for 2023 yet.
    assert_equal(results, [
        (8, 2024, 'dwd', 'common hazel'),
        (30, 2025, 'dwd', 'common hazel'),
    ])


def test_export_sqlite_species_group(tmp_path):

    # Export annual/recent to SQLite database.
    dbpath = tmp_path / "test.sqlite"
    command = f"""
    phenodata export-observations \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel,Sal-Weide,Winterraps \
        --target=sqlite:///{dbpath}
        """
    run_command(command)

    # Run query to validate data.
    sql = """
    SELECT
        reference_year,
        day_of_year,
        source,
        species_name_de,
        phase_name_de,
        station_name
    FROM dwd_phenology_group
    WHERE true
        AND group_name = 'mellifera-de-primary-openhive'
        AND phase_name_en LIKE '%flowering%'
        AND station_full LIKE '%müncheberg%';
    """
    sqlite = sqlite3.connect(dbpath)
    cursor = sqlite.execute(sql)
    results = cursor.fetchall()

    assert_equal(results, [
        (2023, 77, 'dwd', 'Sal-Weide', 'Blüte Beginn', 'Müncheberg (Ph)'),
        (2023, 116, 'dwd', 'Winterraps', 'Blüte Beginn', 'Müncheberg (Ph)'),
        (2024, 69, 'dwd', 'Sal-Weide', 'Blüte Beginn', 'Müncheberg (Ph)'),
        (2024, 94, 'dwd', 'Winterraps', 'Blüte Beginn', 'Müncheberg (Ph)'),
        (2025, 32, 'dwd', 'Hasel', 'Blüte Beginn', 'Müncheberg (Ph)'),
        (2025, 74, 'dwd', 'Sal-Weide', 'Blüte Beginn', 'Müncheberg (Ph)'),
    ])
