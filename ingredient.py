from globalthings import *

class Ingredient:
    """
        An Ingredient is a physical ingredient located in the Tank. It can be GRAIN or WATER
    """
    
    
    def __init__(self, a_name, a_type, a_quantity):
        """
            Constructor
            :param a_name: Name of the Ingredient
            :param a_type: Type of the Ingredient within GRAIN or WATER
            :param a_quantity: Quantity of the Ingredient in L for water and kg for malted grain
            :type a_name: String
            :type a_type: int = MALTED_GRAIN or WATER
            :type a_quantity: float
        """
        self.__name = a_name
        self.__ingredient_type = a_type
        self.__quantity = a_quantity


    def get_name(self):
        """
            Returns the name of the Ingredient
            
            :return: Name of the Ingredient
            :rtype: Sting
        """
        return self.__name
      
      
    def get_type(self):
        """
            Returns the type of the Ingredient
            
            :return: Type of the Ingredient
            :rtype: int = GRAIN or WATER
        """
        return self.__ingredient_type


    def get_quantity(self):
        """
            Returns the quantity of the Ingredient
            
            :return: Quantity of the ingredient (kg or Liters)
            :rtype: float
        """
        return self.__quantity
      

    def print_self(self):
        """
            Returns the Ingredient as a human readable String ended with a new line
            
            :return: A String detailling the caracteristics of the Ingredient
            :rtype: String
        """
        to_print="Name : "+self.__name
        if(self.__ingredient_type==WATER):
            to_print+=" Type : Water"
        elif(self.__ingredient_type==GRAIN):
            to_print+=" Type : Grain"
        to_print+=" Quantity : "+str(self.__quantity)+"\n"
        return to_print
