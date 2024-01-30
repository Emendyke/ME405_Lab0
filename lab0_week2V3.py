"""! @lab0_week2V2.py.py
Doxygen style docstring for the file 
"""

''' 
   \brief     ME 405 Week 2 Lab 0
   \details   This program visually plots the ADC output data in volts from the MCU over the serial port.
   \author    Jenna Mast (this file), Emily Mendyke (onboard main.py (step_response.py)), and Spluttflob (this file)
   \version   3.0
   \date      1/26/2024
   \Todo      Add the theoretical curve on the same plot for comparison
'''

# """!
# @file lab0example.py
# Run real or simulated dynamic response tests and plot the results. This program
# demonstrates a way to make a simple GUI with a plot in it. It uses Tkinter, an
# old-fashioned and ugly but useful GUI library which is included in Python by
# default.
# This file is based loosely on an example found at
# https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html
# @author Spluttflob
# @date 2023-12-24 Original program, based on example from above listed source
# @copyright (c) 2023 by Spluttflob and released under the GNU Public Licenes V3
# """
import math
import time
import tkinter
import serial
import numpy as np                       #For volt_theo calculation
from random import random
from serial import Serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
def plot_example(plot_axes, plot_canvas, xlabel, ylabel):
    
    """!
    Make an example plot to show a simple(ish) way to embed a plot into a GUI.
    The data is just a nonsense simulation of a diving board from which a
    typically energetic otter has just jumped.
    @param plot_axes The plot axes supplied by Matplotlib
    @param plot_canvas The plot canvas, also supplied by Matplotlib
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    """

    
    # Begin code to obtain the data from the serial port
    
    times = []                                        # For the time data
    volt = []                                         # For the ADC output in volts data

    # Check which com port we're on
    import serial.tools.list_ports as port_list           
    
    ports = list(port_list.comports())
    for p in ports:
        print(p)

    # Set the com port and baud rate.
    ser = serial.Serial('COM5', 115200)


    # Check connection
    if ser.isOpen():
        print("Connected to serial port")
    else:
        print("Failed to connect to serial port")
        exit()

    # Send commands
    try:
        if ser.isOpen():
            print("Connected to serial port")
        else:
            print("Failed to connect to serial port")
            exit()


        # Send CNTRL+C to MCU to stop any program running
        ser.write(b'\x03')
        print("CTRL+C sent to MCU")
        time.sleep(1) 

        # Read and display any response from MCU
        while True:
            data = ser.readline().decode('utf-8').strip()
            if not data:
                break
            print(f"Received from MCU after CTRL+C: {data}")

        # Send CTRL+D to the MCU to start any program on it.
        ser.write(b'\x04')
        print("CTRL+D sent to MCU")
        time.sleep(2)                                         # Optional delay for MCU response

        # Acquire and print data
        
        while True:
            data = ser.readline().decode('utf-8').strip()    # Get the data stream from the serial port and format it. 
            line = data                                      # !!! I think not necessary but will leave for now.
            if not data:                                     # If data list is empty...
                continue                                     # Loop back around to get more data
            if data == 'Program ended':                      # If we're at the end of the ADC output data
                print("Data ended")                           
                break                                          # Break out of the while loop
            print(f"{data}")                                 # Otherwise, print the data list to the serial port.
            values = line.split(',')                           # And split the data string at the commas and place into the values list.
            
            if len(values) != 2:  # Check if values has at least two elements
                continue          # If not, skip to the next while iteration
            
            try:
                times_val = float(values[0])                 # Try to place time component into times_val
                volt_val = float(values[1])                  # Try to place voltage component into the volt_val 
                
                # Check if time_val list is not empty and the number of digits in the new entry is less than the previous entry
                # This filters out entries with dropped digits 
                if times and len(str(abs(int(times_val)))) < len(str(abs(int(times[-1])))):
                    continue
                
                # Put the entries into the lists
                times.append(times_val)
                volt.append(volt_val)
                    
            except ValueError:
                print("Invalid data format in line:", line)
         
              
              
    except serial.SerialException as e:
        print("Error sending/receiving data:", e)
        

    finally:
        
        # Close the serial connection
        ser.close()
        print("Serial connection closed")
    
    # Theoretical curve
    
    V_max = 3.3 # Volts
    R = 100000  # Ohms
    C = 0.0033  # mF since we are using ms
    
  #  import numpy as np
    volts_theo = V_max * (1 - np.exp(-np.array(times) / (R * C)))
    
    # Draw the plot. Of course, the axes must be labeled. A grid is optional
    #plot_axes.plot(times, volt)
    plot_axes.plot(times, volt, label="Experimental ADC Output Data")
    plot_axes.plot(times, volts_theo, color = 'red', label="Theoretical ADC Input Values")
    
    plot_axes.set_xlabel(xlabel)
    plot_axes.set_ylabel(ylabel)
    
    plot_axes.legend()
    plot_axes.grid(True)
    plot_canvas.draw()
    
def tk_matplot(plot_function, xlabel, ylabel, title):
    # """!
    # Create a TK window with one embedded Matplotlib plot.
    # This function makes the window, displays it, and runs the user interface
    # until the user closes the window. The plot function, which must have been
    # supplied by the user, should draw the plot on the supplied plot axes and
    # call the draw() function belonging to the plot canvas to show the plot.
    # @param plot_function The function which, when run, creates a plot
    # @param xlabel The label for the plot's horizontal axis
    # @param ylabel The label for the plot's vertical axis
    # @param title A title for the plot; it shows up in window title bar
    # """
   
   # Create the main program window and give it a title
    
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)
    
    
    # Create a Matplotlib
   
    fig = Figure()
    axes = fig.add_subplot()
   
   
    # Create the drawing canvas and a handy plot navigation toolbar
    
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()
 
 
    # Create the buttons that run tests, clear the screen, and exit the program
    
    button_quit = tkinter.Button(master=tk_root,
    text="Quit",
    command=tk_root.destroy)
    
    button_clear = tkinter.Button(master=tk_root,
    text="Clear",
    command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
    text="Run Test",
    command=lambda: plot_function(axes, canvas,
    xlabel, ylabel))
    
    
    # Arrange things in a grid because "pack" is weird
    
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=2)
    
    
# This function runs the program until the user decides to quit
    tkinter.mainloop()
    
# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program
if __name__ == "__main__":
    tk_matplot(plot_example,
    xlabel="Time (ms)",
    ylabel="Volt (V)",
    title="Experimental ADC Output Voltage Compared to Theoretical ADC Input Voltage vs. Time")
