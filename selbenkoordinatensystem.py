import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy import integrate as integrate
from scipy.optimize import fsolve
from scipy import stats
import csv

def import_data(w_data):
    '''
    Takes two csv files and returns their x and y values in separate lists
    :param w_data: name of the csv file for the w(Tb) graph
    :param :p_data: name of the csv file for the p(Tb) graph
    :return: a tuple with 4 lists => (temp_list0, w_list, temp_list1, p_list)
    '''
    temp_list0 = []
    w_list = []
    # import the w(Tb) Graph
    with open(w_data, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            xval = row[0]  # .replace(',', '.')
            yval = row[1]  # .replace(',', '.')
            temp_list0.append(float(xval))
            w_list.append(float(yval))
    return (temp_list0, w_list)


'''DISTRIBUTION FUNCTIONS'''

def Gauss(x, amp, mu, sigma):
    y = amp * np.exp(-(x - mu) ** 2 / (2 * sigma ** 2))
    return y


def normal_distribution(x, mu, sd):
    return stats.norm.pdf(x, mu, sd)


def skewed_normal_distribution(x, a, loc, scale):
    return stats.skewnorm.pdf(x, a, loc=loc, scale=scale)

def curvefit(x,xdata,ydata):
        curve_w = np.polyfit(xdata, ydata, 5)
        poly_w = np.poly1d(curve_w)
        return np.polyval(poly_w, x)

'''CLASSES'''

class Environment(object):
    def __init__(self, name: str, init_temp, climate_change):
        self.name = name
        self.init_temp = init_temp
        self.climate_change = climate_change
        self.monthly_temp_inc = climate_change/12

    def __str__(self):
        return '\ndie Anfangstemperatur:' + str(self.init_temp) + \
            '\ndie Temperaturänderungsrate (pro Monat):\n ' + str(self.monthly_temp_inc)

    def temp(self, month):
        '''
        returns the temperature of the environment during the given month
        '''
        return self.init_temp + self.monthly_temp_inc * month


class Population(object):
    def __init__(self, name: str, init_q: float, lifespan, w_graphname: str, dist_args,
                 environment: Environment, time_span, selection_allel, new_pop):
        self.name = name
        print(self.name)
        self.w_graphname = w_graphname
        self.init_q = init_q
        self.init_p = 1.0 - self.init_q
        self.sel_allel = selection_allel
        self.new_pop = new_pop

        self.lifespan = lifespan
        self.lifespan_as_month = lifespan*12
        self.time_span = time_span
        self.time_span_as_month = time_span*12
        self.gen_span = int(self.time_span // self.lifespan + 1)
        self.gen_span_as_month = int(self.time_span_as_month//self.lifespan_as_month + 1)
        # print('Number of generations:', self.gen_span_as_month)

        input_data = import_data(w_graphname)  # returns (temp_list0, w_list, temp_list1, p_list)
        self.fitness_graph = (input_data[0], input_data[1])  # (temp_list0, w_list)
        self.dist_args = dist_args
        self.environment = environment
        # print('environment imported\n')

        self.get_x = [i for i in range(self.gen_span_as_month)]
        if self.sel_allel == 'd':
            print('Selektion gegen den dominanten Allel')
            self.get_p = [self.p_val(i) for i in range(self.gen_span_as_month)]
            self.get_q = [1 - self.get_p[i] for i in range(len(self.get_p))]
        elif self.sel_allel == 'r':
            print('Selektion gegen den recessiven  Allel')
            self.get_q = [self.q_val(i) for i in range(self.gen_span_as_month)]
            self.get_p = [1 - self.get_q[i] for i in range(len(self.get_q))]
        elif self.sel_allel == 'h':
            print('Heterozygotenvorteil')
            self.get_p = [self.p_val0(i) for i in range(self.gen_span_as_month)]
            self.get_q = [1 - self.get_p[i] for i in range(len(self.get_p))]

    def get_vals(self):
        return [self.name, self.init_q, self.lifespan, self.w_graphname, self.dist_args,self.environment, self.time_span, self.sel_allel]

    def __str__(self):
        return 'der Populationsname: ' + self.name + \
            '\ndie Anfangsfrequenz von p: ' + str(self.init_p) + \
            '\ndie Anfangsfrequenz von q: ' + str(self.init_q) + \
            '\ndie Lebenserwartung: ' + str(self.lifespan)

    def gen(self, month: float):
        return int(month // self.lifespan_as_month)

    def month(self, gen: int):
        return self.lifespan_as_month * gen

    def w(self, temp):
        '''
        Defines the w(Tb) function using polynomial curve fitting
        :param temp: temperature
        :return: fitness for the given temperature
        '''
        curve_w = np.polyfit(self.fitness_graph[0], self.fitness_graph[1], 6)
        poly_w = np.poly1d(curve_w)
        return np.polyval(poly_w, temp)

    def p(self, temp: float, month):
        '''
        The distribution function generated as a skewed normal distribution.
        :param temp: temperature
        :param time:
        :return:
        '''
        a0, scale0 = self.dist_args
        mu_p = self.environment.temp(month)
        y = skewed_normal_distribution(temp, a0, mu_p, scale0)
        return y

    def f(self, temp: float, time):
        return self.w(temp) * self.p(temp, time)

    def root(self, ):
        roots = fsolve(self.w, [20, 50])
        return roots

    def W(self, func, n):
        '''
        Function that calculates the generational Fitness
        :param func: function self.f
        :param n: generation (int)
        :return: the
        '''
        min = self.root()[0]
        max = self.root()[1]
        integral = integrate.quad(func, min, max, args=(self.month(n)))
        return integral[0]

    def p_val(self, n: int, memo={}):
        '''
        a recursive function that calculates the p-Frequency for the given generation
        :param n: generation (int)
        :param memo:
        :return: p-Frequency of the generation n
        '''
        if self.new_pop == 0 and n == 0:
            memo.clear()
        w = self.W(self.f, n)
        if n <= 0:
            return self.init_p
        try:
            return memo[n]
        except KeyError:
            result = (self.p_val(n - 1) * w) \
                     / (1 - (self.p_val(n-1)*(1-w)*(2-self.p_val(n-1))))
            memo[n] = result
            return result

    def q_val(self, n: int, memo={}):
        '''
        a recursive function that calculates the q-Frequency for the given generation
        :param n: generation (int)
        :param memo:
        :return: q-Frequency of the generation n
        '''
        if self.new_pop == 0 and n == 0:
            memo.clear()
        w = self.W(self.f, n)
        if n <= 0:
            return self.init_q
        try:
            return memo[n]
        except KeyError:
            result = (self.q_val(n - 1) * (1 - (1 - w) * self.q_val(n - 1))) \
                     / (1 - (1 - w) * self.q_val(n - 1) * self.q_val(n - 1))
            memo[n] = result
            return result

    def p_val0(self, n: int, memo={}):
    # heterozygote advantage
        if self.new_pop == 0 and n == 0:
            memo.clear()
        w = self.W(self.f, n)
        if n <= 0:
            return self.init_p
        try:
            return memo[n]
        except KeyError:
            result = (self.p_val0(n - 1) * (1 - (1 - w) * self.p_val0(n - 1))) \
                     / (1 - (1 - w) * (1 + 2*self.p_val0(n-1)*(self.p_val0(n-1)-1)))
            memo[n] = result
            return result

    def q_reaches0(self):
        for i in range(self.gen_span):
            if self.get_q[i] <= 0.005:
                return i

    def p_reaches0(self):
        for i in range(self.gen_span):
            if self.get_p[i]  <= 0.005:
                return i

    def plot(self):
        fig1 = plt.figure(constrained_layout=True)
        gs1 = fig1.add_gridspec(3, 1)
        gs10 = gs1[0].subgridspec(1, 3)
        gs11 = gs1[1:].subgridspec(1, 4)

        ax10 = fig1.add_subplot(gs10[0])
        ax11 = fig1.add_subplot(gs10[1])
        ax12 = fig1.add_subplot(gs10[2])

        ax14 = fig1.add_subplot(gs11[:3])
        ax15 = fig1.add_subplot(gs11[3])

        # plot fitness graph/TPC
        CTmin, CTmax = int(self.root()[0]), int(self.root()[1])
        x1 = np.linspace(CTmin, CTmax)
        ax10.plot(self.fitness_graph[0], self.fitness_graph[1], 'o', color='lightcoral')
        ax10.plot(x1, self.w(x1), color='firebrick')
        ax10.set_ylim(0, 1.1)
        ax10.set_title('die Temperatur-Leistungskurve')
        ax10.set_xlabel('die Temperatur')
        ax10.set_ylabel('die Fitness')

        # plot distribution graph
        x2 = np.linspace(15,40)
        line_p, = ax11.plot(x2, self.p(x2, month=0), color='steelblue', label='Distribution')
        ax11.set_ylim(0, 0.4)
        ax11.set_xlim(15,40)
        ax11.set_title('die Populationsverteilung (in der Zeit = 0)')
        ax11.set_xlabel('die Temperatur',fontsize='large')
        ax11.set_ylabel('die Frequenz',fontsize='large')
        ax11.grid()

        # plot total fitness (W)
        x3 = np.linspace(CTmin + 2, CTmax + 1)
        y3 = self.f(x3, time=0)
        line_f, = ax12.plot(x3, y3, color='seagreen', label='Function')
        ax12.set_ylim(0, 0.4)
        ax12.set_xlabel('die Temperatur',fontsize='large')
        ax12.set_ylabel('die Funktion',fontsize='large')
        ax12.set_title('das gesamte Fitness (in der Zeit = 0)')

        init_W = self.W(self.f, n=0)
        ax12.fill_between(x3, y3, y2=0, label='A', color='lightgreen', alpha=0.7)
        ax12.grid()

        # plot Allel-Frequencies
        x4 = self.get_x
        linep0, = ax14.plot(x4, self.get_p, color='pink', label='p-Frequency')
        lineq0, = ax14.plot(x4, self.get_q, color='purple', label='q-Frequency')

        ax14.set_title('die Allelfrequenzen (in ' + str(self.time_span) + ' Jahren)')
        ax14.set_xlabel('die Generation',fontsize='large')
        ax14.set_ylabel('die Allelfrequenzen',fontsize='large')
        ax14.legend(handles=[linep0, lineq0])
        ax14.set_ylim(0,1.05)
        ax14.grid()

        ax15.get_xaxis().set_visible(False)
        ax15.get_yaxis().set_visible(False)

        text15_0 = ax15.text(0.5, 0.92, 'ALLELFREQUENZ\n',  # title
                             fontsize=14, verticalalignment='top', horizontalalignment='center', color='indigo',
                             weight='bold')
        text15_1 = ax15.text(0.5, 0.75, 'POPULATIONS INFORMATION',  # population title
                             fontsize=12, verticalalignment='top', horizontalalignment='center', color='brown',
                             weight='bold')
        text15_2 = ax15.text(0.1, 0.7, self.__str__(),  # population
                             fontsize=11, verticalalignment='top', horizontalalignment='left')
        text15_3 = ax15.text(0.1, 0.56, '\nInitial Generational Fitness:\n' + str(init_W),  # total fitness
                             fontsize=11, verticalalignment='top', horizontalalignment='left')
        text15_4 = ax15.text(0.5, 0.38, 'UMGEBUNGS INFORMATION',  # population title
                             fontsize=12, verticalalignment='top', horizontalalignment='center', color='brown',
                             weight='bold')
        text15_5 = ax15.text(0.1, 0.35, self.environment.__str__()  # environment
                             , fontsize=11, verticalalignment='top', horizontalalignment='left')

        plt.show()


def get_graphic_dist():
    fig_dist, ax_dist = plt.subplots(1, 1)
    a = 0
    loc = env_init_temp
    scale = 2
    x = np.linspace(0, 60)
    line, = ax_dist.plot(x, skewed_normal_distribution(x, a, loc, scale), color='darkviolet')
    ax_dist.set_title('die Verteilung')
    fig_dist.subplots_adjust(right=0.6)

    text_dist = ax_dist.text(0.75, 0.8, 'die Parametern',  # title
                         fontsize=14, verticalalignment='top', horizontalalignment='center', color='indigo',
                         weight='bold')

    a_ax = fig_dist.add_axes([0.75, 0.6, 0.2, 0.08])
    a_slider = Slider(
        ax=a_ax,
        label="der Quartilskoeffizient der Schiefe",
        valmin=0,
        valmax=20,
        valstep=0.2,
        valinit=a,
        color='plum'
    )

    scale_ax = fig_dist.add_axes([0.75, 0.4, 0.2, 0.08])
    scale_slider = Slider(
        ax=scale_ax,
        label="die Standard Abweichung",
        valmin=0,
        valmax=30,
        valinit=scale,
        color='lightpink'
    )

    def update(val):
        line.set_ydata(skewed_normal_distribution(x, a_slider.val, loc, scale_slider.val))
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


def compare(pop: Population, param: str, param_values:list):
    '''
    creates 4 populaions that are identicle accept the chosen parameter, assigns the different parameter values to each population
    plots them all in the same figure and produces a second figure comparing their Fixierunggeneration
    '''
    pop_name, pop_init_q, pop_lifespan, pop_w_graph, pop_distvals, pop_environment, pop_time_span, pop_sel_allel = pop.get_vals()
    param_val1, param_val2, param_val3, param_val4 = param_values

    if param == 'Anfangsfrequenz von q':
        pop1 = Population('Pop1:'+pop_name, param_val1, pop_lifespan, pop_w_graph, pop_distvals, pop_environment,
                          pop_time_span, pop_sel_allel, 0)
        pop2 = Population('Pop2:'+pop_name, param_val2, pop_lifespan, pop_w_graph, pop_distvals, pop_environment,
                          pop_time_span, pop_sel_allel, 0)
        pop3 = Population('Pop3:'+pop_name, param_val3, pop_lifespan, pop_w_graph, pop_distvals, pop_environment,
                          pop_time_span, pop_sel_allel, 0)
        pop4 = Population('Pop4:'+pop_name, param_val4, pop_lifespan, pop_w_graph, pop_distvals, pop_environment,
                          pop_time_span, pop_sel_allel, 0)

    elif param == 'der Quartilskoeffizient der Schiefe':
        pop1 = Population('Pop1:'+pop_name, pop_init_q, pop_lifespan, pop_w_graph, (param_val1,pop_distvals[1]),
                          pop_environment, pop_time_span, pop_sel_allel, 0)
        pop2 = Population('Pop2:'+pop_name, pop_init_q, pop_lifespan, pop_w_graph, (param_val2,pop_distvals[1]),
                          pop_environment, pop_time_span, pop_sel_allel, 0)
        pop3 = Population('Pop3:'+pop_name, pop_init_q, pop_lifespan, pop_w_graph, (param_val3,pop_distvals[1]),
                          pop_environment, pop_time_span, pop_sel_allel, 0)
        pop4 = Population('Pop4:'+pop_name, pop_init_q, pop_lifespan, pop_w_graph, (param_val4,pop_distvals[1]),
                          pop_environment, pop_time_span, pop_sel_allel, 0)

    elif param == 'die Standardabweichung':
        pop1 = Population('Pop1:'+pop_name, pop_init_q, pop_lifespan, pop_w_graph, (pop_distvals[1], param_val1),
                          pop_environment, pop_time_span, pop_sel_allel, 0)
        pop2 = Population('Pop2:'+pop_name, pop_init_q, pop_lifespan, pop_w_graph, (pop_distvals[1],param_val2),
                          pop_environment, pop_time_span, pop_sel_allel, 0)
        pop3 = Population('Pop3:'+pop_name, pop_init_q, pop_lifespan, pop_w_graph, (pop_distvals[1],param_val3),
                          pop_environment, pop_time_span, pop_sel_allel, 0)
        pop4 = Population('Pop4:'+pop_name, pop_init_q, pop_lifespan, pop_w_graph, (pop_distvals[1],param_val4),
                          pop_environment, pop_time_span, pop_sel_allel, 0)

    elif param == 'Anfangstemperatur':
        new_env1 = Environment(name='new',init_temp=param_val1,climate_change=pop_environment.climate_change)
        pop1 = Population('Pop1:'+pop_name, pop_init_q, pop_lifespan, pop_w_graph, pop_distvals, new_env1,
                          pop_time_span, pop_sel_allel, 0)
        new_env2 = Environment(name='new',init_temp=param_val2,climate_change=pop_environment.climate_change)
        pop2 = Population('Pop2:'+pop_name, pop_init_q, pop_lifespan, pop_w_graph, pop_distvals, new_env2,
                          pop_time_span, pop_sel_allel, 0)
        new_env3 = Environment(name='new',init_temp=param_val3,climate_change=pop_environment.climate_change)
        pop3 = Population('Pop3:'+pop_name, pop_init_q, pop_lifespan, pop_w_graph, pop_distvals, new_env3,
                          pop_time_span, pop_sel_allel, 0)
        new_env4 = Environment(name='new',init_temp=param_val4,climate_change=pop_environment.climate_change)
        pop4 = Population('Pop4:'+pop_name, pop_init_q, pop_lifespan, pop_w_graph, pop_distvals, new_env4,
                          pop_time_span, pop_sel_allel, 0)

    elif param == 'Temperaturänderungsrate':
        new_env1 = Environment(name='new',init_temp=pop_environment.init_temp,climate_change=param_val1)
        pop1 = Population('Pop1:'+pop_name, pop_init_q, pop_lifespan, pop_w_graph, pop_distvals, new_env1,
                          pop_time_span, pop_sel_allel, 0)
        new_env2 = Environment(name='new',init_temp=pop_environment.init_temp,climate_change=param_val2)
        pop2 = Population('Pop2:'+pop_name, pop_init_q, pop_lifespan, pop_w_graph, pop_distvals, new_env2,
                          pop_time_span, pop_sel_allel, 0)
        new_env3 = Environment(name='new',init_temp=pop_environment.init_temp,climate_change=param_val3)
        pop3 = Population('Pop3:'+pop_name, pop_init_q, pop_lifespan, pop_w_graph, pop_distvals, new_env3,
                          pop_time_span, pop_sel_allel, 0)
        new_env4 = Environment(name='new',init_temp=pop_environment.init_temp,climate_change=param_val4)
        pop4 = Population('Pop4:'+pop_name, pop_init_q, pop_lifespan, pop_w_graph, pop_distvals, new_env4,
                          pop_time_span, pop_sel_allel, 0)


    #LAYOUT
    fig2 = plt.figure(constrained_layout=True)
    ax14 = fig2.add_subplot()
    x4 = pop.get_x
    linep1, = ax14.plot(x4, pop1.get_p, color='lightcoral', label=param+': '+str(param_val1))
    lineq1, = ax14.plot(x4, pop1.get_q, color='red', label='q-Frequency')

    linep2, = ax14.plot(x4, pop2.get_p, color='lightblue', label=param+': '+str(param_val2))
    lineq2, = ax14.plot(x4, pop2.get_q, color='blue', label='q-Frequency')

    linep3, = ax14.plot(x4, pop3.get_p, color='limegreen', label=param+': '+str(param_val3))
    lineq3, = ax14.plot(x4, pop3.get_q, color='green', label='q-Frequency')

    linep4, = ax14.plot(x4, pop4.get_p, color='plum', label=param+': '+str(param_val4))
    lineq4, = ax14.plot(x4, pop4.get_q, color='purple', label='q-Frequency')

    ax14.set_title('die Allelfrequenzen (in ' + str(pop.time_span) + ' Jahren) \n Parametern: '+param,fontsize='x-large')
    ax14.set_xlabel('die Generation',fontsize='xx-large')
    ax14.set_ylabel('die Allelfrequenzen',fontsize='xx-large')
    ax14.legend(handles=[linep1, linep2, linep3, linep4])
    ax14.set_ylim(0, 1.05)
    ax14.grid()
    plt.savefig(pop.name+'_'+param+'.png')
    # xdata = [x/ max(param_values) for x in param_values]

    fig3 = plt.figure(constrained_layout=True)
    ax15 = fig3.add_subplot()
    xdata = param_values
    if pop.sel_allel == 'r':
        ydata = [pop1.q_reaches0(),pop2.q_reaches0(),pop3.q_reaches0(),pop4.q_reaches0()]
        for val in ydata:
            if val is None:
                print(val)
                index = ydata.index(val)
                ydata.pop(index)
                xdata.pop(index)
        print(ydata)
        xfit = [i/100 for i in range(int(min(xdata)*100),int((max(xdata)*100)+1))]
        yfit = [curvefit(i,xdata,ydata) for i in xfit]
        ax15.plot(xfit, yfit, linewidth=3, color='dodgerblue')
        ax15.scatter(xdata,ydata,color='red')

    elif pop.sel_allel == 'd':
        ydata = [pop1.p_reaches0(), pop2.p_reaches0(), pop3.p_reaches0(), pop4.p_reaches0()]
        for val in ydata:
            if val is None:
                index = ydata.index(val)
                ydata.pop(index)
                xdata.pop(index)
        print(ydata)
        xfit = [i/100 for i in range(int(min(xdata)*100),int((max(xdata)*100)+1))]
        yfit = [curvefit(i,xdata,ydata) for i in xfit]

        ax15.plot(xfit, yfit, linewidth=3, color='dodgerblue')
        ax15.scatter(xdata, ydata,color='magenta')

    ax15.set_title('der Fixierungsdauer',fontsize='xx-large')
    ax15.set_xlabel(param,fontsize='xx-large')
    ax15.set_ylabel('die Anzahl der benötigten Generationen \nfür die Fixierung',fontsize='x-large')
    ax15.grid()
    plt.show()


print('+++ ALLELFREQUENZEN VORHERSAGMODELL +++\n',
      ' Important: Enter all required values in the required format. Use a dot (.) as the decimal seperator.\n')

'''
ja = input('DO YOU WANT TO INPUT DATA BY HAND?\n yes:[0] / no:[1] ')
if ja == '0':
    print('\nEnvironment Information:')
    env_name = input('Environment Name : ')
    env_init_temp = float(input('Enter Initial Temperature of the Environment [integer/decimal]: '))
    env_climate_change = float(input('Enter Climate Change Rate (Temperature Increase per year) [integer/decimal]: '))

    print('\nPopulation Information:')
    pop_name = input('Enter Population Name : ')
    pop_init_q = float(input('Enter Initial q Frequency [decimal]:'))
    pop_lifespan = float(input('Enter Lifespan: '))
    pop_w_graph = input('Enter the File Name for the TPC Graph : ')
    print('Please take the generation span into consideration, recomended timespan : ' + str(200*pop_lifespan))
    pop_timespan = float(input('Enter The Desired Timespan [integer/decimal]: '))
    print('Enter the allel, that will be selected:\nfor recessiv enter [r]\nfor dominant enter [d]')
    pop_sel_allel =input('for heterozygot advantage enter [h]\n ')

    print('Choose the Method of Distribution Input:\nfor Graphic enter [G]')
    dist = input('for Keyboard enter [K]\n')

    if dist == 'G' or dist == 'g':
        pop_distvals = get_graphic_dist()
    elif dist == 'K' or dist == 'k':
        a = float(input('Enter required values for the Distribution Graph [both as decimals]:\na: '))
        scale = float(input('scale: '))
        pop_distvals = (a, scale)
    print('\n')

    env = Environment(name=env_name,
                      init_temp=env_init_temp,
                      climate_change=env_climate_change)

    population = Population(name=pop_name,
                            init_q=pop_init_q,
                            lifespan=pop_lifespan,
                            w_graphname=pop_w_graph,
                            dist_args=pop_distvals,
                            environment=env,
                            time_span=pop_timespan,
                            selection_allel=pop_sel_allel,
                            new_pop=1)
elif ja == '1':
    env = Environment(name='The Lakes',
                      init_temp=30,
                      climate_change=2)

    population = Population(name='S.punctum',
                            init_q=0.4,
                            lifespan=0.05,
                            w_graphname='S.punctum-TPC.csv',
                            dist_args=(2, 4),
                            environment=env,
                            time_span=20,
                            selection_allel='r',  # r > recessiv, d > dominant, h > heterozygotadvantage
                            new_pop=1)
'''
env = Environment(name='The Lakes',
                    init_temp=30,
                    climate_change=2)

population = Population(name='S.punctum',
                        init_q=0.4,
                        lifespan=0.05,
                        w_graphname='S.punctum-TPC.csv',
                        dist_args=(2, 4),
                        environment=env,
                        time_span=20,
                        selection_allel='r',  # r > recessiv, d > dominant, h > heterozygotadvantage
                        new_pop=1)


# compare(population, 'Anfangstemperatur',[10, 20, 30, 40])
#
# compare(population,'Temperaturänderungsrate',[1,0.2,0.17,0.075])
#
# compare(population, 'Anfangsfrequenz von q', [0.2, 0.4, 0.6, 0.8])
#
# compare(population, 'der Quartilskoeffizient der Schiefe', [-4,-2,0,2])
#
compare(population, 'die Standardabweichung',[8, 6, 4, 2])
#
# population.plot()

