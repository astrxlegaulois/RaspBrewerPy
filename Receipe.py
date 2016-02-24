LEVEL = 2
TRANSITION = 1
STOP = 0

import datetime

class Step:
   'A step is a componnent of a receipe. It can be a transition, level step or stop until conformation'
   
   # a_name is a string, a_type is a type (CONST), a_duration in minutes, a_themperature in degrees celcius (not needed for transition)
   def __init__(self, a_name, a_type, a_duration, a_themperature=0):
      self.__name = a_name
      self.__step_type = a_type
      self.__themperature = a_themperature
      self.__duration = a_duration
      if(self.__duration==0)self.__duration++
      
   def get_name(self):
      return self.__name
      
   def get_type(self):
      return self.__step_type

   def get_themperature(self):
      return self.__themperature
      
   def get_duration(self):
      return self.__duration
      
   #in Steps so that one day we can code different continiuous transitions depending of a new parameter of this Step
   # times as python dateTimes, themperatures in Celcius
   def interpolation(self, start_themp, start_time, stop_themp, current_time):
      #linear interpolation
      delta_th=stop_themp-start_themp
      delta_time=current_time-start_time
      return start_themp+delta_th*(delta_time.seconds()/(self.__duration*60))

class Receipe:
   'A receipe is a list of themperature transitions, level steps and stops (waiting for human confirmation'

   def __init__(self, a_name):
      self.__name = a_name
      self.__receipe_list=[]
      self.__cursor=None
      self.__timer=None

   def add_step(self, a_step):
      #TODO exception if(len(__receipe_list)==0 && a_step.get_type()==LEVEL)
      #TODO exception if no transistion between 2 steps of different themperature
      #TODO exception if two transitions are consecutive
      self.__receipe_list.append(a_step)

   def get_name(self):
      return self.__name
      
   def start(self,initial_themperature):
      self.__receipe_list.insert(0,new Step("Initial themperature",LEVEL, initial_themperature)
      self.__cursor=1 # Begining with a transition that needs an initial themperature and a target themperature for interpolation
      self.__receipe_list.append(new Step("Receipe ended",STOP))

   def get_current_order(self):
      if(self.__receipe_list[self.__cursor].get_type()==TRANSITION) return (self.__receipe_list[self.__cursor].interpolation(self.__receipe_list[self.__cursor-1].get_themperature(), self.__timer,self.__receipe_list[self.__cursor-+].get_themperature(), datetime.datetime.now())
      else return self.__receipe_list[self.__cursor].get_themperature()

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


       
