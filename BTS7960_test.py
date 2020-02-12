#!/usr/bin/python3
"""
        _                 _
       (_)               | |
 _ __   _  __  __   ___  | |
| '__| | | \ \/ /  / _ \ | |
| |    | |  >  <  |  __/ | |
|_|    |_| /_/\_\  \___| |_|


BTS7960_test
============

The goal of this script is to test GPIO and BTS7960 connection from command line
with simple one-letter commands.

Copyright rixel 2020
Distributed under the Boost Software License, Version 1.0.
See accompanying file LICENSE or a copy at https://www.boost.org/LICENSE_1_0.txt
"""



# To use GPIO features with Python on your Raspberry Pi you have to install
# python3-rpi.gpio
import RPi.GPIO as GPIO

from time import sleep



# Use this value to set frequency in Hz for both controller directions.
FREQUENCY = 2500

# List of usable GPIO pins. Use this list to avoid freezing the code.
# If you want to know more about GPIO pins, check this link out:
# https://pinout.xyz
GPIO_PINS = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29,
             31, 32, 33, 35, 36, 37, 38, 40]

# Interval between accelerating/decelerating steps of motor tests. If you're
# able to measure the frequency of output current changes you can identify the
# steps by the interval and you can use smaller value. If you measure with your
# ears higher value is recommended.
SLEEP = 0.5

# Use these constants to change port according to your viring setup.
# Keep in mind, the numbering of the GPIO pins in this script follows the BOARD
# style. if you want to change the numbering style modify GPIO_STYLE.
GPIO_STYLE = GPIO.BOARD

BTS7960_PIN_L_EN = 22
BTS7960_PIN_LPWM = 24
BTS7960_PIN_R_EN = 21
BTS7960_PIN_RPWM = 23



class Driver(object):
    """
    Handles the H-Bridge
    """

    def __init__(self):
        """
        Intializes the class
        """
        global BTS7960_PIN_L_EN
        global BTS7960_PIN_LPWM
        global BTS7960_PIN_R_EN
        global BTS7960_PIN_RPWM

        self.R_EN = BTS7960_PIN_R_EN
        self.L_EN = BTS7960_PIN_L_EN
        self.RPWM = BTS7960_PIN_RPWM
        self.LPWM = BTS7960_PIN_LPWM
        self.setup()



    def cleanup(self):
        """
        Cleans signlas from each GPIO pin
        """

        GPIO.cleanup()



    def left(self):
        """
        Sets the direction to LEFT
        """

        GPIO.output(self.RPWM, False)  # Stop turning right
        GPIO.output(self.LPWM, True)  # start turning left



    def neutral(self):
        """
        Sets the direction to NEUTRAL
        """

        GPIO.output(self.RPWM, False)  # Stop turning right
        GPIO.output(self.LPWM, False)  # stop turning left



    def right(self):
        """
        Sets the direction to RIGHT
        """

        GPIO.output(self.LPWM, False)  # stop turning left
        GPIO.output(self.RPWM, True)  # start turning right



    def setup(self):
        """
        Sets up used GPIO ports
        """

        global GPIO_STYLE

        GPIO.setmode(GPIO_STYLE)
        GPIO.setup(self.R_EN, GPIO.OUT)
        GPIO.setup(self.RPWM, GPIO.OUT)
        GPIO.setup(self.L_EN, GPIO.OUT)
        GPIO.setup(self.LPWM, GPIO.OUT)
        GPIO.output(self.R_EN, True)
        GPIO.output(self.L_EN, True)



def main():
    """
    Handles the main loop
    ---------------------
    """

    global FREQUENCY
    global SLEEP

    driver = Driver()
    lsc = GPIO.PWM(driver.LPWM, FREQUENCY)
    rsc = GPIO.PWM(driver.RPWM, FREQUENCY)
    printhelp()
    noExit = True
    while noExit:
        userinput = input('?>').lower().split(' ')
        if userinput[0] == 'b':
            print('--> Backward.')
            rsc.stop()
            lsc.start(10)
            sleep(SLEEP)
            for i in [25, 50, 75, 100]:
                lsc.ChangeDutyCycle(i)
                sleep(SLEEP)
            # driver.left()
        elif userinput[0] == 'c':
            print('--_ Cleaning up.')
            driver.cleanup()
        elif userinput[0] == 'e':
            print('Bye.')
            lsc.stop()
            rsc.stop()
            driver.cleanup()
            noExit = False
        elif userinput[0] == 'f':
            print('--> Forward.')
            lsc.stop()
            rsc.start(10)
            sleep(SLEEP)
            for i in [25, 50, 75, 100]:
                rsc.ChangeDutyCycle(i)
                sleep(SLEEP)
            # driver.left()
            # driver.right()
        elif userinput[0] == 'i':
            print('[|] (Re)-Init.')
            driver.setup()
        elif userinput[0] == 'n':
            print('--- Neutral.')
            lsc.stop()
            rsc.stop()
            # driver.neutral()
        elif userinput[0] == 'r':
            if userinput[1] == 'b':
                print('>>> Runs BACKWARD with {}% speed.'.format(userinput[2]))
                rsc.stop()
                lsc.start(int(userinput[2]))
            elif userinput[1] == 'f':
                print('>>> Runs FORWARD with {}% speed.'.format(userinput[2]))
                lsc.stop()
                rsc.start(int(userinput[2]))
        elif userinput[0] == 'u':
            if userinput[1] == 'b':
                print('>-> Speeds up BACKWARD with {}% speed.'.format(userinput[2]))
                rsc.stop()
                lsc.start(0)
                for i in range(int(userinput[2])):
                    lsc.ChangeDutyCycle(i)
                    sleep(0.1)
                print('    Fullspeed!')
            elif userinput[1] == 'f':
                print('>-> Speeds up FORWARD with {}% speed.'.format(userinput[2]))
                lsc.stop()
                rsc.start(0)
                for i in range(int(userinput[2])):
                    rsc.ChangeDutyCycle(i)
                    sleep(0.1)
                print('    Fullspeed!')



def pinlist(pins=None):
    """
    Prints the function of GPIO pins in human readable format
    ---------------------------------------------------------
    @Params: pins   (list, iterable)    [optional] List of pins to list. If
                                        omitted, all available pins are listed.
    """

    global GPIO_PINS

    if pins==None:
        pins = GPIO_PINS[:]
    elif not isinstance(pins, list):
        pins = list(pins)
    for pin in pins:
        if GPIO.gpio_function(pin) == GPIO.IN:
            print('Channel #{:2d} is: INPUT'.format(pin))
        elif GPIO.gpio_function(pin) == GPIO.OUT:
            print('Channel #{:2d} is: OUTPUT'.format(pin))
        elif GPIO.gpio_function(pin) == GPIO.SPI:
            print('Channel #{:2d} is: SPI'.format(pin))
        elif GPIO.gpio_function(pin) == GPIO.I2C:
            print('Channel #{:2d} is: I2C'.format(pin))
        elif GPIO.gpio_function(pin) == GPIO.HARD_PWM:
            print('Channel #{:2d} is: PWM'.format(pin))
        elif GPIO.gpio_function(pin) == GPIO.SERIAL:
            print('Channel #{:2d} is: SERIAL'.format(pin))
        elif GPIO.gpio_function(pin) == GPIO.UNKNOWN:
            print('Channel #{:2d} is: UNKNOWN'.format(pin))



def printhelp():
    """
    Print keyboard help screen
    --------------------------
    """

    print('H-Bridge test')
    print('=============')
    print('[b]  Backward (left)')
    print('[c]  Cleanup')
    print('[e]  Exit')
    print('[f]  Forward (right)')
    print('[i]  (Re)-Init.')
    print('[n]  Neutral')
    print('[r] [d] [s]  Runs in "d" direction to "s" speed.')
    print('[u] [d] [s]  Speeds up in "d" direction to "s" speed.')



def setuppins(mode=GPIO.IN):
    """
    Sets each available GPIO pin to the specified mode
    --------------------------------------------------
    @Params: mode (int) [optional] Mode to change to. If omitted, it set each
                        available port to GPO.IN.
    """

    global GPIO_PINS

    for pin in GPIO_PINS:
        try:
            print('Setting #{:2d}'.format(pin), end='')
            GPIO.setup(pin, mode)
            print('\t[Ok.]')
        except Exception as e:
            print('\t[FAILERD.]')
            print(e)



if __name__ == '__main__':
    main()
else:
    print('This is a script, not a module.')
