# =========================================================================

# Module: confs/yaml_interface.py

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

    yaml_interface.py

Description
-----------

    This module contains classes and methods to parse YAML-formatted
    template files and create an external file containing the user
    specified values.

Classes
-------

    YAML()

        This is the base-class object for YAML-formatted template file
        updates and the creation of a YAML-formatted file based on the
        template and the user-specified template variable key and
        value pairs.

    YAMLLoader()

        This is the base-class object for all YAML file parsing
        interfaces; it is a sub-class of SafeLoader.

Functions
---------

    __error__(msg=None)

        This function is the exception handler for the respective
        module.

Author(s)
---------

    Henry R. Winterbottom; 29 November 2022

History
-------

    2022-11-29: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=broad-except
# pylint: disable=too-many-ancestors
# pylint: disable=unused-argument

# ----

import os
import re
from typing import Union

import yaml
from tools import fileio_interface, parser_interface
from utils.error_interface import msg_except_handle
from utils.exceptions_interface import YAMLInterfaceError
from utils.logger_interface import Logger
from yaml import SafeLoader

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class YAML:
    """
    Description
    -----------

    This is the base-class object for YAML-formatted template file
    updates and the creation of a YAML-formatted file based on the
    template and the user-specified template variable key and value
    pairs.

    """

    def __init__(self):
        """
        Description
        -----------

        Creates a new YAMLTemplate object.

        """

        # Define the base-class attributes.
        self.logger = Logger()

    def check_yaml(self, attr_value: str) -> bool:
        """
        Description
        -----------

        This method checks whether the specified value for the
        attr_value parameter is a YAML-formatted file.

        Parameters
        ----------

        attr_value: str

            A Python string containing an attribute value to be check
            for YAML-formatting.

        Returns
        -------

        check: bool

            A Python boolean valued variable specifying whether the
            attribute value is a YAML-formatted file.

        """

        # Check that the file is a YAML-formatted file; proceed
        # accordingly.
        try:
            YAMLLoader(attr_value)
            check = True

        except AttributeError:
            check = False

        return check

    def concat_yaml(
        self,
        yaml_file_list: list,
        yaml_file_out: str,
        fail_nonvalid: bool = True,
        ignore_missing: bool = False,
    ) -> None:
        """
        Description
        -----------

        This method reads a list of YAML-formatted files and
        concatenates the contents into a single YAML-formatted file.

        Parameters
        ----------

        yaml_file_list:

            A Python list of YAML-formatted files.

        yaml_file_out: str

            A Python string specifying the path to the YAML-formatted
            file containing the attributes collected from the
            respective YAML-formatted file list provided upon entry.

        Keywords
        --------

        fail_nonvalid: bool, optional

            A Python boolean valued variable specifying whether to
            raise a YAMLInterfaceError exception if a YAML file path
            for concatenation is not a valid YAML-formatted file.

        ignore_missing: bool, optional

            A Python boolean valued variable specifying whether to
            raise a YAMLInterfaceError exception if a YAML file path
            does not exist.

        Raises
        ------

        YAMLInterfaceError:

            * raised if a specified file is not a YAML-formatted
              and/or valid YAML file; invoked only if the respective
              specified file exists.

            * raised if a specified file path does not exist.

        """

        # Read the contents of the respective YAML-formatted files and
        # aggregate the values into a composite Python dictionary.
        yaml_dict_concat = {}
        for yaml_file in yaml_file_list:

            # Check that the respective YAML file path exists; proceed
            # accordingly.
            exist = fileio_interface.fileexist(path=yaml_file)
            if exist:
                try:

                    # Check that the respective file is a valid
                    # YAML-formatted file; proceed accordingly.
                    # yaml_dict.update(self.read_yaml(yaml_file=yaml_file))
                    yaml_dict = self.read_yaml(yaml_file=yaml_file)

                    try:

                        yaml_dict_concat.update(
                            dict(
                                parser_interface.dict_merge(
                                    dict1=yaml_dict_concat, dict2=yaml_dict
                                )
                            )
                        )

                    except Exception:
                        pass

                except ValueError:

                    if fail_nonvalid:
                        msg = f"{yaml_file} is not a valid YAML file. Aborting!!!"
                        __error__(msg=msg)

                    if not fail_nonvalid:
                        msg = (
                            f"{yaml_file} is not a valid YAML file and will not "
                            "be processed."
                        )
                        self.logger.warn(msg=msg)

            if not exist:

                if ignore_missing:
                    msg = (
                        f"The file path {yaml_file} does not exist and "
                        "will not be processed."
                    )
                    self.logger.warn(msg=msg)

                if not ignore_missing:
                    msg = f"The file path {yaml_file} does not exist. " "Aborting!!!"
                    __error__(msg=msg)

        # Write the resulting composite Python dictionary to
        # YAML-formatted file to contain the concatenated attributes.
        self.write_yaml(yaml_file=yaml_file_out, in_dict=yaml_dict_concat)

    def read_concat_yaml(self, yaml_file: str, return_obj: bool = False) -> Union[dict, object]:
        """ """

        # Define the YAML library loader type.
        YAMLLoader.add_implicit_resolver(
            "!ENV", YAMLLoader.envvar_matcher, None)
        YAMLLoader.add_constructor("!ENV", YAMLLoader.envvar_constructor)

        # Open and read the contents of the specified YAML-formatted
        # file path.
        with open(yaml_file, "r", encoding="utf-8") as stream:
            yaml_full_dict = yaml.load(stream, Loader=YAMLLoader)

        # For each attribute within the parsed YAML-formatted file,
        # determine whether a given file is a YAML-formatted file and
        # whether the respective YAML-formatted file exists; proceed
        # acccordingly.
        yaml_dict_concat = {}
        for attr_key in yaml_full_dict:

            # Collect the attribute corresponding to the respective
            # attribute; proceed accordingly.
            attr_value = parser_interface.dict_key_value(
                dict_in=yaml_full_dict, key=attr_key, no_split=True)
            is_yaml = self.check_yaml(attr_value=attr_value)

            # If the respective attribute value is a YAML-formatted
            # file, check that it exists and proceed accordingly.
            if is_yaml:
                exist = fileio_interface.fileexist(path=attr_value)
                if exist:
                    yaml_dict = self.read_yaml(yaml_file=attr_value)

                    yaml_dict_concat.update(
                        dict(parser_interface.dict_merge(
                            dict1=yaml_dict_concat, dict2=yaml_dict)))

                if not exist:
                    yaml_dict_concat[attr_key] = attr_value

            if not is_yaml:
                yaml_dict_concat[attr_key] = attr_value

        print(yaml_dict_concat['fetch'])

        quit()

    def read_yaml(self, yaml_file: str, return_obj: bool = False) -> Union[dict, object]:
        """
        Description
        -----------

        This method ingests a YAML Ain't Markup Language (e.g., YAML)
        formatted file and returns a Python dictionary containing all
        attributes of the file.

        Parameters
        ----------

        yaml_file: str

            A Python string containing the full-path to the YAML file
            to be parsed.

        Keywords
        --------

        return_obj: bool, optional

            A Python boolean valued variable specifying whether to
            return a Python object containing the YAML-formatted file
            contents; in this instance a Python dictionary will be
            defined using the contents of the YAML-formatted file and
            then the Python object will be constructed; if True,
            yaml_obj is returned instead of yaml_dict.

        Returns
        -------

        yaml_dict: dict

            A Python dictionary containing all attributes ingested
            from the YAML-formatted file; returned if return_obj is
            False upon entry.

        yaml_obj: object

            A Python object containing all attributes injested from
            the YAML-formatted file; returned if return_obj is True
            upon entry.

        """

        # Define the YAML library loader type.
        YAMLLoader.add_implicit_resolver(
            "!ENV", YAMLLoader.envvar_matcher, None)
        YAMLLoader.add_constructor("!ENV", YAMLLoader.envvar_constructor)

        # Open and read the contents of the specified YAML-formatted
        # file path.
        with open(yaml_file, "r", encoding="utf-8") as stream:
            yaml_dict = yaml.load(stream, Loader=YAMLLoader)

        # Define the Python data type to be returned; proceed
        # accordingly.
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

    def write_tmpl(self, yaml_dict: dict, yaml_path: str, yaml_template: str) -> None:
        """
        Description
        -----------

        This method ingests a YAML template file and parses a Python
        dictionary containing key and value pairs for template
        variables to be replaced; the updated template to then written
        to the user-specified path.

        Parameters
        ----------

        yaml_dict: dict

            A Python dictionary containing key and values pairs
            corresponding to the template variables within the
            user-specified YAML-formatted template file.

        yaml_template: str

            A Python string specifying the template variables to be
            sought and updated.

        yaml_path: str

            A Python string specifying the path to the YAML-formatted
            output file derived from the template.

        """

        # Read the template file.
        template_matches = ["<", ">"]
        with open(yaml_template, "r", encoding="utf-8") as file:
            template = file.read().split("\n")

        # Open and write the namelist file while formatting the
        # template values specified upon entry accordingly.
        with open(yaml_path, "w", encoding="utf-8") as file:
            for item in template:
                for key in yaml_dict.keys():
                    if key in item:
                        value = parser_interface.dict_key_value(
                            dict_in=yaml_dict, key=key, no_split=True
                        )
                        item = item.replace(f"<{key}>", str(value))

                if not any(x in item for x in template_matches):
                    file.write(f"{item}\n")

    def write_yaml(
        self,
        yaml_file: str,
        in_dict: dict,
        default_flow_style: bool = False,
        append: bool = False,
    ) -> None:
        """
        Description
        -----------

        This method writes a YAML Ain't Markup Language (e.g., YAML)
        formatted file using the specified Python dictionary.

        Parameters
        ----------

        yaml_file: str

            A Python string containing the full-path to the YAML file
            to be written.

        in_dict: dict

            A Python dictionary containing the attributes to be
            written to the YAML file.

        Keywords
        --------

        default_flow_style: bool, optional

            A Python boolean valued variable specifying the output
            YAML file formatting.

        append: bool, optional

            A Python boolean valued variable specifying whether to
            append to an existing YAML-formatted file; if False upon
            entry any existing YAML-formatted file of the same
            yaml_file attribute name will be overwritten.

        """

        # Open and write the dictionary contents to the specified
        # YAML-formatted file path.
        if append:
            fileopt = "a"
        if not append:
            fileopt = "w"

        with open(yaml_file, fileopt, encoding="utf-8") as file:
            yaml.dump(in_dict, file, default_flow_style=default_flow_style)


# ----


class YAMLLoader(SafeLoader):
    """
    Description
    -----------

    This is the base-class object for all YAML file parsing
    interfaces; it is a sub-class of SafeLoader.

    """

    # Define the YAML library loader type; this follows from the
    # discussion found at https://tinyurl.com/yamlenvparse
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


@msg_except_handle(YAMLInterfaceError)
def __error__(msg: str = None) -> None:
    """
    Description
    -----------

    This function is the exception handler for the respective module.

    Parameters
    ----------

    msg: str

        A Python string containing a message to accompany the
        exception.

    """
