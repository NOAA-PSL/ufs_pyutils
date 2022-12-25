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

Classes
-------

    SQLite3Error(msg)

        This is the base-class for all exceptions; it is a sub-class
        of Error.

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

import sqlite3

from tools import fileio_interface, parser_interface
from utils.error_interface import Error
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


class SQLite3Error(Error):
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

    def __init__(self, msg: str):
        """
        Description
        -----------

        Creates a new SQLite3Error object.

        """
        super(SQLite3Error, self).__init__(msg=msg)


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


def _database_connect(path: str) -> tuple:
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

    SQLite3Error:

        * raised if an exception is encountered while initializing the
          SQLite3 database path.

    """

    # Connect and define the SQLite3 API connection and cursor
    # objects; proceed accordingly.
    try:
        connect = sqlite3.connect(path)
        cursor = connect.cursor()

    except Exception as error:
        msg = (
            "Initializing the SQLite3 database path {0} failed "
            "with error {1}. Aborting!!!".format(path, error)
        )
        raise SQLite3Error(msg=msg)

    return (connect, cursor)


# ----


def _database_execute(cursor: object, exec_str: str, is_read: bool = False) -> dict:
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

    SQLite3Error:

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

    except Exception as error:
        msg = (
            "Executing SQLite3 statement {0} failed with error "
            "{1}. Aborting!!!".format(exec_str, error)
        )
        raise SQLite3Error(msg=msg)


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
        msg = "Database file {0} exists and will be updated.".format(path)
        logger.info(msg=msg)

    if not exist:
        msg = "The database file {0} does not exist.".format(path)
        logger.info(msg=msg)

    return exist


# ----


def create_table(path: str, table_name: str, table_dict: dict) -> None:
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

    SQLite3Error:

        * raised if an exception is encountered while creating the
          specified SQLite3 database table in the specified path.

    """

    # Connect to the SQLite3 database; proceed accordingly.
    (connect, cursor) = _database_connect(path=path)
    try:

        # Define the SQLite3 database table attributes; proceed
        # accordingly.
        try:
            exec_str = "CREATE TABLE IF NOT EXISTS {0} ".format(table_name)
            (column_name_list, column_info) = (list(table_dict.keys()), list())

            # Define the respective column names for the respective
            # SQLite3 database table; proceed accordingly.
            for column_name in column_name_list:
                column_type = parser_interface.dict_key_value(
                    dict_in=table_dict, key=column_name, force=True, no_split=True
                )

                if column_type is None:
                    msg = (
                        "The data type for column {0} could not be determined "
                        "from the specified table attributes. Aborting!!!".format(
                            column_name
                        )
                    )
                    raise SQLite3Error(msg=msg)

                column_info.append("{0} {1}".format(column_name, column_type))

            # Write the database table to the SQLite3 database file
            # path; proceed accordingly.
            column_string = ",".join(column_info)
            try:

                # Build the SQLite3 API execution string.
                exec_str = exec_str + "({0})".format(column_string)

                # Execute the SQLite3 database table command.
                _database_execute(cursor=cursor, exec_str=exec_str)

            except sqlite3.OperationalError:

                # Build the SQLite3 API execution string.
                exec_str = exec_str + "({0})".format(column_string + ";")

                # Execute the SQLite3 database table command.
                _database_execute(cursor=cursor, exec_str=exec_str)

            # Commit/update the respetive SQLite database table.
            _database_commit(connect=connect)
            msg = "Created table {0} in database {1}.".format(table_name, path)
            logger.info(msg=msg)

        except Exception as error:
            msg = (
                "Creating SQLite3 database table {0} for database path "
                "{1} failed with error {2}. Aborting!!!".format(table_name, path, error)
            )
            raise SQLite3Error(msg=msg)

    # If the SQLite3 database exists proceed accordingly.
    except sqlite3.OperationalError:
        msg = (
            "Table {0} already exists in database {1} and will not be "
            "created.".format(table_name, path)
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

    SQLite3Error:

        * raised if an exception is encountered while attempting to
          apply the removal condition for the SQLite3 database table
          within the specified database file path.

    """

    # Delete the respective SQLite3 database table row; proceed
    # accordingly.
    try:
        msg = (
            'Removing any occurrences of row condition "{0}" from '
            "table {1}.".format(rmcond, table_name)
        )
        logger.info(msg=msg)

        # Define the SQLite3 database path connection and SQLite3
        # library API database table command.
        (connect, cursor) = _database_connect(path=path)
        exec_str = "DELETE from {0} where {1}".format(table_name, rmcond)

        # Execute the SQLite3 database table command.
        _database_execute(cursor=cursor, exec_str=exec_str)
        _database_commit(connect=connect)

        # Close the connection to the SQLite3 database file.
        _database_close(connect=connect)

    except Exception as error:
        msg = (
            "Deleting database file path {0} table {1} using removal "
            "condition {2} failed with error {3}. Aborting!!!".format(
                path, table_name, rmcond, error
            )
        )
        raise SQLite3Error(msg=msg)


# ----


def read_columns(path: str, table_name: str) -> list:
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

    SQLite3Error:

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
        exec_str = "SELECT * from {0}".format(table_name)
        cursor = connect.execute(exec_str)
        columns = list(map(lambda x: x[0], cursor.description))

        # Close the connection to the SQLite3 database file.
        _database_close(connect=connect)

    except Exception as error:
        msg = (
            "The query of SQLite3 database file {0} for table {1} "
            "column names failed with error {2}. Aborting!!!".format(
                path, table_name, error
            )
        )
        raise SQLite3Error(msg=msg)

    return columns


# ----


def read_table(path: str, table_name: str) -> dict:
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

    SQLite3Error:

        * raised if the SQLite3 database path does not exist.

        * raised an exception is encountered while reading the
          specified SQLite3 database table.

    """

    # Check that the SQLite3 database file path exists; proceed
    # accordingly.
    exist = _database_exist(path=path)
    if not exist:
        msg = (
            "The SQLite3 database path {0} does not exist and "
            "therefore cannot be read. Aborting!!!".format(path)
        )
        raise SQLite3Error(msg=msg)

    # Define the SQLite3 database path connection and SQLite3 library
    # API database table command; proceed accordingly.
    try:

        # Define the SQLite3 database path connection.
        (connect, cursor) = _database_connect(path=path)
        exec_str = "SELECT * FROM {0}".format(table_name)
        table = _database_execute(cursor=cursor, exec_str=exec_str, is_read=True)

        # Build the Python dictionary containing the SQLite3 database
        # table contents
        table_dict = dict()
        for i, row in enumerate(table):
            table_dict[i] = list(row)

        # Close the connection to the SQLite3 database file.
        _database_close(connect=connect)

    except Exception as error:
        msg = (
            "Reading SQLite3 database table {0} from SQLite3 "
            "database file path {1} failed with error {2}. "
            "Aborting!!!".format(table_name, path, error)
        )
        raise SQLite3Error(msg=msg)

    return table_dict


# ----


def read_tablenames(path: str, format_list: bool = False) -> list:
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
            "The SQLite3 database path {0} does not exist and "
            "therefore cannot be read. Aborting!!!".format(path)
        )
        raise SQLite3Error(msg=msg)

    # Define the SQLite3 database path connection.
    (connect, cursor) = _database_connect(path=path)

    # Collect the table names within the respective database path.
    cursor.execute("SELECT name from sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Create a list of table names from the tuple returned by the
    # SQLite3 command.
    if format_list:
        tablenames = list()
        for (i, item) in enumerate(tables):
            tablenames.append(item[i])

    if not format_list:
        tablenames = tables

    return tablenames


# ----


def write_table(path: str, table_name: str, row_dict: dict) -> None:
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

    """

    # Check that the SQLite3 database file path exists.
    exist = _database_exist(path=path)

    # Write the specified variable fields to the SQLite3 database file
    # path; proceed accordingly.
    try:

        # Compile the SQLite3 database base table contents; proceed
        # accordingly.
        exec_str = "INSERT INTO {0} ".format(table_name)
        column_name_list = list(row_dict.keys())
        (column_names, column_values) = [list() for i in range(2)]
        for column_name in column_name_list:
            column_names.append(column_name)
            column_value = parser_interface.dict_key_value(
                dict_in=row_dict, key=column_name, force=True, no_split=True
            )
            column_values.append(column_value)

        column_names_string = ",".join(column_names)
        column_values_string = ",".join([str(value) for value in column_values])
        exec_str = (
            exec_str
            + "({0})".format(column_names_string)
            + " VALUES ({0});".format(column_values_string)
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
                    "Database path {0} is locked; another attempt "
                    "will be made to update database table {1}.".format(
                        path, table_name
                    )
                )
                logger.warn(msg=msg)

        # Close the connection to the SQLite3 database file.
        _database_close(connect=connect)

    except Exception as error:
        msg = (
            "Writing to SQLite3 database table {0} within "
            "SQLite3 database file path {1} failed with error "
            "{2}. Aborting!!!".format(table_name, path, error)
        )
        raise SQLite3Error(msg=msg)
