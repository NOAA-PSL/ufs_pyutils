# =========================================================================

# Module: tools/fileio_interface.py

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

    fileio_interface.py

Description
-----------

    This module contains functions required to perform various file
    and directory tasks.

Classes
-------

    RNRYAMLLoader()

        This is the base-class object for all YAML file parsing
        interfaces; it is a sub-class of yaml.SafeLoader.

Functions
---------

    concatenate(filelist, concatfile)

        This function concatenates a list of user-specified files
        (filelist) into a single user-specified file (concatfile); the
        respective files are opened in binary mode to increase the
        applicability of the function.

    copyfile(srcfile, dstfile)

        This function will create a local copy of a user specified
        source file to user specified destination file location; if
        the destination file already exists, it will be removed prior
        to the creation of the destination file.

    dircontents(path)

        This function compiles a content list of the user specified
        directory.

    dirpath_tree(path)

        This function checks whether the directory tree (i.e., path)
        exists; if not an attempt will be made to build it.

    fileexist(path)

        This function will ingest a file-path and check whether the
        respective file-path exists; this function is a wrapper around
        os.path.isfile.

    filepermission(path, permission)

        This function defines the permissions for a specified
        file-path.

    filesize(path)

        This function ingests a file-path and obtains the size of the
        file, in bytes; the respective 'typical' file size
        descriptions, namely mega-bytes (MB), giga-bytes (GB), and
        tera-bytes (TB), are computed and returned.

    makedirs(path, force=False)

        This function is a wrapper around os.makedirs and will build
        the directory tree (if needed) and the directory
        leaves/sub-directories.

    read_json(json_file)

        This function ingests a JavaScript Object Notation (e.g.,
        JSON) formatted file and returns a Python dictionary
        containing all attributes of the file.

    read_yaml(yaml_file, return_obj=False)

        This function ingests a YAML Ain't Markup Language (e.g.,
        YAML) formatted file and returns a Python dictionary
        containing all attributes of the file.

    removefiles(filelist)

        This function ingests a list of filenames. The function then
        checks whether the respective filename exists and if so it
        removes it.

    rename(srcfile, dstfile)

        This function will rename a file in accordance with the user
        specifications; this function may also be used to move and
        rename files between different file paths.

    rmdir(path)

        This function will attempt to remove the user specified
        path. the path does not exist, this function does nothing.

    symlink(srcfile, dstfile)

        This function will create a symbolic link from a user
        specified source file to a user specified destination file; if
        the destination file already exists, it will be removed prior
        to the creation of the symbolic link.

    touch(path)

        This function emulates the POSIX UNIX touch application.

    write_jinja2(jinja2_file, in_dict)

        This function writes a Jinja2 formatted file using the
        specified Python dictionary.

    write_json(json_file, in_dict, indent=4)

        This function writes a JavaScript Object Notation (e.g., JSON)
        formatted file using the specified Python dictionary.

    write_yaml(yaml_file, in_dict, default_flow_style=False):

        This function writes a YAML Ain't Markup Language (e.g., YAML)
        formatted file using the specified Python dictionary.

Requirements
------------

- pyyaml; https://pyyaml.org/

Author(s)
---------

    Henry R. Winterbottom; 03 December 2022

History
-------

    2022-12-03: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=consider-using-f-string
# pylint: disable=consider-using-with
# pylint: disable=broad-except
# pylint: disable=too-many-ancestors
# pylint: disable=unspecified-encoding
# pylint: disable=wrong-import-order

# ----

import json
import os
import re
import shutil
import subprocess
import numpy
import yaml

from tools import parser_interface
from typing import Union
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = [
    "concatenate",
    "copyfile",
    "dircontents",
    "dirpath_tree",
    "fileexist",
    "filepermission",
    "filesize",
    "makedirs",
    "read_json",
    "read_yaml",
    "removefiles",
    "rename",
    "rmdir",
    "symlink",
    "touch",
    "write_jinja2",
    "write_json",
    "write_yaml",
]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"


# ----


class RNRYAMLLoader(yaml.SafeLoader):
    """
    Description
    -----------

    This is the base-class object for all YAML file parsing
    interfaces; it is a sub-class of yaml.SafeLoader.

    """

    # Define the YAML library loader type; this follows from the
    # discussion found at
    # https://stackoverflow.com/questions/52412297/\
    #   how-to-replace-environment-variable-value-in-yaml-file-to-be-parsed-using-python
    envvar_matcher = re.compile(r".*\$\{([^}^{]+)\}.*")

    def envvar_constructor(self, node):
        """
        Description
        -----------

        This function is the environment variable template
        constructor.

        """

        return os.path.expandvars(node.value)


# ----


def concatenate(filelist: list, concatfile: str) -> None:
    """
    Description
    -----------

    This function concatenates a list of user-specified files
    (filelist) into a single user-specified file (concatfile); the
    respective files are opened in binary mode to increase the
    applicability of the function.

    Parameters
    ----------

    filelist: list

        A Python list of file paths to compose the concatenated file
        path.

    concatfile: str

        A Python string specifying the path of the concatenated file
        created from the input file list.

    """

    # Concatenate files contained within the specified list of files
    # upon entry.
    with open(concatfile, "wb") as fout:
        for filename in filelist:
            with open(filename, "rb") as fin:
                data = fin.read()
            fout.write(data)


# ----


def copyfile(srcfile: str, dstfile: str) -> None:
    """
    Description
    -----------

    This function will create a local copy of a user specified source
    file to user specified destination file location; if the
    destination file already exists, it will be removed prior to the
    creation of the destination file.

    Parameters
    ----------

    srcfile: str

        A Python string defining the path to the source file to be
        copied.

    dstfile: str

        A Python string defining the path to the destination file from
        which the source file is copied.

    """

    # Check whether the specified destination is a filename or
    # directory path; proceed accordingly.
    if os.path.isfile(dstfile):
        os.remove(dstfile)

    if os.path.isdir(dstfile):
        path = dstfile
        rmdir(path)

    # Copy the specified source file to the corresponding destination
    # file using the respective platform copy method.
    msg = f"Copying file {srcfile} to {dstfile}."
    logger.info(msg=msg)

    cmd = ["cp", "-rRfL", srcfile, dstfile]

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()


# ----


def dircontents(path: str) -> list:
    """
    Description
    -----------

    This function compiles a content list of the user specified
    directory.

    Parameters
    ----------

    path: str

        A Python string defining the path to the directory to be
        parsed.

    Returns
    -------

    contents: list

        A Python list containing the directory contents.

    """

    # Collect the specified directory path list of contents.
    contents = os.listdir(path)

    return contents


# ----


def dirpath_tree(path: str) -> None:
    """
    Description
    -----------

    This function checks whether the directory tree (i.e., path) exists;
    if not an attempt will be made to build it.

    Parameters
    ----------

    path: str

        A Python string specifying the directory tree path to be
        created if it does not (yet) exist.

    Raises
    ------

    StagingError:

        * raised if an exception is encountered while attempting to
          build the specified directory tree.

    """

    # Check whether the directory tree exists; proceed accordingly.
    exist = fileexist(path=path)
    if exist:
        msg = f"The directory tree {path} exists; nothing to be done."
        logger.info(msg=msg)

    if not exist:
        msg = (
            f"The directory tree {path} does not exist; an attempt "
            "will be made to create it."
        )
        logger.warn(msg=msg)

        makedirs(path=path)


# ----


def fileexist(path: str) -> bool:
    """
    Description
    -----------

    This function ingests a file-path and checks whether the
    respective file-path exists; this function is a wrapper around
    os.path.isfile.

    Parameters
    ----------

    path: str

        A Python string defining the path to a respective file.

    Returns
    -------

    exist: bool

        A Python boolean variable specifying whether the respective
        file-path (path) exists.

    """

    # Define a boolean valued variable specifying whether the
    # specified file path exists upon entry.
    exist = os.path.exists(path)

    return exist


# ----


def filepermission(path: str, permission: int) -> None:
    """
    Description
    -----------

    This function defines the permissions for a specified file-path.

    Parameters
    ----------

    path: str

        A Python string defining the path to a respective file.

    permission: int

        A Python integer specifying the UNIX file permissions.

    """

    # Define the permissions for the specified file path.
    os.chmod(path, permission)


# ----


def filesize(path: str) -> tuple:
    """
    Description
    -----------

    This function ingests a file-path and obtains the size of the
    file, in bytes; the respective 'typical' file size descriptions,
    namely mega-bytes (MB), giga-bytes (GB), and tera-bytes (TB), are
    computed and returned.

    Parameters
    ----------

    path: str

        A Python string defining the path to a respective file.

    Returns
    -------

    bytes_path: int

        A Python integer specifying the file size in bytes.

    megabytes_path: int

        A Python integer specifying the file size in mega-bytes (MB).

    gigabytes_path: int

        A Python integer specifying the file size in giga-bytes (GB).

    terabytes_path: int

        A Python integer specifying the file size in tera-bytes (TB).

    """

    # Define and/or compute the specified file path sizes.
    bytes_path = os.path.getsize(path)
    megabytes_path = numpy.int(bytes_path / 1.0e6)
    gigabytes_path = numpy.int(bytes_path / 1.0e9)
    terabytes_path = numpy.int(bytes_path / 1.0e12)
    bytes_path = numpy.int(bytes_path)

    return (bytes_path, megabytes_path, gigabytes_path, terabytes_path)


# ----


def makedirs(path: str, force: bool = False) -> None:
    """
    Description
    -----------

    This function is a wrapper around os.makedirs and will build the
    directory tree (if needed) and the directory
    leaves/sub-directories.

    Parameters
    ----------

    path: str

        A Python string defining the path to the directory to be
        constructed.

    Keywords
    --------

    force: bool, optional

        A Python boolean variable indicating whether any previous
        directories should be forcibly removed prior to constucting
        the directory tree; default is False.

    """

    # Build the directory path specified upon entry.
    if os.path.isdir(path):
        if force:
            rmdir(path)

    try:
        os.makedirs(path)
    except OSError:
        pass


# ----


def read_json(json_file: str) -> dict:
    """
    Description
    -----------

    This function ingests a JavaScript Object Notation (e.g., JSON)
    formatted file and returns a Python dictionary containing all
    attributes of the file.

    Parameters
    ----------

    json_file: str

        A Python string containing the full-path to the JSON file to
        be parsed.

    Returns
    -------

    json_dict: dict

        A Python dictionary containing all attributes contained within
        the ingested JSON file.

    """

    # Open and read the contents of the specified JSON-formatted file
    # path.
    with open(json_file, "r") as stream:
        json_dict = json.load(stream)

    return json_dict


# ----


def read_yaml(yaml_file: str, return_obj: bool = False) -> Union[dict, object]:
    """
    Description
    -----------

    This function ingests a YAML Ain't Markup Language (e.g., YAML)
    formatted file and returns a Python dictionary containing all
    attributes of the file.

    Parameters
    ----------

    yaml_file: str

        A Python string containing the full-path to the YAML file to
        be parsed.

    Keywords
    --------

    return_obj: bool, optional

        A Python boolean valued variable specifying whether to return
        a Python object containing the YAML-formatted file contents;
        in this instance a Python dictionary will be defined using the
        contents of the YAML-formatted file and then the Python object
        will be constructed; if True, yaml_obj is returned instead of
        yaml_dict.

    Returns
    -------

    yaml_dict: dict

        A Python dictionary containing all attributes ingested from
        the YAML-formatted file; returned if return_obj is False upon
        entry.

    yaml_obj: object

        A Python object containing all attributes injested from the
        YAML-formatted file; returned if return_obj is True upon
        entry.

    """

    # Define the YAML library loader type.
    RNRYAMLLoader.add_implicit_resolver("!ENV", RNRYAMLLoader.envvar_matcher, None)
    RNRYAMLLoader.add_constructor("!ENV", RNRYAMLLoader.envvar_constructor)

    # Open and read the contents of the specified YAML-formatted file
    # path.
    with open(yaml_file, "r") as stream:
        yaml_dict = yaml.load(stream, Loader=RNRYAMLLoader)

    # Define the Python data type to be returned; proceed accordingly.
    yaml_return = None
    if return_obj:
        (attr_list, yaml_obj) = ([], parser_interface.object_define())
        for key in yaml_dict.keys():
            attr_list.append(key)
            value = parser_interface.dict_key_value(
                dict_in=yaml_dict, key=key, no_split=True
            )
            yaml_obj = parser_interface.object_setattr(
                object_in=yaml_obj, key=key, value=value
            )
        yaml_return = yaml_obj

    if not return_obj:

        yaml_return = yaml_dict

    return yaml_return


# ----


def removefiles(filelist: list) -> None:
    """
    Description
    -----------

    This function ingests a list of filenames; the function then
    checks whether the respective filename exists and if so it removes
    it.

    Parameters
    ----------

    filelist: list

        A Python list containing a list of files to be removed.

    """

    # Remove the list of files provided upon entry.
    for filename in filelist:
        if os.path.isfile(filename):
            os.remove(filename)


# ----


def rename(srcfile: str, dstfile: str) -> None:
    """
    Description
    -----------

    This function will rename a file in accordance with the user
    specifications; this function may also be used to move and rename
    files between different file paths.

    Parameters
    ----------

    srcfile: str

        A Python string defining the path to the source file to be
        renamed/moved.

    dstfile: str

        A Python string defining the path to the destination file from
        which the source file is to be renamed/moved.

    """

    # Rename (i.e., move) the source file path specified upon entry to
    # the destination file path specified upon entry.
    try:
        shutil.move(srcfile, dstfile)

    except Exception:
        pass


# ----


def rmdir(path: str) -> None:
    """
    Description
    -----------

    This function will attempt to remove the user specified path. the
    path does not exist, this function does nothing.

    Parameters
    ----------

    path: str

        A Python string containing the path to the directory to be
        removed.

    """

    # Check whether the specified path is an existing directory tree
    # upon entry; proceed accordingly.
    if os.path.isdir(path):
        shutil.rmtree(path)

    if not os.path.isdir(path):
        pass


# ----


def symlink(srcfile: str, dstfile: str) -> None:
    """
    Description
    -----------

    This function will create a symbolic link from a user specified
    source file to a user specified destination file; if the
    destination file already exists, it will be removed prior to the
    creation of the symbolic link.

    Parameters
    ----------

    srcfile: str

        A Python string defining the path to the source file to be
        symbolically linked.

    dstfile: str

        A Python string defining the path to the destination file from
        which the source file is to be symbolically linked.

    """

    # Check whether the destination symbolic link exists upon entry;
    # proceed accordingly.
    if os.path.isfile(dstfile):
        os.remove(dstfile)

    try:
        os.symlink(srcfile, dstfile)
    except OSError:
        pass


# ----


def touch(path: str):
    """
    Description
    -----------

    This function emulates the POSIX UNIX touch application.

    Parameters
    ----------

    path: str

        A Python string specifying the file path for which to apply
        the UNIX touch application.

    """

    # Open and append to the file path specified upon entry.
    with open(path, "a"):
        os.utime(path, None)


# ----


def write_jinja2(jinja2_file: str, in_dict: dict) -> None:
    """
    Description
    -----------

    This function writes a Jinja2 formatted file using the specified
    Python dictionary.

    Parameters
    ----------

    jinja2_file: str

        A Python string containing the full-path to the Jinja2 file to
        be written.

    in_dict: dict

        A Python dictionary containing the attributes to be written to
        the Jinja2 file.

    """

    # Open and write the dictionary contents to the specified
    # Jinja2-formatted file path.
    with open(jinja2_file, "w") as file:
        file.write("#!Jinja2\n")
        for key in in_dict.keys():
            value = in_dict[key]

            if isinstance(value, str):
                string = f'set {key} = "{value}"'
            else:
                string = f"set {key} = {value}"

            file.write("{%% %s %%}\n" % string)


# ----


def write_json(json_file: str, in_dict: dict, indent: int = 4) -> None:
    """
    Description
    -----------

    This function writes a JavaScript Object Notation (e.g., JSON)
    formatted file using the specified Python dictionary.

    Parameters
    ----------

    json_file: str

        A Python string containing the full-path to the JSON file to
        be written.

    in_dict: dict

        A Python dictionary containing the attributes to be written to
        the JSON file.

    Keywords
    --------

    indent: int, optional

        A Python integer defining the indentation level for the
        attributes within the JSON-formatted file.

    """

    # Open and write the dictionary contents to the specified
    # JSON-formatted file path.
    with open(json_file, "w") as file:
        json.dump(in_dict, file, indent=indent)


# ----


def write_yaml(yaml_file: str, in_dict: dict, default_flow_style: bool = False) -> None:
    """
    Description
    -----------

    This function writes a YAML Ain't Markup Language (e.g., YAML)
    formatted file using the specified Python dictionary.

    Parameters
    ----------

    yaml_file: str

        A Python string containing the full-path to the YAML file to
        be written.

    in_dict: dict

        A Python dictionary containing the attributes to be written to
        the YAML file.

    Keywords
    --------

    default_flow_style: bool, optional

        A Python boolean variable specifying the output YAML file
        formatting.

    """

    # Open and write the dictionary contents to the specified
    # YAML-formatted file path.
    with open(yaml_file, "w") as file:
        yaml.dump(in_dict, file, default_flow_style=default_flow_style)
