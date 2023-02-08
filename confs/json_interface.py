# =========================================================================

# Module: confs/json_interface.py

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

    json_interface.py

Description
-----------

    This module contains classes and functions to read and write
    JSON-formatted files.

Functions
---------

    read_json(json_file)

        This function ingests a JavaScript Object Notation (e.g.,
        JSON) formatted file and returns a Python dictionary
        containing all attributes of the file.

    write_json(json_file, in_dict, indent=4)

        This function writes a JavaScript Object Notation (e.g., JSON)
        formatted file using the specified Python dictionary.

Author(s)
---------

    Henry R. Winterbottom; 27 December 2022

History
-------

    2022-12-27: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=broad-except
# pylint: disable=raise-missing-from

# ----

import json
from typing import Dict

from utils.exceptions_interface import JSONInterfaceError
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["read_json", "write_json"]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


def read_json(json_file: str) -> Dict:
    """
    Description
    -----------

    This function ingests a JavaScript Object Notation (e.g., JSON)
    formatted file and returns a Python dictionary containing all
    attributes of the file.

    Parameters
    ----------

    json_file: str

        A Python string containing the full-path to the JSON file to
        be parsed.

    Returns
    -------

    json_dict: dict

        A Python dictionary containing all attributes contained within
        the ingested JSON file.

    Raises
    ------

    JSONInterfaceError:

        * raised is an exception is encountered while reading from the
          JSON-formatted file specified upon entry.

    """

    # Open and read the contents of the specified JSON-formatted file
    # path; proceed accordingly.
    msg = f"Reading from JSON-formatted file {json_file}."
    logger.info(msg=msg)

    try:
        with open(json_file, "r", encoding="utf-8") as stream:
            json_dict = json.load(stream)

    except Exception as errmsg:
        msg = f"Reading JSON-formatted file {json_file} failed with error {errmsg}. Aborting!!!"
        raise JSONInterfaceError(msg=msg)

    return json_dict


# ----


def write_json(json_file: str, in_dict: Dict, indent: int = 4) -> None:
    """
    Description
    -----------

    This function writes a JavaScript Object Notation (e.g., JSON)
    formatted file using the specified Python dictionary.

    Parameters
    ----------

    json_file: str

        A Python string containing the full-path to the JSON file to
        be written.

    in_dict: dict

        A Python dictionary containing the attributes to be written to
        the JSON file.

    Keywords
    --------

    indent: int, optional

        A Python integer defining the indentation level for the
        attributes within the JSON-formatted file.

    Raises
    ------

    JSONInterfaceError:

        * raised is an exception is encountered while writing to the
          JSON-formatted file specified upon entry.

    """

    # Open and write the Python dictionary contents to the specified
    # JSON-formatted file path; proceed accordingly.
    msg = f"Writing to JSON-formatted file {json_file}."
    logger.info(msg=msg)

    try:
        with open(json_file, "w", encoding="utf-8") as file:
            json.dump(in_dict, file, indent=indent)

    except Exception as errmsg:
        msg = f"Writing JSON-formatted file {json_file} failed with error {errmsg}. Aborting!!!"
        raise JSONInterfaceError(msg=msg)
