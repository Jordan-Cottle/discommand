""" Test module for project meta data. """
from subprocess import run, PIPE

from discommand import __version__


def test_version():
    """Check version of package matched project meta data."""
    poetry_version = run(
        "poetry version -s", stdout=PIPE, check=True, shell=True, text=True
    ).stdout.strip()
    assert __version__ == poetry_version
