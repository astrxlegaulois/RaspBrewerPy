"""
    pip install beautifulsoup4 needed in order to parse the xml
"""

import datetime
from bs4 import BeautifulSoup

from globalthings import *
from step import Step

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


    def config_from_file(self, a_path):
        """
            Creates the Steps according to the selected receipe file
            :param a_path: path and name of the receipe
            :type a_path: String
        """
        with open(a_path) as f:
            content = f.read()
        y = BeautifulSoup(content,"xml")
        self.__name = y.receipe['name']
        found_steps=y.find_all('step')
        for index in range(1,len(found_steps)+1):
            for i in range(0,len(found_steps)):
                if(int(found_steps[i].get('index'))==index):
                    n_name=found_steps[i].get('name')
                    if(found_steps[i].get('type')=="LEVEL"):
                        n_type=LEVEL
                    elif(found_steps[i].get('type')=="TRANSITION"):
                        n_type=TRANSITION
                    elif(found_steps[i].get('type')=="STOP"):
                        n_type=STOP
                    n_duration=int(found_steps[i].get('duration'))
                    if(found_steps[i].get('temperature')==None):
                        n_temperature=None
                    else:
                        n_temperature=float(found_steps[i].get('temperature'))
                    n_inertia=found_steps[i].get('inertia')
                    self.add_step(Step(n_name,n_type,n_duration,n_temperature,n_inertia))
                    break
        return self.__name


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
            :rtype: float
        """
        if(self.__receipe_list[self.__cursor].get_type()==TRANSITION):
	    return (self.__receipe_list[self.__cursor].interpolation(self.__receipe_list[self.__cursor-1].get_temperature(), self.__timer,self.__receipe_list[self.__cursor+1].get_temperature(), datetime.datetime.now()))
        else:
	    return self.__receipe_list[self.__cursor].get_temperature()


    def get_next_temperature_instruction(self):
        """
            Returns the next non transition Step's temperature instruction, according to the receipe. If current step is a non transition, the current temperature instruction is returned
            
            :return: The temperature instruction of the next non transition step, in degrees Celcius. Or 0 if there is no next step
            :rtype: float
        """
        if(self.__receipe_list[self.__cursor].get_type()==TRANSITION):
            if(self.__cursor+1<len(self.__receipe_list)):
                return self.__receipe_list[self.__cursor+1].get_temperature()
            else:
                print "next_temp_instruct ERROR : End of receipe"
                return 0
        else:
            return self.__receipe_list[self.__cursor].get_temperature()


    def get_current_step(self):
        """
            Returns the currently being performed Step.
            
            :return: The current Step or None is the receipe is over
            :rtype: Step or None
        """
        if(self.__cursor>=len(self.__receipe_list)):
            return None
        else:
            return self.__receipe_list[self.__cursor]
            
    def goto_next_step(self):
        """
            This function is called when it is needed to go to the next step.
        """
        if(self.__cursor<len(self.__receipe_list)):
            self.__cursor+=1
            self.__timer==datetime.datetime.now() #We restart the timer by storing the begining date & time for the new step  

    def update_step(self):
        """
            This function is making sure that we change the current Steps accordingly to the Receipe. Function to be called regularily (every second for instance) in order to update the current step
        """
        print "self.__cursor"+str(self.__cursor)+"list_len:"+str(len(self.__receipe_list))
        if(self.__cursor>=len(self.__receipe_list)):
            return None
        if(self.__timer==None):
            self.__timer=datetime.datetime.now() #We start the timer by storing the begining date & time
        print "step begining time:"+str(self.__timer)+"now is :"+str(datetime.datetime.now())
        if(((datetime.datetime.now()-self.__timer).total_seconds()//60)>=self.get_current_step().get_duration()):
            self.goto_next_step()

    def user_force_next_step(self):
        """
            This function allows the user to skip to the next Step. It is the only way to pass through a STOP Step.
        """
        self.goto_next_step()
            
    def transition_complete(self):
        """
            This function is called when the temperature reached the target. It is the normal way to pass through a TRANSITION Step.
        """
        self.goto_next_step()

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


       
