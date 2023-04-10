import json
import sys

import pytest
from datadiff.tools import assert_equal

from tests.util import run_command


def test_cli_list_species(capsys):
    """
    CLI test: Verify the `list-species` subcommand works.
    """
    run_command("phenodata list-species --source=dwd --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    first = {
      "Objekt_ID": 25,
      "Objekt": "Rüben",
      "Objekt_englisch": "beet",
      "Objekt_latein": "Beta vulgaris"
    }
    assert_equal(response[0], first)


def test_cli_list_phases(capsys):
    """
    CLI test: Verify the `list-phases` subcommand works.
    """
    run_command("phenodata list-phases --source=dwd --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    first = {
      "Phase_ID": 1,
      "Phase": "Ergrünen Beginn",
      "Phase_englisch": "beginning of turning green"
    }
    assert_equal(response[0], first)


def test_cli_list_quality_levels(capsys):
    """
    CLI test: Verify the `list-quality-levels` subcommand works.
    """
    run_command("phenodata list-quality-levels --source=dwd --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    reference = [
      {
        "Qualitaetsniveau": 1,
        "Beschreibung": "nur formale Prüfung beim Entschlüsseln und Laden"
      },
      {
        "Qualitaetsniveau": 7,
        "Beschreibung": "in ROUTINE geprüft, aber keine Korrekturen (z.B. RR_UN vor Korrektur)"
      },
      {
        "Qualitaetsniveau": 10,
        "Beschreibung": "in ROUTINE geprüft, routinemäßige Korrektur beendet"
      }
    ]
    assert_equal(response, reference)


@pytest.mark.skipif(sys.platform == "linux", reason="Charset encoding weirdness. Works on macOS.")
def test_cli_list_quality_bytes(capsys):
    """
    CLI test: Verify the `list-quality-bytes` subcommand works.
    """
    run_command("phenodata list-quality-bytes --source=dwd --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    reference = [
      {
        "Qualiaetsbyte": 0,
        "Beschreibung": "Feldwert ungeprüft"
      },
      {
        "Qualiaetsbyte": 1,
        "Beschreibung": "Feldwert nicht beanstandet"
      },
      {
        "Qualiaetsbyte": 2,
        "Beschreibung": "Feldwert korrigiert"
      },
      {
        "Qualiaetsbyte": 3,
        "Beschreibung": "Feldwert trotz Beanstandung bestätigt"
      },
      {
        "Qualiaetsbyte": 5,
        "Beschreibung": "Feldwert zweifelhaft"
      },
      {
        "Qualiaetsbyte": 7,
        "Beschreibung": "ungültiges Eintrittsdatum, z.B. 31. April, wird automatisch"
      },
      {
        "Qualiaetsbyte": 8,
        "Beschreibung": "Feldwert falsch"
      }
    ]
    assert_equal(response, reference)


def test_cli_list_filenames_immediate_recent(capsys):
    """
    CLI test: Verify the `list-filenames` subcommand works.
    """
    run_command("phenodata list-filenames --source=dwd --dataset=immediate --partition=recent")

    out, err = capsys.readouterr()
    response = out.splitlines()

    assert_equal(response[0], "PH_Sofortmelder_Landwirtschaft_Kulturpflanze_Dauergruenland_akt.txt")
    assert_equal(response[-1], "PH_Sofortmelder_Wildwachsende_Pflanze_Wiesen-Fuchsschwanz_akt.txt")


def test_cli_list_filenames_immediate_historical(capsys):
    """
    CLI test: Verify the `list-filenames` subcommand works.
    """
    run_command("phenodata list-filenames --source=dwd --dataset=immediate --partition=historical")

    out, err = capsys.readouterr()
    response = out.splitlines()

    assert_equal(response[0], "PH_Sofortmelder_Landwirtschaft_Kulturpflanze_Dauergruenland_1979_2021_hist.txt")
    assert_equal(response[-1], "PH_Sofortmelder_Wildwachsende_Pflanze_Wiesen-Fuchsschwanz_1979_2021_hist.txt")


def test_cli_list_filenames_annual_recent(capsys):
    """
    CLI test: Verify the `list-filenames` subcommand works.
    """
    run_command("phenodata list-filenames --source=dwd --dataset=annual --partition=recent")

    out, err = capsys.readouterr()
    response = out.splitlines()

    assert_equal(response[0], "PH_Jahresmelder_Landwirtschaft_Kulturpflanze_Dauergruenland_akt.txt")
    assert_equal(response[-1], "PH_Jahresmelder_Wildwachsende_Pflanze_Zweigriffliger_Weissdorn_akt.txt")


def test_cli_list_filenames_annual_historical(capsys):
    """
    CLI test: Verify the `list-filenames` subcommand works.
    """
    run_command("phenodata list-filenames --source=dwd --dataset=annual --partition=historical")

    out, err = capsys.readouterr()
    response = out.splitlines()

    assert_equal(response[0], "PH_Jahresmelder_Landwirtschaft_Kulturpflanze_Dauergruenland_1936_2021_hist.txt")
    assert_equal(response[-1], "PH_Jahresmelder_Wildwachsende_Pflanze_Zweigriffliger_Weissdorn_1936_2021_hist.txt")


def test_cli_list_urls_immediate_recent(capsys):
    """
    CLI test: Verify the `list-urls` subcommand works.
    """
    run_command("phenodata list-urls --source=dwd --dataset=immediate --partition=recent")

    out, err = capsys.readouterr()
    response = out.splitlines()

    assert response[0].startswith("ftp://opendata.dwd.de/climate_environment/CDC/observations_germany/phenology/immediate_reporters/crops/recent")
