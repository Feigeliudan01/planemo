""" Provide abstractions over click testing of the
app and unittest.
"""
import os

from click.testing import CliRunner

from planemo import cli
from sys import version_info

from galaxy.tools.deps.commands import which


if version_info < (2, 7):
    from unittest2 import TestCase, skip
else:
    from unittest import TestCase, skip


EXIT_CODE_MESSAGE = ("Planemo command [%s] resulted in unexpected exit code "
                     "[%s], expected exit code [%s]]. Command output [%s]")


# More information on testing click applications at following link.
# http://click.pocoo.org/3/testing/#basic-testing
class CliTestCase(TestCase):

    def setUp(self):  # noqa
        self._runner = CliRunner()

    @property
    def _cli(self):
        return cli

    def _isolate(self):
        return self._runner.isolated_filesystem()

    def _invoke(self, command_list):
        planemo_cli = self._cli.planemo
        return self._runner.invoke(planemo_cli, command_list)

    def _check_exit_code(self, command_list, exit_code=0):
        expected_exit_code = exit_code
        result = self._invoke(command_list)
        result_exit_code = result.exit_code
        if result_exit_code != expected_exit_code:
            message = EXIT_CODE_MESSAGE % (
                " ".join(command_list),
                result_exit_code,
                expected_exit_code,
                result.output,
            )
            raise AssertionError(message)
        return result


def skip_unless_environ(var):
    if var in os.environ:
        return lambda func: func
    template = "Environment variable %s not found, dependent test skipped."
    return skip(template % var)


def skip_unless_module(module):
    available = True
    try:
        __import__(module)
    except ImportError:
        available = False
    if available:
        return lambda func: func
    return skip("Module %s could not be loaded, dependent test skipped." % module)


def skip_unless_executable(executable):
    if which(executable):
        return lambda func: func
    return skip("PATH doesn't contain executable %s" % executable)


__all__ = [
    "TestCase",
    "CliTestCase",
]
