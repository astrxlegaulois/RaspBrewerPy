"""
    Possible type values for a transition. Global variables
"""
LEVEL = 2
TRANSITION = 1
STOP = 0

import datetime

class Step:
    """
        A step is a componnent of a receipe. It can be a transition, level step or stop until user confirmation
    """
    
    
    def __init__(self, a_name, a_type, a_duration, a_temperature=0):
        """
            Constructor
            :param a_name: Name of the step
            :param a_type: Type of the step within LEVEL,TRANSITION or STOP
            :param a_duration: Duration of the step in minutes (unused for a STOP Step)
            :param a_temperature: If the step is not TRANSITION, the target temperature shall be send as parameter
            :type a_name: String
            :type a_type: int LEVEL,TRANSITION or STOP
            :type a_duration: unsigned int
            :type a_temperature: int
            
            :Exemple:
            >>> new Step("Alpha proteines conversion step", LEVEL, 35, 62)
            good!
            
            .. warnings:: This function is unprotected agains wrong parameters types or values. Use carfully
            .. todo:: Make the function more robust to lazy inputers
        """
        self.__name = a_name
        self.__step_type = a_type
        self.__temperature = a_temperature
        self.__duration = a_duration
        if(self.__duration==0)self.__duration++


    def get_name(self):
        """
            Returns the name of the step
            
            :return: Name of the step
            :rtype: Sting
        """
        return self.__name
      
      
    def get_type(self):
        """
            Returns the type of the step
            
            :return: Type of the step
            :rtype: int LEVEL,TRANSITION or STOP
        """
        return self.__step_type


    def get_temperature(self):
        """
            Returns the target temperature of the step
            
            :return: Target temperature of the step in degrees Celcius
            :rtype: int
        """
        return self.__temperature
      
      
    def get_duration(self):
        """
            Returns the duration of the step
            
            :return: Requested duration of the step in minutes (ignored for a STOP Step)
            :rtype: unsigned int
        """
        return self.__duration
      

    def interpolation(self, start_temperature, start_time, stop_temperature, current_time):
        """
            This function defines the target temperature at every seconds during a TRANSITION step. The computation is such as the interpolation is linear between the previous step temperature and the following.
            
            :param start_temperature: Previous step's start temperature in degrees Celcius
            :param start_time: Time at the beggining of the transition step
            :param stop_temperature: Next step's start temperature in degrees Celcius
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
        return start_temperature+delta_th*(delta_time.seconds()/(self.__duration*60))

        def print_self(self):
            """
                Returns the Step as a human readable String ended with a new line
                
                :return: A String detailling the values of the Step
                :rtype: String
            """
            to_print="Name : "+self.__name
            to_print+="Type : "+self.__step_type
            to_print+="Target temperature : "+self.__temperature
            to_print+="Duration : "+self.__duration+"\n"
            return to_print


class Receipe:
    """
        A receipe is a list of temperature transitions, level steps and stops (waiting for human confirmation'
    """
    
    
    def __init__(self, a_name):
        self.__name = a_name
        self.__receipe_list=[]
        self.__cursor=None
        self.__timer=None

    def add_step(self, a_step):
        #TODO exception if(len(__receipe_list)==0 && a_step.get_type()==LEVEL)
        #TODO exception if no transistion between 2 steps of different temperature
        #TODO exception if two transitions are consecutive
        self.__receipe_list.append(a_step)

    def get_name(self):
        return self.__name
      
    def start(self,initial_temperature):
        self.__receipe_list.insert(0,new Step("Initial temperature",LEVEL, initial_temperature)
        self.__cursor=1 # Begining with a transition that needs an initial temperature and a target temperature for interpolation
        self.__receipe_list.append(new Step("Receipe ended",STOP))

    def get_current_order(self):
        if(self.__receipe_list[self.__cursor].get_type()==TRANSITION) return (self.__receipe_list[self.__cursor].interpolation(self.__receipe_list[self.__cursor-1].get_temperature(), self.__timer,self.__receipe_list[self.__cursor-+].get_temperature(), datetime.datetime.now())
        else return self.__receipe_list[self.__cursor].get_temperature()

    def update_step(self,current_temperature): #Function to be called every seconds in order to update the current step
        if(self.get_current_step(self).get_type()!=STOP):
            if(self.__timer==None):
                self.__timer=datetime.datetime.now() #We start the timer by storing the begining date & time
            if(((datetime.datetime.now()-self.__timer).seconds//60)>=self.get_current_step(self).get_duration):
                self.__timer=None
                self.__cursor++

    def user_force_next_step(self):
        if(self.__cursor<len(self.__receipe_list)):
            self.__cursor++
            self.__timer=None


       
