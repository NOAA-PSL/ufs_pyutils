# =========================================================================

# $$$ MODULE DOCUMENTATION BLOCK

# UFS-RNR :: ush/tools/nml_interface.py

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

    nml_interface.py

Description
-----------

    This module contains methods to parse namelist-type template files
    and create an external file containing the user specified values.

Classes
-------

    Namelist(log_messages=False,no_string_quotes=False,remove_comments=False,
             strip_dblequotes=False)

        This is the base-class object for all namelist-type template
        file parsing and external namelist-type file creation.

    TemplateStringUpdate()

        This is the base-class object for all template string parsing.

    YAMLTemplate()

        This is the base-class object for YAML-formatted template file
        updates and the creation of a YAML-formatted file based on the
        template and the user-specified template variable key and
        value pairs.

Author(s)
--------- 

   Henry R. Winterbottom; 07 August 2022

History
-------

   2022-08-07: Henry Winterbottom -- Initial implementation.

"""

# ----

import re

from tools import datetime_interface
from tools import fileio_interface
from tools import parser_interface

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class Namelist(object):
    """
    Description
    -----------

    This is the base-class object for all namelist-type template file
    parsing and external namelist-type file creation.

    Keywords
    --------

    log_messages: bool, optional

        A Python boolean variable specifying whether to include
        template file path and file creation time in formatted output
        file.

    no_string_quotes: bool, optional

        A Python boolean variable indicating whether to include quotes
        around strings in the namelist-type formatted file created
        from the template.

    remove_comments: bool, optional

        A Python boolean variable specifying whether to remove
        comments within the template file from the output
        namelist-type file.

    strip_dblquotes: bool, optional

        A Python boolean variable specifying whether to remove (strip)
        any double quotes (i.e., " ") from strings write to the output
        namelist-type file.

    """

    def __init__(self, log_messages=False, no_string_quotes=False,
                 remove_comments=False, strip_dblequotes=False):
        """ 
        Description
        -----------

        Creates a new Namelist object.

        """

        # Define the base-class attributes.
        nml_attr_list = ['log_messages', 'no_string_quotes',
                         'remove_comments', 'strip_dblequotes']
        for item in nml_attr_list:
            self = tools.parser_interface.object_setattr(
                object_in=self, key=item, value=eval(item))

    def check_float(self, string):
        """
        Description
        ----------

        This method attempts to convert a string to a float value; if
        successful, the return value (float_valid) is True; if
        unsuccessful (e.g., a ValueError exception is encountered),
        the return value (float_valid) is False.

        Parameters
        ----------

        string: str

            A Python string to be tested for a float conversion.

        Returns
        -------

        float_valid: bool

            A Python boolean value specifying the success of the
            string to float conversion.

        """

        # Check the input string upon entry and proceed accordingly.
        char_chks = ['e']
        if any(item in string for item in char_chks):
            try:
                float(string)
                float_valid = True
            except ValueError:
                float_valid = False
        else:
            float_valid = None
        return float_valid

    def dblequotes_strip(self, nml_path):
        """
        Description
        -----------

        This method will strip string embedded between double quotes
        (i.e., " ") and update the respective lines/strings within the
        namelist-type output file path.

        Parameters
        ----------

        nml_path: str

            A Python string specifying the path to the formatted
            namelist-type output file.

        """

        # Remove any occurances of double quotation marks.
        with open(nml_path, 'r') as f:
            data = f.read()
        filelist = list()
        filelist.append(nml_path)
        tools.fileio_interface.removefiles(filelist=filelist)
        with open(nml_path, 'w') as f:
            for line in data.split('\n'):
                line = re.sub('["]', '', line)
                f.write('{0}\n'.format(line))

    def write(self, nml_dict, nml_template, nml_path):
        """
        Description
        -----------

        This method parses a Python dictionary and replaces all
        variables within a user specified namelist-type template file.

        Parameters
        ----------

        nml_dict: dict

            A Python dictionary containing key and values pairs
            corresponding to the available variables within the
            user-specified namelist-type template file.

        nml_template: str

            A Python string specifying the namelist-type template file
            to be parsed.

        nml_path: str

            A Python string specifying the path to the formatted
            namelist-type output file.

        """

        # Read the namelist template file provided upon entry.
        with open(nml_template, 'rt') as f:
            data = f.read().split('\n')
        idchars = set('<>')

        # Open the namelist output file and proceed accordingly.
        with open(nml_path, 'wt') as f:
            if self.log_messages:
                f.write('! File created from {0}.\n'.format(nml_template))

            # Build the namelist in accordance with the namelist
            # template attributes.
            for nml_line in data:
                for key in nml_dict.keys():
                    check_key = '<{0}>'.format(key)
                    if check_key in nml_line:
                        value = nml_dict[key]
                        test_value = value
                        if isinstance(test_value, str):

                            # Handle float values accordingly.
                            float_valid = self.check_float(string=test_value)
                            if float_valid is not None:
                                if float_valid:
                                    try:
                                        nml_line = nml_line.replace(
                                            '{0}'.format(check_key), '{0}'.format(float(value)))
                                    except ValueError:
                                        nml_line = nml_line.replace(
                                            '{0}'.format(check_key), '"{0}"'.format(value))

                            # Handle boolean type values accordingly.
                            if (value.lower() == 't') or (value.lower() == 'f'):
                                nml_line = nml_line.replace(
                                    '{0}'.format(check_key), '{0}'.format(value))
                                break

                            # Handle string type values accordingly.
                            if ',' in test_value:
                                value = str()
                                for item in test_value.split(','):
                                    float_valid = self.check_float(string=item)
                                    if float_valid:
                                        try:
                                            value = value + \
                                                '{0},'.format(float(item))
                                        except ValueError:
                                            value = value + \
                                                '"{0}",'.format(item)
                                    else:
                                        try:
                                            int(item)
                                            value = value + '{0},'.format(item)
                                        except ValueError:
                                            value = value + \
                                                '"{0}",'.format(item)
                                nml_line = nml_line.replace(
                                    '{0}'.format(check_key), '{0}'.format(value))
                            else:

                                # Handle strings containing quotations accordingly.
                                if self.no_string_quotes:
                                    nml_line = nml_line.replace(
                                        '{0}'.format(check_key), '{0}'.format(value))
                                else:
                                    nml_line = nml_line.replace(
                                        '{0}'.format(check_key), '"{0}"'.format(value))

                        # Handle boolean type values accordingly.
                        elif isinstance(test_value, bool):
                            if value:
                                nml_line = nml_line.replace(
                                    '{0}'.format(check_key), 'T')
                            else:
                                nml_line = nml_line.replace(
                                    '{0}'.format(check_key), 'F')
                        else:
                            nml_line = nml_line.replace(
                                '{0}'.format(check_key), '{0}'.format(value))

                # Write to the output namelist file accordingly.
                if all(idc in nml_line for idc in idchars):
                    nml_line = None
                if nml_line is not None:

                    # Handle comment strings accordingly.
                    if self.remove_comments:
                        if ('!' not in nml_line) and (nml_line is not str()):
                            f.write('{0}\n'.format(nml_line))
                    else:
                        f.write('{0}\n'.format(nml_line))

            # Add logging message to the end of the file.
            if self.log_messages:
                timestamp = tools.datetime_interface.current_date(
                    frmttyp='%Y-%m-%d %H:%M:%S')
                f.write('! Updated: {0}.\n'.format(timestamp))

    def run(self, nml_dict, nml_template, nml_path):
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Parses a Python dictionary and replaces all variables
            within a user specified namelist-type template file.

        Parameters
        ----------

        nml_dict: dict

            A Python dictionary containing key and values pairs
            corresponding to the available variables within the
            user-specified namelist-type template file.

        nml_template: str

            A Python string specifying the namelist-type template file
            to be parsed.

        nml_path: str

            A Python string specifying the path to the formatted
            namelist-type output file.

        """

        # Build the namelist file and proceed accordingly.
        self.write(nml_dict=nml_dict, nml_template=nml_template,
                   nml_path=nml_path)
        if self.strip_dblequotes:
            self.dblequotes_strip(nml_path=nml_path)

# ----


class TemplateStringUpdate(object):
    """
    Description
    -----------

    This is the base-class object for all template string parsing.

    """

    def __init__(self):
        """
        Description
        -----------

        Creates a new TemplateStringUpdate object.

        """

    def write(self, str_template, str_dict):
        """
        Description
        -----------

        This method parses a Python dictionary and replaces all
        variables within a user specified template string.

        Parameters
        ----------

        str_dict: dict

            A Python dictionary containing key and values pairs
            corresponding to the available variables within the
            user-specified template string.

        str_template: str

            A Python string specifying the template string to be
            parsed.

        Returns
        -------

        str_update: str

            A Python string containing the updated string in
            accordance with the template attribute.

        """

        # Define the updated string relative to the template
        # attribute.
        str_update = str_template
        for key in str_dict.keys():
            check_key = '<{0}>'.format(key)
            if check_key in str_template:
                value = str_dict[key]
                str_update = str_update.replace(
                    '{0}'.format(check_key), '{0}'.format(value))
        return str_update

    def run(self, str_template, str_dict):
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Parses a Python dictionary and replaces all variables
            within a user-specified template string.

        Parameters
        ----------

        str_dict: dict

            A Python dictionary containing key and values pairs
            corresponding to the available variables within the
            user-specified template string.

        str_template: str

            A Python string specifying the template string to be
            parsed.

        """

        # Update all template strings accordingly.
        str_update = self.write(str_template=str_template,
                                str_dict=str_dict)
        return str_update

# ----


class YAMLTemplate(object):
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

    def write(self, nml_path, nml_template, nml_dict):
        """
        Description
        -----------

        This method ingests a YAML template file and parses a Python
        dictionary containing key and value pairs for template
        variables to be replaced; the updated template to then written
        to the user-specified path.

        Parameters
        ----------

        nml_dict: dict

            A Python dictionary containing key and values pairs
            corresponding to the template variables within the
            user-specified YAML-formatted template file.

        nml_template: str

            A Python string specifying the template variables to be
            sought and updated.

        nml_path: str

            A Python string specifying the path to the YAML-formatted
            output file derived from the template.

        """

        # Read the template file.
        template_matches = ['<', '>']
        with open(nml_template, 'r') as f:
            template = f.read().split('\n')

        # Open and write the namelist file while formatting the
        # template values specified upon entry accordingly.
        with open(nml_path, 'w') as f:
            for item in template:
                for key in nml_dict.keys():
                    if key in item:
                        item = item.replace(
                            '<{0}>'.format(key), str(nml_dict[key]))
                if not any(x in item for x in template_matches):
                    f.write('{0}\n'.format(item))

    def run(self, nml_path, nml_template, nml_dict):
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Parse a YAML-formatted template file and replaces the
            templated variables (defined by < template variable >)
            using the key and value pairs within the user-specified
            Python dictionary.

        (2) Writes the updated template to the user-specified path.

        """

        # Parse the YAML-formatted template file and proceed
        # accordingly.
        self.write(nml_path=nml_path, nml_template=nml_template,
                   nml_dict=nml_dict)
