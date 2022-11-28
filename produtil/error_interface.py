# =========================================================================

# $$$ MODULE DOCUMENTATION BLOCK

# UFS-RNR :: ush/produtil/error_interface.py

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

    Error()

        This is the base-class for all Python Exception instances.

Author(s)
---------

    Henry R. Winterbottom; 07 January 2022

History
-------

    2022-01-07: Henry Winterbottom -- Initial implementation.

"""

# ----

from produtil.logger_interface import Logger

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

    def __init__(self, msg):
        """
        Description
        -----------

        Creates a new Error object.

        """
        logger = Logger()
        logger.error(msg=msg)
        super(Error, self).__init__()
