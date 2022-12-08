# =========================================================================

# Module: ioapps/tests/test_tarball_interface.py

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

    test_tarfile_interface.py

Description
-----------

    This module provides unit-tests for the respective
    tarfile_interface module functions.

Classes
-------

    TestTarFileMethods()

        This is the base-class object for all tarfile_interface
        unit-tests; it is a sub-class of TestCase.

Requirements
------------

- pytest; https://docs.pytest.org/en/7.2.x/

- pytest-order; https://github.com/pytest-dev/pytest-order

Author(s)
---------

    Henry R. Winterbottom; 01 December 2022

History
-------

    2022-12-01: Henry Winterbottom -- Initial implementation.

"""

# ----

import os
import pytest
import subprocess

from ioapps import tarfile_interface
from tools import fileio_interface
from unittest import TestCase

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class TesTarFileMethods(TestCase):
    """
    Description
    -----------

    This is the base-class object for all tarfile_interface
    unit-tests; it is a sub-class of TestCase.

    """

    def setUp(self):
        """
        Description
        -----------

        This method defines the base-class attributes for all
        tarball_interface unit-tests.

        """

        # Define the base-class attributes.
        self.nmems = 5
        self.dirpath = os.getcwd()
        self.tarball = os.path.join(self.dirpath, "tests", "member_files.tar")

        # Define and create the local files to compose the tarball.
        self.filelist = list()
        for mem in range(self.nmems):

            # Create the respective member file for the tarball.
            filepath = os.path.join(
                self.dirpath, "tests", "member_file.%03d.file" % mem
            )
            self.filelist.append(filepath)
            fileio_interface.touch(path=filepath)

            # Define the message to accompany any unit-test failures.
        self.unit_test_msg = (
            "The unit-test for tarball_interface function {0} " "failed."
        )

    @pytest.mark.order(100)
    def test_cleanup(self):
        """
        Description
        -----------

        This method removes the tarball file and the respective member
        files for the respective tarfile_interface unit-tests; this is
        not an actual unit-test but is simply used to remove the the
        respective files following the completion of the actual (i.e.,
        valid) unit-tests; this should be the last test that is
        executed by pytest.

        """

        filelist = self.filelist
        filelist.append(self.tarball)

        # Remove the specified files.
        fileio_interface.removefiles(filelist=filelist)

    @pytest.mark.order(2)
    def test_read_tarfile(self):
        """
        Description
        -----------

        This method provides a unit-test for the tarfile_interface
        read_tarfile fnuction.

        """

        # Read the tarball file and extract the respective member
        # files.
        tarfile_interface.read_tarfile(path=self.dirpath, tarball_path=self.tarball)

        assert True

        # Check that the respective member files exist.
        for filename in self.filelist:

            exist = fileio_interface.fileexist(path=filename)

            self.assertTrue(exist, msg=(self.unit_test_msg.format("read_tarfile")))

    @pytest.mark.order(1)
    def test_write_tarfile(self):
        """
        Description
        -----------

        This method provides a unit-test for the tarfile_interface
        write_tarfile fnuction.

        """

        # Create the tarball file from the respective member files.
        tarfile_interface.write_tarfile(
            path=self.dirpath, tarball_path=self.tarball, filelist=self.filelist
        )

        assert True

        # Check that the tarball file exists (i.e., was created).
        exist = fileio_interface.fileexist(path=self.tarball)

        self.assertTrue(exist, msg=(self.unit_test_msg.format("write_tarfile")))

        # Remove the member files.
        fileio_interface.removefiles(filelist=self.filelist)


# ----


if __name__ == "__main__":
    unittest.main()
