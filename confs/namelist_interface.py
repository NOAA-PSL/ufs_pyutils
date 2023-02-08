# =========================================================================

# Module: confs/namelist_interface.py

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

    namelist_interface.py

Description
-----------

    This module contains methods to parse FORTRAN 90 namelist-type
    template files and create an external file containing the user
    specified values.

Classes
-------

    Namelist(log_messages=False, no_string_quotes=False,
             remove_comments=False, strip_dblequotes=False)

        This is the base-class object for all FORTRAN 90 namelist-type
        template file parsing and external FORTRAN 90 namelist-type
        file creation.

Author(s)
---------

    Henry R. Winterbottom; 08 December 2022

History
-------

    2022-12-08: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=broad-except
# pylint: disable=consider-using-f-string
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-nested-blocks
# pylint: disable=too-many-statements

# ----

import re

from tools import datetime_interface, fileio_interface
from utils.exceptions_interface import NamelistInterfaceError

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class Namelist:
    """
    Description
    -----------

    This is the base-class object for all FORTRAN 90 namelist-type
    template file parsing and external FORTRAN 90 namelist-type file
    creation.

    Keywords
    --------

    log_messages: bool, optional

        A Python boolean variable specifying whether to include
        template file path and file creation time in formatted output
        file.

    no_string_quotes: bool, optional

        A Python boolean variable indicating whether to include quotes
        around strings in the namelist-type formatted file created
        from the template.

    remove_comments: bool, optional

        A Python boolean variable specifying whether to remove
        comments within the template file from the output
        namelist-type file.

    strip_dblquotes: bool, optional

        A Python boolean variable specifying whether to remove (strip)
        any double quotes (i.e., " ") from strings write to the output
        namelist-type file.

    """

    def __init__(
        self,
        log_messages: bool = False,
        no_string_quotes: bool = False,
        remove_comments: bool = False,
        strip_dblequotes: bool = False,
    ):
        """
        Description
        -----------

        Creates a new Namelist object.

        """

        # Define the base-class attributes.
        self.log_messages = log_messages
        self.no_string_quotes = no_string_quotes
        self.remove_comments = remove_comments
        self.strip_dblequotes = strip_dblequotes

    def check_float(self, string: str) -> bool:
        """
        Description
        ----------

        This method attempts to convert a string to a float value; if
        successful, the return value (float_valid) is True; if
        unsuccessful (e.g., a ValueError exception is encountered),
        the return value (float_valid) is False.

        Parameters
        ----------

        string: str

            A Python string to be tested for a float conversion.

        Returns
        -------

        float_valid: bool

            A Python boolean value specifying the success of the
            string to float conversion.

        """

        # Check the input string upon entry and proceed accordingly.
        char_chks = ["e"]

        if any(item in string for item in char_chks):
            try:
                float(string)
                float_valid = True

            except ValueError:
                float_valid = False

        else:
            float_valid = None

        return float_valid

    def dblequotes_strip(self, nml_path: str) -> None:
        """
        Description
        -----------

        This method will strip string embedded between double quotes
        (i.e., " ") and update the respective lines/strings within the
        FORTRAN 90 namelist-type output file path.

        Parameters
        ----------

        nml_path: str

            A Python string specifying the path to the formatted
            FORTRAN 90 namelist-type output file.

        """

        # Remove any occurances of double quotation marks.
        with open(nml_path, "r", encoding="utf-8") as file:
            data = file.read()

        filelist = []
        filelist.append(nml_path)
        fileio_interface.removefiles(filelist=filelist)

        with open(nml_path, "w", encoding="utf-8") as file:
            for line in data.split("\n"):
                line = re.sub('["]', "", line)
                file.write(f"{line}\n")

    def write(self, nml_dict: dict, nml_template: str, nml_path: str) -> None:
        """
        Description
        -----------

        This method parses a Python dictionary and replaces all
        variables within a user specified FORTRAN 90 namelist-type
        template file.

        Parameters
        ----------

        nml_dict: dict

            A Python dictionary containing key and values pairs
            corresponding to the available variables within the
            user-specified namelist-type template file.

        nml_template: str

            A Python string specifying the FORTRAN 90 namelist-type
            template file to be parsed.

        nml_path: str

            A Python string specifying the path to the formatted
            FORTRAN 90 namelist-type output file.

        Notes
        -----

        This method will be updated in the future to reduce Pylint
        'too-many-branches' and 'too-many-statements' detections;
        these errors are disabled for now.

        """

        # Read the namelist template file provided upon entry.
        with open(nml_template, "rt", encoding="utf-8") as file:
            data = file.read().split("\n")
        idchars = set("<>")

        # Open the namelist output file and proceed accordingly.
        with open(nml_path, "wt", encoding="utf-8") as file:
            if self.log_messages:
                file.write(f"! File created from {nml_template}.\n")

            # Build the namelist in accordance with the namelist
            # template attributes.
            for nml_line in data:
                for key in nml_dict.keys():
                    check_key = f"<{key}>"
                    if check_key in nml_line:
                        value = nml_dict[key]
                        test_value = value
                        if isinstance(test_value, str):

                            # Handle float values accordingly.
                            float_valid = self.check_float(string=test_value)
                            if float_valid is not None:
                                if float_valid:
                                    try:
                                        nml_line = nml_line.replace(
                                            f"{check_key}",
                                            "{0}".format(float(value)),
                                        )

                                    except ValueError:
                                        nml_line = nml_line.replace(
                                            f"{check_key}",
                                            f'"{value}"',
                                        )

                            # Handle boolean type values accordingly.
                            if (value.lower() == "t") or (value.lower() == "f"):
                                nml_line = nml_line.replace(f"{check_key}", f"{value}")
                                break

                            # Handle string type values accordingly.
                            if "," in test_value:
                                value = str()
                                for item in test_value.split(","):
                                    float_valid = self.check_float(string=item)
                                    if float_valid:
                                        try:
                                            value = value + "{0},".format(float(item))

                                        except ValueError:
                                            value = value + f'"{item}",'
                                    else:
                                        try:
                                            int(item)
                                            value = value + f"{item},"

                                        except ValueError:
                                            value = value + f'"{item}",'

                                nml_line = nml_line.replace(f"{check_key}", f"{value}")

                            else:

                                # Handle strings containing quotations accordingly.
                                if self.no_string_quotes:
                                    nml_line = nml_line.replace(
                                        f"{check_key}", f"{value}"
                                    )
                                else:
                                    nml_line = nml_line.replace(
                                        f"{check_key}", f'"{value}"'
                                    )

                        # Handle boolean type values accordingly.
                        elif isinstance(test_value, bool):
                            if value:
                                nml_line = nml_line.replace(f"{check_key}", "T")
                            else:
                                nml_line = nml_line.replace(f"{check_key}", "F")
                        else:
                            nml_line = nml_line.replace(f"{check_key}", f"{value}")

                # Write to the output namelist file accordingly.
                if all(idc in nml_line for idc in idchars):
                    nml_line = None
                if nml_line is not None:

                    # Handle comment strings accordingly.
                    if self.remove_comments:
                        if ("!" not in nml_line) and (nml_line is not str()):
                            file.write(f"{nml_line}\n")

                    else:
                        file.write("{0}\n".format(nml_line))

            # Add logging message to the end of the file.
            if self.log_messages:
                timestamp = datetime_interface.current_date(frmttyp="%Y-%m-%d %H:%M:%S")
                file.write(f"! Updated: {timestamp}.\n")

    def run(self, nml_dict: dict, nml_template: str, nml_path: str) -> None:
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Parses a Python dictionary and replaces all variables
            within a user specified namelist-type template file.

        Parameters
        ----------

        nml_dict: dict

            A Python dictionary containing key and values pairs
            corresponding to the available variables within the
            user-specified namelist-type template file.

        nml_template: str

            A Python string specifying the namelist-type template file
            to be parsed.

        nml_path: str

            A Python string specifying the path to the formatted
            namelist-type output file.

        Raises
        ------

        NamelistInterfaceError:

            * raised if an exception is raised when creating the
              FORTRAN 90 namelist file.

        """

        # Build the namelist file and proceed accordingly.
        try:
            self.write(nml_dict=nml_dict, nml_template=nml_template, nml_path=nml_path)

            if self.strip_dblequotes:
                self.dblequotes_strip(nml_path=nml_path)

        except Exception as errmsg:
            msg = (
                f"Creation of FORTRAN 90 namelist file {nml_path} failed with "
                f"error {errmsg}. Aborting!!!"
            )
            raise NamelistInterfaceError(msg=msg) from errmsg
