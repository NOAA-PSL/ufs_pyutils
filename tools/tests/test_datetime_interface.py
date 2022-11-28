# =========================================================================

# $$$ UNIT TEST DOCUMENTATION BLOCK

# UFS-RNR :: ush/tools/tests/test_datetime_interface.py

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
Tests
-----

    test_datetime_interface.py

Description
-----------

    The following unit tests contain functions to execute and assert
    that the results for the relevant datetime_interface functions are
    correct.

Functions
---------

    test_datestrcomps()

        This method provides a unit test for the
        datetime_interface.datestrcomps function.

    test_datestrfrmt()

        This method provides a unit test for the
        datetime_interface.datestrfrmt function.

    test_datestrupdate()

        This method provides a unit test for the
        datetime_interface.datestrupdate function.

    test_elapsed_seconds()

        This method provides a unit test for the
        datetime_interface.elapsed_seconds function.

Author(s)
---------

    Henry R. Winterbottom; 01 September 2022

History
-------

    2022-06-29: Henry Winterbottom -- Initial implementation.

"""

# ----

from tools import datetime_interface
from tools import parser_interface

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


def test_datestrcomps():
    """
    Description
    -----------

    This method provides a unit test for the
    datetime_interface.datestrcomps function.

    """

    # Define the unit-test attributes.
    datestr = '20000101065803'
    frmttyp = '%Y%m%d%H%M%S'
    date_comps_obj = datetime_interface.datestrcomps(
        datestr=datestr, frmttyp=frmttyp)
    test_dict = {'year': '2000', 'month': '01', 'day': '01', 'hour': '06',
                 'minute': '58', 'second': '03', 'month_name_long': 'January',
                 'month_name_short': 'Jan', 'weekday_long': 'Saturday',
                 'weekday_short': 'Sat', 'century': '1999', 'century_short':
                 '19', 'year_short': '00', 'date_string': '2000-01-01_06:58:03',
                 'cycle': '20000101065803', 'day_of_year': '001', 'julian_day':
                 2451544.7903125, 'total_seconds_of_day': '25083'}

    # Execute the unit-test.
    for key in test_dict.keys():
        result = parser_interface.dict_key_value(dict_in=test_dict, key=key,
                                                 force=True, no_split=True)
        value = parser_interface.object_getattr(
            object_in=date_comps_obj, key=key)

        assert(result == value), 'Date string component {0} should be {1}.'.format(
            key, result)

# ----


def test_datestrfrmt():
    """
    Description
    -----------

    This method provides a unit test for the
    datetime_interface.datestrfrmt function.

    """

    # Define the unit-test attributes.
    offset_seconds = 21600
    test_dict = {'20000101000000': {'frmttyp': '%Y%m%d%H%M%S',
                                    'result': '20000101060000'
                                    },
                 '2000-01-01_00:00:00': {'frmttyp': '%Y-%m-%d_%H:%M:%S',
                                         'result': '2000-01-01_06:00:00'
                                         }
                 }

    # Execute the unit-test.
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

        assert(outdatestr == result), 'Date string of format {0} should be {1}.'.format(
            frmttyp, result)

# ----


def test_datestrupdate():
    """
    Description
    -----------

    This method provides a unit test for the
    datetime_interface.datestrupdate function.

    """

    # Define the unit-test attributes.
    datestr = '2000-01-01_00:00:00'
    in_frmttyp = '%Y-%m-%d_%H:%M:%S'
    out_frmttyp = 'outfile.%Y%m%d%H%M%S.test'
    offset_seconds = 43200

    # Execute the unit-test.
    outdatestr = datetime_interface.datestrupdate(
        datestr=datestr, in_frmttyp=in_frmttyp, out_frmttyp=out_frmttyp,
        offset_seconds=offset_seconds)
    result = 'outfile.20000101120000.test'

    assert(outdatestr == result), 'Updated date string should be {0}.'.format(
        result)

# ----


def test_elapsed_seconds():
    """
    Description
    -----------

    This method provides a unit test for the
    datetime_interface.elapsed_seconds function.

    """

    # Define the unit-test attributes.
    start_datestr = '2000-01-01_00:00:00'
    start_frmttyp = '%Y-%m-%d_%H:%M:%S'
    stop_datestr = '20001231180000'
    stop_frmttyp = '%Y%m%d%H%M%S'

    # Execute the unit-test.
    seconds = datetime_interface.elapsed_seconds(
        start_datestr=start_datestr, start_frmttyp=start_frmttyp,
        stop_datestr=stop_datestr, stop_frmttyp=stop_frmttyp)
    result = 31600800.0

    assert(seconds == result), 'The total elapsed seconds should be {0}.'.format(
        result)
