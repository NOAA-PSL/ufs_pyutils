# =========================================================================

# Module: setup.py

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
Script
------

    setup.py

Description
-----------

    This script will attempt to build the UFS Python utilties
    application package.

Functions
---------

    setup(name, version, description, author, author_email, url,
          license, classifiers, install_requires)

        This function provides the interface to the Python setuptools
        setup application; all parameters are specific to the
        respective application.

Author(s)
---------

    Henry R. Winterbottom; 03 December 2022

History
-------

    2022-12-03: Henry Winterbottom -- Initial implementation.

"""

# ----

from setuptools import setup

# ----

# Define the package attributes.
AUTHOR = 'Henry R. Winterbottom'
AUTHOR_EMAIL = 'henry.winterbottom@noaa.gov'
LICENSE = "License :: OSI Approved :: LGPL-2.0 License"
NAME = 'ufs_pyutils'
URL = 'https://github.com/HenryWinterbottom-NOAA/ufs_pytils'
VERSION = '0.0.0'

DESCRIPTION = "Unified Forecast System Python utilities package."

classifiers = [f"Development Status :: Version {VERSION}",
               "Programming Language :: Python :: >= 3.5",
               "Intended Audience :: Science/Research",
               "License :: OSI Approved :: LGPL-2.0 License",
               "Topic :: Software Development :: Libraries :: Python Modules"]

# ----

# Define the package dependencies.
install_requires = ["astropy==5.2", "boto3==1.24.28", "bs4==0.0.1", "croniter==1.3.8",
                    "netcdf4==1.6.2", "numpy==1.22.4", "pytest==7.2.0",
                    "pytest-order==1.0.1", "pyyaml==6.0"]

# ----

# This function provides the interface to the Python setuptools setup
# application; all parameters are specific to the respective
# application.

# Install and build the package dependencies and the respective
# package.
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=LICENSE,
    classifiers=classifiers,
    install_requires=install_requires,
)
