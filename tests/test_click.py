import click
from click.testing import CliRunner

from pyup.pyup import pyup


def test_without_arguments():
    runner = CliRunner()
    result = runner.invoke(pyup)
    assert result.exit_code == 2
    assert 'Error: Missing argument "source_file".' in result.output


def test_with_nonexistent_file():
    runner = CliRunner()
    result = runner.invoke(pyup, ['foo'])
    assert result.exit_code == 2
    assert 'Error: Invalid value for "source_file": Path "foo" does not exist.' in result.output
