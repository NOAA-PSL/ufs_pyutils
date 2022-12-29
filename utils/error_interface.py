# =========================================================================

# Module: utils/error_interface.py

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

    error_interface.py

Description
-----------

    This module loads the error package.

Classes
-------

    Error(msg)

        This is the base-class for all exceptions; it is a sub-class
        of Exceptions.

Functions
---------

    msg_except_handle(err_cls):

        This function provides a decorator to be used to raise
        specified exceptions

Author(s)
---------

    Henry R. Winterbottom; 29 November 2022

History
-------

    2022-11-29: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=raise-missing-from
# pylint: disable=unused-argument

# ----

from collections.abc import Callable

from utils.logger_interface import Logger

# ----

logger = Logger()

# ----

__all__ = ["Error",
           "msg_except_handle"]

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class Error(Exception):
    """
    Description
    -----------

    This is the base-class for all exceptions; it is a sub-class of
    Exceptions.

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

        Creates a new Error object.

        """

        # Define the base-class attributes.
        logger.error(msg=msg)
        super().__init__()


# ----


def msg_except_handle(err_cls: object) -> Callable:
    """
    Description
    -----------

    This function provides a decorator to be used to raise specified
    exceptions.

    Parameters
    ----------

    err_cls: object

        A Python object containing the Error subclass to be used for
        exception raises.

    Parameters
    ----------

    decorator: Callable

        A Python decorator.

    """

    # Define the decorator function.
    def decorator(func: Callable):

        # Execute the caller function; proceed accordingly.
        def call_function(msg: str) -> None:

            # If an exception is encountered, raise the respective
            # exception.
            raise err_cls(msg=msg)

        return call_function

    return decorator
