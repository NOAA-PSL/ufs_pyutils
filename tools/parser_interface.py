# =========================================================================

# $$$ MODULE DOCUMENTATION BLOCK

# UFS-RNR :: ush/tools/parser_interface.py

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

    parser_interface.py

Description
-----------

    This module contains functions to perform various tasks which
    involve the parsing of dictionaries, lists, and other Python type
    comprehensions.

Classes
-------

    ParserInterfaceError(msg)

        This is the base-class for all exceptions; it is a sub-class
        of Error.

Functions
---------

    dict_formatter(in_dict)

        This function formats a Python dictionary; all UNICODE and
        data-type conversions are performed within this function.

    dict_key_remove(dict_in, key):

        This function attempts to remove a Python dictionary key and
        value pair.

    dict_key_value(dict_in, key, force=False, max_value=False,
                   min_value=False, index_value=None, no_split=False)

        This function ingests a Python dictionary and a dictionary key
        and return the value(s) corresponding to the respective
        dictionary key; if the optional variable 'force' is True and
        the dictionary key does not exist within the Python
        dictionary, the function will return NoneType.

    enviro_get(envvar)

        This function retrieves the environment variable corresponding
        to the user specified string; if the environment variable is
        not defined, NoneType is returned.

    enviro_set(envvar, value)

        This function defines the environment variable corresponding to
        the user specified string.

    find_commonprefix(strings_list)

        This function returns the common prefix from a list of strings.

    list_get_type(in_list, dtype):

        This function parses a list and returns a list of values in
        accordance with the specified data type.

    match_list(in_list, match_string, exact=False):

        This function ingests a Python list and a Python string and
        matches, either exact or partial, are sought for the string
        within the provided list and a tuple of values is returned; if
        exact='True', a Python string is returned if a match is found
        (i.e., match_chk=True) or 'None' if no match is found; if
        exact='False', a list of Python strings if matches are found
        (i.e., match_chk=True).

    object_append(object_in, object_key, dict_in):

        This function appends the contents of Python dictionary to user
        specified object key.

    object_compare(obj1, obj2)

        This function compares two Python objects.

    object_deepcopy(object_in):

        This function ingests a Python object and returns a deep copy of
        the respective object.

    object_define()

        This function defines an empty Python object.

    object_getattr(object_in, key, force=False)

        This function ingests a Python object and a Python attribute and
        returns the value of the respective attribute; if force is
        True and the Python object attribute does not exist, this
        function returns NoneType; if force is False and the Python
        object attribute does not exist, this function raises an
        ParserInterfaceError exception.

    object_hasattr(object_in, key)

        This function checks whether a Python object contains an
        attribute and returns an appropriate boolean value indicating
        the result of the inquiry.

    object_setattr(object_in, key, value)

        This function ingests a Python object and a Python key and value
        pair and defines the attributes for the respective object.

    object_todict(object_in)

        This function ingests a Python object and returns a Python
        dictionary containing the contents of the respective object.

    sanitize_list(list_in, list_id):

        This function modifies/rearranges items in a list in accordance
        with the user specifications.

    single_true(bool_list)

        This function ingests a list of boolean (e.g., logical)
        variables (bool_list) and returns True if a single true value
        is in the boolean list or False otherwise.

    string_parser(in_list)

        This function ingests a Python list of variables and returns
        Python list of appropriately formatted values.

    true_or_false(argval) 

        This function checks whether an argument is a Boolean-type
        value; if so, this function defines the appropriate Python
        boolean-type; otherwise, this function returns NoneType.

    unique_list(in_list)

        This function ingests a list, possibly with duplicate values,
        and returns a list of only unique values.

Author(s)
--------- 

    Henry R. Winterbottom; 21 August 2022

History
-------

    2022-08-21: Henry Winterbottom -- Initial implementation.

"""

# ----

import collections
import copy
import numpy
import os
import sys
import types

from utils.error_interface import Error

# ----

# Define all available functions.
__all__ = ['dict_formatter',
           'dict_key_remove',
           'dict_key_value',
           'enviro_get',
           'enviro_set',
           'find_commonprefix',
           'list_get_type',
           'match_list',
           'object_append',
           'object_compare',
           'object_deepcopy',
           'object_define',
           'object_getattr',
           'object_hasattr',
           'object_setattr',
           'object_todict',
           'sanitize_list',
           'single_true',
           'string_parser',
           'true_or_false',
           'unique_list'
           ]

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class ParserInterfaceError(Error):
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

    def __init__(self, msg):
        """
        Description
        -----------

        Creates a new ParserInterfaceError object.

        """
        super(ParserInterfaceError, self).__init__(msg=msg)

# ----


def dict_formatter(in_dict):
    """
    Description
    -----------

    This function formats a Python dictionary; all UNICODE and
    data-type conversions are performed within this function.

    Parameters
    ----------

    in_dict: dict 

        A standalone Python dictionary to be formatted.

    Returns
    -------

    out_dict: dict

        A standalone Python dictionary which has been formatted.

    """

    # Define local function to sort and format the input Python
    # dictionary upon entry.
    def sorted_by_keys(dct,):
        new_dct = collections.OrderedDict()
        for key, value in sorted(dct.items(), key=lambda key: key):

            # Check the Python version and proceed accordingly.
            if sys.version_info < (3, 0, 0):
                if isinstance(value, unicode):
                    value = value.encode('ascii', 'ignore')
                if isinstance(key, unicode):
                    key = key.encode('ascii', 'ignore')

            # Write the key and value pair for the output dictionary.
            if isinstance(value, dict):
                new_dct[key] = sorted_by_keys(value)
            else:

                # Check the Python version and proceed accordingly.
                if sys.version_info < (3, 0, 0):
                    if isinstance(key, unicode):
                        key = key.encode('ascii', 'ignore')
                    if isinstance(value, unicode):
                        value = value.encode('ascii', 'ignore')
                test_value = value

                # Check if the key and value pair is a boolean type
                # argument and proceed accordingly.
                if isinstance(test_value, bool):
                    if test_value:
                        value = True
                    if not test_value:
                        value = False

                # Check if the key and value pair is a string type
                # argument and proceed accordingly.
                if isinstance(test_value, str):
                    try:
                        dummy = float(test_value)
                        if '.' in test_value:
                            value = float(test_value)
                        else:
                            value = int(test_value)
                    except ValueError:
                        if test_value.lower() == 'none':
                            value = None
                        elif test_value.lower() == 'true':
                            value = True
                        elif test_value.lower() == 'false':
                            value = False
                        else:
                            value = str(test_value)

                # Update the output dictionary key and value pair.
                new_dct[key] = value
        return new_dct

    # Define the formatted output dictionary.
    out_dict = sorted_by_keys(dct=in_dict)
    return out_dict

# ----


def dict_key_remove(dict_in, key):
    """
    Description
    -----------

    This function attempts to remove a Python dictionary key and value
    pair.

    Parameters
    ----------

    dict_in: dict

        A Python dictionary to be parsed.

    key: str

        A Python string indicating the dictionary key within the
        Python dictionary (see above).

    Returns
    -------

    dict_in: dict

        A Python dictionary from which the specified key and value
        pair has been removed (if present in the Python dictionary on
        entry).

    """

    # Attempt to remove the dictionary value corresponding to the key
    # specified upon entry.
    try:
        del dict_in[key]
    except KeyError:
        pass
    return dict_in

# ----


def dict_key_value(dict_in, key, force=False, max_value=False, min_value=False,
                   index_value=None, no_split=False):
    """
    Description
    -----------

    This function ingests a Python dictionary and a dictionary key and
    return the value(s) corresponding to the respective dictionary
    key; if the optional variable 'force' is True and the dictionary
    key does not exist within the Python dictionary, the function will
    return NoneType.

    Parameters
    ----------

    dict_in: dict

        A Python dictionary to be parsed.

    key: str

        A Python string indicating the dictionary key within the
        Python dictionary (see above).

    force: str, optional

        A Python boolean variable; if True and in the absence of the
        respective dictionary key within the Python dictionary,
        NoneType is returned.

    max_value: bool, optional

        A Python boolean variable; if True, and a Python list yielded
        via the Python dictionary key, the maximum value within the
        Python list will be returned; the default value is False.

    min_value: bool, optional

        A Python boolean variable; if True, and a Python list yielded
        via the Python dictionary key, the minimum value within the
        Python list will be returned; the default value is False.

    index_value: int, optional

        A Python integer defining the index within the Python list (as
        yielded by the Python dictionary key) to return; the default
        value is NoneType.

    no_split: bool, optional

        A Python boolean variable; if True and if a string, the string
        will not be split into and returned as a comma-delimited list.

    Returns
    -------

    value: list or str

        A list of values collected from the ingested Python dictionary
        and the respective dictionary key if no_split is False; a
        string otherwise.

    Raises
    ------

    ParserInterfaceError:

        * raised if both minimum and maximum values of a list are
          requested; only minimum or only maximum may be requested
          upon entry.

        * raised if the keyword argument combinations passed upon
          entry are incorrect.

    """
    if max_value and min_value:
        msg = ('The user has requested both minimum and maximum list '
               'values. Please check that only one threshold value is '
               'is to be sought from the list. Aborting!!!')
        raise ParserInterfaceError(msg=msg)
    if index_value is not None:
        if max_value:
            msg = ('The user has selected both a single value (as per '
                   'the specified index) and the maximum list value. '
                   'Please check which criteria to fulfill. Aborting!!!')
            raise ParserInterfaceError(msg=msg)
        if min_value:
            msg = ('The user has selected both a single value (as per '
                   'the specified index) and the minimum list value. '
                   'Please check which criteria to fulfill. Aborting!!!')
            raise ParserInterfaceError(msg=msg)
    try:
        value = dict_in[key]
        if no_split:
            return value
        try:
            in_list = dict_in[key].split(',')
            value = list(string_parser(in_list=in_list))
            if max_value:
                value = max(value)
            if min_value:
                value = min(value)
            if index_value is not None:
                value = value[index_value]
        except AttributeError:
            value = dict_in[key]
    except KeyError:
        if not force:
            msg = ('Key {0} could not be found in user provided dictionary. '
                   'Aborting!!!'.format(key))
            raise ParserInterfaceError(msg=msg)
        if force:
            value = None
    return value

# ----


def enviro_get(envvar):
    """
    Description
    -----------

    This function retrieves the environment variable corresponding to
    the user specified string; if the environment variable is not
    defined, NoneType is returned.

    Parameters
    ----------

    envvar: str

        A Python string specifying the environment variable name.

    Returns
    -------

    envvarval: any type

        A Python type that contains the query for the environment
        variable.

    """

    # Parse the run-time environment and return the attributes of the
    # environment variable specified upon entry.
    if envvar in os.environ:
        envvarval = os.environ.get(envvar)
    else:
        envvarval = None
    return envvarval

# ----


def enviro_set(envvar, value):
    """
    Description
    -----------

    This function defines the environment variable corresponding to
    the user specified string.

    Parameters
    ----------

    envvar: str

        A Python string specifying the environment variable name.

    value: any type

        A Python value specifying the value of the environment
        variable.

    """

    # Define the run-time environment variable.
    os.environ[envvar] = value

# ----


def find_commonprefix(strings_list):
    """
    Description
    -----------

    This function returns the common prefix from a list of strings.

    Parameters
    ----------

    strings_list: list

        A Python list of strings

    Returns
    -------

    common_prefix: str

        A Python string specifying the common prefix determined from a
        list of Python strings; NoneType if a common prefix cannot be
        determined.

    """

    # Seek common prefix values from the list of strings specified
    # upon entry.
    common_prefix = None
    if strings_list:
        common_prefix = os.path.commonprefix(strings_list)
    return common_prefix

# ----


def list_get_type(in_list, dtype):
    """
    Description
    -----------

    This function parses a list and returns a list of values in
    accordance with the specified data type.

    Parameters
    ----------

    in_list: list

        A Python list containing values possibly of various data
        types.

    dtype: str

        A Python string specifying the data type to be sought.

    Returns
    -------

    var_list: list

        A Python list contain values collected from the input list but
        of the specified data type.

    """

    # Find all items within the list specified upon entry of a
    # specified data type upon entry.
    var_list = list()
    try:
        for item in in_list:
            if type(item) is dtype:
                var_list.append(item)
    except TypeError:
        var_list.append(numpy.nan)
    return var_list

# ----


def object_append(object_in, object_key, dict_in):
    """
    Description
    -----------

    This function appends the contents of Python dictionary to user
    specified object key.

    Parameters
    ----------

    object_in: obj

        A Python object to be appended.

    object_key: str

        A Python string value specifying the input Python object
        attribute.

    dict_in: dict

        A Python dictionary containing the key and value pairs to
        append to the input Python object.

    Returns
    -------

    object_out: obj 

        An appended Python object containing the input Python
        dictionary key and value pairs relative to the user-specified
        Python object attribute.

    """

    # Define the output object and the Python dictionary in accordance
    # with the arguments provided upon entry.
    object_out = object_in
    object_dict = object_getattr(object_in=object_in, key=object_key)

    # Build the Python dictionary.
    for key in dict_in.keys():
        value = dict_key_value(dict_in=dict_in, key=key, no_split=True)
        object_dict[key] = value

    # Build the output Python object.
    object_out = object_setattr(object_in=object_out, key=object_key,
                                value=object_dict)
    return object_out

# ----


def object_compare(obj1, obj2):
    """
    Description
    -----------

    This function compares two Python objects.

    Parameters
    ----------

    obj1: obj

        A Python object against which to compare with another object.

    obj2: obj

        A Python object to compare to obj1 (above). 

    Returns
    -------

    compare: bool

        A Python boolean variable specifying whether the respective
        Python objects are identical.

    """

    # Compare the Python objects provided upon entry.
    compare = (obj1 == obj2)
    return compare

# ----


def object_deepcopy(object_in):
    """
    Description
    -----------

    This function ingests a Python object and returns a deep copy of
    the respective object.

    Parameters
    ----------

    object_in: obj

        A Python object for which to create a deep copy.

    Returns
    -------

    object_out: obj

        A Python object which is a deep copy of the user specified
        input object (e.g., object_in).

    """

    # Create and return a deep copy of the Python object provided upon
    # entry.
    object_out = copy.deepcopy(object_in)
    return object_out


# ----


def object_define():
    """ 
    Description
    -----------

    This function defines an empty Python object.

    Returns
    -------

    empty_obj: obj

        An empty Python object.

    """

    # Initialize an empty Python object/namespace.
    empty_obj = types.SimpleNamespace()
    return empty_obj

# ----


def object_getattr(object_in, key, force=False):
    """
    Description
    -----------

    This function ingests a Python object and a Python attribute and
    returns the value of the respective attribute; if force is True
    and the Python object attribute does not exist, this function
    returns NoneType.

    Parameters
    ----------

    object_in: obj

        A Python object within which to search for attributes.

    key: str

        A Python string value specifying the attribute to seek.

    force: bool, optional

        A Python boolean variable; if True and in the absence of the
        respective attribute within the Python object, NoneType is
        returned; otherwise, an ParserInterfaceError is raised.

    Returns
    -------

    value: any type

        The result of the respective attribute search.

    Raises
    ------

    ParserInterfaceError:

        * raised if force is False and the Python object attribute
          does not exist.

    """

    # Check whether the Python object passed upon entry contains the
    # key specified upon entry.
    if hasattr(object_in, key):
        value = getattr(object_in, key)

    # Return the value corresponding to the key or raise an exception
    # accordingly.
    if not hasattr(object_in, key):
        if force:
            value = None
        if not force:
            msg = ('The object {0} does not contain attribute {1}. '
                   'Aborting!!!'.format(object_in, key))
            raise ParserInterfaceError(msg=msg)
    return value

# ----


def match_list(in_list, match_string, exact=False):
    """
    Description
    -----------

    This function ingests a Python list and a Python string and
    matches, either exact or partial, are sought for the string within
    the provided list and a tuple of values is returned; if
    exact='True', a Python string is returned if a match is found
    (i.e., match_chk=True) or 'None' if no match is found; if
    exact='False', a list of Python strings if matches are found
    (i.e., match_chk=True).

    Parameters
    ----------

    in_list: list

        A Python list of strings within matches will be sought.

    match_string: str

        A Python string for which to search for matches within the
        ingested list.

    exact: bool, optional

        A Python boolean variable; if 'True', a Python string will be
        returned assuming a match is made; if 'False', a Python list
        of strings matching 'match_string' will be returned assuming
        matches can be made; the default value is 'False'.

    Returns
    -------

    match_chk: bool

        A Python boolean variable indicating whether a match (or
        matches) has (have) been made.

    match_str: str

        A Python string (if exact=True) or a Python list of strings
        (if exact=False) containing all matches to the input match
        string; if no matches can be found, either NoneType (if
        exact=True) or an empty list (if exact=False) is returned.

    """
    lower_list = [word for word in in_list if word.islower()]
    upper_list = [word for word in in_list if word.isupper()]
    mixed_list = [word for word in in_list if not word.islower() and
                  not word.isupper()]
    match_chk = False
    if not exact:
        match_str = list()
        for string in lower_list:
            if match_string.lower() in string.lower():
                match_str.append(string)
        for string in upper_list:
            if match_string.lower() in string.lower():
                match_str.append(string)
        for string in mixed_list:
            if match_string.lower() in string.lower():
                match_str.append(string)
        if len(match_str) > 0:
            match_chk = True
        return (match_chk, match_str)
    if exact:
        match_str = None
        for string in lower_list:
            if match_string.lower() == string.lower():
                match_chk = True
                match_str = string
                break
        for string in upper_list:
            if match_string.lower() in string.lower():
                match_chk = True
                match_str = string
                break
        for string in mixed_list:
            if match_string.lower() == string.lower():
                match_chk = True
                match_str = string
                break
        return (match_chk, match_str)

# ----


def object_hasattr(object_in, key):
    """
    Description
    -----------

    This function checks whether a Python object contains an attribute
    and returns an appropriate boolean value indicating the result of
    the inquiry.

    Parameters
    ----------

    object_in: obj 

        A Python object within which to inquire about attributes.

    key: str 

        A Python string value specifying the attribute to inquire
        about.

    Returns
    -------

    chk_attr: bool 

        A Python boolean value containing the result of the attribute
        inquiry.

    """

    # Check whether the Python object specified upon entry contains
    # the key specified upon entry.
    chk_attr = hasattr(object_in, key)
    return chk_attr

# ----


def object_setattr(object_in, key, value):
    """
    Description
    -----------

    This function ingests a Python object and a Python key and value
    pair and defines the attributes for the respective object.

    Parameters
    ----------

    object_in: obj

        A Python object within which to search for attributes.

    key: str

        A Python string value specifying the attribute to define.

    value: any type

        A Python variable value specifying the value to accompany the
        Python object attribute (key).

    Returns
    -------

    object_out: obj 

       A Python object containing the user specified key and value
       pair (e.g., attribute).

    """

    # Copy the Python object specified upon entry and define the new
    # attribute using the key and value pair specified upon entry.
    object_out = object_in
    setattr(object_out, key, value)
    return object_out

# ----


def object_todict(object_in):
    """
    Description
    -----------

    This function ingests a Python object and returns a Python
    dictionary containing the contents of the object.

    Parameters
    ----------

    object_in: obj

        A Python object containing specified content.

    Returns
    -------

    dict_out: dict

        A Python dictionary containing the contents of the Python
        object.

    """

    # Build a Python dictionary containing the contents of the Python
    # object specified upon entry.
    dict_out = [name for name in dir(object_in)]
    return dict_out

# ----


def sanitize_list(list_in, list_id):
    """
    Description
    -----------

    This function modifies/rearranges items in a list in accordance
    with the user specifications.

    Parameters
    ----------

    list_in: list

        A Python list (possibly) containing the user specified item.

    list_id: str

        A Python string specifying the user item.

    Returns
    -------

    list_out: list

        A Python list modified/rearranged in accordance with the user
        specifications.

    """

    # Initialize the output list and proceed accordingly.
    list_out = list_in
    for item in list_out:
        try:
            i = list_out.index(list_id)
            j = list_out[i]
            list_out.pop(i)
            list_out.append(j)
        except ValueError:
            pass
    return list_out

# ----


def singletrue(bool_list):
    """
    Description
    -----------

    This function ingests a list of boolean (e.g., logical) variables
    (bool_list) and returns True if a single true value is in the
    boolean list or False otherwise.

    Parameters
    ----------

    bool_list: list

        A Python list of boolean type variables.

    Returns
    -------

    check: bool

        A Python boolean variable specifying whether only a single
        True value is within the respective boolean list; if so, True
        is returned; if not False is returned.

    """

    # Build a generator function using the list of boolean variables
    # specified upon entry.
    iterator = iter(bool_list)

    # Check the total number of True values within the list of boolean
    # variables specified upon entry and proceed accordingly.
    has_true = any(iterator)
    has_another_true = any(iterator)
    check = (has_true and not has_another_true)
    return check

# ----


def string_parser(in_list, remove_comma=False):
    """
    Description
    -----------

    This function ingests a Python list of variables and returns a
    Python list of appropriately formatted values.

    Parameters
    ----------

    in_list: list

        A Python list of variable values to be formatted.

    remove_comma: bool, optional

        A Python boolean variable specifying to remove any comma
        string occurances in the returned list (see out_list).

    Returns
    -------

    out_list: list

        A Python list of appropriately formatted variable values.

    """
    out_list = list()
    try:
        for value in in_list:
            test_value = value
            try:
                if isinstance(test_value, unicode):
                    test_value = test_value.encode('ascii', 'ignore')
            except NameError:
                pass
            if isinstance(test_value, bool):
                if test_value:
                    value = True
                    if not test_value:
                        value = False
            if isinstance(test_value, str):
                try:
                    dummy = float(test_value)
                    if '.' in test_value:
                        value = float(test_value)
                    else:
                        value = int(test_value)
                except ValueError:
                    if test_value.lower() == 'none':
                        value = None
                    elif test_value.lower() == 'true':
                        value = True
                    elif test_value.lower() == 'false':
                        value = False
                    else:
                        value = str(test_value)
            try:
                value = value.rsplit()[0]
            except AttributeError:
                pass
            out_list.append(value)
    except TypeError:
        value = None
        out_list.append(value)
    if remove_comma:
        new_list = list()
        for item in out_list:
            if item != ',':
                new_list.append(item)
        out_list = new_list
    return out_list

# ----


def true_or_false(argval):
    """
    Description
    -----------

    This function checks whether an argument is a Boolean-type value;
    if so, this function defines the appropriate Python boolean-type;
    otherwise, this function returns NoneType.

    Parameters
    ----------

    argval: any type 

        A value corresponding to an argument.

    Returns
    -------

    pytype: bool

        A Python boolean-type value if the argument is a boolean
        variable; otherwise, NoneType.

    """

    # Check the arguments provided upon entry and proceed accordingly.
    ua = str(argval).upper()
    if 'TRUE'.startswith(ua):
        pytype = True
    elif 'FALSE'.startswith(ua):
        pytype = False
    else:
        pytype = None
    return pytype

# ----


def unique_list(in_list):
    """
    Description
    -----------

    This function ingests a list, possibly with duplicate values, and
    returns a list of only unique values.

    Parameters
    ----------

    in_list: list

        A N-dimensional Python list containing strings.

    Returns
    -------

    out_list: list

        A Python list containing only uniquely-valued strings.

    """
    out_list = list()
    out_dict = collections.OrderedDict.fromkeys(x for x in in_list if x not
                                                in out_list)
    out_list = list()
    for key in sorted(out_dict.keys()):
        out_list.append(key.replace(' ', ''))
    return out_list
