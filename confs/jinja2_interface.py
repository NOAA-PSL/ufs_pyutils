# =========================================================================

# Module: confs/jinja2_interface.py

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

    jinja2_interface.py

Description
-----------

    This module contains classes and functions to read and write
    Jinja2-formatted files.

Functions
---------

    write_jinja2(jinja2_file, in_dict)

        This function writes a Jinja2 formatted file using the
        specified Python dictionary.

Author(s)
---------

    Henry R. Winterbottom; 27 December 2022

History
-------

    2022-12-27: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=broad-except
# pylint: disable=consider-using-f-string
# pylint: disable=raise-missing-from
# pylint: disable=unused-argument

# ----

from utils.error_interface import msg_except_handle
from utils.exceptions_interface import Jinja2InterfaceError
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["write_jinja2"]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


def write_jinja2(jinja2_file: str, in_dict: dict) -> None:
    """
    Description
    -----------

    This function writes a Jinja2 formatted file using the specified
    Python dictionary.

    Parameters
    ----------

    jinja2_file: str

        A Python string containing the full-path to the Jinja2 file to
        be written.

    in_dict: dict

        A Python dictionary containing the attributes to be written to
        the Jinja2 file.

    Raises
    ------

    Jinja2InterfaceError:

        * raised if an exception is encountered while writing the
          Jinja2-formatted file.

    """

    # Open and write the dictionary contents to the specified
    # Jinja2-formatted file path; proceed accordingly.
    msg = f"Writing Jinja2 formatted file {jinja2_file}."
    logger.info(msg=msg)

    try:
        with open(jinja2_file, "w", encoding="utf-8") as file:
            file.write("#!Jinja2\n")
            for key in in_dict.keys():
                value = in_dict[key]

                if isinstance(value, str):
                    string = f'set {key} = "{value}"'
                else:
                    string = f"set {key} = {value}"

                file.write("{%% %s %%}\n" % string)

    except Exception as error:
        msg = f"Writing Jinja2-formatted file {jinja2_file} failed with error {error}. Aborting!!!"
        raise Jinja2InterfaceError(msg=msg)
