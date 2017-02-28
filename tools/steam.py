#!/usr/bin/env python3
#-*- coding: utf-8 -*-

##This software is available to you under the terms of the GPL-3, see "/usr/share/common-licenses/GPL-3".
##Copyright:
##- Tomasz Makarewicz (makson96@gmail.com)

import os, tarfile, urllib.request, pickle
from subprocess import call

start(login, password, engineer_dir, s_appid, game_dir):
	status = "Downloading and installing game data"
	percent = 90
	pickle.dump([status, percent], open(engineer_dir+"status_list.p", "wb"))
	os.chdir(engineer_dir)
	if os.path.isfile(engineer_dir+"steamcmd.sh") == False:
		urllib.request.urlretrieve("http://media.steampowered.com/client/steamcmd_linux.tar.gz", engineer_dir + "steamcmd_linux.tar.gz")
		tar = tarfile.open(engineer_dir + "steamcmd_linux.tar.gz")
		tar.extractall()
		tar.close()
	if os.path.isfile(engineer_dir+"steam_log.txt") == True:
		os.remove(engineer_dir+"steam_log.txt")
	s_download = call("./steamcmd.sh +@sSteamCmdForcePlatformType windows +login " + login + " " + password + " +force_install_dir " + game_dir + " +app_update " + s_appid + " validate +quit > steam_log.txt", shell=True)
	status = "Finalising Installation"
	percent = 95
	pickle.dump([status, percent], open(engineer_dir+"status_list.p", "wb"))
