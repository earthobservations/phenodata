import re

import pytest

from tests.util import run_command


def test_cli_info(capsys):
    """
    CLI test: Verify `phenodata info` works.
    """
    run_command("phenodata info")

    out, err = capsys.readouterr()
    assert "phenodata is an acquisition and manipulation toolkit" in out


def test_cli_version(capsys):
    """
    CLI test: Verify `phenodata info` works.
    """
    with pytest.raises(SystemExit):
        run_command("phenodata --version")

    out, err = capsys.readouterr()
    assert re.match("phenodata \d+\.\d+\.\d+.*", out)
