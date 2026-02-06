import json

import marko
from datadiff.tools import assert_equal

from tests.util import run_command




def test_cli_observations_immediate_recent_filter_station_id(capsys):
    """
    CLI test: Verify the `observations` subcommand works.
    """
    run_command("phenodata observations --source=dwd --dataset=immediate --partition=recent --filename=Hasel --station-id=19475 --humanize --show-ids --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    first = {
        "Jahr": 2024,
        "Datum": "2024-01-13",
        "Tag": 13,
        "Spezies": "common hazel [113]",
        "Phase": "beginning of flowering [5]",
        "Station": "Angermünde (Ph), Brandenburg [19475]",
        "QS-Level": "Load time checks [1]",
        "QS-Byte": "Feldwert nicht beanstandet [1]"
    }
    assert_equal(response[0], first)


def test_cli_observations_immediate_recent_filter_station_name(capsys):
    """
    CLI test: Verify the `observations` subcommand works.
    """
    run_command("phenodata observations --source=dwd --dataset=annual --partition=recent --filename=Hasel --station=berlin,brandenburg --humanize --sort=Datum --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    first = {
        "Jahr": 2023,
        "Datum": "2023-02-02",
        "Tag": 33,
        "Spezies": "common hazel",
        "Phase": "beginning of flowering",
        "Station": "Dahlwitz-Hoppegarten, Brandenburg",
        "QS-Level": "ROUTKLI validated and corrected",
        "QS-Byte": "Feldwert korrigiert"
    }
    assert_equal(response[0], first)


def test_cli_observations_immediate_historical(capsys):
    """
    CLI test: Verify the `observations` subcommand works.
    """
    run_command("phenodata observations --source=dwd --dataset=immediate --partition=historical --filename=Hasel --station=berlin,brandenburg --humanize --sort=Datum --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    first = {
        "Jahr": 2007,
        "Datum": "2007-01-12",
        "Tag": 12,
        "Spezies": "common hazel",
        "Phase": "beginning of flowering",
        "Station": "Prenzlau, Brandenburg",
        "QS-Level": "ROUTKLI validated",
        "QS-Byte": "Feldwert nicht beanstandet"
    }
    assert_equal(response[0], first)


def test_cli_observations_annual_recent(capsys):
    """
    CLI test: Verify the `observations` subcommand works.
    """
    run_command("phenodata observations --source=dwd --dataset=annual --partition=recent --filename=Hasel --station=berlin,brandenburg --humanize --sort=Datum --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    first = {
        "Jahr": 2023,
        "Datum": "2023-02-02",
        "Tag": 33,
        "Spezies": "common hazel",
        "Phase": "beginning of flowering",
        "Station": "Dahlwitz-Hoppegarten, Brandenburg",
        "QS-Level": "ROUTKLI validated and corrected",
        "QS-Byte": "Feldwert korrigiert"
    }
    assert_equal(response[0], first)


def test_cli_observations_annual_historical(capsys):
    """
    CLI test: Verify the `observations` subcommand works.
    """
    run_command("phenodata observations --source=dwd --dataset=annual --partition=historical --filename=Hasel --station=berlin,brandenburg --humanize --sort=Datum --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    first = {
        "Jahr": 1936,
        "Datum": "1936-03-10",
        "Tag": 70,
        "Spezies": "common hazel",
        "Phase": "beginning of flowering",
        "Station": "Berlin-Dahlem, Berlin",
        "QS-Level": "Load time checks",
        "QS-Byte": "Feldwert nicht beanstandet"
    }
    assert_equal(response[0], first)


def test_cli_observations_filter_year(capsys):
    """
    CLI test: Verify the `observations` subcommand works, with filtering by year.
    """
    run_command("phenodata observations --source=dwd --dataset=immediate --partition=recent --filename=Hasel --station-id=7521,7532 --year=2022,2023 --humanize --show-ids --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    first = {
        "Jahr": 2023,
        "Datum": "2023-02-25",
        "Tag": 56,
        "Spezies": "common hazel [113]",
        "Phase": "beginning of flowering [5]",
        "Station": "Norder-Hever-Koog, Schleswig-Holstein [7532]",
        "QS-Level": "ROUTKLI validated [7]",
        "QS-Byte": "Feldwert nicht beanstandet [1]"
    }
    assert_equal(response[0], first)


def test_cli_observations_filter_species_id(capsys):
    """
    CLI test: Verify the `observations` subcommand works, with filtering by species-id.
    """
    run_command("phenodata observations --source=dwd --dataset=immediate --partition=recent --filename=Hasel --station-id=7521,7532 --species-id=113,127 --humanize --show-ids --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    first = {
        "Jahr": 2023,
        "Datum": "2023-02-25",
        "Tag": 56,
        "Spezies": "common hazel [113]",
        "Phase": "beginning of flowering [5]",
        "Station": "Norder-Hever-Koog, Schleswig-Holstein [7532]",
        "QS-Level": "ROUTKLI validated [7]",
        "QS-Byte": "Feldwert nicht beanstandet [1]"
    }
    assert_equal(response[0], first)


def test_cli_observations_filter_invalid_readings(capsys):
    """
    CLI test: Verify the `observations` subcommand works, with filtering by quality-byte.
    """
    run_command("phenodata observations --source=dwd --dataset=immediate --partition=recent --year=2023 --filename=Hasel --quality-byte=5,6,7,8 --humanize --show-ids --format=json")

    out, err = capsys.readouterr()
    response = json.loads(out)

    first = {
        "Jahr": 2023,
        "Datum": "2023-02-14",
        "Tag": 45,
        "Spezies": "common hazel [113]",
        "Phase": "beginning of flowering [5]",
        "Station": "Hemmingstedt, Schleswig-Holstein [7807]",
        "QS-Level": "ROUTKLI validated [7]",
        "QS-Byte": "Feldwert zweifelhaft [5]"
    }
    assert_equal(first, response[0])


def test_cli_observations_filter_sql(capsys):
    """
    CLI test: Verify the `observations` subcommand works, with filtering by quality-byte.
    """
    run_command("""
    phenodata observations \
        --source=dwd --dataset=annual --partition=recent \
        --filename=Hasel \
        --year=2022 \
        --species-preset=mellifera-de-primary --phase="beginning of flowering" \
        --humanize --language=german \
        --sql="SELECT * FROM data WHERE Station LIKE '%Berlin%' ORDER BY Datum" \
        --format=json
    """)

    out, err = capsys.readouterr()
    response = json.loads(out)

    first = {
        "Jahr": 2022,
        "Datum": "2022-01-11",
        "Tag": 11,
        "Spezies": "Hasel",
        "Phase": "Blüte Beginn",
        "Station": "Berlin-Marienfelde, Berlin",
        "QS-Level": "ROUTKLI geprüft und korrigiert",
        "QS-Byte": "Feldwert nicht beanstandet"
    }
    assert_equal(response[0], first)


def test_cli_observations_format_csv(capsys):
    """
    CLI test: Verify the `observations` subcommand works with CSV output.
    """
    run_command("phenodata observations --source=dwd --dataset=immediate --partition=recent --filename=Hasel --station-id=19475 --humanize --show-ids --format=csv")

    out, err = capsys.readouterr()
    assert out.startswith("""
Jahr,Datum,Tag,Spezies,Phase,Station,QS-Level,QS-Byte
2024,2024-01-13,13,common hazel [113],beginning of flowering [5],"Angermünde (Ph), Brandenburg [19475]",Load time checks [1],Feldwert nicht beanstandet [1]
2025,2025-02-03,34,common hazel [113],beginning of flowering [5],"Angermünde (Ph), Brandenburg [19475]",Load time checks [1],Feldwert nicht beanstandet [1]
2025,2025-03-28,87,common hazel [113],end of flowering in the observation area [41],"Angermünde (Ph), Brandenburg [19475]",Load time checks [1],Feldwert nicht beanstandet [1]
2026,2025-12-25,-7,common hazel [113],beginning of flowering [5],"Angermünde (Ph), Brandenburg [19475]",Load time checks [1],Feldwert nicht beanstandet [1]
    """.strip())


def test_cli_observations_format_tabular(capsys):
    """
    CLI test: Verify the `observations` subcommand works with tabular output.

    `tabular:pipe` actually yields a Markdown table, so let's validate it using a Markdown parser.
    """
    run_command("phenodata observations --source=dwd --dataset=immediate --partition=recent --filename=Hasel --station-id=19475 --humanize --show-ids --format=tabular:pipe")

    out, err = capsys.readouterr()

    html = marko.convert(out)

    assert html.startswith("<p>|   Jahr | Datum      |   Tag | Spezies")
    assert html.endswith("| Feldwert nicht beanstandet [1] |</p>\n")
