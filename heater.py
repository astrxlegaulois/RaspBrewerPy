"""
    pip install RPi.GPIO and running this code from raspberry pi needed in order to drive the heater
    Needs to be run as root...
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
            :param a_pin: The number of the GPIO pin (BCM mode) used to drive the heater
            :type a_name: String
            :type a_power: Int
            :type a_pin: Int
        """
        self.__name = a_name
        self.__power = a_power
        self.__GPIO_pin = a_pin
        GPIO.setmode(GPIO.BCM)
	#GPIO.setup(a_pin, GPIO.OUT, initial=GPIO.LOW)
	#As the R Pi does only 3.3V, we use the 5V  input pull-up in order to generate the 5V needed to trigger the relay => counter-intuitive init and use...
        GPIO.setup(self.__GPIO_pin, GPIO.IN) #For safety we initialize the heater at non heating...
     
      
    def activate(self):
        """
            Activates the Heater
        """
        #GPIO.output(self.__GPIO_pin, GPIO.HIGH)
	#As the R Pi does only 3.3V, we use the 5V  input pull-up in order to generate the 5V needed to trigger the relay => counter-intuitive init and use...
        GPIO.setup(self.__GPIO_pin, GPIO.OUT)
	


    def deactivate(self):
        """
            Deactivate the Heater
        """
        #GPIO.output(self.__GPIO_pin, GPIO.LOW)
	#As the R Pi does only 3.3V, we use the 5V  input pull-up in order to generate the 5V needed to trigger the relay => counter-intuitive init and use...
        GPIO.setup(self.__GPIO_pin, GPIO.IN)
 
 
    def get_state(self):
        """
            Returns 1 if the heater is running and 0 if not
            
            :return: Current state of the heater
            :rtype: Boolean
        """
        #return GPIO.input(self.__GPIO_pin)
	#As the R Pi does only 3.3V, we use the 5V  input pull-up in order to generate the 5V needed to trigger the relay => counter-intuitive init and use...
	return not GPIO.gpio_function(self.__GPIO_pin)   
    

    def get_name(self):
        """
            Returns the name of the Brewer
            
            :return: Name of the Brewer
            :rtype: Sting
        """
        return self.__name


    def print_self(self):
        """
            Returns the Heater as a human readable String
            
            :return: A String detailling the caracteristics of the heater
            :rtype: String
        """
        to_print="Name : "+self.__name
        to_print+=" Power: "+str(self.__power)
        to_print+=" GPIO pin : "+str(self.__GPIO_pin)
        to_print+=" State : "+str(self.get_state())+"\n"
        return to_print
