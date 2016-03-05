class Tank:
    """
        A Tank has one or several heaters, a thermometer and some ingredients. This gives it a forecastable thermodynamical behaviour.
    """
    """ TODO """
    
    def add_heater(self, a_heater):
        """
            Add a heater to the Tank
            :param a_heater: Ready to use Heater object
            :type a_heater: Heater
        """
        self.__heaters.append(a_heater)
