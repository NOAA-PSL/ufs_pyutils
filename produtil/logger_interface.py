# =========================================================================

# $$$ MODULE DOCUMENTATION BLOCK

# UFS-RNR :: ush/produtil/logger_interface.py

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

import logging
import types
import sys

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"


# ----


class Logger(object):
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
        self.colors()

        # Define the logging object attributes.
        log_format = '%(asctime)s %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
        self.logger = logging
        self.logger.basicConfig(stream=sys.stdout, level=logging.INFO,
                                format=log_format, datefmt=date_format)

    def colors(self):
        """
        Description
        -----------

        This method defines the base-class object 'colors_obj' which
        contains the colors available for each type of logger event.

        """

        # Assign the terminal colors for the respective logger message
        # type.s
        self.colors_obj = types.SimpleNamespace()
        def cyan(text): return '\033[0;36m' + text + '\033[0m'
        def green(text): return '\033[0;32m' + text + '\033[0m'
        def red(text): return '\033[0;31m' + text + '\033[0m'
        colors_list = ['cyan', 'green', 'red']
        for item in colors_list:
            setattr(self.colors_obj, item, eval(item))

    def error(self, msg):
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

        # Print the ERROR level message to the user terminal.
        self.logger.error(self.colors_obj.red('ERROR: {0}'.format(msg)))

    def info(self, msg):
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

        # Print the INFO level message to the user terminal.
        self.logger.info(self.colors_obj.cyan('INFO: {0}'.format(msg)))

    def warn(self, msg):
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

        # Print the WARN level message to the user terminal.
        self.logger.warn(self.colors_obj.green('WARNING: {0}'.format(msg)))
