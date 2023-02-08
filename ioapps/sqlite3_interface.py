# =========================================================================

# Module: ioapps/sqlite3_interface.py

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

    sqlite3_interface.py

Description
-----------

    This module contains functions which interface with the Python
    SQLite3 library API.

Functions
---------

    _database_close(connect)

        This function closes an open SQLite3 database connection.

    _database_commit(connect)

        This function commits a database update for the current
        transaction.

    _database_connect(path)

        This function initializes a SQLite3 database; if the database
        path exist prior to entry, this function simply open the
        respective SQL database.

    _database_execute(cursor, exec_str, is_read=False)

        This function executes a SQLite3 library API statement.

    _database_exist(path)

        This function checks for the existence of the specified SQLite3
        database path.

    create_table(path, table_name, table_dict)

        This function creates a previously non-existent a SQLite3
        database table in the specified SQLite3 database file path.

    delete_row(path, table_name, rmcond)

        This function deletes a row within a specified table based on a
        provided removal condition.

    read_columns(path, table_name)

        This function returns a list for the respective column names
        within the specified SQLite3 database table.

    read_table(path, table_name)

        This function reads values from an existing SQLite3 database.

    read_tablenames(path, format_list=False)

        This method parses the SQLite3 database path and returns a
        list of table names within the respective SQLite3 database
        path.

    write_table(path, table_name, row_dict)

        This function writes values into an existing SQLite3 database.

Author(s)
---------

    Henry R. Winterbottom; 25 September 2022

History
-------

    2022-09-25: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=broad-except
# pylint: disable=inconsistent-return-statements
# pylint: disable=raise-missing-from
# pylint: disable=too-many-locals

# ----

import sqlite3
from typing import Dict, List, Tuple, Union

from tools import fileio_interface, parser_interface
from utils.exceptions_interface import SQLite3InterfaceError
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = [
    "create_table",
    "delete_row",
    "read_columns",
    "read_table",
    "read_tablenames",
    "write_table",
]

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

logger = Logger()

# ----


def _database_close(connect: object) -> None:
    """
    Description
    -----------

    This function closes an open SQLite3 database connection.

    Parameters
    ----------

    connect: object

        A Python object SQLite3 library API connection object.

    """

    # Close the connection to a SQLite3 database file path.
    connect.close()


# ----


def _database_commit(connect: object) -> None:
    """
    Description
    -----------

    This function commits a database update for the current transaction.

    Parameters
    ----------

    connect: object

        A Python object SQLite3 API connection object.

    """

    # Commit the update to the open SQLite3 database connection.
    connect.commit()


# ----


def _database_connect(path: str) -> Tuple:
    """
    Description
    -----------

    This function initializes a SQLite3 database; if the database path
    exist prior to entry, this function simply opens the respective
    SQLite3 database path.

    Parameters
    ----------

    path: str

        A Python string specifying the path to the SQLite3 database
        file.

    Returns
    -------

    connect: object

        A Python object SQLite3 API connection object.

    cursor : object

        A Python object SQLite3 API cursor object.

    Raises
    ------

    SQLite3InterfaceError:

        * raised if an exception is encountered while initializing the
          SQLite3 database path.

    """

    # Connect and define the SQLite3 API connection and cursor
    # objects; proceed accordingly.
    try:
        connect = sqlite3.connect(path)
        cursor = connect.cursor()

    except Exception as errmsg:
        msg = (
            f"Initializing the SQLite3 database path {path} failed "
            f"with error {errmsg}. Aborting!!!"
        )
        raise SQLite3InterfaceError(msg=msg)

    return (connect, cursor)


# ----


def _database_execute(
    cursor: object, exec_str: str, is_read: bool = False
) -> Union[Dict, Dict]:
    """
    Description
    -----------

    This function executes a SQLite3 library API statement.

    Parameters
    ----------

    cursor : object

        A Python object SQLite3 API cursor object.

    exec_str: str

        A Python string specifying the SQLite3 statement to be
        executed.

    Keywords
    --------

    is_read: bool, optional

        A Python boolean value specifying whether to read the SQLite3
        table contents in accordance with the SQLite3 statement to be
        executed; if True, the respective database table contents will
        be returned.

    Returns
    -------

    table: dict

        A Python dictionary containing the contents of the SQLite3
        database table; this is returned only if is_read is True upon
        entry; otherwise NoneType is returned.

    Raises
    ------

    SQLite3InterfaceError:

        * raised if an exception is encountered while executing the
          SQLite3 statement.

    """

    # Execute the SQLite3 database statement; proceed accordingly.
    try:
        if is_read:

            # Define and return the SQLite3 database table contents.
            table = cursor.execute(exec_str).fetchall()

            return table

        if not is_read:

            # Execute the SQLite3 database table command.
            cursor.execute(exec_str)

        return None

    except Exception as errmsg:
        msg = (
            f"Executing SQLite3 statement {exec_str} failed with error "
            f"{errmsg}. Aborting!!!"
        )
        raise SQLite3InterfaceError(msg=msg)


# ----


def _database_exist(path: str) -> bool:
    """
    Description
    -----------

    This function checks for the existence of the specified SQLite3
    database path.

    Parameters
    ----------

    path: str

        A Python string specifying the path to the SQLite3 database
        file.

    Returns
    -------

    exist: bool

        A Python boolean valued variable specifying whether the
        SQLite3 database path exists.

    """
    exist = fileio_interface.fileexist(path=path)
    if exist:
        msg = f"Database file {path} exists."
        logger.info(msg=msg)

    if not exist:
        msg = f"The database file {path} does not exist."
        logger.info(msg=msg)

    return exist


# ----


def create_table(path: str, table_name: str, table_dict: Dict) -> None:
    """
    Description
    -----------

    This function creates a previously non-existent a SQLite3 database
    table in the specified SQLite3 database file path.

    Parameters
    ----------

    path: str

        A Python string specifying the path to the SQLite3 database
        file.

    table_name: str

        A Python string specifying the name for the SQLite3 database
        table.

    table_dict: dict

        A Python dictionary containing the SQLite3 database table
        attributes; the dictionary keys are the respective SQLite3
        database table column names and the associated dictionary key
        values are the database types for the respective columns;
        accepted datatypes are BLOB, INTEGER, NULL, REAL, and TEXT.

    Raises
    ------

    SQLite3InterfaceError:

        * raised if an exception is encountered while creating the
          specified SQLite3 database table in the specified path.

    """

    # Connect to the SQLite3 database; proceed accordingly.
    (connect, cursor) = _database_connect(path=path)
    try:

        # Define the SQLite3 database table attributes; proceed
        # accordingly.
        try:
            exec_str = f"CREATE TABLE IF NOT EXISTS {table_name} "
            (column_name_list, column_info) = (list(table_dict.keys()), [])

            # Define the respective column names for the respective
            # SQLite3 database table; proceed accordingly.
            for column_name in column_name_list:
                column_type = parser_interface.dict_key_value(
                    dict_in=table_dict, key=column_name, force=True, no_split=True
                )

                if column_type is None:
                    msg = (
                        f"The data type for column {column_name} could not be determined "
                        "from the specified table attributes. Aborting!!!"
                    )
                    raise SQLite3InterfaceError(msg=msg)

                column_info.append(f"{column_name} {column_type}")

            # Write the database table to the SQLite3 database file
            # path; proceed accordingly.
            column_string = ",".join(column_info)
            try:

                # Build the SQLite3 API execution string.
                exec_str = exec_str + f"({column_string})"

                # Execute the SQLite3 database table command.
                _database_execute(cursor=cursor, exec_str=exec_str)

            except sqlite3.OperationalError:

                # Build the SQLite3 API execution string.
                exec_str = exec_str + f"({column_string})" + ";"

                # Execute the SQLite3 database table command.
                _database_execute(cursor=cursor, exec_str=exec_str)

            # Commit/update the respetive SQLite database table.
            _database_commit(connect=connect)
            msg = f"Created table {table_name} in database {path}."
            logger.info(msg=msg)

        except Exception as errmsg:
            msg = (
                f"Creating SQLite3 database table {table_name} for database path "
                f"{path} failed with error {errmsg}. Aborting!!!"
            )
            raise SQLite3InterfaceError(msg=msg)

    # If the SQLite3 database exists proceed accordingly.
    except sqlite3.OperationalError:
        msg = (
            f"Table {table_name} already exists in database {path} and will not be "
            f"created."
        )
        logger.warn(msg=msg)

    # Close the connection to the SQLite3 database file.
    _database_close(connect=connect)


# ----


def delete_row(path: str, table_name: str, rmcond: str) -> None:
    """
    Description
    -----------

    This function deletes a row within a specified table based on a
    provided removal condition.

    Parameters
    ----------

    path: str

        A Python string specifying the path to the SQLite3 database
        file.

    table_name: str

        A Python string specifying the existing table name within the
        SQLite3 database file.

    rmcond: str

        A Python string specifying the removal condition.

    Raises
    ------

    SQLite3InterfaceError:

        * raised if an exception is encountered while attempting to
          apply the removal condition for the SQLite3 database table
          within the specified database file path.

    """

    # Delete the respective SQLite3 database table row; proceed
    # accordingly.
    try:
        msg = (
            f'Removing any occurrences of row condition "{rmcond}" from '
            f"table {table_name}."
        )
        logger.info(msg=msg)

        # Define the SQLite3 database path connection and SQLite3
        # library API database table command.
        (connect, cursor) = _database_connect(path=path)
        exec_str = f"DELETE from {table_name} where {rmcond}"

        # Execute the SQLite3 database table command.
        _database_execute(cursor=cursor, exec_str=exec_str)
        _database_commit(connect=connect)

        # Close the connection to the SQLite3 database file.
        _database_close(connect=connect)

    except Exception as errmsg:
        msg = (
            f"Deleting database file path {path} table {table_name} using removal "
            f"condition {rmcond} failed with error {errmsg}. Aborting!!!"
        )
        raise SQLite3InterfaceError(msg=msg)


# ----


def read_columns(path: str, table_name: str) -> List:
    """
    Description
    -----------

    This function returns a list for the respective column names
    within the specified SQLite3 database table.

    Parameters
    ----------

    path: str

        A Python string specifying the path to the SQLite3 database
        file.

    table_name: str

        A Python string specifying the existing table name within the
        SQLite3 database file.

    Returns
    -------

    columns: list

        A Python list of the column names within the specified SQLite3
        database table.

    Raises
    ------

    SQLite3InterfaceError:

        * raised if an exception is encountered while attempting to
          collect column names from the SQLite3 database table names.

    """

    # Define the SQLite3 database path connection and SQLite3 library
    # API database table command; proceed accordingly.
    try:

        # Define the SQLite3 database path connection.
        (connect, cursor) = _database_connect(path=path)

        # Execite the SQLite3 library API strong and collect the
        # SQLite3 database table names.
        exec_str = f"SELECT * from {table_name}"
        cursor = connect.execute(exec_str)
        columns = list(map(lambda x: x[0], cursor.description))

        # Close the connection to the SQLite3 database file.
        _database_close(connect=connect)

    except Exception as errmsg:
        msg = (
            f"The query of SQLite3 database file {path} for table {table_name} "
            f"column names failed with error {errmsg}. Aborting!!!"
        )
        raise SQLite3InterfaceError(msg=msg)

    return columns


# ----


def read_table(path: str, table_name: str) -> Dict:
    """
    Description
    -----------

    This function reads values from an existing SQLite3 database.

    Parameters
    ----------

    path: str

        A Python string specifying the path to the SQLite3 database
        file.

    table_name: str

        A Python string specifying the existing table name within the
        SQLite3 database file.

    Returns
    -------

    table_dict: dict

        A Python dictionary containing an enumerated list of the
        SQLite3 database table contents.

    Raises
    ------

    SQLite3InterfaceError:

        * raised if the SQLite3 database path does not exist.

        * raised an exception is encountered while reading the
          specified SQLite3 database table.

    """

    # Check that the SQLite3 database file path exists; proceed
    # accordingly.
    exist = _database_exist(path=path)
    if not exist:
        msg = (
            f"The SQLite3 database path {path} does not exist and "
            "therefore cannot be read. Aborting!!!"
        )
        raise SQLite3InterfaceError(msg=msg)

    # Define the SQLite3 database path connection and SQLite3 library
    # API database table command; proceed accordingly.
    try:

        # Define the SQLite3 database path connection.
        (connect, cursor) = _database_connect(path=path)
        exec_str = f"SELECT * FROM {table_name}"
        table = _database_execute(cursor=cursor, exec_str=exec_str, is_read=True)

        # Build the Python dictionary containing the SQLite3 database
        # table contents
        table_dict = {}
        for i, row in enumerate(table):
            table_dict[i] = list(row)

        # Close the connection to the SQLite3 database file.
        _database_close(connect=connect)

    except Exception as errmsg:
        msg = (
            f"Reading SQLite3 database table {table_name} from SQLite3 "
            f"database file path {path} failed with error {errmsg}. "
            "Aborting!!!"
        )
        raise SQLite3InterfaceError(msg=msg)

    return table_dict


# ----


def read_tablenames(path: str, format_list: bool = False) -> List:
    """
    Description
    -----------

    This method parses the SQLite3 database path and returns a list of
    table names within the respective SQLite3 database path.

    Parameters
    ----------

    path: str

        A Python string specifying the path to the SQLite3 database
        file.

    Keywords
    --------

    format_list: bool, optional

        A Python boolean valued variable specifying whether to format
        the table names returned by the SQLite3 query as a list; if
        format_list is False upon entry, the returned list contains a
        tuple containing all database table names; if format_list is
        True upon entry, the returned list contains each table name
        withini the respective SQLite3 database path.

    Returns
    -------

    tablenames: list

        A Python list of table names contained within the respective
        SQLite3 database path.

    """

    # Check that the SQLite3 database file path exists; proceed
    # accordingly.
    exist = _database_exist(path=path)
    if not exist:
        msg = (
            f"The SQLite3 database path {path} does not exist and "
            "therefore cannot be read. Aborting!!!"
        )
        raise SQLite3InterfaceError(msg=msg)

    # Define the SQLite3 database path connection.
    (_, cursor) = _database_connect(path=path)

    # Collect the table names within the respective database path.
    cursor.execute("SELECT name from sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Create a list of table names from the tuple returned by the
    # SQLite3 command.
    if format_list:
        tablenames = []
        for (i, item) in enumerate(tables):
            tablenames.append(item[i])

    if not format_list:
        tablenames = tables

    return tablenames


# ----


def write_table(path: str, table_name: str, row_dict: Dict) -> None:
    """
    Description
    -----------

    This function writes values into an existing SQLite3 database.

    Parameters
    ----------

    path: str

        A Python string specifying the path to the SQLite3 database
        file.

    table_name: str

        A Python string specifying the existing table name within the
        SQLite3 database file.

    row_dict: dict

        A Python dictionary containing the variable fields to be
        written to the SQLite3 database table.

    Raises
    ------

    SQLite3InterfaceError:

        * raised if the database file path does not exist upon entry.

    """

    # Check that the SQLite3 database file path exists.
    exist = _database_exist(path=path)
    if not exist:
        msg = f"The database file path {path} does not exist. Aborting!!!"
        raise SQLite3InterfaceError(msg=msg)

    # Write the specified variable fields to the SQLite3 database file
    # path; proceed accordingly.
    try:

        # Compile the SQLite3 database base table contents; proceed
        # accordingly.
        exec_str = f"INSERT INTO {table_name} "
        column_name_list = list(row_dict.keys())
        (column_names, column_values) = [[] for i in range(2)]
        for column_name in column_name_list:
            column_names.append(column_name)
            column_value = parser_interface.dict_key_value(
                dict_in=row_dict, key=column_name, force=True, no_split=True
            )
            column_values.append(column_value)

        column_names_string = ",".join(column_names)
        column_values_string = ",".join([str(value) for value in column_values])
        exec_str = (
            exec_str + f"({column_names_string})" + f" VALUES ({column_values_string});"
        )

        # Execute the SQLite3 database table command; if database is
        # locked, continue until write task is successful.
        while True:

            try:

                # Define the SQLite3 database path connection.
                (connect, cursor) = _database_connect(path=path)

                # Execute the SQLite3 database table command.
                _database_execute(cursor=cursor, exec_str=exec_str)
                _database_commit(connect=connect)

                # Exit loop following success.
                break

            except sqlite3.OperationalError:

                # Print message to user and repeat the process
                # (indefinitely) until success.
                msg = (
                    f"Database path {path} is locked; another attempt "
                    f"will be made to update database table {table_name}."
                )
                logger.warn(msg=msg)

        # Close the connection to the SQLite3 database file.
        _database_close(connect=connect)

    except Exception as errmsg:
        msg = (
            f"Writing to SQLite3 database table {table_name} within "
            f"SQLite3 database file path {path} failed with error "
            f"{errmsg}. Aborting!!!"
        )
        raise SQLite3InterfaceError(msg=msg)
