"""
    pip install beautifulsoup4 needed in order to parse the xml
"""
from bs4 import BeautifulSoup
import signal, time, sys
from select import select

from receipe import Receipe
from tank import Tank
from ingredient import Ingredient
from thermometer import Thermometer
from heater import Heater
from globalthings import *

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
        self.__receipe = None
        self.__brewing_started = False

    def config_from_file(self, a_path):
        """
            Configure the Brewer instantiates elements and populates the Tank as described by the selected config file
            :param a_path: path and name of the config file
            :type a_path: String
        """
        with open(a_path) as f:
            content = f.read()
        y = BeautifulSoup(content,"xml")
        self.__name = y.brewer['name']
        self.__receipe=Receipe("Fill me !")
        self.__receipe.config_from_file(y.brewer.receipe.contents[0])
        thermo_tank=Thermometer(y.brewer.tank.equipments.thermometer['name'], y.brewer.tank.equipments.thermometer.path.contents[0])
        if(y.brewer.tank['drivetype']=="BOOLEAN"):
            self.__tank=Tank(y.brewer.tank['name'],int(y.brewer.tank['diameter']),thermo_tank, BOOLEAN)
        elif(y.brewer.tank['drivetype']=="PID"):
            self.__tank=Tank(y.brewer.tank['name'],int(y.brewer.tank['diameter']),thermo_tank, PID)      
        elif(y.brewer.tank['drivetype']=="PREDICTIVE"):
            self.__tank=Tank(y.brewer.tank['name'],int(y.brewer.tank['diameter']),thermo_tank, PREDICTIVE)    
        for a_heater in y.find_all('heater'):
            self.__tank.add_heater(Heater(a_heater.get('name'),int(a_heater.get('power')),int(a_heater.get('GPIOpin'))))
        for an_ingredient in y.find_all('ingredient'):
            if(an_ingredient.get('type')=="Grain"):
                self.__tank.add_ingredient(Ingredient(an_ingredient.get('name'),GRAIN,float(an_ingredient.get('quantity'))))
            elif(an_ingredient.get('type')=="Water"):
                self.__tank.add_ingredient(Ingredient(an_ingredient.get('name'),WATER,float(an_ingredient.get('quantity'))))
        self.__outside_thermometer = Thermometer(y.brewer.outsidethermometer['name'],y.brewer.outsidethermometer.path.contents[0])   
        return self.__name
      

    def get_name(self):
        """
            Returns the name of the Brewer
            
            :return: Name of the Brewer
            :rtype: Sting
        """
        return self.__name


    def print_self(self):
        """
            Returns the Brewer as a human readable String ended with a new line
            
            :return: A String detailling the caracteristics of the Brewer
            :rtype: String
        """
        to_print="Name : "+self.__name
        to_print+="Outside thermometer : "+self.__outside_thermometer.print_self()
        to_print+="Tank : "+self.__tank.print_self()
        to_print+="Receipe : "+self.__receipe.print_self()+"\n"
        return to_print


    def init_brewing(self):
        """
            Checks that everything is ready for brewing and starts the receipe
            
            :return: A Boolean True = started OK, False for any anomaly
            :rtype: Boolean
        """
        if(self.__name == None or self.__tank == None or self.__receipe == None or self.__brewing_started == True):return False
        self.__brewing_started = True
        self.__receipe.start(self.__tank.get_current_temperature())
        print "***************************************************"
        print "Updated receipe "+self.__receipe.print_self()
        return True


    def brew(self):
        """
            This function is the main brewing function : ajusting the temperature according to the receipe. Function to be called regularily (every 5 seconds for instance).
        """
        while 1==1 :
            self.__receipe.update_step()
            if(self.__receipe.get_current_step()==None):
                print "Receipe completed"
                return True
            self.__tank.temperature_drive(self.__receipe.get_current_temperature_instruction())
            print "Current step : "+self.__receipe.get_current_step().print_self()
            print "Temperature instuction : "+str(self.__receipe.get_current_temperature_instruction())
            print "Current temperature : "+str(self.__tank.get_current_temperature())
 
            print 'Type "N" if you want to skip the current step',
            rlist, _, _ = select([sys.stdin], [], [], UPDATE_PERIOD)
            if rlist:
                s = sys.stdin.readline()
                if(s == "N\n"):
                    print "Skip order received"
                    self.__receipe.user_force_next_step()
            else:
                print "No input. Moving on..."
                
                



    
