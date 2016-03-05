"""
    pip install RPi.GPIO needed in order to drive the heater
"""
import RPi.GPIO as GPIO

class Heater:
    """
        A Heater allows to increase the temperature of the tank
    """

    def __init__(self, a_name, a_power, a_pin):
        """
            Constructor
            :param a_name: Name of the Heater
            :param a_power: Power in Watt of the electrical heater
            :param a_pin: The number of the GPIO pin (BOARD mode) used to drive the heater
            :type a_name: String
            :type a_power: Int
            :type a_pin: Int
        """
        self.__name = a_name
        self.__power = a_power
        self.__GPIO_pin = a_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(a_pin, GPIO.OUT, initial=GPIO.LOW)
     
      
    def activate(self):
        """
            Activates the Heater
        """
        GPIO.output(a_pin, GPIO.HIGH)


    def deactivate(self):
        """
            Deactivate the Heater
        """
        GPIO.output(a_pin, GPIO.LOW)
 
 
    def get_state(self):
        """
            Returns 1 if the heater is running and 0 if not
            
            :return: Current state of the heater
            :rtype: Boolean
        """
        return GPIO.input(a_pin)   
    

    def get_name(self):
        """
            Returns the name of the Brewer
            
            :return: Name of the Brewer
            :rtype: Sting
        """
        return self.__name
