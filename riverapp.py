import time
import board
import json
import RPi.GPIO as GPIO
import atexit

from time import sleep

from states.machine import Machine, InactiveState, StartupState
from ledcontroller import LEDController
from buttoncontroller import ButtonController
from states.vitalconnectionstate import VitalConnectionState
from states.nowandthenstate import NowAndThenState
from states.riversoflifestate import RiversOfLifeState
from states.watershedstate import WatershedState
from movieplayer import MoviePlayer
from relaycontroller import RelayController

GPIO.setmode(GPIO.BCM)

relayList = [RelayController(20), RelayController(26)]

vitalConnectionButton = ButtonController(board.D23, VitalConnectionState.NAME)
watershedButton = ButtonController(board.D22, WatershedState.NAME)
thenAndNowButton = ButtonController(board.D27, NowAndThenState.NAME)
riversOfLifeButton = ButtonController(board.D17, RiversOfLifeState.NAME)

riverStateMachine = Machine()
moviePlayer = None

# https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/
# black log in screen
# https://www.raspberrypi.org/forums/viewtopic.php?t=228394


def main():

    #print(GPIO.RPI_INFO)
    with open('/home/pi/riverapp/riverdata.json') as f:
        appData = json.load(f)

    #print(appData)

    riverStateMachine.appData = appData
    
    ledController = LEDController(appData["totalLeds"])
    ledController.buildRivers(appData["allRivers"])
    moviePlayer = MoviePlayer(appData['volume'])

    vitalConnectionButton.add_listener(ButtonController.BUTTON_EVENT, handleEvent)
    watershedButton.add_listener(ButtonController.BUTTON_EVENT, handleEvent)
    thenAndNowButton.add_listener(ButtonController.BUTTON_EVENT, handleEvent)
    riversOfLifeButton.add_listener( ButtonController.BUTTON_EVENT, handleEvent)

    riverStateMachine.addState(InactiveState.NAME, InactiveState() )
    riverStateMachine.addState(StartupState.NAME, StartupState( moviePlayer, ledController, relayList, getSceneByName(StartupState.NAME, appData["scene"])))
    riverStateMachine.addState(VitalConnectionState.NAME, VitalConnectionState( moviePlayer, ledController, relayList, getSceneByName(VitalConnectionState.NAME, appData["scene"])))
    riverStateMachine.addState(WatershedState.NAME, WatershedState( moviePlayer, ledController, relayList, getSceneByName(WatershedState.NAME, appData["scene"])))
    riverStateMachine.addState(NowAndThenState.NAME, NowAndThenState( moviePlayer, ledController, relayList, getSceneByName(NowAndThenState.NAME, appData["scene"])))
    riverStateMachine.addState(RiversOfLifeState.NAME, RiversOfLifeState( moviePlayer, ledController, relayList, getSceneByName(RiversOfLifeState.NAME, appData["scene"])))

    riverStateMachine.setCurrentState(StartupState.NAME)

    while True:
        vitalConnectionButton.update()
        watershedButton.update()
        thenAndNowButton.update()
        riversOfLifeButton.update()

        riverStateMachine.update()

        sleep(0.001)


def handleEvent(state):
    print(state)
    riverStateMachine.setCurrentState(state)


def getSceneByName(id, list):

    for i in list:
        if i["name"] == id:
            return i
    return None

# https://pymotw.com/2/atexit/

# register function call to clean up on close

def onQuit():
    for relay in relayList:
        relay.destroy()
    riverStateMachine.destroy()
    #GPIO.cleanup()

atexit.register(onQuit)

main()
