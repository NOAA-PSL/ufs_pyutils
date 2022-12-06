# =========================================================================

# Module: tools/datetime_interface.py

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
    time strings as required by the caller application.

Functions
---------

    _get_dateobj(datestr, frmttyp)

        This method builds/defines and returns the Python datetime
        object relative to the attributes provided upon entry.

    compare_crontab(datestr, cronstr, frmttyp)

        This function compares the user-specified date to the a
        crontab formatted value and returns a boolean value specifying
        whether the crontab string (specifying when to execute an
        action) and user-specified date match.

    current_date(frmttyp)

        This function returns the current time (at invocation of this
        function) formatted according to the parameter values
        specified upon entry.

    datestrcomps(datestr, frmttyp=None)

        This function returns a Python object containing the user
        specified date string component values; the following
        attributes are returned:

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

        2-digit year (e.g., year without the century value;
        year_short)

        date string (date_string; formatted as %Y-%m-%d_%H:%M:%S,
        assuming the UNIX POSIX convention)

        cycle string (cycle_string; formatted as %Y%m%d%H, assuming
        the UNIX POSIX convention)

        Julian date (julian_day)

        The HH:MM:SS as the total elapsed seconds, formatted as
        5-digit integer (total_seconds_of_day)

        The day of the year (day_of_year); begins from day 1 of
        respective year.

    datestrfrmt(datestr, frmttyp, offset_seconds=None)

        This function ingests a date string of format (assuming UNIX
        POSIX convention) yyyy-mm-dd_HH:MM:SS; optional argument
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

   Henry R. Winterbottom; 03 December 2022

History
-------

   2022-12-03: Henry Winterbottom -- Initial implementation.

"""

# ----

import datetime
import time
import sqlite3
import croniter

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

def _get_dateobj(datestr: str, frmttyp: str) -> object:
    """
    Description
    -----------

    This method builds/defines and returns the Python datetime object
    relative to the attributes provided upon entry.

    Parameters
    ----------

    datestr: str

        A Python string containing a date string.

    frmttyp: str

        A Python string specifying the format of the timestamps
        string; this assumes UNIX POSIX convention date attribute
        characters.

    Returns
    -------

    dateobj: object

        A Python datetime object defined relative to the attributes
        provided upon entry.

    """

    dateobj = datetime.datetime.strptime(datestr, frmttyp)

    return dateobj

# ----


def compare_crontab(datestr: str, cronstr: str, frmttyp: str) -> bool:
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

    frmttyp: str

        A Python string specifying the format of the timestamps string;
        this assumes UNIX POSIX convention date attribute characters.

    Returns
    -------

    crontab_match: bool

        A Python boolean valued variable specifying whether the
        crontab string (specifying when to execute an action) and
        user-specified date match.

    """

    # Compare the date string and crontab formatted datastring and
    # determine whether they match.
    dateobj = _get_dateobj(datestr, frmttyp)
    crontab_match = croniter.croniter.match(cronstr, dateobj)

    return crontab_match

# ----


def current_date(frmttyp: str) -> str:
    """Description
    -----------

    This function returns the current time (at invocation of this
    function) formatted according to the parameter values specified
    upon entry.

    Parameters
    ----------

    frmttyp: str

        A Python string specifying the format of the timestamps
        string; this assumes UNIX POSIX convention date attribute
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
        strftime(f'{frmttyp}')

    return timestamp

# ----


def datestrcomps(datestr: str, frmttyp: str) -> object:
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
    the UNIX POSIX convention)

    cycle string (cycle_string; formatted as %Y%m%d%H, assuming the
    UNIX POSIX convention)

    Julian date (julian_day)

    The HH:MM:SS as the total elapsed seconds, formatted as 5-digit
    integer (total_seconds_of_day)

    The day of the year (day_of_year); begins from day 1 of respective
    year.

    Parameters
    ----------

    datestr: str

        A Python string containing a date string.

    frmttyp: str

        A Python string specifying the format for the input date
        string (datestr).

    Returns
    -------

    date_comps_obj: object

        A Python object containing the date string component values
        for the user specfied date string.

    """

    # Initialize the Python datetime objects.
    def date_comps_obj():
        return None
    dateobj = _get_dateobj(datestr, frmttyp)

    # Loop through timestamp attributes and append values to local
    # list.
    date_comps_dict = {'year': '%Y',
                       'month': '%m',
                       'day': '%d',
                       'hour': '%H',
                       'minute': '%M',
                       'second': '%S',
                       'month_name_long': '%B',
                       'month_name_short': '%b',
                       'century_short': '%G',
                       'year_short': '%y',
                       'century': '%G',
                       'weekday_long': '%A',
                       'weekday_short': '%a',
                       'date_string': '%Y-%m-%d_%H:%M:%S',
                       'cycle': '%Y%m%d%H%M%S',
                       'day_of_year': '%j'
                       }

    for (key, item) in date_comps_dict.items():
        value = datetime.datetime.strftime(dateobj, item)
        if key.lower() == 'century_short':
            century_list = [int(d) for d in str(value)]
            value = (f'{century_list[0]}{century_list[1]}')
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
    value = list(connect.execute(f'select julianday("{datestr}")'))[0][0]
    date_comps_obj = parser_interface.object_setattr(
        object_in=date_comps_obj, key='julian_day', value=value)
    timedate = time.strptime(datestr, '%Y-%m-%d %H:%M:%S')

    # Collect the total number of seconds of the day corresponding to
    # the respective timestamp provided upon entry.
    value = datetime.timedelta(hours=timedate.tm_hour, minutes=timedate.tm_min,
                               seconds=timedate.tm_sec).total_seconds()
    value = f'{int(value):05d}'  # .format(int(value))
    date_comps_obj = parser_interface.object_setattr(
        object_in=date_comps_obj, key='total_seconds_of_day',
        value=value)

    # Add the date and time component list corresponding to the
    # respective timestamp provided upon entry.
    date_comps_obj = parser_interface.object_setattr(
        object_in=date_comps_obj, key='comps_list',
        value=vars(date_comps_obj))

    return date_comps_obj

# ----


def datestrfrmt(datestr: str, frmttyp: str,
                offset_seconds: int = None) -> str:
    """
    "Description
    -----------

    This function ingests a date string and computes and returns a
    (newly/different) formatted date string; the format of the
    respective date string is defined by the frmttyp parameter
    specified upon entry; an optional keyword offset_seconds defines a
    datestr relative to the value for parameter datestr and the the
    specified number of seconds; both positive and negative values for
    offset_seconds is supported.

    Parameters
    ----------

    datestr: str

        A Python string containing a date string; the input date
        string is assumed to have format % Y-%m-%d_ % H: % M: % S assuming
        the UNIX POSIX convention.

    frmttyp: str

        A Python string specifying the format of the timestamps
        string; this assumes UNIX POSIX convention date attribute
        characters.

    Keywords
    --------

    offset_seconds: int, optional

        A Python integer defining the total number of offset-seconds
        relative to the datestr variable(see above) for the output
        time-stamp/date-string; the default is NoneType.

    Returns
    -------

    outdatestr: str

        A Python string containing the appropriately formatted
        time-stamp/date-string.

    """

    # Define the specified format for the respective date and
    # timestamp provided upon entry.
    dateobj = _get_dateobj(datestr, '%Y-%m-%d_%H:%M:%S')

    if offset_seconds is not None:
        dateobj = dateobj+datetime.timedelta(0, offset_seconds)

    outdatestr = datetime.datetime.strftime(dateobj, frmttyp)

    return outdatestr

# ----


def datestrupdate(datestr: str, in_frmttyp: str, out_frmttyp: str,
                  offset_seconds: int = None) -> str:
    """
    Description
    -----------

    This function ingests a date string and an optional argument
    'offset_seconds' to define a new datestr relative to the user
    provided datestr and the number of seconds and the input and
    output date string formats; this function also permits non-POSIX
    standard time attributes, as determined by datestrcomps(above)
    and user specified template values(denoted between < > in the
    out_frmttyp parameter).

    Parameters
    ----------

    datestr: str

        A Python string containing a date string of format in_frmttyp
        (see below).

    in_frmttyp: str

        A Python string specifying the UNIX POSIX convention for the
        datestr variable upon input.

    out_frmttyp: str

        A Python string specifying the UNIX POSIX convention for the
        datestr variable upon output.

    Keywords
    --------

    offset_seconds: int, optional

        A Python integer defining the total number of offset-seconds
        relative to the datestr variable(see above) for the output
        time-stamp/date-string; the default is NoneType.

    Returns
    -------

    outdatestr: str

        A Python string containing the appropriately formatted
        time-stamp/date-string.

    """

    # Update the date and timestamp in accordance with the specified
    # arguments.
    dateobj = _get_dateobj(datestr, in_frmttyp)

    if offset_seconds is not None:
        dateobj = dateobj + datetime.timedelta(0, offset_seconds)
    outdatestr = datetime.datetime.strftime(dateobj, out_frmttyp)
    date_comps_obj = datestrcomps(datestr=datestr, frmttyp=in_frmttyp)
    comps_list = parser_interface.object_getattr(
        object_in=date_comps_obj, key='comps_list')

    for item in comps_list:
        if f'<{item}>' in outdatestr:
            time_attr = parser_interface.object_getattr(
                date_comps_obj, key=item)
            outdatestr = outdatestr.replace(f'<{item}>', time_attr)

    return outdatestr

# ----


def elapsed_seconds(start_datestr: str, start_frmttyp: str, stop_datestr: str,
                    stop_frmttyp: str) -> float:
    """
    Description
    -----------

    This function computes and returns the total number of seconds
    (e.g., the difference) between two input date strings.

    Parameters
    ----------

    start_datestr: str

        A Python string containing a date string of format
        start_frmttyp(below).

    start_frmttyp: str

       A Python string specifying the UNIX POSIX convention for the
       start_datestr variable.

    stop_datestr: str

        A Python string containing a date string of format
        stop_frmttyp(below).

    stop_frmttyp: str

        A Python string specifying the UNIX POSIX convention for the
        stop_datestr variable.

    Returns
    -------

    seconds: float

        A Python float value specifying the total number of seconds
        between the two input date strings.

    """

    # Compute the total number of seconds between the specified
    # datestrings upon entry.
    start_dateobj = _get_dateobj(start_datestr, start_frmttyp)
    stop_dateobj = _get_dateobj(stop_datestr, stop_frmttyp)

    seconds = float((stop_dateobj - start_dateobj).total_seconds())

    return seconds
