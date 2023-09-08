import Population as pop
import matplotlib.pyplot as plt


print('plotting module imported')

class plot(object):
    def __init__(self, population: pop.Population, time=36):
        self.population = population
        self.time = time

        self.selectionresults = population.selection_func(time)
        self.p_freq = self.selectionresults[0].values()

        self.W_list_dict = self.selectionresults[1]
        self.W_list = self.W_list_dict.values()

        # creating a list for the q frequencys based on the p_freq list
        self.q_freq = [1-i for i in self.p_freq]

        # calculating how many generations the timespan corresponds to
        self.gen_lenght = int(time//population.lifespan + 1)
        # then creating a list 
        self.gen_list = [i for i in range(self.gen_lenght)]


    def print_test(self):
        '''
        a silly little function for me to check if there is something whong with the lists
        '''
        print('self.p_freq:', self.p_freq)
        print('self.q_freq:', self.q_freq)
        print('self.W_list:', self.W_list)
        print('self.gen_list:', self.gen_list)


    def tpc(self):
        '''
        Plots the TPC Graph of the population

        x-axis: temperature
            self.population.tpc_xvals
        y-axis: fitness
            self.population.tpc_yvals
        '''

        # assigning the x values: temp
        x_values = self.population.tpc_xvals
        # assigning the y values: fitness
        y_values = self.population.tpc_yvals

        # create the figure
        tpc_fig = plt.figure()
        ax = tpc_fig.add_subplot()

        ax.plot(x_values, y_values)

        # making the plot *pretty*
        # setting the title and naming the axis 
        ax.set_title('Temperature Performance Curve')
        ax.set_xlabel('Temperature')
        ax.set_ylabel('Fitness')

        return (x_values, y_values)


    def dist(self):
        '''
        Plots the body temperatue distribution of the population

        x-axis: body temperature
            self.population.tpc_xvals
            limits: 
        y-axis: frequency
            self.population.tpc_yvals
            limits: [0; 1]
        '''

        # assigning the x values: body temperature
        x_values = self.population.tpc_xvals
        # assigning the y values: frequency
        y_values = [self.population.body_temp_dist_func(gen=0,body_temp=i) for i in self.population.tpc_xvals]

        # create the figure
        dist_fig = plt.figure()
        ax = dist_fig.add_subplot()

        ax.plot(x_values, y_values)

        # making the plot *pretty*
        # setting the title and naming the axis 
        ax.set_title('Body Temperature Distribution')
        ax.set_xlabel('Temperature')
        ax.set_ylabel('Frequency') 

        return (x_values, y_values)


    def W_vals(self):
        # assigning the x values: generation
        x_values = self.gen_list
        # assigning the y values: W values
        y_values = self.W_list

        # create the figure
        w_fig = plt.figure()
        ax = w_fig.add_subplot()

        ax.plot(x_values, y_values)

        # making the plot *pretty*
        # setting the title and naming the axis 
        ax.set_title('Total Fitness During the Selection')
        ax.set_xlabel('Generation')
        ax.set_ylabel('Total Fitness') 

        return (x_values,y_values)


    def allel_freq(self):
        # assigning the x values: generation
        x_values = self.gen_list
        # assigning the y values: alle frequencies
        y_value0_p = self.p_freq
        y_value1_q = self.q_freq

        # create the figure
        freq_fig = plt.figure()
        ax = freq_fig.add_subplot()


        # plot the line for p values
        ax.plot(x_values, y_value0_p, color='red')
        # plot the line for q values
        ax.plot(x_values, y_value1_q, 'blue')


        # making the plot *pretty*
        # setting the title and naming the axis 
        ax.set_title('Allel Frequencies During the Selection')
        ax.set_xlabel('Generation')
        ax.set_ylabel('Allel Frequencies') 

        return (x_values, y_value0_p, y_value1_q)