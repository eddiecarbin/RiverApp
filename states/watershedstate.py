
from states.machine import State

class WatershedState (State):

    NAME = "WatershedState"

    def __init__(self, player, led, relays, data):
        super().__init__(self.NAME, data, player, led, relays)
