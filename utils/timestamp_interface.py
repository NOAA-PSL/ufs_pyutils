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

    timestamp_global: str

        Global timestamp format; this is the format from which all
        others should be defined/determined.

Author(s)
---------

    Henry R. Winterbottom; 13 December 2022

History
-------

    2022-12-13: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

# Global timestamp format; this is the format from which all others
# should be defined/determined.
timestamp_global = "%Y%m%d%H%M%S"
