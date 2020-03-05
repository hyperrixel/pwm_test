# Command line test tool for BTS7960 pwm connected via RPi GPIO

What is this

This ` python ` srcipt is a small test tool to explore how BTS7960 or similar PWM controler works if connected with Raspberry Pi via GPIO ports.

The goal of this project is to play with the PWM as simply as possible using just a terminal. You can use it just to test with an engine but you can use it with oscilloscope as well to discover how duty-cycles in real life work. It's only up to you.

## Installation

1. Download or clone this repository.

2. Get ` python3-rpi.gpio ` if you don't already have it.

3. Wire your PWM controler according to its documentation. You can use ` BTS7960_PIN_L_EN `, ` BTS7960_PIN_LPWM `, ` BTS7960_PIN_R_EN ` and ` BTS7960_PIN_RPWM ` constants as the pins enable 1st direction, control 1st direction, enable 2nd direction and control 2nd direction respectively. Note we're using direction LEFT and RIGHT since we're controling a small vehicle but clokwise, negative-clockwise or any other direction names could be also used.

## Usage

Just run the script without any command-line argument and use commands to drive your PWM controler.

Please ceep in mind this is a test tool only. Command input processing doesn't have input error checks.

### List of commands and their meaning

- ` b ` Speeds up the PWM in steps 25-50-75-100 percentage in the 1st direction.

- ` c ` Cleans up PWM signal pins.

- ` e ` Exists the script.

- ` f ` Speeds up the PWM in steps 25-50-75-100 percentage in the 1st direction.

- ` i ` Initializes controler instance again.

- ` n ` Sets the PWM to neutral.

- ` r ` More precisely: ` r <direction> <speed-in-percentage> `. Sets PWM to the selected direction (` b ` or ` f `) and speed in percentage. You can use this function to stop PWM too.

- ` u ` More precisely: ` u <direction> <top-speed-in-percentage> ` Speeds up PWM in the selected direction (` b ` or ` f `) to the top speed in percentage. Step of speed change is 1 percentage, each step is 0.1 seconds long.

## Fine tuning

You can set some variables to personalyse the control flow oy the PWM test.

- ` FREQUENCY ` Frequency in Hz for both controller directions. One side of setting the frequency are the customization needs of your script and the other side is the frequency of the PWM controler. It's a good practice to use an oscilloscope if you want to really fine tune this value.

- ` GPIO_PINS ` List of GPIO pins in board style. This constant is used only by ` setuppins() ` function. Both the constant and function are rarely used in real world if you don't understand the reason of it it's definitely a good practice if you don't use them at all.

- ` SLEEP ` Duration of accelerating or deccelerating stages in seconds. This constant is used by commands ` b ` and ` f `.

- ` GPIO_STYLE ` The style of identifying the pins. We're using GPIO.BOARD but any other style is just fine. If you change this value keep in mind to change the pin Ids too.

- ` BTS7960_PIN_L_EN ` 1st direction enable/disable sender pin.

- ` BTS7960_PIN_LPWM ` 1st direction frequency sender pin.

- ` BTS7960_PIN_R_EN ` 2nd direction enable/disable sender pin.

- ` BTS7960_PIN_RPWM ` 2nd direction frequency sender pin.

## More fine tuning

Before you change anything else aside of things listed above please consider to read all the comments in the script carefully.
