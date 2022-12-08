# =========================================================================

# Module: ioapps/tarfile_interface.py

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

    tarfile_interface.py

Description
-----------

    This module contains functions to create and read local host
    tarball files.

Classes
-------

    TarFileError(msg)

        This is the base-class for all exceptions; it is a sub-class
        of Error

Functions
---------

    read_tarfile(path, tarball_path, mode=None, filelist=None):

        This function parses a specified tarball archive and extracts
        the specified files; if filelist is NoneType on entry, all
        files within the archive will be extracted.

    write_tarfile(path, tarball_path, filelist=None, filedict=None,
                 ref_local=False, gzip=False, compress_level=1)

        This function creates a POSIX compliant tarball file and
        appends the files within the user-specified filelist to the
        respective tarball file.

Author(s)
--------- 

    Henry R. Winterbottom; 25 September 2022

History
-------

    2022-09-25: Henry Winterbottom -- Initial implementation.

"""

# ----

import os
import tarfile

from tools import parser_interface
from utils.error_interface import Error
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["read_tarfile", "write_tarfile"]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class TarFileError(Error):
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

        Creates a new TarFileError object.

        """
        super(TarFileError, self).__init__(msg=msg)


# ----


def read_tarfile(path, tarball_path, mode=None, filelist=None) -> None:
    """
    Description
    -----------

    This function parses a specified tarball archive and extracts the
    specified files; if filelist is NoneType upon entry, all files
    within the archive will be extracted.

    Parameters
    ----------

    path: str

        A Python string specifying the path beneath which the contents
        of the tarball are to be extracted to.

    tarball_path: str

        A Python string specifying the path to the tarball to be read.

    Keywords
    --------

    mode: str, optional

        A Python string specifying the mode to be used to open the
        tarball archive; a complete list of combinations can be found
        at https://docs.python.org/3/library/tarfile.html#tarfile.open.

    filelist: list, optional

        A Python list of member files within the tarball archive to be
        extracted.

    Raises
    ------

    TarballError:

        * raised if an exception is encountered while extracting files
          from the tarball file path specified upon entry.

        * raised if an execption is encountered while extracting a
          specified file from the tarball file path specified upon
          entry.

    """

    # Move to the working directory within which to extract the files
    # within the tarball archive.
    msg = "The contents of tarball path {0} will be extracted to " "path {1}.".format(
        tarball_path, path
    )
    logger.warn(msg=msg)
    os.chdir(path)

    # Open the existing tarball.
    msg = "Opening tarball file {0}.".format(tarball_path)
    logger.info(msg=msg)
    if mode is None:
        mode = "r"

    tarball = tarfile.open(tarball_path, mode)

    # If filelist is NoneType upon entry, extract the entire archive;
    # proceed accordingly.
    if filelist is None:

        # Extract all files in the tarball; proceed accordingly.
        try:
            msg = "Extracting all files from tarball path {0}.".format(tarball_path)
            logger.info(msg=msg)
            tarball.extractall()

        except Exception as error:
            msg = (
                "The extraction of all files from tarball path {0} "
                "failed with error {1}. Aborting!!!".format(tarball_path, error)
            )
            raise TarFileError(msg=msg)

    # Extract only the files specified within the filelist attribute
    # upon entry; proceed accordingly.
    if filelist is not None:
        for filename in filelist:
            try:
                msg = "Determining tarball object path for file {0}.".format(filename)
                logger.info(msg=msg)
                tarball_obj = tarball.getmember(filename)
                msg = "Extracting file {0} from tarball path {1}.".format(
                    filename, tarball_path
                )
                logger.info(msg=msg)
                tarball.extract(tarball_obj)

            except Exception as error:
                msg = (
                    "The extraction of file {0} from tarball path {1} "
                    "failed with error {2}. Aborting!!!".format(
                        filename, tarball_path, error
                    )
                )
                raise TarFileError(msg=msg)

    # Close the open tarball archive.
    tarball.close()


# ----


def write_tarfile(
    path,
    tarball_path,
    filelist=None,
    filedict=None,
    ref_local=False,
    gzip=False,
    compresslevel=1,
) -> None:
    """
    Description
    -----------

    This function creates a POSIX compliant tarball file and appends
    the files within the user-specified filelist to the respective
    tarball file.

    Parameters
    ----------

    path: str

        A Python string specifying the path beneath which the files to
        be archived (see filelist) exist on the local host.

    tarball_path: str

        A Python string specifying the path to the tarball, containing
        the contents of path, to be written.

    Keywords
    --------

    filelist: list, optional

        A Python list of filename and/or paths beneath the path to be
        archived (see path, above); if provided, only the files
        contained within the list will be writen to tarball archive.

    filedict: dict, optional

        A Python dictionary containing the key and value pairs to be
        used to construct the tarball file; the key values are the
        local filename path and the corresponding values are the
        tarball file member file paths.

    ref_local: bool, optional

        A Python boolean variable specifying whether to define the
        archive path, within the user-specified tarball, relative to
        the working directory (path).

    gzip: bool, optional

        A Python boolean variable specifying whether to apply gzip
        compression to the tarball.

    compresslevel: int, optional

        A Python integer value specifying the compression level for
        the archive; the default is minimal compression.

    Raises
    ------

    TarFileError:

        * raised if an exception is encountered while validating the
          parameter values provided upon entry.

    """

    # Check that the attributes provided upon entry are valid.
    if (filelist is None) and (filedict is None):
        msg = (
            "Neither the filelist or filedict keyword parameters have "
            "been specified upon entry; this may cause this method "
            "to (not) produce the expected results."
        )
        logger.warn(msg=msg)

    if (filelist is not None) and (filedict is not None):
        msg = (
            "The write_tarfile method does not support file name "
            "lists (filelist) and file and archive file mapping "
            "names (filedict) simultaneously. Aborting!!!"
        )
        raise TarFileError(msg=msg)

    # Define the tarball archive attributes accordingly.
    if gzip:
        mode = "w:gz"
        kwargs = {"compresslevel": compresslevel}

    else:
        mode = "w"
        kwargs = dict()

    # Open the tarball archive and proceed accordingly.
    os.chdir(path)
    tarball = tarfile.open(tarball_path, mode, **kwargs)

    # Check the status of the attributes provided upon entry and
    # proceed accordingly.
    if filelist is not None:

        # Write the respective file names to the tarball archive path;
        # proceed accordingly.
        for filename in filelist:
            msg = "Adding file {0} to tarball file {1}.".format(filename, tarball_path)
            logger.info(msg=msg)

            # Define the tarball archive member file name attributes;
            # proceed accordingly.
            if ref_local:
                tarball.add("./{0}".format(filename))
            if not ref_local:
                tarball.add(filename)

    # Check the status of the attributes provided upon entry and
    # proceed accordingly.
    if filedict is not None:

        # Write the respective file names to the tarball archive path;
        # proceed accordingly.
        for filename in filedict.keys():

            # Define the tarball archive member file name.
            arcname = parser_interface.dict_key_value(
                dict_in=filedict, key=filename, no_split=True
            )
            msg = "Adding file {0} to tarball file {1} as {2}.".format(
                filename, tarball_path, arcname
            )
            logger.info(msg=msg)

            # Define the tarball archive member file name attributes;
            # proceed accordingly.
            if ref_local:
                kwargs = {"arcname": "./%s" % arcname}
            if not ref_local:
                kwargs = {"arcname": arcname}

            tarball.add(filename, **kwargs)

    # Close the open tarball archive.
    tarball.close()
