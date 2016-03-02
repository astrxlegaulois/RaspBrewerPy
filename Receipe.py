"""
    Possible type values for a transition. Global variables
"""
LEVEL = 2
TRANSITION = 1
STOP = 0

import datetime

class Step:
    """
        A Step is a componnent of a Receipe. It can be a TRANSITION, LEVEL or STOP to pause the receipe until user confirmation
    """
    
    
    def __init__(self, a_name, a_type, a_duration, a_temperature=0):
        """
            Constructor
            :param a_name: Name of the Step
            :param a_type: Type of the Step within LEVEL,TRANSITION or STOP
            :param a_duration: Duration of the Step in minutes (unused for a STOP Step)
            :param a_temperature: If the Step is not TRANSITION, the target temperature shall be send as parameter
            :type a_name: String
            :type a_type: int LEVEL,TRANSITION or STOP
            :type a_duration: unsigned int
            :type a_temperature: int
            
            :Exemple:
            >>> Step("Alpha proteines conversion Step", LEVEL, 35, 62)
            good!
            
            .. warnings:: This function is unprotected against wrong parameters types or values. Use carfully
            .. todo:: Make the function more robust to lazy inputers
        """
        self.__name = a_name
        self.__step_type = a_type
        self.__temperature = a_temperature
        self.__duration = a_duration
        if(self.__duration==0):self.__duration+=1


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
      

    def interpolation(self, start_temperature, start_time, stop_temperature, current_time):
        """
            This function defines the target temperature at every seconds during a TRANSITION Step. The computation is such as the interpolation is linear between the previous Step's temperature and the temperature of the following one.
            
            :param start_temperature: Previous Step's start temperature in degrees Celcius
            :param start_time: Time at the beggining of the TRANSITION Step
            :param stop_temperature: Next Step's start temperature in degrees Celcius
            :param current_time: Time now
            :type start_temperature: int
            :type start_time: Python's dateTime
            :type stop_temperature: int
            :type current_time: Python's dateTime
            
            :return: Current target temperature based on linear interpolation
            :rtype: int
            
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
        if(self.__step_type==LEVEL):to_print+=" Type : LEVEL"
        if(self.__step_type==STOP):to_print+=" Type : STOP"
        to_print+=" Target temperature : "+str(self.__temperature)
        to_print+=" Duration : "+str(self.__duration)+"\n"
        return to_print


class Receipe:
    """
        A receipe is a list of temperature TRANSISIONs, LEVEL Steps and STOPs (waiting for human confirmation). The Receipe must begin with a TRANSITION and there shall always be a TRANSITION between two any other type of Step. No TRANSITION shall be next to a TRANSITION.
    """
    
    def __init__(self, a_name):
        """
            Constructor for an empty Receipe
            
            :param a_name: Name of the Receipe
            :type a_name: String
        """
        self.__name = a_name
        self.__receipe_list=[]
        self.__cursor=None
        self.__timer=None


    def add_step(self, a_step):
        """
            This function appends an already fully featured Step to the Receipe's list
            
            :param a_step: The Step to add at the end of the Receipe
            :type a_step: Step

            .. warnings:: This function is unprotected against wrong parameters types or values. Use carfully.
            .. todo:: Make the function more robust to lazy inputers : exception if(len(__receipe_list)==0 && a_step.get_type()!=TRANSITION)
            .. todo:: Make the function more robust to lazy inputers : exception if no transistion between 2 steps of different temperature
            .. todo:: Make the function more robust to lazy inputers : exception if two transitions are consecutive
        """
        self.__receipe_list.append(a_step)


    def get_name(self):
        """
            Returns the name of the Receipe
            
            :return: Name of the Receipe
            :rtype: Sting
        """
        return self.__name
      
      
    def start(self,initial_temperature):
        """
            Starts running the Receipe.
            
            :param initial_temperature: The initial measured temperature of the tank. Needed for interpolation with the first STEP.
            :type initial_temperature: int
            
            .. note:: For safety reasons, a STOP step with a temperature of 0 is always added at the end of every receipe in order to make sure that we stop the heaters.
        """
        self.__receipe_list.insert(0,Step("Initial temperature",LEVEL,1, initial_temperature))
        self.__receipe_list.append(Step("Receipe ended",STOP,1,0))
        self.__cursor=1 # Begining with a TRANSITION that needs an initial temperature and a target temperature for interpolation
        self.update_step()


    def get_current_temperature_instruction(self):
        """
            Returns the current temperature instruction, according to the receipe.
            
            :return: The current temperature instruction, in degrees Celcius
            :rtype: int
        """
        if(self.__receipe_list[self.__cursor].get_type()==TRANSITION):
			return (self.__receipe_list[self.__cursor].interpolation(self.__receipe_list[self.__cursor-1].get_temperature(), self.__timer,self.__receipe_list[self.__cursor+1].get_temperature(), datetime.datetime.now()))
        else:
			return self.__receipe_list[self.__cursor].get_temperature()


    def get_current_step(self):
        """
            Returns the currently performed Step.
            
            :return: The current Step
            :rtype: Step
        """
        return self.__receipe_list[self.__cursor]


    def update_step(self):
        """
            This function is making sure that we change the current Steps accordingly to the Receipe. Function to be called regularily (every second for instance) in order to update the current step
        """
        if(self.get_current_step().get_type()!=STOP):
            if(self.__timer==None):
                self.__timer=datetime.datetime.now() #We start the timer by storing the begining date & time
            if(((datetime.datetime.now()-self.__timer).total_seconds()//60)>=self.get_current_step().get_duration):
                self.__timer=datetime.datetime.now() #We restart the timer by storing the begining date & time for the new step
                self.__cursor+=1


    def user_force_next_step(self):
        """
            This function allows the user to skip to the next Step. It is the only way to pass through a STOP Step.
        """
        if(self.__cursor<len(self.__receipe_list)):
            self.__cursor+=1
            self.__timer==datetime.datetime.now() #We restart the timer by storing the begining date & time for the new step
    
    
    def print_self(self):
        """
            Returns the Receipe as a human readable String ended with a new line
            
            :return: A String detailling the content of the Receipe
            :rtype: String
        """
        to_print="Name : "+self.__name
        if(self.__cursor!=None):to_print+="Current step : "+str(self.__cursor)
        if(self.__timer!=None):to_print+="Current step beginning time: "+str(self.__timer)
        i=0
        for astep in self.__receipe_list:
            to_print+="Step "+str(i)+" : "+astep.print_self()
            i+=1
        return to_print


       
