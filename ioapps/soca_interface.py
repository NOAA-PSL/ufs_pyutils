"""
Module
------

   soca_interface.py

Description
-----------

   This module contains methods for various applications involving the
   Joint Effort for Data-assimilation Integration (JEDI) Sea-ice and
   Ocean Coupled Analysis (SOCA) CICE model fields for
   data-assimilation applications.

Classes
-------

   CICE2SOCA()

       This is the base-class object for all CICE forecast model to
       SOCA file format applications.

   CICEcheckpoint_model(analy_filepath, bkgrd_filepath, output_filepath, 
                        rescale_yaml)

       This is the base-class object for all CICE model SOCA
       checkpoint_model applications

   CICEEnsInitConds()

       This is the base-class object for generating CICE model initial
       condition files from ensemble member files generated by the
       SOCA ensemble perturbations (ens_pert) application.

   CICEState(fname, rescale_yaml, output = None)

       This is the base-class object for the CICE state update
       performed following the SOCA data-assimilation application
       analysis production; this has been adapted from the
       SOCA-science tools/seaice/soca_seaice.py 9dce8a7 stable-nightly
       release tag.

   MOM6EnsInitConds(rescale_yaml)

       This is the base-class object for all Modular Ocean Model
       (MOM6) ensemble member initial condition updates and quality
       checks.

   SOCAInterfaceError(msg)

       This is the base-class for all exceptions; it is a sub-class of
       Error.

Author(s)
--------- 

   Henry R. Winterbottom; 27 May 2021

History
-------

   2021-05-27: Henry Winterbottom -- Initial implementation.

   2022-01-06: Henry Winterbottom -- Updated SOCAInterfaceError class.

"""

# ----

import numbers
import os

import numpy
import produtil
import tools
from produtil.error_interface import Error
from produtil.logger_interface import Logger

import ioapps

logger = Logger()

# ----

__author__ = "Henry R. Winterbottom"
__version__ = "1.0.0"
__maintainer__ = "Henry R. Winterbottom"
__email__ = "henry.winterbottom@noaa.gov"
__status__ = "Development"

# ----


class CICE2SOCA(object):
    """
    Description
    -----------

    This is the base-class object for all CICE forecast model to SOCA
    file format applications.

    """

    def __init__(self):
        """
        Description
        -----------

        Creates a new CICE2SOCA object.

        """
        self.vardict = {"aicen": "aicen", "vicen": "vicen", "vsnon": "vsonn"}

    def build_soca(self):
        """
        Description
        -----------

        This method defines the base-class attribute model_obj which
        contains the CICE state variables converted (e.g., aggregated)
        to the SOCA state variable format.

        """
        aice = numpy.sum(self.model_obj.aicen, axis=0)
        kwargs = {"object_in": self.model_obj, "key": "aice", "value": aice}
        self.model_obj = tools.parser_interface.object_setattr(**kwargs)
        hice = numpy.sum(self.model_obj.vicen, axis=0)
        kwargs = {"object_in": self.model_obj, "key": "hice", "value": hice}
        self.model_obj = tools.parser_interface.object_setattr(**kwargs)
        hsno = numpy.sum(self.model_obj.vsnon, axis=0)
        kwargs = {"object_in": self.model_obj, "key": "hsno", "value": hsno}
        self.model_obj = tools.parser_interface.object_setattr(**kwargs)

    def read_model(self, filepath):
        """
        Description
        -----------

        This method reads a CICE forecast model file generated by the
        respective forecast application and defines a Python object
        containing the respective state variables.

        Parameters
        ----------

        filepath: str

            A Python string specifying the path to CICE forecast model
            file.

        """
        self.model_obj = tools.parser_interface.object_define()
        msg = "Reading CICE model variables from file %s." % filepath
        logger.info(msg=msg)
        ncfile = filepath
        ncvarname = "aicen"
        kwargs = {"ncfile": ncfile, "ncvarname": ncvarname}
        ncvar = numpy.squeeze(ioapps.netcdf4_interface.ncreadvar(**kwargs)[:])
        kwargs = {"object_in": self.model_obj, "key": "aicen", "value": ncvar}
        self.model_obj = tools.parser_interface.object_setattr(**kwargs)
        ncfile = filepath
        ncvarname = "vicen"
        kwargs = {"ncfile": ncfile, "ncvarname": ncvarname}
        ncvar = numpy.squeeze(ioapps.netcdf4_interface.ncreadvar(**kwargs)[:])
        kwargs = {"object_in": self.model_obj, "key": "vicen", "value": ncvar}
        self.model_obj = tools.parser_interface.object_setattr(**kwargs)
        ncfile = filepath
        ncvarname = "vsnon"
        kwargs = {"ncfile": ncfile, "ncvarname": ncvarname}
        ncvar = numpy.squeeze(ioapps.netcdf4_interface.ncreadvar(**kwargs)[:])
        kwargs = {"object_in": self.model_obj, "key": "vsnon", "value": ncvar}
        self.model_obj = tools.parser_interface.object_setattr(**kwargs)
        hicen = numpy.zeros(numpy.shape(self.model_obj.vicen))
        I = numpy.where(self.model_obj.aicen > 0.0)
        hicen = self.model_obj.vicen / self.model_obj.aicen
        kwargs = {"object_in": self.model_obj, "key": "hicen", "value": hicen}
        self.model_obj = tools.parser_interface.object_setattr(**kwargs)
        hsnon = self.model_obj.vsnon / self.model_obj.aicen
        kwargs = {"object_in": self.model_obj, "key": "hsnon", "value": hsnon}
        self.model_obj = tools.parser_interface.object_setattr(**kwargs)

    def write_soca(self, filepath):
        """
        Description
        -----------

        This method writes the netCDF4 formatted SOCA state variable
        file to be used by the respective SOCA data-assimilation
        application.

        Parameters
        ----------

        filepath: str

            A Python string specifying the path to SOCA state variable
            file for the respective SOCA data-assimilation
            application.

        """
        ncfile = filepath
        (ncdim_obj, ncvar_obj) = (
            tools.parser_interface.object_define() for i in range(2)
        )
        xaxis_1 = numpy.shape(self.model_obj.aice)[1]
        kwargs = {"object_in": ncdim_obj, "key": "xaxis_1", "value": xaxis_1}
        ncdim_obj = tools.parser_interface.object_setattr(**kwargs)
        self.xaxis_1 = numpy.ones(xaxis_1)
        yaxis_1 = numpy.shape(self.model_obj.aice)[0]
        kwargs = {"object_in": ncdim_obj, "key": "yaxis_1", "value": yaxis_1}
        ncdim_obj = tools.parser_interface.object_setattr(**kwargs)
        self.yaxis_1 = numpy.ones(yaxis_1)
        time = 1
        kwargs = {"object_in": ncdim_obj, "key": "Time", "value": time}
        ncdim_obj = tools.parser_interface.object_setattr(**kwargs)
        ncvar_dict = {
            "aicen": {
                "varname": "aicen",
                "dims": ["Time", "yaxis_1", "xaxis_1"],
                "type": "float64",
                "values": self.model_obj.aice,
            },
            "hicen": {
                "varname": "hicen",
                "dims": ["Time", "yaxis_1", "xaxis_1"],
                "type": "float64",
                "values": self.model_obj.hice,
            },
            "hsnon": {
                "varname": "hsnon",
                "dims": ["Time", "yaxis_1", "xaxis_1"],
                "type": "float64",
                "values": self.model_obj.hsno,
            },
            "xaxis_1": {
                "varname": "xaxis_1",
                "dims": "xaxis_1",
                "type": "float64",
                "values": self.xaxis_1,
            },
            "yaxis_1": {
                "varname": "yaxis_1",
                "dims": "yaxis_1",
                "type": "float64",
                "values": self.yaxis_1,
            },
        }
        for key in ncvar_dict.keys():
            dict_in = dict()
            for item in ncvar_dict[key].keys():
                kwargs = {"dict_in": ncvar_dict[key], "key": item}
                try:
                    value = tools.parser_interface.dict_key_value(**kwargs)[:]
                    if len(value) == 1:
                        value = value[0]
                except TypeError:
                    value = tools.parser_interface.dict_key_value(**kwargs)
                dict_in[item] = value
            kwargs = {"object_in": ncvar_obj, "key": key, "value": dict_in}
            ncvar_obj = tools.parser_interface.object_setattr(**kwargs)
        msg = "Creating netCDF file %s." % ncfile
        logger.info(msg=msg)
        kwargs = {"ncfile": ncfile, "ncdim_obj": ncdim_obj, "ncvar_obj": ncvar_obj}
        ioapps.netcdf4_interface.ncwrite(**kwargs)

    def run(self, cice_filepath, soca_filepath):
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Reads the CICE state variables from external netCDF
            formatted file.

        (2) Defines the SOCA state vector from the CICE state
            variables.

        (3) Writes a netCDF4 formatted file containing the SOCA state
            variables for the respective SOCA data-assimilation
            application.

        Parameters
        ----------

        cice_filepath: str

            A Python string specifying the path to CICE forecast model
            file.

        soca_filepath: str

            A Python string specifying the path to SOCA state variable
            file for the respective SOCA data-assimilation
            application.

        """
        kwargs = {"filepath": cice_filepath}
        self.read_model(**kwargs)
        self.build_soca()
        kwargs = {"filepath": soca_filepath}
        self.write_soca(**kwargs)


# ----


class CICEcheckpoint_model(object):
    """
    Description
    -----------

    This is the base-class object for all CICE model SOCA
    checkpoint_model applications.

    Parameters
    ----------

    analy_filepath: str

        A Python string specifying the path to SOCA data-assimilation
        application analysis file.

    bkgrd_filepath: str

        A Python string specifying the path to CICE background
        forecast file.

    output_filepath: str

        A Python string specifying the output filepath for the updated
        CICE analysis; this is only used when updating the CICE state
        variables following a SOCA data-assimilation application.

    rescale_yaml: str

        A Python string specifying the path to the external
        YAML-formatted file containing the CICE model SOCA scaling and
        variable values to be used to define the SOCA sea-ice
        analysis.

    """

    def __init__(self, analy_filepath, bkgrd_filepath, output_filepath, rescale_yaml):
        """
        Description
        -----------

        Creates a new CICEcheckpoint_model object.

        """
        kwargs = {
            "fname": bkgrd_filepath,
            "rescale_yaml": rescale_yaml,
            "output": output_filepath,
        }
        self.bkg = CICEState(**kwargs)
        kwargs = {"fname": analy_filepath, "rescale_yaml": rescale_yaml}
        self.ana = CICEState(**kwargs)

    def run(self):
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Reads the CICE state variables from the CICE background
            forecast.

        (2) Converts (e.g., aggregates) the CICE background forecast
            state variables to the SOCA state vector format.

        (3) Reads the SOCA data-assimilation application analysis
            state variables.

        (4) Converts (e.g., deaggregates) the SOCA data-assimilation
            application analysis state variables to CICE state
            variables.

        (5) Updates the CICE background forecast file with the new
            CICE state variable values.

        """
        self.bkg.read_model()
        self.bkg.aggregate()
        self.ana.read_soca()
        self.bkg.balance(self.ana)
        self.bkg.write_cice()


# ----


class CICEEnsInitConds(object):
    """
    Description
    -----------

    This is the base-class object for generating CICE model initial
    condition files from ensemble member files generated by the SOCA
    ensemble perturbations (ens_pert) application.

    """

    def __init__(self):
        """
        Description
        -----------

        Creates a new CICEEnsInitConds object.

        """
        self.analy_vardict = {"aicen": "aicen", "hicen": "hicen", "hsnon": "hsnon"}
        self.analy_obj = tools.parser_interface.object_define()

    def checkpoint_model(self, output_filepath):
        """
        Description
        -----------

        This method performs sanity checks on the respective ensemble
        member analysis file and updates an external netCDF formatted
        file for the respective ensemble member CICE initial
        conditions (output_filepath).

        Parameters
        ----------

        output_filepath: str

            A Python string specifying the path to the netCDF
            formatted CICE model initial condition file for the
            respective ensemble member.

        """
        self.analy_obj.aicen[self.analy_obj.aicen < 0.0] = 0.0
        self.analy_obj.aicen[self.analy_obj.aicen > 1.0] = 1.0
        self.analy_obj.hicen[self.analy_obj.hicen < 0.0] = 0.0
        chkpntmdl_dict = {"aicen": self.analy_obj.aicen, "hicen": self.analy_obj.hicen}
        ncfile = output_filepath
        for key in chkpntmdl_dict.keys():
            ncvarname = key
            msg = "Writing netCDF variable %s to netCDF file %s." % (ncvarname, ncfile)
            logger.info(msg=msg)
            kwargs = {"dict_in": chkpntmdl_dict, "key": key}
            ncvar = tools.parser_interface.dict_key_value(**kwargs)
            kwargs = {"ncfile": output_filepath, "ncvarname": ncvarname, "ncvar": ncvar}
            ioapps.netcdf4_interface.ncwritevar(**kwargs)

    def read_analy(self, analy_filepath):
        """
        Description
        -----------

        This method reads an ensemble member analysis file generated
        by the SOCA ensemble perturbation (enspert) application and
        defines the base-class attribute analy_obj.

        Parameters
        ----------

        analy_filepath: str

            A Python string specifying the path to respective CICE
            ensemble member analysis file specified by the SOCA
            ensemble perturbation (enspert) application.

        """
        msg = "Reading CICE analysis from file %s." % analy_filepath
        logger.info(msg=msg)
        ncfile = analy_filepath
        for key in self.analy_vardict.keys():
            kwargs = {"dict_in": self.analy_vardict, "key": key, "no_split": True}
            ncvarname = tools.parser_interface.dict_key_value(**kwargs)
            kwargs = {"ncfile": ncfile, "ncvarname": ncvarname}
            ncvar = ioapps.netcdf4_interface.ncreadvar(**kwargs)
            kwargs = {"object_in": self.analy_obj, "key": key, "value": ncvar}
            self.analy_obj = tools.parser_interface.object_setattr(**kwargs)

    def setup(self, bkgrd_filepath, analy_filepath, output_filepath):
        """
        Description
        -----------

        This method prepares the working directory for the respective
        CICE ensemble member SOCA checkpoint_model update.

        Parameters
        ----------

        analy_filepath: str

            A Python string specifying the path to respective CICE
            ensemble member analysis file specified by the SOCA
            ensemble perturbation (enspert) application.

        output_filepath: str

            A Python string specifying the path to the netCDF
            formatted CICE model initial condition file; note that
            this file is not generated by SOCA and most often is the
            control member filepath that is used to generate the SOCA
            ensemble using the SOCA ensemble perturbation (ens_pert)
            application.

        output_filepath: str

            A Python string specifying the path to the netCDF
            formatted CICE model initial condition file for the
            respective ensemble member.

        """
        srcfile = bkgrd_filepath
        dstfile = output_filepath
        msg = "Copying file %s to %s." % (srcfile, dstfile)
        logger.info(msg=msg)
        kwargs = {"srcfile": srcfile, "dstfile": dstfile}
        tools.fileio_interface.copyfile(**kwargs)
        kwargs = {"analy_filepath": analy_filepath}
        self.read_analy(**kwargs)

    def run(self, bkgrd_filepath, analy_filepath, output_filepath):
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Prepares the working directory for the respective CICE
            ensemble member initial condition file update.

        (2) Updates the CICE initial condition file using the SOCA
            analysis for the respective ensemble member.

        Parameters
        ----------

        analy_filepath: str

            A Python string specifying the path to respective CICE
            ensemble member analysis file specified by the SOCA
            ensemble perturbation (enspert) application.

        output_filepath: str

            A Python string specifying the path to the netCDF
            formatted CICE model initial condition file; note that
            this file is not generated by SOCA and most often is the
            control member filepath that is used to generate the SOCA
            ensemble using the SOCA ensemble perturbation (ens_pert)
            application.

        output_filepath: str

            A Python string specifying the path to the netCDF
            formatted CICE model initial condition file for the
            respective ensemble member.

        """
        kwargs = {
            "bkgrd_filepath": bkgrd_filepath,
            "analy_filepath": analy_filepath,
            "output_filepath": output_filepath,
        }
        self.setup(**kwargs)
        kwargs = {"output_filepath": output_filepath}
        self.checkpoint_model(**kwargs)


# ----


class CICEState(object):
    """
    Description
    -----------

    This is the base-class object for the CICE state update performed
    following the SOCA data-assimilation application analysis
    production; this has been adapted from the SOCA-science
    tools/seaice/soca_seaice.py 9dce8a7 stable-nightly release tag.

    Parameters
    ----------

    fname: str

        A Python string specifying the path to CICE forecast model
        file.

    rescale_yaml: str

        A Python string specifying the path to the external
        YAML-formatted file containing the CICE model SOCA scaling and
        variable values to be used to define the SOCA sea-ice
        analysis.

    output: str, optional

        A Python string specifying the output filepath for the updated
        CICE analysis; this is only used when updating the CICE state
        variables following a SOCA data-assimilation application.

    """

    def __init__(self, fname, rescale_yaml, output=None):
        """
        Description
        -----------

        Creates a new CICEState object.

        """
        obj_attrs_list = ["fname", "output"]
        for obj_attr in obj_attrs_list:
            kwargs = {"object_in": self, "key": obj_attr, "value": eval(obj_attr)}
            self = tools.parser_interface.object_setattr(**kwargs)
        kwargs = {"yaml_file": rescale_yaml}
        yaml_dict = tools.fileio_interface.read_yaml(**kwargs)
        kwargs = {"dict_in": yaml_dict, "key": "rescale", "no_split": True}
        self.rescale_dict = tools.parser_interface.dict_key_value(**kwargs)

    def aggregate(self):
        """
        Description
        -----------

        This method converts the CICE model state categories to the
        SOCA state vector.

        """
        self.aice = numpy.sum(self.aicen, axis=0)
        self.hice = numpy.sum(self.vicen, axis=0)
        self.hsno = numpy.sum(self.vsnon, axis=0)

    def balance(self, ana):
        """
        Description
        -----------

        This method cleans up and balances (i.e., removes extreme
        values) from the respective SOCA analysis state variables
        converts the SOCA state variables to the respective CICE state
        (e.g., deaggregates).

        Parameters
        ----------

        ana: obj

            A Python object containing the SOCA analysis state
            variables.

        """
        rescale_obj = tools.parser_interface.object_define()
        for key in self.rescale_dict.keys():
            kwargs = {"dict_in": self.rescale_dict, "key": key, "no_split": True}
            value = tools.parser_interface.dict_key_value(**kwargs)
            kwargs = {"object_in": rescale_obj, "key": key, "value": value}
            rescale_obj = tools.parser_interface.object_setattr(**kwargs)
        ana.aice[ana.aice < 0.0] = 0.0
        ana.aice[ana.aice > 1.0] = 1.0
        ana.hice[ana.hice < 0.0] = 0.0
        alpha = numpy.ones(numpy.shape(ana.aice))
        I = numpy.where(self.aice > rescale_obj.minval)
        alpha[I] = ana.aice[I] / self.aice[I]
        alpha[alpha < rescale_obj.alpha_min] = rescale_obj.alpha_min
        alpha[alpha > rescale_obj.alpha_max] = rescale_obj.alpha_max
        self.aicen_ana = self.aicen
        self.aicen_ana = alpha * self.aicen
        self.vicen_ana = self.vicen
        self.vicen_ana = alpha * self.vicen
        self.hice = numpy.sum(self.vicen, axis=0)
        I = numpy.where(self.hice > rescale_obj.minval)
        alpha[I] = ana.hice[I] / self.hice[I]
        alpha[alpha < rescale_obj.alpha_min] = rescale_obj.alpha_min
        alpha[alpha > rescale_obj.alpha_max] = rescale_obj.alpha_max
        self.vicen_ana = alpha * self.vicen
        hice_bad = numpy.sum(self.vicen_ana, axis=0)
        hice_good = numpy.sum(self.vicen_ana, axis=0)
        hice_good[hice_good > 10.0] = 10.0
        I = numpy.where(hice_bad > 10.0)
        alpha = numpy.ones(numpy.shape(ana.aice))
        alpha[I] = hice_good[I] / hice_bad[I]
        alpha[alpha < rescale_obj.alpha_min] = rescale_obj.alpha_min
        alpha[alpha > rescale_obj.alpha_max] = rescale_obj.alpha_max
        self.vicen_ana = alpha * self.vicen_ana

    def read_model(self):
        """
        Description
        -----------

        This method reads a CICE forecast model file generated by the
        respective forecast application and defines a Python object
        containing the respective state variables.

        """
        msg = "Reading CICE model variables from file %s." % self.fname
        logger.info(msg=msg)
        ncfile = self.fname
        ncvarname = "aicen"
        kwargs = {"ncfile": ncfile, "ncvarname": ncvarname}
        ncvar = numpy.squeeze(ioapps.netcdf4_interface.ncreadvar(**kwargs)[:])
        self.aicen = ncvar
        ncfile = self.fname
        ncvarname = "vicen"
        kwargs = {"ncfile": ncfile, "ncvarname": ncvarname}
        ncvar = numpy.squeeze(ioapps.netcdf4_interface.ncreadvar(**kwargs)[:])
        self.vicen = ncvar
        ncfile = self.fname
        ncvarname = "vsnon"
        kwargs = {"ncfile": ncfile, "ncvarname": ncvarname}
        ncvar = numpy.squeeze(ioapps.netcdf4_interface.ncreadvar(**kwargs)[:])
        self.vsnon = ncvar
        self.hicen = numpy.zeros(numpy.shape(self.vicen))
        I = numpy.where(self.aicen > 0.0)
        self.hicen = self.vicen / self.aicen
        self.hsnon = self.vsnon / self.aicen

    def read_soca(self):
        """
        Description
        -----------

        This method reads the state vector from the CICE aggregated
        file provided to SOCA.

        """
        msg = "Reading SOCA variables from file %s." % self.fname
        logger.info(msg=msg)
        ncfile = self.fname
        ncvarname = "aicen"
        kwargs = {"ncfile": ncfile, "ncvarname": ncvarname}
        ncvar = numpy.squeeze(ioapps.netcdf4_interface.ncreadvar(**kwargs)[:])
        self.aice = ncvar
        ncfile = self.fname
        ncvarname = "hicen"
        kwargs = {"ncfile": ncfile, "ncvarname": ncvarname}
        ncvar = numpy.squeeze(ioapps.netcdf4_interface.ncreadvar(**kwargs)[:])
        self.hice = ncvar
        ncfile = self.fname
        ncvarname = "hsnon"
        kwargs = {"ncfile": ncfile, "ncvarname": ncvarname}
        ncvar = numpy.squeeze(ioapps.netcdf4_interface.ncreadvar(**kwargs)[:])
        self.hsno = ncvar

    def write_cice(self):
        """
        Description
        -----------

        This method copies the original CICE background file and
        updates the respective CICE state variables using the
        deaggregated SOCA state vector.

        """
        ncfile = self.output
        ncvarname = "aicen"
        msg = "Updating CICE variable %s." % ncvarname
        logger.info(msg=msg)
        ncvar = self.aicen_ana
        kwargs = {"ncfile": ncfile, "ncvarname": ncvarname, "ncvar": ncvar}
        ioapps.netcdf4_interface.ncwritevar(**kwargs)
        ncfile = self.output
        ncvarname = "vicen"
        msg = "Updating CICE variable %s." % ncvarname
        logger.info(msg=msg)
        ncvar = self.vicen_ana
        kwargs = {"ncfile": ncfile, "ncvarname": ncvarname, "ncvar": ncvar}
        ioapps.netcdf4_interface.ncwritevar(**kwargs)


# ----


class MOM6EnsInitConds(object):
    """
    Description
    -----------

    This is the base-class object for all Modular Ocean Model (MOM6)
    ensemble member initial condition updates and quality checks.

    Parameters
    ----------

    rescale_yaml: str

        A Python string specifying the path to the external
        YAML-formatted file containing the MOM6 initial condition
        variable values to be assigned for NaN value instances.

    """

    def __init__(self, rescale_yaml):
        """
        Description
        -----------

        Creates a new MOM6EnsInitConds object.

        """
        self.analy_obj = tools.parser_interface.object_define()
        self.analy_varlist = ["ave_ssh", "h", "u", "v", "Salt", "Temp"]
        kwargs = {"path": rescale_yaml}
        exist = tools.fileio_interface.fileexist(**kwargs)
        if not exist:
            msg = (
                "The location for the YAML-formatted file containing "
                "the MOM6 rescaling values for the MOM6 analysis variables "
                "(soca_rescale_ocean_yaml) could not be determined from "
                "the user experiment configuration. Aborting!!!"
            )
            raise SOCAInterfaceError(msg=msg)
        kwargs = {"yaml_file": rescale_yaml}
        self.yaml_dict = tools.fileio_interface.read_yaml(**kwargs)

    def read_analy(self, analy_filepath):
        """
        Description
        -----------

        This method reads a MOM6 ensemble member analysis file
        generated by the SOCA ensemble perturbation (enspert)
        application and defines the base-class attribute analy_obj.

        Parameters
        ----------

        analy_filepath: str

            A Python string specifying the path to respective MOM6
            ensemble member analysis file specified by the SOCA
            ensemble perturbation (enspert) application.

        """
        msg = "Reading MOM6 analysis from file %s." % analy_filepath
        logger.info(msg=msg)
        ncfile = analy_filepath
        for analy_var in self.analy_varlist:
            ncvarname = analy_var
            kwargs = {"ncfile": ncfile, "ncvarname": ncvarname}
            ncvar = ioapps.netcdf4_interface.ncreadvar(**kwargs)
            kwargs = {"object_in": self.analy_obj, "key": analy_var, "value": ncvar}
            self.analy_obj = tools.parser_interface.object_setattr(**kwargs)

    def updateics(self, analy_filepath, output_filepath):
        """
        Description
        -----------

        This method updates the MOM6 initial condition file with the
        respective SOCA analysis variables; this method also checks
        whether the user experiment configuration specifies to reset
        NaN valued elements of the respective analysis variable arrays
        prior to updating the MOM6 initial condition file.

        Parameters
        ----------

        analy_filepath: str

            A Python string specifying the path to respective MOM6
            ensemble member analysis file specified by the SOCA
            ensemble perturbation (enspert) application.

        output_filepath: str

            A Python string specifying the path to the netCDF
            formatted MOM6 model initial condition file for the
            respective ensemble member.

        """
        msg = (
            "Updating MOM6 initial condition file %s using MOM6 "
            "analysis in file %s." % (output_filepath, analy_filepath)
        )
        logger.info(msg=msg)
        ncfile = output_filepath
        for analy_var in self.analy_varlist:
            ncvarname = analy_var
            kwargs = {"object_in": self.analy_obj, "key": ncvarname}
            ncvar = tools.parser_interface.object_getattr(**kwargs)
            if analy_var in self.yaml_dict.keys():
                kwargs = {"dict_in": self.yaml_dict, "key": analy_var}
                rescale_value = tools.parser_interface.dict_key_value(**kwargs)
                msg = (
                    "Resetting all NaN valued variables for analysis "
                    "variable %s to %s." % (analy_var, rescale_value)
                )
                logger.warn(msg=msg)
                ncvar[numpy.isnan(ncvar)] = rescale_value
            if ncvar is None:
                msg = (
                    "The analysis variable %s cannot be NoneType. "
                    "Aborting!!!" % ncvarname
                )
                raise SOCAInterfaceError(msg=msg)
            kwargs = {"ncfile": ncfile, "ncvarname": ncvarname, "ncvar": ncvar}
            ioapps.netcdf4_interface.ncwritevar(**kwargs)

    def setup(self, analy_filepath, bkgrd_filepath, output_filepath):
        """
        Description
        -----------

        This method prepares the working directory for the respective
        MOM6 ensemble member initial condition file update.

        Parameters
        ----------

        analy_filepath: str

            A Python string specifying the path to respective MOM6
            ensemble member analysis file specified by the SOCA
            ensemble perturbation (enspert) application.

        output_filepath: str

            A Python string specifying the path to the netCDF
            formatted MOM6 model initial condition file; note that
            this file is not generated by SOCA and most often is the
            control member filepath that is used to generate the SOCA
            ensemble using the SOCA ensemble perturbation (ens_pert)
            application.

        output_filepath: str

            A Python string specifying the path to the netCDF
            formatted MOM6 model initial condition file for the
            respective ensemble member.

        """
        srcfile = bkgrd_filepath
        dstfile = output_filepath
        msg = "Copying file %s to %s." % (srcfile, dstfile)
        logger.info(msg=msg)
        kwargs = {"srcfile": srcfile, "dstfile": dstfile}
        tools.fileio_interface.copyfile(**kwargs)
        kwargs = {"analy_filepath": analy_filepath}
        self.read_analy(**kwargs)

    def run(self, analy_filepath, bkgrd_filepath, output_filepath):
        """
        Description
        -----------

        This method performs the following tasks:

        (1) Prepares the working directory for the respective MOM6
            ensemble member initial condition file update.

        (2) Updates the MOM6 initial condition file using the SOCA
            analysis for the respective ensemble member.

        Parameters
        ----------

        analy_filepath: str

            A Python string specifying the path to respective MOM6
            ensemble member analysis file specified by the SOCA
            ensemble perturbation (enspert) application.

        output_filepath: str

            A Python string specifying the path to the netCDF
            formatted MOM6 model initial condition file; note that
            this file is not generated by SOCA and most often is the
            control member filepath that is used to generate the SOCA
            ensemble using the SOCA ensemble perturbation (ens_pert)
            application.

        output_filepath: str

            A Python string specifying the path to the netCDF
            formatted MOM6 model initial condition file for the
            respective ensemble member.

        """
        kwargs = {
            "analy_filepath": analy_filepath,
            "bkgrd_filepath": bkgrd_filepath,
            "output_filepath": output_filepath,
        }
        self.setup(**kwargs)
        kwargs = {"analy_filepath": analy_filepath, "output_filepath": output_filepath}
        self.updateics(**kwargs)


# ----


class SOCAInterfaceError(Error):
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

        Creates a new SOCAInterfaceError object.

        """
        super(SOCAInterfaceError, self).__init__(msg=msg)
