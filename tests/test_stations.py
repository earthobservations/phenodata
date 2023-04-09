import json

from datadiff.tools import assert_equal

from tests.util import run_command


def test_cli_stations(capsys):
    """
    CLI test: Verify the `list-stations` subcommand works.
    """
    run_command("phenodata list-stations --source=dwd --dataset=immediate --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    first = {
      "Stations_id": 662,
      "Stationsname": "Braunschweig",
      "geograph.Breite": 52.2915,
      "geograph.Laenge": 10.4464,
      "Stationshoehe": 81,
      "Naturraumgruppe_Code": 62,
      "Naturraumgruppe": "Weser-Aller-Flachland",
      "Naturraum_Code": 6230,
      "Naturraum": "Burgdorf-Peiner Geestplatten",
      "Datum Stationsaufloesung": None,
      "Bundesland": "Niedersachsen"
    }
    assert_equal(response[0], first)


nearest_station = {
    "Stations_id": 12365,
    "Stationsname": "Wansdorf",
    "Distanz": 25167.5671969595,
    "geograph.Breite": 52.65,
    "geograph.Laenge": 13.1,
    "Stationshoehe": 35,
    "Naturraumgruppe_Code": 78,
    "Naturraumgruppe": "Luchland",
    "Naturraum_Code": 7820,
    "Naturraum": "Bellin und Glin",
    "Datum Stationsaufloesung": None,
    "Bundesland": "Brandenburg"
}


def test_cli_nearest_stations(capsys):
    """
    CLI test: Verify the `nearest-stations` subcommand works.
    """
    run_command("phenodata nearest-stations --source=dwd --dataset=immediate --latitude=52.520007 --longitude=13.404954 --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    assert_equal(response[0], nearest_station)


def test_cli_nearest_station(capsys):
    """
    CLI test: Verify the `nearest-station` subcommand works.
    """
    run_command("phenodata nearest-station --source=dwd --dataset=immediate --latitude=52.520007 --longitude=13.404954 --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    assert_equal(response[0], nearest_station)


def test_cli_stations_filter_string(capsys):
    """
    CLI test: Verify the `list-stations` subcommand works, with filtering by string.
    """
    run_command("phenodata list-stations --source=dwd --dataset=annual --filter='Fränkische Alb' --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    first = {
        "Stations_id": 2895,
        "Stationsname": "Lauterhofen-Trautmannshofen",
        "geograph.Breite": 49.3442,
        "geograph.Laenge": 11.5664,
        "Stationshoehe": 585,
        "Naturraumgruppe_Code": 8,
        "Naturraumgruppe": "Fränkische Alb (Frankenalb)",
        "Naturraum_Code": 810,
        "Naturraum": "Mittlere Frankenalb",
        "Datum Stationsaufloesung": None,
        "Bundesland": "Bayern"
    }
    assert_equal(response[0], first)
