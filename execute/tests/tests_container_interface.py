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
        self.build_sfd_yaml = os.path.join(self.dirpath, "tests", "test_files",
                                           "build.hello_world.yaml")

        # Define the message to accompany any unit-test failures.
        self.unit_test_msg = (
            "The unit-test for container_interface function {0} " "failed."
        )

    @pytest.mark.order(1)
    def test_build_sfd_local(self):
        """ """

        # Build the Singularity image from the Docker containerized
        # image.
        yaml_dict = YAML().read_yaml(yaml_file=self.build_sfd_yaml)
        build_dict = parser_interface.dict_key_value(
            dict_in=yaml_dict, key='hello_world')

        (stderr, stdout) = [os.path.join(self.dirpath, "tests", 'hello_world.err'),
                            os.path.join(self.dirpath, "tests",
                                         'hello_world.out')
                            ]

        sif_name = container_interface.build_sfd_local(build_dict=build_dict,
                                                       stderr=stderr, stdout=stdout)

        assert True

        # Check that the Singularity image exists locally.
        exist = fileio_interface.fileexist(path=sif_name)

        self.assertTrue(exist, msg=(
            self.unit_test_msg.format('build_sfd_local')))


# ----
if __name__ == "__main__":
    unittest.main()
