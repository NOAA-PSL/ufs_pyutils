# =========================================================================

# $$$ MODULE DOCUMENTATION BLOCK

# UFS-RNR :: ush/ioapps/grib_interface.py

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

Classes
-------

   GRIBError(msg)

       This is the base-class for all exceptions; it is a sub-class of
       Exceptions.

Functions
---------

   _check_cnvgrib_env()

       This function checks whether the cnvgrib environment has been
       loaded; if not, a GRIBError will be thrown; if so, the path to
       the cnvgrib executable will be defined and returned.

   _check_grbindex_env()

       This function checks whether the grbindex application for GRIB
       version 1 environment has been loaded; if not, a GRIBError will
       be thrown; if so, the path to the grbindex executable will be
       defined and returned.

   _check_grb2index_env()

       This function checks whether the grbindex application for GRIB
       version 2 environment has been loaded; if not, a GRIBError will
       be thrown; if so, the path to the grbindex executable will be
       defined and returned.

   _check_wgrib_env()

       This function checks whether the wgrib environment has been
       loaded; if not, a GRIBError will be thrown; if so, the path to
       the wgrib executable will be defined and returned.

   _check_wgrib2_env()

       This function checks whether the wgrib2 environment has been
       loaded; if not, a GRIBError will be thrown; if so, the path to
       the wgrib2 executable will be defined and returned.

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

       This function parses a GRIB-formatted file and returns the GRIB
       records within.

   wgrib_remap(remap_obj, gribfile)

       This function remaps the variables within the respective WMO
       GRIB version 2 formatted file to a grid projection specified by
       the user in the remap_obj parameter; the remapped file is named
       <gribfile>.remap.

Author(s)
--------- 

   Henry R. Winterbottom; 30 January 2021

History
-------

   2021-01-30: Henry Winterbottom -- Initial implementation.

"""

# ----

import os
import subprocess

from produtil.error_interface import Error

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

__all__ = ['cnvgribg21', 'get_timestamp', 'grbindex', 'parse_file',
           'read_file', 'wgrib_remap']

# ----

class GRIBError(Exception):
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

    def __init__(self, msg):
        """
        Description
        -----------

        Creates a new GRIBError object.

        """
        super(GRIBError, self).__init__(msg=msg)

# ----

def _check_cnvgrib_env():
    """
    Description
    -----------

    This function checks whether the cnvgrib environment has been
    loaded; if not, a GRIBError will be thrown; if so, the path to the
    cnvgrib executable will be defined and returned.

    Returns
    -------

    cnvgrib: str

        A Python string specifying the path to the cnvgrib executable.

    Raises
    ------

    GRIBError:

        * raised if the cnvgrib executable path cannot be determined
          for the run-time platform.

    """

    # Define the cnvgrib executable path for the respective platform;
    # throw a GRIBError exception if it cannot be determined.
    cmd = ['which', 'cnvgrib']
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if len(out) > 0:
        cnvgrib = out.rstrip().decode('utf-8')
    else:
        msg = ('\n\nThe cnvgrib executable could not be determined for your '
               'system; please check that the appropriate GRIB '
               'libaries/modules are loaded prior to calling this function. '
               'Aborting!!!')
        raise GRIBError(msg=msg)
    return cnvgrib   

# ----

def _check_grbindex_env():
    """
    Description
    -----------

    This function checks whether the grbindex application for GRIB
    version 1 environment has been loaded; if not, a GRIBError will be
    thrown; if so, the path to the grbindex executable will be defined
    and returned.

    Returns
    -------

    grbindex: str

        A Python string specifying the path to the grbindex for GRIB
        version 1 executable.

    Raises
    ------

    GRIBError:

        * raised if the grbindex executable path cannot be determined
          for the run-time platform.

    """

    # Define the grbindex executable path for the respective platform;
    # throw a GRIBError exception if it cannot be determined.
    cmd = ['which', 'grbindex']
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if len(out) > 0:
        grbindex = out.rstrip().decode('utf-8')
    else:
        msg = ('\n\nThe grbindex executable could not be determined for '
               'your system; please check that the appropriate GRIB '
               'libaries/modules are loaded prior to calling this function. '
               'Aborting!!!')
        raise GRIBError(msg=msg)
    return grbindex   

# ----

def _check_grb2index_env():
    """
    Description
    -----------

    This function checks whether the grbindex application for GRIB
    version 2 environment has been loaded; if not, a GRIBError will be
    thrown; if so, the path to the grbindex executable will be defined
    and returned.

    Returns
    -------

    grbindex: str

        A Python string specifying the path to the grbindex for GRIB
        version 2 executable.

    Raises
    ------

    GRIBError:

        * raised if the grb2index executable path cannot be determined
          for the run-time platform.

    """

    # Define the grb2index executable path for the respective
    # platform; throw a GRIBError exception if it cannot be
    # determined.
    cmd = ['which', 'grb2index']
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if len(out) > 0:
        grb2index = out.rstrip().decode('utf-8')
    else:
        msg = ('\n\nThe grb2index executable could not be determined for '
               'your system; please check that the appropriate GRIB '
               'libaries/modules are loaded prior to calling this script. '
               'Aborting!!!')
        raise GRIBError(msg=msg)
    return grb2index    
            
# ----

def _check_wgrib_env():
    """
    Description
    -----------

    This function checks whether the wgrib environment has been
    loaded; if not, a GRIBError will be thrown; if so, the path to the
    wgrib executable will be defined and returned.

    Returns
    -------

    wgrib: str

        A Python string specifying the path to the wgrib executable.

    Raises
    ------

    GRIBError:

        * raised if the wgrib executable path cannot be determined for
          the run-time platform.

    """

    # Define the wgrib executable path for the respective platform;
    # throw a GRIBError exception if it cannot be determined.
    cmd = ['which', 'wgrib']
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if len(out) > 0:
        wgrib = out.rstrip().decode('utf-8')
    else:
        msg = ('\n\nThe wgrib executable could not be determined for '
               'your system; please check that the appropriate wgrib '
               'libaries/modules are loaded prior to calling this script. '
               'Aborting!!!')
        raise GRIBError(msg=msg)
    return wgrib

# ----

def _check_wgrib2_env():
    """
    Description
    -----------

    This function checks whether the wgrib2 environment has been
    loaded; if not, a GRIBError will be thrown; if so, the path to the
    wgrib2 executable will be defined and returned.

    Returns
    -------

    wgrib: str

        A Python string specifying the path to the wgrib executable.

    Raises
    ------

    GRIBError:

        * raised if the wgrib2 executable path cannot be determined
          for the run-time platform.

    """

    # Define the wgrib2 executable path for the respective platform;
    # throw a GRIBError exception if it cannot be determined.
    cmd = ['which', 'wgrib2']
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if len(out) > 0:
        wgrib = out.rstrip().decode('utf-8')
    else:
        msg = ('\n\nThe wgrib2 executable could not be determined for your system; '
               'please check that the appropriate wgrib libaries/modules are '
               'loaded prior to calling this script. Aborting!!!')
        raise GRIBError(msg=msg)
    return wgrib

# ----

def cnvgribg21(in_grib_file, out_grib_file):
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
    cnvgrib = _check_cnvgrib_env()
    cmd = ['{0}'.format(cnvgrib), '-g21', in_grib_file, out_grib_file]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (grbindex_out, grbindex_err) = proc.communicate()
    proc.wait()    
    
# ----


def get_timestamp(grib_file, grib_var=None):
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
    timestamp_list = list()
    for item in wgrib_out.rsplit():
        if grib_var is None:
            timestamp = item.split(':')[2].split('d=')[1]
        if grib_var is not None:
            if grib_var.lower() in item.lower():
                timestamp = item.split(':')[2].split('d=')[1]
        timestamp_list.append(timestamp)
    timestamp_list = list(set(timestamp_list))
    return timestamp_list

# ----

def grbindex(in_grib_file, out_gribidx_file, is_grib2=False):
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
    # throw a GRIBError exception if it cannot be determined.
    if is_grib2:
        grbindex_exe = _check_grb2index_env()
    if not is_grib2:
        grbindex_exe = _check_grbindex_env()
    cmd = ['{0}'.format(grbindex_exe), '{0}'.format(in_grib_file),
           '{0}'.format(out_gribidx_file)]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (grbindex_out, grbindex_err) = proc.communicate()
    proc.wait()

# ----

def parse_file(in_grib_file, parse_str, out_grib_file,
               is_grib2=False, tmp_out_path=None):
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
        GRIB-formatted (version 1 or 2) file; is not specified, the
        output file will be written to the directory in which this
        function was called.

    """

    # Specify the wgrib application in accordance with the input
    # GRIB-formatted file format upon entry.
    if is_grib2:
        wgrib = _check_wgrib2_env()
        cmd_base = [wgrib, in_grib_file, '-match']
    if not is_grib2:
        wgrib = _check_wgrib_env()
        cmd_base = [wgrib]
    if tmp_out_path is None:
        out_path = os.path.dirname(out_grib_file)
    if tmp_out_path is not None:
        out_path = tmp_out_path

    # Parse the input GRIB-formatted file accordingly.
    if is_grib2:
        cmd = ['{0}'.format(parse_str), '-grib', out_grib_file]   
        cmd = cmd_base + cmd
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        (wgrib_out, wgrib_err) = proc.communicate()
        proc.wait()
    if not is_grib2:
        cmd = ['{0} {1} | {2} | {3} -i {4} -grib -o {5}'.
               format(wgrib, in_grib_file, parse_str, wgrib, in_grib_file,
                      out_grib_file)]
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        (wgrib_out, wgrib_err) = proc.communicate()
        proc.wait()
    
# ----


def read_file(grib_file, is_4yr=True):
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
    wgrib = _check_wgrib_env()
    cmd = ['{0}'.format(wgrib)]
    if is_4yr:
        cmd.append('-4yr')
    cmd.append(grib_file)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (wgrib_out, wgrib_err) = proc.communicate()
    wgrib_out = wgrib_out.decode('utf-8')
    return wgrib_out

# ----

def wgrib2_remap(remap_obj, gribfile):
    """
    Description
    -----------

    This function remaps the variables within the respective WMO GRIB
    version 2 formatted file to a grid projection specified by the
    user in the remap_obj parameter; the remapped file is named
    <gribfile>.remap.

    Parameters
    ----------

    remap_obj: obj

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
    gribremap_file = gribfile + '.remap'
    wgrib = _check_wgrib2_env()
    cmd_base = [wgrib, gribfile]
    if remap_obj.new_grid.lower() == 'latlon':
        if remap_obj.new_grid_winds is not None:
            cmd = ['-new_grid_winds', '{0}'.format(remap_obj.new_grid_winds])
            cmd_base = cmd_base + cmd
        cmd = ['-new_grid', '%s' % remap_obj.new_grid, '%s:%s:%s' % \
               (remap_obj.lon0, remap_obj.nlons, remap_obj.dlon),
               '%s:%s:%s' % (remap_obj.lat0, remap_obj.nlats,
                             remap_obj.dlat), '%s' % gribremap_file]
        cmd = cmd_base + cmd
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (wgrib_out, wgrib_err) = proc.communicate()
    proc.wait()
    return gribremap_file 
