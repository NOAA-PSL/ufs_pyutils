# =========================================================================

# Module: utils/arguments_interface.py

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

    arguments_interface.py

Description
-----------

    This is the base-class object for all command line argument(s)
    parsing.

Classes
-------

    Arguments()

        This is the base-class object for all command line argument(s)
        parsing.

    ArgumentsError(msg)

        This is the base-class for all exceptions; it is a sub-class
        of Error.

Author(s)
---------

    Henry R. Winterbottom; 12 December 2022

History
-------

    2022-12-12: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=too-few-public-methods

# ----

from argparse import ArgumentParser
from tools import parser_interface
from utils.error_interface import Error

# ----


class Arguments:
    """
    Description
    -----------

    This is the base-class object for all command line argument(s)
    parsing.

    """

    def run(self) -> object:
        """
        Description
        -----------

        This method collects the arguments passed for the command line
        to the respective caller script and builds a Python object
        containing the respective arguments.

        The command line arguments may be specified as follows.

        user@host:$ python <caller_script>.py --key=value

        user@host:$ python <caller_script>.py -key=value

        Here 'key' is the argument name and 'value' is the value
        attributed to the respective argument.

        Returns
        --------

        options_obj: object

            A Python object containing the command line argument key
            and value pairs.

        Raises
        ------

        ArgumentsError:

            * raised if an exception is encountered while parsing the
              command line arguments.

        """

        # Define the base-class attributes.
        parser = ArgumentParser()
        arg_key_strip = ["-", "--"]

        # Collect the command line arguments.
        (_, args) = parser.parse_known_args()

        # Build the Python object containing the command line
        # arguments.
        options_obj = parser_interface.object_define()

        for arg in args:

            # Define the argument and the respective value; proceed
            # accordingly.
            (key, value) = arg.split("=")

            for arg_key in arg_key_strip:
                key = key.strip(arg_key)

            # Define the Python object attributes.
            options_obj = parser_interface.object_setattr(
                object_in=options_obj, key=key, value=value
            )

        return options_obj


# ----


class ArgumentsError(Error):
    """
    Description
    -----------

    This is the base-class for all exceptions; it is a sub-class of
    Error.

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

        Creates a new ArgumentsError object.

        """
        super().__init__(msg=msg)
