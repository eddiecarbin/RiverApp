import adafruit_fancyled.adafruit_fancyled as fancy
import board
import adafruit_dotstar

# https://readthedocs.org/projects/adafruit-circuitpython-dotstar/downloads/pdf/latest/


class LEDController:

    activeRivers = []

    riverMap = []

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
 
    palette = [
        fancy.CRGB(0.0, 0.5, 0.5),  # Cyan
        fancy.CRGB(0.0, 0.0, 1.0),  # Blue
        fancy.CRGB(0.0, 0.0, 0.0)]  # off

    spread = 5

    isPlaying = False

    def __init__(self, t):
        self.totalled = t
        self.ledStrip = adafruit_dotstar.DotStar(board.SCK, board.MOSI, self.totalled, brightness=1,
                                                 auto_write=False)
        self.ledStrip.fill(fancy.CRGB(0.0, 0.0, 0.0))
        self.ledStrip.show()

    def buildRivers(self, riverslist):
        self.riverMap = []

        for river in riverslist:
            efx = RiverLEDEfx(river["id"], river["led"][0], river["led"][1], river["dir"])
            self.riverMap.append(efx)

    def activateRivers(self, name, color="blue"):
        self.isPlaying = True
        river = self.getRiverByName(name)
        river.color = color
        if (river):
            self.activeRivers.append(river)
        # add deactive rivers here
        return river

    def getRiverByName(self, id):
        for river in self.riverMap:
            if (river.getName() == id):
                return river

    def reset(self):
        self.activeRivers = []
        self.stop()

    def stop(self):
        self.isPlaying = False
        self.activeRivers = []
        self.ledStrip.fill(fancy.CRGB(0.0, 0.0, 0.0))
        self.ledStrip.show()
 
    def play(self):
        self.isPlaying = True

    def update(self):

        if (self.isPlaying == False):
            return
            
        for effect in self.activeRivers:
            total = effect.total()
            start = effect.start()
            dir = effect.direction()
            palette = self.colorPalettes[effect.color]
            for i in range(total):
                color = fancy.palette_lookup(
                    palette, effect.offset() + (i / self.spread) * dir)
                color = fancy.gamma_adjust(color, brightness=0.8)
                self.ledStrip[start + i] = color.pack()

            effect.setOffset(effect.offset() + 0.1)

        self.ledStrip.show()

    def destroy(self):
        self.ledStrip.fill(fancy.CRGB(0.0, 0.0, 0.0))
        self.ledStrip.show()
        self.ledStrip.deinit()


class RiverLEDEfx:

    # offset = 0
    _offset = 0

    color = "blue"

    def __init__(self, name, start, end, dir):
        self.name = name
        self._start = start
        self._end = end
        self._direction = dir
        self.switch = 0

    def start(self):
        return self._start

    def offset(self):
        return self._offset

    def direction(self):
        if (self.switch > 0):
            return -self._direction

        return self._direction

    def setOffset(self, value):
        self._offset = value

    def getName(self):
        return self.name

    def total(self):
        return self._end - self._start
