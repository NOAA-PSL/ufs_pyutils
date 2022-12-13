# =========================================================================

# Module: utils/timestamp_interface.py

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

    timestamp_interface.py

Description
-----------

    This module defines supported time-stamp string formats; all
    formats assume the POSIX UNIX convention.

Globals
-------

    GLOBAL: str

        Global timestamp format; this is the format from which all
        others should be defined/determined.

Classes
-------

    TimestampInterfaceError(msg)

        This is the base-class for all exceptions; it is a sub-class
        of Error.

Functions
---------

    check_frmt(datestr, in_frmttyp = GLOBAL, out_frmttyp = GLOBAL)

        This function checks that the format for a provided timestamp
        matches the expected format.

Author(s)
---------

    Henry R. Winterbottom; 13 December 2022

History
-------

    2022-12-13: Henry Winterbottom -- Initial implementation.

"""

# ----

from tools import datetime_interface
from utils.error_interface import Error

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

# Global timestamp format; this is the format from which all others
# should be defined/determined.
GLOBAL = "%Y%m%d%H%M%S"

# ----


class TimestampInterfaceError(Error):
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

        Creates a new TimestampInterfaceError object.

        """
        super().__init__(msg=msg)


# ----


def check_frmt(
    datestr: str, in_frmttyp: str = GLOBAL, out_frmttyp: str = GLOBAL
) -> None:
    """
    Description
    -----------

    This function checks that the format for a provided timestamp
    matches the expected format.

    Parameters
    ----------

    datestr: str

        A Python string specifying the timestamp.

    Keywords
    --------

    in_frmttyp: str, optional

        A Python string specifying the assumed format for the
        timestamp string parameter; this assumes the POSIX UNIX
        convention.

    out_frmttyp: str, optional

        A Python string specifying the expected format for the
        timestamp string parameters; this assumes the POSIX UNIX
        convention.

    Raises
    ------

    TimestampInterfaceError:

        * raised if the provided timestamp string is not of the proper
          format.

    """

    # Define the timestamp string against which to compare the
    # parameter specified upon entry.
    check = datetime_interface.datestrupdate(
        datestr=datestr, in_frmttyp=in_frmttyp, out_frmttyp=out_frmttyp
    )

    if check != datestr:
        msg = (
            f"The timestamp string {datestr} does not match the format "
            f"{out_frmttyp}. Aborting!!!"
        )
        raise TimestampInterfaceError(msg=msg)
