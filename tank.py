
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
        self.__current_transition_energy_need=0
        self.__current_transition_energy_done=0
        self.__last_temp=self.__thermometer.read_temperature()
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
            :type temperature_target: float 
        """
        if(self.__drive_type==BOOLEAN):
            if(self.__thermometer.read_temperature()>temperature_target+HYSTERESIS):
                for a_heater in self.__heaters:
                    a_heater.deactivate()
            elif(self.__thermometer.read_temperature()<temperature_target-HYSTERESIS):
                for a_heater in self.__heaters:
                    a_heater.activate()

    def sum_of_squares(self,n):
        """
            Computes the sum of the squares up to n
            :param n: the sum limit
            :return: the sum
            :rtype: int
        """
	return ((2*n)*(n+1)*n)/6

    def compute_nrj(self,ini_temperature,final_temperature,external_temperature):
        """
            Computes the required energy in order to perform a transition
            :param ini_temperature: The initial temperature
            :param final_temperature: The desired temperature
            :param external_temperature: The external temperature
            :type ini_temperature: float 
            :type final_temperature: float 
            :type external_temperature: float 
            :return: the energy needed in Joules
            :rtype: float
        """
        if(ini_temperature>final_temperature):
            return 0
	    # heat losses estimation
        heating_time=(final_temperature-ini_temperature)/(HEATER_EFFECT)
        print "Estimated TRANSITION time (seconds):"+str(heating_time*UPDATE_PERIOD)
        losses=HEAT_PROPORTIONNAL_LEAKS*((final_temperature+ini_temperature)/2-external_temperature)*heating_time #terrible aproximation. Integrals should be used. TODO just after passing all model constants en per-second.
        losses+=HEAT_SQUARE_LEAKS*((final_temperature+ini_temperature)*3/4-external_temperature)*((final_temperature+ini_temperature)*3/4-external_temperature)*heating_time#terrible aproximation. Integrals should be used. TODO just after passing all model constants en per-second.
        return losses+9.5*CALOR_WATER*(final_temperature-ini_temperature) #9.5 = 8Lwater + 1.5L malt TODO 9.5 variable

    
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
                    print "next target:"+str(next_target)+"cur_temp"+str(cur_temp)+"INERTIA_TIME"+str(INERTIA_TIME)+"HEATING_SPEED"+str(HEATING_SPEED)
                    return True
                if(cur_temp>temperature_target):
                    for a_heater in self.__heaters:
                        a_heater.deactivate()
                elif(cur_temp<temperature_target-HYSTERESIS):
                    for a_heater in self.__heaters:
                        a_heater.activate()


    def temperature_model_drive(self, temperature_target, next_target, external_temperature):
        """
            Drives the heaters in order to follow the temperature target
            :param temperature_target: The current desired temperature for the tank
            :param next_target: The desired temperature for the tank for the next level step
            :param external_temperature: The outside temperature
            :type temperature_target: float 
            :type next_target: float 
            :type external_temperature: float 
        """
        cur_temp=self.__thermometer.read_temperature()
        print "temp target:"+str(temperature_target)+" next_target:"+str(next_target)+"external_temperature:"+str(external_temperature)
        if(self.__drive_type==BOOLEAN):
            if(temperature_target==next_target):                            #currently doing a LEVEL or STOP...    
                print "doing LEVEL or STOP" 
                if(cur_temp>temperature_target):
                    for a_heater in self.__heaters:
                        a_heater.deactivate()
                elif(cur_temp<temperature_target-HYSTERESIS):
                    for a_heater in self.__heaters:
                        a_heater.activate()
            else:                                                           #currently doing a TRANSITION...
                if (self.__current_transition_energy_need==0):
                    self.__current_transition_energy_need=self.compute_nrj(cur_temp,next_target,external_temperature)
                    self.__current_transition_energy_done=0
                if(cur_temp>next_target):  		#safety first
                    for a_heater in self.__heaters:
                        a_heater.deactivate()						
                elif((self.__last_temp<=cur_temp) and (self.__current_transition_energy_done<=self.__current_transition_energy_need)):  #target not reached using model, heating until temp reached... USE A FLAG HERE BECAUSE AS SOON AS THE FAILOVER HEATING HAS EFFECT IT STOPS....
                    print "heating!!!!"
                    for a_heater in self.__heaters:
                        a_heater.activate()
                        self.__current_transition_energy_done+=HEATER_EFF*a_heater.get_power()*UPDATE_PERIOD
                else:
                    print "no heat condition"
                    for a_heater in self.__heaters:
                        a_heater.deactivate()
        print "heating done:"+str(self.__current_transition_energy_done)+" of :"+str(self.__current_transition_energy_need)
        self.__last_temp=cur_temp

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
