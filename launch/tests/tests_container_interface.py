# =========================================================================

# Module: launch/tests/test_container_interface.py

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

from launch import container_interface
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
        dirpath = os.getcwd()
        self.build_sfd_yaml = os.path.join(dirpath, "tests", "test_files",
                                           "build.hello_world.yaml")

    @pytest.mark.order(1)
    def test_build_sfd(self):
        """ """

        # Build the Singularity image from the Docker containerized
        # image.
        build_dict = fileio_interface.read_yaml(yaml_file=self.build_sfd_yaml)
        container_interface.build_sfd(build_dict=build_dict)

        assert True

# ----


if __name__ == "__main__":
    unittest.main()
