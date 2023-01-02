# =========================================================================

# Module: confs/tests/test_yaml_interface.py

# Author: Henry R. Winterbottom

# Email: henry.winterbottom@noaa.gov

# This program is free software: you can redistribute it and/or modify
# it under the terms of the respective public license published by the
# Free Software Foundation and included with the repository within
# which this application is contained.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.

# =========================================================================

"""
Module
------

    test_yaml_interface.py

Description
-----------

    This module provides unit-tests for the respective yaml_interface
    module functions.

Classes
-------

    TestYAMLMethods()

        This is the base-class object for all yaml_interface
        unit-tests; it is a sub-class of TestCase.

Requirements
------------

- pytest; https://docs.pytest.org/en/7.2.x/

- pytest-order; https://github.com/pytest-dev/pytest-order

Author(s)
---------

    Henry R. Winterbottom; 08 December 2022

History
-------

    2022-12-08: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=undefined-variable

# ----

import os
from unittest import TestCase

import pytest
from confs import yaml_interface
from tools import fileio_interface

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class TestYAMLMethods(TestCase):
    """
    Description
    -----------

    This is the base-class object for all yaml_interface unit-tests;
    it is a sub-class of TestCase.

    """

    def setUp(self):
        """
        Description
        -----------

        This method defines the base-class attributes for all
        yaml_interface unit-tests.

        """

        # Define the base-class attributes.
        self.yaml_test_dict = {
            "OBSNAME": "obsname",
            "OBSDATAIN": "obsdatain.nc",
            "OBSDATAOUT": "obsdataout.nc",
            "OBS_VARIABLE": "obs_variable",
            "LENGTHSCALE": "200e3",
            "THRESHOLD": 5.0,
        }

        # Define the file paths required for the test method(s).
        dirpath = os.path.join(os.getcwd(), "tests")
        self.yaml_template = os.path.join(
            dirpath, "test_files", "yaml.template")
        self.yaml_check = os.path.join(dirpath, "test_files", "yaml.check")
        self.yaml_path = os.path.join(dirpath, "yaml.test")

        # Define the message to accompany any unit-test failures.
        self.unit_test_msg = "The unit-test for yaml_interface failed."

    @pytest.mark.order(100)
    def test_cleanup(self):
        """
        Description
        -----------

        This method removes the test files used for the respective
        yaml_interface function unit-tests; it is not an actual
        unit-test but is simply used to remove the test files file
        following the completion of the actual (i.e., valid)
        unit-tests; this should be the last test that is executed by
        pytest.

        """

        # Define the list of (the) test file(s) to be removed.
        filelist = [self.yaml_path]

        # Remove the specified files.
        fileio_interface.removefiles(filelist=filelist)

    @pytest.mark.order(1)
    def test_yaml(self):
        """
        Description
        -----------

        This method provides a unit-test for the yaml_interface
        module.

        """

        # Write the YAML-formatted file.
        yaml = yaml_interface.YAML()
        yaml.write_tmpl(
            yaml_dict=self.yaml_test_dict,
            yaml_template=self.yaml_template,
            yaml_path=self.yaml_path,
        )

        assert True

        # Compare the generated YAML-formatted file to the example
        # YAML-formatted file.
        with open(self.yaml_check, "r", encoding="utf-8") as file:
            yaml_check = file.read().rstrip()
        with open(self.yaml_path, "r", encoding="utf-8") as file:
            yaml_path = file.read().rstrip()

        assert yaml_check == yaml_path, self.unit_test_msg


# ----
if __name__ == "__main__":
    unittest.main()
