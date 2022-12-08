# =========================================================================

# Module: ioapps/tests/test_netcdf4_interface.py

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

    test_netcdf4_interface.py

Description
-----------

    This module provides unit-tests for the respective
    netcdf4_interface module functions.

Classes
-------

    TestNetCDF4Methods()

        This is the base-class object for all netcdf4_interface
        unit-tests; it is a sub-class of TestCase.

Requirements
------------

- pytest; https://docs.pytest.org/en/7.2.x/

- pytest-order; https://github.com/pytest-dev/pytest-order

Author(s)
---------

    Henry R. Winterbottom; 30 November 2022

History
-------

    2022-11-30: Henry Winterbottom -- Initial implementation.

"""

# ----

import numpy
import os
import pytest

from ioapps import netcdf4_interface
from tools import fileio_interface
from tools import parser_interface
from unittest import TestCase

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class TestNetCDF4Methods(TestCase):
    """
    Description
    -----------

    This is the base-class object for all netcdf4_interface
    unit-tests; it is a sub-class of TestCase.

    """

    def setUp(self):
        """
        Description
        -----------

        This method defines the base-class attributes for all
        netcdf4_interface unit-tests.

        """

        # Define the base-class attributes.
        (self.ncdim_obj, self.ncvar_obj) = [
            parser_interface.object_define() for i in range(2)
        ]
        self.ncfile = os.path.join(os.getcwd(), "tests", "ncwrite.nc")
        print("I AM IN PATH %s" % self.ncfile)
        self.ncfrmt = "NETCDF4_CLASSIC"

        # Build the Python object containing the netCDF-formatted file
        # dimension(s) attribute(s).
        (self.ncdim_name, self.ncdim_value) = ("nlocs", 10)
        self.ncdim_obj = parser_interface.object_setattr(
            object_in=self.ncdim_obj, key=self.ncdim_name, value=self.ncdim_value
        )

        # Build the Python object containing the netCDF-formatted file
        # variable attributes.
        self.ncvarname = "locations"
        ncvar = numpy.random.rand(self.ncdim_value)
        ncvar_dict = {
            self.ncvarname: {
                "type": "float",
                "varname": self.ncvarname,
                "dims": self.ncdim_name,
                "values": ncvar,
            }
        }

        for ncvar in ncvar_dict.keys():
            dict_in = dict()
            for item in ncvar_dict[ncvar].keys():
                value = parser_interface.dict_key_value(
                    dict_in=ncvar_dict[ncvar], key=item, no_split=True
                )
                dict_in[item] = value

            self.ncvar_obj = parser_interface.object_setattr(
                object_in=self.ncvar_obj, key=ncvar, value=dict_in
            )

        # Check whether the netCDF-formatted file exists; if so,
        # define the netCDF variable array; this will be used for the
        # subsequent netCDF reader methods.
        exist = fileio_interface.fileexist(path=self.ncfile)
        if exist:

            # Define the netCDF variable array.
            self.ncvar = netcdf4_interface.ncreadvar(
                ncfile=self.ncfile,
                ncvarname=self.ncvarname,
                ncfrmt=self.ncfrmt,
                from_ncgroup=False,
            )

        # Define the message to accompany any unit-test failures.
        self.unit_test_msg = (
            "The unit-test for netcdf4_interface function {0} " "failed."
        )

    @pytest.mark.order(100)
    def test_cleanup(self):
        """
        Description
        -----------

        This method removes the netCDF-formatted file used for the
        respective netcdf4_interface function unit-tests; this is not
        an actual unit-test but is simply used to remove the
        netCDF-formatted file following the completion of the actual
        (i.e., valid) unit-tests; this should be the last test that is
        executed by pytest.

        """

        # Define the list of (the) netCDF-formatted file(s) to be
        # removed.
        filelist = [self.ncfile]

        # Remove the specified netCDF-formatted file(s).
        fileio_interface.removefiles(filelist=filelist)

    @pytest.mark.order(2)
    def test_nccheck(self):
        """
        Description
        -----------

        This method provides a unit-test for the netcdf4_interface
        nccheck function.

        """

        # Check that the netCDF file path is a netCDF-formatted file.
        nccheck = netcdf4_interface.nccheck(ncfile=self.ncfile, ncfrmt=self.ncfrmt)

        self.assertTrue(nccheck, msg=self.unit_test_msg.format("nccheck"))

    @pytest.mark.order(3)
    def test_ncreaddim(self):
        """
        Description
        -----------

        This method provides a unit-test for the netcdf4_interface
        ncreaddim function.

        """

        # Read the dimension variable from the netCDF-formatted file.
        ncdim = netcdf4_interface.ncreaddim(
            ncfile=self.ncfile, ncdimname=self.ncdim_name, ncfrmt=self.ncfrmt
        )

        self.assertTrue(
            ncdim == self.ncdim_value, msg=self.unit_test_msg.format("ncreaddim")
        )

    @pytest.mark.order(3)
    def test_ncreadvar(self):
        """
        Description
        -----------

        This smethod provides a unit-test for the netcdf4_interface
        ncwrite function.

        """

        # Read the netCDF variable from the netCDF-formatted file.
        ncvar = netcdf4_interface.ncreadvar(
            ncfile=self.ncfile,
            ncvarname=self.ncvarname,
            ncfrmt=self.ncfrmt,
            from_ncgroup=False,
        )

        assert all(
            [a == b for (a, b) in zip(list(self.ncvar), list(ncvar))]
        ), self.unit_test_msg.format("ncreadvar")

    @pytest.mark.order(3)
    def test_ncvarexist(self):
        """
        Description
        -----------

        This smethod provides a unit-test for the netcdf4_interface
        ncvarexist function.

        """

        # Check that the netCDF variable exists within the
        # netCDF-formatted file.
        ncvarexist = netcdf4_interface.ncvarexist(
            ncfile=self.ncfile, ncvarname=self.ncvarname, ncfrmt=self.ncfrmt
        )

        self.assertTrue(ncvarexist, msg=(self.unit_test_msg.format("ncvarexist")))

        ncvarexist = netcdf4_interface.ncvarexist(
            ncfile=self.ncfile, ncvarname="dummy_test_var", ncfrmt=self.ncfrmt
        )

        self.assertTrue(not ncvarexist, msg=(self.unit_test_msg.format("ncvarexist")))

    @pytest.mark.order(1)
    def test_ncwrite(self):
        """
        Description
        -----------

        This method provides a unit-test for the netcdf4_interface
        ncwrite function.

        """

        # Write the netCDF-formatted file.
        netcdf4_interface.ncwrite(
            ncfile=self.ncfile,
            ncdim_obj=self.ncdim_obj,
            ncvar_obj=self.ncvar_obj,
            ncfrmt=self.ncfrmt,
        )

        assert True, self.unit_test_msg.format("ncwrite")

        # Check that the netCDF-formatted file exists.
        exist = fileio_interface.fileexist(path=self.ncfile)
        self.assertTrue(
            exist,
            msg=(
                "The netCDF-formatted file {0} does " "not exist.".format(self.ncfile)
            ),
        )


# ----

if __name__ == "__main__":
    unittest.main()
