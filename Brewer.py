from bs4 import BeautifulSoup

class Brewer:
    """
        A brewer uses the thermometers and heaters in order to follow the receipe. Each brewer has a single tank who knows its own composition in order to perform kick-ass calculations'
    """

    def __init__(self):
        """
            Constructor
        """
        self.__name = None
        self.__outside_thermometer = None
        self.__tank = None


    def config_from_file(self, a_path):
        """
            Configure the Brewer instantiates elements and populates the tank from the selected config file
            :param a_path: path and name of the config file
            :type a_path: String
        """
        with open(a_path) as f:
            content = f.read()
        y = BeautifulSoup(content,"xml")
        self.__name = y.brewer['name']
        #TODO load receipe
        #TODO create and load Tank
        """
            for heater in y.brewer.tank.equipments:
            print(heater)
        """
        self.__outside_thermometer = Thermometer(y.brewer.outsidethermometer['name'],y.brewer.outsidethermometer.path.contents[0])   
        return self.__name


    def add_thermometer(self, a_thermometer):
        """
            Add a thermometer to the Brewer
            :param a_thermometer: Ready to use Thermometer object, located outside any tank
            :type a_thermometer: Thermometer
            .. warning:: Other thermometers may  be located in the tank
        """
        self.__outside_thermometer=a_thermometer
      

    def get_name(self):
        """
            Returns the name of the Brewer
            
            :return: Name of the Brewer
            :rtype: Sting
        """
        return self.__name
