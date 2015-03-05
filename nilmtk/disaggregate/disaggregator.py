from __future__ import print_function, division
import pandas as pd
from itertools import repeat, tee
from time import time
from copy import deepcopy
from collections import OrderedDict
import numpy as np
import yaml
from os.path import isdir, isfile, join, exists, dirname
from os import listdir, makedirs, remove
from shutil import rmtree
import re
from nilm_metadata.convert_yaml_to_hdf5 import _load_file
from nilmtk.timeframe import TimeFrame
from nilmtk.node import Node

# do not edit! added by PythonBreakpoints
from pdb import set_trace as _breakpoint

class Disaggregator(object):
    """
    Provides a common interface to all disaggregation classes.
    Subclasses only need to override train_on_chunk() and disaggregate_chunk().

    Attributes
    ----------
    Each subclass should internally store models learned from training.
    """
    def __init__(self):
        """
        Parameters
        ----------
        """
        
    ####################### current interface

    def train(self, metergroup):
        """
        Trains the model given a metergroup containing a appliance meters (supervised) or a site meter (unsupervised).

        Parameters
        ----------
        metergroup : a nilmtk.MeterGroup object
        """

        raise NotImplementedError("NotImplementedError")
        
    def disaggregate(self, mains, output_datastore):
        """Disaggregate mains using model learned by train(), and saves the disaggregated data to output_datastore.

        Parameters
        ----------
        mains : nilmtk.ElecMeter (single-phase) or nilmtk.MeterGroup (multi-phase)
        output_datastore : instance of nilmtk.DataStore subclass
        """
        
        raise NotImplementedError("NotImplementedError")
        
    ####################### interface proposed by Jack on 1 Feb
        
    def train_on_chunk(self, chunk):
        """Signature is fine for site meter dataframes (unsupervised learning). Would need to be called for each appliance meter along with appliance identifier for supervised learning.

        Parameters
        ----------
        chunk : pd.DataFrame (in NILMTK format)"""

        raise NotImplementedError("NotImplementedError")
    
    def disaggregate_chunk(self, chunk):
        """Loads all of a DataFrame from disk.

        Parameters
        ----------
        chunk : pd.DataFrame (in NILMTK format)
        
        Returns
        -------
        DataFrame"""

        raise NotImplementedError("NotImplementedError")

    ####################### helper methods (Disaggregator superclass)
    
    def write_disaggregated_chunk_to_datastore(self, chunk, datastore):
        """

        Parameters
        ----------
        chunk : pd.DataFrame representing a single appliance (chunk needs to include metadata)
        datastore : nilmtk.DataStore
        
        """

        raise NotImplementedError("NotImplementedError")
    
    def disaggregate(self, mains, output_datastore):
        """
        Passes each chunk from mains generator to disaggregate_chunk() and passes the output to write_disaggregated_chunk_to_datastore()

        Parameters
        ----------
        mains : nilmtk.ElecMeter (single-phase) or nilmtk.MeterGroup (multi-phase)
        output_datastore : str or nilmtk.DataStore to save output to
        
        """

        raise NotImplementedError("NotImplementedError")
        
    ####################### methods to be overriden to save/load learned model to disk
    
    def import_model(self, filename):
        """
        Loads learned model from file

        Parameters
        ----------
        filename : str path to file to load model from
        
        """

        raise NotImplementedError("NotImplementedError")
        
    def export_model(self, filename):
        """
        Saves learned model to file 

        Parameters
        ----------
        filename : str path to file to save model to
        
        """

        raise NotImplementedError("NotImplementedError")
