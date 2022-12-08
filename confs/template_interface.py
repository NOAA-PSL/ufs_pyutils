# =========================================================================

# Module confs/template_interface.py

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

    template_interface.py

Description
-----------

    This module contains classes and methods for template file string
    parsing.

Classes
-------

    Template()

        This is the base-class object for all template string parsing.

    TemplateError(msg)

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


class Template():
    """
    Description
    -----------

    This is the base-class object for all template string parsing.

    """

    def __init__(self):
        """
        Description
        -----------

        Creates a new Template object.

        """

    def write(self, str_dict: dict, str_template: str) -> str:
        """
        Description
        -----------

        This method parses a Python dictionary and replaces all
        variables within a user specified template string.

        Parameters
        ----------

        str_dict: dict

            A Python dictionary containing key and values pairs
            corresponding to the available variables within the
            user-specified template string.

        str_template: str

            A Python string specifying the template string to be
            parsed.

        Returns
        -------

        str_update: str

            A Python string containing the updated string in
            accordance with the template attribute.

        """

        # Define the updated string relative to the template
        # attribute.
        str_update = str_template

        for key in str_dict.keys():
            check_key = f'<{key}>'

            if check_key in str_template:
                value = parser_interface.dict_key_value(
                    dict_in=str_dict, key=key, no_split=True)
                str_update = str_update.replace(
                    f'{check_key}', f'{value}')

        return str_update

    def run(self, str_dict: dict, str_template: str) -> str:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Parses a Python dictionary and replaces all variables
            within a user-specified template string.

        Parameters
        ----------

        str_dict: dict

            A Python dictionary containing key and values pairs
            corresponding to the available variables within the
            user-specified template string.

        str_template: str

            A Python string specifying the template string to be
            parsed.

        Returns
        -------

        str_update: str

            A Python string containing the updated string in
            accordance with the template attribute.

        Raises
        ------

        TemplateError:

            * raised if an exception is encountered while parsing the
              template string.

        """

        # Update all template strings accordingly.
        try:
            str_update = self.write(str_template=str_template,
                                    str_dict=str_dict)

        except Exception as error:

            msg = (f'Template string {str_template} parsing failed with error '
                   '{error}. Aborting!!!')
            raise TemplateError(msg=msg) from error

        return str_update

# ----


class TemplateError(Error):
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

        Creates a new TemplateError object.

        """
        super().__init__(msg=msg)
