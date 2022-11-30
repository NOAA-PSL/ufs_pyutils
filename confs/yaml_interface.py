#!/usr/bin/env python3

# =========================================================================

# Module: app_confs/yaml_interface.py

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

    yaml_interface.py

Description
-----------

    This module contains classes and methods to parse YAML-formatted
    template files and create an external file containing the user
    specified values.

Classes
-------

    YAML()

        This is the base-class object for YAML-formatted template file
        updates and the creation of a YAML-formatted file based on the
        template and the user-specified template variable key and
        value pairs.

    YAMLError(msg)

        This is the base-class for all exceptions; it is a sub-class
        of Error.

Author(s)
--------- 

    Henry R. Winterbottom; 29 November 2022

History
-------

    2022-11-29: Henry Winterbottom -- Initial implementation.

"""

# ----

from tools import parser_interface
from utils.error_interface import Error

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class YAML(object):
    """
    Description
    -----------

    This is the base-class object for YAML-formatted template file
    updates and the creation of a YAML-formatted file based on the
    template and the user-specified template variable key and value
    pairs.

    """

    def __init__(self):
        """ 
        Description
        -----------

        Creates a new YAMLTemplate object.

        """

    def write(self, yaml_dict: dict, yaml_path: str, yaml_template: str):
        """
        Description
        -----------

        This method ingests a YAML template file and parses a Python
        dictionary containing key and value pairs for template
        variables to be replaced; the updated template to then written
        to the user-specified path.

        Parameters
        ----------

        yaml_dict: dict

            A Python dictionary containing key and values pairs
            corresponding to the template variables within the
            user-specified YAML-formatted template file.

        yaml_template: str

            A Python string specifying the template variables to be
            sought and updated.

        yaml_path: str

            A Python string specifying the path to the YAML-formatted
            output file derived from the template.

        """

        # Read the template file.
        template_matches = ['<', '>']
        with open(yaml_template, 'r') as f:
            template = f.read().split('\n')

        # Open and write the namelist file while formatting the
        # template values specified upon entry accordingly.
        with open(yaml_path, 'w') as f:
            for item in template:
                for key in yaml_dict.keys():
                    if key in item:
                        value = parser_interface.dict_key_value(
                            dict_in=yaml_dict, key=key, no_split=True)
                        item = item.replace(
                            '<{0}>'.format(key), str(value))

                if not any(x in item for x in template_matches):
                    f.write('{0}\n'.format(item))

    def run(self, yaml_dict: dict, yaml_path: str, yaml_template: str):
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Parse a YAML-formatted template file and replaces the
            templated variables (defined by < template variable >)
            using the key and value pairs within the user-specified
            Python dictionary.

        (2) Writes the updated template to the user-specified path.

        """

        # Parse the YAML-formatted template file and proceed
        # accordingly.
        try:
            self.write(yaml_path=yaml_path, yaml_template=yaml_template,
                       yaml_dict=yaml_dict)

        except Exception as error:

            msg = ('Creation of YAML-formatted file {0} failed with '
                   'error {1}. Aborting!!!'.format(yaml_path, error))
            raise YAMLError(msg=msg)

# ----


class YAMLError(Error):
    """
    Description
    -----------

    This is the base-class for all exceptions; it is a sub-class of
    Error.

    Parameters
    ----------

    msg: str

        A Python string containing a message to accompany the
        exception.

    """

    def __init__(self, msg: str):
        """
        Description
        -----------

        Creates a new YAMLError object.

        """
        super(YAMLError, self).__init__(msg=msg)
