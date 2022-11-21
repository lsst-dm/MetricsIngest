# This file is part of MetricsIngest package.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# coding: utf-8
"""Test make-dispatch-sh"""

import unittest
import os
from os import environ
from pathlib import Path

from tempfile import TemporaryDirectory

from lsst.Metrics.MIUtils import MIUtils

TEST_DATA_PATH = Path(
    environ["METRICS_DIR"], "tests", "data", "minput.yaml"
)

TEST_MAKE_JS_NAME = "make-dispatch-sh"
CURR_DIR = os.getcwd()


class TestMakeDispatchSh(unittest.TestCase):
    def test_make_dispatch_sh(self):
        miu = MIUtils(TEST_DATA_PATH)

        with TemporaryDirectory() as temp_dir:
            test_dir = Path(temp_dir)
            os.chdir(test_dir)
            " Now create the dispatch.sh script"
            miu.make_dispatch_sh()
            "this creates dispatch.sh  file in tmp directory"
            comp_file = Path(
                environ["METRICS_DIR"], "tests", "data", "dispatch.sh")
            test_file = os.path.realpath("./dispatch.sh")
            test_lines = list()
            created_lines = list()
            for line in open(comp_file, 'r'):
                test_lines.append(line)
            for line in open(test_file, 'r'):
                created_lines.append(line)

            self.assertEqual(len(test_lines), len(created_lines))
            for (line1, line2) in zip(test_lines, created_lines):
                self.assertEqual(line1, line2)