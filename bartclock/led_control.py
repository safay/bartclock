#!/usr/bin/python

# Simple strand test for Adafruit Dot Star RGB LED strip.
# This is a basic diagnostic tool, NOT a graphics demo...helps confirm
# correct wiring and tests each pixel's ability to display red, green
# and blue and to forward data down the line.  By limiting the number
# and color of LEDs, it's reasonably safe to power a couple meters off
# USB.  DON'T try that with other code!

import time
from dotstar import Adafruit_DotStar


def init_strip(numpixels, datapin, clockpin):
    

numpixels = 60 # Number of LEDs in strip
datapin   = 23
clockpin  = 24
strip     = Adafruit_DotStar(numpixels, datapin, clockpin)
strip.begin()           # Initialize pins for output
strip.setBrightness(64) # Limit brightness to ~1/4 duty cycle
return strip

# Runs 10 LEDs at a time along strip, cycling through red, green and blue.
# This requires about 200 mA for all the 'on' pixels + 1 mA per 'off' pixel.

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
