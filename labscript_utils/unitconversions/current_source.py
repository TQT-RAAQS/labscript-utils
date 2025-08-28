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

class current_source(UnitConversion):
    base_unit = 'V'
    derived_units = ['A']

    def __init__(self,calibration_parameters={'A_per_V':0.4}):
        self.parameters = calibration_parameters

        UnitConversion.__init__(self,self.parameters)

    def A_to_base(self,amps):
        volts = amps/self.parameters['A_per_V']
        return volts
    def A_from_base(self,volts):
        amps = volts * self.parameters['A_per_V']
        return amps

