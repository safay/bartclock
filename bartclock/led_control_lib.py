# Modified from Adafruit Dot Star RGB LED strip test code.

import math
from time import sleep

import numpy as np
from dotstar import Adafruit_DotStar


def gamma_correct_vector(gamma):
    powers = [math.pow(x, gamma) for x in range(255)]
    gamma_corrected = [int(x * 255 / max(powers)) for x in powers]
    return gamma_corrected


def init_strip(numpixels, datapin, clockpin):
    strip = Adafruit_DotStar(numpixels, datapin, clockpin)
    strip.begin()           # Initialize pins for output
    strip.setBrightness(64)  # Limit brightness to ~1/4 duty cycle
    return strip


def sine_modulate(wavelength, height, vector):
    # sinewave modulation of an array
    # in this application used to generate a new vector of one of the three colors (RGB) in the dotstar strip
    modulated_values = height * (np.sin(np.array(vector) / (wavelength * np.pi)) + 1)
    array_of_color_intensities = [int(round(x * 255)) for x in modulated_values]
    return array_of_color_intensities


def increment_vector(vector, maximum=100):
    out_vector = []
    for v in vector:
        if v > maximum:
            out_vector.append(0)
        else:
            out_vector.append(v + 1)
    return out_vector


class BartStrip(object):  # check to see how to inherit from the DotStar object...
    # Note: This is not the master controller.  It is the strip controller; keep its functionality limited so
    def __init__(self, numpixels, datapin, clockpin, gamma):
        self.strip = init_strip(numpixels=numpixels, datapin=datapin, clockpin=clockpin)
        self.led_ix = range(0, numpixels)
        self.gamma = gamma_correct_vector(gamma)

    def update(self, bartinfo):
        """
        take the bart API info (as bartinfo) and update the strip
        """
        print bartinfo

        def _rgb_tuple_color(info, _station):
            # returns a gamma-corrected tuple of rgb colors given bartinfo and station
            basecolor = info.get('times').get(_station).get('color')[1:]
            r = basecolor[0:2]
            g = basecolor[2:4]
            b = basecolor[4:6]
            return self.gamma[int(g, 16) - 1], self.gamma[int(r, 16) - 1], self.gamma[int(b, 16) - 1]
        for i in self.led_ix:
            self.strip.setPixelColor(i, 0, 0, 0)  # set all pixels to black
        for station in bartinfo.get('times').keys():
            color = _rgb_tuple_color(bartinfo, station)
            for t in bartinfo.get('times').get(station).get('times'):
                try:
                    self.strip.setPixelColor(int(t) - 1, color[0], color[1], color[2])
                except ValueError:
                    print "Error, time = {}".format(t)
        self.strip.show()

    def idle(self, mode, maxstep=60000):
        # This is a mode with pretty lights.  For testing and use when BART is not running.
        # How do we get in and out of this mode?  Do we need concurrency to check the BART API periodically?
        # I can imagine going into the mode with a while loop.  But then we need a way to break out.
        step = 0
        while True:
            sleep(0.2)
            frame = [x + step for x in self.led_ix]
            red = sine_modulate(mode['red']['wl'], mode['red']['h'], frame)
            green = sine_modulate(mode['green']['wl'], mode['green']['h'], frame)
            blue = sine_modulate(mode['blue']['wl'], mode['blue']['h'], frame)
            for ix, r, g, b in zip(self.led_ix, red, green, blue):
                self.strip.setPixelColor(ix, self.gamma[g - 1], self.gamma[r - 1], self.gamma[b - 1])
            self.strip.show()
            if step <= maxstep:
                step += 1
            else:
                step = 0
