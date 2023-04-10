import json

from datadiff.tools import assert_equal

from tests.util import run_command




def test_cli_forecast_immediate_recent(capsys):
    """
    CLI test: Verify the `forecast` subcommand works.
    """
    run_command("phenodata forecast --source=dwd --dataset=immediate --partition=recent --filename=Hasel --station-id=7521,7532 --humanize --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    first = {
        "Jahr": 2023,
        "Datum": "2023-02-26",
        "Tag": 57,
        "Spezies": "common hazel",
        "Phase": "beginning of flowering",
        "Station": "Norder-Hever-Koog, Schleswig-Holstein"
    }
    assert_equal(response[0], first)


def test_cli_forecast_annual_recent(capsys):
    """
    CLI test: Verify the `forecast` subcommand works, also select German.

    Event sequence for each species
    -------------------------------
    Forecast of all observations at station "Berlin-Dahlem".
    Use all species of the "primary group" (dito).
    Sort by species and date, ascending.

    """
    run_command("""
    phenodata forecast \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Apfel \
        --station-id=12132 \
        --humanize --language=german \
        --sort=Spezies,Datum \
        --format=json
    """)

    out, err = capsys.readouterr()
    response = json.loads(out)

    first = {
        "Jahr": 2023,
        "Datum": "2023-04-04",
        "Tag": 94,
        "Spezies": "Apfel, frühe Reife",
        "Phase": "Austrieb Beginn",
        "Station": "Berlin-Dahlem, Berlin"
    }
    assert_equal(response[0], first)
