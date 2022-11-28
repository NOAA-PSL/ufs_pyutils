# =========================================================================

# $$$ MODULE DOCUMENTATION BLOCK

# UFS-RNR :: ush/tools/datetime_interface.py

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

    datetime_interface.py

Description
-----------

    This module contains functions in order to manipulate date and
    time strings as required by the system workflow.

Functions
---------

    compare_crontab(datestr, cronstr, frmttyp=None)

        This function compares the user-specified date to the a
        crontab formatted value and returns a boolean value specifying
        whether the crontab string (specifying when to execute an
        action) and user-specified date match.

    current_date(frmttyp)

        This function returns the current time (at invocation of this
        function) formatted according to the user specifications.

    datestrcomps(datestr, frmttyp=None)

        This function returns a Python object containing the user
        specified date string component values.

    datestrfrmt(datestr, offset_seconds=None, frmttyp=None) 

        This function ingests a date string of format (assuming UNIX
        convention) yyyy-mm-dd_HH:MM:SS; optional argument
        'offset_seconds' defines a new datestr relative to the user
        provided datestr and the number of seconds.

    datestrupdate(datestr, in_frmttyp, out_frmttyp,
                  offset_seconds=None)

        This function ingests a date string and an optional argument
        'offset_seconds' to define a new datestr relative to the user
        provided datestr and the number of seconds and the input and
        output date string formats; this function also permits
        non-POSIX standard time attributes, as determined by
        datestrcomps (above) and user specified template values
        (denoted between < > in the out_frmttyp parameter).

    elapsed_seconds(start_datestr, start_frmttyp, stop_datestr,
                    stop_frmttyp)

        This function computes and returns the total number of seconds
        (e.g., the difference) between two input date strings.

Requirements
------------

- croniter; https://github.com/kiorky/croniter

Author(s)
--------- 

   Henry R. Winterbottom; 07 August 2022

History
-------

   2022-08-07: Henry Winterbottom -- Initial implementation.

"""

# ----

import croniter
import datetime
import sqlite3
import time

from tools import parser_interface

# ----

# Define all available functions.
__all__ = ['compare_crontab',
           'current_date',
           'datestrcomps',
           'datestrfrmt',
           'datestrupdate',
           'elapsed_seconds'
           ]

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


def compare_crontab(datestr, cronstr, frmttyp=None):
    """
    Description
    -----------

    This function compares the user-specified date to the a crontab
    formatted value and returns a boolean value specifying whether the
    crontab string (specifying when to execute an action) and
    user-specified date match.

    Parameters
    ----------

    datestr: str 

        A Python string containing a date string.

    cronstr: str

        A Python string specifying a crontab formatted date string for
        which to perform an action.

    Keywords
    --------

    frmttyp: str, optional

        A Python string specifying the format of the timestamps string;
        this assumes UNIX convention date attribute characters.

    Returns
    -------

    crontab_match: bool

        A Python boolean valued variable specifying whether the
        crontab string (specifying when to execute an action) and
        user-specified date match.

    """

    # Compare the date string and crontab formatted datastring and
    # determine whether they match.
    if frmttyp is None:
        dateobj = datetime.datetime.strptime(datestr, '%Y-%m-%d_%H:%M:%S')
    if frmttyp is not None:
        dateobj = datetime.datetime.strptime(datestr, frmttyp)
    crontab_match = croniter.croniter.match(cronstr, dateobj)

    return crontab_match

# ----


def current_date(frmttyp):
    """
    Description
    -----------

    This function returns the current time (at invocation of this
    function) formatted according to the user specifications.

    Parameters
    ----------

    frmttyp: str

        A Python string specifying the format of the timestamps
        string; this assumes UNIX convention date attribute
        characters.

    Returns
    -------

    timestamp: str

        A Python string containing the current time (at invocation of
        this function) formatted according to the user specifications.

    """

    # Determine the timestamp corresponding to the current time upon
    # function entry.
    timestamp = datetime.datetime.fromtimestamp(time.time()).\
        strftime('{0}'.format(frmttyp))

    return timestamp

# ----


def datestrcomps(datestr, frmttyp=None):
    """
    Description
    -----------

    This function returns a Python object containing the user
    specified date string component values; the following attributes
    are returned:

    year (year)

    month of year (month)

    day of month (day)

    hour of day (hour)

    minute of hour (minute)

    second of minute (second)

    full month name (month_name_long)

    abbreviated month name (month_name_short)

    full day name (weekday_long)

    abbreviated day name (weekday_short)

    century (century)

    2-digit century (e.g., 2015 is 20; century_short)

    2-digit year (e.g., year without the century value; year_short)

    date string (date_string; formatted as %Y-%m-%d_%H:%M:%S, assuming
    the UNIX convention)

    cycle string (cycle_string; formatted as %Y%m%d%H, assuming the
    UNIX convention)

    Julian date (julian_day)

    The HH:MM:SS as the total elapsed seconds, formatted as 5-digit
    integer (total_seconds_of_day)

    The day of the year (day_of_year); begins from day 1 of respective
    year.

    Parameters
    ----------

    datestr: str 

        A Python string containing a date string.

    Keywords
    --------

    frmttyp: str, optional

        A Python string specifying the format for the input date
        string (datestr); if NoneType, a format of
        yyyy-mm-dd_HH:MM:SS, assuming the UNIX POSIX convention, is
        implied.

    Returns
    -------

    date_comps_obj: object

        A Python object containing the date string component values
        for the user specfied date string.

    """

    # Initialize the Python datetime object.
    def date_comps_obj(): return None
    if frmttyp is None:
        dateobj = datetime.datetime.strptime(datestr, '%Y-%m-%d_%H:%M:%S')
    if frmttyp is not None:
        dateobj = datetime.datetime.strptime(datestr, frmttyp)

    # Loop through timestamp attributes and append values to local
    # list.
    date_comps_dict = {'year': '%Y', 'month': '%m', 'day': '%d', 'hour': '%H',
                       'minute': '%M', 'second': '%S', 'month_name_long': '%B',
                       'month_name_short': '%b', 'century_short': '%G', 'year_short':
                       '%y', 'century': '%G', 'weekday_long': '%A', 'weekday_short':
                       '%a', 'date_string': '%Y-%m-%d_%H:%M:%S', 'cycle': '%Y%m%d%H%M%S',
                       'day_of_year': '%j'}
    for key in date_comps_dict.keys():
        value = datetime.datetime.strftime(dateobj, date_comps_dict[key])
        if key.lower() == 'century_short':
            century_list = [int(d) for d in str(value)]
            value = '{0}{1}'.format(century_list[0], century_list[1])
        date_comps_obj = parser_interface.object_setattr(
            object_in=date_comps_obj, key=key, value=value)

    # Define connect object for SQlite3 library and define the
    # timestamp values accordingly.
    connect = sqlite3.connect(':memory:')
    datestr = '{0}-{1}-{2} {3}:{4}:{5}'.format(
        parser_interface.object_getattr(object_in=date_comps_obj, key='year'),
        parser_interface.object_getattr(object_in=date_comps_obj, key='month'),
        parser_interface.object_getattr(object_in=date_comps_obj, key='day'),
        parser_interface.object_getattr(object_in=date_comps_obj, key='hour'),
        parser_interface.object_getattr(
            object_in=date_comps_obj, key='minute'),
        parser_interface.object_getattr(object_in=date_comps_obj, key='second'))

    # Collect the Julian attribute using SQLite3 and proceed
    # accordingly.
    value = list(connect.execute('select julianday("{0}")'.
                                 format(datestr)))[0][0]
    date_comps_obj = parser_interface.object_setattr(
        object_in=date_comps_obj, key='julian_day', value=value)
    x = time.strptime(datestr, '%Y-%m-%d %H:%M:%S')

    # Collect the total number of seconds of the day corresponding to
    # the respective timestamp provided upon entry.
    value = datetime.timedelta(hours=x.tm_hour, minutes=x.tm_min,
                               seconds=x.tm_sec).total_seconds()
    value = '{:05d}'.format(int(value))
    date_comps_obj = parser_interface.object_setattr(
        object_in=date_comps_obj, key='total_seconds_of_day',
        value=value)

    # Add the date and time component list corresponding to the
    # respective timestamp provided upon entry.
    comps_list = vars(date_comps_obj)
    date_comps_obj = parser_interface.object_setattr(
        object_in=date_comps_obj, key='comps_list',
        value=vars(date_comps_obj))

    return date_comps_obj

# ----


def datestrfrmt(datestr, offset_seconds=None, frmttyp=None):
    """
    Description
    -----------

    This function ingests a date string of format (assuming UNIX
    convention) yyyy-mm-dd_HH:MM:SS; optional argument
    'offset_seconds' defines a new datestr relative to the user
    provided datestr and the number of seconds.

    Parameters
    ----------

    datestr: str

        A Python string containing a date string of, assuming the UNIX
        convention yyyy-mm-dd_HH:MM:SS.

    Keywords
    --------

    offset_seconds: int, optional

        A Python integer defining the total number of offset-seconds
        relative to the datestr variable (see above) for the output
        time-stamp/date-string; the default is NoneType.

    frmttyp: str, optional

        A Python string specifying the format of the timestamps
        string; this assumes UNIX convention date attribute
        characters; if NoneType, the returned value will be formatted
        as (assuming the UNIX convention) %Y-%m-%d_%H:%M:%S.

    Returns
    -------

    outdatestr: str

        A Python string containing the appropriately formatted
        time-stamp/date-string.

    """

    # Define the specified format for the respective date and
    # timestamp provided upon entry.
    default_frmttyp = '%Y-%m-%d_%H:%M:%S'
    try:
        dateobj = datetime.datetime.strptime(datestr, '%Y%m%d%H')
    except ValueError:
        dateobj = datetime.datetime.strptime(datestr,
                                             default_frmttyp)
    if offset_seconds is not None:
        dateobj = dateobj+datetime.timedelta(0, offset_seconds)
    if frmttyp is None:
        outdatestr =\
            datetime.datetime.strftime(dateobj, default_frmttyp)
    else:
        outdatestr = datetime.datetime.strftime(dateobj, frmttyp)

    return outdatestr

# ----


def datestrupdate(datestr, in_frmttyp, out_frmttyp, offset_seconds=None):
    """
    Description
    -----------

    This function ingests a date string and an optional argument
    'offset_seconds' to define a new datestr relative to the user
    provided datestr and the number of seconds and the input and
    output date string formats; this function also permits non-POSIX
    standard time attributes, as determined by datestrcomps (above)
    and user specified template values (denoted between < > in the
    out_frmttyp parameter).

    Parameters
    ----------

    datestr: str

        A Python string containing a date string of format in_frmttyp
        (see below).

    in_frmttyp: str

        A Python string specifying the UNIX convention for the datestr
        variable upon input.

    out_frmttyp: str

        A Python string specifying the UNIX convention for the datestr
        variable upon output.

    Keywords
    --------

    offset_seconds: int, optional

        A Python integer defining the total number of offset-seconds
        relative to the datestr variable (see above) for the output
        time-stamp/date-string; the default is NoneType.

    Returns
    -------

    outdatestr: str

        A Python string containing the appropriately formatted
        time-stamp/date-string.

    """

    # Update the date and timestamp in accordance with the specified
    # arguments.
    dateobj = datetime.datetime.strptime(datestr, in_frmttyp)
    if offset_seconds is not None:
        dateobj = dateobj + datetime.timedelta(0, offset_seconds)
    outdatestr = datetime.datetime.strftime(dateobj, out_frmttyp)
    date_comps_obj = datestrcomps(datestr=datestr, frmttyp=in_frmttyp)
    comps_list = parser_interface.object_getattr(
        object_in=date_comps_obj, key='comps_list')
    for item in comps_list:
        if '<{0}>'.format(item) in outdatestr:
            time_attr = parser_interface.object_getattr(
                date_comps_obj, key=item)
            outdatestr = outdatestr.replace('<{0}>'.format(item),
                                            time_attr)

    return outdatestr

# ----


def elapsed_seconds(start_datestr, start_frmttyp, stop_datestr,
                    stop_frmttyp):
    """
    Description
    -----------

    This function computes and returns the total number of seconds
    (e.g., the difference) between two input date strings.

    Parameters
    ----------

    start_datestr: str

        A Python string containing a date string of format
        start_frmttyp (below).

    start_frmttyp: str

       A Python string specifying the UNIX convention for the
       start_datestr variable.

    stop_datestr: str

        A Python string containing a date string of format
        stop_frmttyp (below).

    stop_frmttyp: str

        A Python string specifying the UNIX convention for the
        stop_datestr variable.

    Returns
    -------

    seconds: float

        A Python float value specifying the total number of seconds
        between the two input date strings.

    """

    # Compute the total number of seconds between the specified
    # datestrings upon entry.
    start_dateobj = datetime.datetime.strptime(start_datestr,
                                               start_frmttyp)
    stop_dateobj = datetime.datetime.strptime(stop_datestr,
                                              stop_frmttyp)
    seconds = float((stop_dateobj - start_dateobj).total_seconds())

    return seconds
