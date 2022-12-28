# =========================================================================

# Module: utils/schema_interface.py

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

    schema_interface.py

Description
-----------

    This module contains functions to validate calling class and/or
    function attributes.

Classes
-------

    SchemaError(msg=msg)

        This is the base-class for all exceptions; it is a sub-class
        of Error.

Functions
---------

    validate_opts(cls_schema, cls_opts)

        This function validates the calling class schema; if the
        respective schema is not validated an exception will be
        raised; otherwise this function is passive.

Requirements
------------

- schema; https://github.com/keleshev/schema

Author(s)
---------

    Henry R. Winterbottom; 27 December 2022

History
-------

    2022-12-27: Henry Winterbottom -- Initial implementation.

"""

# ----

from schema import Schema
from utils.error_interface import Error
from utils.error_interface import gen_except_handle

# ----

# Define all available functions.
__all__ = ["validate_opts"]

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class SchemaError(Error):
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

        Creates a new SchemaError object.

        """
        super().__init__(msg=msg)

# ----


@gen_except_handle(SchemaError)
def validate_opts(cls_schema: dict, cls_opts: dict) -> None:
    """
    Description
    -----------

    This function validates the calling class schema; if the
    respective schema is not validated an exception will be raised;
    otherwise this function is passive.

    Parameters
    ----------

    cls_schema: dict

        A Python dictionary containing the calling class schema.

    cls_opts: dict

        A Python dictionary containing the options (i.e., parameter
        arguments, keyword arguments, etc.,) passed to the respective
        calling class.

    """

    # Define the schema.
    schema = Schema([cls_schema])

    # Check that the class attributes are valid; proceed accordingly.
    schema.validate([cls_opts])
