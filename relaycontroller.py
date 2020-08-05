from pyjon.events import EventDispatcher
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

class RelayState:
    OFF = 0
    ON = 1

class RelayController(metaclass=EventDispatcher):

    def __init__(self, channel):
        self._channel = channel
        GPIO.setup(channel, GPIO.OUT)
        GPIO.output(self._channel, GPIO.HIGH)
        # self.relay = GPIO(self._channel, GPIO.OUT, initial=GPIO.LOW)

    def state(self, value):
        #print("something calling me")
        #raise Exception("Sorry, no numbers below zero")
        if (value == RelayState.ON):
            GPIO.output(self._channel, GPIO.LOW)
        else:
            GPIO.output(self._channel, GPIO.HIGH)

    def destroy(self):
        GPIO.output(self._channel, GPIO.HIGH)

