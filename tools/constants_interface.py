# =========================================================================

# Module: tools/constants_interface.py

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

    constants_interface.py

Description
-----------

    This module defines conversion values for transformations between
    compatiable unit systems.

Globals
-------

    kts2mps: float

        Conversion value for transforming nautical miles per hour
        (knots) to meters per second.

    mps2kts: float

        Conversion value for transforming meters per second to
        nautical miles per hour (knots).

Author(s)
---------

    Henry R. Winterbottom; 07 August 2022

History
-------

    2022-08-07: Henry Winterbottom -- Initial implementation.

"""

# ----

from astropy import units

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

# Conversion value for transforming nautical miles per hour (knots) to
# meters per second.
kts2mps = (units.imperial.kn).to(units.meter / units.second) * (
    units.meter / units.second
)

# Conversion value for transforming meters per second to nautical
# miles per hour (knots).
mps2kts = (units.meter / units.second).to(units.imperial.kn) * units.imperial.kn
