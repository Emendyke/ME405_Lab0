"""! @file main.py
Doxygen style docstring for the file 
"""

''' 
   \brief     ME 405 Week 1 Lab 0
   \details   This program records the steps to increase the voltage in a pin from 0V to 3.3V
   \author    Emily Mendyke
   \version   1.0
   \date      1/17/2024
'''

from cqueue import IntQueue, FloatQueue
import task_share
import micropython
from pyb import Timer, Pin, ADC
import time 
micropython.alloc_emergency_exception_buf(100)

pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP) # output in 
pinB0 = pyb.Pin(pyb.Pin.board.PB0, pyb.Pin.IN) # input pin
adc = pyb.ADC(pinB0)  # analog to digital conversion


runtime = 5 # runtime for 5 seconds
freq = 1000

int_queue = IntQueue(runtime*freq)  #creating queue for time
float_queue = FloatQueue(runtime*freq)  #creating queue for voltage


def timer_int(tim_num):
    
    val = adc.read()
    
#     if int_queue.full(): # checks if queue is full
#         tim.callback(None)    # disables callback
#         return

    float_queue.put(val)

# runs when requested by user or through gui
def step_response(t_channel, frequency, runtime):
    
    tim = pyb.Timer(t_channel, freq = frequency)   # initialize timer object
    tim.callback(timer_int) # timer callback
    
    pinC0.high() 
    
    try:
        
        while not float_queue.full():
            pass
        
        tim.callback(None)
            
        for i in range(frequency*runtime):
            int_queue.put(int(1/frequency*1000*i)) # the time in ms is going to 
        
        
        while float_queue.any():    # while there is anything in the voltage queue
            
            time = int_queue.get()
            voltage = float_queue.get()/4096*3.3  #conversion for readable voltage value
            print(f"{time}, {voltage}")
            
        raise KeyboardInterrupt
        
    except KeyboardInterrupt:
        pinC0.low()
        pass
    
    print('Program ended')

if __name__ == "__main__":
      step_response(1, freq, runtime)