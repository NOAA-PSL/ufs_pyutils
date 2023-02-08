# =========================================================================

# Module: ioapps/wget_interface.py

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

    wget_interface.py

Description
-----------

    This module contains functions to create and collect internet
    (world-wide web; WWW) files using the Python wget package.

Functions
---------

    _check_wget_env()

        This function checks whether the run-time environment contains
        the wget application executable; if not, a WgetError will be
        thrown; if so, the path to the wget executable will be defined
        and returned.

    get_webfile(url, path, ignore_missing=False):

        This function collects the specified URL path using the Python
        wget package.

    get_weblist(url, path, matchstr=None, remove_webfile=True, ext=None):

        This function collects a list of files beneath the specified
        URL.

Author(s)
---------

    Henry R. Winterbottom; 02 December 2022

History
-------

    2022-12-02: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=broad-except
# pylint: disable=consider-using-with
# pylint: disable=raise-missing-from
# pylint: disable=too-many-locals
# pylint: disable=unused-argument

# ----

import os
import subprocess
from typing import List

from bs4 import BeautifulSoup
from tools import fileio_interface, system_interface
from utils.exceptions_interface import WgetInterfaceError
from utils.logger_interface import Logger

# ----

__all__ = ["get_webfile", "get_weblist"]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


def _check_wget_env() -> str:
    """
    Description
    -----------

    This function checks whether the run-time environment contains the
    wget application executable; if not, an WgetInterfaceError will be
    thrown; if so, the path to the wget executable will be defined and
    returned.

    Returns
    -------

    wget_exec: str

        A Python string specifying the path to the wget application
        executable.

    Raises
    ------

    WgetInterfaceError:

        * raised if the wget application executable path cannot be
          determined.

    """

    # Check the run-time environment in order to determine the wget
    # application executable path; proceed accordingly.
    wget_exec = system_interface.get_app_path(app="wget")

    if wget_exec is None:
        msg = (
            "The wget application executable could not be determined "
            "from the run-time environment. Aborting!!!"
        )
        raise WgetInterfaceError(msg=msg)

    return wget_exec


# ----


def get_webfile(url: str, path: str, ignore_missing: bool = False):
    """
    Description
    -----------

    This function collects the specified URL path using the Python
    wget package.

    Parameters
    ----------

    url: str

        A Python string specifying the path to the internet
        (world-wide web; WWW) file to be retrieved.

    path: str

        A Python string specifying the local path to which to write
        the retrieved file.

    Keywords
    --------

    ignore_missing: bool, optional

        A Python boolean valued variable specifying whether to ignore
        missing files (True) or raise CurlError for missing files
        (False).

    Raises
    ------

    WgetInterfaceError:

        * raised if an Exception related to a missing URL path is
          encountered; the respective error message accompanys the
          message string passed to the WgetInterfaceError class.

    """

    # Establish the wget application executable path.
    wget_exec = _check_wget_env()

    # Attempt to collect the specified URL path; proceed accordingly.
    msg = f"Collecting URL path {url}."
    logger.info(msg=msg)
    try:

        # Download the respective URL path.
        msg = f"Writing collected URL path {url} to local path {path}."
        logger.info(msg=msg)
        cmd = [f"{wget_exec}", f"{url}", "-O", f"{path}"]

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate()
        proc.wait()

    except Exception as errmsg:

        # Proceed accordingly for internet-based file paths that are
        # missing.
        if ignore_missing:
            pass

        if not ignore_missing:
            msg = (
                f"Collecting of internet path {url} failed with error {errmsg}. "
                "Aborting!!!"
            )
            raise WgetInterfaceError(msg=msg)


# ----


def get_weblist(
    url: str,
    path: str,
    matchstr: str = None,
    remove_webfile: bool = True,
    ext: str = None,
) -> List:
    """
    Description
    -----------

    This function collects a list of files beneath the specified URL.

    Parameters
    ----------

    url: str

        A Python string specifying the path to the internet
        (world-wide web; WWW) file to be retrieved.

    path: str

        A Python string specifying the local path to which to write
        the retrieved file.

    Keywords
    --------

    matchstr: str, optional

        A Python string specifying a character string for which to
        search while compiling the list of webfiles; if NoneType on
        entry, the entire list of files beneath the specified URL will
        be returned; if not NoneType, a list of files containing the
        specified string will be returned.

    remove_webfile: bool, optional

        A Python boolean valued variable specifying whether to remove
        the downloaded file containing the contents of the web
        directory defined by the specified URL; this value is set as
        True by default.

    ext: str, optional

        A Python string specifying the web filename extension; if
        NoneType on entry the value defaults to to an empty string.

    Returns
    -------

    weblist: list

        A Python list containing the files beneath the specified URL.

    Raises
    ------

    WgetInterfaceError:

        * raised if an Exception is encountered; the respective error
          message accompanys the message string passed to the
          WgetInterfaceError class.

    """

    # Establish the wget application executable path.
    wget_exec = _check_wget_env()

    # Attempt to collect the specified list of URL paths; proceed
    # accordingly.
    webpage = os.path.join(path, f"{0}.local".format(os.path.basename(url)))
    try:

        # Format the URL path; this is to make sure that the URL
        # string represents a directory tree rather than a file path.
        if url[-1:] != "/":
            url = os.path.join(f"{url}", str())
        msg = f"Downloading URL {url} to local path {webpage}."
        logger.info(msg=msg)

        # Attempt to download the URL path.
        cmd = [f"{wget_exec}", f"{url}", "-O", f"{webpage}"]

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.communicate()
        proc.wait()

        # Read the contents of the collected URL path.
        with open(webpage, "rb") as file:
            webdata = file.read()

        # Compile a list of all URL paths.
        soup = BeautifulSoup(webdata, "html.parser")
        if ext is None:
            ext = str()

        webfiles = (
            node.get("href")
            for node in soup.find_all("a")
            if node.get("href").endswith(ext)
        )
        weblist = []

        for webfile in webfiles:
            weblist.append(webfile)

        # Removing the specified files.
        if remove_webfile:
            filelist = [webpage]
            msg = f"The following files will be removed: {filelist}"
            logger.warn(msg=msg)
            fileio_interface.removefiles(filelist)

    except Exception as errmsg:
        msg = (
            f"Collection of files available at internet path {url} failed "
            f"with error {errmsg}. Aborting!!!"
        )
        raise WgetInterfaceError(msg=msg)

    return weblist
