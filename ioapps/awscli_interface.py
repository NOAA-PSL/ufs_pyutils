#!/usr/bin/env python3

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
    Services (AWS) command-line interface (CLI) for AWS s3 bucket and
    object paths.

Classes
------- 

    AWSCLIError(msg)

        This is the base-class for all exceptions; it is a sub-class
        of Error.

Functions
---------

    _check_awscli_env()

        This function checks whether the AWS CLI environment has been
        loaded; if not, an AWSCLIError will be thrown; if so, the path
        to the AWS CLI executable will be defined and returned.

    put_awsfile(aws_path, path, is_dir=False, is_wildcards=False,
                aws_exclude=None, aws_include=None, profile=None,
                errlog=None, outlog=None):

        This function provides an interface to the Amazona Web
        Services (AWS) command line interface (CLI) application to
        stage local files within specified AWS s3 bucket and object
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

import subprocess

from utils.error_interface import Error
from utils.logger_interface import Logger
from tools import parser_interface

# ----

# Define all available functions.
__all__ = ['put_awsfile'
           ]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class AWSCLIError(Error):
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

    def __init__(self, msg: str):
        """
        Description
        -----------

        Creates a new AWSCLIError object.

        """
        super(AWSCLIError, self).__init__(msg=msg)

# ----


def _check_awscli_env() -> str:
    """
    Description
    -----------

    This function checks whether the AWS CLI environment has been
    loaded; if not, an AWSCLIError will be thrown; if so, the path to
    the AWS CLI executable will be defined and returned.

    Returns
    -------

    awscli: str

        A Python string specifying the path to the AWS CLI executable.

    Raises
    ------

    AWSCLIError:

        * raised if the AWS CLI executable path cannot be determined.

    """

    # Check the run-time environment in order to determine the AWS CLI
    # executable path.
    cmd = ['which',
           'aws'
           ]

    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = proc.communicate()

    # Define the AWS CLI executable path; proceed accordingly.
    if len(out) > 0:
        awscli = out.rstrip().decode('utf-8')

    else:
        msg = ('The AWS CLI executable could not be determined for your '
               'system; please check that the appropriate AWS CLI '
               'libaries/modules are loaded prior to calling this script. '
               'Aborting!!!')
        raise AWSCLIError(msg=msg)

    return awscli

# ----


def put_awsfile(aws_path: str, path: str, is_dir: bool = False,
                is_wildcards: bool = False, aws_exclude: str = None,
                aws_include: str = None, profile: str = None,
                errlog: str = None, outlog: str = None):
    """
    Description
    -----------

    This function provides an interface to the Amazona Web Services
    (AWS) command line interface (CLI) application to stage local
    files within specified AWS s3 bucket and object paths.

    Parameters
    ----------

    aws_path: str

        A Python string specifying the AWS s3 bucket and object path
        for the staged file.

    path: str

        A Python string specifying the path for the local file to be
        staged within the specified AWS s3 bucket and object path (see
        aws_path above).

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

    AWSCLIError:

        * raised if the parameter values specified upon entry are
          non-compliant with the wildcards attribute.

        * raised if an exception is countered for the AWS CLI
          application.

    """

    # Establish the AWS CLI executable environment.
    awscli = _check_awscli_env()

    # Define the Python dictionaries and list of parameter keys and
    # values provided upon entry.
    awss3_kwargs_list = ['aws_exclude',
                         'aws_include',
                         'is_dir',
                         'is_wildcards'
                         ]

    awss3_kwargs_dict = {'aws_exclude': 'exclude',
                         'aws_include': 'include'
                         }

    # Define the keywords provided upon entry and proceed accordingly.
    awss3_obj = parser_interface.object_define()
    for awss3_kwarg in awss3_kwargs_list:
        value = eval(awss3_kwarg)
        awss3_obj = parser_interface.object_setattr(
            object_in=awss3_obj, key=awss3_kwarg, value=value)

    # Check that the associated keywords provided upon entry are
    # valid.
    if awss3_obj.is_wildcards:
        if not any([awss3_obj.aws_exclude, awss3_obj.aws_include]):
            msg = ('For AWS s3 wildcard strings to be valid, either/'
                   'aws_exclude and/or aws_include must not be '
                   'NoneType. Aborting!!!')
            raise AWSCLIError(msg=msg)

    if not awss3_obj.is_wildcards:
        for item in ['aws_exclude',
                     'aws_include'
                     ]:

            if parser_interface.object_getattr(
                    object_in=awss3_obj, key=item) is not None:

                # Reset the value for the wildcard related keyword
                # values.
                msg = ('The keyword {0} had a value of {1} upon '
                       'entry; wildcards are not supported by the '
                       'parameters provided upon entry; resetting to '
                       'NoneType.'.format(item, parser_interface.object_getattr(
                           object_in=awss3_obj, key=item)))
                logger.warn(msg=msg)
                awss3_obj = parser_interface.object_setattr(
                    object_in=awss3_obj, key=item, value=None)

    # Build the AWS CLI command line string and proceed accordingly.
    cmd = ['{0}'.format(awscli),
           's3',
           'cp'
           ]

    if awss3_obj.is_dir:
        cmd.append('--recursive')

    # Establish the keyword arguments for the AWS CLI executable
    # relative to the parameter values provided upon entry.
    for awss3_kwarg in awss3_kwargs_list:

        # Define the appropriate variable value attributes; proceed
        # accordingly.
        if awss3_kwarg in list(awss3_kwargs_dict.keys()):
            strval = parser_interface.dict_key_value(
                dict_in=awss3_kwargs_dict, key=awss3_kwarg, no_split=True)
            value = parser_interface.object_getattr(
                object_in=awss3_obj, key=awss3_kwarg)

            # Check that the keyword argument value is not NoneType;
            # proceed accordingly.
            if value is not None:
                if isinstance(value, str):
                    cmd.append('{0} "{1}"'.format(strval, value))
                if not isinstance(value, str):
                    cmd.append('{0} {1}'.format(strval, value))

    # Add the local and AWS s3 file paths for the AWS CLI executable
    # application.
    cmd.append('{0}'.format(path))
    cmd.append('{0}'.format(aws_path))

    # Determine the permission attributes for the AWS CLI executable.
    if profile is None:
        cmd.append('--no-sign-request')
    if profile is not None:
        cmd.append('--profile')
        cmd.append('{0}'.format(profile))

    # Check the subprocess stderr and stdout attributes provided upon
    # entry; proceed accordingly.
    if errlog is None:
        stderr = subprocess.PIPE
    if errlog is not None:
        msg = ('The stderr from the AWS CLI application will be written '
               'to {0}.'.format(errlog))
        logger.warn(msg=msg)
        stderr = open(errlog, 'w')

    if outlog is None:
        stdout = subprocess.PIPE
    if outlog is not None:
        msg = ('The stdout from the AWS CLI application will be written '
               'to {0}.'.format(outlog))
        logger.warn(msg=msg)
        stdout = open(outlog, 'w')

    # Upload the local file path to the AWS s3 bucket and object path;
    # proceed accordingly.
    msg = ('Uploading files from path {0} to AWS s3 path {1}.'
           .format(path, aws_path))
    logger.info(msg=msg)
    try:
        proc = subprocess.Popen(cmd, stdout=stdout, stderr=stderr)
        proc.communicate()
        proc.wait()

    except Exception as error:
        msg = ('The AWS CLI application failed with error {0}. '
               'Aborting!!!'.format(error))
        raise AWSCLIError(msg=msg)

    # Check the subprocess stderr and stdout attributes; proceed
    # accordingly.
    if errlog is not None:
        stderr.close()
    if outlog is not None:
        stdout.close()
