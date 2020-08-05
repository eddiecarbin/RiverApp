from states.machine import State

class NowAndThenState (State):

    NAME = "NowAndThenState"

    def __init__(self, player, led, relays, data):
        super().__init__(self.NAME, data, player, led, relays)
      