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
    Servo driving constant variables. Hysteresis in degrees Celcius
"""
HYSTERESIS_UP = 5.0
HYSTERESIS = 1.0

