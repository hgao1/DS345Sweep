# -*- coding: utf-8 -*-

'''
From DS345.py, modified to chirp instead of running at a constant frequency.
This version includes:
    Modulation Waveform (MDWF)
    Modulation Type (MTYP)
    Modulation Rate (RATE)
    Sweep Stop Frequency (SPFR)
    Sweep Start Frequency (STFR)
    Modulation On and Off (MENA)
    Addition of a trigger (*TRG)
    Trigger Source (TRSC)

If the user is interested in running at a cosntant frequency,
this file as well as Qacam.py must be modified.
In this file:
155-168, 171-277 
'''

from PyQt5.QtCore import pyqtProperty
from common.QSerialDevice import QSerialDevice
import numpy as np
from parse import parse

import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class DS345(QSerialDevice):
    '''Abstraction of a Stanford Research DS345 Function Generator

    Attributes
    ----------
    amplitude : float
       Output amplitude [Vpp]
    frequency : float
       Output frequency [Hz]
    offset : float
       Offset voltage [V]
    phase : float
       Output phase relative to reference [degrees]
    waveform : 0 .. 5
       Index of output waveform selection
    invert : bool
       If True, invert output signal
    mute : bool
       If True, set amplitude to 0 V.
       Else, set amplitude to last value.
    identification : str
       Identification string returned by instrument
    modwaveform: 0 .. 6
        Index of output modulation waveform selection
    modtype: 0 .. 5
        Index of modulation types
    modrate: float
        Sets the modulation rate as input [Hz] per second..?
    startfrequency: float
        Starting frequency for frequency sweep [Hz]
    stopfrequency: float
        Stopping frequency for frequency sweep [Hz]
    triggersource: 0 .. 4
        Sets the trigger source
    modOnOff: 0,1
        Turns modulation on or off
    Methods
    -------
    identify() : bool
        Returns True if serial device is connected to a DS345
    '''

    def __init__(self):
        super(DS345, self).__init__(baudrate=QSerialDevice.Baud9600,
                                    databits=QSerialDevice.Data8,
                                    parity=QSerialDevice.NoParity,
                                    stopbits=QSerialDevice.TwoStop)
        self._mute = False
        self.amplitude = 0.

    def identify(self):
        '''Check identity of instrument

        Returns
        -------
        identify : bool
            True if attached instrument identifies itself as a DS345
        '''
        res = self.handshake('*IDN?')
        logger.debug(' Received: {}'.format(res))
        found = 'DS345' in res
        logger.info(' DS345: {}'.format(found))
        return found

    def busy(self):
        return False

    # Properties
    @pyqtProperty(bool)
    def mute(self):
        '''Output muted'''
        return self._mute

    @mute.setter
    def mute(self, set_mute):
        if set_mute:
            self.send('AMPL 0.00VP')
            self._mute = True
        elif self._mute:
            self._mute = False
            self.amplitude = self._amplitude

    # Function output adjustable properties
    @pyqtProperty(float)
    def amplitude(self):
        '''Output amplitude [Vpp]'''
        if self._mute:
            return self._amplitude
        else:
            return float(parse('{}VP', self.handshake('AMPL?'))[0])

    @amplitude.setter
    def amplitude(self, value):
        self._amplitude = float(value)
        if not self._mute:
            self.send('AMPL {:.2f}VP'.format(self._amplitude))

    @pyqtProperty(float)
    def frequency(self):
        '''Output frequency [Hz]'''
        return float(self.handshake('FREQ?'))

    @frequency.setter
    def frequency(self, value):
        self.send('FREQ {:.4f}'.format(float(value)))
    def freq(self):
        return float(self.handshake('FREQ?'))

    @property
    def data(self):
        res = self.handshake('FREQ?')
        va = res
        logger.debug('frequency: {} '.format(va))
        return float(va)

    @pyqtProperty(float)
    def offset(self):
        '''Output offset [V]'''
        return float(self.handshake('OFFS?'))

    @offset.setter
    def offset(self, value):
        self.send('OFFS {:.2f}'.format(float(value)))
    '''
    @pyqtProperty(float)
    def phase(self):
        Output phase [degrees]
        return float(self.handshake('PHSE?'))

    @phase.setter
    def phase(self, value):
        self.send('PHSE {:.2f}'.format(float(value)))

    DS345 manual states that this will produce an error
    if a frequency sweep is enabled: Un-comment the above
    for a single frequency.
    '''

    # The following can be commented out for a single frequency:
    @pyqtProperty(float)
    def startfrequency(self):
        '''Starting output frequency for sweep [Hz] '''
        return float(self.handshake('STFR?'))

    @startfrequency.setter
    def startfrequency(self, value):
        self.send('STFR {:.4f}'.format(float(value)))

    @pyqtProperty(float)
    def stopfrequency(self):
        '''Stopping output frequency for sweep [Hz] '''
        return float(self.handshake('SPFR?'))

    @stopfrequency.setter
    def stopfrequency(self,value):
        self.send('SPFR {:.4f}'.format(float(value)))


    @pyqtProperty(float)
    def modrate(self):
        '''Sweep rate of frequency per second [Hz] '''
        return float(self.handshake('RATE?'))

    @modrate.setter
    def modrate(self,value):
        self.send('RATE {:.4f}'.format(float(value)))

    @pyqtProperty(int)
    def waveform(self):
        '''Output waveform
           0: sine
           1: square
           2: triangle
           3: ramp
           4: noise
           5: arbitrary
        '''
        return int(self.handshake('FUNC?'))

    @waveform.setter
    def waveform(self, value):
        self.send('FUNC {}'.format(np.clip(int(value), 0, 5)))
    @pyqtProperty(int)
    def triggersource(self):
        '''Set the trigger source
           0: single
           1: internal
           2: + Ext
           3: - Ext
           4: line
         '''
        return int(self.handshake('TSRC?'))

    @triggersource.setter
    def triggersource(self, value):
        self.send('TSRC {}'.format(np.clip(int(value),0,4)))
    def trigger(self):
        self.send('*TRG')

    @pyqtProperty(int)
    def modwaveform(self):
        '''Output waveform
            0: single sweep
            1: ramp
            2: triangle
            3: sine
            4: square
            5: arbitrary
            6: none
         '''
        return int(self.handshake('MDWF?'))

    @modwaveform.setter
    def modwaveform(self,value):
        self.send('MDWF {}'.format(np.clip(int(value),0,6)))

    @pyqtProperty(int)
    def modOnOff(self):
        '''Turns modulation:
           0: off
           1: on
        '''
        return int(self.handshake('MENA?'))

    @modOnOff.setter
    def modOnOff(self,value):
        self.send('MENA {}'.format(np.clip(int(value),0,1)))


    @pyqtProperty(int)
    def modtype(self):
        '''Modulation Type
            0: linear sweep
            1: log sweep
            2: AM
            3: FM
            4: PM
            5: Burst
         '''
        return int(self.handshake('MTYP?'))

    @modwaveform.setter
    def modtype(self,value):
        self.send('MTYP {}'.format(np.clip(int(value),0,5)))

# Stop here, keep code below for both.

    @pyqtProperty(int)
    def invert(self):
        return int(self.handshake('INVT?'))

    @invert.setter
    def invert(self, value):
        self.send('INVT {}'.format(np.clip(int(value), 0, 1)))

    def setECL(self):
        '''Set ECL levels: 1Vpp, -1.3V offset'''
        self.send('AECL')

    def setTTL(self):
        '''Set TTL levels: 5Vpp, 2.5V offset'''
        self.send('ATTL')

    def setPhaseZero(self):
        '''Set waveform phase to zero'''
        self.send('PCLR')
