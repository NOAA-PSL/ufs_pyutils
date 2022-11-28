"""

"""

# ----

import os
import produtil

from produtil.error_interface import Error
from produtil.logger_interface import Logger

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__version__ = "1.0.0"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"
__status__ = "Development"

# ----

class CylcError(Error):
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

        Creates a new CylcError object.

        """
        super(CylcError, self).__init__(msg=msg)

# ----

class Cylc(object):
    """

    """
    def __init__(self, rnrexpt_obj, rnrpath_obj):
        """
        Description
        -----------

        Creates a new Cylc object.

        """
        self.logger = Logger()
        attrs_list = ['rnrexpt_obj', 'rnrpath_obj']
        for attr in attrs_list:
            kwargs = {'object_in': self, 'key': attr, 'value':
                      eval(attr)}
            self = tools.parser_interface.object_setattr(**kwargs)
        kwargs = {'object_in': self.rnrexpt_obj, 'key': 'containers'}
        self.containers_dict = tools.parser_interface.object_getattr(**kwargs)
        self.cylc_image_owner = self.singularity.owner_info()

# ----

c
