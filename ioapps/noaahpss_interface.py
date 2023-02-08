# =========================================================================

# Module: ioapps/noaahpss_interface.py

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

    noaahpss_interface.py

Description
-----------

    This module contains functions and classes to interface with the
    National Oceanographic and Atmospheric Administration (NOAA)
    High-Performance Storage System (HPSS).

Functions
---------

    _check_hpss_env()

        This function checks whether the HPSS environment has been
        loaded; if not, a NOAAHPSSInterfaceError will be thrown; if so, the
        paths to the htar and hsi executables will be defined
        respectively as the base-class attributes htar and hsi.

    check_filepath(tarball_path, filename, include_slash=True)

        This function extracts the contents of a user specified
        tarball into memory and checks whether the respective
        user-specified filename exists within the archive; a boolean
        value is returned specifying the result of the search.

    get_hpssfile(hpss_filepath)

        This function attempts to collect a user specified NOAA HPSS
        filepath and place it within the directory path from which
        this function is called.

    path_build(path)

        This function attempts to build a path on the NOAA HPSS; if a
        path cannot be created, this function throws a NOAAHPSSInterfaceError.

    path_exist(path)

        This function checks that the top-level NOAA HPSS path to
        which an archive to be written exists.

    path_filelist(path)

        This function queries a user specified NOAA HPSS path and
        returns the contents; this includes all returns from the
        directory contents query commands; downstream applications
        should understand how to parse (i.e., search) the returned
        list.

    put_hpssfile(filepath, hpss_filepath)

        This function attempts to archive a local file to a user
        specified NOAA HPSS filepath.

    read_tarball(path, tarball_path, filename, force=False,
                 strip_dir=False, include_slash=True)

        This function attempts to read a tarball and extract the
        user-specified file from the respective tarball and write it
        to the user-specified path.

    write_tarball(path, tarball_path, tarball_idx_path, filelist=None)

        This function will attempt to write a tarball and
        corresponding tarball index file to the NOAA HPSS; if one
        cannot be written, this function will thrown a NOAAHPSSInterfaceError;
        a returncode of 70, meaning the HPSS tarball file path is too
        long, is ignored as it is erroneous.

Author(s)
---------

    Henry R. Winterbottom; 03 December 2022

History
-------

    2022-12-03: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=broad-except
# pylint: disable=consider-using-with
# pylint: disable=raise-missing-from
# pylint: disable=simplifiable-if-statement
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals

# ----

import os
import subprocess
from typing import List, Tuple

import numpy
from tools import fileio_interface, system_interface
from utils.exceptions_interface import NOAAHPSSInterfaceError
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = [
    "check_filepath",
    "get_hpssfile",
    "path_build",
    "path_exist",
    "path_filelist",
    "put_hpssfile",
    "read_tarball",
    "write_tarball",
]

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

logger = Logger()

# ----


def _check_hpss_env() -> Tuple:
    """
    Description
    -----------

    This function checks whether the HPSS environment has been loaded;
    if not, a NOAAHPSSInterfaceError will be thrown; if so, the paths
    to the htar and hsi executables will be defined respectively as
    the base-class attributes htar and hsi.

    Returns
    -------

    hsi: str

        A Python string specifying the path to the hsi executable.

    htar: str

        A Python string specifying the path to the htar executable.

    Raises
    ------

    NOAAHPSSInterfaceError:

        * raised if the htar executable path cannot be determined.

        * raised if the hsi executable path cannot be determined.

    """

    # Check the run-time environment in order to determine the htar
    # executable path; proceed accordingly.
    htar = system_interface.get_app_path(app="htar")

    if htar is None:
        msg = "The htar executable could not be determined for your system. Aborting!!!"
        raise NOAAHPSSInterfaceError(msg=msg)

    # Check the run-time environment in order to determine the hsi
    # executable path.
    hsi = system_interface.get_app_path(app="hsi")

    if hsi is None:
        msg = "The hsi executable could not be determined for your system. Aborting!!!"
        raise NOAAHPSSInterfaceError(msg=msg)

    return (hsi, htar)


# ----


def check_filepath(
    tarball_path: str, filename: str, include_slash: bool = True
) -> bool:
    """
    Description
    -----------

    This function extracts the contents of a user specified tarball
    into memory and checks whether the respective user-specified
    filename exists within the archive; a boolean value is returned
    specifying the result of the search.

    Parameters
    ----------

    tarball_path: str

        A Python string specifying the path to the tarball on the NOAA
        HPSS to be evaluated/searched.

    filename: str

        A Python string specifying the filename to be queried within
        the tarball (tarball_path) archive.

    Keywords
    --------

    include_slash: bool, optional

        A Python boolean variable, that if True, will append a './' to
        the filename string within the tarball file to be collected;
        if False, the filename string is not modified.

    Returns
    -------

    exist: bool

        A Python boolean variable specifying the result of the
        filename search within the respective tarball archive.

    """

    # Build the htar command line string and proceed accordingly.
    (_, htar) = _check_hpss_env()
    cmd = [f"{htar}", "-tvf", f"{tarball_path}"]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, _) = proc.communicate()
    out = list(out.rstrip().decode("utf-8").rsplit())

    if include_slash:
        if f"./{filename}" in out:
            exist = True
        else:
            exist = False

    if not include_slash:
        if f"{filename}" in out:
            exist = True
        else:
            exist = False

    return exist


# ----


def get_hpssfile(hpss_filepath: str) -> None:
    """
    Description
    -----------

    This function attempts to collect a user specified NOAA HPSS
    filepath and place it within the directory path from which this
    function is called.

    Parameters
    ----------

    hpss_filepath: str

        A Python string specifying the path to the NOAA HPSS file to
        be collected.

    Raises
    ------

    NOAAHPSSInterfaceError:

        * raised if an exception is encountered during the HPSS file
          collection.

    """

    # Build the hsi command line string and proceed accordingly.
    (hsi, _) = _check_hpss_env()
    cmd = [f"{hsi}".format(hsi), "get", f"{hpss_filepath}"]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        proc.communicate()

    except Exception as errmsg:
        msg = (
            f"Collecting file {hpss_filepath} from the NOAA HPSS failed with "
            f"error {errmsg}. Aborting!!!"
        )
        raise NOAAHPSSInterfaceError(msg=msg)


# ----


def path_build(path: str) -> None:
    """
    Description
    -----------

    This function attempts to build a path on the NOAA HPSS; if a path
    cannot be created, this function throws a NOAAHPSSInterfaceError.

    Parameters
    ----------

    path: str

        A Python string specifying the NOAA HPSS path to create.

    Raises
    ------

    NOAAHPSSInterfaceError:

        * raised if the specified HPSS path cannot be created.

    """

    # Build the hsi command line string and proceed accordingly.
    (hsi, _) = _check_hpss_env()
    cmd = [f"{hsi}", "mkdir", "-p", f"{path}"]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.wait()

    if proc.returncode != 0:
        msg = f"The NOAA HPSS path {path} could not be created. Aborting!!!"
        raise NOAAHPSSInterfaceError(msg=msg)


# ----


def path_exist(path: str) -> bool:
    """
    Description
    -----------

    This function checks that the top-level NOAA HPSS path to which an
    archive to be written exists.

    Parameters
    ----------

    path: str

        A Python string specifying the top-level NOAA HPSS path to
        which an archive is to be written exists.

    Returns
    -------

    exist: bool

        A Python boolean value indicating whether the top-level NOAA
        HPSS path exists.

    """

    # Build the hsi command line string and proceed accordingly.
    (hsi, _) = _check_hpss_env()
    cmd = [f"{hsi}", "ls", f"{path}"]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.wait()
    if proc.returncode != 0:
        exist = False

    else:
        exist = True

    return exist


# ----


def path_filelist(path: str) -> List:
    """
    Description
    -----------

    This function queries a user specified NOAA HPSS path and returns
    the contents; this includes all returns from the directory
    contents query commands; downstream applications should understand
    how to parse (i.e., search) the returned list.

    Parameters
    ----------

    path: str

        A Python string specifying the path to where the
        user-specified filename is to be extract to.

    Returns
    -------

    filelist: list

        A Python list of all items returned by the directory contents.
        query.

    Raises
    ------

    NOAAHPSSInterfaceError:

        * raised if the NOAA HPSS path does not exist.

    """

    # Build the hsi command line string and proceed accordingly.
    (hsi, _) = _check_hpss_env()
    exist = path_exist(path=path)

    if not exist:
        msg = "The NOAA HPSS path does not exist. Aborting!!!"
        raise NOAAHPSSInterfaceError(msg=msg)

    cmd = [f"{hsi}", "-q", "ls", "-l", f"{path}"]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (_, hpss_list) = list(proc.communicate())

    filelist = []
    for item in hpss_list.split():
        filelist.append(item.decode("utf-8"))

    return filelist


# ----


def put_hpssfile(filepath: str, hpss_filepath: str) -> None:
    """
    Description
    -----------

    This function attempts to archive a local file to a user specified
    NOAA HPSS filepath.

    Parameters
    ----------

    filepath: str

        A Python string specifying the local file to be archived to
        the user specified NOAA HPSS filepath.

    hpss_filepath: str

        A Python string specifying the path to the NOAA HPSS file to
        be created.

    Raises
    ------

    NOAAHPSSInterfaceError:

        * raised if an exception is encountered while archiving the
          respective file path to the NOAA HPSS.

    """

    # Build the hsi command line string and proceed accordingly.
    (hsi, _) = _check_hpss_env()
    cmd = [f"{hsi}", "put", "-P", f"{filepath} : {hpss_filepath}"]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        proc.communicate()

    except Exception as errmsg:
        msg = (
            f"The archiving of file {filepath} to the NOAA HPSS failed with "
            f"error {errmsg}. Aborting!!!"
        )
        raise NOAAHPSSInterfaceError(msg=msg)


# ----


def read_tarball(
    path: str,
    tarball_path: str,
    filename: str,
    force: bool = False,
    strip_dir: bool = False,
    include_slash: bool = True,
) -> None:
    """
    Description
    -----------

    This function attempts to read a tarball and extract the
    user-specified file from the respective tarball and write it to
    the user-specified path.

    Parameters
    ----------

    path: str

        A Python string specifying the path to where the
        user-specified filename is to be extract to.

    tarball_path: str

        A Python string specifying the path to the tarball on the NOAA
        HPSS.

    filename: str

        A Python string specifying the filename to be extracted from
        within the tarball (tarball_path, above) archive.

    Keywords
    --------

    force: bool, optional

        A Python boolean variable; if False and the user-specified
        filename is not found in the tarball (tarball_path), a
        NOAAHPSSInterfaceError will be thrown; if True, this function
        carries on gracefully.

    strip_dir: bool, optional

        A Python boolean variable, that if True, will remove the
        parent directory tree (if any) from the basename file
        specified by the user.

    include_slash: bool, optional

        A Python boolean variable, that if True, will append a './' to
        the filename string within the tarball file to be collected;
        if False, the filename string is not modified.

    """

    # Build the htar command line string and proceed accordingly.
    cwd = os.getcwd()
    (_, htar) = _check_hpss_env()
    os.chdir(path)

    if include_slash:
        cmd = [f"{htar}" "-xvf", f"{tarball_path}", f"./{filename}"]

    if not include_slash:
        cmd = [
            f"{htar}",
            "-xvf",
            f"{tarball_path}",
            f"{filename}",
        ]

    proc = subprocess.Popen(cmd)
    proc.wait()

    if not force:
        if proc.returncode != 0:
            msg = (
                f"The HPSS file {filename} collection from tarball "
                f"{tarball_path} failed with returncode {proc.returncode}."
            )
            logger.warn(msg=msg)

    # Build the local filename path accordingly.
    if strip_dir:
        basename = os.path.basename(filename)
        dirname = os.path.dirname(filename)
        if dirname != "":
            srcfile = os.path.join(dirname, basename)
            dstfile = os.path.join(path, basename)
            try:
                fileio_interface.copyfile(srcfile=srcfile, dstfile=dstfile)
                for dirpath in filter(os.path.isdir, os.listdir(path)):
                    fileio_interface.rmdir(path=os.path.join(path, dirpath))

            except Exception:
                pass

    os.chdir(cwd)


# ----


def write_tarball(
    path: str, tarball_path: str, tarball_idx_path: str, filelist: List = None
) -> None:
    """
    Description
    -----------

    This function will attempt to write a tarball and corresponding
    tarball index file to the NOAA HPSS; if one cannot be written,
    this function will thrown a NOAAHPSSInterfaceError; a returncode
    of 70, meaning the HPSS tarball file path is too long, is ignored
    as it is erroneous.

    Parameters
    ----------

    path: str

        A Python string specifying the path to be archived within a
        tarball (tarball_path) specified by the user.

    tarball_path: str

        A Python string specifying the path to the tarball, containing
        the contents of path, to be written.

    tarball_idx_path: str

        A Python string specifying the path to the tarball index file,
        containing the contents of path, to be written.

    Keywords
    --------

    filelist: list, optional

        A Python list containing specific files within the path to be
        archived within a tarball (tarball_path) specified by the
        user.

    Raises
    ------

    NOAAHPSSInterfaceError:

        * raised if the return code from the NOAA HPSS is neither 0 or
          70; this indicates that the file was most likely not created
          on the NOAA HPSS tape archive.

    """

    # Build the htar command line string and proceed accordingly.
    htar_max_gigabyte = numpy.int(68.0)
    (_, htar) = _check_hpss_env()
    os.chdir(path)
    if filelist is None:
        cmd = [
            f"{htar}",
            "-cvf",
            f"{tarball_path}",
            "-I",
            f"{tarball_idx_path}",
            "./",
        ]

    if filelist is not None:
        cmd = [
            f"{htar}",
            "-cvf",
            f"{tarball_path}",
            "-I",
            f"{tarball_idx_path}",
        ]

        for item in filelist:
            filename = os.path.join(path, item)

            # Check the size of the tarball member file and proceed
            # accordingly.
            (_, _, gigabytes_path, _) = fileio_interface.filesize(path=filename)

            if gigabytes_path >= htar_max_gigabyte:
                msg = (
                    f"File {filename} has file size {gigabytes_path} TB which exceeds "
                    f"the htar maximum file size {htar_max_gigabyte} TB and will not "
                    "be archived."
                )
                logger.warn(msg=msg)

            if gigabytes_path < htar_max_gigabyte:
                msg = f"File {filename} has size {gigabytes_path} TB and will be archived."
                logger.info(msg=msg)
                cmd.append(item)

    # Push the member file to the specified NOAA HPSS tarball path.
    proc = subprocess.Popen(cmd)
    proc.wait()

    if proc.returncode not in (0, 70):
        msg = (
            f"The HPSS archive creation failed with returncode {proc.returncode}. "
            "Aborting!!!"
        )
        raise NOAAHPSSInterfaceError(msg=msg)
