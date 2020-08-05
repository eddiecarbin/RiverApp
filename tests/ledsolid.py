import adafruit_fancyled.adafruit_fancyled as fancy
import board
import adafruit_dotstar
import time

num_leds = 1085
spread = 5

# Declare a NeoPixel object on pin D6 with num_leds pixels, no auto-write.
# Set brightness to max because we'll be using FancyLED's brightness control.

pixels = adafruit_dotstar.DotStar(board.SCK, board.MOSI, num_leds, brightness=1.0,
                                  auto_write=False)

offset = 0  # Positional offset into color palette to get it to 'spin'


blue = fancy.CRGB(0.0, 0.0, 1.0)  # Blue
red = fancy.CRGB(1.0, 0.0, 1.0)  # Pink
yellow = fancy.CRGB(1.0, 1.0, 0.0)  # Yellow

pixels.fill((0.0, 0.0, 1.0) )
pixels.show()

time.sleep(3)

# pixels.

while True:
    pass
    #pixels.show()
