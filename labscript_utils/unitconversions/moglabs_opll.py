#####################################################################
#                                                                   #
# detuning.py                                                       #
#                                                                   #
# Copyright 2013, Monash University                                 #
#                                                                   #
# This file is part of the labscript suite (see                     #
# http://labscriptsuite.org) and is licensed under the Simplified   #
# BSD License. See the license.txt file in the root of the project  #
# for the full license.                                             #
#                                                                   #
#####################################################################
from .UnitConversionBase import *

class moglabs_opll(UnitConversion):
    base_unit = 'V'
    derived_units = ['MHz']

    def __init__(self,calibration_parameters={'central_freq_MHz':98,'max_depth_MHz':250,'max_gain_factor':1073709056,'gain':1}):
        self.parameters = calibration_parameters

        UnitConversion.__init__(self,self.parameters)

    def MHz_to_base(self,freq):
        volts = (freq - self.parameters['central_freq_MHz'])/(self.parameters['max_depth_MHz']*self.parameters['gain']/self.parameters['max_gain_factor'])
        return volts
    def MHz_from_base(self,volts):
        freq = self.parameters['central_freq_MHz'] + self.parameters['max_depth_MHz']*(self.parameters['gain']/self.parameters['max_gain_factor'])*volts
        return freq

