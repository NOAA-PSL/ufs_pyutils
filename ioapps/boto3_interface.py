# =========================================================================

# Module: ioapps/boto3_interface.py

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

Functions
---------

    _aws_credentials(profile_name=None)

        This function establishes the boto3 credentials as a function
        of the entry value of the parameter attribute profile_name.

    _client(unsigned=False, session=None, profile_name=None,
            resource="s3")

        This function defines the boto3 resource bucket client object.

    _list(client, bucket, object_path=None)

        This function yields a generator function containing the
        contents of a resource bucket path.

    _read(client, bucket, file_name, object_name)

        This function downloads (i.e., read) a resource bucket object to a
        local file.

    _resource(unsigned=False, profile_name=None, resource="s3")

        This function defines the boto3 resource bucket object.

    _session(profile_name)

        This method defines a boto3 session in accordance with the
        profile_name attribute value.

    _write(client, bucket, file_name, object_name)

        This function uploads (i.e., writes) a local file to a
        resource bucket object.

    filelist(bucket, object_path=None, profile_name=None,
             resource="s3")

        This function returns a list containing the contents of a
        resource bucket path.

    get(bucket, filedict=None, into_mem=False, object_path=None,
        profile_name=None, resource="s3")

        This function downloads objects from a user specified resource
        bucket either onto the respective platforms local disk
        (into_mem = False) or into memory (into_mem = True).

    put(bucket, filedict, profile_name=None, resource="s3")

        This function uploads objects to a user specified resource
        bucket.

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

# pylint: disable=broad-except
# pylint: disable=consider-using-with
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
# pylint: disable=raise-missing-from
# pylint: disable=redefined-outer-name

# ----

from tempfile import NamedTemporaryFile
from typing import Dict, List, Tuple

import boto3
from botocore import UNSIGNED
from botocore.config import Config
from utils.exceptions_interface import Boto3InterfaceError
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["filelist", "get", "put"]

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

logger = Logger()

# ----


def _aws_credentials(profile_name: str = None) -> Tuple:
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

    session: object

        A Python boto3 Session object for the respective entry value
        of the parameter profile_name; if profile_name is NoneType
        upon entry, the returned value is NoneType.

    Raises
    ------

    Boto3InterfaceError:

        * raised if an exception is encountered establishing the boto3
          Session object for non-NoneType entry values for the
          profile_name parameter.

    """

    # Define the AWS resource session and client attributes; proceed
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

            (unsigned, session) = (False, boto3.Session(profile_name=profile_name))

        except Exception as errmsg:
            msg = (
                f"Establishing the boto3 session for profile name {profile_name} "
                f"failed with error {errmsg}. Aborting!!!"
            )
            raise Boto3InterfaceError(msg=msg)

    return (unsigned, session)


# ----


def _client(
    unsigned: bool = False,
    session: object = None,
    profile_name: str = None,
    resource: str = "s3",
) -> object:
    """
    Description
    -----------

    This function defines the boto3 resource bucket client object.

    Keywords
    --------

    unsigned: bool, optional

        A Python boolean valued variable specifying whether or not to
        provided UNSIGNED credentials to the AWS resource client
        configuration.

    session: object, optional

        A Python boto3 Session object for the respective entry value
        of the parameter profile_name; if profile_name is NoneType
        upon entry, the returned value is NoneType.

    profile_name: str, optional

        A Python string specifying the profile name beneath the user
        ~/.aws/credentials file to be used to initiate the boto3
        session; if NoneType upon entry an unsigned session is
        implied.

    resource: str, optional

        A Python string specifying the supported AWS resource;
        allowable storage resources can be found at
        https://tinyurl.com/AWS-Storage-Resources.

    Returns
    -------

    client: object

        A Python boto3 resource bucket client object.

    """

    # Check parameter values provided upon entry; proceed accordingly.
    if not unsigned and session is None:
        msg = (
            "The boto3 client cannot be established for instances when "
            "using neither UNSIGNED credentials of a valid "
            "~/.aws/credentials profile name. Aborting!!!"
        )
        raise Boto3InterfaceError(msg=msg)

    if unsigned and session is not None:
        msg = (
            "A boto3 client configuration cannot be determined when "
            "UNSIGNED credentials are specified and the profile_name "
            "parameter value upon entry is not NoneType. Aborting!!!"
        )
        raise Boto3InterfaceError(msg=msg)

    # Establish the boto3 resource bucket client object in accordance
    # with the upon entry parameter values.
    if unsigned:
        client = boto3.client(resource, config=Config(signature_version=UNSIGNED))

    if session is not None:
        session = _session(profile_name=profile_name)
        client = session.client(resource)

    return client


# ----


def _list(client: object, bucket: str, object_path: str = None) -> List:
    """
    Description
    -----------

    This function returns a list containing the contents of a resource
    bucket path as specified by the bucket object keys.

    Parameters
    ----------

    client: object

        A Python boto3 resource bucket client object.

    bucket: str

        A Python string specifying the name of the resource bucket.

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
        specified resource bucket.

    """

    # Compile a list of the bucket contents accordingly.
    (filelist, kwargs) = ([], {})
    if object_path is None:
        while True:
            response = client.list_objects_v2(Bucket=bucket)
            for obj in response["Contents"]:
                filelist.append(obj["Key"])
            try:
                kwargs["ContinuationToken"] = response["NextContinuationToken"]

            except KeyError:
                break

    if object_path is not None:
        response = client.list_objects(Bucket=bucket, Prefix=object_path)
        for content in response.get("Contents", []):
            filelist.append(content.get("Key"))

    return filelist


# ----


def _read(client: object, bucket: str, file_name: str, object_name: str) -> None:
    """
    Description
    -----------

    This function downloads (i.e., read) a resource bucket object to a
    local file.

    Parameters
    ----------

    client: object

        A Python boto3 resource bucket client object.

    bucket: str

        A Python string specifying the name of the resource bucket.

    file_name: str

        A Python string specifying the local file path to which the
        resource bucket object is to be downloaded.

    object_name: str

        A Python string specifying the resource bucket object
        corresponding to the file_name attribute.

    """

    # Download the contents of the specified resource bucket object.
    try:
        client.download_file(bucket, object_name, file_name)

    except Exception as errmsg:
        msg = (
            f"Reading from bucket {bucket} object path {object_name} caused "
            f"the following exception to occur: {errmsg}"
        )
        logger.warn(msg=msg)


# ----


def _resource(
    unsigned: bool = False, profile_name: str = None, resource: str = "s3"
) -> object:
    """
    Description
    -----------

    This function defines the boto client resource object.

    Keywords
    --------

    unsigned: bool, optional

        A Python boolean valued variable specifying whether or not to
        provided UNSIGNED credentials to the AWS resource
        configuration.

    profile_name: str, optional

        A Python string specifying the profile name beneath the user
        ~/.aws/credentials file to be used to initiate the boto3
        session; if NoneType upon entry an unsigned session is
        implied.

    resource: str, optional

        A Python string specifying the supported AWS resource;
        allowable storage resources can be found at
        https://tinyurl.com/AWS-Storage-Resources.

    Returns
    -------

    resource_obj: object

        A Python boto3 client resource object.

    """

    # Establish the boto3 resource bucket client object.
    if unsigned:
        resource_obj = boto3.resource(
            resource, config=Config(signature_version=UNSIGNED)
        )

    if not unsigned:

        session = _session(profile_name=profile_name)
        resource_obj = session.resource(resource)

    return resource_obj


# ----


def _session(profile_name: str) -> object:
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

    session: object

        A Python boto3 Session object for the respective entry value
        of the parameter profile_name.

    """

    # Define the boto3 session object.
    session = boto3.Session(profile_name=profile_name)

    return session


# ----


def _write(client: object, bucket: str, file_name: str, object_name: str) -> None:
    """
    Description
    -----------

    This function uploads (i.e., writes) a local file to a resource
    bucket object.

    Parameters
    ----------

    client: object

        A Python boto3 resource bucket client object.

    bucket: str

        A Python string specifying the name of the resource bucket.

    file_name: str

        A Python string specifying the local file path to be uploaded
        as a resource bucket object.

    object_name: str

        A Python string specifying the resource bucket object
        corresponding to the file_name attribute.

    """

    # Upload the specified local file path to the specified resource
    # bucket and object path.
    client.upload_file(file_name, bucket, object_name)


# ----


def filelist(
    bucket: str, object_path: str = None, profile_name: str = None, resource: str = "s3"
) -> List:
    """
    Description
    -----------

    This function returns a list containing the contents of a resource
    bucket path.

    Parameters
    ----------

    bucket: str

        A Python string specifying the name of the resource bucket.

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

    resource: str, optional

        A Python string specifying the supported AWS resource;
        allowable storage resources can be found at
        https://tinyurl.com/AWS-Storage-Resources.

    Returns
    -------

    filelist: list

        A Python list containing the contents of the resource bucket.

    """

    # Collect the contents of the respective resource bucket path.
    (unsigned, session) = _aws_credentials(profile_name=profile_name)
    client = _client(
        unsigned=unsigned, session=session, profile_name=profile_name, resource=resource
    )
    filelist = _list(client=client, bucket=bucket, object_path=object_path)

    return filelist


# ----


def get(
    bucket: str,
    filedict: dict = None,
    into_mem: bool = False,
    object_path: str = None,
    profile_name: str = None,
    resource: str = "s3",
) -> object:
    """
    Description
    -----------

    This function downloads objects from a user specified resource
    bucket either onto the respective platforms local disk (into_mem =
    False) or into memory (into_mem = True).

    Parameters
    ----------

    bucket: str

        A Python string specifying the name of the resource bucket.

    Keywords
    --------

    filedict: dict, optional

        A Python dictionary containing key and value pairs for the
        objects to be read from the resource bucket objects; the
        dictionary keys are the local file path and the respective
        dictionary key values are the resource object names.

    into_mem: bool, optional

        A Python boolean valued variable specifying whether to read
        the contents of the resource bucket and object path (see
        object_path, below) into memory.

    object_path: str, optional

        A Python string specifying the respective resource bucket
        object path; required and used only if into_mem is True upon
        entry.

    profile_name: str, optional

        A Python string specifying the profile name beneath the user
        ~/.aws/credentials file to be used to initiate the boto3
        session; if NoneType upon entry an unsigned session is
        implied.

    resource: str, optional

        A Python string specifying the supported AWS resource;
        allowable storage resources can be found at
        https://tinyurl.com/AWS-Storage-Resources.

    Returns
    -------

    object_memory: object

        A Python tempfile NamedTemporaryFile object containing the
        contents of the resource bucket and object path specified upon
        entry; if the into_mem parameter is False upon entry, the
        returned value is NoneType.

    Raises
    ------

    Boto3InterfaceError:

        * raised if parameter values provided upon entry are invalid.

        * raised if the downloading of a specified object path
          into local memory encounters and exception.

        * raised if the downloading of a specified object path
          encounters and exception.

    """

    # Define the Python boto3 access credentials.
    (unsigned, session) = _aws_credentials(profile_name=profile_name)

    # Check the method to be used for the respective object retrieval;
    # proceed accordingly.
    if into_mem:

        # Check the parameter values provided upon entry and proceed
        # accordingly.
        if object_path is None:
            msg = (
                "For into memory retrievals, the parameter variable "
                "object_path value cannot be NoneType. Aborting!!!"
            )
            raise Boto3InterfaceError(msg=msg)

        # Define the Python boto3 bucket resource object.
        resource_obj = _resource(
            unsigned=unsigned, profile_name=profile_name, resource=resource
        )

        # Collect the object path and store the contents into memory;
        # proceed accordingly.
        try:

            # Define the resource attributes and read the contents of
            # the specified object path into memory.
            bucket = resource_obj.Bucket(bucket)
            bucket_object = bucket.Object(object_path)
            object_memory = NamedTemporaryFile()
            with open(object_memory.name, "wb") as filepath:
                bucket_object.download_fileobj(filepath)

        except Exception as errmsg:
            msg = (
                f"Reading {resource} object path {object_path} into memory failed with "
                f"error {errmsg}. Aborting!!!"
            )
            raise Boto3InterfaceError(msg=msg) from errmsg

    if not into_mem:

        # Reset the value returned by the method; since the retrieval
        # will not be read into memory, set to NoneType.
        object_memory = None

        # Check the parameter values provided upon entry and proceed
        # accordingly.
        if filedict is None:
            msg = (
                "For file retrievals to the local platform/disk, the "
                "parameter variable filedict cannot be NoneType upon "
                "entry. Aborting!!!"
            )
            raise Boto3InterfaceError(msg=msg)

        # Define the Python boto3 bucket client object.
        client = _client(
            unsigned=unsigned,
            session=session,
            profile_name=profile_name,
            resource=resource,
        )

        # Collect the specified files from the respective resource
        # bucket and object path.
        for key in filedict.keys():
            msg = (
                f"Downloading object {filedict[key]} from {resource} bucket "
                f"{bucket} to {key}."
            )
            logger.info(msg=msg)
            try:
                _read(
                    client=client,
                    bucket=bucket,
                    file_name=key,
                    object_name=filedict[key],
                )

            except Exception as errmsg:
                msg = (
                    f"Downloading of object {filedict[key]} from {resource} bucket "
                    f"{bucket} to {key} failed with error {errmsg}. Aborting!!!"
                )
                raise Boto3InterfaceError(msg=msg) from errmsg

    return object_memory


# ----


def put(
    bucket: str, filedict: Dict, profile_name: str = None, resource: str = "s3"
) -> None:
    """
    Description
    -----------

    This function uploads objects to a user specified resource bucket.

    Parameters
    ----------

    bucket: str

        A Python string specifying the name of the resource bucket.

    filedict: dict

        A Python dictionary containing key and value pairs for the
        objects to be written to the resource bucket objects; the
        dictionary keys are the local file path and the respective
        dictionary key values are the object names.

    Keywords
    --------

    profile_name: str, optional

        A Python string specifying the profile name beneath the user
        ~/.aws/credentials file to be used to initiate the boto3
        session; if NoneType upon entry an unsigned session is
        implied.

    resource: str, optional

        A Python string specifying the supported AWS resource;
        allowable storage resources can be found at
        https://tinyurl.com/AWS-Storage-Resources.

    Raises
    ------

    Boto3InterfaceError:

        * raised if the uploading of a specified object path
          encounters and exception.

    """

    # Define the Python boto3 bucket client object.
    (unsigned, session) = _aws_credentials(profile_name=profile_name)
    client = _client(
        unsigned=unsigned, session=session, profile_name=profile_name, resource=resource
    )

    # Upload the specified files from the resource bucket and object
    # path.
    for key in filedict.keys():
        msg = (
            f"Uploading file {key} to {resource} bucket {bucket} object "
            f"{filedict[key]}."
        )
        logger.info(msg=msg)
        try:
            _write(
                client=client, bucket=bucket, file_name=key, object_name=filedict[key]
            )

        except Exception as errmsg:
            msg = (
                f"Uploading of file {key} to {resource} bucket {bucket} object {filedict[key]} "
                f"failed with error {errmsg}. Aborting!!!"
            )
            raise Boto3InterfaceError(msg=msg) from errmsg
