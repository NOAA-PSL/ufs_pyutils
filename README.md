[![License](https://img.shields.io/badge/license-LGPL_v2.1-lightgray)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/blob/develop/LICENSE)
![Linux](https://img.shields.io/badge/linux-ubuntu%7Ccentos-black)
![Python Version](https://img.shields.io/badge/python-3.5|3.6|3.7-blue)
![Dependencies](https://img.shields.io/badge/dependencies-astropy_boto3_bs4_croniter_netcdf4_numpy_pyyaml_schema-orange)

[![Unit Tests](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/unittests.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/unittests.yaml)
[![Python Coding Standards](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/pycodestyle.yaml/badge.svg)](https://github.com/HenryWinterbottom-NOAA/ufs_pyutils/actions/workflows/pycodestyle.yaml)

# Disclaimer

The United States Department of Commerce (DOC) GitHub project code is
provided on an "as is" basis and the user assumes responsibility for
its use. DOC has relinquished control of the information and no longer
has responsibility to protect the integrity, confidentiality, or
availability of the information. Any claims against the Department of
Commerce stemming from the use of its GitHub project will be governed
by all applicable Federal law. Any reference to specific commercial
products, processes, or services by service mark, trademark,
manufacturer, or otherwise, does not constitute or imply their
endorsement, recommendation or favoring by the Department of
Commerce. The Department of Commerce seal and logo, or the seal and
logo of a DOC bureau, shall not be used in any manner to imply
endorsement of any commercial product or activity by DOC or the United
States Government.

# Cloning

This repository utilizes several sub-modules from various sources. To
obtain the entire system, do as follows.

~~~
user@host:$ git clone --recursive https://github.com/HenryWinterbottom-NOAA/ufs_pyutils
~~~

# Dependencies

The package dependencies and the respective repository and manual
installation attributes are provided in the table below.

<div align="center">

| Dependency Package | Installation Instructions |
| :-------------: | :-------------: | 
| [`astropy`](https://github.com/astropy/astropy) | <div align="left">`pip install astropy==5.2`</div> | 
| [`boto3`](https://github.com/boto/boto3) | <div align="left">`conda install -c anaconda boto3==1.24.28`</div> | 
| [`bs4`](https://github.com/waylan/beautifulsoup) | <div align="left">`pip install bs4==0.0.1`</div> | 
| [`croniter`](https://github.com/kiorky/croniter) | <div align="left">`pip install croniter==1.3.8`</div> | 
| [`netcdf4`](https://github.com/Unidata/netcdf4-python) | <div align="left">`pip install netcdf4==1.6.2`</div> |
| [`numpy`](https://github.com/numpy/numpy) | <div align="left">`pip install numpy==1.22.4`</div> |
| [`pyyaml`](https://github.com/yaml/pyyaml) | <div align="left">`conda install -c anaconda pyyaml==6.0`</div> |
| [`schema`](https://github.com/keleshev/schema) | <div align="left">`pip install schema==0.7.5`</div> | 

</div>

# Building and Installing

In order to install via the Python setup applications, do as follows.

~~~
user@host:$ cd ufs_pyutils
user@host:$ python setup.py build
user@host:$ python setup.py install
~~~

For additional information and options for building Python packages, see [here](https://docs.python.org/3.5/distutils/setupscript.html)

# Forking

If a user wishes to contribute modifications done within their
respective fork(s) to the authoritative repository, we request that
the user first submit an issue and that the fork naming conventions
follow those listed below.

- `docs/user_fork_name`: Documentation additions and/or corrections for the application(s).

- `feature/user_fork_name`: Additions, enhancements, and/or upgrades for the application(s).

- `fix/user_fork_name`: Bug-type fixes for the application(s) that do not require immediate attention.

- `hotfix/user_fork_name`: Bug-type fixes which require immediate attention to fix issues that compromise the integrity of the respective application(s).  