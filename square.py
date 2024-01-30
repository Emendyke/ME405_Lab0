# ME 405 Lab 1 Week 1

#Part 2: Write a script in main.py which sets pin C0 as an output
#        then runs a loop in which C0 is at logic 0 for 5 seconds
#        then logic 1 for 5 seconds, and repeats until Ctrl-C is pressed.
#        Save your script as square.py.

import pyb
import time

# Configuring and controlling a digital output pin. Turning it on and off.
pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP)      # Sets the pin PC0 to output, and push pull and creates an object pinC0 to call it by.
while True:
    pinC0.value(1)                                          # Turns the pin on
    time.sleep(5)                                           #Pause for 5 seconds
    pinC0.value(0)                                          # Turns the pin off
    time.sleep(5)                                           #Pause for 5 seconds