from globalthings import *

class Step:
    """
        A Step is a componnent of a Receipe. It can be a TRANSITION, LEVEL or STOP to pause the receipe until user confirmation
    """
    
    
    def __init__(self, a_name, a_type, a_duration, a_temperature=0.0, an_inertia=0.0):
        """
            Constructor
            :param a_name: Name of the Step
            :param a_type: Type of the Step within LEVEL,TRANSITION or STOP
            :param a_duration: Duration of the Step in minutes (unused for a STOP Step)
            :param a_temperature: If the Step is not TRANSITION, the target temperature shall be send as parameter
            :param an_inertia: The brew's inertia under those conditions in degrees Celcius. It is good to write 1 degree celcius less than target so that the step begins with a non heating step.
            :type a_name: String
            :type a_type: int LEVEL,TRANSITION or STOP
            :type a_duration: unsigned int
            :type a_temperature: float
            :type an_inertia: float
            
            :Exemple:
            >>> Step("Alpha proteines conversion Step", LEVEL, 35, 62, 1.2)
            good!
            
            .. warnings:: This function is unprotected against wrong parameters types or values. Use carfully
            .. todo:: Make the function more robust to lazy inputers
        """
        self.__name = a_name
        self.__step_type = a_type
        self.__duration = a_duration
        if(self.__duration==0):self.__duration+=1
        if(a_temperature==None):a_temperature=0
        self.__temperature = a_temperature
        self.__inertia = an_inertia


    def get_name(self):
        """
            Returns the name of the Step
            
            :return: Name of the Step
            :rtype: Sting
        """
        return self.__name
      
      
    def get_type(self):
        """
            Returns the type of the Step
            
            :return: Type of the Step
            :rtype: int LEVEL,TRANSITION or STOP
        """
        return self.__step_type


    def get_temperature(self):
        """
            Returns the target temperature of the Step
            
            :return: Target temperature of the Step in degrees Celcius
            :rtype: int
        """
        return self.__temperature
      
      
    def get_duration(self):
        """
            Returns the duration of the Step
            
            :return: Requested duration of the Step in minutes (value never used for a STOP Step)
            :rtype: unsigned int
        """
        return self.__duration

    def get_inertia(self):
        """
            Returns the inertia of the Step
            
            :return: Requested inertia of the Step in degrees celcius
            :rtype: float
        """
        return self.__inertia   

    def interpolation(self, start_temperature, start_time, stop_temperature, current_time):
        """
            This function defines the target temperature at every seconds during a TRANSITION Step. The computation is such as the interpolation is linear between the previous Step's temperature and the temperature of the following one.
            
            :param start_temperature: Previous Step's start temperature in degrees Celcius
            :param start_time: Time at the beggining of the TRANSITION Step
            :param stop_temperature: Next Step's start temperature in degrees Celcius
            :param current_time: Time now
            :type start_temperature: float
            :type start_time: Python's dateTime
            :type stop_temperature: float
            :type current_time: Python's dateTime
            
            :return: Current target temperature based on linear interpolation
            :rtype: float
            
            .. note:: This is coded within the class Steps so that one day we can code different continiuous transitions depending of a new parameter of this Step
        """
        delta_th=stop_temperature-start_temperature
        delta_time=current_time-start_time
        return start_temperature+delta_th*(delta_time.total_seconds()/(self.__duration*60))


    def print_self(self):
        """
            Returns the Step as a human readable String ended with a new line
            
            :return: A String detailling the values of the Step
            :rtype: String
        """
        to_print="Name : "+self.__name
        if(self.__step_type==TRANSITION):to_print+=" Type : TRANSITION"
        elif(self.__step_type==LEVEL):to_print+=" Type : LEVEL"
        elif(self.__step_type==STOP):to_print+=" Type : STOP"
        to_print+=" Target temperature : "+str(self.__temperature)
        to_print+=" current inertia : "+str(self.__inertia)
        to_print+=" Duration : "+str(self.__duration)+"\n"
        return to_print
