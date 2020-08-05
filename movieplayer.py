from omxplayer.player import OMXPlayer
from pathlib import Path
from pyjon.events import EventDispatcher

# https://python-omxplayer-wrapper.readthedocs.io/en/latest/omxplayer/
# https://www.raspberrypi.org/forums/viewtopic.php?t=228394

# https://raspberrypi.stackexchange.com/questions/3268/how-to-disable-local-terminal-showing-through-when-playing-video
# https://pypi.org/project/pyjon.events/


class MoviePlayer(metaclass=EventDispatcher):

    # Evemts
    MOVIE_STOP_EVENT = "MoviePlayer:Stop"
    MOVIE_START_EVENT = "MoviePlayer:Start"
    MOVIE_TRIGER_EVENT = "MoviePlayer:Trigger"
    MOVIE_PLAY_EVENT = "MoviePlayer:Play"
    MOVIE_EXIT_EVENT = "MoviePlayer:Exit"

    player = None

    isPlaying = False

    _triggers = []

    def __init__(self, volume=4):
        self.volume = volume

    def play(self, url, loop=False):
        self.path = Path(url)
        self._triggers = []

        if (self.player == None):
            #, '--vol', '0'
            props = ['--no-osd', '--no-keys']

            if (loop):
                props.append('--loop')

            self.player = OMXPlayer(self.path, args=props)
            # self.player.pauseEvent += lambda _: player_log.info("Pause")
            # self.player.playEvent += lambda _: player_log.info("Play")
            self.player.exitEvent += lambda _, exit_code: self.handleExit(
                exit_code)
            
        else:
            self.player.load(self.path)

        self.isPlaying = True
        

    def handleExit(self, eve):
        self.isPlaying = False
        self.emit_event(MoviePlayer.MOVIE_EXIT_EVENT)

    def addTriggers(self, triggers):
        self._triggers = []

        if (len(triggers) > 0):
            for trigger in triggers:
                self._triggers.append(
                    Trigger(trigger["time"], trigger["actions"]))

    def update(self):
        try:
            if (self.isPlaying == True and self.player != None and len(self._triggers) > 0 and self.player.is_playing() == True):
                frame = self.player.position()
                for t in self._triggers:
                    if(frame >= t.frame):
                        self._triggers.remove(t)
                        self.emit_event(MoviePlayer.MOVIE_TRIGER_EVENT, t.actions)
        except:
            pass
        
        
    def pause(self):
        self.isPlaying = False

    def stop(self):
        self.isPlaying = False
        self._triggers = []
        try:
            self.player.stop()
            self.player = None
        except ValueError:
            print("Oops!  That was no valid number.  Try again...")

    def destroy(self):
        self.player.quit()
        self.player = None
        self._triggers = []


class Trigger():
    def __init__(self, frame, actions):
        self.frame = frame
        self.actions = []
        for action in actions :
            self.actions.append( Action(action["command"], action) )

class Action():

    def __init__(self, command, actions):
        self.command = command
        self.actions = actions
