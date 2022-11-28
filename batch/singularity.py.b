# =========================================================================

# $$$ MODULE DOCUMENTATION BLOCK

# UFS-RNR :: ush/batch/singularity.py

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


"""

# ----

import os
import subprocess

from produtil.error_interface import Error
from produtil.logger_interface import Logger
from tools import datetime_interface
from tools import parser_interface

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

# Define all available functions.
__all__ = ['run'
           ]

# ----

logger = Logger()

# ----


class SingularityError(Error):
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

        Creates a new SingularityError object.

        """
        super(SingularityError, self).__init__(msg=msg)

# ----


def _build_appcmds(container, path, exec_launcher, exec_ntasks,
                   root_path, exec_launcher_flags=None, exec_cmds=None):
    """ """

    # Initialize the commands for the Singularity container
    # application.
    app_cmds = ['{0}'.format(singularity),
                'exec',
                '{0}'.format(container),
                '--bind',
                '{0}:{1}'.format(path, root_path),
                '{0}'.format(exec_launcher),
                '-n',
                '{0}'.format(int(exec_ntasks)),
                ]

    # Append (any) application launcher flags to the Singularity
    # container application.
    if exec_launcher_flags is not None:

        for exec_launcher_flag in exec_launcher_flags:
            app_cmds.append('{0}'.format(exec_launcher_flag))

    # Define the executable application to be launched within the
    # Singularity container; proceed accordingly.
    exec_app_path = parser_interface.dict_key_value(
        dict_in=exec_dict, key='exec_app_path', force=True,
        no_split=None)
    if exec_app_path is None:
        msg = ('The executable application path could not be determined '
               'from the user experiment configuration. Aborting!!!')
        raise SingularityError(msg=msg)

    app_cmds.append('{0}'.format(exec_app_path))

    # Append (any) executable application commands to the Singularity
    # container application.
    if exec_cmds is not None:

        for exec_cmd in execs_cmds:
            app_cmds.append('{0}'.format(exec_cmd))

    return app_cmds

# ----


def _build_runscript(container, script, path, **kwargs):
    """ """

    # Collect the path for the Singularity application executable
    # path.
    singularity = _check_singularity_env()

    # Collect the necessary attributes from the key-ord arguments.
    run_script_attrs_list = ['app_args',
                             'app_launch',
                             'app_path'
                             ]

    run_script_obj = parser_interface.object_define()
    for run_script_attr in run_script_attrs_list:

        # Collect the respective attribute from the keyword arguments;
        # proceed accordingly.
        value = parser_interface.dict_key_value(
            dict_in=kwargs, key=run_script_attr, force=True, no_split=True)
        if value is None:
            msg = ('The attribute {0} has not provided within the keyword '
                   'arguments and will not be included.'.format(run_script_attr))
            logger.warn(msg=msg)

        run_script_obj = parser_interface.object_setattr(
            object_in=run_script_obj, key=run_script_attr, value=value)

    # Define the Singularity command to be used to execute the
    # respective container application; proceed accordingly.

    print(all([parser_interface.object_getattr(object_in=run_script_obj,
                                               key=app_attr) is None for app_attr in vars(run_script_obj).keys()]))

    if all([parser_interface.object_getattr(
            object_in=run_script_obj, key=app_attr) is None
            for app_attr in vars(run_script_obj).keys()]):

        # Define the Singularity command.
        command = 'run'

    else:

        # Define the Singularity command.
        command = 'exec'

    # Write the bash-formatted script containing the Singularity
    # container application instructions.
    msg = ('Writing Singularity container application instructions to {0}.'
           .format(script))
    logger.info(msg=msg)
    cmd = str()
    with open(script, 'w') as f:
        f.write('#!/bin/bash --norc --noprofile -posix\n')
        f.write('cd {0}\n'.format(path))
        cmd = cmd + '{0} {1} {2}'.format(singularity, command, container)

        if run_script_obj.app_launch is not None:
            for item in run_script_obj.app_launch:

                cmd = cmd + '{0}'.format(item)

        if run_script_obj.app_path is not None:
            for item in run_script_obj.app_path:

                cmd = cmd + '{0}'.format(item)

        if run_script_obj.app_args is not None:
            for item in run_script_obj.app_path:

                cmd = cmd + '{0}'.format(item)

        # Write the application command/attributes to the
        # bash-formatted script file.
        f.write('{0}\n'.format(cmd))
        current_date = datetime_interface.current_date(
            frmttyp='%H:%M:%S %A %B %d, %Y')
        f.write('\n# Created: {0}'.format(current_date))

# ----


def _check_singularity_env():
    """
    Description
    -----------

    This function parses the run-time environment for the Singularity
    application executable path.

    Returns
    -------

    singularity: str

        A Python string specifying the path to the Singularity
        application executable.

    Raises
    ------

    SingularityError:

        * raised if the Singularity application executable path cannot
          be determined for the respective run-time environment.

    """

    # Check the run-time environment in order to determine the
    # Singularity executable path; proceed accordingly.
    cmd = ['which',
           'singularity'
           ]

    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if len(out) > 0:
        singularity = out.rstrip().decode('utf-8')

    else:
        msg = ('The Singularity executable could not be determined '
               'for the system. Aborting!!!')
        raise SingularityError(msg=msg)

    return singularity

# ----


def _check_container_execpath(container, name_exec):
    """ """

    # Define the path to the Singularity executable.
    singularity = _check_singularity_env()

    # Determine the executable path within the container.
    cmd = ['{0}'.format(singularity),
           'run',
           '{0}'.format(container),
           'which',
           '{0}'.format(name_exec)
           ]

    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, err) = proc.communicate()
    if len(out) > 0:
        singularity = out.rstrip().decode('utf-8')

    else:
        msg = ('The file {0} could not be found in the environment '
               'for container {1} . Aborting!!!'.format(name_exec,
                                                        container))
        raise SingularityError(msg=msg)

    return path_exec

# ----


def _launch_app(app_cmds, path, errlog=None, outlog=None):
    """
    Description
    -----------

    This function attempts to launch the specified directives (i.e.,
    app_cmds; application) within specified Singularity container.

    Parameters
    ----------

    app_cmds: list

        A Python list of commands for the Python subprocess library
        interface.

    path: str

        A Python string specifying the path in which the respective
        Singularity container is to be executed.

    Keywords
    --------

    errlog: str, optional

        A Python string specifying the path to which to write the
        standard error (e.g., stderr) for the Singularity container
        application execution; if NoneType upon entry this defaults to
        err.log in the Singularity container application run path
        (i.e., the path attribute).

    outlog: str, optional

        A Python string specifying the path to which to write the
        standard output (e.g., stdout) for the Singularity container
        application execution; if NoneType upon entry this defaults to
        out.log in the Singularity container application run path
        (i.e., the path attribute).

    Raises
    ------

    SingularityError:

        * raised if an error is encountered while launching the
          respective application within the Singularity container.

    """

    # Define and open the stderr (standard error) and stdout (standard
    # output) file paths.
    if errlog is None:
        errlog = os.path.join(path, 'err.log')
    stderr = open(errlog, 'w')

    if outlog is None:
        outlog = os.path.join(path, 'out.log')
    stdout = open(outlog, 'w')

    msg = ('The standard error will be written to {0}.'.format(errlog))
    logger.warn(msg=msg)
    msg = ('The standard output will be written to {0}.'.format(outlog))
    logger.warn(msg=msg)

    # Launch the Singularity container application.
    proc = subprocess.Popen(app_cmds, stdout=stdout, stderr=err)
    proc.wait()
    proc.communicate()

    # Close the stdout and stderr files and proceed accordingly.
    stderr.close()
    stdout.close()
    if proc.returncode != 0:
        msg = ('Singularity application failed! Please refer to {0} for more '
               'information. Aborting!!!'.format(errlog))
        raise SingularityError(msg=msg)

# ----


def run(path, exec_dict, exec_ntasks, errlog=None, exec_cmds=None,
        outlog=None):
    """
    Description
    -----------

    This function provides an interface to the Singularity container
    and the applications within; this is the driver function for
    Singularity.

    Parameters
    ----------

    path: str

        A Python string specifying the path in which the respective
        Singularity container is to be executed.

    exec_dict: dict

        A Python dictionary containing the respective Singularity
        container executable application attributes; this is collected
        from a YAML-formatted configuration file.

    exec_ntasks: int

        A Python integer specifying the total number of compute tasks
        to be used for the respective Singularity container
        application.

    Keywords
    --------

    errlog: str, optional

        A Python string specifying the path to which to write the
        standard error (e.g., stderr) for the Singularity container
        application execution; if NoneType upon entry this defaults to
        err.log in the Singularity container application run path
        (i.e., the path attribute).

    exec_cmds: list, optional

        A Python list of command line arguments to be provided to the
        Singularity container application; if NoneType upon entry it
        is assumed that the respective executable application does not
        require command line arguments.

    outlog: str, optional

        A Python string specifying the path to which to write the
        standard output (e.g., stdout) for the Singularity container
        application execution; if NoneType upon entry this defaults to
        out.log in the Singularity container application run path
        (i.e., the path attribute).

    """

    # Define the Singularity executable path.
    singularity = _check_singularity_env()

    # Define the Singularity container for the respective application;
    # proceed accordingly.
    container = parser_interface.dict_key_value(
        dict_in=exec_dict, key='container', force=True,
        no_split=True)

    if container is None:
        msg = ('The container within which to run the respective '
               'application cannot be determined from the user experiment '
               'configuration. Aborting!!!')
        raise SingularityError(msg=msg)

    exec_launcher_path = _check_container_execpath(container=container,
                                                   name_exec=exec_launcher)

    # Define any flags for the application launcher; proceed accordingly.
    exec_launcher_flags = parser_interface.dict_key_value(
        dict_in=exec_dict, key='exec_launcher_flags', force=True,
        no_split=True)

    # Define the commands for the Singularity container.
    app_cmds = _build_appcmds(container=container, path=path,
                              exec_launcher=exec_launcher,
                              exec_ntasks=exec_ntasks,
                              exec_launcher_flags=exec_launcher_flags,
                              exec_cmds=exec_cmds)

    # Launch the application within the respective Singularity
    # container.
    _launch_app(apps_cmd=apps_cmd, path=path, errlog=errlog, outlog=outlog)
