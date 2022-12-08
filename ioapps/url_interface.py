# =========================================================================

# Module: ioapps/url_interface.py

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

    url_interface.py

Description
-----------

    This module contains functions to parse a Uniform Resource Locator
    (URL) paths.

Classes
-------

    URLError(msg)

        This is the base-class for all exceptions; it is a sub-class
        of Error.

Functions
---------

    get_weblist(url, ext=None, include_dirname=False)

        This function builds a list of files beneath the specified URL
        file path.

    read_webfile(url, ignore_missing=False, split=None, return_string=False)

        This function collects the contents of a specified URL path
        and returns a Python list containing the respective contents.

Requirements
------------

- bs4; https://www.crummy.com/software/BeautifulSoup/

- urllib; https://github.com/python/cpython/tree/3.10/Lib/urllib/

Author(s)
---------

    Henry R. Winterbottom; 02 December 2022

History
-------

    2022-12-02: Henry Winterbottom -- Initial implementation.

"""

# ----

import os
import urllib

from bs4 import BeautifulSoup
from utils.error_interface import Error
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["get_weblist", "read_webfile"]

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

logger = Logger()

# ----


class URLError(Error):
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

        Creates a new URLError object.

        """
        super(URLError, self).__init__(msg=msg)


# ----


def get_weblist(url: str, ext: str = None, include_dirname: bool = False) -> list:
    """
    Description
    -----------

    This function builds a list of files beneath the specified URL
    file path.

    Parameters
    ----------

    url: str

        A Python string specifying the path to the internet
        (world-wide web; WWW) file to be retrieved.

    Keywords
    --------

    ext: str, optional

        A Python string specifying the web filename extension; if
        NoneType on entry the value defaults to to an empty string.

    include_dirname: bool, optional

        A Python boolean valued variable specifying whether to append
        the URL path directory name to the retrieved file names; if
        False upon entry, the retrieved files will simply be the
        basename for the respective retrieved file names.

    Returns
    -------

    weblist: list

        A Python list containing the files beneath the specified URL.

    Raises
    ------

    URLError:

        * raised if an Exception is encountered while attempting to
          parse the URL path contents; the respective error message
          accompanys the message string passed to the URLError class.

    """

    # Collect the contents of the URL file path into memory and parse
    # the contents of the URL file path; proceed accordingly.
    try:
        request = urllib.request.Request(url=url)
        with urllib.request.urlopen(url=request) as response:
            url_contents = response.read()
        soup = BeautifulSoup(url_contents, "html.parser")

    except Exception as error:
        msg = (
            "Retrieving the URL path {0} failed with error {1}. "
            "Aborting!!!".format(url, error)
        )
        raise URLError(msg=msg)

    # Compile a list of all URL file paths beneath the respective URL
    # file path provided upon entry; compile a list of the respective
    # files in accordance with the function attributes provided upon
    # entry; proceed accordingly.
    try:
        if ext is None:
            ext = str()
        webfiles = (
            node.get("href")
            for node in soup.find_all("a")
            if node.get("href").endswith(ext)
        )
        weblist = list()
        for webfile in webfiles:
            if include_dirname:
                filename = os.path.join(os.path.dirname(url), webfile)

            if not include_dirname:
                filename = webfile
            weblist.append(filename)

    except Exception as error:
        msg = (
            "Compilation of URL paths beneath URL {0} failed with "
            "error {1}. Aborting!!!".format(url, error)
        )
        raise URLError(msg=msg)

    return weblist


# ----


def read_webfile(
    url: str,
    ignore_missing: bool = False,
    split: str = None,
    return_string: bool = False,
) -> list:
    """
    Description
    -----------

    This function collects the contents of a specified URL path and
    returns a Python list containing the respective contents.

    Parameters
    ----------

    url: str

        A Python string specifying the path to the internet
        (world-wide web; WWW) file to be retrieved.

    Keywords
    --------

    ignore_missing: bool, optional

        A Python boolean valued variable specifying whether to ignore
        URL path requests that raise urllib.error.HTTPError; if True
        upon entry the returned list (see below) will be an empty
        list.

    split: str, optional

        A Python string specifying the string/characters to be used to
        split the contents of the respective file.

    return_string: bool, optional

        A Python boolean valued variable specifying whether to return
        the contents of the URL path as a string; if False upon entry,
        the default format of the file (typically bytes) will be
        returned.

    Returns
    -------

    contents: list

        A Python list containing the contents of the specified URL
        path.

    Raises
    ------

    URLError:

        * raised if an exception is encountered while establishing the
          URL path request.

        * raised if the opening the specified URL path fails due to a
          missing endpoint; raised only if ignore_missing is False
          upon entry.

        * raised if an exception is encountered while parsing the
          contents of the URL file path specified upon entry.

    """

    # Establish a connection to the specified URL file path; proceed
    # accordingly.
    try:
        request = urllib.request.Request(url=url)

    except Exception as error:
        msg = (
            "Retrieving the URL path {0} failed with error {1}. "
            "Aborting!!!".format(url, error)
        )
        raise URLError(msg=msg)

    # Read the contents of the URL file path; proceed accordingly.
    try:

        # Open the URL path and collect the contents of the file; the
        # contents will be returned as strings if return_string is
        # True upon entry; otherwise the default format of the file is
        # returned.
        contents = list()
        try:
            with urllib.request.urlopen(url=request) as response:
                contents = response.read()
            if return_string:
                contents = str(contents)

            if split is not None:
                contents = str(contents).split(split)

        # If an urllib.error.HTTPError exception is raised (i.e., the
        # URL path does not exist), proceed in accordance with the
        # attributes provided upon entry.
        except urllib.error.HTTPError as url_error:
            if ignore_missing:
                msg = (
                    "Opening URL {0} path failed with error {1}; "
                    "collection of URL path contents will not be "
                    "performed.".format(url, url_error)
                )
                logger.warn(msg=msg)

            if not ignore_missing:
                msg = (
                    "Opening URL path {0} failed with error {1}. "
                    "Aborting!!!".format(url, url_error)
                )
                raise URLError(ms=msg)

    except Exception as error:
        msg = (
            "Reading the contents of URL path {0} failed with error "
            "{1}. Aborting!!!".format(url, error)
        )
        raise URLError(msg=msg)

    return contents
