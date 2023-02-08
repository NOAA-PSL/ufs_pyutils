# =========================================================================

# Module: ioapps/awscli_interface.py

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

    awscli_interface.py

Description
-----------

    This module contains functions which interface with the Amazon Web
    Services (AWS) command-line interface (CLI) for AWS resource
    bucket and object paths.

Functions
---------

    _check_awscli_env()

        This function checks whether the AWS CLI environment has been
        loaded; if not, an AWSCLIInterfaceError will be thrown; if so,
        the path to the AWS CLI executable will be defined and
        returned.

    exist_awspath(aws_path, resource='s3', profile=None)

        This function queries the respective Amazon Web Services (AWS)
        resource bucket and object path to, using the command line
        interface (CLI), in order to determine whether a file/path
        exists; a boolean value indicating the status is returned.

    list_awspath(aws_path, resource='s3', profile=None)

        This function provides an interface to the Amazon Web Services
        (AWS) command line interface (CLI) application to list the
        specified resource bucket contents.

    put_awsfile(aws_path, path, is_dir=False, is_wildcards=False,
                aws_exclude=None, aws_include=None, resource='s3',
                profile=None, errlog=None, outlog=None):

        This function provides an interface to the Amazona Web
        Services (AWS) command line interface (CLI) application to
        stage local files within specified AWS resource `bucket and object
        paths.

Requirements
------------

- awscli; https://aws.amazon.com/cli/

Author(s)
---------

    Henry R. Winterbottom; 29 November 2022

History
-------

    2022-11-29: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=broad-except
# pylint: disable=consider-using-with
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
# pylint: disable=unused-argument

# ----

import subprocess
from ast import literal_eval
from typing import List

from tools import parser_interface, system_interface
from utils.exceptions_interface import AWSCLIInterfaceError
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["exist_awspath", "list_awspath", "put_awsfile"]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


def _check_awscli_env() -> str:
    """
    Description
    -----------

    This function checks whether the AWS CLI environment has been
    loaded; if not, an AWSCLIInterfaceError will be thrown; if so, the
    path to the AWS CLI executable will be defined and returned.

    Returns
    -------

    awscli: str

        A Python string specifying the path to the AWS CLI executable.

    Raises
    ------

    AWSCLIInterfaceError:

        * raised if the AWS CLI executable path cannot be determined.

    """

    # Check the run-time environment in order to determine the AWS CLI
    # executable path.
    awscli = system_interface.get_app_path(app="aws")

    if awscli is None:
        msg = (
            "The AWS CLI executable could not be determined for your "
            "system; please check that the appropriate AWS CLI "
            "libaries/modules are loaded prior to calling this script. "
            "Aborting!!!"
        )
        raise AWSCLIInterfaceError(msg=msg)

    return awscli


# ----


def exist_awspath(aws_path: str, resource: str = "s3", profile: str = None) -> bool:
    """
    Description
    -----------

    This function queries the respective Amazon Web Services (AWS)
    resource bucket and object path to, using the command line
    interface (CLI), in order to determine whether a file/path exists;
    a boolean value indicating the status is returned.

    Parameters
    ----------

    aws_path: str

        A Python string specifying the AWS resource bucket and object
        path within which to collect the respective contents.

    Keywords
    --------

    resource: str, optional

        A Python string specifying the supported AWS resource;
        allowable storage resources can be found at
        https://tinyurl.com/AWS-Storage-Resources.

    profile: str, optional

        A Python string specifying the AWS CLI credentials; if
        NoneType upon entry the AWS CLI assumes the --no-sign-request
        attribute; if this value is not NoneType, the credentials
        corresponding to the respective string must live beneath the
        ~/.aws/credentials path and contain the appropriate AWS
        aws_access_key_id and aws_secret_access_key attributes.

    Returns
    -------

    exist: bool

        A Python boolean valued variable specifying whether the AWS
        path provided upon entry exists.

    """

    # Establish the AWS CLI executable environment.
    awscli = _check_awscli_env()
    cmd = [f"{awscli}", f"{resource}", "ls", f"{aws_path}"]

    # Determine the permission attributes for the AWS CLI executable.
    if profile is None:
        cmd.append("--no-sign-request")
    if profile is not None:
        cmd.append("--profile")
        cmd.append(f"{profile}")

    # Query the AWS path; proceed accordingly.
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (contents, _) = proc.communicate()
    proc.wait()

    # If the contents list returned by the AWS CLI is not empty, the
    # AWS path is assumed to exist; otherwise it is assumed not to
    # exist.
    exist = len(contents.decode("utf-8")) > 0

    return exist


# ----


def list_awspath(aws_path: str, resource: str = "s3", profile: str = None) -> List:
    """
    Description
    -----------

    This function provides an interface to the Amazon Web Services
    (AWS) command line interface (CLI) application to list the
    specified resource bucket contents.

    Parameters
    ----------

    aws_path: str

        A Python string specifying the AWS resource bucket and object
        path within which to collect the respective contents.

    Keywords
    --------

    resource: str, optional

        A Python string specifying the supported AWS resource;
        allowable storage resources can be found at
        https://tinyurl.com/AWS-Storage-Resources.

    profile: str, optional

        A Python string specifying the AWS CLI credentials; if
        NoneType upon entry the AWS CLI assumes the --no-sign-request
        attribute; if this value is not NoneType, the credentials
        corresponding to the respective string must live beneath the
        ~/.aws/credentials path and contain the appropriate AWS
        aws_access_key_id and aws_secret_access_key attributes.

    Returns
    -------

    awspath_list: list

        A Python list containing the contents of the specified AWS
        resource bucket and object path.

    Raises
    ------

    AWSCLIInterfaceError:

        * raised if an exception is encountered while creating the
          list of files within the specified AWS resource bucket and
          object path.

    """

    # Establish the AWS CLI executable environment.
    awscli = _check_awscli_env()
    cmd = [f"{awscli}", f"{resource}", "ls", f"{aws_path}"]

    # Determine the permission attributes for the AWS CLI executable.
    if profile is None:
        cmd.append("--no-sign-request")
    if profile is not None:
        cmd.append("--profile")
        cmd.append(f"{profile}")

    # Create a list of the contents in the specified AWS resource
    # path; proceed accordingly.
    try:

        # Collect a list of the AWS resource path contents.
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (path_list, _) = proc.communicate()
        proc.wait()

        # Build a list of the respective files; encode and decode as
        # necessary and proceed accordingly.
        awspath_list = []
        try:

            # Update the list with the respective file; format
            # accordingly.
            for item in path_list.split("\n".encode()):
                awspath_list.append(str(item.split()[3].decode("utf-8")))

        except IndexError:
            pass

    except Exception as errmsg:
        msg = (
            f"Determining the files in AWS path {aws_path} for AWS "
            f"resource {resource} failed with error {errmsg}. Aborting!!!"
        )
        raise AWSCLIInterfaceError(msg=msg) from errmsg

    return awspath_list


# ----


def put_awsfile(
    aws_path: str,
    path: str,
    is_dir: bool = False,
    is_wildcards: bool = False,
    aws_exclude: str = None,
    aws_include: str = None,
    resource: str = "s3",
    profile: str = None,
    errlog: str = None,
    outlog: str = None,
) -> None:
    """
    Description
    -----------

    This function provides an interface to the Amazon Web Services
    (AWS) command line interface (CLI) application to stage local
    files within specified AWS resource bucket and object paths.

    Parameters
    ----------

    aws_path: str

        A Python string specifying the AWS resource bucket and object
        path for the staged file.

    path: str

        A Python string specifying the path for the local file to be
        staged within the specified AWS resource bucket and object
        path (see aws_path above).

    Keywords
    --------

    is_dir: bool, optional

        A Python boolean valued variable specifying whether the local
        file path (see path above) is a directory; if True, the
        --recursive attribute will be invoked for the AWS CLI
        application.

    is_wildcards: bool, optional

        A Python boolean valued variable specifying whether strings
        with wild cards are to be included for the AWS CLI
        application; if True, at least aws_exclude and/or aws_include
        must not be NoneType.

    aws_exclude: str, optional

        A Python string specifying the file strings to be excluded;
        utilized only if is_wildcards (above) is True.

    aws_include: str, optional

        A Python string specifying the file strings to be included;
        utilized only if is_wildcards (above) is True.

    resource: str, optional

        A Python string specifying the supported AWS resource;
        allowable storage resources can be found at
        https://tinyurl.com/AWS-Storage-Resources.

    profile: str, optional

        A Python string specifying the AWS CLI credentials; if
        NoneType upon entry the AWS CLI assumes the --no-sign-request
        attribute; if this value is not NoneType, the credentials
        corresponding to the respective string must live beneath the
        ~/.aws/credentials path and contain the appropriate AWS
        aws_access_key_id and aws_secret_access_key attributes.

    errlog: str, optional

        A Python string specifying the path to which the AWS CLI
        application stderr should be written; if NoneType, the stderr
        is written to subprocess.PIPE.

    outlog: str, optional

        A Python string specifying the path to which the AWS CLI
        application stdout should be written; if NoneType, the stdout
        is written to subprocess.PIPE.

    Raises
    ------

    AWSCLIInterfaceError:

        * raised if the parameter values specified upon entry are
          non-compliant with the wildcards attribute.

        * raised if an exception is countered for the AWS CLI
          application.

    """

    # Establish the AWS CLI executable environment.
    awscli = _check_awscli_env()

    # Define the Python dictionaries and list of parameter keys and
    # values provided upon entry.
    aws_kwargs_list = ["aws_exclude", "aws_include", "is_dir", "is_wildcards"]

    aws_kwargs_dict = {"aws_exclude": "exclude", "aws_include": "include"}

    # Define the keywords provided upon entry and proceed accordingly.
    aws_obj = parser_interface.object_define()
    for aws_kwarg in aws_kwargs_list:
        value = literal_eval(aws_kwarg)
        aws_obj = parser_interface.object_setattr(
            object_in=aws_obj, key=aws_kwarg, value=value
        )

    # Check that the associated keywords provided upon entry are
    # valid.
    if aws_obj.is_wildcards:
        if not any([aws_obj.aws_exclude, aws_obj.aws_include]):
            msg = (
                "For AWS resource wildcard strings to be valid, either/"
                "aws_exclude and/or aws_include must not be "
                "NoneType. Aborting!!!"
            )
            raise AWSCLIInterfaceError(msg=msg)

    if not aws_obj.is_wildcards:
        for item in ["aws_exclude", "aws_include"]:

            if parser_interface.object_getattr(object_in=aws_obj, key=item) is not None:

                # Reset the value for the wildcard related keyword
                # values.
                msg = (
                    f"The keyword {item} had a value of {0} upon "
                    "entry; wildcards are not supported by the "
                    "parameters provided upon entry; resetting to "
                    "NoneType.".format(
                        parser_interface.object_getattr(
                            object_in=aws_obj, key=item),
                    )
                )
                logger.warn(msg=msg)
                aws_obj = parser_interface.object_setattr(
                    object_in=aws_obj, key=item, value=None
                )

    # Build the AWS CLI command line string and proceed accordingly.
    cmd = [f"{awscli}", f"{resource}", "cp"]

    if aws_obj.is_dir:
        cmd.append("--recursive")

    # Establish the keyword arguments for the AWS CLI executable
    # relative to the parameter values provided upon entry.
    for aws_kwarg in aws_kwargs_list:

        # Define the appropriate variable value attributes; proceed
        # accordingly.
        if aws_kwarg in list(aws_kwargs_dict.items()[0]):
            strval = parser_interface.dict_key_value(
                dict_in=aws_kwargs_dict, key=aws_kwarg, no_split=True
            )
            value = parser_interface.object_getattr(
                object_in=aws_obj, key=aws_kwarg)

            # Check that the keyword argument value is not NoneType;
            # proceed accordingly.
            if value is not None:
                if isinstance(value, str):
                    cmd.append(f'{strval} "{value}"')
                if not isinstance(value, str):
                    cmd.append(f"{strval} {value}")

    # Add the local and AWS resource file paths for the AWS CLI
    # executable application.
    cmd.append(f"{path}")
    cmd.append(f"{aws_path}")

    # Determine the permission attributes for the AWS CLI executable.
    if profile is None:
        cmd.append("--no-sign-request")
    if profile is not None:
        cmd.append("--profile")
        cmd.append(f"{profile}")

    # Check the subprocess stderr and stdout attributes provided upon
    # entry; proceed accordingly.
    if errlog is None:
        stderr = subprocess.PIPE
    if errlog is not None:
        msg = f"The stderr from the AWS CLI application will be written to {errlog}."
        logger.warn(msg=msg)
        stderr = open(errlog, "w", encoding="utf-8")

    if outlog is None:
        stdout = subprocess.PIPE
    if outlog is not None:
        msg = f"The stdout from the AWS CLI application will be written to {outlog}."
        logger.warn(msg=msg)
        stdout = open(outlog, "w", encoding="utf-8")

    # Upload the local file path to the AWS resource bucket and object
    # path; proceed accordingly.
    msg = f"Uploading files from path {path} to AWS {resource} path {aws_path}."
    logger.info(msg=msg)
    try:
        proc = subprocess.Popen(cmd, stdout=stdout, stderr=stderr)
        proc.communicate()
        proc.wait()

    except Exception as errmsg:
        msg = f"The AWS CLI application failed with error {errmsg}. Aborting!!!"
        raise AWSCLIInterfaceError(msg=msg) from errmsg

    # Check the subprocess stderr and stdout attributes; proceed
    # accordingly.
    if errlog is not None:
        stderr.close()

    if outlog is not None:
        stdout.close()
