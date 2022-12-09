# =========================================================================

# Module: confs/tests/test_namelist_interface.py

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

    test_namelist_interface.py

Description
-----------

    This module provides unit-tests for the respective
    namelist_interface module functions.

Classes
-------

    TestNamelistMethods()

        This is the base-class object for all namelist_interface
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
# pylint: disable=wrong-import-order

# ----

import filecmp
import os
import pytest

from confs import namelist_interface
from tools import fileio_interface
from unittest import TestCase

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class TestNamelistMethods(TestCase):
    """
    Description
    -----------

    This is the base-class object for all namelist_interface
    unit-tests; it is a sub-class of TestCase.

    """

    def setUp(self):
        """
        Description
        -----------

        This method defines the base-class attributes for all
        namelist_interface unit-tests.

        """

        # Define the base-class attributes.
        self.nml_test_dict = {
            "TEST_STRING": "This is a test string.",
            "TEST_FLOAT1": 10.0,
            "TEST_FLOAT2": 1.0e6,
            "TEST_INT": 1,
            "TEST_COMMA_LIST": "1, 10, 100",
        }

        # Define the file paths required for the test method(s).
        dirpath = os.path.join(os.getcwd(), "tests")
        self.nml_template = os.path.join(
            dirpath, "test_files", "namelist.template")
        self.nml_check = os.path.join(dirpath, "test_files", "namelist.check")
        self.nml_path = os.path.join(dirpath, "namelist.test")

        # Define the message to accompany any unit-test failures.
        self.unit_test_msg = "The unit-test for namelist_interface failed."

    @pytest.mark.order(100)
    def test_cleanup(self):
        """
        Description
        -----------

        This method removes the test files used for the respective
        namelist_interface function unit-tests; it is not an actual
        unit-test but is simply used to remove the test files file
        following the completion of the actual (i.e., valid)
        unit-tests; this should be the last test that is executed by
        pytest.

        """

        # Define the list of (the) test file(s) to be removed.
        filelist = [self.nml_path]

        # Remove the specified files.
        fileio_interface.removefiles(filelist=filelist)

    @pytest.mark.order(1)
    def test_namelist(self):
        """
        Description
        -----------

        This method provides a unit-test for the namelist_interface
        module.

        """

        # Write the FORTRAN 90 formatted namelist file.
        namelist = namelist_interface.Namelist()
        namelist.run(
            nml_dict=self.nml_test_dict,
            nml_template=self.nml_template,
            nml_path=self.nml_path,
        )

        assert True

        # Compare the generated FORTRAN 90 formatted namelist file to
        # the example FORTRAN 90 formatted namelist file.
        check = filecmp.cmp(self.nml_path, self.nml_check)

        self.assertTrue(check, msg=self.unit_test_msg)


# ----


if __name__ == "__main__":
    unittest.main()
