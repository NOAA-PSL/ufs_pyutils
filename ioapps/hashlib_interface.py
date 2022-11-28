# =========================================================================

# $$$ MODULE DOCUMENTATION BLOCK

# UFS-RNR :: ush/ioapps/hashlib_interface.py

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

    hashlib_interface.py

Description
-----------

    This module contains functions to create and read local host
    tarball files.

Classes
-------

    HashLibError(msg)

        This is the base-class for all exceptions; it is a sub-class
        of Error.

Functions
---------

    get_hash(filepath, hash_level=None):

        This function defines a secure hash for the user specified
        file path.

Author(s)
--------- 

    Henry R. Winterbottom; 23 August 2022

History
-------

    2022-08-23: Henry Winterbottom -- Initial implementation.

"""

# ----

import hashlib
import os

from produtil.error_interface import Error
from produtil.logger_interface import Logger
from tools import parser_interface

# ----

# Define all available functions.
__all__ = ['get_hash'
           ]

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

logger = Logger()

# ----


class HashLibError(Error):
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

        Creates a new HashLibError object.

        """
        super(HashLibError, self).__init__(msg=msg)

# ----


def get_hash(filepath, hash_level=None):
    """
    Description
    -----------

    This method defines and returns a secure hash for the user
    specified file path.

    Parameters
    ----------

    filepath: str

        A Python string specifying the path to the file for which to
        generate a hash index.

    Keywords
    --------

    hash_level: str, optional

        A Python string specifying the hash level for the respective
        hash index; currently supported values are md5, new,
        pbkdf2_hmac, sha1, sha224, sha256, sha384, and sha512; if
        NoneType, the md5 hash level is assumed.

    Returns
    -------

    hash_index: str

        A Python string containing the hash index for the user
        specified file path.

    """

    # Define the hash level/type.
    if hash_level is None:
        hash_level = 'md5'

    # Define the type of hash library object based on the hash
    # level/type and proceed accordingly.
    hash_obj = parser_interface.object_getattr(
        object_in=hashlib, key=hash_level.lower())
    with open(filepath, 'rb') as f:
        c = f.read()
    hash_index = hash_obj(c).hexdigest()

    return hash_index
