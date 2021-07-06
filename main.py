"""Uses a Rotaty encoder to control an LED ring within a selenite crystal - Designed to be run from a Trinket M0"""

import rotaryio
import board
import neopixel
from time import sleep
from digitalio import DigitalInOut, Direction, Pull
import adafruit_fancyled.adafruit_fancyled as fancy
import random

#Initialize Leds

number_of_leds = 12
led_pin = board.D2
np = neopixel.NeoPixel(led_pin, number_of_leds, auto_write = False, brightness = 1)


#Initialize Rotary encoder

rotary_pin_1 = board.D3
rotary_pin_2 = board.D4
button_pin = board.D0
last_pos = None

dial = rotaryio.IncrementalEncoder(rotary_pin_1, rotary_pin_2)

#Dial Button
button = DigitalInOut(button_pin)
button.direction = Direction.INPUT
button.pull = Pull.UP

def test1():
    """check rotary encoder function"""
    last_pos = None
    while True:
        pos = dial.position
        if last_pos is None or pos != last_pos:
            print(pos)
        last_pos = pos

def test2():
    """check button function"""
    while True:
        if button.value is False:
            print('pushed')
            sleep(.25)

def turn_white():
        color = fancy.gamma_adjust(fancy.CHSV(1.0, 0, 1.0))
        np.fill(color.pack())
        np.write()

def flash_red():
        color = fancy.gamma_adjust(fancy.CHSV(1.0, 1.0, 1.0))
        np.fill(color.pack())
        np.write()
        sleep(.05)
        color = fancy.gamma_adjust(fancy.CHSV(0.0, 0.0, 1.0))
        np.fill(color.pack())
        np.write()
        sleep(.05)
        turn_white()

def turn_off():
    np.fill((0,0,0))
    np.write()

def random_initial_color():
    """creates a random intial hue for the lights"""
    random_hue = random.randint(0,100)/100
    color = fancy.gamma_adjust(fancy.CHSV(random_hue, 1.0, 1.0))
    np.fill(color.pack())
    np.write()
    return(random_hue)


def rotate_color():
    last_pos = 0
    while True:
        pos = dial.position
        if last_pos is None or pos != last_pos:
            H = pos/200
            color = fancy.gamma_adjust(fancy.CHSV(H, 1.0, 1.0))
            np.fill(color.pack())
            np.write()
            print(pos, H)
        last_pos = pos
        if button.value is False:
            sleep(.25)
            if button.value is False:
                turn_off()
                sleep(1.5)
            else:
                turn_white()
                sleep(1.5)


def main():
    random_initial_color()
    rotate_color()

main()
