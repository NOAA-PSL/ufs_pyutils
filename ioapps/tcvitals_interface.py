# =========================================================================

# Module: ioapps/tcvitals_interface.py

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

    tcvitals_interface.py

Description
-----------

    This module contains functions to write TC-vitals records.

Classes
-------

    TCVitalsError(msg)

        This is the base-class for all exceptions; it is a sub-class
        of Error.

Functions
---------

    write_tcvfile(filepath, tcvstr)

        This function writes a user-specified TC-vitals record(s) to a
        specified filepath.

    write_tcvstr(tcvit_obj)

        This function writes a string formatted in accordance with the
        TC-vitals format.

Author(s)
--------- 

    Henry R. Winterbottom; 03 December 2022

History
-------

    2022-12-02: Henry Winterbottom -- Initial implementation.

"""

# ----

import numpy
from tools import parser_interface
from utils import constants_interface
from utils.error_interface import Error
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["write_tcvfile", "write_tcvstr"]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class TCVitalsError(Error):
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

        Creates a new TCVitalsError object.

        """
        super(TCVitalsError, self).__init__(msg=msg)


# ----


def write_tcvfile(filepath: str, tcvstr: str) -> None:
    """
    Description
    -----------

    This function writes a user-specified TC-vitals record(s) to a
    specified filepath.

    Parameters
    ----------

    filepath: str

        A Python string specifying the file path to which to write the
        TC-vitals record(s).

    tcvstr: str

        A Python string containing the TC-vitals record(s).

    """

    # Write the TC-vitals record(s) to the specified filepath.
    msg = "Writing TC-Vitals file {0}.".format(filepath)
    logger.info(msg=msg)
    with open(filepath, "w") as f:
        f.write(tcvstr)


# ----


def write_tcvstr(tcvit_obj: object) -> str:
    """
    Description
    -----------

    This function writes a string formatted in accordance with the
    TC-vitals format.

    Parameters
    ----------

    tcvit_obj: object

        A Python object containing the TC-vitals record attributes;
        the Python object attributes are as follows:

        Required Attributes
        -------------------

        lat: a Python float valued variable specifying the latitude
        geographical coordinate position; a negative value denotes a
        position in the Southern Hemisphere; input values range is
        -90.0 to 90.0; units are degrees.

        lon: a Python float valued variable specifying the longitude
        geographical coordinate position; a negative value denotes a
        position in the Western Hemisphere; input values range is
        -180.0 to 180.0 degrees; units are degrees.

        mslp: a Python float valued variable specifying minimum
        sea-level pressure intensity; units are hectoPascals (e.g.,
        millibars).

        tcid: a Python string variable specifying the TC identifier
        (e.g, 01L, for the first TC in the North Atlantic basin); this
        string has a 3-character maximum length.

        time_ymd: a Python string specifying the year/month/day
        attribute for the respective TC-vitals record; this string
        assumes the POSIX UNIX time-stamp convention %Y%m%d; this
        string has a 8-character maximum length.

        time_hm: a Python string specifying the hour/minute attribute
        for the respective TC-vitals record; this string assumes the
        POSIX UNIX time-stamp convention %H%M; this string has a
        4-character maximum length.

        vmax: a Python float valued variable specifying maximum wind
        speed intensity; units are meters per second.

        Optional Attributes
        -------------------

        event_name: a Python string specifying the name assigned by
        the respective forecast center (if any); if one has not been
        specified, a value of 'NAMELESS' will be assigned; this string
        has a 9-character maximum length.

        NE34, SE34, SW34, NW34: a Python float value specifying the
        radius of the 34-knot wind in the respective quadrant of the
        TC; units are kilometers; if one has not been specified, a
        value of -999 will be assigned.

        poci: a Python float value specifying the pressure of the
        outer-most closed isobar relative to the TC geographical
        coordinates position (above); units are hectoPascals (e.g.,
        millibars); if one has not been specified, a value of -999
        will be assigned.

        rmw: a Python float value specifying the radius of maximum
        wind speed; units are kilometers; if one has not been
        specified, a value of -99 will be assigned.

        roci: a Python float value specifying the radius of the
        outer-most closed isobar relative to the TC geographical
        coordinates position (above); units are kilometers; if one has
        not been specified, a value of -999 will be assigned.

        tcv_center: a Python string variable specifying the
        forecasting center from which the TC-vitals record corresponds
        or was created (from); if one has not been specified, a value
        of 'XXXX' will be assigned.

        stormdepth: a Python string value specifying the TC depth
        (e.g., 'S' for top of circulation at 700-hPa, 'M' for top of
        circulation at 400-hPa, and 'D' for top of circulation at
        200-hPa); if one has not been specified, a value of 'X' will
        be assigned.

        stormdir: a Python float value specifying the translational
        direction for the TC in the respective TC-vitals record; units
        are degrees relative to North; if one has been specified, a
        value of -99 will be assigned.

        stormspeed: a Python string specifying the translational speed
        for the TC in the respective TC-vitals record; units are
        meters per second; if one has been specified, a value of -99
        will be assigned.

    Returns
    -------

    tcvstr: str

        A Python string containing the TC-vitals record.

    Raises
    ------

    TCVitalsError:

        * raised if the TC-vitals attribute object provided upon entry
          does not contain a mandatory TC-vitals record
          attribute/value.

    """

    # Define the TC-vitals record attributes.
    tcvstr = str()
    tcvobj = parser_interface.object_define()
    tcvstr_frmt = (
        "%-4s %-3s %-9s %s %s %s %s %03d %03d %04d %04d %04d "
        "%02d %03d %04d %04d %04d %04d %s\n"
    )

    # Check that all mandatory TC-vitals record attributes are
    # specified; proceed accordingly.
    mand_attr_list = ["lat", "lon", "mslp",
                      "tcid", "time_hm", "time_ymd", "vmax"]

    for mand_attr in mand_attr_list:
        if not parser_interface.object_hasattr(object_in=tcvit_obj, key=mand_attr):
            msg = (
                "The input TC-vitals variable object does not contain "
                "the mandatory attribute {0}. Aborting!!!".format(mand_attr)
            )
            raise TCVitalsError(msg=msg)

        # Build the TC-vitals record object.
        value = parser_interface.object_getattr(
            object_in=tcvit_obj, key=mand_attr)
        tcvobj = parser_interface.object_setattr(
            object_in=tcvobj, key=mand_attr, value=value
        )

    # Check the TC-vitals record attributes; proceed accordingly.
    if (
        (tcvobj.lat is None)
        or (tcvobj.lon is None)
        or (tcvobj.mslp is None)
        or (tcvobj.vmax is None)
    ):
        msg = (
            "Received a NoneType value for a required TC vitals record; no "
            "TC-vitals string will be created."
        )
        logger.warn(msg=msg)

        return tcvstr

    # Convert the wind speed units from knots to meters-per-second.
    tcvobj.vmax = (tcvobj.vmax * constants_interface.kts2mps).value

    # Define default values for the optional TC-vitals record
    # attributes.
    opt_attr_dict = {
        "event_name": "NAMELESS",
        "NE34": -999,
        "SE34": -999,
        "SW34": -999,
        "NW34": -999,
        "poci": -999,
        "rmw": -99,
        "roci": -999,
        "tcv_center": "XXXX",
        "stormdepth": "X",
        "stormdir": -99,
        "stormspeed": -99,
    }

    # Define the optional TC-vitals record attributes in accordance
    # with the values provided upon entry.
    for opt_attr in opt_attr_dict.keys():

        # Collect the TC-vitals record attribute; proceed accordingly.
        if parser_interface.object_hasattr(object_in=tcvit_obj, key=opt_attr):
            value = parser_interface.object_getattr(
                object_in=tcvit_obj, key=opt_attr)
        else:
            value = parser_interface.dict_key_value(
                dict_in=opt_attr_dict, key=opt_attr, no_split=True
            )

        # Define the TC-vitals record attribute.
        tcvobj = parser_interface.object_setattr(
            object_in=tcvobj, key=opt_attr, value=value
        )

    # Check that the TC-vitals records are valid; proceed accordingly.
    if (tcvobj.lat is not None) and (tcvobj.lon is not None):

        # Scale the hemisphere values accordingly.
        hemip = "N" if (tcvobj.lat > 0) else "S"
        hemim = "E" if (tcvobj.lon < 0) else "W"
        tcvobj.lat = "%03d%s" % (numpy.abs(numpy.rint(tcvobj.lat * 10)), hemip)
        tcvobj.lon = "%04d%s" % (numpy.abs(numpy.rint(tcvobj.lon * 10)), hemim)

        # Write the TC-vitals record.
        tcvstr = tcvstr_frmt % (
            tcvobj.tcv_center,
            tcvobj.tcid,
            tcvobj.event_name,
            tcvobj.time_ymd,
            tcvobj.time_hm,
            tcvobj.lat,
            tcvobj.lon,
            tcvobj.stormdir,
            tcvobj.stormspeed,
            tcvobj.mslp,
            tcvobj.poci,
            tcvobj.roci,
            tcvobj.vmax,
            tcvobj.rmw,
            tcvobj.NE34,
            tcvobj.SE34,
            tcvobj.SW34,
            tcvobj.NW34,
            tcvobj.stormdepth,
        )
        msg = "Constructed the following TC-vitals record:\n{0}".format(tcvstr)
        logger.info(msg=msg)

    return tcvstr
