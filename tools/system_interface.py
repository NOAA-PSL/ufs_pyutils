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

        This method defines the calling application stack frame.

    app_path(app)

        This function invokes the POSIX UNIX command function to retrieve
        the path to the application specified upon entry.

    chown(path, user, group=None)

        This function changes the ownership credentials for the
        specified file path.

    task_exit()

        This method (gracefully) exits the respective application and
        returns a status code of 0 (i.e., success).

    user()

        This method invokes the POSIX UNIX command whoami to determine
        the respective user calling this function.

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
import subprocess
import sys

from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["app_path", "chown", "task_exit", "user"]

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

    This method defines the calling application stack frame.

    Returns
    -------

    stack: list

        A Python list containing the calling application stack frame.

    """

    # Collect the calling application stack frame.
    stack = inspect.stack()

    return stack

# ----


def app_path(app: str) -> str:
    """
    Description
    -----------

    This function invokes the POSIX UNIX command function to retrieve
    the path to the application specified upon entry.

    Parameters
    ----------

    app: str

        A Python string specifying the name of the application for
        which the path is to be determined.

    Returns
    -------

    path: str

        A Python string specifying the path determined for the
        application name specified upon entry; if no path for the
        respective application name can be determined NoneType is
        returned.

    """

    # Query the run-time environment in order to collect the path for
    # the application name specified upon entry.
    cmd = ['command',
           '-V',
           app
           ]

    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    (out, err) = proc.communicate()

    # Collect the run-time environment path from the query for the
    # application name specified upon entry.
    if len(out) > 0:
        path = out.rstrip().decode("utf-8").split()[2]
    else:
        path = None

    return path

# ----


def chown(path: str, user: str, group: str = None) -> None:
    """
    Description
    -----------

    This function changes the ownership credentials for the specified
    file path.

    Parameters
    ----------

    path: str

        A Python string specifying the file path for which to change
        the ownership credentials.

    user: str

        A Python string specifying the host name for the user to be
        used for the file path ownership credentials.

    Keywords
    --------

    group: str

        A Python string specifying the host group name to be user for
        the path owner credentials.

    """

    # Change the ownership credentials for the specified file path in
    # accordance with the parameter values provided upon entry.
    shutil.chown(path=path, user=user, group=group)


# ----


def task_exit() -> None:
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
    msg = f"Task exit called from file {module} line number " "{lineno}."
    logger.warn(msg=msg)

    sys.exit(0)

# ----


def user() -> str:
    """
    Description
    -----------

    This method invokes the POSIX UNIX command whoami to determine the
    respective user calling this function.

    Returns
    -------

    username: str

        A Python string specifying the POSIX UNIX whoami command
        result; if the whoami command returns an empty string, the
        return is NoneType.

    """

    # Query the POSIX UNIX environment to determine the user invoking
    # this function.
    cmd = ["whoami"]

    proc = subprocess.Popen(cmd, stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    (out, err) = proc.communicate()

    # Collect the POSIX UNIX environment user name from the query.
    if len(out) > 0:
        username = out.rstrip().decode("utf-8")
    else:
        username = None

    return username
