# coding: utf-8
"""
    Dirty module to declare global variables and functions. Thx a lot Python ^^
"""

"""
    Possible type values for a step. Global variables
"""
LEVEL = 2
TRANSITION = 1
STOP = 0

"""
    Possible type values for an Ingredient. Global variables
"""
GRAIN =1
WATER = 0

"""
    Possible temperature driving types for a Tank. Global variables
"""
BOOLEAN = 0
PID = 1
PREDICTIVE = 2

"""
    Global update period for everything (in seconds) : temperature readouts and heaters status
"""
UPDATE_PERIOD = 5

"""
    Inertia driving constant variables. Seconds, degrees/seconds, degrees Celcius
"""
INERTIA_TIME = 50
HEATING_SPEED = 0.09
HYSTERESIS = 1.0

"""
    Model driving constant variables. Seconds, degrees/seconds, degrees Celcius
"""
#model constants
CALOR_WATER = 4186
CALOR_GRAIN = 26
HEATER_EFF = 0.85 #efficiency
HEAT_PROPORTIONNAL_LEAKS = 0.0008 #system temperature leaks
HEAT_SQUARE_LEAKS = 0.000014 #system temperature leaks (for a closed tank) 0.00003 if open
HEATER_EFFECT = 0.16 #Average increase of degrees of the mesh caused by one step of heater activation
