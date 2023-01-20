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

Author(s)
---------

    Henry R. Winterbottom; 12 December 2022

History
-------

    2022-12-12: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=broad-except
# pylint: disable=unnecessary-list-index-lookup

# ----

from argparse import ArgumentParser
from dataclasses import dataclass

from tools import parser_interface

from utils import schema_interface
from utils.error_interface import msg_except_handle
from utils.exceptions_interface import ArgumentsInterfaceError

# ----


@dataclass
class Arguments:
    """
    Description
    -----------

    This is the base-class object for all command line argument(s)
    parsing.

    """

    @msg_except_handle(ArgumentsInterfaceError)
    def __error__(self, msg: str = None) -> None:
        """
        Description
        -----------

        This function is the exception handler for the respective
        module.

        Keywords
        --------

        msg: str

            A Python string containing a message to accompany the
            exception.

        """

    def run(self, eval_schema=False, cls_schema=None) -> object:
        """
        Description
        -----------

        This method collects the arguments passed for the command line
        to the respective caller script and builds a Python object
        containing the respective arguments.

        The command line arguments may be specified as follows.

        user@host:$ python <caller_script>.py --key value

        user@host:$ python <caller_script>.py -key value

        Here 'key' is the argument name and 'value' is the value
        attributed to the respective argument/key.

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

        # Collect the command-line argument key and value pairs.
        (_, args) = ArgumentParser().parse_known_args()
        (arg_keys, arg_values) = ([item.strip("-")
                                   for item in args[::2]], args[1::2])

        # Build the Python object containing the command line
        # arguments.
        options_obj = parser_interface.object_define()

        for (idx, _) in enumerate(arg_keys):

            # Define the Python object attributes.
            options_obj = parser_interface.object_setattr(
                object_in=options_obj, key=arg_keys[idx], value=arg_values[idx]
            )

        # Check whether to evaluate the argument schema; proceed
        # accordingly.
        if eval_schema:

            try:

                # Build the Python dictionary containing the command
                # line arguments.
                cls_opts = {}
                for option in vars(options_obj):
                    cls_opts[option] = parser_interface.object_getattr(
                        object_in=options_obj, key=option, force=True
                    )
                cls_opts = parser_interface.dict_formatter(in_dict=cls_opts)

                # Evalute the schema; proceed accordingly.
                schema_interface.validate_opts(
                    cls_schema=cls_schema, cls_opts=cls_opts)

            except Exception as error:

                msg = f"Arguments validation failed with error {error}. Aborting!!!"
                self.__error__(msg=msg)

        return options_obj
