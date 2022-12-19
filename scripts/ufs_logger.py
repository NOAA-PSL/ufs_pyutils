# =========================================================================

# Script: scripts/ufs_logger.py

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
Script
------

    ufs_logger.py

Description
-----------

    This script contains a functional interface to the
    ufs_pyutils/utils/logger_interface.py module.

Classes
-------

    UFSLogger(option_opts)

        This is the base-class object for all supported logging levels
        of the ufs_pyutils logger_interface module.

    UFSLoggerError(msg)

        This is the base-class for all exceptions; it is a sub-class
        of Error.

Functions
---------

    main()

        This is the driver-level method to invoke the tasks within
        this script.

Requirements
------------

- ufs_pytils; https://github.com/HenryWinterbottom-NOAA/ufs_pyutils

Author(s)
---------

    Henry R. Winterbottom; 19 December 2022

History
-------

    2022-12-19: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=too-few-public-methods

# ----

import os
import time

from tools import parser_interface
from utils.arguments_interface import Arguments
from utils.error_interface import Error
from utils.logger_interface import Logger

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

logger = Logger()

# ----


class UFSLogger:
    """
    Description
    -----------

    This is the base-class object for all supported logging levels of
    the ufs_pyutils logger_interface module.

    Parameters
    ----------

    options_obj: object

        A Python object containing the command line argument
        attributes.

    """

    def __init__(self, options_obj: object):
        """
        Description
        -----------

        Creates a new UFSLogger object.

        """

        # Define the base-class attributes.
        self.options_obj = options_obj

        self.logger_opts = {"msg": options_obj.msg, "msgtype": options_obj.msgtype}

        self.msgtype_opts = {
            "info": logger.info,
            "error": logger.error,
            "warn": logger.warn,
        }

    def run(self) -> None:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Collects the command line arguments and determines whether
        they are valid.

        (2) Creates a Python logging message using the respective
        (i.e., specified) logger level.

        Raises
        ------

        UFSLoggerError:

            * raised if the logger message cannot be determined from
              the command line arguments.

            * raised if the logging level cannot be determined from
              the command line attributes.

            * raised if the logging level is not supported.

        """

        # Define the logger message from the command line attributes.
        logger_msg = parser_interface.object_getattr(
            object_in=self.options_obj, key="msg", force=True
        )
        if logger_msg is None:
            msg = "The logger message cannot be NoneType. " "Aborting!!!"
            raise UFSLoggerError(msg=msg)

        # Determine the logging level from the command line
        # attributes.
        logger_level = parser_interface.object_getattr(
            object_in=self.options_obj, key="msgtype", force=True
        )
        if logger_level is None:
            msg = "The logger level type cannot be NoneType. " "Aborting!!!"
            raise UFSLoggerError(msg=msg)

        if logger_level.lower() not in self.msgtype_opts:
            msg = (
                f"The logger level type {logger_level} is not supported. " "Aborting!!!"
            )
            raise UFSLoggerError(msg=msg)

        # Create the logger message using the respective logging
        # level.
        method = parser_interface.dict_key_value(
            dict_in=self.msgtype_opts, key=logger_level.lower(), no_split=True
        )
        method(msg=logger_msg)


# ----


class UFSLoggerError(Error):
    """
    Description
    -----------

    This is the base-class for all exceptions; it is a sub-class of
    Error.

    Parameters
    ----------

    msg: str

        A Python string to accompany the raised exception.

    """

    def __init__(self, msg: str):
        """
        Description
        -----------

        Creates a new UFSLoggerError object.

        """
        super().__init__(msg=msg)


# ----


def main():
    """
    Description
    -----------

    This is the driver-level function to invoke the tasks within this
    script.

    """

    # Collect the command line arguments.
    script_name = os.path.basename(__file__)
    start_time = time.time()
    msg = f"Beginning application {script_name}."
    logger.info(msg=msg)
    options_obj = Arguments().run()

    # Launch the task.
    task = UFSLogger(options_obj=options_obj)
    task.run()
    stop_time = time.time()
    msg = f"Completed application {script_name}."
    logger.info(msg=msg)
    total_time = stop_time - start_time
    msg = f"Total Elapsed Time: {total_time} seconds."
    logger.info(msg=msg)


# ----


if __name__ == "__main__":
    main()
