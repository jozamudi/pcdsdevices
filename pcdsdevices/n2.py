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
               io='io',
               kind='normal',
               doc='Mass of the N2 in lbs')

    pressure = Cpt(PytmcSignal,
                   ':PRESSURE',
                   io='io',
                   kind='normal',
                   doc='Pressure of the N2 in psi')

    start_exchange = Cpt(PytmcSignal,
                         ':START_EXCHANGE',
                         io='io',
                         kind='normal',
                         doc='Start N2 exchange')

    finish_exchange = Cpt(PytmcSignal,
                          ':FINISH_EXCHANGE',
                          io='io',
                          kind='normal',
                          doc='Finish N2 exchange')

    max_mass = Cpt(PytmcSignal,
                   ':MAX_MASS',
                   io='io',
                   kind='normal',
                   doc='Maximum allowable mass of N2 in lbs')

    min_mass = Cpt(PytmcSignal,
                   ':MIN_MASS',
                   io='io',
                   kind='normal',
                   doc='Minimum allowable mass of N2 in lbs')

    min_mass_threshold = Cpt(PytmcSignal,
                             ':MIN_MASS_THRESHOLD',
                             io='io',
                             kind='normal',
                             doc='Minimum mass threshold in lbs')

    min_pressure_threshold = Cpt(PytmcSignal,
                                 ':MIN_PRESS_THRESHOLD',
                                 io='io',
                                 kind='normal',
                                 doc='Minimum pressure threshold in psi')

    warning_mass_threshold = Cpt(PytmcSignal,
                                 ':MIN_MASS_WARNING_THRESHOLD',
                                 io='io',
                                 kind='normal',
                                 doc='Warning if mass is less than threshold in lbs')

    led_status = Cpt(PytmcSignal,
                     ':LED',
                     io='io',
                     kind='normal',
                     doc='LED status indicator')
