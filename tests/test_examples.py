import os
import sys


def test_example_stations(capfd):
    os.system(f"{sys.executable} examples/stations.py")

    out, err = capfd.readouterr()
    assert "Index: 323 entries" in out
    assert "Data columns (total 10 columns)" in out
    assert "Stationsname" in out
    assert "[323 rows x 10 columns]" in out


def test_example_observations(capfd):
    os.system(f"{sys.executable} examples/observations.py")

    out, err = capfd.readouterr()
    assert "Index: 6 entries" in out
    assert "Data columns (total 8 columns)" in out
    assert "Stations_id" in out
