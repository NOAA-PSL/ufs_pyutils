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

Author(s)
---------

    Henry R. Winterbottom; 29 November 2022

History
-------

    2022-11-29: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: raise-missing-from

# ----

from collections.abc import Callable
from typing import TypeVar

from typing_extensions import ParamSpec

from utils.logger_interface import Logger

# ----

__all__ = ["gen_except_handle"]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

# Define the type hint attributes.
Params = ParamSpec("Params")
Returns = TypeVar("Returns")

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


def gen_except_handle(err_cls: object):
    """
    Description
    -----------

    This function provides a decorator for general exceptions.

    Parameters
    ----------

    err_cls: object

        A Python object specifying the error class to be raised when
        an exception is encountered.

    Returns
    -------

    decorate: object

        A Python object containing the respetive general exception
        handler decorator.

    """

    # Define the decorator function.
    def decorator(func: Callable):

        # Execute the caller function; proceed accordingly.
        def call_function(*args: Params.args, **kwargs: Params.kwargs) -> Returns:
            try:

                # Execute the callable function/method.
                func(*args, **kwargs)

            except Exception as error:

                # Raise the specified Error class.
                raise err_cls(msg=error)

        return call_function

    return decorator
