# =========================================================================

# Module: execute/subprocess_interface.py

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

    subprocess_interface.py

Description
-----------

    This module provides an interface to launch supported job types
    for the respective platform using the Python subprocess library.

Functions
---------

    __job_info__(job_type, app=None)

        This function defines the launcher and task attributes for the
        job type specified upon entry.

    _launch(cmd, infile, errlog, outlog)

        This function launches the command string arguments (cmd) and
        writes the output and error to the outlog and errlog paths; if
        errlog and/or outlog are NoneType, they default to err.log
        and/or out.log, respectively; if an exception is encountered,
        this function raises SubprocessInterfaceError.

    run(exe, job_type="slurm", ntasks=1, args=None, infile=None, errlog=None,
        outlog=None, multi_prog=False, multi_prog_conf=None)

        This function launches a job application in accordance with
        the parameters received upon entry.

Author(s)
---------

    Henry R. Winterbottom; 31 December 2022

History
-------

    2022-12-31: Henry Winterbottom -- Initial implementation.

"""

# ----

# pylint: disable=broad-except
# pylint: disable=consider-using-with
# pylint: disable=raise-missing-from
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches

# ----

import glob
import re
import subprocess
from typing import List, Tuple

from tools import system_interface
from utils.exceptions_interface import SubprocessInterfaceError
from utils.logger_interface import Logger

# ----

# Define all available functions.
__all__ = ["run"]

# ----

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"

# ----

# Define the supported job types.
job_types_list = ["app", "python", "slurm"]

# ----


def __job_info__(job_type: str, app: str = None) -> Tuple:
    """
    Description
    -----------

    This function defines the launcher and task attributes for the job
    type specified upon entry.

    Parameters
    ----------

    job_type: str

        A Python string specifying the job type.

    Keywords
    --------

    app: str

        A Python string specifying the application name; required only
        if job_type is "app" upon entry.

    Returns
    -------

    launcher: str

        A Python string specifying the path to the respective
        supported job type application launcher for the respective
        platform.

    ntasks: str

        A Python string specifying the number of tasks attribute for
        the respective application launcher.

    Raises
    ------

    SubprocessInterfaceError:

        * raised if the job type specified upon entry is not
          supported.

        * raised if an exception is encountered while determing the
          application launcher; this is currently only relative to
          SLURM.

        * raised if the launcher for the respective job type is
          NoneType following assignment.

    """

    # Check that the job type is supported; proceed accordingly.
    if job_type.lower() not in job_types_list:
        msg = f"The job type {job_type.lower()} is not supported. Aborting!!!"
        raise SubprocessInterfaceError(msg=msg)

    msg = f"Configuring {job_type} type jobs."
    logger.info(msg=msg)

    # Define the job attributes for application job types.
    if job_type.lower() == "app":
        (launcher, tasks) = [app, None]

    # Define the job attributes for Python job types.
    if job_type.lower() == "python":
        launcher = system_interface.get_app_path(app="python")
        tasks = None

    # Define job attributes for SLURM workload scheduler job types.
    if job_type.lower() == "slurm":

        try:
            launcher = system_interface.get_app_path(app="srun")
            tasks = "--ntasks"

        except Exception as error:
            msg = (
                "Determining the application launcher for SLURM "
                f"failed with error {error}. Aborting!!!"
            )
            raise SubprocessInterfaceError(msg=msg)

    # Check that the launcher type has been determined from the run
    # time environment; proceed accordingly.
    if job_type.lower() != "app":
        if launcher is None:
            msg = (
                f"The path for job type {job_type} launcher could not be "
                "determined for the respective platform. Aborting!!!"
            )
            raise SubprocessInterfaceError(msg=msg)

    return (launcher, tasks)


# ----


def _launch(cmd: List, infile: str, errlog: str, outlog: str) -> int:
    """
    Description
    -----------

    This function launches the command string arguments (cmd) and
    writes the output and error to the outlog and errlog paths; if
    errlog and/or outlog are NoneType, they default to err.log and/or
    out.log, respectively; if an exception is encountered, this
    function raises SubprocessInterfaceError.

    Parameters
    ----------

    cmd: list

        A Python list containing the SLURM commands for launching the
        respective executable task.

    infile: str

        A Python string specifying the path to a file to be opened and
        used as input to the respective executable; if NoneType upon
        entry, the stdin argument to the subprocess Popen object is
        ignored; this parameter may also contain wildcard (e.g., *)
        values; if wildcards are present, the Python glob library is
        used to collect the relevant files and the collected files are
        then appended to the command string; for wildcard instances,
        the parameter shell is passed to the subprocess object and set
        to True.

    errlog: str

        A Python string specifying the path to the error-output (e.g.,
        stderr) information; if NoneType upon entry, the stderr is
        written to err.log.

    outlog: str

        A Python string specifying the path to the standard-output
        (e.g., stdout) information; if NoneType upon entry, the stdout
        is written to out.log.

    Returns
    -------

    returncode: int

        A Python integer specifying the return code provided by the
        subprocess command.

    Raises
    ------

    SubprocessInterfaceError:

        * raised if an exception is encountered during the launch of
          the respective application.

    """

    # Define and open the stdout (standard out) and stderr (standard
    # error) file paths.
    if outlog is None:
        outlog = "out.log"
    stdout = open(outlog, "w", encoding="utf-8")

    if errlog is None:
        errlog = "err.log"
    stderr = open(errlog, "w", encoding="utf-8")

    # Check whether the executable input file contains any
    # wildcard values.
    if infile is not None:
        has_wildcards = re.search(r"[^.]\*", infile)
        if has_wildcards:
            stdin = glob.glob(infile)
        if not has_wildcards:
            stdin = open(infile, "r", encoding="utf-8")

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
                    cmd_string = cmd_string + f"{item} "
                for item in stdin:
                    cmd_string = cmd_string + f"{item} "

                # Execute the application accordingly.
                proc = subprocess.Popen(
                    cmd_string, stdout=stdout, stderr=stderr, shell=True
                )

            # Build the command line arguments assuming that no
            # wildcard values are included.
            if not has_wildcards:
                proc = subprocess.Popen(
                    cmd, stdin=stdin, stdout=stdout, stderr=stderr)

        # Launch the executable and proceed accordingly.
        proc.wait()
        proc.communicate()
        returncode = proc.returncode

    except Exception as msg:
        raise SubprocessInterfaceError(msg=msg)

    # Close the stdout and stderr files and proceed accordingly.
    stderr.close()
    stdout.close()

    if (infile is not None) and (not has_wildcards):
        stdin.close()

    if returncode != 0:
        msg = (
            f"Executable failed! Please refer to {errlog} for more "
            "information. Aborting!!!"
        )
        raise SubprocessInterfaceError(msg=msg)

    return returncode


# ----


def run(
    exe,
    job_type: str = "slurm",
    ntasks: int = 1,
    args: List = None,
    infile: str = None,
    errlog: str = None,
    outlog: str = None,
    multi_prog: bool = False,
    multi_prog_conf: str = None,
) -> int:
    """
    Description
    -----------

    This function launches a job application in accordance with the
    parameters received upon entry.

    Parameters
    ----------

    exe: str

        A Python string specifying the path to the application to be
        launched.

    Keywords
    --------

    job_type: str, optional

        A Python string specifying the job type; this applies to
        workload scheduler (e.g., SLURM, PBS, SGE, etc.,).

    ntasks: int, optional

        A Python integer specifying the number of compute tasks; if
        NoneType upon entry, a default value of 1 is assumed.

    args: list, optional

        A Python list of arguments to be passed to the executable via
        the command line parser; if NoneType upon entry, no command
        line arguments are assumed.

    infile: str, optional

        A Python string specifying the path to a file to be open and
        used as input to the respective executable; if NoneType upon
        entry, the stdin argument to the subprocess Popen object is
        ignored.

    outlog: str, optional

        A Python string specifying the path to the standard-output
        (e.g., stdout) information; if NoneType upon entry, the stdout
        is written to out.log.

    errlog: str, optional

        A Python string specifying the path to the error-output (e.g.,
        stderr) information; if NoneType upon entry, the stderr is
        written to err.log.

    multi_prog: bool, optional

        A Python boolean valued variable specifying whether to
        implement the SLURM multi_prog capabilities for the respective
        task; if True, multi_prog_conf must be specified; note that is
        not (yet) supported for MVAPICH at run-time
        configurations/executables.

    multi_prog_conf: str, optional

        A Python string specifying the path to the file containing the
        SLURM multi_prog directives; if multi_prog (above) is True,
        this value is required; note that is not (yet) supported for
        MVAPICH run-time configurations/executables.

    Returns
    -------

    returncode: int

        A Python integer specifying the return code provided by the
        subprocess command.

    Raises
    ------

    SubprocessInterfaceError:

        * raised if a specified configuration is not supported.

    """

    # Check that the parameter and keyword values are valid; proceed
    # accordingly.
    if job_type.lower() != "slurm":

        # Reset the parameter and keywork values accordingly.
        if multi_prog:

            msg = (
                "Multiple program support is not available for "
                "workload managers other than SLURM; resetting value "
                "for multi_prog to False; this may cause some unexpected "
                "results."
            )
            logger.warn(msg=msg)
            multi_prog_conf = None

    # Define the command line arguments for the respective
    # launcher application; proceed accordingly.
    cmd = []
    (launcher, tasks) = __job_info__(job_type=job_type, app=exe)

    # Define the launcher for the respective job type; proceed
    # accordingly.
    if launcher is None:
        msg = ("The launcher application cannot be NoneType upon entry."
               "Aborting!!!"
               )
        raise SubprocessInterfaceError(msg=msg)

    if launcher is not None:
        if tasks is None:
            cmd.append(f"{launcher}")

        if tasks is not None:
            for item in [f"{launcher}", f"{tasks}", f"{ntasks}"]:
                cmd.append(item)

    if job_type.lower() != "app":
        cmd.append(exe)

    # Check that the multi-prog capabilities are supported; proceed
    # accordingly; currently this is only supported for SLURM job
    # types.
    if multi_prog:
        if multi_prog_conf is None:
            msg = (
                "For multiple program support (e.g., multi_prog implementation) "
                ", a configuration file containing the multi-task paritioning "
                f"required; got {multi_prog_conf} for parameter multi_prog_conf "
                "upon entry. Aborting!!!"
            )
            raise SubprocessInterfaceError(msg=msg)

        for item in ["--multi-prog", f"{multi_prog_conf}", f"{exe}"]:
            cmd.append(item)

    if not multi_prog:
        if args is not None:
            for item in args:
                cmd.append(f"{item}")

    # Remove any NoneType instances from the command line string.
    cmd = list(item for item in cmd if item is not None)

    # Launch the respective application.
    returncode = _launch(cmd=cmd, infile=infile, errlog=errlog, outlog=outlog)

    return returncode
