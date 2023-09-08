import numpy as np

print('Environment module imported')

class Environment(object):
    """
    A class to represent an environment.
    ...

    Attributes
    ----------
    name : str
        name of the environment
    init_temp : float
        the initial temperature of the environment
    temp_inc_func : str
        the temperature increase function
    lin_temp_inc : float
        the annual temperature increase
    exp_temp_inc : float
        the esponential temperature increase rate

        
    Methods
    -------
    temp(self, month, temp_inc_func):
        Prints the person's name and age.
    """

    def __init__(self, init_temp: float, temp_inc_func: str, temp_inc_rate= 0.0, name='env'):
        """
        Constructs all the necessary attributes for the environment object.

        Parameters
        ----------
            name : str
                name of the environment
            init_temp : float
                the initial temperature of the environment
            temp_inc_func : str
                the temperature increase function
                1. val: 'lin' -> linear temperature increase function
                2. val: 'exp' -> exponential temperature increase function
            lin_temp_inc : float
                the annual temperature increase
            exp_temp_inc : float
                the exponential temperature increase rate
        """

        self.name = name
        self.init_temp = init_temp
        self.temp_inc_func = temp_inc_func

        self.temp_inc_rate = temp_inc_rate


    def __str__(self):
        return 


    def temp(self, time: int):
        '''
        Returns the temperature of the environment during the given month
        
            Parameters:
                    time (int): The given month

            Returns:
                    temperature (float): Temperature of the environment during the given month
        '''

        temp_inc_func = self.temp_inc_func

        try:
            if temp_inc_func == 'lin':
                temperature = self.init_temp + (time * self.temp_inc_rate)

            elif temp_inc_func == 'exp':
                temperature = self.init_temp * np.exp(time * self.temp_inc_rate)

            return temperature
        except UnboundLocalError:
            print(temp_inc_func)

        


