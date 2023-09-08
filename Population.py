import numpy as np
import warnings
warnings.simplefilter('ignore', np.RankWarning)

import Environment
import input_functions 
import math_functions 


print('Population module imported')

class Population(object):
    """
        A class to represent a population. 
        ... more specificly its genetic dynamics.

        ...

        Attributes
        ----------
        name : str
            name of the population
        lifespan : float
            expected lifespan of the population in months
        environment : Environment 
            the environment that the population lives in
        
       selection_case : str
            the selected case
            1. val: 'recessiv' -> selection 
            2. val: 'dominant' -> 
            3. val: 'heterozygote_adv' ->

        init_q: float
            the initial q-frequency    
        tpc_graph_file : str
            the name of the TPC graph
        body_temp_dist: tuple
            [0]: a value
            [1]: scale value
        new_pop: Boolean
            True: new population
            False: same population
            

        Methods
        -------
        info(additional=""):
            Prints the person's name and age.

        get_attributes():

        time_interval(gen):


    """

    def __init__(self, name: str, lifespan: float, environment: Environment, 
                 selection_case: str, init_q: float, tpc_file_name: str, body_temp_dist, new_pop=False):
        
        self.name = name
        self.lifespan = lifespan # in months!!!
        self.environment = environment

        self.selection_case = selection_case
        self.init_q = init_q
        self.init_p = 1.0 - self.init_q
        
        # initializing the tpc graph values
        self.tpc_file_name = tpc_file_name
        self.tpc_graph = input_functions.import_fitness_graph(tpc_file_name)
        self.tpc_xvals = self.tpc_graph[0]
        self.tpc_yvals = self.tpc_graph[1]

        # initiliazing the body temperature distribution graph values
        self.body_temp_dist = body_temp_dist
        self.body_temp_a = body_temp_dist[0]
        self.body_temp_scale = body_temp_dist[1]

        self.new_pop = new_pop

        # curve fitting for the tpc graph
        fitness_curve = np.polyfit(self.tpc_xvals, self.tpc_yvals, deg=6)
        self.poly_w = np.poly1d(fitness_curve)

        self.roots = math_functions.get_roots(self.tpc_func)
        

    def get_attributes(self):
            '''
            Returns the attributes of the Population class in a list

            ind         attribute
            0           name
            1           lifespan
            2           environment
            3           selection_case
            4           init_q
            5           tpc_file_name
            6           body_temp_dist
            '''
            return [self.name, self.lifespan, self.environment, self.selection_case, self.init_q, self.tpc_file_name, self.body_temp_dist]


    def __str__(self):
        string = 'name:'+str(self.name)+'\nlifespan:'+str(self.lifespan)+'\nselection case:'+str(self.selection_case)+'\nbody_temp:'+str(self.body_temp_dist)+'\n----\ninit temp:'+str(self.environment.init_temp)
        return string


    def time_interval(self, gen):
        '''
            Returns a 2 item list with the beginning and end months of the generation
            Parameters:
                    gen (int): generation

            Returns:
                    time_intervsl (list): [beginning, end]

                    
            --- Further explanation ---
            Example:
            When the lifespan of the population is 3 months (1 gen = 3 months)
            the time intervals for generations would be as follows: [0, 3], [3, 6] 
            '''
        time_interval = []

        begin = self.lifespan * (gen - 1)
        end =  self.lifespan * gen

        time_interval[0] = begin
        time_interval[1] = end

        return time_interval


    def average_time(self, gen):
        '''
            Determines the temperature performance curve using *polynomial curve fitting
            and returns the corresponding fitness value  

            Parameters:
                    gen (int): generation

            Returns:
                    avarege_time (float): corresponding fitness value

                    
            --- Further explanation ---
            Example:
            When the lifespan of the population is 3 months (1 gen = 3 months)
            the time intervals for generations would be as follows: [0, 3], [3, 6]
            and his function returns the average (or the 'Mittelwert') of the time interval
            average_time(4) 
            '''
        average_time = (gen -0.5) * self.lifespan
        return average_time


    def tpc_func(self, body_temp):
        '''
            Determines the temperature performance curve using *polynomial curve fitting
            and returns the corresponding fitness value  

            Parameters:
                    body_temp (int): body temperature

            Returns:
                    fitness (float): corresponding fitness value

                    
            --- Further explanation ---

            np.polyfit(x, y, **deg)
                x: an array of x values
                y: an array of y values
                deg: the degree of the polynomial function 

            The goal is to find the best fitting polynomial function to the .csv data

            * other curve fitting methods could be tested
            ** deg=6 gives satisfactory results both in duration and accuracy. However other options can be tested.
        '''
        # print('     tpc_func func is being called')

        fitness = np.polyval(self.poly_w, body_temp)
        return fitness


    def body_temp_dist_func(self, gen, body_temp):
        '''
            Determines the body temperature distribution function for the generation
            and returns the frequency of the body temperature   

            Parameters:
                    gen (int): generation
                    body_temp (float): the body temperature whose frequency is calculated

            Returns:
                    frequency (float): a value between 0.0-1.0 


            --- Further Explanation ---

            math_functions.skew_norm_dist is:
                np.stats.norm.pdf(x, a, loc, stats)
                    a: skewness parameter 
                    loc: mean
                    scale: standard deviation

            The mean of the function is equal to the environment temperature:
            mean = self.environment.temp(average_time)

            The other parameters don't change in time.
        '''
        # print('     body_temp_dist_func func is being called')
        average_time = self.average_time(gen)
        mean = self.environment.temp(average_time)
        a, scale = self.body_temp_dist

        frequency = math_functions.skew_norm_dist(x= body_temp, a= a, loc= mean, scale= scale)
        return frequency


    def product_func(self, gen ,body_temp):
        '''
            The product function of tpc_func() and body_temp_dist_func()

            Parameters:
                    time (float): the month
                    body_temp (float): body temperature

            Returns:
                    product (float): product of the two functions

                    
            *** Further explanation:        
            This is an intermediate step to calculate the total fitness of the population.
            The integal of this function gives the total fitness.
        '''
        # print('     product_func is being called')
        average_time = self.average_time(gen)
        product = self.tpc_func(body_temp) * self.body_temp_dist_func(average_time, body_temp)
        return product
         

    def total_fitness_func(self, product_func, gen):
        '''
            Calculates the integral of the product_fun()

            Parameters:
                    product_func (function)
                    gen (int): generation

            Returns:
                    total_fitness (float): total fitness of the generation (refered to as 'W')

                    
            --- Further Explanation ---   

            math_functions.integrate contains:
                scipy.integrate.quad(func, a, b, args=())
                    func: a Python function or method to integrate
                    a: lower limit of integration
                    loc: upper limit of integration
                    args: extra arguments to pass into the function, in this case time

        '''
        # print('     total_fitness_func is being called')
        average_time = self.average_time(gen)
        total_fitness = math_functions.integrate(product_func, average_time, roots=self.roots)

        return total_fitness
    

    def selection_func(self, time: float, p_val_dict={}, W_val_dict={}):
        '''
            some real great definition 

            Parameters:
                    gen (int): generation
                    # memo (dictionary) = {}: recursive function optimization something

            Returns:
                    a tuple: (p_val_dict, W_val_dict)
                    p_val_dict (dictionary): key-> generation, item-> p_value 
                    W_val_dict (dictionary): key-> generation, item-> W_value


                    
            --- Further explanation ---
            
            
        '''

        # check if new population
        if self.new_pop == True:
            p_val_dict.clear()
            W_val_dict.clear()

        # time !!
        gen_lenght = int(time//self.lifespan + 1)
        

        if self.selection_case == 'recessiv':
            for gen in range(gen_lenght):
                p_val, W_val = self.rec_q(gen)

                p_val_dict[gen] = p_val
                W_val_dict[gen] = W_val

        elif self.selection_case == 'dominant':
            for gen in range(gen_lenght):
                p_val = self.dom_p(gen)
                p_val_dict[gen] = p_val 

                W_val = self.dom_p(gen)[1]
                W_val_dict[gen] = W_val
        
        elif self.selection_case == 'heterozygote_adv':
            for gen in range(gen_lenght):
                p_val = self.het_adv_p(gen)
                p_val_dict[gen] = p_val 

                W_val = self.het_adv_p(gen)[1]
                W_val_dict[gen] = W_val_dict
        
        print('dictionaries complete')

        return (p_val_dict, W_val_dict)


    def rec_q(self, gen: int, memo={}):
        '''
            some real great definition 

            Parameters:
                    gen (int): generation
                    memo (dictionary) = {}: recursive function optimization something

            Returns:
                    p_value (float): calculated p value for the generation
                    W_value (float): calculated W value for the generation

                    
            --- Further explanation ---
            The formula: q(n+1) = q*(1-s*q) / 1-sq^2
            
        '''
        print('gen:', gen)
        # check if it is the same population
        if gen <= 0 and self.new_pop == True:
            memo.clear()

        # calculate the total fitnes aka. W for the generation
        W = self.total_fitness_func(product_func=self.product_func, gen=gen)
        
        if gen <= 0:
            # for the fist generation return init_q 
            # print('     return for gen<=0')
            memo[0] = (1-self.init_q, W)
            return (1-self.init_q, W)
        
        else:    
            try:
                # check if the q frequency for this generation was already calculated, if so return that
                print('     returns from memory')
                return memo[gen]
            
            except KeyError:
                # if the requested value wasnt already calculated (wasnt in memory), calculate it
                
                # calculate q and s using pre-defined functions 
                # print('except is running')
                # print(memo)

                q = 1- memo[gen-1][0]
                s = 1 - W

                p_value = 1-((q * (1-s*q)) / (1-s*q*q))
                memo[gen] = (p_value, W)
                return (p_value, W)


    def dom_p(self, gen: int, memo={}):
        '''
            some real great definition 

            Parameters:
                    gen (int): generation
                    memo (dictionary) = {}: recursive function optimization something

            Returns:
                    p_value (float): calculated p value for the generation

                    
            --- Further explanation ---
            The formula: p(n+1) = p(1-s) / 1-ps(2-p)
            
        '''
        print('gen:', gen)
        # check if it is the same population
        if self.new_pop == True:
            memo.clear()

        # calculate the total fitnes aka. W for the generation
        W = self.total_fitness_func(self.product_func, gen)
        
        if gen <= 0:
            # for the fist generation return init_p 
            return (self.init_p, W)
        
        try:
            # check if the p frequency for this generation was already calculated, if so return that
            return (memo[gen], W)
        
        except KeyError:
            # if the requested value wasn't already calculated (wasnt in memory), calculate it
            
            # calculate p and s using pre-defined functions 
            
            p = self.dom_p(gen-1)[0]
            s = 1 - W

            p_value = (p * (1-s)) / (1 - (p*s*(2 - p)))
            return (p_value, W)


    def het_adv_p(self, gen: int, memo={}):
        '''
            some real great definition 

            Parameters:
                    gen (int): generation
                    memo (dictionary) = {}: recursive function optimization something

            Returns:
                    p_value (float): calculated p value for the generation

                    
            --- Further explanation ---
            The formula: p(n+1) = p(1-ps) / 1-s(1+2p^2-2p)
            
        '''
        print('gen:', gen)
        # check if it is the same population
        if self.new_pop == True:
            memo.clear()

        # calculate the total fitnes aka. W for the generation
        W = self.total_fitness_func(self.product_func, gen)
        
        if gen <= 0:
            # for the fist generation return init_p 
            return (self.init_p, W)
        
        try:
            # check if the p frequency for this generation was already calculated, if so return that
            return (memo[gen], W)
        
        except KeyError:
            # if the requested value wasn't already calculated (wasnt in memory), calculate it
            
            # calculate p and s using pre-defined functions 
            p = self.het_adv_p(gen-1)[0]
            s = 1 - W

            p_value = (p * (1 - (p*s))) / (1 - (s*(1 + (2*p*p) - (2*p))))
            return (p_value, W)

'''
    def fixation_func(self):

        if self.selection_case == 'recessiv':
            for i in range(self.gen_span):
                if self.get_q[i] <= 0.005:
                    return i

        elif self.selection_case == 'dominant':
            for gen in gen_lenght:
                p_val = self.dom_p(gen)
                p_val_dict[gen] = p_val 
        
        elif self.selection_case == 'heterozygote_adv':
            for gen in gen_lenght:
                p_val = self.het_adv_p(gen)
                p_val_dict[gen] = p_val 

'''



    

