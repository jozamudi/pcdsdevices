from ophyd.device import Component as Cpt
from ophyd.device import Device

from .interface import BaseInterface
from .signal import PytmcSignal


class N2(BaseInterface, Device):
    """
    Device class for controlling Nitrogen (N2) systems.

    """
    mass = Cpt(PytmcSignal,
               ':MASS',
               kind='normal',
               doc='Mass of the N2 in kg')

    pressure = Cpt(PytmcSignal,
                   ':PRESSURE',
                   kind='normal',
                   doc='Pressure of the N2 in Pa')

    start_exchange = Cpt(PytmcSignal,
                         ':START_EXCHANGE',
                         kind='normal',
                         doc='Start N2 exchange')

    finish_exchange = Cpt(PytmcSignal,
                          ':FINISH_EXCHANGE',
                          kind='normal',
                          doc='Finish N2 exchange')
