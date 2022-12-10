# =========================================================================

# Module: launch/container_interface.py

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

Requirements
------------

- docker; https://github.com/docker

- golang; https://github.com/golang/go

- singularity; https://github.com/sylabs/singularity

Author(s)
---------

    Henry R. Winterbottom; 09 December 2022

History
-------

    2022-12-09: Henry Winterbottom -- Initial implementation.

"""

# ----


# ----

import os
import subprocesss

from utils.error_interface import Error
from utils.logger_interface import Logger
from tools import parser_interface

# ----

# Define all available functions.
__all__ = [
    "build_from_docker"
]

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

logger = Logger()

# ----


class SingularityError(Error):
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

        Creates a new Singularity Error object.

        """
        super().__init__(msg=msg)

# ----


def _check_docker_env() -> str:
    """ """

    cmd = [
        'which',
        'docker'
    ]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if len(out) > 0:
        docker = out.rstrip().decode("utf-8")

    else:

        msg = ('The Docker application could not be determined; '
               'either install the application or if it is already install, '
               'update the runtime PATH environment variable. Aborting!!!')
        raise SingularityError(msg=msg)

    return docker

# ----


def _check_singularity_env() -> str:
    """ """

    cmd = [
        'which',
        'singularity'
    ]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if len(out) > 0:
        singularity = out.rstrip().decode("utf-8")

    else:

        msg = ('The singularity application could not be determined; '
               'either install the application or if it is already install, '
               'update the runtime PATH environment variable. Aborting!!!')
        raise SingularityError(msg=msg)

    return singularity


# ----

def build_sfd(build_dict: dict) -> None:
    """
    Description
    -----------

    This method builds a Singularity image from am exiting Docker
    containerized image using the attributes provided upon entry.

    Parameters
    ----------

    build_dict: dict

        A Python dictionary containing the attributes necessary to
        build a Singularity image from an existing Docker
        containerized image.

    """

    # Define the attributes and the respective default values required
    # to build the Singularity image from the respective Docker
    # containerized image.
    sfd_attrs_dict = {'sif_name': None,
                      'sif_owner': None,
                      'docker_tag': 'latest',
                      'docker_image': None
                      }

    # Define the mandatory attributes required to build the
    # Singularity image.
    sfd_manattrs_list = ['sif_name',
                         'docker_image'
                         ]

    # Parse the attributes provided upon entry and proceed
    # accordingly.
    # HERE

    # Establish the respective platform singularity application
    # executable.
    singularity = _check_singularity_env()

    # Build the Singularity image locally.
    cmd = [f'{singularity}',
           '-f'

           ]
