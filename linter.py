#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Aparajita Fishman
# Copyright (c) 2013 Aparajita Fishman
#
# License: MIT
#

"""This module exports the PEP257 plugin linter class."""

import os

from SublimeLinter.lint import highlight, PythonLinter, util


class PEP257(PythonLinter):

    """Provides an interface to the pep257 python module/script."""

    syntax = 'python'
    cmd = 'pep257@python'
    version_args = '--version'
    version_re = r'(?P<version>\d+\.\d+\.\d+)'
    version_requirement = '>= 0.3.0'
    regex = r'^.+?:(?P<line>\d+).*:\r?\n\s*(?P<message>.+)$'
    multiline = True
    default_type = highlight.WARNING
    error_stream = util.STREAM_STDERR
    line_col_base = (1, 0)  # pep257 uses one-based line and zero-based column numbers
    tempfile_suffix = 'py'
    module = 'pep257'
    check_version = True

    # Internal
    checker = None

    def check(self, code, filename):
        """Run pep257 on code and return the output."""
        if self.checker is None:
            self.checker = self.module.PEP257Checker()

        errors = []
        for error in self.checker.check_source(code, os.path.basename(filename)):
            if getattr(error, 'code', None) is not None:
                errors.append(str(error))

        return '\n'.join(errors)
