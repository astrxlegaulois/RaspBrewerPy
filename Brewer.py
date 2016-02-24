class Brewer:
    """
        A brewer uses the thermometers and heaters in order to follow the receipe. Each brewer has a single tank who knows its own composition in order to perform kick-ass calculations'
    """


    def __init__(self, a_name, a_receipe, a_tank):
        """
            Constructor
            :param a_name: Name of the brewer
            :param a_receipe: Fully feathured receipe to be started right now!
            :param a_tank: A tank to brew in
            :type a_name: String
            :type a_receipe: Receipe
            :type a_tank: Tank
                     
            .. warnings:: This function is unprotected agains wrong parameters types or values. Use carfully
            .. todo:: Shouldn't thermometer and heaters be located in the tank instead ?
        """
        self.__name = a_name
        self.__receipe = a_receipe
        self.__tank = a_tank
        self.__thermometers=[]
        self.__heaters=[]


    def add_thermometer(self, a_thermometer):
         """
            Add a thermometer to the Brewer
            :param a_thermometer: Ready to use Thermometer object
            :type a_thermometer: Thermometer

            .. todo:: Shouldn't thermometer and heaters be located in the tank instead ?
        """
        self.__thermometers.append(a_thermometer)
      
      
    def add_heater(self, a_heater):
        """
            Add a heater to the Brewer
            :param a_heater: Ready to use Heater object
            :type a_heater: Heater

            .. todo:: Shouldn't thermometer and heaters be located in the tank instead ?
        """
        self.__heaters.append(a_heater)


    def get_name(self):
        """
            Returns the name of the Brewer
            
            :return: Name of the Brewer
            :rtype: Sting
        """
        return self.__name
