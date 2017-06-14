#!/usr/bin/env python
# -*- coding: utf-8 -*-
############
# Standard #
############
import time
from collections import OrderedDict

###############
# Third Party #
###############
import numpy as np

##########
# Module #
##########
from pcdsdevices.sim.pim import (PIMPulnixDetector, PIMMotor, PIM)

# PIMPulnixDetector Tests

def test_PIMPulnixDetector_instantiates():
    assert(PIMPulnixDetector("TEST"))

def test_PIMPulnixDetector_runs_ophyd_functions():
    pim_pdet = PIMPulnixDetector("TEST")
    assert(isinstance(pim_pdet.read(), OrderedDict))
    assert(isinstance(pim_pdet.describe(), OrderedDict))
    assert(isinstance(pim_pdet.describe_configuration(), OrderedDict))
    assert(isinstance(pim_pdet.read_configuration(), OrderedDict))

def test_PIMPulnixDetector_stats_plugin_reads():
    pim_pdet = PIMPulnixDetector("TEST")
    assert(isinstance(pim_pdet.stats2.read(), OrderedDict))

def test_PIMPulnixDetector_centroid_noise():
    pim_pdet = PIMPulnixDetector("TEST", noise_x=5, noise_y=20)
    pim_pdet.stats2.centroid.x.put(300)
    pim_pdet.stats2.centroid.y.put(400)
    test_x = 300 + int(np.round(300 + np.random.uniform(-1,1)*5))
    test_y = 400 + int(np.round(400 + np.random.uniform(-1,1)*20))
    assert(pim_pdet.centroid_x == test_x or 
           np.isclose(pim_pdet.centroid_x, 300, atol=5))
    assert(pim_pdet.centroid_x == test_y or 
           np.isclose(pim_pdet.centroid_y, 400, atol=20))
    
def test_PIMPulnixDetector_centroid_override():
    pim_pdet = PIMPulnixDetector("TEST")
    def centroid_override_x():
        pim_pdet.stats2.centroid.x.put(pim_pdet.stats2.centroid.x.value + 10)
    pim_pdet._cent_x = centroid_override_x    
    assert(pim_pdet.centroid_x == 10)
    assert(pim_pdet.centroid_x == 20)
    assert(pim_pdet.centroid_x == 30)
    def centroid_override_y():
        pim_pdet.stats2.centroid.y.put(pim_pdet.stats2.centroid.y.value + 20)
    pim_pdet._cent_y = centroid_override_y
    assert(pim_pdet.centroid_y == 20)
    assert(pim_pdet.centroid_y == 40)
    assert(pim_pdet.centroid_y == 60)

def test_PIMPulnixDetector_zeros_centroid_outside_yag():
    pim_pdet = PIMPulnixDetector("TEST", zero_outside_yag=True)
    pim_pdet.stats2.centroid.x.put(300)
    pim_pdet.stats2.centroid.y.put(400)
    assert(pim_pdet.centroid_x == 300)
    assert(pim_pdet.centroid_y == 400)
    # Left side
    pim_pdet.stats2.centroid.x.put(-100)
    assert(pim_pdet.centroid_x == 0)
    assert(pim_pdet.centroid_y == 0)
    # Reset
    pim_pdet.stats2.centroid.x.put(300)
    assert(pim_pdet.centroid_x == 300)
    assert(pim_pdet.centroid_y == 400)
    # Right side
    pim_pdet.stats2.centroid.x.put(pim_pdet.cam.size.size_x.value + 100)
    assert(pim_pdet.centroid_x == 0)
    assert(pim_pdet.centroid_y == 0)
    # Reset
    pim_pdet.stats2.centroid.x.put(300)
    assert(pim_pdet.centroid_x == 300)
    assert(pim_pdet.centroid_y == 400)
    # Below
    pim_pdet.stats2.centroid.y.put(-100)
    assert(pim_pdet.centroid_x == 0)
    assert(pim_pdet.centroid_y == 0)
    # Reset
    pim_pdet.stats2.centroid.y.put(400)
    assert(pim_pdet.centroid_x == 300)
    assert(pim_pdet.centroid_y == 400)
    # Right side
    pim_pdet.stats2.centroid.y.put(pim_pdet.cam.size.size_y.value + 200)
    assert(pim_pdet.centroid_x == 0)
    assert(pim_pdet.centroid_y == 0)
    # Reset
    pim_pdet.stats2.centroid.y.put(400)
    assert(pim_pdet.centroid_x == 300)
    assert(pim_pdet.centroid_y == 400)
    
# PIMMotor Tests

def test_PIMMotor_instantiates():
    assert(PIMMotor("TEST"))

def test_PIMMotor_runs_ophyd_functions():
    pmotor = PIMMotor("TEST")
    assert(isinstance(pmotor.read(), OrderedDict))
    assert(isinstance(pmotor.describe(), OrderedDict))
    assert(isinstance(pmotor.describe_configuration(), OrderedDict))
    assert(isinstance(pmotor.read_configuration(), OrderedDict))

def test_PIMMotor_transitions_states_correctly():
    pmotor = PIMMotor("TEST")
    status = pmotor.move("OUT")
    assert(pmotor.position == "OUT")
    assert(status.success)
    status = pmotor.move("IN")
    assert(pmotor.position == "IN")
    assert(status.success)
    status = pmotor.move("DIODE")
    assert(pmotor.position == "DIODE")
    assert(status.success)

def test_PIMMotor_noise_on_read():
    pmotor = PIMMotor("TEST", pos_in=5, noise=0.1)
    status = pmotor.move("IN")
    assert(status.success)
    assert(pmotor.pos !=  5 and np.isclose(pmotor.pos, 5, atol=0.1))

def test_PIMMotor_noise_changes_every_read():
    pmotor = PIMMotor("TEST", pos_in=5, noise=0.1)
    status = pmotor.move("IN")
    assert(status.success)
    pos = [pmotor.pos for i in range(10)]
    assert(len(pos) == len(set(pos)))

# PIM Tests

def test_PIM_instantiates():
    assert(PIM("TEST"))

def test_PIM_runs_ophyd_functions():
    pim = PIM("TEST")
    assert(isinstance(pim.read(), OrderedDict))
    assert(isinstance(pim.describe(), OrderedDict))
    assert(isinstance(pim.describe_configuration(), OrderedDict))
    assert(isinstance(pim.read_configuration(), OrderedDict))
    
def test_PIM_has_centroid():
    pim = PIM("TEST")
    assert(isinstance(pim.detector.stats2.centroid.x.read(), dict))
    assert(isinstance(pim.detector.stats2.centroid.y.read(), dict))
    
def test_PIM_fake_sleep_move_time():
    pim = PIM("TEST")
    pim.move("OUT")
    pim.fake_sleep = 1
    t0 = time.time()
    status = pim.move("IN")
    t1 = time.time() - t0
    assert(np.isclose(t1, pim.fake_sleep + 0.1, rtol=0.1))
    assert(pim.position == "IN")
    assert(status.success)

def test_PIM_noise():
    pim = PIM("TEST", x=5, y=5, z=5, noise_x=0.1, noise_y=0.1, noise_z=0.1)
    status = pim.move("IN")
    assert(status.success)
    assert(pim._x != 5 and np.isclose(pim._x, 5, atol=0.1))
    assert(pim._y != 5 and np.isclose(pim._y, 5, atol=0.1))
    assert(pim._z != 5 and np.isclose(pim._z, 5, atol=0.1))

def test_PIM_noise_changes_on_every_read():
    pim = PIM("TEST", x=5, y=5, z=5, noise_x=0.1, noise_y=0.1, noise_z=0.1)
    x_vals = [pim._x for i in range(10)]
    assert(len(x_vals) == len(set(x_vals)))
    y_vals = [pim._y for i in range(10)]
    assert(len(y_vals) == len(set(y_vals)))
    z_vals = [pim._z for i in range(10)]
    assert(len(z_vals) == len(set(z_vals)))
