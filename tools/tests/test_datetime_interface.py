# =========================================================================

# Module: tools/tests/test_datetime_interface.py

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

    test_datetime_interface.py

Description
-----------

    The following unit tests contain functions to execute and assert
    that the results for the relevant datetime_interface functions are
    correct.

Classes
-------

    TestDateTimeMethods()

        This is the base-class object for all datetime_interface
        unit-tests; it is a sub-class of TestCase.

Author(s)
---------

    Henry R. Winterbottom; 03 Deceember 2022

History
-------

    2022-12-03: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=consider-iterating-dictionary
# pylint: disable=consider-using-dict-items
# pylint: disable=undefined-variable
# pylint: disable=wrong-import-order

# ----

from tools import datetime_interface
from tools import parser_interface
from unittest import TestCase

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class TestDateTimeMethods(TestCase):
    """
    Description
    -----------

    This is the base-class object for all datetime_interface
    unit-tests; it is a sub-class of TestCase.

    """

    def setUp(self):
        """
        Description
        -----------

        This method defines the base-class attributes for all
        datetime_interface unit-tests.

        """

        # Define the message to accompany any unit-test failures.
        self.unit_test_msg = ('The unit-test for datetime_interface function {0} '
                              'failed.')

    def test_datestrcomps(self):
        """
        Description
        -----------

        This method provides a unit test for the datetime_interface
        datestrcomps function.

        """

        # Define the date and timestamp string attributes.
        datestr = '20000101065803'
        frmttyp = '%Y%m%d%H%M%S'
        date_comps_obj = datetime_interface.datestrcomps(
            datestr=datestr, frmttyp=frmttyp)
        test_dict = {'year': '2000',
                     'month': '01',
                     'day': '01',
                     'hour': '06',
                     'minute': '58',
                     'second': '03',
                     'month_name_long': 'January',
                     'month_name_short': 'Jan',
                     'weekday_long': 'Saturday',
                     'weekday_short': 'Sat',
                     'century': '1999',
                     'century_short': '19',
                     'year_short': '00',
                     'date_string': '2000-01-01_06:58:03',
                     'cycle': '20000101065803',
                     'day_of_year': '001',
                     'julian_day': 2451544.7903125,
                     'total_seconds_of_day': '25083'
                     }

        # Collect the date and timestamp attributes from the local
        # attribute; compare the values and proceed accordingly.
        for key in test_dict.keys():
            result = parser_interface.dict_key_value(dict_in=test_dict, key=key,
                                                     force=True, no_split=True)
            value = parser_interface.object_getattr(
                object_in=date_comps_obj, key=key)

            assert(result == value), (self.unit_test_msg.format('datestrcomps') +
                                      f'; date string component {key} should be {result}.')

    def test_datestrfrmt(self):
        """
        Description
        -----------

        This method provides a unit test for the datetime_interface
        datestrfrmt function.

        """

        # Define the date and timestamp attributes.
        offset_seconds = 21600
        datestr = '2000-01-01_00:00:00'
        test_dict = {datestr: {'frmttyp': '%Y%m%d%H%M%S',
                               'result': '20000101060000'
                               },
                     datestr: {'frmttyp': '%Y-%m-%d_%H:%M:%S',
                               'result': '2000-01-01_06:00:00'
                               },
                     datestr: {'frmttyp': '%Y%m%d',
                               'result': '20000101'
                               }
                     }

        # Build the date and timestamp strings and check the results;
        # proceed accordingly.
        for key in test_dict.keys():
            datestr = key
            frmttyp = parser_interface.dict_key_value(dict_in=test_dict[key],
                                                      key='frmttyp', force=True,
                                                      no_split=True)
            result = parser_interface.dict_key_value(dict_in=test_dict[key],
                                                     key='result', force=True,
                                                     no_split=True)

            outdatestr = datetime_interface.datestrfrmt(
                datestr=datestr, offset_seconds=offset_seconds, frmttyp=frmttyp)

            assert(outdatestr == result), (self.unit_test_msg.format('datestrfrmt') +
                                           f'; date string of format {frmttyp} should be {result}.')

    def test_datestrupdate(self):
        """
        Description
        -----------

        This method provides a unit test for the datetime_interface
        datestrupdate function.

        """

        # Define the date and timestamp string attributes.
        datestr = '2000-01-01_00:00:00'
        in_frmttyp = '%Y-%m-%d_%H:%M:%S'
        out_frmttyp = 'outfile.%Y%m%d%H%M%S.test'
        offset_seconds = 43200

        # Define the updated date and timestamp string; proceed
        # accordingly.
        outdatestr = datetime_interface.datestrupdate(
            datestr=datestr, in_frmttyp=in_frmttyp, out_frmttyp=out_frmttyp,
            offset_seconds=offset_seconds)
        result = 'outfile.20000101120000.test'

        assert(outdatestr == result), (self.unit_test_msg.format('datestrupdate') +
                                       f'; the updated date string should be {result}.')

    def test_elapsed_seconds(self):
        """
        Description
        -----------

        This method provides a unit test for the datetime_interface
        elapsed_seconds function.

        """

        # Define the unit-test attributes.
        start_datestr = '2000-01-01_00:00:00'
        start_frmttyp = '%Y-%m-%d_%H:%M:%S'
        stop_datestr = '20001231180000'
        stop_frmttyp = '%Y%m%d%H%M%S'

        # Define the total number of seconds within the respective
        # time interval above; proceed accordingly.
        seconds = datetime_interface.elapsed_seconds(
            start_datestr=start_datestr, start_frmttyp=start_frmttyp,
            stop_datestr=stop_datestr, stop_frmttyp=stop_frmttyp)
        result = 31600800.0

        assert(seconds == result), (self.unit_test_msg.format('elapsed_seconds') +
                                    f'; the total elapsed seconds should be {result}.')


# ----

if __name__ == '__main__':
    unittest.main()
