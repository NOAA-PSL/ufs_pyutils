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

from utils.logger_interface import Logger

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
        logger = Logger()
        logger.error(msg=msg)
        super().__init__()
