import os
import sys
import vlc
import pygame as pg
import time

vlcInstance = vlc.Instance()


def initVLC():

    # Create new instance of vlc player
    player = vlcInstance.media_player_new()
    # Add a callback
    em = player.event_manager()
    #em.event_attach(vlc.EventType.MediaPlayerTimeChanged, callback, player)

    # Pass pygame window id to vlc player, so it can render its contents there.
    win_id = pg.display.get_wm_info()['window']
    # Pass pygame window id to vlc player, so it can render its contents there.
    player.set_xwindow(win_id)

    return(vlcInstance, player)


def playVLC(player, movie):

    media = vlcInstance.media_new(movie)

    # Load movie into vlc player instance
    player.set_media(media)
    #	 print(state)

    return(player)


def main():
	pg.init()
	# width = 1920//2
	# height = 1080//2
	# display = (1920//2,1080//2)
	# movie = "videos/beeShort.mp4"

	# pg.display.set_mode((width, height), pg.RESIZABLE)
	pg.display.toggle_fullscreen()

    # Create instane of VLC and create reference to movie.
	vlcInstance, player = initVLC()
	player = playVLC(player, "videos/beeLong.mp4")

	# Quit pygame mixer to allow vlc full access to audio device (REINIT AFTER MOVIE PLAYBACK IS FINISHED!)
	pg.mixer.quit()
	print("here")

	player.audio_set_volume(100)
	vlc.PlaybackMode.loop
	player.play()
	time.sleep(100)
	player.stop()

	while True:
		print(player.get_time())


main()

pg.quit()
