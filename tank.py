
from globalthings import *

class Tank:
    """
        A Tank has a diameter, one or several heaters, a thermometer and some ingredients. This gives it a forecastable thermodynamical behaviour.
    """

    def __init__(self, a_name, a_diameter, a_thermometer, a_drive_type):
        """
            Constructor
            
            :param a_name: The name of the Tank
            :param a_thermometer: A ready to use Thermometer giving the brew's temperature
            :param a_diameter: The diameter of the tank in cm
            :param a_drive_type: The temperature driving strategy : BOOLEAN, PID or PREDICTIVE
            :type a_name: String
            :type a_thermometer: Thermometer
            :type a_diameter: int
        """
        self.__name = a_name
        self.__diameter= a_diameter
        self.__thermometer= a_thermometer
        self.__drive_type=a_drive_type
        self.__heaters = []
        self.__ingredients = []
    
    
    def add_heater(self, a_heater):
        """
            Add a heater to the Tank
            :param a_heater: Ready to use Heater object, representing a heater plunged in the brew
            :type a_heater: Heater
        """
        self.__heaters.append(a_heater)
        
        
    def add_ingredient(self, an_ingredient):
        """
            Add an Ingredient to the Tank
            :param an_ingredient: Ready to use Ingredient object (water or malted grain)
            :type an_ingredient: Ingredient
        """
        self.__ingredients.append(an_ingredient)
    
    
    def print_self(self):
        """
            Returns the tank as a human readable String
            
            :return: A String detailling the Tank
            :rtype: String
        """
        to_print="Name : "+self.__name
        to_print+="Diameter : "+str(self.__diameter)
        to_print+="Thermometer :"+self.__thermometer.print_self()
        i=0
        for an_heater in self.__heaters:
            i+=1
            to_print+="Heater"+str(i)+" :"+an_heater.print_self()
        i=0
        for an_ingredient in self.__ingredients:
            i+=1
            to_print+="Ingredient"+str(i)+" :"+an_ingredient.print_self()
        return to_print

    def get_current_temperature(self):
        """
            Returns the current temperature of the Tank
            
            :return: the current temperature in degrees Celcius
            :rtype: float
        """
        return self.__thermometer.read_temperature()


    def temperature_hysteresis_drive(self, temperature_target):
        """
            Drives the heaters in order to follow the temperature target
            :param temperature_target: The current desired temperature for the tank
            :type temperature_targe: float 
        """
        if(self.__drive_type==BOOLEAN):
            if(self.__thermometer.read_temperature()>temperature_target+HYSTERESIS):
                for a_heater in self.__heaters:
                    a_heater.deactivate()
            elif(self.__thermometer.read_temperature()<temperature_target-HYSTERESIS):
                for a_heater in self.__heaters:
                    a_heater.activate()
        #TODO implement PID and PREDICTIVE (based on the content of the tank)

    
    def temperature_inertia_drive(self, temperature_target, next_target):
        """
            Drives the heaters in order to follow the temperature target
            :param temperature_target: The current desired temperature for the tank
            :param next_target: The desired temperature for the tank for the next level step
            :type temperature_targe: float 
            :type next_target: float 
        """
        cur_temp=self.__thermometer.read_temperature()
        if(self.__drive_type==BOOLEAN):
            if(temperature_target==next_target):                            #currently doing a LEVEL or STOP...           
                if(cur_temp>temperature_target):
                    for a_heater in self.__heaters:
                        a_heater.deactivate()
                elif(cur_temp<temperature_target-HYSTERESIS):
                    for a_heater in self.__heaters:
                        a_heater.activate()
            else:                                                           #currently doing a TRANSITION...
                if(cur_temp+INERTIA_TIME*HEATING_SPEED>next_target):
                    for a_heater in self.__heaters:
                        a_heater.deactivate()
                    print "Inertia overheat protection triggered"
                    return True
                if(cur_temp>temperature_target):
                    for a_heater in self.__heaters:
                        a_heater.deactivate()
                elif(cur_temp<temperature_target-HYSTERESIS):
                    for a_heater in self.__heaters:
                        a_heater.activate()


    def get_heating_status(self):
        """
            Returns whether or not the heaters are activated
            :return: the current activation state of each heater as an int made of booleans (bit 0 is activation state of the first heater,...)
            :rtype: int
        """
        retval=0
	cur_bit=0
	for a_heater in self.__heaters:
            retval+=(a_heater.get_state()<<cur_bit)
            cur_bit+=1
        return retval

