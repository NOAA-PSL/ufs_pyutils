# =========================================================================

# Module: tools/fileio_interface.py

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

    fileio_interface.py

Description
-----------

    This module contains functions required to perform various file
    and directory tasks.

Functions
---------

    concatenate(filelist, concatfile, sepfiles=False)

        This function concatenates a list of user-specified files
        (filelist) into a single user-specified file (concatfile); the
        respective files are opened in binary mode to increase the
        applicability of the function.

    copyfile(srcfile, dstfile)

        This function will create a local copy of a user specified
        source file to user specified destination file location; if
        the destination file already exists, it will be removed prior
        to the creation of the destination file.

    dircontents(path)

        This function compiles a content list of the user specified
        directory.

    dirpath_tree(path)

        This function checks whether the directory tree (i.e., path)
        exists; if not an attempt will be made to build it.

    fileexist(path)

        This function will ingest a file-path and check whether the
        respective file-path exists; this function is a wrapper around
        os.path.isfile.

    filepermission(path, permission)

        This function defines the permissions for a specified
        file-path.

    filesize(path)

        This function ingests a file-path and obtains the size of the
        file, in bytes; the respective 'typical' file size
        descriptions, namely mega-bytes (MB), giga-bytes (GB), and
        tera-bytes (TB), are computed and returned.

    makedirs(path, force=False)

        This function is a wrapper around os.makedirs and will build
        the directory tree (if needed) and the directory
        leaves/sub-directories.

    removefiles(filelist)

        This function ingests a list of filenames. The function then
        checks whether the respective filename exists and if so it
        removes it.

    rename(srcfile, dstfile)

        This function will rename a file in accordance with the user
        specifications; this function may also be used to move and
        rename files between different file paths.

    rmdir(path)

        This function will attempt to remove the user specified
        path. the path does not exist, this function does nothing.

    symlink(srcfile, dstfile)

        This function will create a symbolic link from a user
        specified source file to a user specified destination file; if
        the destination file already exists, it will be removed prior
        to the creation of the symbolic link.

    touch(path)

        This function emulates the POSIX UNIX touch application.

    virtual_file(delete=True)

        This function opens (i.e., creates) a temporary (e.g.,
        virtual) file beneath /tmp to be utilized by the respective
        calling application; the open virtual file path may be closed
        in the calling script using os.unlink().

Requirements
------------

- pyyaml; https://pyyaml.org/

Author(s)
---------

    Henry R. Winterbottom; 03 December 2022

History
-------

    2022-12-03: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=consider-using-f-string
# pylint: disable=consider-using-with
# pylint: disable=broad-except
# pylint: disable=too-many-ancestors
# pylint: disable=unspecified-encoding

# ----

import os
import shutil
import subprocess
import tempfile
from typing import List, Tuple

import numpy
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = [
    "concatenate",
    "copyfile",
    "dircontents",
    "dirpath_tree",
    "fileexist",
    "filepermission",
    "filesize",
    "makedirs",
    "removefiles",
    "rename",
    "rmdir",
    "symlink",
    "touch",
    "virtual_file",
]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


def concatenate(filelist: List, concatfile: str, sepfiles: bool = False) -> None:
    """
    Description
    -----------

    This function concatenates a list of user-specified files
    (filelist) into a single user-specified file (concatfile); the
    respective files are opened in binary mode to increase the
    applicability of the function.

    Parameters
    ----------

    filelist: list

        A Python list of file paths to compose the concatenated file
        path.

    concatfile: str

        A Python string specifying the path of the concatenated file
        created from the input file list.

    Keywords
    --------

    sepfiles: bool, optional

        A Python boolean valued variable specifying whether to include
        a blank line seperator between the contents of the respective
        files to be concatenated.

    """

    # Concatenate files contained within the specified list of files
    # upon entry.
    with open(concatfile, "wb") as fout:
        for filename in filelist:
            with open(filename, "rb") as fin:
                data = fin.read()
            fout.write(data)
            if sepfiles:
                fout.write(b"\n")


# ----


def copyfile(srcfile: str, dstfile: str) -> None:
    """
    Description
    -----------

    This function will create a local copy of a user specified source
    file to user specified destination file location; if the
    destination file already exists, it will be removed prior to the
    creation of the destination file.

    Parameters
    ----------

    srcfile: str

        A Python string defining the path to the source file to be
        copied.

    dstfile: str

        A Python string defining the path to the destination file from
        which the source file is copied.

    """

    # Check whether the specified destination is a filename or
    # directory path; proceed accordingly.
    if os.path.isfile(dstfile):
        os.remove(dstfile)

    if os.path.isdir(dstfile):
        path = dstfile
        rmdir(path)

    # Copy the specified source file to the corresponding destination
    # file using the respective platform copy method.
    msg = f"Copying file {srcfile} to {dstfile}."
    logger.info(msg=msg)

    cmd = ["cp", "-rRfL", srcfile, dstfile]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    proc.communicate()


# ----


def dircontents(path: str) -> List:
    """
    Description
    -----------

    This function compiles a content list of the user specified
    directory.

    Parameters
    ----------

    path: str

        A Python string defining the path to the directory to be
        parsed.

    Returns
    -------

    contents: list

        A Python list containing the directory contents.

    """

    # Collect the specified directory path list of contents.
    contents = os.listdir(path)

    return contents


# ----


def dirpath_tree(path: str) -> None:
    """
    Description
    -----------

    This function checks whether the directory tree (i.e., path) exists;
    if not an attempt will be made to build it.

    Parameters
    ----------

    path: str

        A Python string specifying the directory tree path to be
        created if it does not (yet) exist.

    """

    # Check whether the directory tree exists; proceed accordingly.
    exist = fileexist(path=path)
    if exist:
        msg = f"The directory tree {path} exists; nothing to be done."
        logger.info(msg=msg)

    if not exist:
        msg = (
            f"The directory tree {path} does not exist; an attempt "
            "will be made to create it."
        )
        logger.warn(msg=msg)

        makedirs(path=path)


# ----


def fileexist(path: str) -> bool:
    """
    Description
    -----------

    This function ingests a file-path and checks whether the
    respective file-path exists; this function is a wrapper around
    os.path.isfile.

    Parameters
    ----------

    path: str

        A Python string defining the path to a respective file.

    Returns
    -------

    exist: bool

        A Python boolean variable specifying whether the respective
        file-path (path) exists.

    """

    # Define a boolean valued variable specifying whether the
    # specified file path exists upon entry.
    exist = os.path.exists(path)

    return exist


# ----


def filepermission(path: str, permission: int) -> None:
    """
    Description
    -----------

    This function defines the permissions for a specified file-path.

    Parameters
    ----------

    path: str

        A Python string defining the path to a respective file.

    permission: int

        A Python integer specifying the UNIX file permissions.

    """

    # Define the permissions for the specified file path.
    os.chmod(path, permission)


# ----


def filesize(path: str) -> Tuple:
    """
    Description
    -----------

    This function ingests a file-path and obtains the size of the
    file, in bytes; the respective 'typical' file size descriptions,
    namely mega-bytes (MB), giga-bytes (GB), and tera-bytes (TB), are
    computed and returned.

    Parameters
    ----------

    path: str

        A Python string defining the path to a respective file.

    Returns
    -------

    bytes_path: int

        A Python integer specifying the file size in bytes.

    megabytes_path: int

        A Python integer specifying the file size in mega-bytes (MB).

    gigabytes_path: int

        A Python integer specifying the file size in giga-bytes (GB).

    terabytes_path: int

        A Python integer specifying the file size in tera-bytes (TB).

    """

    # Define and/or compute the specified file path sizes.
    bytes_path = os.path.getsize(path)
    megabytes_path = numpy.int(bytes_path / 1.0e6)
    gigabytes_path = numpy.int(bytes_path / 1.0e9)
    terabytes_path = numpy.int(bytes_path / 1.0e12)
    bytes_path = numpy.int(bytes_path)

    return (bytes_path, megabytes_path, gigabytes_path, terabytes_path)


# ----


def makedirs(path: str, force: bool = False) -> None:
    """
    Description
    -----------

    This function is a wrapper around os.makedirs and will build the
    directory tree (if needed) and the directory
    leaves/sub-directories.

    Parameters
    ----------

    path: str

        A Python string defining the path to the directory to be
        constructed.

    Keywords
    --------

    force: bool, optional

        A Python boolean variable indicating whether any previous
        directories should be forcibly removed prior to constucting
        the directory tree; default is False.

    """

    # Build the directory path specified upon entry.
    if os.path.isdir(path):
        if force:
            rmdir(path)

    try:
        os.makedirs(path)

    except OSError:
        pass


# ----


def removefiles(filelist: List) -> None:
    """
    Description
    -----------

    This function ingests a list of filenames; the function then
    checks whether the respective filename exists and if so it removes
    it.

    Parameters
    ----------

    filelist: list

        A Python list containing a list of files to be removed.

    """

    # Remove the list of files provided upon entry.
    for filename in filelist:
        if os.path.isfile(filename):
            os.remove(filename)


# ----


def rename(srcfile: str, dstfile: str) -> None:
    """
    Description
    -----------

    This function will rename a file in accordance with the user
    specifications; this function may also be used to move and rename
    files between different file paths.

    Parameters
    ----------

    srcfile: str

        A Python string defining the path to the source file to be
        renamed/moved.

    dstfile: str

        A Python string defining the path to the destination file from
        which the source file is to be renamed/moved.

    """

    # Rename (i.e., move) the source file path specified upon entry to
    # the destination file path specified upon entry.
    try:
        shutil.move(srcfile, dstfile)

    except Exception:
        pass


# ----


def rmdir(path: str) -> None:
    """
    Description
    -----------

    This function will attempt to remove the user specified path. the
    path does not exist, this function does nothing.

    Parameters
    ----------

    path: str

        A Python string containing the path to the directory to be
        removed.

    """

    # Check whether the specified path is an existing directory tree
    # upon entry; proceed accordingly.
    if os.path.isdir(path):
        shutil.rmtree(path)

    if not os.path.isdir(path):
        pass


# ----


def symlink(srcfile: str, dstfile: str) -> None:
    """
    Description
    -----------

    This function will create a symbolic link from a user specified
    source file to a user specified destination file; if the
    destination file already exists, it will be removed prior to the
    creation of the symbolic link.

    Parameters
    ----------

    srcfile: str

        A Python string defining the path to the source file to be
        symbolically linked.

    dstfile: str

        A Python string defining the path to the destination file from
        which the source file is to be symbolically linked.

    """

    # Check whether the destination symbolic link exists upon entry;
    # proceed accordingly.
    if os.path.isfile(dstfile):
        os.remove(dstfile)

    try:
        os.symlink(srcfile, dstfile)

    except OSError:
        pass


# ----


def touch(path: str):
    """
    Description
    -----------

    This function emulates the POSIX UNIX touch application.

    Parameters
    ----------

    path: str

        A Python string specifying the file path for which to apply
        the UNIX touch application.

    """

    # Open and append to the file path specified upon entry.
    with open(path, "a"):
        os.utime(path, None)


# ----


def virtual_file(delete: bool = True) -> object:
    """
    Description
    -----------

    This function opens (i.e., creates) a temporary (e.g., virtual)
    file beneath /tmp to be utilized by the respective calling
    application; the open virtual file path may be closed in the
    calling script using os.unlink().

    Keywords
    --------

    delete: bool, optional

        A Python boolean valued variable specifying whether to
        maintain the respective virtual file path beneath /tmp; if
        False the downstream application should call
        close_virtual_file (see above) following the respective
        application.

    Returns
    -------

    file_obj: object

        A Python object containing the virtual file path attributes.

    """

    # Open the virtual file path.
    file_obj = tempfile.NamedTemporaryFile(delete=delete)

    return file_obj
