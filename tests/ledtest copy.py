import adafruit_fancyled.adafruit_fancyled as fancy
import board
import adafruit_dotstar
import time

num_leds = 1085
spread = 5

# Declare a 6-element RGB rainbow palette
palette = [
           fancy.CRGB(0.0, 0.5, 0.5), # Cyan
           fancy.CRGB(0.0, 0.0, 1.0), # Blue
           fancy.CRGB(0.0, 0.0, 0.0)] # off


colorPalettes  = { 
        "blue": [
        fancy.CRGB(0.0, 0.5, 0.5),  # Cyan
        fancy.CRGB(0.0, 0.0, 1.0),  # Blue
        fancy.CRGB(0.0, 0.0, 0.0)],  # off

        "magenta" : [
        fancy.CRGB(0.8, 0.0, 0.4),  # Magenta
        fancy.CRGB(1.0, 0.0, 1.0),  # Pink
        fancy.CRGB(0.0, 0.0, 0.0)],  # off

        "yellow" : [
        fancy.CRGB(1.0, 1.0, 0.0),  # Yellow
        fancy.CRGB(1.0, 1.0, 1.0),  # White
        fancy.CRGB(0.0, 0.0, 0.0)]  # off

    }

_palette = colorPalettes["yellow"]
# Declare a NeoPixel object on pin D6 with num_leds pixels, no auto-write.
# Set brightness to max because we'll be using FancyLED's brightness control.

pixels = adafruit_dotstar.DotStar(board.SCK, board.MOSI, num_leds, brightness=1.0,
                           auto_write=False)

offset = 0  # Positional offset into color palette to get it to 'spin'

pixels.fill(fancy.CRGB(0.0, 0.0, 0.0))
pixels.show()

time.sleep(3)

# pixels.

while True:
#     for i in range(num_leds, 0, -1):
    for i in range(num_leds):
        # Load each pixel's color from the palette using an offset, run it
        # through the gamma function, pack RGB value and assign to pixel.
        color = fancy.palette_lookup(_palette, offset - i / spread)
        color = fancy.gamma_adjust(color, brightness=0.99)
        pixels[i] = color.pack()
        
    pixels.show()

    offset += 0.01  # Bigger number = faster spin
    