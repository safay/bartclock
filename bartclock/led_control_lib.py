
# Modified from Adafruit Dot Star RGB LED strip test code.

import time

import numpy as np

from dotstar import Adafruit_DotStar

from time import sleep

numpixels = 60 # Number of LEDs in strip
datapin   = 23
clockpin  = 24

pretty_smooth = {'red':{'wl':17, 'h':0.25},
            'green':{'wl':7, 'h':0.25},
            'blue':{'wl':13, 'h':0.25}}

worm_glitch = {'red':{'wl':-5, 'h':0.25},
            'green':{'wl':7, 'h':0.25},
            'blue':{'wl':3, 'h':-0.25}}

candy_gradient = {'red':{'wl':-2, 'h':0.25},
            'green':{'wl':7, 'h':0.25},
            'blue':{'wl':5, 'h':0.25}}

pretty_stripes = {'red':{'wl':1.3, 'h':0.1},
            'green':{'wl':-1.1, 'h':0.1},
            'blue':{'wl':1, 'h':0.1}}

very_smooth = {'red':{'wl':17, 'h':0.25},
            'green':{'wl':11, 'h':0.25},
            'blue':{'wl':23, 'h':0.25}}


def init_strip(numpixels, datapin, clockpin):
    strip = Adafruit_DotStar(numpixels, datapin, clockpin)
    strip.begin()           # Initialize pins for output
    strip.setBrightness(64) # Limit brightness to ~1/4 duty cycle
    return strip

# Runs 10 LEDs at a time along strip, cycling through red, green and blue.
# This requires about 200 mA for all the 'on' pixels + 1 mA per 'off' pixel.

def rgb_runner_test():
    strip = init_strip(numpixels=numpixels, datapin=datapin, clockpin=clockpin)
    head  = 0               # Index of first 'on' pixel
    tail  = -10             # Index of last 'off' pixel
    color = 0xFF0000        # 'On' color (starts red)
    while True:                              # Loop forever
        strip.setPixelColor(head, color) # Turn on 'head' pixel
        strip.setPixelColor(tail, 0)     # Turn off 'tail'
        strip.show()                     # Refresh strip
        time.sleep(1.0 / 50)             # Pause 20 milliseconds (~50 fps)
        head += 1                        # Advance head position
        if(head >= numpixels):           # Off end of strip?
            head    = 0              # Reset to start
    color >>= 8              # Red->green->blue->black
    if(color == 0): color = 0xFF0000 # If black, reset to red
    tail += 1                        # Advance tail position
    if(tail >= numpixels): tail = 0  # Off end? Reset



def light_pixel(index, color, brightness):
    pass

# how would a bart strip look as an object?
# A strip has state.
# Lights should brighten and dim in a defined manner; take about 2 seconds for the transition.
# There should be an update method for the BartStrip
# When the update is received, A routine moves each pixel to its new value.
# The actual rate of updates is not significant.  Every 15 sec?  More than often enough.
# Curious to know how to peg a process to the internal clock.  Look into this.
# Ramp up to an arbitrary value.
# 20fps
# so it would look something like this:

def make_rgb_hex(red, green, blue):
    def _make_hex(input):
        out = hex(input)[2:]
        if len(out) == 1:
            out = "0" + out
        return out
    total = blue + (256 * green) + (256 * 256 * red)
    return total


def sine_modulate(wavelength, height, vector):
    # sinewave modulation of an array
    # in this application used to generate a new vector of one of the three colors (RGB) in the dotstar strip
    modulated_values = height * (np.sin(np.array(vector) / (wavelength * np.pi)) + 1)
    array_of_color_intensities = [int(round(x*255)) for x in modulated_values]
    return array_of_color_intensities


def increment_vector(vector, max=100):
    out_vector = []
    for v in vector:
        if v > max:
            out_vector.append(0)
        else:
            out_vector.append(v + 1)
    return out_vector


class BartStrip(object): # check to see how to inherit from the DotStar object...
    # Note: This is not the master controller.  It is the strip controller; keep its functionality limited so
    def __init__(self, numpixels, datapin, clockpin):
        self.strip = init_strip(numpixels=numpixels, datapin=datapin, clockpin=clockpin)
        self.led_ix = range(0, numpixels)

    def update(self, bartinfo):
        # simple implementation: take the bart API info and update the strip
        # example: {'message': None, 'times': {'Richmond': {'color': '#ff9933', 'times': ['15', '35', '57']},
        # 'Warm Springs': {'color': '#ff9933', 'times': ['15', '35', '55']}}}
        #int(color, 16)
        print bartinfo['times'].keys()




    def idle(self, settings=pretty_smooth, maxstep=60000):
        # This is a mode with pretty lights.  For testing and use when BART is not running.
        # How do we get in and out of this mode?  Do we need concurrency to check the BART API periodically?
        # I can imagine going into the mode with a while loop.  But then we need a way to break out.
        step = 0
        while True:
            sleep(0.2)
            # set the pixel colors
            frame = [x + step for x in self.led_ix]
            red = sine_modulate(settings['red']['wl'], settings['red']['h'], frame)
            green = sine_modulate(settings['green']['wl'], settings['green']['h'], frame)
            blue = sine_modulate(settings['blue']['wl'], settings['blue']['h'], frame)
            for ix, r, g, b in zip(self.led_ix, red, green, blue):
                color = make_rgb_hex(r, g, b)
                self.strip.setPixelColor(ix, color)
            # show the strip
            self.strip.show()
            if step <= maxstep:
                step += 1
            else:
                step = 0

