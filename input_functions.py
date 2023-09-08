'''
File name
some sort of explanation
'''
import math_functions
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import csv


print('input_functions module imported')


def import_fitness_graph(file_name):
    ''' 
    Creates two lists for the x and y-values of the input Temperature Performance Graph (TPC)
    The x-axis of a TPC graph is the temperature and the y-axis is the fitness

    The function returns a tuple  of the two lists: (temp_list, fitness_list)

            Parameters:
                    file_name (string): File name for the fitness graph 

            Returns:
                    graph_values (tuple): A tuple of the x and y-values in seperate lists
    '''

    temp_list, fitness_list = [], []
    
    # reading the .csv file with the name 'file_name' 
    try: 
        with open(file_name, 'r') as csvfile:
            plots = csv.reader(csvfile, delimiter=',')

            for row in plots:

                # adding the fist item of each row to the temperature list
                xval = row[0] 
                temp_list.append(float(xval))

                # adding the second item of each row to the fitness list
                yval = row[1]  
                fitness_list.append(float(yval))

        # temp_list contains the x-values
        # fitness_list contains the y-values
        print('tpc graph import complete')        
        return (temp_list, fitness_list)
    except FileNotFoundError:
        print('this is sample data!')
        temp_list = [10, 12, 14, 16, 18, 20]
        fitness_list = [10, 12, 14, 12, 10, 8]
        return (temp_list, fitness_list)


def get_graphic_dist(init_temp):
    '''
        Lets the user pick the body distribution graph using sliders

            Parameters:
                    pop (Population)

            Returns:
                    body_temp_dist_values (tuple): (a, scale)

                    
            --- Further Explanation ---   

            math_functions.integrate contains:
            scipy.integrate.quad(func, a, b, args=())
                    func: a Python function or method to integrate
                    a: lower limit of integration
                    loc: upper limit of integration
                    args: extra arguments to pass into the function, in this case time

    '''

    fig_dist, ax_dist = plt.subplots(1, 1)

    # initialize the skewed dist parameters
    a = 0
    loc = init_temp
    scale = 2

    x = np.linspace(0, 60)
    line, = ax_dist.plot(x, math_functions.skew_norm_dist(x, a, loc, scale), color='darkviolet')

    ax_dist.set_title('Distribution')
    fig_dist.subplots_adjust(right=0.6)

    text_dist = ax_dist.text(0.75, 0.8, 'Parameters',  # title
                         fontsize=14, verticalalignment='top', horizontalalignment='center', color='indigo',
                         weight='bold')

    a_ax = fig_dist.add_axes([0.75, 0.6, 0.2, 0.08])
    a_slider = Slider(
        ax=a_ax,
        label="Quantile Coefficient",
        valmin=0,
        valmax=20,
        valstep=0.2,
        valinit=a,
        color='plum'
    )

    scale_ax = fig_dist.add_axes([0.75, 0.4, 0.2, 0.08])
    scale_slider = Slider(
        ax=scale_ax,
        label="Standard Deviation",
        valmin=0,
        valmax=30,
        valinit=scale,
        color='lightpink'
    )

    def update(val):
        line.set_ydata(math_functions.skew_norm_dist(x, a_slider.val, loc, scale_slider.val))
        fig_dist.canvas.draw_idle()

    a_slider.on_changed(update)
    scale_slider.on_changed(update)

    resetax = fig_dist.add_axes([0.75, 0.25, 0.12, 0.05])
    reset_button = Button(resetax, 'Reset', hovercolor='0.975')

    select_ax = fig_dist.add_axes([0.75, 0.15, 0.12, 0.05])
    select_button = Button(select_ax, 'Select', hovercolor='0.975')

    def reset(event):
        a_slider.reset()
        scale_slider.reset()

    slider_vals_dict = {}

    def select(event):
        a = a_slider.val
        scale = scale_slider.val
        plt.close()
        slider_vals_dict['key'] = (a, scale)

    reset_button.on_clicked(reset)
    select_button.on_clicked(select)
    plt.show()
    slider_vals = slider_vals_dict['key']
    return slider_vals


# def get_keyboard_dist():
#     
#     
#     return 
# 