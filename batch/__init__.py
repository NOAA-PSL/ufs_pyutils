# =========================================================================

# $$$ MODULE DOCUMENTATION BLOCK

# UFS-RNR :: ush/batch/__init__.py

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

    __init__.py

Description
-----------

    This module loads the batch package.

Classes
-------

    BatchError(msg)

        This is the base-class for all exceptions; it is a sub-class
        of Error.

    ProcsLayout(yaml_file, apptype, fcsttype)

        This is the base-class for all processor layout
        determinations.

    Singularity(sif_name, sif_path, path, owner=None)

        This is the base-class for launching all Singularity container
        images.

    SLURM()

        This is the base-class object for all SLURM scheduler
        applications.

Functions
---------

    get_exec_path(exec_yaml, exec_name, check_exist=True)

        This function parses a YAML-formatted file containing
        executable application paths and checks for the specified
        application and optionally checks that the file path exists.

Author(s)
---------

    Henry R. Winterbottom; 23 August 2022

History
-------

    2022-08-23: Henry Winterbottom -- Initial implementation.

"""

# ----

import glob
import itertools
import numpy
import os
import re
import shutil
import subprocess

from produtil.error_interface import Error
from produtil.logger_interface import Logger
from tools import fileio_interface
from tools import parser_interface

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----


class BatchError(Error):
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

        Creates a new BatchError object.

        """
        super(BatchError, self).__init__(msg=msg)

# ----


class ProcsLayout(object):
    """
    Description
    -----------

    This is the base-class for all processor layout determinations.

    Parameters
    ----------

    yaml_file: str

        A Python string containing the file path to YAML-formatted
        file containing the processor layout for the respective
        UFS-RNR forecast application.

    apptype: str

        A Python string specifying the forecast application type; this
        value is either 'bkgrd_forecast' or 'prod_forecast' referring
        to data-assimilation application background forecasts or
        production type forecasts, respectively.

    fcsttype: str

        A Python string specifying the forecast application type; this
        value is either 'deterministic' or 'ensemble' for control-type
        forecasts and ensemble member forecasts, respectively.

    """

    def __init__(self, yaml_file, apptype, fcsttype):
        """
        Description
        -----------

        Creates a new ProcsLayout object.

        """

        # Determine the total number of tasks from the run-time
        # environment.
        self.total_tasks = int(parser_interface.enviro_get(
            envvar='TOTALTASKSrnr'))
        if self.total_tasks is None:
            msg = ('The total number of tasks could not be determined from '
                   'the user environment. Aborting!!!')
            raise BatchError(msg=msg)

        # Define the application type for which to configure the
        # processor layout.
        self.yaml_dict = fileio_interface.read_yaml(
            yaml_file=yaml_file)
        apptype_dict = parser_interface.dict_key_value(
            dict_in=self.yaml_dict, key=apptype, force=True)

        # Determine the supported run-time platform/host attributes.
        platform = parser_interface.enviro_get(
            envvar='PLATFORMrnr')
        if platform is None:
            msg = ('The platform could not be determined from the run-time '
                   'environment. Aborting!!!')
            raise BatchError(msg=msg)
        platform_dict = parser_interface.dict_key_value(
            dict_in=apptype_dict, key=platform, force=True)
        if platform_dict is None:
            msg = ('The processor configuration for application {0} for '
                   'platform {1} could not be determined from the user '
                   'experiment configuration. Aborting!!!'.format(
                       apptype, platform))
            raise BatchError(msg=msg)

        # Define the attributes for the respective application.
        self.fcsttype_dict = parser_interface.dict_key_value(
            dict_in=platform_dict, key=fcsttype)
        fcsttype_list = [fcsttype.lower() for fcsttype in self.fcsttype.keys()]
        if 'atmos' not in self.fcsttype_dict.keys():
            msg = ('The atmosphere model is required of all UFS-RNR '
                   'experiments; please check that the processor '
                   'configuration YAML-formatted file contains the '
                   'atmosphere model processor layout. Aborting!!!')
            raise BatchError(msg=msg)

        # Define the list of allocated cores for the respective
        # application.
        self.core_list = numpy.arange(0, self.total_tasks, 1).tolist()

    def fcst_core_layout(self, model_list, ntiles, coupled=False):
        """
        Description
        -----------

        This method parses the experiment run-time environment and a
        YAML-formatted file containing the forecast tasks processor
        attributes and returns a Python object containing the
        respective UFS-RNR component model processor configuration
        attributes.

        Parameters
        ----------

        model_list: list

            A Python list containing the respective forecast component
            models.

        ntiles: int

            A Python integer specifying the total number of
            cubed-sphere tiles.

        Keywords
        --------

        coupled: bool, optional

            A Python boolean valued variable specifying whether the
            UFS-RNR application is a coupled-model application.

        Returns
        -------

        core_layout_obj: obj

            A Python object containing the UFS-RNR component model
            processor configuration attributes.

        Raises
        ------

        BatchError:

            * raised if the total number of available cores has been
              exceeded by the atmosphere forecast model.

            * raised if the total number of available cores for a
              specified forecast model or application has been
              exceeded.

            * raised if the atmosphere model has not been defined
              within the core/processor layout/topology; the
              atmosphere model (at minimum) is required for all UFS
              applications.

        """

        # Initialize the attributes for the application processor
        # configuration.
        model_list.insert(0, 'io')
        core_layout_attrs = ['total_cores', 'model_core_list']
        core_list = self.core_list
        core_layout_obj = parser_interface.object_define()

        # Loop through each application (i.e., forecast model) and
        # proceed accordingly.
        for model in model_list:
            core_layout_dict = dict()

            # Determine the processor layout for the atmosphere model
            # and proceed accordingly.
            if model.lower() == 'atmos':
                model_dict = parser_interface.dict_key_value(
                    dict_in=self.fcsttype_dict, key=model)
                model_dict = parser_interface.dict_formatter(
                    in_dict=model_dict)
                layout_x = parser_interface.dict_key_value(
                    dict_in=model_dict, key='layout_x')
                layout_y = parser_interface.dict_key_value(
                    dict_in=model_dict, key='layout_y')
                total_cores = (layout_x*layout_y*ntiles)
                model_core_list = list(
                    itertools.islice(core_list, total_cores))
                if len(core_list) >= total_cores:
                    core_list = core_list[total_cores:]
                    core_layout_dict['layout_x'] = layout_x
                    core_layout_dict['layout_y'] = layout_y
                else:
                    msg = ('The total number of available cores has been exceeded by '
                           'the atmosphere forecast model; the total number of cores '
                           'allocated for the task is {0} and the atmosphere model is '
                           'requesting {1} Aborting!!!'.format(self.total_tasks, total_cores))
                    raise BatchError(msg=msg)

            # Determine the processor layout for the I/O tasks.
            elif model.lower() == 'io':
                io_attr_list = ['write_groups', 'write_tasks_per_group']
                model_dict = parser_interface.dict_key_value(
                    dict_in=self.fcsttype_dict, key=model)
                write_tasks_per_group = parser_interface.dict_key_value(
                    dict_in=model_dict, key='write_tasks_per_group')
                value = parser_interface.dict_key_value(
                    dict_in=model_dict, key='write_groups', force=True)
                if value is None:
                    write_groups = 1
                if value is not None:
                    write_groups = value
                total_cores = (write_groups*write_tasks_per_group)
                model_core_list = list(
                    itertools.islice(core_list, total_cores))
                core_list = core_list[total_cores:]
                for item in io_attr_list:
                    core_layout_dict[item] = eval(item)

            # Determine the processor layout for the remaining
            # forecast models and applications and proceed
            # accordingly.
            else:
                if model in self.fcsttype_dict.keys():
                    if coupled:
                        model_dict = parser_interface.dict_key_value(
                            dict_in=self.fcsttype_dict, key=model)
                        total_cores = model_dict
                        model_core_list = list(
                            itertools.islice(core_list, total_cores))
                        if len(core_list) >= total_cores:
                            core_list = core_list[total_cores:]
                        else:
                            msg = ('The total number of available cores has been exceeded by '
                                   'the {0} forecast model; the total number of cores allocated '
                                   'for the task is {1} and the atmosphere model is requesting {2}. '
                                   'Aborting!!!'.format(model, self.total_tasks, total_cores))
                            raise BatchError(msg=msg)
                    if not coupled:
                        break
                else:
                    total_cores = None
                    model_core_list = None

            # Define the core/processor layout attributes.
            for core_layout_attr in core_layout_attrs:
                core_layout_dict[core_layout_attr] = eval(core_layout_attr)
            core_layout_obj = parser_interface.object_setattr(
                object_in=core_layout_obj, key=model, value=core_layout_dict)

        # Check that the atmosphere model is defined within the
        # core/processor layout; the atmosphere model is required for
        # all UFS applications.
        atmos_check = parser_interface.object_getattr(
            object_in=core_layout_obj, key='atmos', force=True)
        if atmos_check is None:
            msg = ('The atmosphere model is required of all UFS-RNR experiments; no '
                   'processor configuration could be determined from the user experiment '
                   'configuration. Aborting!!!')
            raise BatchError(msg=msg)
        return core_layout_obj

# ----


class Singularity(object):
    """
    Description
    -----------

    This is the base-class for launching all Singularity container
    images.

    Parameters
    ----------

    sif_name: str

        A Python string containing the base-name for the Singularity
        container image.

    sif_path: str

        A Python string containing the Singularity container working
        directory name.

    path: str

        A Python string containing the platform working directory
        path; this is the path that is bound to the Singularity
        container image working directory name.

    Keywords
    --------

    owner: str, optional

        A Python string containing a group on the respective platform
        that has Singularity permissions; this is useful for when only
        certain users/groups on a platform have Singularity
        permissions and can provide an override.

    envvar_dict: dict, optional

        A Python dictionary containing key (environment variable
        names) and values (environment variable values) for the
        Singularity container application.

    """

    def __init__(self, sif_name, sif_path, path, owner=None,
                 envvar_dict=None):
        """
        Description
        -----------

        Creates a new Singularity object.

        """

        # Define the base-class attributes.
        attrs_list = ['envvar_dict', 'owner', 'path', 'sif_name',
                      'sif_path']
        for item in attrs_list:
            self = parser_interface.object_setattr(
                object_in=self, key=item, value=eval(item))
        self.sif_obj = parser_interface.object_define()
        self.check_singularity_exists()

    def check_singularity_exists(self):
        """
        Description
        -----------

        This method checks whether the Singularity application is
        available on the respective platform.

        Raises
        ------

        BatchError:

            * raised if the Singularity executable cannot be
              determined for the respective platform and/or run-time
              environment.

        """

        # Determine the Singularity executable for the respective
        # platform and run-time environment.
        cmd = ['which', 'singularity']
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = proc.communicate()
        if len(out) > 0:
            singularity = out.rstrip().decode('UTF-8')
            kwargs = {'object_in': self.sif_obj, 'key': 'singularity',
                      'value': singularity}
            self.sif_obj = parser_interface.object_setattr(
                object_in=self.sif_obj, key='singularity', value=singularity)
        else:
            msg = ('The Singularity executable could not be located on '
                   'on the respective platform; singularity applications '
                   'cannot be performed. Aborting!!!')
            raise BatchError(msg=msg)

    def launch(self, cmd):
        """
        Description
        -----------

        This method launches the Singularity container image using the
        commands string arguments (cmd).

        Parameters
        ----------

        cmd: list

            A Python list containing the commands for launching the
            respective Singularity container image.

        Raises
        ------

        BatchError:

            * raised if the Singularity container application returns
              a non-zero code (i.e., failed).

        """

        # Launch the Singularity container application.
        proc = subprocess.Popen(cmd)
        proc.wait()
        proc.communicate()
        if proc.returncode != 0:
            msg = ('Singularity image failed! Aborting!!!')
            raise BatchError(msg=msg)

    def run(self):
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Builds the subprocess module commands required to launch
            the Singularity container image application.

        (2) Launches the Singularity container image application.

        """

        # Build the Singularity container command line arguments.
        if self.owner is not None:
            path = os.path.join(self.path, self.sif_name)
            shutil.chown(path=path, group=self.owner)
        cmd = ['{0}'.format(self.sif_obj.singularity),
               'run', '--bind',
               '{0}:/{1}'.format(self.path, self.sif_path),
               '{0}'.format(self.sif_name)]

        # Define the environment variables to be passed to the
        # Singularity container application.
        if self.envvar_dict is not None:
            envvar_list = list()
            for key in self.envvar_dict.keys():
                value = self.envvar_dict[key]
                envvar_list.append('env')
                envvar_list.append('{0}={1}'.format(key, value))
            cmd = envvar_list + cmd

        # Launch the Singularity application container.
        self.launch(cmd=cmd)

# ----


class SLURM(object):
    """
    Description
    -----------

    This is the base-class object for all SLURM scheduler
    applications.

    Raises
    ------

    BatchError:

        * raised if the total number of tasks for the respective
          application could not be determined from the run-time
          environment.

    """

    def __init__(self):
        """
        Description
        -----------

        Creates a new SLURM object.

        """

        # Define the base-class attributes.
        self.total_tasks = int(parser_interface.enviro_get(
            envvar='TOTALTASKSrnr'))
        if self.total_tasks is None:
            msg = ('The total number of tasks could not be determined from '
                   'the user environment. Aborting!!!')
            raise BatchError(msg=msg)

        # Determine the executable for to be used for launching the
        # respective batch job.
        exeopts_list = ['MPIRUNrnr']
        for exeopt in exeopts_list:
            value = parser_interface.enviro_get(envvar=exeopt)
            if value is None:
                self = parser_interface.object_setattr(
                    object_in=self, key=exeopt.lower(), value=False)
            if value is not None:
                self = parser_interface.object_setattr(
                    object_in=self, key=exeopt.lower(), value=value)

    def hostfile(self, path):
        """
        Description
        -----------

        This method collects the list of host names corresponding to
        allocated tasks/cores specified by the user environment.

        Parameters
        ----------

        path: str

           A Python string specifying the path to the external file to
           contain the list of host names corresponding to the
           allocated tasks/cores.

        Raises
        ------

        BatchError:

            * raised if the SLURM hostfile executable cannot be
              determined for the respective platform.

        """

        # Define the hostname executable for the respective platform
        # and proceed accordingly.
        cmd = ['which', 'hostname']
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = proc.communicate()
        if len(out) > 0:
            hostname = out.rstrip().decode('utf-8')
        else:
            msg = ('The SLURM hostfile executable could not be determined for '
                   'your system. Aborting!!!')
            raise BatchError(msg=msg)

        # Define the command required to collect the hostfile
        # information for the respective platform and proceed
        # accordingly.
        if self.mpirunrnr:
            cmd = ['mpiexec', '-l', '{0}'.format(hostname)]
        if not self.mpirunrnr:
            cmd = ['srun', '-l', '{0}'.format(hostname)]
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, err) = proc.communicate()

        # Write the hostfile list to the specified external file.
        with open(path, 'w') as f:
            if len(out) > 0:
                for item in out.splitlines(True):
                    host = item.decode('utf-8').split('\n')[0].split()[1]
                    f.write('{0}\n'.format(host))

    def launch(self, cmd, infile, outlog, errlog):
        """
        Description
        -----------

        This method launches the command string arguments (cmd) and
        writes the output and error to the outlog and errlog paths; if
        outlog and/or errlog are NoneType, they default to out.log
        and/or err.log, respectively; if an error is encountered, this
        method throws a BatchError exception.

        Parameters
        ----------

        cmd: list

            A Python list containing the SLURM commands for launching
            the respective executable task.

        infile: str

            A Python string specifying the path to a file to be opened
            and used as input to the respective executable; if
            NoneType upon entry, the stdin argument to the subprocess
            Popen object is ignored; this parameter may also contain
            wildcard (e.g., *) values; if wildcards are present, the
            Python glob library is used to collect the relevant files
            and the collected files are then appended to the command
            string; for wildcard instances, the parameter shell is
            passed to the subprocess object and set to True.

        outlog: str

            A Python string specifying the path to the standard-output
            (e.g., stdout) information; if NoneType upon entry, the
            stdout is written to out.log.

        errlog: str

            A Python string specifying the path to the error-output
            (e.g., stderr) information; if NoneType upon entry, the
            stderr is written to err.log.

        Raises
        ------

        BatchError:

            * raised if the respective executable application fails.

        """

        # Define and open the stdout (standard out) and stderr
        # (standard error) file paths.
        if outlog is None:
            outlog = 'out.log'
        stdout = open(outlog, 'w')
        if errlog is None:
            errlog = 'err.log'
        stderr = open(errlog, 'w')

        # Check whether the executable input file contains any
        # wildcard values.
        if infile is not None:
            has_wildcards = re.search(r'[^.]\*', infile)
            if has_wildcards:
                stdin = glob.glob(infile)
            if not has_wildcards:
                stdin = open(infile, 'r')

        # Launch the respective executable and proceed accordingly.
        try:
            if infile is None:
                proc = subprocess.Popen(cmd, stdout=stdout, stderr=stderr)
            if infile is not None:

                # Build the command line arguments assuming that
                # wildcard values are included.
                if has_wildcards:

                    # Build the command line arguments for the
                    # respective application.
                    cmd_string = str()
                    for item in cmd:
                        cmd_string = cmd_string + '{0} '.format(item)
                    for item in stdin:
                        cmd_string = cmd_string + '{0} '.format(item)

                    # Execute the application accordingly.
                    proc = subprocess.Popen(cmd_string, stdout=stdout,
                                            stderr=stderr, shell=True)

                # Build the command line arguments assuming that no
                # wildcard values are included.
                if not has_wildcards:
                    proc = subprocess.Popen(
                        cmd, stdin=stdin, stdout=stdout, stderr=stderr)

            # Launch the executable and proceed accordingly.
            proc.wait()
            proc.communicate()
        except Exception as msg:
            raise BatchError(msg=msg)

        # Close the stdout and stderr files and proceed accordingly.
        stderr.close()
        stdout.close()
        if (infile is not None) and (not has_wildcards):
            stdin.close()
        if proc.returncode != 0:
            msg = ('Executable failed! Please refer to {0} for more '
                   'information. Aborting!!!'.format(errlog))
            raise BatchError(msg=msg)

    def run(self, exe, ntasks=None, args=None, infile=None, outlog=None,
            errlog=None, multi_prog=False, multi_prog_conf=None):
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Builds the subprocess module commands, including the SLURM
            loader and executable instructions.

        (2) Launches the executable task assuming the attributes of
            the SLURM loader.

        Parameters
        ----------

        exe: str

            A Python string specifying the path to the executable to
            be launched.

        Keywords
        --------

        ntasks: int, optional

            A Python integer specifying the number of compute tasks;
            if NoneType upon entry, a default value of 1 is assumed.

        args: list, optional

            A Python list of arguments to be passed to the executable
            via the command line parser; if NoneType upon entry, no
            command line arguments are assumed.

        infile: str, optional

            A Python string specifying the path to a file to be open
            and used as input to the respective executable; if
            NoneType upon entry, the stdin argument to the subprocess
            Popen object is ignored.

        outlog: str, optional

            A Python string specifying the path to the standard-output
            (e.g., stdout) information; if NoneType upon entry, the
            stdout is written to out.log.

        errlog: str, optional

            A Python string specifying the path to the error-output
            (e.g., stderr) information; if NoneType upon entry, the
            stderr is written to err.log.

        multi_prog: bool, optional

            A Python boolean valued variable specifying whether to
            implement the SLURM multi_prog capabilities for the
            respective task; if True, multi_prog_conf must be
            specified; note that is not (yet) supported for MVAPICH
            run-time configurations/executables.

        multi_prog_conf: str, optional

            A Python string specifying the path to the file containing
            the SLURM multi_prog directives; if multi_prog (above) is
            True, this value is required; note that is not (yet)
            supported for MVAPICH run-time configurations/executables.

        Raises
        ------

        BatchError:

            * raised if a specified configuration is not supported.

        """
        # Define the command line arguments for the respective
        # parallel executables executable.
        cmd = list()

        # Initialize the command line arguments assuming the MVAPICH
        # parallel task executable.
        if self.mpirunrnr:
            if multi_prog:
                msg = ('Multi-processor configurations are not currently '
                       'available for MVAPICH. Aborting!!!')
                raise BatchError(msg=msg)
            if not multi_prog:
                cmd.append('mpiexec')

        # Initialize the command line arguments assuming the SLURM
        # parallel task executable and proceed accordingly.
        if not self.mpirunrnr:
            cmd.append('srun')
            if ntasks is None:
                ntasks = 1
            cmd.append('--ntasks={0}'.format(ntasks))
        if multi_prog:
            if multi_prog_conf is None:
                msg = ('For multi_prog implementation, a configuration '
                       'file containing the multi-task paritioning is '
                       'required and instead, got NoneType. Aborting!!!')
                raise BatchError(msg=msg)
            cmd.append('--multi-prog')
            cmd.append('{0}'.format(multi_prog_conf))
        if not multi_prog:
            cmd.append('{0}'.format(exe))
            if args is not None:
                for item in args:
                    cmd.append('{0}'.format(item))

        # Launch the parallel task executable.
        self.launch(cmd=cmd, infile=infile, outlog=outlog, errlog=errlog)

# ----


def get_exec_path(exec_yaml, exec_name, check_exist=True):
    """
    Description
    -----------

    This function parses a YAML-formatted file containing executable
    application paths and checks for the specified application and
    optionally checks that the file path exists.

    Parameters
    ----------

    exec_yaml: str

        A Python string specifying the path to the YAML-formatted file
        containing the executable application paths.

    exec_name: str

        A Python string specifying the executable application name;
        this string is used to collect the respective path
        corresponding the executable application.

    Keywords
    --------

    check_exist: bool, optional

        A Python boolean valued variable specifying whether to check
        that the executable application path is valid (i.e., exists).

    Returns
    -------

    exec_path: str

        A Python string specifying the path to the executable
        application.

    Raises
    ------

    BatchError:

        * raised if the requested executable application could not be
          determined from the YAML-formatted file containing the
          executable application paths.

        * (optionally) raised if the path for the requested executable
          application does not exist.

    """

    # Collect the executables information from the user experiment
    # configuration.
    exec_dict = fileio_interface.read_yaml(yaml_file=exec_yaml)

    # Collect the path to the respective executable; proceed
    # accordingly.
    exec_path = parser_interface.dict_key_value(
        dict_in=exec_dict, key=exec_name, force=True, no_split=True)
    if exec_path is None:
        msg = ('The attribute {0} could not be determined from the '
               'executables configuration file {1}. Aborting!!!'
               .format(exec_name, exec_yaml))
        raise BatchError(msg=msg)

    # Check that the executable path exists; proceed accordingly.
    if check_exist:
        exist = fileio_interface.fileexist(path=exec_path)
        if not exist:
            msg = ('The executable file path {0} does not exist. Aborting!!!'.
                   format(exec_path))
            raise BatchError(msg=msg)

    return exec_path
