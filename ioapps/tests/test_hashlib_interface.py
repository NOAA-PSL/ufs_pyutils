# =========================================================================

# Module: ioapps/tests/test_hashlib_interface.py

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

    test_hashlib_interface.py

Description
-----------

    This module provides unit-tests for the respective
    hashlib_interface module functions.

Classes
-------

    TestHashLibMethods()

        This is the base-class object for all hashlib_interface
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

from ioapps import hashlib_interface
from tools import fileio_interface
from tools import parser_interface
from unittest import TestCase

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

# Define the respective checkum/hash level types; the dictionary keys
# are the checksum/hash algorithm constructs for the Python hashlib
# library (see
# (https://docs.python.org/3/library/hashlib.html#hash-algorithms) and
# the dictionary values correspond to the UNIX-based platform
# executable to compute the respective hash index.
hash_types_dict = {'md5': 'md5sum',
                   'sha1': 'sha1sum',
                   'sha224': 'sha224sum',
                   'sha256': 'sha256sum',
                   'sha384': 'sha384sum',
                   'sha512': 'sha512sum'
                   }

# ----


class TestHashLibMethods(TestCase):
    """
    Description
    -----------

    This is the base-class object for all hashlib_interface
    unit-tests; it is a sub-class of TestCase.

    """

    def setUp(self):
        """
        Description
        -----------

        This method defines the base-class attributes for all
        hashlib_interface unit-tests.

        """

        # Define the base-class attributes.
        self.hash_obj = parser_interface.object_define()

        # Define and create a local file for which to compute the
        # respective checksum/hash levels.
        dirpath = os.getcwd()
        self.hashlib_file = os.path.join(dirpath, 'hashlib.file')
        with open(self.hashlib_file, 'w') as f:
            f.write('This is a hashlib_interface test file.')

        # Compute the checksum/hash level for the respective file and
        # build the base-class attribute hash_obj.
        for hash_type in hash_types_dict.keys():

            # Define the UNIX-based platform corresponding to the
            # respective checksum/hash algorithm.
            algorithm = parser_interface.dict_key_value(
                dict_in=hash_types_dict, key=hash_type, no_split=True)

            # Compute the checksum/hash level for the respective file.
            cmd = ['{0}'.format(algorithm),
                   '{0}'.format(self.hashlib_file)
                   ]

            self.hashlib_stdout = os.path.join(dirpath, 'hashlib.out')
            stdout = open(self.hashlib_stdout, 'w')
            proc = subprocess.Popen(cmd, stdout=stdout)
            proc.communicate()
            proc.wait()
            stdout.close()

            # Collect the checksum/hash level value for the respective
            # file and update the base-class attribute object
            # hash_obj.
            with open(self.hashlib_stdout, 'r') as f:
                hash_info = f.read().split()
            hash_index = hash_info[0]
            self.hash_obj = parser_interface.object_setattr(
                object_in=self.hash_obj, key=hash_type, value=hash_index)

        # Define the message to accompany any unit-test failures.
        self.unit_test_msg = ('The unit-test for hashlib_interface function {0} '
                              'failed.')

    @pytest.mark.order(100)
    def test_cleanup(self):
        """
        Description
        -----------

        This method removes the test files used for the respective
        hashlib_interface function unit-tests; it is not an actual
        unit-test but is simply used to remove the test files file
        following the completion of the actual (i.e., valid)
        unit-tests; this should be the last test that is executed by
        pytest.

        """

        # Define the list of (the) test file(s) to be removed.
        filelist = [self.hashlib_file,
                    self.hashlib_stdout
                    ]

        # Remove the specified files.
        fileio_interface.removefiles(filelist=filelist)

    @pytest.mark.order(1)
    def test_get_hash(self):
        """
        Description
        -----------

        This method provides a unit-test for the hashlib_interface
        get_hash function.

        """

        # For each allowable checkum/hash level type, define the index
        # computed by the corresponding UNIX-like platform value and
        # that computed by the hashlib_interface get_hash function.
        for hash_level in vars(self.hash_obj):

            # Define the checksum/hash level value for the respective
            # algorithm type as determined from the hashlib_interface
            # get_hash function.
            hash_index = hashlib_interface.get_hash(
                filepath=self.hashlib_file, hash_level=hash_level)

            # Define the corresponding checksum/hash level computed by
            # the corresponding UNIX-like platform.
            unix_index = parser_interface.object_getattr(
                object_in=self.hash_obj, key=hash_level)

            assert(hash_index == unix_index), \
                self.unit_test_msg.format('get_hash')


# ----


if __name__ == '__main__':
    unittest.main()
