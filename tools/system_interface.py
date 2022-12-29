# =========================================================================

# Module: tools/system_interface.py

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

        This function defines the calling application stack frame.

    get_app_path(app)

        This function collects the path for the specified application;
        if the path cannot be determined, NoneType is returned.

    sleep(seconds=0)

        This function allows specific calling applications to suspend
        execution for a specified number of seconds.

    task_exit()

        This function (gracefully) exits the respective application
        and returns a status code of 0 (i.e., success).

Author(s)
---------

    Henry R. Winterbottom; 03 December 2022

History
-------

    2022-12-03: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=unused-variable

# ----

import inspect
import shutil
import sys
import time

from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["get_app_path", "sleep", "task_exit"]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


def _get_stack() -> list:
    """
    Description
    -----------

    This function defines the calling application stack frame.

    Returns
    -------

    stack: list

        A Python list containing the calling application stack frame.

    """

    # Collect the calling application stack frame.
    stack = inspect.stack()

    return stack

# ----


def get_app_path(app: str) -> str:
    """
    Description
    -----------

    This function collects the path for the specified application; if
    the path cannot be determined, NoneType is returned.

    Parameters
    ----------

    app: str

        A Python string specifying the name of the application for
        which to return the respective path.

    Returns
    -------

    app_path: str

        A Python string specifying the path to the application name
        provided upon entry; if the application path cannot be
        determined, this value is NoneType.

    """

    # Collect the application path.
    app_path = shutil.which(app)

    return app_path

# ----


def sleep(seconds: int = 0) -> None:
    """
    Description
    -----------

    This function allows specific calling applications to suspend
    execution for a specified number of seconds.

    Keywords
    --------

    seconds: int, optional

        A Python integer specifying the number of seconds for which to
        suspend execution.

    """

    # Suspend execution for the specified number of seconds.
    time.sleep(seconds)


# ----


def task_exit() -> None:
    """
    Description
    -----------

    This function (gracefully) exits the respective application and
    returns a status code of 0 (i.e., success).

    """

    # Define the calling application stack frame.
    stack = _get_stack()

    # Define calling application attributes.
    [module, lineno] = (stack[2][1], stack[2][2])

    # Gracefully exit task.
    msg = f"Task exit called from file {module} line number {lineno}."
    logger.warn(msg=msg)

    sys.exit(0)
