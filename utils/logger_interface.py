# =========================================================================

# Module: utils/logger_interface.py

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

    logger_interface.py

Description
-----------

    This module contains wrapper methods for the Python logging
    package.

Classes
-------

    Logger()

        This is the base-class for all Python logging instances.

Author(s)
---------

    Henry R. Winterbottom; 02 November 2022

History
-------

    2022-11-02: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=eval-used
# pylint: disable=unused-variable

# ----

from importlib import reload
import logging
import sys

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class Logger:
    """
    Description
    -----------

    This is the base-class object for all logger-type messages.

    """

    def __init__(self):
        """
        Description
        -----------

        Creates a new Logger object.

        """

        # Define the base-class attributes.
        self.log_format = "%(asctime)s :: %(levelname)s :: %(message)s"
        self.date_format = "%Y-%m-%d %H:%M:%S"
        self.stream = sys.stdout

    def __get_logfrmt__(self, level: str) -> str:
        """
        Description
        -----------

        This module defines the format for the logger object string;
        the designated color formats may be found at
        https://tinyurl.com/python-logger-string-colors.

        Parameters
        ----------

        level: str

            A Python string specifying the logger type;
            case-insensitive.

        Returns
        -------

        logfrmt: str

            A Python string containing the logger object format
            string.

        """

        # Define the color attributes for the respective logger
        # levels.
        reset = "\x1b[0m"
        colors_dict = {"CRITICAL": "\x1b[1;42m",
                       "DEBUG": "\x1b[38;5;39m",
                       "INFO": "\x1b[37;21m",
                       "ERROR": "\x1b[1;41m",
                       "WARNING": "\x1b[38;5;226m"
                       }

        # Define the logger object format string in accordance with
        # the logger level specified upon entry.
        logfrmt = colors_dict[level.upper()] + self.log_format + reset

        return logfrmt

    def __get_logger__(self, level: object, log_format: str) -> object:
        """
        Description
        -----------

        This method defines the logger object; the object is
        constructed based on the logging level and the format of the
        logger string, both specified upon entry.

        Parameters
        ----------

        level: object

            A Python logging level object; available levels may be
            found at https://tinyurl.com/python-logging-levels.

        log_format: str

            A Python string specifying the logger string format.

        Returns
        -------

        logger: object

            A Python logger object for the respective logger level and
            format string provided upon entry.

        """

        # Define the logging object accordingly.
        self.__reset__()
        logger = logging
        logger.basicConfig(
            stream=sys.stdout, level=level, format=log_format,
            datefmt=self.date_format)

        return logger

    def __reset__(self) -> None:
        """
        Description
        -----------

        This method shutsdown and subsequently reloads the logging
        module; this is step is necessary in order to reset the
        attributes of the logger handlers and allow for different
        logger levels to be instantiated from the same calling
        class/module.

        """

        # Shutdown and reload the Python logging library.
        logging.shutdown()
        reload(logging)

    def critical(self, msg: str):
        """
        Description
        -----------

        This method writes a message to the base-class Python logger
        via the CRITICAL level.

        Parameters
        ----------

        msg: str

            A Python string containing the Python logger level
            message.

        """

        # Define the logger object.
        log_format = self.__get_logfrmt__(level="critical")
        logger = self.__get_logger__(
            level=logging.CRITICAL, log_format=f"{log_format}")

        # Write the logger message.
        logger.critical(msg)

    def debug(self, msg: str):
        """
        Description
        -----------

        This method writes a message to the base-class Python logger
        via the DEBUG level.

        Parameters
        ----------

        msg: str

            A Python string containing the Python logger level
            message.

        """

        # Define the logger object.
        log_format = self.__get_logfrmt__(level="debug")
        logger = self.__get_logger__(
            level=logging.DEBUG, log_format=f"{log_format}")

        # Write the logger message.
        logger.debug(msg)

    def error(self, msg: str):
        """
        Description
        -----------

        This method writes a message to the base-class Python logger
        via the ERROR level.

        Parameters
        ----------

        msg: str

            A Python string containing the Python logger level
            message.

        """

        # Define the logger object.
        log_format = self.__get_logfrmt__(level="error")
        logger = self.__get_logger__(
            level=logging.ERROR, log_format=f"{log_format}")

        # Write the logger message.
        logger.error(msg)

    def info(self, msg: str):
        """
        Description
        -----------

        This method writes a message to the base-class Python logger
        via the INFO level.

        Parameters
        ----------

        msg: str

            A Python string containing the Python logger level
            message.

        """

        # Define the logger object.
        log_format = self.__get_logfrmt__(level="info")
        logger = self.__get_logger__(
            level=logging.INFO, log_format=f"{log_format}")

        # Write the logger message.
        logger.info(msg)

    def warn(self, msg: str):
        """
        Description
        -----------

        This method writes a message to the base-class Python logger
        via the WARN level.

        Parameters
        ----------

        msg: str

            A Python string containing the Python logger level
            message.

        """

        # Define the logger object.
        log_format = self.__get_logfrmt__(level="warning")
        logger = self.__get_logger__(
            level=logging.WARNING, log_format=f"{log_format}")

        # Write the logger message.
        logger.warning(msg)
