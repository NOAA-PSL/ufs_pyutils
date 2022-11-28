"""
Module
------  

   __init__.py

Description
-----------

   This module loads the produtil package.

Author(s)
---------

   Henry R. Winterbottom; 07 January 2022

History
-------

   2022-01-07: Henry Winterbottom -- Initial implementation.

"""

# ----

__author__ = "Henry R. Winterbottom"
__version__ = "1.0.0"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"
__status__ = "Development"

# ----

module_list = ['error_interface', 'logger_interface']
__all__ = module_list
from produtil import *
