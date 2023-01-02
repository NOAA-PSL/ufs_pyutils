# =========================================================================

# Module: execute/tests/test_container_interface.py

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

"""

# ----

import os
import pytest

from confs.yaml_interface import YAML
from execute import container_interface
from tools import fileio_interface
from tools import parser_interface
from unittest import TestCase

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class TestContainerMethods(TestCase):
    """


    """

    def setUp(self):
        """

        """

        # Define the base-class attributes.
        self.dirpath = os.getcwd()
        yaml_file = os.path.join(self.dirpath, "tests", "test_files",
                                 "test.hello_world.yaml")
        self.yaml_dict = YAML().read_yaml(yaml_file=yaml_file)

        # Define the message to accompany any unit-test failures.
        self.unit_test_msg = (
            "The unit-test for container_interface function {0} " "failed."
        )

    @pytest.mark.order(1)
    def test_build_sfd_local(self):
        """ """

        # Build the Singularity image from the Docker containerized
        # image.
        build_dict = parser_interface.dict_key_value(
            dict_in=self.yaml_dict, key='hello_world_sfd')

        (stderr, stdout) = [os.path.join(self.dirpath, "tests", 'hello_world_sfd.err'),
                            os.path.join(self.dirpath, "tests",
                                         'hello_world_sfd.out')
                            ]

        sif_name = container_interface.build_sfd_local(build_dict=build_dict,
                                                       stderr=stderr, stdout=stdout)

        assert True

        # Check that the Singularity image exists locally.
        exist = fileio_interface.fileexist(path=sif_name)

        self.assertTrue(exist, msg=(
            self.unit_test_msg.format('build_sfd_local')))

    @pytest.mark.order(100)
    def test_cleanup(self):
        """
        Description
        -----------

        This method removes the Singularity container image(s)
        built/used for the respective container_interface function
        unit-tests.

        """

        # Define the list of (the) netCDF-formatted file(s) to be
        # removed.
        filelist = [item for item in
                    fileio_interface.dircontents(path=os.path.join(self.dirpath, "tests")
                                                 if "hello_world_sfd" in item]

        # Remove the specified netCDF-formatted file(s).
        fileio_interface.removefiles(filelist=filelist)


# ----
if __name__ == "__main__":
    unittest.main()
