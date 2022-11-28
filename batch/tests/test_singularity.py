# =========================================================================

# $$$ UNIT TEST DOCUMENTATION BLOCK

# UFS-RNR :: ush/batch/tests/test_singularity.py

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

""" """

# ----

import os

from batch import singularity
from tools import fileio_interface
from tools import parser_interface

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


def test_singularity():
    """ """

    # Define the unit-test attributes.
    path = os.getcwd()
    yaml_file = os.path.join(path, 'tests', 'singularity.yaml')
    yaml_dict = fileio_interface.read_yaml(yaml_file=yaml_file)
    exec_dict = parser_interface.dict_key_value(
        dict_in=yaml_dict, key='lolcow', force=True,
        no_split=True)

    # Build the Singularity application.
    singularity.run(path=path, exec_dict=exec_dict, exec_ntasks=1)
