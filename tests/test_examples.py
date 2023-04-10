import os


def test_example_stations(capfd):
    os.system("python examples/stations.py")

    out, err = capfd.readouterr()
    assert "Int64Index: 323 entries" in out
    assert "Data columns (total 10 columns)" in out
    assert "Stationsname" in out
    assert "[323 rows x 10 columns]" in out


def test_example_observations(capfd):
    os.system("python examples/observations.py")

    out, err = capfd.readouterr()
    assert "Int64Index: 6 entries" in out
    assert "Data columns (total 8 columns)" in out
    assert "Stations_id" in out
