# =========================================================================

# $$$ MODULE DOCUMENTATION BLOCK

# UFS-RNR :: ush/tools/system_interface.py

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

    system_interface.py

Description
-----------

    This module contains functions to perform various system-level
    tasks.

Functions
---------

    _get_stack()

        This method defines the calling application stack frame.

    task_exit()

        This method (gracefully) exits the respective application and
        returns a status code of 0 (i.e., success).

Author(s)
---------

    Henry R. Winterbottom; 13 October 2022

History
-------

    2022-10-13: Henry Winterbottom -- Initial implementation.

"""

# ----

import inspect
import sys

from produtil.error_interface import Error
from produtil.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ['task_exit'
           ]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


def _get_stack():
    """
    Description
    -----------

    This method defines the calling application stack frame.

    Returns
    -------

    stack: obj

        A Python object containing the calling application stack
        frame.

    """

    # Collect the calling application stack frame.
    stack = inspect.stack()

    return stack

# ----


def task_exit():
    """
    Description
    -----------

    This method (gracefully) exits the respective application and
    returns a status code of 0 (i.e., success).

    """

    # Define the calling application stack frame.
    stack = _get_stack()

    # Define calling application attributes.
    [module, lineno] = (stack[2][1], stack[2][2])

    # Gracefully exit task.
    msg = ('Task exit called from file {0} line number {1}.'
           .format(module, lineno))
    logger.warn(msg=msg)
    sys.exit(0)
