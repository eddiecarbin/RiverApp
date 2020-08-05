from pyjon.events import EventDispatcher
# import RPi.GPIO as gpio
import digitalio
from adafruit_debouncer import Debouncer

#https://pypi.org/project/pyjon.events/

class ButtonController(metaclass=EventDispatcher):
    BUTTON_EVENT = "ButtonController_buttonEvent"

    def __init__(self, pin, id):
        # just a sample initialization, you can do whatever you want, of course.
        self.id = id
        self.pin = pin

        self.button = digitalio.DigitalInOut(self.pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP
        self.switch = Debouncer(self.button, interval=0.1)

    def update(self):
        self.switch.update()
        if self.switch.rose:
            self.emit_event(ButtonController.BUTTON_EVENT, self.id)
            # print('Just released')
            
