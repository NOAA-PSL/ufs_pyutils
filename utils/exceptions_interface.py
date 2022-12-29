# =========================================================================

# Module: utils/exceptions_interface.py

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


"""

# ----

from utils.error_interface import Error
from utils.error_interface import msg_except_handle

# ----

# Define all available attributes.
__all__ = ["ArgumentsInterfaceError",
           "SchemaInterfaceError",
           "TimestampsInterfaceError"]

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class ArgumentsInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    utils/arguments_interface module; it is a sub-class of Error.

    """

# ----


class SchemaInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    utils/schema_interface module; it is a sub-class of Error.

    """

# ----


class TimestampInterfaceError(Error):
    """
    Description
    -----------

    This is the base-class for exceptions encountered within the
    utils/timestamp_interface module; it is a sub-class of Error.

    """

# ----
