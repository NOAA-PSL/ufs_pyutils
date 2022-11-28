# =========================================================================

# $$$ MODULE DOCUMENTATION BLOCK

# UFS-RNR :: ush/ioapps/boto3_interface.py

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

    boto3_interface.py

Description
-----------

    This module contains functions for various Amazon Web Services
    (AWS) storage interfaces provided by the Python boto3 library.

Classes
-------

    Boto3Error(msg)

        This is the base-class for all exceptions; it is a sub-class
        of Error.

Functions
---------

    _aws_credentials(profile_name=None)

        This function establishes the boto3 credentials as a function
        of the entry value of the parameter attribute profile_name.

    _s3client(unsigned=False, session=None, profile_name=None)

        This function defines the boto s3 bucket client object.

    _s3list(client, bucket, object_path=None)

        This function yields a generator function containing the
        contents of a s3 bucket path.

    _s3read(client, bucket, file_name, object_name)

        This function downloads (i.e., read) a s3 bucket object to a
        local file.

    _s3resource(unsigned=False, profile_name=None)

        This function defines the boto s3 bucket resource object.

    _s3session(profile_name)

        This method defines a boto3 session in accordance with the
        profile_name attribute value.

    _s3write(client, bucket, file_name, object_name)

        This function uploads (i.e., writes) a local file to a s3
        bucket object.

    s3filelist(bucket, object_path=None, profile_name=None)

        This function returns a list containing the contents of a s3
        bucket path.

    s3get(bucket, filedict=None, into_mem=False, object_path=None,
          profile_name=None)

        This function downloads objects from a user specified s3
        bucket either onto the respective platforms local disk
        (into_mem = False) or into memory (into_mem = True).

    s3put(bucket, filedict, profile_name=None)

        This function uploads objects to a user specified s3 bucket.

Notes
-----

    The functions within this module, when employed for credentialed
    sessions, requires that the credentials (i.e., aws_access_key_id
    and aws_secret_access_key) corresponding to the profile_name
    parameter value upon entry exist in the user path
    ~/.aws/credentials.

Requirements
------------

- boto3; https://github.com/boto/boto3

Author(s)
---------

   Henry R. Winterbottom; 22 August 2022

History
-------

   2022-08-22: Henry Winterbottom -- Initial implementation.

"""

# ----

import boto3
import os

from botocore import UNSIGNED
from botocore.config import Config
from produtil.error_interface import Error
from produtil.logger_interface import Logger
from tempfile import NamedTemporaryFile
from tools import fileio_interface
from tools import parser_interface

# ----

# Define all available functions.
__all__ = ['s3filelist',
           's3get',
           's3put'
           ]

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

logger = Logger()

# ----


class Boto3Error(Error):
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

        Creates a new Boto3Error object.

        """
        super(Boto3Error, self).__init__(msg=msg)

# ----


def _aws_credentials(profile_name=None):
    """
    Description
    -----------

    This function establishes the boto3 credentials as a function of
    the entry value of the parameter attribute profile_name.

    Keywords
    --------

    profile_name: str, optional

        A Python string specifying the profile name beneath the user
        ~/.aws/credentials file to be used to initiate the boto3
        session; if NoneType upon entry an unsigned session is
        implied.

    Returns
    -------

    unsigned: bool

        A Python boolean valued variable specifying whether or not to
        provided UNSIGNED credentials to the boto3 client
        configuration.

    session: obj

        A Python boto3 Session object for the respective entry value
        of the parameter profile_name; if profile_name is NoneType
        upon entry, the returned value is NoneType.

    Raises
    ------

    Boto3Error:

        * raised if an exception is encountered establishing the boto3
          Session object for non-NoneType entry values for the
          profile_name parameter.

    """

    # Define the AWS s3 session and client attributes; proceed
    # accordingly.
    if profile_name is None:

        # If the value for the profile_name parameters is not
        # specified upon entry, assume an unsigned session; proceed
        # accordingly.
        (unsigned, session) = (True, None)

    if profile_name is not None:

        # If the parameter profile_name is not NoneType upon entry
        # this implies that credentials are required in order to
        # initiate a boto3 session; proceed accordingly.
        try:

            (unsigned, session) = (False,
                                   boto3.Session(profile_name=profile_name))

        except Exception as error:
            msg = ('Establishing the boto3 session for profile name {0} '
                   'failed with error {1}. Aborting!!!'.format(profile_name,
                                                               error))
            raise Boto3Error(msg=msg)

    return (unsigned, session)

# ----


def _s3client(unsigned=False, session=None, profile_name=None):
    """
    Description
    -----------

    This function defines the boto3 s3 bucket client object.

    Keywords
    --------

    unsigned: bool, optional

        A Python boolean valued variable specifying whether or not to
        provided UNSIGNED credentials to the AWS s3 client
        configuration.

    session: obj, optional

        A Python boto3 Session object for the respective entry value
        of the parameter profile_name; if profile_name is NoneType
        upon entry, the returned value is NoneType.

    profile_name: str, optional

        A Python string specifying the profile name beneath the user
        ~/.aws/credentials file to be used to initiate the boto3
        session; if NoneType upon entry an unsigned session is
        implied.

    Returns
    -------

    client: obj

        A Python boto3 s3 bucket client object.

    """

    # Check parameter values provided upon entry; proceed accordingly.
    if not unsigned and session is None:
        msg = ('The boto3 client cannot be established for instances when '
               'using neither UNSIGNED credentials of a valid '
               '~/.aws/credentials profile name. Aborting!!!')
        raise Boto3Error(msg=msg)

    if unsigned and session is not None:
        msg = ('A boto3 client configuration cannot be determined when '
               'UNSIGNED credentials are specified and the profile_name '
               'parameter value upon entry is not NoneType. Aborting!!!')
        raise Boto3Error(msg=msg)

    # Establish the boto3 s3 bucket client object in accordance with
    # the upon entry parameter values.
    if unsigned:
        client = boto3.client('s3', config=Config(
            signature_version=UNSIGNED))

    if session is not None:
        session = _s3session(profile_name=profile_name)
        client = session.client('s3')

    return client

# ----


def _s3list(client, bucket, object_path=None):
    """
    Description
    -----------

    This function returns a list containing the contents of a s3
    bucket path as specified by the s3 object keys.

    Parameters
    ----------

    client: obj

        A Python boto3 s3 bucket client object.

    bucket: str

        A Python string specifying the name of the s3 bucket.

    Keywords
    --------

    object_path: str, optional

        A Python string specifying the object directory beneath the
        respective bucket; if present, the boto3 interface will seek
        only the contents with the specified object path within the
        specified bucket; if not present (e.g., NoneType), the entire
        contents of the bucket will be returned.

    Returns
    -------

    filelist: list

        A Python list containing the contents (keys) of the user
        specified s3 bucket.

    """

    # Compile a list of the s3 bucket contents accordingly.
    (filelist, kwargs) = (list(), dict())
    if object_path is None:
        while True:
            response = client.list_objects_v2(Bucket=bucket)
            for obj in response['Contents']:
                filelist.append(obj['Key'])
            try:
                kwargs['ContinuationToken'] = response['NextContinuationToken']

            except KeyError:
                break

    if object_path is not None:
        response = client.list_objects(Bucket=bucket, Prefix=object_path)
        for content in response.get('Contents', []):
            filelist.append(content.get('Key'))

    return filelist

# ----


def _s3read(client, bucket, file_name, object_name):
    """
    Description
    -----------

    This function downloads (i.e., read) a s3 bucket object to a local
    file.

    Parameters
    ----------

    client: obj

        A Python boto3 s3 bucket client object.

    bucket: str

        A Python string specifying the name of the s3 bucket.

    file_name: str

        A Python string specifying the local file path to which the s3
        bucket object is to be downloaded.

    object_name: str

        A Python string specifying the s3 bucket object corresponding
        to the file_name attribute.

    """

    # Download the contents of the specified s3 bucket object.
    try:
        client.download_file(bucket, object_name, file_name)

    except Exception as error:
        msg = ('Reading from S3 caused the following exception to '
               'occur:\n {0}'.format(error))
        logger.warn(msg=msg)

# ----


def _s3resource(unsigned=False, profile_name=None):
    """
    Description
    -----------

    This function defines the boto s3 bucket resource object.

    Keywords
    --------

    unsigned: bool, optional

        A Python boolean valued variable specifying whether or not to
        provided UNSIGNED credentials to the AWS s3 resource
        configuration.

    profile_name: str, optional

        A Python string specifying the profile name beneath the user
        ~/.aws/credentials file to be used to initiate the boto3
        session; if NoneType upon entry an unsigned session is
        implied.

    Returns
    -------

    resource: obj

        A Python boto3 s3 bucket resource object.

    """

    # Establish the boto3 s3 bucket client object.
    if unsigned:
        resource = boto3.resource('s3', config=Config(
            signature_version=UNSIGNED))

    if not unsigned:

        session = _s3session(profile_name=profile_name)
        resource = session.resource('s3')

    return resource

# ----


def _s3session(profile_name):
    """
    Description
    -----------

    This method defines a boto3 session in accordance with the
    profile_name attribute value.

    Parameters
    ----------

    profile_name: str

        A Python string specifying the profile name beneath the user
        ~/.aws/credentials file to be used to initiate the boto3
        session.

    Returns
    -------

    session: obj

        A Python boto3 Session object for the respective entry value
        of the parameter profile_name.

    """

    # Define the boto3 session object.
    session = boto3.Session(profile_name=profile_name)

    return session

# ----


def _s3write(client, bucket, file_name, object_name):
    """
    Description
    -----------

    This function uploads (i.e., writes) a local file to a s3 bucket
    object.

    Parameters
    ----------

    client: obj

        A Python boto3 s3 bucket client object.

    bucket: str

        A Python string specifying the name of the s3 bucket.

    file_name: str

        A Python string specifying the local file path to be uploaded
        as a s3 bucket object.

    object_name: str

        A Python string specifying the s3 bucket object corresponding
        to the file_name attribute.

    """

    # Upload the specified local file path to the specified s3 bucket
    # and object path.
    client.upload_file(file_name, bucket, object_name)

# ----


def s3filelist(bucket, object_path=None, profile_name=None):
    """
    Description
    -----------

    This function returns a list containing the contents of a s3
    bucket path.

    Parameters
    ----------

    bucket: str

        A Python string specifying the name of the s3 bucket.

    Keywords
    --------

    object_path: str, optional

        A Python string specifying the object directory beneath the
        respective bucket; if present, the boto3 interface will seek
        only the contents with the specified object path within the
        specified bucket; if not present (e.g., NoneType), the entire
        contents of the bucket will be returned.

    profile_name: str, optional

        A Python string specifying the profile name beneath the user
        ~/.aws/credentials file to be used to initiate the boto3
        session; if NoneType upon entry an unsigned session is
        implied.

    Returns
    -------

    filelist: list

        A Python list containing the contents of the s3 bucket.

    """

    # Collect the contents of the respective s3 bucket path.
    (unsigned, session) = _aws_credentials(profile_name=profile_name)
    client = _s3client(unsigned=unsigned, session=session,
                       profile_name=profile_name)
    filelist = _s3list(client=client, bucket=bucket, object_path=object_path)

    return filelist


# ----


def s3get(bucket, filedict=None, into_mem=False, object_path=None,
          profile_name=None):
    """
    Description
    -----------

    This function downloads objects from a user specified s3 bucket
    either onto the respective platforms local disk (into_mem = False)
    or into memory (into_mem = True).

    Parameters
    ----------

    bucket: str

        A Python string specifying the name of the s3 bucket.

    Keywords
    --------

    filedict: dict, optional

        A Python dictionary containing key and value pairs for the
        objects to be read from the s3 bucket objects; the dictionary
        keys are the local file path and the respective dictionary key
        values are the s3 object names.

    into_mem: bool, optional

        A Python boolean valued variable specifying whether to read
        the contents of the s3 bucket and object path (see
        object_path, below) into memory.

    object_path: str, optional

        A Python string specifying the respective s3 bucket object
        path; required and used only if into_mem is True upon entry.

    profile_name: str, optional

        A Python string specifying the profile name beneath the user
        ~/.aws/credentials file to be used to initiate the boto3
        session; if NoneType upon entry an unsigned session is
        implied.

    Returns
    -------

    object_memory: obj

        A Python tempfile NamedTemporaryFile object containing the
        contents of the s3 bucket and object path specified upon
        entry; if the into_mem parameter is False upon entry, the
        returned value is NoneType.

    Raises
    ------

    Boto3Error:

        * raised if parameter values provided upon entry are invalid.

        * raised if the downloading of a specified object path
          into local memory encounters and exception.

        * raised if the downloading of a specified object path
          encounters and exception.

    """

    # Define the Python boto3 access credentials.
    (unsigned, session) = _aws_credentials(profile_name=profile_name)

    # Check the method to be used for the respective s3 object
    # retrieval; proceed accordingly.
    if into_mem:

        # Check the parameter values provided upon entry and proceed
        # accordingly.
        if object_path is None:
            msg = ('For into memory retrievals, the parameter variable '
                   'object_path value cannot be NoneType. Aborting!!!')
            raise Boto3Error(msg=msg)

        # Define the Python boto3 bucket resource object.
        resource = _s3resource(unsigned=unsigned, profile_name=profile_name)

        # Collect the s3 object and store the contents into memory;
        # proceed accordingly.
        try:

            # Define the s3 attributes and read the contents of the
            # specified s3 object path into memory.
            bucket = resource.Bucket(bucket)
            object = bucket.Object(object_path)
            object_memory = NamedTemporaryFile()
            f = open(object_memory.name, 'wb')
            object.download_fileobj(f)
            f.close()

        except Exception as error:
            msg = ('Reading s3 object path {0} into memory failed with '
                   'error {1}. Aborting!!!'.format(object_path, error))
            raise Boto3Error(msg=msg)

    if not into_mem:

        # Reset the value returned by the method; since the retrieval
        # will not be read into memory, set to NoneType.
        object_memory = None

        # Check the parameter values provided upon entry and proceed
        # accordingly.
        if filedict is None:
            msg = ('For file retrievals to the local platform/disk, the '
                   'parameter variable filedict cannot be NoneType upon '
                   'entry. Aborting!!!')
            raise Boto3Error(msg=msg)

        # Define the Python boto3 bucket client object.
        client = _s3client(unsigned=unsigned, session=session,
                           profile_name=profile_name)

        # Collect the specified files from the s3 bucket and object path.
        for key in filedict.keys():
            msg = ('Downloading object {0} from s3 bucket {1} to {2}.'.
                   format(filedict[key], bucket, key))
            logger.info(msg=msg)
            try:
                _s3read(client=client, bucket=bucket,
                        file_name=key, object_name=filedict[key])

            except Exception as error:
                msg = ('Downloading of object {0} from s3 bucket {1} to {2} failed '
                       'with error {3}. Aborting!!!'.format(
                           filedict[key], bucket, key, error))
                raise Boto3Error(msg=msg)

    return object_memory


# ----


def s3put(bucket, filedict, profile_name=None):
    """
    Description
    -----------

    This function uploads objects to a user specified s3 bucket.

    Parameters
    ----------

    bucket: str

        A Python string specifying the name of the s3 bucket.

    filedict: dict

        A Python dictionary containing key and value pairs for the
        objects to be written to the s3 bucket objects; the dictionary
        keys are the local file path and the respective dictionary key
        values are the s3 object names.

    Keywords
    --------

    profile_name: str, optional

        A Python string specifying the profile name beneath the user
        ~/.aws/credentials file to be used to initiate the boto3
        session; if NoneType upon entry an unsigned session is
        implied.

    Raises
    ------

    Boto3Error:

        * raised if the uploading of a specified object path
          encounters and exception.

    """

    # Define the Python boto3 s3 bucket client object.
    (unsigned, session) = _aws_credentials(profile_name=profile_name)
    client = _s3client(unsigned=unsigned, session=session,
                       profile_name=profile_name)

    # Upload the specified files from the s3 bucket and object path.
    for key in filedict.keys():
        msg = ('Uploading file {0} to s3 bucket {1} object {2}.'.format(
            key, bucket, filedict[key]))
        logger.info(msg=msg)
        try:
            _s3write(client=client, bucket=bucket,
                     file_name=key, object_name=filedict[key])

        except Exception as error:
            msg = ('Uploading of file {0} to s3 bucket {1} object {2} failed '
                   'with error {3}. Aborting!!!'.format(
                       key, bucket, filedict[key], error))
            raise Boto3Error(msg=msg)
