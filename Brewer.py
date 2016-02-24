class Brewer:
    'A brewer uses the thermometers and heaters in order to follow the receipe. Each brewer has a single tank who knows its own composition in order to perform kick-ass calculations'

   def __init__(self, a_name, a_receipe, a_tank):
      self.__name = a_name
      self.__receipe = a_receipe
      self.__tank = a_tank
      self.__thermometers=[]
      self.__heaters=[]

   def add_thermometer(self, a_thermometer):
      self.__thermometers.append(a_thermometer)
      
   def add_heater(self, a_heater):
      self.__heaters.append(a_heater)

    def get_name(self):
        return self.__name
