# =========================================================================

# Module: ioapps/tests/test_tcvitals_interface.py

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

    test_tcvitals_interface.py

Description
-----------

    This module provides unit-tests for the respective
    tcvitals_interface module functions.

Classes
-------

    TestTCVitalsMethods()

        This is the base-class object for all tcvitals_interface
        unit-tests; it is a sub-class of TestCase.

Requirements
------------

- pytest; https://docs.pytest.org/en/7.2.x/

- pytest-order; https://github.com/pytest-dev/pytest-order

Author(s)
---------

    Henry R. Winterbottom; 02 December 2022

History
-------

    2022-12-02: Henry Winterbottom -- Initial implementation.

"""

# ----

import filecmp
import os
import pytest

from ioapps import tcvitals_interface
from tools import fileio_interface
from tools import parser_interface
from tools.constants_interface import mps2kts
from unittest import TestCase

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

# Define the TC-vitals attributes; the dictionary keys are the
# entries and the corresponding values are the column index.
tcv_attrs_dict = {
    "tcv_center": {"idx": 0, "dtype": str},
    "tcid": {"idx": 1, "dtype": str},
    "event_name": {"idx": 2, "dtype": str},
    "time_ymd": {"idx": 3, "dtype": str},
    "time_hm": {"idx": 4, "dtype": str},
    "lat": {"idx": 5, "dtype": str},
    "lon": {"idx": 6, "dtype": str},
    "stormdir": {"idx": 7, "dtype": float},
    "stormspeed": {"idx": 8, "dtype": float},
    "mslp": {"idx": 9, "dtype": float},
    "poci": {"idx": 10, "dtype": float},
    "roci": {"idx": 11, "dtype": float},
    "vmax": {"idx": 12, "dtype": float},
    "rmw": {"idx": 13, "dtype": float},
    "NE34": {"idx": 14, "dtype": float},
    "SE34": {"idx": 15, "dtype": float},
    "SW34": {"idx": 16, "dtype": float},
    "NW34": {"idx": 17, "dtype": float},
}

# ----


class TestTCVitalsMethods(TestCase):
    """
    Description
    -----------

    This is the base-class object for all tcvitals_interface
    unit-tests; it is a sub-class of TestCase.

    """

    def setUp(self):
        """
        Description
        -----------

        This method defines the base-class attributes for all
        tcvitals_interface unit-tests.

        """

        # Define the base-class attributes.
        dirpath = os.getcwd()
        self.tcv_exfile = os.path.join(
            dirpath, "tests", "test_files", "tcvitals.syndat"
        )
        self.tcv_file = os.path.join(dirpath, "tests", "tcvitals.syndat")

        # Collect the contents of the example TC-vitals file.
        with open(self.tcv_exfile, "r") as f:
            self.tcinfo = f.read()

        # Define the message to accompany any unit-test failures.
        self.unit_test_msg = (
            "The unit-test for tcvitals_interface function {0} " "failed."
        )

    @pytest.mark.order(100)
    def test_cleanup(self):
        """Description
        -----------

        This method removes the test files used for the respective
        tcvitals_interface function unit-tests; it is not an actual
        unit-test but is simply used to remove the test files file
        following the completion of the actual (i.e., valid)
        unit-tests; this should be the last test that is executed by
        pytest.

        """

        # Define the list of (the) test file(s) to be removed.
        filelist = [self.tcv_file]

        # Remove the specified files.
        fileio_interface.removefiles(filelist=filelist)

    @pytest.mark.order(1)
    def test_write_tcvfile(self):
        """
        Description
        -----------

        This method provides a unit-test for the tcvitals_interface
        write_tcvfile function.

        """

        # Write the TC-vitals attributes to the output file to be
        # used for comparison.
        tcvitals_interface.write_tcvfile(filepath=self.tcv_file, tcvstr=self.tcinfo)

        # Compare the example file to the generated TC-vitals file.
        check = filecmp.cmp(self.tcv_exfile, self.tcv_file)

        self.assertTrue(check, msg=(self.unit_test_msg.format("write_tcvfile")))

    @pytest.mark.order(1)
    def test_write_tcvstr(self):
        """
        Description
        -----------

        This method provides a unit-test for the tcvitals_interface
        write_tcvstr function.

        """

        # For each TC event in the example TC-vitals file, build the
        # local attribute and write a TC-vitals file.
        for tc in self.tcinfo.strip().split("\n"):

            # Build the local attribute containing the TC-vitals
            # attributes for the respective TC event.
            tcvit_obj = parser_interface.object_define()
            for tcv_attr in tcv_attrs_dict.keys():

                idx = parser_interface.dict_key_value(
                    dict_in=tcv_attrs_dict[tcv_attr], key="idx", no_split=True
                )
                dtype = parser_interface.dict_key_value(
                    dict_in=tcv_attrs_dict[tcv_attr], key="dtype", no_split=True
                )

                value = dtype(tc.split()[idx])
                tcvit_obj = parser_interface.object_setattr(
                    object_in=tcvit_obj, key=tcv_attr, value=value
                )

            # Format the geographical location accordingly.
            scale = 0.1
            if "S" in tcvit_obj.lat[-1]:
                scale = -0.1
            value = float(tcvit_obj.lat[:-1]) * scale
            tcvit_obj = parser_interface.object_setattr(
                object_in=tcvit_obj, key="lat", value=value
            )

            scale = 0.1
            if "E" in tcvit_obj.lon[-1]:
                scale = -0.1
            value = float(tcvit_obj.lon[:-1]) * scale
            tcvit_obj = parser_interface.object_setattr(
                object_in=tcvit_obj, key="lon", value=value
            )

            # Scale the maximum wind speed value from knots to meters
            # per second.
            value = tcvit_obj.vmax * mps2kts
            tcvit_obj = parser_interface.object_setattr(
                object_in=tcvit_obj, key="vmax", value=value
            )

            # Write the formatted TC-vitals attributes for the
            # respective TC event.
            tcvstr = tcvitals_interface.write_tcvstr(tcvit_obj=tcvit_obj).split()[:-1]

            assert tcvstr == list(tc.split()), self.unit_test_msg.format("write_tcvstr")


# ----

if __name__ == "__main__":
    unittest.main()
