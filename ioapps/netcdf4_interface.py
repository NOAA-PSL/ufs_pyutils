# =========================================================================

# $$$ MODULE DOCUMENTATION BLOCK

# UFS-RNR :: ush/ioapps/netcdf4_interface.py

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

    netcdf4_interface.py

Description
-----------

    This module contains functions which interface with the Python
    netCDF4 library.

Classes
-------

    NCError(msg)

        This is the base-class for all exceptions; it is a sub-class
        of Error.

Functions
---------

    _get_ncapp_path(ncapp):

        This function checks whether the netCDF application request
        upon entry exists; loaded; if not, a NCError will be thrown;
        if so, the path to the respective netCDF application will be
        defined and returned.


    _read_ncdim_obj(ncdim_obj)

        This function parses a user-specified object containing netCDF
        dimension variable attributes and builds a Python dictionary
        containing key and value pairs define the a netCDF variable
        dimensions; the designation between user-specified attributes
        and namespace attributes is made by checking the respective
        string formats.

    _read_ncvar_obj(ncvar_obj)

        This function parses a user-specified object containing netCDF
        variable attributes and builds a Python dictionary containing
        key and value pairs define the a netCDF variable attronites;
        the designation between user-specified attributes and
        namespace attributes is made by checking the respective string
        formats.

    nccheck(ncfile, ncfrmt=None)

        This function checks whether a given file path is a netCDF
        formatted file and returns a boolean valued variable
        specifying such.

    ncconcat(ncfilelist, ncfile, ncdim, ncfrmt=None)

        This function concatenates a list of netCDF files, provided in
        ncfilelist, into a single file (ncfile); the concatenation is
        performed along a single user-specified dimension (ncdim);
        optional arguments enable the user to specify the format of
        the concatenated file.

    nccopy(ncfilein, ncfileout, ncfrmtout, ncfrmtin=None,
           ncvarlist=None, ncunlimval=None, use_nccopy=False):

        This function performs a direct copy of an input netCDF file
        to a user specified output netCDF file of a user specified
        format.

    nccopyvar(ncfilein, ncfileout, ncvarname, ncvar, ncout_mode,
              ncfrmtin=None, ncfrmtout=None):

        This function performs a direct copy of a user specified
        variable from a user specified input (e.g., source) file to a
        user specified output (destination) file.

    ncnumvar(ncfile, ncfrmt=None)

        This function parses a netCDF file to determine the total
        number of variable arrays within the respective file.

    ncreadattr(ncfile, ncattrname, ncvarname=None, ncfrmt=None):

        This function parses a netCDF file to collect the user
        specified netCDF attribute value(s).

    ncreaddim(ncfile, ncdimname, ncfrmt=None):

        This function parses a netCDF file to collect and return the
        dimension size for the user specified dimension variable name.

    ncreadvar(ncfile, ncvarname, ncfrmt=None, from_ncgroup=False,
              ncgroupname=None, squeeze=False, axis=None, level=None)

        This function parses a netCDF file in order to collect and
        return the values for the user specified variable; this
        function also provides optional capabilities to apply the
        numpy squeeze application to truncate to the user specified
        dimensions.

    ncvarlist(ncfile, ncfrmt=None):

        This function reads and returns a list of variables within the
        netCDF file specified upon entry.

    ncvarexist(ncfilein, ncvarname, ncfrmtin=None)

        This function reads a netCDF file and queries the variable
        list for the existence of a user specified variable name
        (ncvarname); it returns a boolean values indicating whether
        the variable name has been found.

    ncwrite(ncfile, ncdim_obj, ncvar_obj, ncfrmt=None):

        This function writes a netCDF file, containing the dimensions,
        variables, and (optional) attributes, specified by the user.

    ncwritevar(ncfile, ncvarname, ncvar, ncfrmt=None)

        This function opens a netCDF file and writes the array(ncvar)
        values for the user specified variable to the respective
        (open) netCDF file.

Requirements
------------

- netCDF4; https://github.com/Unidata/netcdf4-python

Author(s)
---------

    Henry R. Winterbottom; 22 August 2022

History
-------

    2022-08-22: Henry Winterbottom - - Initial implementation.

"""

# ----

import netCDF4
import numpy
import os
import subprocess

from produtil.error_interface import Error
from produtil.logger_interface import Logger
from tools import parser_interface

# ----

# Define all available functions.
__all__ = ['nccheck',
           'ncconcat',
           'nccopy',
           'nccopyvar',
           'ncnumvar',
           'ncreadattr',
           'ncreaddim',
           'ncreadvar',
           'ncvarexist',
           'ncvarlist',
           'ncwrite',
           'ncwritevar'
           ]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class NCError(Error):
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

    def __init__(self, msg):
        """
        Description
        -----------

        Creates a new NCError object.

        """
        super(NCError, self).__init__(msg=msg)

# ----


def _get_ncapp_path(ncapp):
    """
    Description
    -----------

    This function checks whether the netCDF application request upon
    entry exists; loaded; if not, a NCError will be thrown; if so, the
    path to the respective netCDF application will be defined and
    returned.

    Parameters
    ----------

    ncapp: str

        A Python string specifying the name of the netCDF application.

    Returns
    -------

    ncapp_path: str

        A Python string specifying the path to the netCDF application
        specified upon entry.

    Raises
    ------

    NCError:

        * raised if the netCDF application path cannot be determined.

    """

    # Check the run-time environment in order to determine the netCDF
    # application path.
    cmd = ['which', '{0}'.format(ncapp)]
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = proc.communicate()

    # Define the netCDF application path; proceed accordingly.
    if len(out) > 0:
        ncapp_path = out.rstrip().decode('utf-8')
    else:
        msg = ('The path for the netCDF application {0} could not be '
               'determined for your system; please check that the appropriate '
               'libaries/modules are loaded prior to calling this script. '
               'Aborting!!!'.format(ncapp))
        raise NCError(msg=msg)

    return ncapp_path


# ----


def _read_ncdim_obj(ncdim_obj):
    """
    Description
    -----------

    This function parses a user-specified object containing netCDF
    dimension variable attributes and builds a Python dictionary
    containing key and value pairs define the a netCDF variable
    dimensions; the designation between user-specified attributes and
    namespace attributes is made by checking the respective string
    formats.

    Parameters
    ----------

    ncdim_obj: obj

        A user specified Python object containing(a) netCDF dimension
        attribute(s).

    Returns
    -------

    ncdim_dict: dict

        A Python dictionary containing the user-specified netCDF
        variable dimension attributes.

    """

    # Collect the netCDF dimension attributes.
    ncdim_dict = dict()
    keys = vars(ncdim_obj)
    for key in keys:
        value = parser_interface.object_getattr(
            object_in=ncdim_obj, key=key)
        ncdim_dict[key] = value

    return ncdim_dict

# ----


def _read_ncvar_obj(ncvar_obj):
    """
    Description
    -----------

    This function parses a user-specified object containing netCDF
    variable attributes and builds a Python dictionary containing key
    and value pairs define the a netCDF variable attronites; the
    designation between user-specified attributes and namespace
    attributes is made by checking the respective string formats.

    Parameters
    ----------

    ncvar_obj: obj

        A user specified Python object containing the netCDF variable
        attribute(s).

    Returns
    -------

    ncvar_dict: dict

        A Python dictionary containing the user-specified netCDF
        variable attributes.

    """

    # Collect the netCDF variable attributes.
    ncvar_dict = dict()
    keys = vars(ncvar_obj)
    for key in keys:
        value = parser_interface.object_getattr(
            object_in=ncvar_obj, key=key)
        ncvar_dict[key] = value

    return ncvar_dict

# ----


def nccheck(ncfile, ncfrmt=None):
    """
    Description
    -----------

    This function checks whether a given file path is a netCDF
    formatted file and returns a boolean valued variable specifying
    such.

    Parameters
    ----------

    ncfile: str

        A Python string specifying the netCDF file to be read.

    Keywords
    --------

    ncfrmt: str, optional

        A Python string specifying the format of the netCDF file(to
        be created); available options are NETCDF4_CLASSIC,
        NETCDF3_CLASSIC, NETCDF3_64BIT_OFFSET, or NETCDF3_64BIT_DATA;
        if not specified, NETCDF4_CLASSIC is assumed.

    Returns
    -------

    is_ncfile: bool

        A Python boolean valued variable specifying whether the
        specified input file is a netCDF formatted file.

    """

    # Check whether the specified file path is a valid
    # netCDF-formatted file and proceed accordingly.
    if ncfrmt is None:
        ncfrmt = 'NETCDF4_CLASSIC'
    try:
        ncfile = netCDF4.Dataset(filename=ncfile, mode='r',
                                 format=ncfrmt)
        is_ncfile = True
    except OSError:
        is_ncfile = False

    return is_ncfile

# ----


def ncconcat(ncfilelist, ncfile, ncdim, ncfrmt=None):
    """
    Description
    -----------

    This function concatenates a list of netCDF files, provided in
    ncfilelist, into a single file(ncfile); the concatenation is
    performed along a single user-specified dimension(ncdim);
    optional arguments enable the user to specify the format of the
    concatenated file.

    Parameters
    ----------

    ncfilelist: str

        A Python string containing the list of netCDF files to be
        concatenated.

    ncfile: str

        A Python string specifying the netCDF file(to be created)
        containing the concatenated values collected from each of the
        files to be concatenated.

    ncdim: str

        A Python string specifying the netCDF variable dimension along
        which to concatenated the respective netCDF files list.

    Keywords
    --------

    ncfrmt: str, optional

        A Python string specifying the format of the netCDF file
        containing the concatenated values collected from each of the
        files to be concatenated; available options are
        NETCDF4_CLASSIC, NETCDF3_CLASSIC, NETCDF3_64BIT_OFFSET, or
        NETCDF3_64BIT_DATA; if not specified, NETCDF4_CLASSIC is
        assumed.

    """

    # Open the destination netCDF-formatted file and read each
    # variable dimension from the respective source files and define
    # the total array dimension along which the source
    # netCDF-formatted files are to be concatenated.
    if ncfrmt is None:
        ncfrmt = 'NETCDF4_CLASSIC'
    ncdimsum = 0
    dstfile = netCDF4.Dataset(filename=ncfile, mode='w', format=ncfrmt)
    for item in ncfilelist:
        srcfile = netCDF4.Dataset(item)
        for (name, dimension) in srcfile.dimensions.items():
            if name == ncdim:
                ncdimsum = ncdimsum + len(dimension)
        srcfile.close()

    # Define the total dimension size for the destination
    # netCDF-formatted file arrays.
    srcfile = netCDF4.Dataset(filename=ncfilelist[0], mode='r')
    for (name, dimension) in srcfile.dimensions.items():
        if name == ncdim:
            dimsize = ncdimsum
        else:
            dimsize = (len(dimension) if not dimension.isunlimited()
                       else None)
        dstfile.createDimension(name, dimsize)

    # Collect and define the destination netCDF-formatted file
    # attributes.
    for (name, variable) in srcfile.variables.items():
        x = dstfile.createVariable(
            name, variable.datatype, variable.dimensions)
        dstfile[name].setncatts(srcfile[name].__dict__)
    dstfile.setncatts(srcfile.__dict__)

    # Concatenate the variables along the specified axis (i.e.,
    # dimension) and write the results to the destination
    # netCDF-formatted file.
    mxncdimsum = ncdimsum
    ncdimsum = 0
    for item in ncfilelist:
        srcfile = netCDF4.Dataset(item)
        ncdimval = len(srcfile.dimensions[ncdim])
        start = ncdimsum
        stop = start + ncdimval
        for (name, variable) in srcfile.variables.items():
            if ncdim in variable.dimensions:
                dstfile[name][start:stop] = srcfile[name][:]
        ncdimsum = stop
    dstfile.close()
    srcfile.close()

# ----


def nccopy(ncfilein, ncfileout, ncfrmtout, ncfrmtin=None, ncvarlist=None,
           ncunlimval=None, use_nccopy=False):
    """
    Description
    -----------

    This function performs a direct copy of an input netCDF file to a
    user specified output netCDF file of a user specified format.

    Parameters
    ----------

    ncfilein: str

        A Python string specifying the input netCDF file to be copied.

    ncfileout: str

        A Python string specifying the netCDF file(to be created)
        containing the contents of the input netCDF file.

    ncfrmtout: str

        A Python string specifying the format of the netCDF file to be
        created; available options are NETCDF4_CLASSIC,
        NETCDF3_CLASSIC, NETCDF3_64BIT_OFFSET, or NETCDF3_64BIT_DATA.

    Keywords
    --------

    ncfrmtin: str, optional

        A Python string specifying the format of the input netCDF
        file; available options are NETCDF4_CLASSIC, NETCDF3_CLASSIC,
        NETCDF3_64BIT_OFFSET, or NETCDF3_64BIT_DATA; if not specified,
        NETCDF4_CLASSIC is assumed.

    ncvarlist: list, optional

        A Python list of variable name strings; if NoneType, the
        variables within the list will be the only variables written
        to the destination netCDF file.

    ncunlimval: int, optional

        A Python integer value specifying the unlimited dimension
        size; if NoneType, the dimension size will be 0.

    use_nccopy: bool, optional

        A Python boolean valued variable specifying whether to use the
        netCDF nccopy utility to produce a direct copy of the
        netCDF-formatted file specified upon entry.

    """

    # Use the netCDF applications on the local platform to produce a
    # copy of the netCDF formatted file provided upon entry; this
    # should be used in instances of netCDF files containing
    # hierarchial groups.
    if use_nccopy:

        # Define the nccopy application for the local platform.
        nccopy_app = _get_ncapp_path(ncapp='nccopy')

        # Define the argument string corresponding to the format of
        # the copied netCDF formatted file; proceed accordingly.
        ncfrmtout_dict = {'NETCDF4_CLASSIC': '4',
                          'NETCDF3_CLASSIC': '3',
                          'NETCDF3_64BIT_OFFSET': '2',
                          'NETCDF3_64BIT_DATA': '6'
                          }
        nccopy_app_str = parser_interface.dict_key_value(
            dict_in=ncfrmtout_dict, key=ncfrmtout, force=True,
            no_split=True)
        if nccopy_app_str is None:
            msg = ('The netCDF nccopy application output file formatted '
                   'type {0} is not supported. Aborting!!!'.format(ncfrmtout))
            raise NCError(msg=msg)

        # Create a direct copy of the netCDF formatted file provided
        # upon entry.
        msg = ('Creating a direct copy of netCDF-formatted file path {0} '
               'as {1} and format {2}.'.format(ncfilein, ncfileout,
                                               ncfrmtout.upper()))
        logger.info(msg=msg)
        cmd = ['{0}'.format(nccopy_app), '-{0}'.format(nccopy_app_str),
               '{0}'.format(ncfilein), '{0}'.format(ncfileout)]
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = proc.communicate()

    # Create a direct copy of the netCDF formatted file provided upon
    # entry using the Python netCDF4 library attributes.
    if not use_nccopy:

        # Initialize the source and destination netCDF-formatted
        # files.
        if ncfrmtin is None:
            ncfrmt = 'NETCDF4_CLASSIC'
        srcfile = netCDF4.Dataset(ncfilein, 'r', format=ncfrmtin)
        dstfile = netCDF4.Dataset(ncfileout, 'w', format=ncfrmtout)

        # Loop through each variable and dimension and define the
        # array dimensions for the destination netCDF-formatted file.
        for (name, dimension) in srcfile.dimensions.items():
            if ncunlimval is None:
                dimsize = (len(dimension) if not dimension.isunlimited()
                           else None)
            if ncunlimval is not None:
                dimsize = (len(dimension) if not dimension.isunlimited()
                           else ncunlimval)
            dstfile.createDimension(name, dimsize)

        # Determine the netCDF variables to be copied and proceed
        # accordingly.
        if ncvarlist is None:
            for (name, variable) in srcfile.variables.items():
                dstfile.createVariable(
                    name, variable.datatype, variable.dimensions)
                dstfile[name][:] = srcfile[name][:]
                dstfile[name].setncatts(srcfile[name].__dict__)
        if ncvarlist is not None:
            for (name, variable) in srcfile.variables.items():
                if name in ncvarlist:
                    dstfile.createVariable(
                        name, variable.datatype, variable.dimensions)
                    dstfile[name][:] = srcfile[name][:]
                    dstfile[name].setncatts(srcfile[name].__dict__)
        dstfile.setncatts(srcfile.__dict__)

        # Close the open netCDF-formatted files.
        dstfile.close()
        srcfile.close()

# ----


def nccopyvar(ncfilein, ncfileout, ncvarname, ncvar, ncout_mode,
              ncfrmtin=None, ncfrmtout=None):
    """
    Description
    -----------

    This function performs a direct copy of a user specified variable
    from a user specified input(e.g., source) file to a user
    specified output(destination) file.

    Parameters
    ----------

    ncfilein: str

        A Python string specifying the input(source) netCDF file.

    ncfileout: str

        A Python string specifying the output(destination) netCDF
        file.

    ncvarname: str

        A Python string specifying the netCDF variable to be copied.

    ncvar: array-type

        A Python array containing the values for the respective user
        specified netCDF variable.

    ncout_mode: str

        A Python string specifying the write-mode for the output
        netCDF file; this should typically be either 'w' for a new
        file write(this will clobber any previous existence of
        ncfileout) or 'a' to append to an existing file.

    Keywords
    --------

    ncfrmtin: str, optional

        A Python string specifying the format of the netCDF input
        file; available options are NETCDF4_CLASSIC, NETCDF3_CLASSIC,
        NETCDF3_64BIT_OFFSET, or NETCDF3_64BIT_DATA.

    ncfrmtout: str, optional

        A Python string specifying the format of the netCDF file to be
        written to; available options are NETCDF4_CLASSIC,
        NETCDF3_CLASSIC, NETCDF3_64BIT_OFFSET, or NETCDF3_64BIT_DATA.

    """

    # Initialize the source and destination netCDF-formatted file.
    if ncfrmtin is None:
        ncfrmtin = 'NETCDF4_CLASSIC'
    if ncfrmtout is None:
        ncfrmtout = 'NETCDF4_CLASSIC'
    srcfile = netCDF4.Dataset(filename=ncfilein, mode='r',
                              format=ncfrmtin)
    dstfile = netCDF4.Dataset(filename=ncfileout, mode=ncout_mode,
                              format=ncfrmtout)

    # Loop through each variable within the netCDF-formatted file and
    # copy the specified variables to the destination netCDF-formatted
    # file.
    for (name, variable) in srcfile.variables.items():
        if ncvarname == name:
            dstfile.createVariable(
                name, variable.datatype, variable.dimensions)
            dstfile[name].setncatts(srcfile[name].__dict__)
            dstfile[name][:] = ncvar

    # Close the open netCDF-formatted files.
    dstfile.close()
    srcfile.close()

# ----


def ncnumvar(ncfile, ncfrmt=None):
    """
    Description
    -----------

    This function parses a netCDF file to determine the total number
    of variable arrays within the respective file.

    Parameters
    ----------

    ncfile: str

        A Python string specifying the netCDF file to be read.

    Keywords
    --------

    ncfrmt: str, optional

        A Python string specifying the format of the netCDF file(to
        be created); available options are NETCDF4_CLASSIC,
        NETCDF3_CLASSIC, NETCDF3_64BIT_OFFSET, or NETCDF3_64BIT_DATA;
        if not specified, NETCDF4_CLASSIC is assumed.

    Returns
    -------

    numvar: int

        A Python integer specifying the total number of variable
        arrays within the respective input file.

    """

    # Open the netCDF-formatted file and proceed accordingly.
    if ncfrmt is None:
        ncfrmt = 'NETCDF4_CLASSIC'
    ncfile = netCDF4.Dataset(filename=ncfile, mode='r', format=ncfrmt)
    numvar = len(ncfile.variables)

    # Close the open netCDF-formatted file and return the netCDF
    # variable array.
    ncfile.close()

    return numvar

# ----


def ncreadattr(ncfile, ncattrname, ncvarname=None, ncfrmt=None):
    """
    Description
    -----------

    This function parses a netCDF file to collect the user specified
    netCDF attribute value(s).

    Parameters
    ----------

    ncfile: str

        A Python string specifying the netCDF file to be read.

    ncattrname: str

        A Python string specifying the netCDF attribute to collect and
        return.

    Keywords
    --------

    ncvarname: str, optional

       A Python string specifying the netCDF variable from which to
       retrieve the specified netCDF attribute; a value of NoneType
       implies a global attribute is to be retrieved.

    ncfrmt: str, optional

        A Python string specifying the format of the netCDF file(to
        be created); available options are NETCDF4_CLASSIC,
        NETCDF3_CLASSIC, NETCDF3_64BIT_OFFSET, or NETCDF3_64BIT_DATA;
        if not specified, NETCDF4_CLASSIC is assumed.

    Returns
    -------

    ncattr: str/float/int/tuple

        A Python type containing the value(s) for the user specified
        netCDF attribute.

    """

    # Open the netCDF-formatted file.
    if ncfrmt is None:
        ncfrmt = 'NETCDF4_CLASSIC'
    ncfile = netCDF4.Dataset(filename=ncfile, mode='r', format=ncfrmt)

    # Collect the netCDF attributes accordingly.
    if ncvarname is None:
        ncattr = parser_interface.object_getattr(
            object_in=ncfile, key=ncattrname, force=True)
    if ncvarname is not None:
        ncvar = ncfile.variables[ncvarname]
        ncattr = parser_interface.object_getattr(
            object_in=ncvar, key=ncattrname, force=True)

    # Close the open netCDF-formatted file and return the netCDF
    # attribute.
    ncfile.close()

    return ncattr

# ----


def ncreaddim(ncfile, ncdimname, ncfrmt=None):
    """
    Description
    -----------

    This function parses a netCDF file to collect and return the
    dimension size for the user specified dimension variable name.

    Parameters
    ----------

    ncfile: str

        A Python string specifying the netCDF file to be read.

    ncdimname: str

        A Python string specifying the netCDF dimension to be
        retrieved and returned.

    Keywords
    --------

    ncfrmt: str, optional

        A Python string specifying the format of the netCDF file(to
        be created); available options are NETCDF4_CLASSIC,
        NETCDF3_CLASSIC, NETCDF3_64BIT_OFFSET, or NETCDF3_64BIT_DATA;
        if not specified, NETCDF4_CLASSIC is assumed.

    Returns
    -------

    ncdim: int

        A Python integer specifying the value for the user specified
        dimension variable.

    """

    # Open the netCDF-formatted file.
    if ncfrmt is None:
        ncfrmt = 'NETCDF4_CLASSIC'
    ncfile = netCDF4.Dataset(filename=ncfile, mode='r', format=ncfrmt)

    # Collect the netCDF dimensions accordingly.
    try:
        ncdim = len(ncfile.dimensions[ncdimname])
    except KeyError:
        ncdim = None

    # Close the open netCDF-formatted file and return the netCDF
    # dimension.
    ncfile.close()

    return ncdim

# ----


def ncreadvar(ncfile, ncvarname, ncfrmt=None, from_ncgroup=False,
              ncgroupname=None, squeeze=False, axis=None, level=None):
    """
    Description
    -----------

    This function parses a netCDF file in order to collect and return
    the values for the user specified variable; this function also
    provides optional capabilities to apply the numpy squeeze
    application to truncate to the user specified dimensions.

    Parameters
    ----------

    ncfile: str

        A Python string specifying the netCDF file to be read.

    ncvarname: str

        A Python string specifying the netCDF variable to be retrieved
        and returned.

    Keywords
    --------

    ncfrmt: str, optional

        A Python string specifying the format of the netCDF file(to
        be created); available options are NETCDF4_CLASSIC,
        NETCDF3_CLASSIC, NETCDF3_64BIT_OFFSET, or NETCDF3_64BIT_DATA;
        if not specified, NETCDF4_CLASSIC is assumed.

    from_ncgroup: bool, optional

        A Python boolean variable specifying whether the respective
        netCDF variable is contained within a netCDF group/container;
        if True, the parameter ncgroupname must be specified (see
        below).

    ncgroupname: str, optional

        A Python string specifying the netCDF group/container name;
        used only if from_ncgroup is True upon entry.

    squeeze: bool, optional

        A Python boolean variable specifying whether to apply the
        numpy squeeze application to truncate the user specified
        variable dimension(axis; see below); if True, the variable
        axis(below) must be specified.

    axis: int, optional

        A Python integer value specifying the variable axis to be
        truncated via the numpy squeeze application.

    level: int, optional

        A Python integer value specifying the variable level to be
        collected and returned.

    Returns
    -------

    ncvar: array-type

        A Python array containing the values for the respective user
        specified netCDF variable.

    Raises
    ------

    NCError:

        * raised if the squeeze attribute is implement without
          specifying the variable axis along which to apply the
          squeeze function.

        * raised if the netCDF group/container name is not specified
          when from_ncgroup is True upon entry.

    """

    # Check the function parameters.
    if squeeze:
        if axis is None:
            msg = ('If implementing the squeeze attribute, the '
                   'axis about which to squeeze the ingested variable '
                   'must be specified. Aborting!!!')
            raise NCError(msg=msg)

    # Open the netCDF-formatted files.
    if ncfrmt is None:
        ncfrmt = 'NETCDF4_CLASSIC'
    ncfile = netCDF4.Dataset(filename=ncfile, mode='r', format=ncfrmt)

    # Check whether to read the netCDF variable from a group
    # container; proceed accordingly.
    if from_ncgroup:

        # Check the parameter values provided upon entry and proceed
        # accordingly.
        if ncgroupname is None:
            msg = ('The netCDF group name attribute ncgroupname cannot be '
                   'NoneType upon entry if attempting to read a netCDF '
                   'variable from a netCDF group container. Aborting!!!')
            raise NCError(msg=msg)

        # Define the netCDF groups contained within the
        # netCDF-formatted file provided upon entry.
        ncgroups = ncfile.groups[ncgroupname]

    # Collect the netCDF variable accordingly.
    if level is None:
        if from_ncgroup:
            ncvar = ncgroups.variables[ncvarname][...]
        if not from_ncgroup:
            ncvar = ncfile.variables[ncvarname][...]
    if level is not None:
        if from_ncgroup:
            ncvar = ncgroups.variables[ncvarname][:, level, :, :]
        if not from_ncgroup:
            ncvar = ncfile.variables[ncvarname][:, level, :, :]
    ncfile.close()

    # If specified, truncate the respective netCDF dimension.
    if squeeze:
        try:
            ncvar = numpy.squeeze(ncvar, axis=axis)
        except ValueError:
            ncvar = ncvar[0, ...]

    return ncvar

# ----


def ncvarexist(ncfilein, ncvarname, ncfrmtin=None):
    """
    Description
    -----------

    This function reads a netCDF file and queries the variable list
    for the existence of a user specified variable name (ncvarname);
    it returns a boolean values indicating whether the variable name
    has been found.

    Parameters
    ----------

    ncfile: str

        A Python string specifying the netCDF file to be read.

    ncvarname: str

        A Python string specifying the netCDF variable to be queried.

    Keywords
    --------

    ncfrmt: str, optional

        A Python string specifying the format of the netCDF file (to
        be created); available options are NETCDF4_CLASSIC,
        NETCDF3_CLASSIC, NETCDF3_64BIT_OFFSET, or NETCDF3_64BIT_DATA;
        if not specified, NETCDF4_CLASSIC is assumed.

    Returns
    -------

    ncvarexist: bool

        A Python boolean variable indicating whether the
        user-specified queried variable exists within the respective
        netCDF file.

    """

    # Open the netCDF-formatted file.
    if ncfrmtin is None:
        ncfrmt = 'NETCDF4_CLASSIC'
    ncfile = netCDF4.Dataset(filename=ncfilein, mode='r', format=ncfrmtin)

    # Check that the specified netCDF variable exists and proceed
    # accordingly.
    ncvarexist = False
    for (name, _) in ncfile.variables.items():
        if (ncvarname == name):
            ncvarexist = True
            break

    # Close the netCDF-formatted file and return a boolean value
    # regarding whether the parameter variable specified upon entry
    # exists.
    ncfile.close()

    return ncvarexist

# ----


def ncvarlist(ncfile, ncfrmt=None):
    """
    Description
    -----------

    This function reads and returns a list of variables within the
    netCDF file specified upon entry.

    Parameters
    ----------

    ncfile: str

        A Python string specifying the netCDF file to be read.

    Keywords
    --------

    ncfrmt: str, optional

        A Python string specifying the format of the netCDF file (to
        be created); available options are NETCDF4_CLASSIC,
        NETCDF3_CLASSIC, NETCDF3_64BIT_OFFSET, or NETCDF3_64BIT_DATA;
        if not specified, NETCDF4_CLASSIC is assumed.

    Returns
    -------

    varlist: list

        A Python list of variables within the netCDF file specified
        upon entry.

    """

    # Open the netCDF-formatted file.
    if ncfrmt is None:
        ncfrmt = 'NETCDF4_CLASSIC'
    ncfile = netCDF4.Dataset(filename=ncfile, mode='r', format=ncfrmt)
    varlist = list()
    for (name, variable) in ncfile.variables.items():
        varlist.append(name)

    return varlist

# ----


def ncwrite(ncfile, ncdim_obj, ncvar_obj, ncfrmt=None):
    """
    Description
    -----------

    This function writes a netCDF file, containing the dimensions,
    variables, and (optional) attributes, specified by the user.

    Parameters
    ----------

    ncfile: str

        A Python string specifying the netCDF file (to be created).

    ncdim_obj: obj

        A Python object containing the dimension variable attributes
        for the netCDF file (to be created).

    ncvar_obj: obj

        A Python object containing the variable attributes for the
        netCDF file (to be created).

    Keywords
    --------

    ncfrmt: str, optional

        A Python string specifying the format of the netCDF file (to
        be created); available options are NETCDF4_CLASSIC,
        NETCDF3_CLASSIC, NETCDF3_64BIT_OFFSET, or NETCDF3_64BIT_DATA;
        if not specified, NETCDF4_CLASSIC is assumed.

    """

    # Open the netCDF-formatted file.
    if ncfrmt is None:
        ncfrmt = 'NETCDF4_CLASSIC'
    ncfile = netCDF4.Dataset(filename=ncfile, mode='w', format=ncfrmt)

    # Define the netCDF attibutes and proceed accordingly.
    ncdim_dict = _read_ncdim_obj(ncdim_obj=ncdim_obj)
    ncvar_dict = _read_ncvar_obj(ncvar_obj=ncvar_obj)
    for key in ncdim_dict.keys():
        value = ncdim_dict[key]
        ncfile.createDimension(key, value)

    # Build the netCDF-formatted file and write each variable.
    for key in ncvar_dict.keys():
        try:
            var_dict = ncvar_dict[key]
            if var_dict['type'].lower() == 'char':
                datatype = str
            else:
                datatype = parser_interface.object_getattr(
                    object_in=numpy, key=var_dict['type'])
            var = ncfile.createVariable(
                varname=var_dict['varname'], datatype=datatype, dimensions=var_dict['dims'])
            if 'attrs' in var_dict.keys():
                attr_dict = parser_interface.dict_key_value(
                    dict_in=var_dict, key='attrs')
                for attr in attr_dict.keys():
                    value = parser_interface.dict_key_value(
                        dict_in=attr_dict, key=attr, no_split=True)
                    var = parser_interface.object_setattr(
                        object_in=var, key=attr, value=value)
            vallist = numpy.reshape(list(map(datatype, var_dict['values'])),
                                    var.shape)
            var[:] = numpy.array(vallist, dtype=datatype)
        except TypeError:
            pass

    # Close the open netCDF-formatted file.
    ncfile.close()


# ----

def ncwritevar(ncfile, ncvarname, ncvar, ncfrmt=None):
    """
    Description
    -----------

    This function opens a netCDF file and writes the array (ncvar)
    values for the user specified variable to the respective (open)
    netCDF file.

    Parameters
    ----------

    ncfile: str

        A Python string specifying the netCDF file to be written to.

    ncvarname: str

        A Python string specifying the netCDF variable to be
        written/updated.

    ncvar: array-type

         A Python array containing the values for the respective user
         specified netCDF variable.

    Keywords
    --------

    ncfrmt: str, optional

        A Python string specifying the format of the netCDF file (to
        be created); available options are NETCDF4_CLASSIC,
        NETCDF3_CLASSIC, NETCDF3_64BIT_OFFSET, or NETCDF3_64BIT_DATA;
        if not specified, NETCDF4_CLASSIC is assumed.

    """

    # Open the netCDF-formatted file.
    if ncfrmt is None:
        ncfrmt = 'NETCDF4_CLASSIC'
    ncfile = netCDF4.Dataset(filename=ncfile, mode='a', format=ncfrmt)

    # Write the specified variable to the specified netCDF-formatted
    # file.
    for (name, _) in ncfile.variables.items():
        if ncvarname == name:
            ncfile.variables[ncvarname][:] = ncvar
