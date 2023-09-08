from typing import Any, Optional, Tuple, Union
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from PIL import ImageTk, Image

import math_functions
import Environment
import Population 
import input_functions
import plotting_gui
from settings import *
import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog as fd


# THE ACTUAL APP
class Modellapp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)

        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.window_width = 1000
        self.window_height = 600
        self.minsize(1000, 600)

        # fonts
        global mainfont, titlefont, subtitlefont, smallfont, buttonfont, boldfont 
        mainfont = ctk.CTkFont(FONT, MAIN_TEXTSIZE)
        titlefont = ctk.CTkFont(FONT, size=TITLE_TEXTSIZE, weight='bold')
        subtitlefont = ctk.CTkFont(FONT, size=TITLE_TEXTSIZE-8, weight='bold')
        smallfont = ctk.CTkFont(FONT, MAIN_TEXTSIZE-4)
        buttonfont = ctk.CTkFont(FONT, MAIN_TEXTSIZE-8)
        boldfont = ctk.CTkFont(FONT, size=S_TEXTSIZE, weight='bold')

        # centering the window on the screen
        left = int((self.screen_width-self.window_width)/2)
        top = int((self.screen_height-self.window_height)/2)

        self.geometry(f'{self.window_width}x{self.window_height}+{left}+{top}')

        # customising the app icon
        ctk.CTk.iconbitmap(self, default='')
        ctk.CTk.wm_title(self, 'Temperature Based Selection Model')


        container = ctk.CTkFrame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        # the dictionary where all the frames are supposed to be at
        self.frames = {}

        for F in (StartPage, EnvPage, PopPage, LoadingPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky='nsew')
 
        frame = ResultsPage(container, self)
        self.frames[ResultsPage] = frame
        frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame(StartPage)
    

    def show_frame(self, cont):
         
         frame = self.frames[cont]
         frame.tkraise()



# START PAGE
class StartPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=main)

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1,2,3), weight=1)

        bg = ctk.CTkImage(Image.open("back8.jpg"), size=(controller.screen_width, controller.screen_height))
        labelbg = ctk.CTkImage(Image.open("labelbg.jpg"), size=(controller.screen_width, 280))
        smalllabelbg = ctk.CTkImage(Image.open("smalllabelbg.jpg"), size=(controller.screen_width, 80))

        bg_label = ctk.CTkLabel(self, text='e', image=bg)



        # widgets
        welcomelabel = ctk.CTkLabel(self, text='\nWelcome to the', font=subtitlefont,
                                     text_color=light_main, image=labelbg)
        title = ctk.CTkLabel(self, text='Temperature Based Selection Modeln',
                             font=titlefont, text_color=accent, image=labelbg)

        nextbutton = ctk.CTkButton(self, text= 'Next', command=lambda: controller.show_frame(EnvPage),
                                   fg_color=light_main, hover_color=light_secondary, text_color=main,
                                   font=subtitlefont, width=240, height=60)
        additionaltext = ctk.CTkLabel(self, text='god does not play dice,\nor does she?', text_color=light_secondary,
                                      font=mainfont, image=smalllabelbg)

        # layout
        bg_label.grid(row=0, column=0, rowspan=4, sticky='nsew')
        # welcomelabel.grid(row=0, column=0, pady=10, sticky='nsew')
        title.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        nextbutton.grid(row=2, column=0, padx=20)
        additionaltext.grid(row=3, column=0,pady=20, sticky='nsew')
  

# LOADING PAGE
class LoadingPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BACKGROUND_COLOR)

        # Label
        label = ctk.CTkLabel(self, text='\n\n\nwell its loading...',
                             text_color=TITLE_COLOR,
                             font=titlefont)
        label.pack(fill='both')


# ENV PAGE ITSELF
class EnvPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(master=parent, fg_color=BACKGROUND_COLOR)
        self.controller = controller

        # grid configuration
        self.rowconfigure(0,weight=3)
        self.rowconfigure((1,2,3,4,5),weight=1)
        self.rowconfigure(6,weight=2)
        self.columnconfigure((0,1), weight=4)


        # ctk Variables
        self.init_temp_val = ctk.DoubleVar(value=28)
        self.temp_inc_func_val = ctk.StringVar(value='lin')
        self.temp_inc_rate_val = ctk.DoubleVar(value=0.2)
        self.time_val = ctk.IntVar(value=12)

        # title and frames
        title_label = ctk.CTkLabel(self, text='ENVIRONMENT INFO', font=titlefont, text_color=TITLE_COLOR)

        init_temp_frame(self, self.init_temp_val)
        temp_inc_func_frame(self, self.temp_inc_func_val)
        temp_inc_rate_frame(self, self.temp_inc_rate_val)
        time_frame(self, self.time_val)
        temp_func_plot_frame(self)
        

        # buttons
        backbutton = ctk.CTkButton(self, text='Back', command=lambda: controller.show_frame(StartPage),
                                   fg_color=BUTTON_COLOR, hover_color=B_HOVER_COLOR, text_color=B_TEXT_COLOR,
                                   font=buttonfont)
        nextbutton = ctk.CTkButton(self, text= 'Next', command=lambda: self.next_func(),
                                   fg_color=BUTTON_COLOR, hover_color=B_HOVER_COLOR, text_color=B_TEXT_COLOR,
                                   font=buttonfont)
        
        # layout
        title_label.grid(row=0, column=0, columnspan=2)
        backbutton.grid(row=5, column=0, sticky='e', padx=5)
        nextbutton.grid(row=5, column=1, sticky='w', padx=5)
        

    def get_input_values(self):
        # print('EnvPage.get_input_values: ', self.init_temp_val.get(), self.temp_inc_func_val.get(), self.temp_inc_rate_val.get(), self.time_val.get())
        return (self.init_temp_val.get(), self.temp_inc_func_val.get(), self.temp_inc_rate_val.get(), self.time_val.get())

    def next_func(self):
        self.controller.show_frame(PopPage)
        self.get_input_values()



# ENV PAGE FRAMES
class init_temp_frame(ctk.CTkFrame):
    def __init__(self, parent, init_temp_val):
        '''
        Initial Temperature
        ---
        val: (float)
        '''
        super().__init__(master=parent, fg_color=FRAME_COLOR)
        self.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # grid configuration
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # widgets
        init_temp_label = ctk.CTkLabel(self, text='Initial Temperature',
                                       font=mainfont ,text_color=TEXT_COLOR)
        init_temp_entry = ctk.CTkEntry(self, textvariable=init_temp_val,
                                       fg_color=ENTRY_COLOR ,text_color=E_TEXT_COLOR,
                                       border_color=E_BORDER_COLOR, font=mainfont,
                                       width=200)
        
        # layout
        init_temp_label.grid(row=0, column=0, sticky='w', padx=20, pady=10)
        init_temp_entry.grid(row=0, column=1, sticky='e', padx=10, pady=20)

class temp_inc_func_frame(ctk.CTkFrame):
    def __init__(self, parent, temp_inc_func_val):
        '''
        Temperature Increase Function
        ---
        val: (str)
        linear -> 'lin'
        exponential -> 'exp'
        '''
        super().__init__(master=parent, fg_color=FRAME_COLOR)
        self.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

        # grid configuration
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2)
        self.columnconfigure((1,2), weight=1)

        # widgets
        temp_inc_func_label = ctk.CTkLabel(self, text='Temperature Increase\nFunction',
                                           font=mainfont, text_color=TEXT_COLOR)
        temp_inc_func_lin = ctk.CTkRadioButton(self, text='Linear', value='lin',
                                               variable=temp_inc_func_val,
                                               fg_color=RADIOBUTTON_COLOR,
                                               hover_color=RB_HOVER_COLOR,
                                               border_color=RB_BORDER_COLOR,
                                               text_color=RB_TEXT_COLOR,
                                               font=smallfont)
        temp_inc_func_exp = ctk.CTkRadioButton(self, text='Exponential', value='exp', 
                                               variable=temp_inc_func_val,
                                               fg_color=RADIOBUTTON_COLOR,
                                               hover_color=RB_HOVER_COLOR,
                                               border_color=RB_BORDER_COLOR,
                                               text_color=RB_TEXT_COLOR,
                                               font=smallfont)

        # layout
        temp_inc_func_label.grid(row=0, column=0, sticky='w', padx=20, pady=10)
        temp_inc_func_lin.grid(row=0, column=1)
        temp_inc_func_exp.grid(row=0, column=2)
        
class temp_inc_rate_frame(ctk.CTkFrame):
    def __init__(self, parent, temp_inc_rate_val):
        '''
        Temperature Increase Rate
        ---
        val: (float)
        '''
        super().__init__(master=parent, fg_color=FRAME_COLOR) 
        self.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)

        # grid configuration
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        
        # widgets
        temp_inc_rate_label = ctk.CTkLabel(self, text='Temperature Increase\nRate',
                                           font=mainfont ,text_color=TEXT_COLOR)
        temp_inc_rate_entry = ctk.CTkEntry(self, textvariable=temp_inc_rate_val,
                                           fg_color=ENTRY_COLOR ,text_color=E_TEXT_COLOR,
                                           border_color=E_BORDER_COLOR, font=mainfont,
                                           width=200)

        # layout
        temp_inc_rate_label.grid(row=0, column=0, sticky='w', padx=20, pady=10)
        temp_inc_rate_entry.grid(row=0, column=1, sticky='e', padx=10, pady=20)

class time_frame(ctk.CTkFrame):
    def __init__(self, parent, time_val):
        super().__init__(master=parent, fg_color=FRAME_COLOR) 
        self.grid(row=4, column=0, sticky='nsew', padx=10, pady=10)

        # grid configuration
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # widgets
        time_label = ctk.CTkLabel(self, text='Time',font=mainfont ,text_color=TEXT_COLOR)
        time_entry = ctk.CTkEntry(self, textvariable=time_val,
                                fg_color=ENTRY_COLOR ,text_color=E_TEXT_COLOR,
                                border_color=E_BORDER_COLOR, font=mainfont,
                                width=200)
        
        # layout
        time_label.grid(row=0, column=0, sticky='w', padx=20, pady=10)
        time_entry.grid(row=0, column=1, sticky='e', padx=10, pady=20)

class temp_func_plot_frame(ctk.CTkFrame):
    def __init__(self, parent):
        '''
        Temperature Plot
        ---

        '''
        super().__init__(master=parent, fg_color=FRAME_COLOR)
        self.grid(row=1, column=1, rowspan=4, sticky='nsew', padx=10, pady=10)
        self.parent = parent

        # grid configuration
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=6)
        self.columnconfigure(0, weight=1)

        # initializing a matplotlib figure
        figure = plt.figure(figsize=(5,4))
        self.ax = figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(figure, self)
        self.canvas.draw()

        # widgets
        self.plotbutton=ctk.CTkButton(self, text="plot", command=lambda: self.draw_plot(self.ax, self.canvas),
                                      fg_color=BUTTON_COLOR, hover_color=B_HOVER_COLOR, text_color=B_TEXT_COLOR,
                                      font=buttonfont)

        # layout
        self.canvas.get_tk_widget().grid(row=1, column=0, padx=40, pady=20, sticky='nsew')
        self.plotbutton.grid(row=0,column=0, padx=10, pady=10)
        
    def draw_plot(self, ax, canvas):  
        ''' 
        Draw Plot
        ---
        clears the canvas
        creates an environment object with the input values
        plots the environment temperature for 24 months
        '''
        # print(str(self.parent.get_input_values()))

        ax.clear()  # clears the canvas
  
        a, b, c, time = self.parent.get_input_values()   
        print(a, b, c)

        env = Environment.Environment(init_temp=a, temp_inc_func=b, temp_inc_rate=c)

        x_values = [i for i in range(time)]
        y_values = [env.temp(i) for i in range(time)]

        ax.set_title('Environment Temperature', color=PLOT_TEXT_COLOR)
        ax.set_xlabel('Time (in months)', color=PLOT_TEXT_COLOR2)
        ax.set_ylabel('Temperature in (C)', color=PLOT_TEXT_COLOR2)

        ax.plot(x_values, y_values, color=PLOT_COLOR)
        canvas.draw()
        


# POP PAGE ITSELF
class PopPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(master=parent, fg_color=BACKGROUND_COLOR)
        self.app = parent
        self.controller = controller

        # layout
        self.rowconfigure((0,1,2),weight=3)
        self.rowconfigure((3,4), weight=1)
        self.columnconfigure((0,1), weight=4)


        # data
        self.pop_name_val = ctk.StringVar(value='')
        self.lifespan_val = ctk.DoubleVar(value=1.0)
        self.init_q_val = ctk.DoubleVar(value=0.5)
        self.tpc_file_name_val = ctk.StringVar()
        self.body_temp_a_val = ctk.DoubleVar(value=4.0)
        self.body_temp_scale_val = ctk.DoubleVar(value=2.0)
        self.body_temp_dist_val = (self.body_temp_a_val.get(), self.body_temp_scale_val.get())
        self.selection_case_val = ctk.StringVar(value='recessiv')


        # widgets
        pop_page_title = ctk.CTkLabel(self, text='POPULATION INFO', font=titlefont, text_color=TITLE_COLOR)

        pop_name_frame(self, self.pop_name_val)
        lifespan_frame(self, self.lifespan_val)
        init_q_frame(self, self.init_q_val)
        selection_case_frame(self, self.selection_case_val)
        tpc_frame(self)
        body_temp_frame(self)

        backbutton = ctk.CTkButton(self, text='Back',
                                   fg_color=BUTTON_COLOR,
                                   hover_color=B_HOVER_COLOR,
                                   text_color=B_TEXT_COLOR,
                                   font=buttonfont,
                                   command=lambda: controller.show_frame(EnvPage))
        nextbutton = ctk.CTkButton(self, text= 'Next',
                                   fg_color=BUTTON_COLOR,
                                   hover_color=B_HOVER_COLOR,
                                   text_color=B_TEXT_COLOR,
                                   font=buttonfont,
                                   command=lambda: self.next_page())


        # layout
        pop_page_title.grid(row=0, column=0, columnspan=2)
        backbutton.grid(row=4, column=0, sticky='e', padx=5, pady=5)
        nextbutton.grid(row=4, column=1, sticky='w', padx=5, pady=5)


    def get_input_values(self):
        return (self.pop_name_val.get(),self.lifespan_val.get(), self.init_q_val.get(), self.selection_case_val.get(), self.tpc_file_name_val.get(), self.body_temp_dist_val)

    def next_page(self):
        print('next page function runs\n')
        self.controller.show_frame(LoadingPage)
        self.controller.frames[LoadingPage].after(8000, self.some_other_func_name)
        self.controller.frames[ResultsPage].update_info()
            

    def some_other_func_name(self):
        self.controller.show_frame(ResultsPage)
        


# POP PAGE FRAMES
class pop_name_frame(ctk.CTkFrame):
    def __init__(self, parent, pop_name_val):
        super().__init__(master=parent, fg_color=FRAME_COLOR)
        self.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # grid configuration
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # widgets
        pop_name_label = ctk.CTkLabel(self, text='Population Name',
                                      font=mainfont, text_color=TEXT_COLOR)
        pop_name_entry = ctk.CTkEntry(self, textvariable=pop_name_val,
                                      width=200,
                                      font=mainfont, text_color=E_TEXT_COLOR,
                                      fg_color=ENTRY_COLOR, border_color=E_BORDER_COLOR)
        
        # layout
        pop_name_label.grid(row=0, column=0, sticky='w', padx=20, pady=10)
        pop_name_entry.grid(row=0, column=1, sticky='e', padx=10)

class lifespan_frame(ctk.CTkFrame):
    def __init__(self, parent, lifespan_val):
        super().__init__(master=parent, fg_color=FRAME_COLOR)
        self.grid(row=2, column=0, sticky='nsew', padx=10, pady=10)

        # grid configuration
        self.rowconfigure(0, weight=1)
        self.columnconfigure((0,1), weight=1)


        # widgets
        lifespan_label = ctk.CTkLabel(self, text='Lifespan',
                                      font=mainfont, text_color=TEXT_COLOR)
        lifespan_entry = ctk.CTkEntry(self, textvariable=lifespan_val,
                                      font=mainfont, text_color=E_TEXT_COLOR,
                                      fg_color=ENTRY_COLOR, border_color=E_BORDER_COLOR,
                                      width=200)
        
        # layout
        lifespan_label.grid(row=0, column=0, sticky='w', padx=20, pady=10)
        lifespan_entry.grid(row=0, column=1, sticky='e', padx=10)

class init_q_frame(ctk.CTkFrame):
    def __init__(self, parent, init_q_val):
        super().__init__(master=parent, fg_color=FRAME_COLOR)
        self.grid(row=1, column=1, sticky='nsew', padx=10, pady=10)

        # grid configuration
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # widgets
        init_q_label = ctk.CTkLabel(self, text='Initial q Frequency',
                                      font=mainfont, text_color=TEXT_COLOR)
        init_q_entry = ctk.CTkEntry(self, textvariable=init_q_val,
                                      font=mainfont, text_color=E_TEXT_COLOR,
                                      fg_color=ENTRY_COLOR, border_color=E_BORDER_COLOR,
                                      width=200)

        # layout
        init_q_label.grid(row=0, column=0, sticky='w', padx=20, pady=10)
        init_q_entry.grid(row=0, column=1, sticky='e', padx=10)

class selection_case_frame(ctk.CTkFrame):
    def __init__(self, parent, selection_case_val):
        super().__init__(master=parent, fg_color=FRAME_COLOR)
        self.grid(row=2, column=1, sticky='nsew', padx=10, pady=10)

        # grid configuration
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # widgets
        selection_case_label = ctk.CTkLabel(self, text='Selection Case',
                                      font=mainfont, text_color=TEXT_COLOR)
        
        selection_case_list = ['recessiv','dominant','heterozygote_adv']        
        selection_case_combobox = ctk.CTkComboBox(self, variable=selection_case_val, values=selection_case_list,
                                                  bg_color=COMBO_BG_COLOR, fg_color=COMBO_FG_COLOR,
                                                  border_color=COMBO_BORDER_COLOR,
                                                  button_color=COMBO_BUTTON_COLOR,
                                                  button_hover_color=COMBO_BUTTON_H_COLOR,
                                                  dropdown_fg_color=COMBO_DD_FG_COLOR,
                                                  dropdown_hover_color=COMBO_DD_HOVER_COLOR,
                                                  dropdown_text_color=COMBO_DD_TEXT_COLOR,
                                                  text_color=COMBO_TEXT_COLOR,
                                                  font=mainfont,
                                                  width=200)

        # layout
        selection_case_label.grid(row=0, column=0, sticky='w', padx=20, pady=10)
        selection_case_combobox.grid(row=0, column=1, sticky='e', padx=10)    

class tpc_frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=FRAME_COLOR)
        self.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        self.parent = parent

        # font
        self.secondfont = ctk.CTkFont(FONT, size=MAIN_TEXTSIZE-8)
        
        # grid configuration
        self.rowconfigure((0,1,2), weight=2)
        self.columnconfigure(0, weight=1)
        
        # widgets
        tpc_label = ctk.CTkLabel(self, text='Temperature Perfonmance Curve', font=mainfont,
                                 text_color=TEXT_COLOR)
        open_file_button = ctk.CTkButton(self, text='Open File',
                                         fg_color=BUTTON_COLOR,
                                         hover_color=B_HOVER_COLOR,
                                         text_color=B_TEXT_COLOR,
                                         font=buttonfont,
                                         command=lambda: self.select_tpc_file_func())
        filename_label = ctk.CTkLabel(self,text=' ',font=self.secondfont)

        # initializing a matplotlib figure
        figure = plt.figure(figsize=(5,3))
        self.ax = figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(figure, self)
        self.canvas.draw()

        # layout
        tpc_label.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
        open_file_button.grid(row=1, column=0, columnspan=2, sticky='s')
        filename_label.grid(row=2, column=0, columnspan=2)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
        

        
    def select_file(self):
        # opening a file  
        filetypes = (
            ('csv files', '*.csv'),
            ('All files', '*.*')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
        
        return filename 
    
    def plot_tpc(self, ax, canvas):

        ax.clear()
        tpc_file_name = self.parent.tpc_file_name_val.get()
        x_values, y_values = input_functions.import_fitness_graph(tpc_file_name)

        ax.set_title('Temperature Performance Curve', color=PLOT_TEXT_COLOR)
        ax.set_xlabel('Temperature', color=PLOT_TEXT_COLOR2)
        ax.set_ylabel('Fitness', color=PLOT_TEXT_COLOR2)

        ax.plot(x_values, y_values, color=PLOT_COLOR)
        canvas.draw()

    def select_tpc_file_func(self):
        tpc_file_name = self.select_file()
        self.parent.tpc_file_name_val.set(tpc_file_name)

        file_name_label = ctk.CTkLabel(self, text=tpc_file_name,
                                       text_color=TEXT_COLOR,
                                       font=self.secondfont).grid(row=2, column=0, columnspan=2)
        self.plot_tpc(self.ax, self.canvas)

        print(self.parent.tpc_file_name_val.get())
    
class body_temp_frame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent, fg_color=FRAME_COLOR)
        self.grid(row=3, column=1, sticky='nsew', padx=10, pady=10)
        self.parent = parent
        
        # grid configuration
        self.rowconfigure((0,1), weight=1)
        self.rowconfigure(2, weight=3)
        self.columnconfigure(0, weight=3)
        self.columnconfigure((1,2), weight=1)

        # data
        self.a_val_string = ctk.StringVar(value=str(round(self.parent.body_temp_a_val.get(),2)))
        self.scale_val_string = ctk.StringVar(value=str(round(self.parent.body_temp_scale_val.get(),2)))

        # tracing
        parent.body_temp_a_val.trace('w', self.update_dist_vals)
        parent.body_temp_scale_val.trace('w', self.update_dist_vals)

        # widgets
        bodytemp_label = ctk.CTkLabel(self, text='Body Temperature Distribution',
                                      font=mainfont, text_color=TEXT_COLOR)
        a_slider = ctk.CTkSlider(self,
                                from_=-10, to=10, 
                                variable=parent.body_temp_a_val,
                                number_of_steps=20,
                                height=10,
                                progress_color=S_PROGRESS_COLOR,
                                button_color=S_BUTTON_COLOR,
                                button_hover_color=S_HOVER_COLOR,
                                fg_color=S_BORDER_COLOR)
        a_label = ctk.CTkLabel(self, text='a     =', text_color=TEXT_COLOR, font=mainfont)
        aval_label = ctk.CTkLabel(self, text=self.a_val_string,
                               text_color=TEXT_COLOR,
                               textvariable=self.a_val_string,
                               font=mainfont)

        scale_slider = ctk.CTkSlider(self,
                                    from_=1, to=10,
                                    number_of_steps=10,
                                    height=10,
                                    progress_color=S_PROGRESS_COLOR,
                                    button_color=S_BUTTON_COLOR,
                                    button_hover_color=S_HOVER_COLOR,
                                    variable=parent.body_temp_scale_val,
                                    fg_color=S_BORDER_COLOR)
        scale_label = ctk.CTkLabel(self, text='scale =', text_color=TEXT_COLOR, font=mainfont)
        scaleval_label = ctk.CTkLabel(self, text=self.scale_val_string,
                                   text_color=TEXT_COLOR,
                                   textvariable=self.scale_val_string,
                                   font=mainfont)
        

        # initializing a matplotlib figure
        figure = plt.figure(figsize=(5,3))
        self.ax = figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(figure, self)
        self.canvas.draw()

        # layout
        bodytemp_label.grid(row=0, column=0, columnspan=3, sticky='nsew', padx=10, pady=10)
        a_slider.grid(row=1, column=0, sticky='ew', padx=10, pady=5)
        a_label.grid(row=1, column=1, sticky='e', padx=5, pady=5)
        aval_label.grid(row=1, column=2, sticky='w', padx=10, pady=5)
        scale_slider.grid(row=2, column=0, sticky='ew', padx=10, pady=5)
        scale_label.grid(row=2, column=1, sticky='e', padx=5, pady=5)
        scaleval_label.grid(row=2, column=2, sticky='w', padx=10, pady=5)
        # selectbutton.grid(row=0, column=1, rowspan=2)
        self.canvas.get_tk_widget().grid(row=3, column=0, columnspan=3, sticky='nsew', padx=10, pady=10)
    

    def update_dist_vals(self, *args):
        a_val = round(self.parent.body_temp_a_val.get(),2)
        scale_val = round(self.parent.body_temp_scale_val.get(),2)
        self.a_val_string.set(str(a_val))
        self.scale_val_string.set(str(scale_val))
        self.plot_dist(self.ax, self.canvas)

    def plot_dist(self, ax, canvas):
        ax.clear()

        a = self.parent.body_temp_a_val.get()
        scale = self.parent.body_temp_scale_val.get()
        mean = 25

        x_values = [i for i in range(10, 40)]
        y_values= [math_functions.skew_norm_dist(x= i, a= a, loc= mean, scale= scale) for i in range(10, 40)]

        ax.set_title('Body Temperature Distribution', color=PLOT_TEXT_COLOR)
        ax.set_xlabel('Temperature', color=PLOT_TEXT_COLOR2)
        ax.set_ylabel('Frequency', color=PLOT_TEXT_COLOR2)

        ax.plot(x_values, y_values, color=PLOT_COLOR)
        canvas.draw()



# RESULTS PAGE
class ResultsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BACKGROUND_COLOR)
        self.app = controller

        # grid configuration
        self.rowconfigure((0,1,2), weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure((1,2), weight=3)

        # getting the values submitted in the firt two pages
        self.env_inputs = controller.frames[EnvPage].get_input_values()
        self.pop_inputs = controller.frames[PopPage].get_input_values()

        # unpacking the values 
        self.init_temp, self.temp_inc_func, self.temp_inc_rate, self.time = self.env_inputs
        self.pop_name, self.lifespan, self.init_q, self.selection_case, self.tpc_file_name, self.body_temp_dist = self.pop_inputs


        # creating an environment and a population based on the inputs from frames
        self.env = Environment.Environment(self.init_temp, self.temp_inc_func, self.temp_inc_rate)
        self.pop = Population.Population(self.pop_name, self.lifespan, self.env, self.selection_case,
                                         self.init_q, self.tpc_file_name, self.body_temp_dist)
        self.plot = plotting_gui.plot(self.pop, time=self.time)
        
        # defining ctk Variables
        self.init_temp_var = ctk.StringVar()
        self.temp_inc_func_var = ctk.StringVar()
        self.temp_inc_rate_var = ctk.DoubleVar()
        self.time_var = ctk.IntVar()

        self.pop_name_var = ctk.StringVar()
        self.lifespan_var = ctk.DoubleVar()
        self.init_q_var = ctk.DoubleVar()
        self.body_temp_a_var = ctk.DoubleVar()
        self.body_temp_scale_var = ctk.DoubleVar()
        self.body_temp_dist_var = (self.body_temp_a_var.get(), self.body_temp_scale_var.get())


        # widgets
        title = ctk.CTkLabel(self, text='THE RESULT PAGE', font=titlefont, text_color=TITLE_COLOR)
        self.infopanel = InfoPanel_frame(self)
        self.displayframe = Display_frame(self)
        backbutton = ctk.CTkButton(self, text= 'Back', command=lambda:self.back_button(), font=buttonfont,
                                   fg_color=BUTTON_COLOR, hover_color=B_HOVER_COLOR, text_color=B_TEXT_COLOR)


        # layout
        title.grid(row=0, column=0, columnspan=3)
        backbutton.grid(row=2, column=0, padx=10)


    def back_button(self):
        self.app.show_frame(PopPage)
        self.displayframe.w_vals_frame.w_vals_canvas.clear()
        self.displayframe.allel_freq_frame.allel_freq_canvas.clear()
        

    def update_info(self):
        # data
        self.env_inputs = self.app.frames[EnvPage].get_input_values()
        self.pop_inputs = self.app.frames[PopPage].get_input_values()
        print('env inputs:', self.env_inputs,'\npop inputs:', self.pop_inputs)


        # unpacking the inputs
        self.init_temp, self.temp_inc_func, self.temp_inc_rate, self.time = self.env_inputs
        self.pop_name, self.lifespan, self.init_q, self.selection_case, self.tpc_file_name, self.body_temp_dist = self.pop_inputs
        self.selection_case = 'recessiv'

        # creating an environment and a population based on the inputs from frames
        self.env = Environment.Environment(self.init_temp, self.temp_inc_func, self.temp_inc_rate)
        self.pop = Population.Population(self.pop_name, self.lifespan, self.env, self.selection_case,
                                         self.init_q, self.tpc_file_name, self.body_temp_dist, new_pop=True)
        self.plot = plotting_gui.plot(self.pop, time=self.time)

        # setting the ctk variables
        self.init_temp_var.set(self.env.init_temp)
        self.temp_inc_func_var.set(self.env.temp_inc_func)
        self.temp_inc_rate_var.set(self.env.temp_inc_rate)
        self.time_var.set(self.time)

        self.pop_name_var.set(self.pop.name)
        self.lifespan_var.set(self.pop.lifespan)
        self.init_q_var.set(self.pop.init_q)
        self.body_temp_a_var.set(self.pop.body_temp_a)
        self.body_temp_scale_var.set(self.pop.body_temp_scale)
        self.body_temp_dist_var = self.pop.body_temp_dist

        self.infopanel.pop_attributes_frame.update_pop_attributes()
        self.displayframe.draw_display_graphs()


# RESULTS PAGE FRAMES
class InfoPanel_frame(ctk.CTkFrame):
    def __init__(self, resultspage_frame):
        super().__init__(resultspage_frame, fg_color=FRAME_COLOR)
        self.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1), weight=1)
        self.parent = resultspage_frame

        self.env_att = env_attributes_frames(self)
        self.pop_attributes_frame = pop_attributes_frame(self)
   

class env_attributes_frames(ctk.CTkFrame):
    def __init__(self, info_panel_frame):
        super().__init__(info_panel_frame, fg_color=FRAME_COLOR)
        self.resultspage = info_panel_frame.parent
        self.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        # grid configuration
        self.rowconfigure(0, weight=2)
        self.rowconfigure((1,2,3), weight=1)
        self.columnconfigure((0,1), weight=1)
                
        titlelabel = ctk.CTkLabel(self, text='ENVIRONMENT',
                                text_color=TITLE_COLOR, font=subtitlefont)
                
        # environment attribute labels 
        init_temp_label0 = ctk.CTkLabel(self, text='Initial Temperature:',
                                       text_color=TEXT_COLOR, font=mainfont)
        init_temp_label1 = ctk.CTkLabel(self, textvariable=self.resultspage.init_temp_var,
                                       text_color=TEXT_COLOR, font=boldfont)
        
        temp_inc_func_label0 = ctk.CTkLabel(self, text='Temperature Increase Function:',
                                           text_color=TEXT_COLOR, font=mainfont) 
        temp_inc_func_label1 = ctk.CTkLabel(self, textvariable=self.resultspage.temp_inc_func_var,
                                           text_color=TEXT_COLOR, font=boldfont) 
        
        temp_inc_rate_label0 = ctk.CTkLabel(self, text='Temperature Increase Rate:',
                                           text_color=TEXT_COLOR, font=mainfont)
        temp_inc_rate_label1 = ctk.CTkLabel(self, textvariable=self.resultspage.temp_inc_rate_var,
                                           text_color=TEXT_COLOR, font=boldfont)
        
        # layout
        titlelabel.grid(row=0, column=0, columnspan=2)
        init_temp_label0.grid(row=1, column=0, sticky='w', padx=10)
        init_temp_label1.grid(row=1, column=1, sticky='e', padx=10)
        temp_inc_func_label0.grid(row=2, column=0, sticky='w', padx=10)
        temp_inc_func_label1.grid(row=2, column=1, sticky='e', padx=10)
        temp_inc_rate_label0.grid(row=3, column=0, sticky='w', padx=10)
        temp_inc_rate_label1.grid(row=3, column=1, sticky='e', padx=10)

class pop_attributes_frame(ctk.CTkFrame):
    def __init__(self, info_panel_frame):
        super().__init__(info_panel_frame, fg_color=FRAME_COLOR)
        # direct access to the result page
        self.resultspage = info_panel_frame.parent
        self.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')


        # grid configuration 
        self.columnconfigure((0,1), weight=1)
        self.rowconfigure((1,2,3,4), weight=2)


        # title
        titlelabel = ctk.CTkLabel(self, text='POPULATION',
                    text_color=TITLE_COLOR, font=subtitlefont)
                
        # population attributes
        pop_name_label0 = ctk.CTkLabel(self, text='Population Name:',
                                       text_color=TEXT_COLOR, font=mainfont)
        pop_name_label1 = ctk.CTkLabel(self, textvariable=self.resultspage.pop_name_var,
                                       text_color=TEXT_COLOR, font=boldfont)
        
        lifespan_label0 = ctk.CTkLabel(self, text='Lifespan:',
                                           text_color=TEXT_COLOR, font=mainfont) 
        lifespan_label1 = ctk.CTkLabel(self, textvariable=self.resultspage.lifespan_var,
                                           text_color=TEXT_COLOR, font=boldfont) 
        
        init_q_label0 = ctk.CTkLabel(self, text='Initial q:',
                                           text_color=TEXT_COLOR, font=mainfont)
        init_q_label1 = ctk.CTkLabel(self, textvariable=self.resultspage.init_q_var,
                                           text_color=TEXT_COLOR, font=boldfont)
        
        self.plot = plotting_gui.plot(info_panel_frame.parent.pop)

        self.tpc_fig = plt.figure(figsize=(2,2),facecolor=FRAME_COLOR)  
        self.tpc_ax = self.tpc_fig.add_subplot()    
        self.tpc_canvas = FigureCanvasTkAgg(self.tpc_fig, self)
        self.tpc_canvas.draw()


        self.dist_fig = plt.figure(figsize=(2,2), facecolor=FRAME_COLOR)  
        self.dist_ax = self.dist_fig.add_subplot() 
        self.dist_canvas = FigureCanvasTkAgg(self.dist_fig, self)
        self.dist_canvas.draw()     
        
        
        # layout
        titlelabel.grid(row=0, column=0, columnspan=2)
        pop_name_label0.grid(row=1, column=0, sticky='w', padx=10)
        pop_name_label1.grid(row=1, column=1, sticky='e', padx=10)
        lifespan_label0.grid(row=2, column=0, sticky='w', padx=10)
        lifespan_label1.grid(row=2, column=1, sticky='e', padx=10)
        init_q_label0.grid(row=3, column=0, sticky='w', padx=10)
        init_q_label1.grid(row=3, column=1, sticky='e', padx=10)
        self.tpc_canvas.get_tk_widget().grid(row=4, column=0, sticky='nsew', padx=10, pady=10)
        self.dist_canvas.get_tk_widget().grid(row=4, column=1, sticky='nsew', padx=10, pady=10)

    def update_pop_attributes(self):
        print('update_pop_attributes is running')

        # drawing the tpc graph
        self.tpc_ax.clear()

        the_plot = self.resultspage.plot
        x_tpc, y_tpc = the_plot.tpc()

        self.tpc_ax.plot(x_tpc, y_tpc, color=PLOT_COLOR)
        self.tpc_ax.set_title('Temperature Performance Curve', color=PLOT_TEXT_COLOR)
        self.tpc_ax.set_xlabel('Temperature', color=PLOT_TEXT_COLOR2)
        self.tpc_ax.set_ylabel('Fitness', color=PLOT_TEXT_COLOR2)
        self.tpc_canvas.draw()


        # drawing the distribution graph
        self.dist_ax.clear()
        x_dist, y_dist = the_plot.dist()

        self.dist_ax.plot(x_dist,y_dist, color=PLOT_COLOR)
        self.dist_ax.set_title('Body Temperature Distribution', color=PLOT_TEXT_COLOR)
        self.dist_ax.set_xlabel('Temperature', color=PLOT_TEXT_COLOR2)
        self.dist_ax.set_ylabel('Frequency', color=PLOT_TEXT_COLOR2) 
        self.dist_canvas.draw()     

class Display_frame(ctk.CTkFrame):
    def __init__(self, resultspage_frame):
        super().__init__(resultspage_frame, fg_color=FRAME_COLOR)
        self.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')
        self.resultspage = resultspage_frame
        self.plot = self.resultspage.plot

        # grid configuration
        self.columnconfigure(0, weight=1)
        self.rowconfigure((0,1), weight=1)

        # subframes
        self.w_vals_frame = wvals_frame(self)
        self.allel_freq_frame = allelfreq_frame(self)
        
        self.windowNum = 0

        self.framelist = []
        self.framelist.append(self.w_vals_frame)
        self.framelist.append(self.allel_freq_frame)
        self.framelist[1].forget()

        switch = ctk.CTkButton(self, text = "Switch", command=self.switchWindows,
                            fg_color=BUTTON_COLOR, hover_color=B_HOVER_COLOR, text_color=B_TEXT_COLOR,
                            font=mainfont)
        switch.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
    

    def draw_display_graphs(self):
        print('draw_display_graphs is running ...')
        frame1 = self.allel_freq_frame
        frame2 = self.w_vals_frame

        # allel frequencies graph
        allel_freq_ax = frame1.allel_freq_figure.add_subplot()
        # y_allelf0 -> p frequency
        # y_allelf1 -> q frequency
        x_allelf, y_allelf0, y_allelf1 = self.resultspage.plot.allel_freq()
        # print('x_allelf:',x_allelf,'\ny_allelf:',y_allelf0)
 
        allel_freq_ax.set_title('Allele Frequencies During the Selection', color=PLOT_TEXT_COLOR)
        allel_freq_ax.set_xlabel('Generation', color=PLOT_TEXT_COLOR2)
        allel_freq_ax.set_ylabel('Allele Frequencies', color=PLOT_TEXT_COLOR2) 
        p_freq_line, = allel_freq_ax.plot(x_allelf, y_allelf0, color=PLOT_COLOR)
        q_freq_line, = allel_freq_ax.plot(x_allelf, y_allelf1, color=PLOT_COLOR2)
        allel_freq_ax.legend([p_freq_line, q_freq_line], ['p-frequency', 'q-frequency'])
        frame1.allel_freq_canvas.draw()

        # w vals graph
        frame2.w_vals_ax = frame2.w_vals_figure.add_subplot()
        x_wval, y_wval = self.resultspage.plot.W_vals()
        # print('\nx_wval:',x_wval,'\ny_wval:',y_wval)

        frame2.w_vals_ax.plot(x_wval, y_wval, color=PLOT_COLOR)
        frame2.w_vals_ax.set_title('Total Fitness During the Selection', color=PLOT_TEXT_COLOR)
        frame2.w_vals_ax.set_xlabel('Generation', color=PLOT_TEXT_COLOR2)
        frame2.w_vals_ax.set_ylabel('Total Fitness', color=PLOT_TEXT_COLOR2) 
        frame2.w_vals_canvas.draw()

    def switchWindows(self):
        self.framelist[self.windowNum].forget()
        self.windowNum = (self.windowNum + 1) % len(self.framelist)
        self.framelist[self.windowNum].tkraise()
        self.framelist[self.windowNum].grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

class allelfreq_frame(ctk.CTkFrame):
    def __init__(self, display_frame):
        super().__init__(display_frame, fg_color=FRAME_COLOR)
        self.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.columnconfigure(0, weight=1)

        allelfreq_label = ctk.CTkLabel(self, text='Allele Frequencies Frame',
                             font=mainfont,
                             text_color=TEXT_COLOR)
        allelfreq_label.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        self.allel_freq_figure = plt.figure()
        self.allel_freq_canvas = FigureCanvasTkAgg(self.allel_freq_figure, self)
        self.allel_freq_canvas.get_tk_widget().grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

class wvals_frame(ctk.CTkFrame):
    def __init__(self, display_frame):
        super().__init__(display_frame, fg_color=FRAME_COLOR)
        self.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.columnconfigure(0, weight=1)
        
        w_vals_label = ctk.CTkLabel(self, text='Fitness Values Frame',
                             font=mainfont,
                             text_color=TEXT_COLOR)
        w_vals_label.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        
        self.w_vals_figure = plt.figure()
        self.w_vals_canvas = FigureCanvasTkAgg(self.w_vals_figure, self)
        self.w_vals_canvas.get_tk_widget().grid(row=1, column=0, sticky='nsew', padx=10, pady=10)



app = Modellapp()
app.mainloop()     
        