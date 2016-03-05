class Thermometer:
    """
        A thermometer is the object representing one the physical thermometers of the system
    """


    def __init__(self, a_name, a_path):
        """
            Constructor
            :param a_name: Name of the brewer
            :param a_path: Path of the driver's file on the system (usually of type "/sys/bus/w1/deveices/@/w1_slave")
            :type a_name: String
            :type a_path: String
        """
        self.__name = a_name
        self.__path = a_path


    def get_name(self):
        """
            Returns the name of the Thermometer
            
            :return: Name of the Thermometer
            :rtype: Sting
        """
        return self.__name


    def read_temperature(self):
        """
            Read the current temperature value
            
            :return: Themperature in °C
            :rtype: Int
        """
        tempfile = open(__path)
        text=tempfile.read()
        tempfile.close()
        tempdata=text.split("\n")[1].split(" ")[9]
        temperature=float(tempdata[2:])
        temperature=temperature/1000
        return temperature
