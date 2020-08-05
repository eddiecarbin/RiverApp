#!/usr/bin/env python3

#
#https://python-omxplayer-wrapper.readthedocs.io/en/latest/omxplayer/
from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep

VIDEO_PATH = Path("videos/beeLong.mp4")

player = OMXPlayer(VIDEO_PATH)

sleep(5)

player.pause()
player.load("videos/Test0.mp4")
sleep(10)
player.quit()