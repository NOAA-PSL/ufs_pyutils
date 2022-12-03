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

    This module contains constant values to convert between various
    variable value units.

Globals
-------

    kts2mps: float

        Conversion value for transforming knots to meters per second.

    mps2kts: float

        Conversion value for transforming meters per second to knots.

Author(s)
---------

    Henry R. Winterbottom; 07 August 2022

History
-------

    2022-08-07: Henry Winterbottom -- Initial implementation.

"""

# ----

import numpy

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

# Conversion value for transforming knots to meters per second.
kts2mps = numpy.float64(0.514444)

# Conversion value for transforming meters per second to knots.
mps2kts = numpy.float64(1.0/kts2mps)
