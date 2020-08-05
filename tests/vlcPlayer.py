import os
import sys
import vlc
import time
from time import sleep

instance = vlc.Instance()
player = instance.media_player_new()
# media = vlc.media_new("videos/beeLong.mp4")

media = instance.media_new("videos/beeLong.mp4")
# player = vlc.MediaPlayer("videos/beeLong.mp4")
player.set_media(media)

player.play()
sleep(5)
player.stop()

media = instance.media_new("videos/Test0.mp4")
# player = vlc.MediaPlayer("videos/beeLong.mp4")
player.set_media(media)

player.play()
sleep(5)


# player = vlc.MediaPlayer("videos/Test0.mp4")


# media = vlc.media_new("videos/Test0.mp4")

# Load movie into vlc player instance
# player.set_media(media)

# player.play()
sleep(100)
