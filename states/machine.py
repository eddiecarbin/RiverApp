from relaycontroller import RelayController
from relaycontroller import RelayState
from movieplayer import MoviePlayer

class Stage():
    BUSY = 0
    READY = 1

class Machine():

    appData = None

    defaultState = None

    states = {}

    _currentState = None

    _previousState = None

    _setNewState = False

    def addState(self, name, state):
        self.states[name] = state
        state.stateMachine = self
        return self

    def getState(self, name):
        return self.states[name]

    def getCurrentState(self):
        return self._currentState

    def update(self):
        self._setNewState = False
        # DefaultState - we get it f no state is set.
        if (self._currentState == None and self.defaultState):
            self.setCurrentState(self.defaultState)

        if (self._currentState):
            self._currentState.update()

        # If didn't set a new state, it counts as transitioning to the
        # current state. This updates prev/current state so we can tell
        # if we just transitioned into our current state.
        if (self._setNewState == False and self._currentState):
            self._previousState = self._currentState

    def setCurrentState(self, name):
        _newState = self.getState(name)

        if (_newState == self._currentState):
            return False

        if (_newState == None):
            print("Can not find state:" + name)

        oldState = self._currentState
        self._setNewState = True

        self._previousState = self._currentState
        self._currentState = _newState

        # Old state gets notified it is changing out.
        if (oldState):
            oldState.exit()

        # New state finds out it is coming in.
        _newState.enter()

        return True

    def destroy(self):
        if (self._currentState):
            self._currentState.exit()

class CommandEnums():
    RIVERS = "rivers"
    RELAY = "relay"
    OLD = "old"

class State():

    stateMachine = None

    def __init__(self, name, data, player, led, relays):
        self._name = name
        self.data = data
        self.moviePlayer = player
        self.ledController = led
        self.relayList = relays

    def name(self):
        return self._name

    def handleMovieTrigger(self, eve):
        for action in eve:
            task = action.actions
            print ( task )
            if action.command == CommandEnums.RELAY :
                relayID = task["relayID"]
                state = task["state"] 
                if state == 1:
                    state = RelayState.ON
                else:
                    state = RelayState.OFF

                self.relayList[relayID].state(state)

            if action.command == CommandEnums.RIVERS :
                riverList = task["riverID"]
                if len(riverList) == 0:
                    self.ledController.stop()
                else:
                    systems = self.stateMachine.appData["systems"]
                    color = task["color"]
                    for name in riverList:
                        rivers = systems[name]
                        for river in rivers:
                            self.ledController.activateRivers(river, color)

    def handleMovieExit(self, eve=None):

        for relay in self.relayList:
            relay.state(RelayState.OFF)

        self.ledController.stop()
        
        self.moviePlayer.remove_listener(
            MoviePlayer.MOVIE_EXIT_EVENT, self.handleMovieExit)

        self.stateMachine.setCurrentState(InactiveState.NAME)


    def enter(self):
        self._stage = Stage.BUSY
        self.ledController.reset()

        self.moviePlayer.play(self.data["movie"])
        self.moviePlayer.add_listener(MoviePlayer.MOVIE_EXIT_EVENT, self.handleMovieExit)
        self.moviePlayer.add_listener(MoviePlayer.MOVIE_TRIGER_EVENT, self.handleMovieTrigger)
        
        self.moviePlayer.addTriggers(self.data["triggers"])

    def exit(self):

        self.moviePlayer.pause()
        self.ledController.stop()
        
        for relay in self.relayList:
            relay.state(RelayState.OFF)

        self._stage = Stage.BUSY
        self.moviePlayer.remove_listener( MoviePlayer.MOVIE_EXIT_EVENT, self.handleMovieExit)
        self.moviePlayer.remove_listener( MoviePlayer.MOVIE_TRIGER_EVENT, self.handleMovieTrigger)
        


    def update(self):
        self.ledController.update()
        self.moviePlayer.update()

    def stage(self):
        return self._stage

class InactiveState(State):

    NAME = "InactiveState"

    def __init__(self):
        super().__init__( self.NAME, None, None, None, None )

    def update(self):
        pass

    def enter(self):
        pass

    def exit(self):
        pass

class StartupState(State):

    NAME = "StartupState"

    def __init__(self, player, led, relays, data):
        super().__init__(self.NAME, data, player, led, relays)
