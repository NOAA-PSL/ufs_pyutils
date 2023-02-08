# =========================================================================

# Module: ioapps/grib_interface.py

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

    grib_interface.py

Description
-----------

    This module contains functions and classes to interface with the
    various GRIB utilities on the respective platform.

Functions
---------

    _get_app_path(app)

        This function checks whether the requested application path
        exists.

    cnvgribg21(in_grib_file, out_grib_file)

        This function converts a GRIB-formatted version 2 file to a
        GRIB-formatted version 1 file.

    get_timestamp(grib_file, grib_var = None)

        This function parses a GRIB-formatted file and returns the
        unique time-stamp elements; if a variable name (grib_var) is
        specified, the unique time-stamp elements correspond only to
        those GRIB records corresponding to the respective variable.

    grbindex(in_grib_file, out_gribidx_file, is_grib2 = False):

        This function generates a GRIB index file from an input
        GRIB-formatted (version 1 or 2) file.

    parse_file(in_grib_file, parse_str, out_grib_file, is_grib2 = False,
               tmp_out_path = None):

       This function parses a GRIB-formatted (version 1 or 2) file and
       collects the user specified variables (parse_str) and
       defines/constructs a new GRIB-formatted (version 1 or 2) file;
       the new GRIB-formatted (version 1 or 2) file is a concatenated
       file created from individual files for each user specified GRIB
       variable and level; following concatenation, all temporary
       GRIB-formatted (version 1 or 2) files are removed.

    read_file(grib_file, is_4yr = True)

        This function parses a GRIB-formatted file and returns the
        GRIB records within.

    wgrib_remap(remap_obj, gribfile)

        This function remaps the variables within the respective WMO
        GRIB version 2 formatted file to a grid projection specified
        by the user in the remap_obj parameter; the remapped file is
        named <gribfile>.remap.

Requirements
------------

- cnvgrib; https://github.com/NOAA-EMC/NCEPLIBS-grib_util

- grbindex; https://github.com/NOAA-EMC/NCEPLIBS-grib_util

- grb2index; https://github.com/NOAA-EMC/NCEPLIBS-grib_util

- wgrib; https://github.com/NOAA-EMC/NCEPLIBS-grib_util

- wgrib2; https://github.com/NOAA-EMC/NCEPLIBS-grib_util

Author(s)
---------

   Henry R. Winterbottom; 29 November 2022

History
-------

   2022-11-29: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=consider-using-with
# pylint: disable=unused-variable

# ----

import os
import subprocess
from typing import List

from tools import system_interface
from utils.exceptions_interface import GRIBInterfaceError

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

__all__ = [
    "cnvgribg21",
    "get_timestamp",
    "grbindex",
    "parse_file",
    "read_file",
    "wgrib2_remap",
]

# ----


def _get_app_path(app: str) -> str:
    """
    Description
    -----------

    This function checks whether the requested application path has
    been loaded; if not, a GRIBError will be thrown.

    Parameters
    ----------

    app: str

        A Python string specifying the name of the application for
        which to return the respective path.

    Returns
    -------

    app_path: str

        A Python string specifying the path to the application name
        provided upon entry; if the application path cannot be
        determined, this value is NoneType.

    Raises
    ------

    GRIBInterfaceError:

        * raised if the cnvgrib executable path cannot be determined
          for the run-time platform.

    """

    # Define the cnvgrib executable path for the respective platform;
    # proceed accordingly.
    app_path = system_interface.get_app_path(app=app)

    if app_path is None:
        msg = f"The {app} path could not be determined for your " "system. Aborting!!!"
        raise GRIBInterfaceError(msg=msg)

    return app_path


# ----


def cnvgribg21(in_grib_file: str, out_grib_file: str) -> None:
    """
    Description
    -----------

    This function converts a GRIB-formatted version 2 file to a
    GRIB-formatted version 1 file.

    Parameters
    ----------

    in_grib_file: str

        A Python string specifying the path to the input
        GRIB-formatted version 2 file.

    out_grib_file: str

        A Python string specifying the path to the output
        GRIB-formatted version 1 file.

    """

    # Convert the GRIB-formatted input file to the output file path
    # specified upon entry.
    cnvgrib = _get_app_path(app="cnvgrib")
    cmd = [f"{cnvgrib}", "-g21", in_grib_file, out_grib_file]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    proc.communicate()
    proc.wait()


# ----


def get_timestamp(grib_file: str, grib_var: str = None) -> List:
    """
    Description
    -----------

    This function parses a GRIB-formatted file and returns the unique
    time-stamp elements; if a variable name (grib_var) is specified,
    the unique time-stamp elements correspond only to those GRIB
    records corresponding to the respective variable.

    Parameters
    ----------

    grib_file: str

        A Python string specifying the path to the GRIB-formatted
        file.

    Keywords
    --------

    grib_var: str, optional

        A Python string specifying the variable name for which to
        retrive time-stamp elements.

    Returns
    -------

    timestamp_list: list

        A Python list containing the unique time-stamp elements
        collected from the GRIB records.

    """

    # Collect the timestamp for the specified GRIB-formatted file in
    # accordance with the specified keyword arguments.
    wgrib_out = read_file(grib_file=grib_file)

    timestamp_list = []
    for item in wgrib_out.rsplit():
        if grib_var is None:
            timestamp = item.split(":")[2].split("d=")[1]

        if grib_var is not None:
            if grib_var.lower() in item.lower():
                timestamp = item.split(":")[2].split("d=")[1]
        timestamp_list.append(timestamp)

    timestamp_list = list(set(timestamp_list))

    return timestamp_list


# ----


def grbindex(in_grib_file: str, out_gribidx_file: str, is_grib2: bool = False) -> None:
    """
    Description
    -----------

    This function generates a GRIB index file from an input
    GRIB-formatted (version 1 or 2) file.

    Parameters
    ----------

    in_grib_file: str

        A Python string specifying the path to the GRIB-formatted
        (version 1 or 2) for which to generate the GRIB index file.

    out_gribidx_file: str

        A Python string specifying the path to the GRIB index file
        generated from the GRIB-formatted (version 1 or 2) input file.

    Keywords
    --------

    is_grib2: bool, optional

        A Python boolean valued variable specifying whether to
        generate the index file using GRIB version 2 index file
        application.

    """

    # Define the cnvgrib executable path for the respective platform;
    # proceed accordingly.
    if is_grib2:
        grbindex_exe = _get_app_path(app="grb2index")

    if not is_grib2:
        grbindex_exe = _get_app_path(app="grbindex")

    cmd = [f"{grbindex_exe}", f"{in_grib_file}", f"{out_gribidx_file}"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    proc.communicate()
    proc.wait()


# ----


def parse_file(
    in_grib_file: str,
    parse_str: str,
    out_grib_file: str,
    is_grib2: bool = False,
    tmp_out_path: str = None,
) -> None:
    """
    Description
    -----------

    This function parses a GRIB-formatted (version 1 or 2) file and
    collects the user specified variables (parse_str) and
    defines/constructs a new GRIB-formatted (version 1 or 2) file; the
    new GRIB-formatted (version 1 or 2) file is a concatenated file
    created from individual files for each user specified GRIB
    variable and level; following concatenation, all temporary
    GRIB-formatted (version 1 or 2) files are removed.

    Parameters
    ----------

    in_grib_file: str

        A Python string specifying the path to the GRIB-formatted
        (version 1 or 2) file to be parsed.

    parse_str: str

        A Python string specifying the GRIB variables to be collected
        to define the new GRIB-formatted (version 1 or 2) file.

    out_grib_file: str

        A Python string specifying the path to the GRIB-formatted
        (version 1 or 2) file concatenated from the temporary
        GRIB-formatted (version 1 or 2) files.

    Keywords
    --------

    is_grib2: bool, optional

        A Python boolean valued variable specifying whether to parse
        the respective input GRIB-formatted version 2 file using the
        wgrib2 applications.

    tmp_out_path: str, optional

        A Python string specifying the path to the output
        GRIB-formatted (version 1 or 2) file; if not specified, the
        output file will be written to the directory in which this
        function was called.

    """

    # Specify the wgrib application in accordance with the input
    # GRIB-formatted file format upon entry.
    if is_grib2:
        wgrib = _get_app_path(app="wgrib2")
        cmd_base = [wgrib, in_grib_file, "-match"]

    if not is_grib2:
        wgrib = _get_app_path(app="wgrib")
        cmd_base = [wgrib]

    if tmp_out_path is None:
        out_path = os.path.dirname(out_grib_file)

    if tmp_out_path is not None:
        out_path = tmp_out_path

    # Parse the input GRIB-formatted file accordingly.
    if is_grib2:
        cmd = [f"{parse_str}", "-grib", out_grib_file]
        cmd = cmd_base + cmd
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate()
        proc.wait()

    if not is_grib2:
        cmd = [
            f"{wgrib} {in_grib_file} | {parse_str} | {wgrib} -i "
            f"{in_grib_file} -grib -o {out_grib_file}"
        ]
        proc = subprocess.Popen(
            cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        proc.communicate()
        proc.wait()


# ----


def read_file(grib_file: str, is_4yr: bool = True) -> List:
    """
    Description
    -----------

    This function parses a GRIB-formatted file and returns the GRIB
    records within.

    Parameters
    ----------

    grib_file: str

        A Python string specifying the path to the GRIB-formatted
        file.

    Keywords
    --------

    is_4yr: bool, optional

        A Python boolean valued variables specifying whether to format
        the respective GRIB record time-stamps using a 4-digit year
        value.

    Returns
    -------

    wgrib_out: list

         A Python list containing the GRIB records from the parsed
         GRIB-formatted file.

    """

    # Collect and return the records contained within the
    # GRIB-formatted file on entry.
    wgrib = _get_app_path(app="wgrib")
    cmd = [f"{wgrib}"]

    if is_4yr:
        cmd.append("-4yr")
    cmd.append(grib_file)

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (wgrib_out, _) = proc.communicate()
    proc.wait()
    wgrib_out = wgrib_out.decode("utf-8")

    return wgrib_out


# ----


def wgrib2_remap(remap_obj: object, gribfile: str) -> str:
    """
    Description
    -----------

    This function remaps the variables within the respective WMO GRIB
    version 2 formatted file to a grid projection specified by the
    user in the remap_obj parameter; the remapped file is named
    <gribfile>.remap.

    Parameters
    ----------

    remap_obj: object

        A Python object containing the WMO GRIB version 2 formatted
        data remapping attributes; currently only 'latlon' remappings
        are supported.

    gribfile: str

        A Python string specifying the path to the WMO GRIB version 2
        formatted file, containing the respective WMO GRIB version 2
        formatted data, to be remapped.

    Returns
    -------

    gribremap_file: str

        A Python string specifying the path to the WMO GRIB version 2
        formatted file containing the remapped data.

    """

    # Parse the GRIB-formatted (version 2) file and project (i.e.,
    # remap) to the grid projection specified on entry.
    gribremap_file = gribfile + ".remap"
    wgrib = _get_app_path(app="wgrib2")
    cmd_base = [wgrib, gribfile]

    if remap_obj.new_grid.lower() == "latlon":
        if remap_obj.new_grid_winds is not None:
            cmd = ["-new_grid_winds", f"{remap_obj.new_grid_winds}"]

            cmd_base = cmd_base + cmd

        cmd = [
            "-new_grid",
            f"{remap_obj.new_grid}",
            f"{remap_obj.lon0}:{remap_obj.nlons}:{remap_obj.dlon}",
            f"{remap_obj.lat0}:{remap_obj.nlats}:{remap_obj.dlat}",
            f"{gribremap_file}",
        ]

        cmd = cmd_base + cmd
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()
    proc.wait()

    return gribremap_file
