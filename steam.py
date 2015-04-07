#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import os, tarfile, urllib.request
from subprocess import call

def steamcmd(user, s_appid, engineer_dir, game_data_dir):
	if os.path.isdir(engineer_dir) == False:
		os.makedirs(engineer_dir)
	os.chdir(engineer_dir)
	if os.path.isfile(engineer_dir+"steamcmd.sh") == False:
		urllib.request.urlretrieve("http://media.steampowered.com/client/steamcmd_linux.tar.gz", engineer_dir + "steamcmd_linux.tar.gz")
		tar = tarfile.open(engineer_dir + "steamcmd_linux.tar.gz")
		tar.extractall()
		tar.close()
	print(user)
	if os.path.isdir(game_data_dir) == False:
		s_download = call("x-terminal-emulator -e './steamcmd.sh +@sSteamCmdForcePlatformType windows +login " + user + " +force_install_dir " + game_data_dir + " +app_update " + s_appid + " validate +quit'", shell=True)
