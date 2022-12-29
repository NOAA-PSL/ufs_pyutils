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

from utils.error_interface import msg_except_handle
from utils.exceptions_interface import SchemaInterfaceError

# ----

# Define all available attributes.
__all__ = ["validate_opts"]

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


@msg_except_handle(SchemaInterfaceError)
def __error__(msg: str = None) -> None:
    """
    Description
    -----------

    This function is the exception handler for the respective module.

    Parameters
    ----------

    msg: str

        A Python string containing a message to accompany the
        exception.

    """
    pass

# ----


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

    Raises
    ------

    SchemaInterfaceError:

        * raised if an exception is encountered while validating the
          schema.

    """

    # Define the schema.
    schema = Schema([cls_schema])

    # Check that the class attributes are valid; proceed accordingly.
    try:

        # Validate the schema.
        schema.validate([cls_opts])

    except Exception as error:

        msg = f"Schema validation failed with error {error}. Aborting!!!"
        __error__(msg=msg)
