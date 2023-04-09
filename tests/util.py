import shlex
import sys

from phenodata.command import run


def run_command(command: str):
    sys.argv = shlex.split(command.strip())
    run()
